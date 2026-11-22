const { createApp, ref, reactive, onMounted, computed, watch, nextTick } = Vue;

const savedLanguage = localStorage.getItem('pgvz-gui-language');
const initialLanguage = savedLanguage || ((navigator.language || '').toLowerCase().startsWith('en') ? 'en' : 'zh');
const i18n = PGvZI18n.createI18n(initialLanguage);

const { readCheckboxState, writeCheckboxState, savedBoolean } = PGvZOptions;

function gameVersionParts(version) {
    return /^(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$/.exec(version)?.slice(1).map(Number);
}

const SwitchRow = {
    props: {
        label: { type: String, required: true },
        modelValue: { type: Boolean, required: true },
    },
    emits: ['update:modelValue', 'change'],
    template: `
        <div class="switch-row">
            <span>{{ label }}</span>
            <el-switch
                :model-value="modelValue"
                @update:model-value="$emit('update:modelValue', $event)"
                @change="$emit('change', $event)"
            />
        </div>
    `,
};

const CheckGroupCard = {
    props: {
        title: { type: String, required: true },
        items: { type: Array, required: true },
        model: { type: Object, required: true },
        label: { type: Function, required: true },
    },
    template: `
        <el-card shadow="never" class="tool-card">
            <template #header>{{ title }}</template>
            <div class="form-stack">
                <div class="option-check-grid">
                    <el-checkbox
                        v-for="key in items"
                        :key="key"
                        :model-value="model[key]"
                        @update:model-value="model[key] = $event"
                    >
                        {{ label(key) }}
                    </el-checkbox>
                </div>
                <slot></slot>
            </div>
        </el-card>
    `,
};

const app = createApp({
    components: {
        SwitchRow,
        CheckGroupCard,
    },
    setup() {
        const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
        // 手机端始终以游戏内状态为准；PC 端才从 localStorage 恢复并推送状态。
        const savedCheckboxState = isMobile ? null : readCheckboxState();
        const savedCheatState = savedCheckboxState && savedCheckboxState.cheat;
        const savedPlacerState = savedCheckboxState && savedCheckboxState.placer;
        const {
            seedTypes,
            zombieTypes,
            setZombieTypes,
            selectRows,
            selectCols,
            packetIdx,
            gridItemTypes,
            easyPlaceModeList,
            scaryPotType,
            scaryPotAppearance,
            coinTypes,
            gameModes,
            lineupCodeMap,
        } = PGvZData;

        const { language, setLanguage, t, optionLabel } = i18n;
        const languageOptions = computed(() => [
            { label: '中文', value: 'zh' },
            { label: 'English', value: 'en' },
        ]);

        const activeTab = ref('player');
        const speedControls = reactive([
            { scope: 'global', action: 'setGlobalSpeed', presets: ['0.1', '0.2', '0.5', '1', '2', '5', '10'] },
            { scope: 'board', action: 'setBoardSpeed', presets: ['0.5', '1', '2', '3'] },
        ].map(control => ({ ...control, current: null, draft: '', pending: null, errorKey: '' })));
        const weather = ref('default');
        const weatherOptions = computed(() => [
            { label: t('weather.default'), value: 'default' },
            { label: t('weather.sunny'), value: 'sunny' },
            { label: t('weather.rain'), value: 'rain' },
            { label: t('weather.storm'), value: 'storm' },
            { label: t('weather.rainStorm'), value: 'rainStorm' },
        ]);

        const sunValue = ref(9990);
        const moneyValue = ref(999999);
        const chocolateValue = ref(999);
        const treeHeight = ref(1000);
        const level = ref(1);
        const finishedAdventure = ref(2);
        const numSurvivalStage = ref(2000);
        const coinX = ref(400);
        const coinY = ref(300);
        const selectedSeedType = ref(seedTypes[0].value);
        const selectedZombieType = ref(zombieTypes[0].value);
        const selectedPacketIdx = ref(packetIdx[0].value);
        const selectedLevel = ref(gameModes[0].value);
        const selectedGridItem = ref(gridItemTypes[2].value);
        const selectedCoin = ref(coinTypes[0].value);
        const selectedRow = ref(-1);
        const selectedCol = ref(-1);
        const selectedScaryPotType = ref(scaryPotType[1].value);
        const selectedScaryPotAppearance = ref(scaryPotAppearance[0].value);
        const isImitater = ref(savedBoolean(savedPlacerState, 'imitater', false));
        const mindCtrl = ref(savedBoolean(savedPlacerState, 'mindCtrl', false));
        const potLeft = ref(savedBoolean(savedPlacerState, 'potReverse', false));
        const lastResult = reactive({ ok: true, key: 'messages.waiting', text: '' });
        const resultText = computed(() => lastResult.key ? t(lastResult.key) : lastResult.text);
        const customCode = ref('');
        const customCodeError = ref('');
        const lineupCode = ref('');
        const selectedSetZbType = ref([]);
        const selectedScene = ref('pool');
        const selectedLineUp = ref('');
        const easyPlaceMode = ref('plant');
        const easyPlaceEnabled = ref(savedBoolean(savedPlacerState, 'easyPlaceEnabled', true));

        const { switchGroups, optionConfig, cheatOption } = PGvZOptions.createCheatOptions(savedCheatState, isMobile);

        watch(() => cheatOption.noSunLimit, enabled => {
            if (!enabled && sunValue.value > 9990) sunValue.value = 9990;
        });

        const scenes = computed(() => [
            { label: t('scene.day'), value: 'day' },
            { label: t('scene.night'), value: 'night' },
            { label: t('scene.pool'), value: 'pool' },
            { label: t('scene.fog'), value: 'fog' },
            { label: t('scene.roof'), value: 'roof' },
            { label: t('scene.moon'), value: 'moon' },
        ]);

        const currentLineupList = computed(() => lineupCodeMap[selectedScene.value] || []);

        let applyingRemoteState = false;
        let syncedWeather = { enabled: false, rain: false, storm: false };
        const terrain = PGvZTerrain.create({ sendAction: (...args) => sendAction(...args) });
        const {
            connected, sessionRejected, unsupportedGameVersion, supportedGameVersions,
            gameVersion, modVersion, connectionState,
            pendingCount, hasUnconfirmedRequests,
            send, sendAction, applyState, connect, releaseSession, takeoverSession,
        } = PGvZConnection.create({
            isMobile, t, setResult, getInitialState, applySyncState, lineupCode,
            onActionResult,
        });
        watch(() => connected.value, ready => {
            if (ready) return;
            terrain.reset();
            for (const control of speedControls) {
                control.current = null;
                control.pending = null;
                control.errorKey = '';
            }
        });

        function speedIsValid(speed) {
            return speed && speed.numerator >= 0 && speed.denominator > 0;
        }

        function currentSpeedLabel(control) {
            const speed = control.current;
            if (!connected.value) return '—';
            if (control.scope === 'board' && !speed) return t('speed.noBoard');
            if (!speedIsValid(speed)) return t('speed.unavailable');
            const { numerator, denominator } = speed;
            return numerator === 0 || denominator === 1 ? `${numerator}×` : `${numerator}/${denominator}×`;
        }

        function speedPresetSelected(control, preset) {
            const speed = control.current;
            return Boolean(speedIsValid(speed) && speed.numerator / speed.denominator === Number(preset));
        }

        const combinedSpeed = computed(() => {
            const [global, board] = speedControls.map(control => control.current);
            if (!connected.value || !speedIsValid(global) || !speedIsValid(board)) return '';
            const product = (global.numerator * board.numerator) / (global.denominator * board.denominator);
            const displayed = Number(product.toPrecision(7));
            return `${product === displayed ? '' : '≈'}${displayed}×`;
        });

        function speedControlDisabled(control) {
            return !connected.value || Boolean(control.pending) || (control.scope === 'board' && !control.current);
        }

        function applySpeed(control, preset) {
            const value = preset ?? control.draft.trim();
            if (speedControlDisabled(control) || !value) return;
            if (preset !== undefined && speedPresetSelected(control, preset)) return;
            const args = control.scope === 'board' ? { value, boardId: control.current.id } : { value };
            control.errorKey = '';
            control.pending = { draft: preset === undefined ? control.draft : null };
            if (!sendAction(control.action, args)) control.pending = null;
        }

        function onActionResult(result) {
            terrain.receive(result);
            const control = speedControls.find(item => item.action === result.name);
            if (!control?.pending) return;
            if (result.ok && control.draft === control.pending.draft) control.draft = '';
            control.pending = null;
            if (result.ok || result.errortype === 'SessionRejected') return;
            const errorKey = {
                InvalidSpeed: `speed.${control.scope}.invalid`,
                SpeedBoardChanged: 'speed.board.changed',
            }[result.errortype];
            control.errorKey = errorKey ?? 'speed.failed';
            return errorKey;
        }

        function terrainTypeShort(kind, value) {
            const item = terrain.typeInfo(kind, value);
            return item ? (language.value === 'zh' ? item.short : item.code) : value;
        }

        function terrainCellLabel(kind, value, row, col) {
            const item = terrain.typeInfo(kind, value);
            const position = kind === 'grid' ? `${t('fields.row')} ${row + 1}, ${t('fields.col')} ${col + 1}` : `${t('fields.row')} ${row + 1}`;
            return `${position}: ${item ? dataLabel(item) : value}`;
        }
        const statusText = computed(() => t(`status.${connectionState.value}`));
        const unsupportedGameVersionDetail = computed(() => {
            if (!unsupportedGameVersion.value) return '';
            const versions = supportedGameVersions.value;
            const current = gameVersionParts(gameVersion.value);
            const newerThanSupported = current && versions.every(version => {
                const supported = gameVersionParts(version);
                if (!supported) return false;
                const difference = current[0] - supported[0] || current[1] - supported[1] || current[2] - supported[2];
                return difference > 0;
            });
            const advice = newerThanSupported ? 'downloadNewerMod' : 'updateGame';
            return t('messages.unsupportedGameVersionDetail')
                .replace('{versions}', versions.join(', '))
                .replace('{advice}', t(`messages.${advice}`));
        });

        function dataLabel(item) {
            if (language.value === 'zh') return item.label;
            return item.en || item.label;
        }

        function setResult(ok, key, text = '') {
            lastResult.ok = ok;
            lastResult.key = key;
            lastResult.text = text;
        }

        function setCheatOption(key, value) {
            applyState({ cheat: { [key]: value } });
        }

        function setPlacerOption(key, value) {
            applyState({ placer: { [key]: value } });
        }

        function setWeather(value) {
            const states = {
                default: { enabled: false, rain: false, storm: false },
                sunny: { enabled: true, rain: false, storm: false },
                rain: { enabled: true, rain: true, storm: false },
                storm: { enabled: true, rain: false, storm: true },
                rainStorm: { enabled: true, rain: true, storm: true },
            };
            applyState({ weather: states[value] });
        }

        function saveCheckboxState() {
            if (isMobile || applyingRemoteState) return;
            writeCheckboxState({
                cheat: { ...cheatOption },
                placer: {
                    imitater: isImitater.value,
                    mindCtrl: mindCtrl.value,
                    potReverse: potLeft.value,
                    easyPlaceEnabled: easyPlaceEnabled.value,
                },
            });
        }

        function getInitialState() {
            const placerUpdates = {
                seedType: selectedSeedType.value,
                zombieType: selectedZombieType.value,
                gridItemType: selectedGridItem.value,
                scaryPotType: selectedScaryPotType.value,
                scaryPotAppearance: selectedScaryPotAppearance.value,
                coinType: selectedCoin.value,
                mindCtrl: mindCtrl.value,
                potReverse: potLeft.value,
                imitater: isImitater.value,
                easyPlaceMode: easyPlaceMode.value,
                easyPlaceEnabled: easyPlaceEnabled.value,
            };
            return { cheat: { ...cheatOption }, placer: placerUpdates };
        }

        watch(
            () => ({ ...cheatOption }),
            (newVal, oldVal) => {
                if (applyingRemoteState) return;
                saveCheckboxState();
                for (const key in newVal) {
                    if (newVal[key] !== oldVal[key]) {
                        setCheatOption(key, newVal[key]);
                    }
                }
            },
            { deep: true }
        );

        watch(
            [isImitater, mindCtrl, potLeft, easyPlaceEnabled],
            saveCheckboxState
        );

        function applySyncState(state) {
            if (state.speed) {
                for (const control of speedControls) {
                    if (Object.prototype.hasOwnProperty.call(state.speed, control.scope)) {
                        control.current = state.speed[control.scope];
                    }
                }
            }
            if (!state.cheat && !state.placer && !state.weather) return;
            applyingRemoteState = true;
            if (state.cheat) {
                Object.keys(state.cheat).forEach(k => {
                    if (Object.prototype.hasOwnProperty.call(cheatOption, k)) cheatOption[k] = state.cheat[k];
                });
            }
            if (state.placer) {
                const p = state.placer;
                if (p.seedType) selectedSeedType.value = p.seedType;
                if (p.zombieType) selectedZombieType.value = p.zombieType;
                if (p.gridItemType) selectedGridItem.value = p.gridItemType;
                if (p.scaryPotType) selectedScaryPotType.value = p.scaryPotType;
                if (p.scaryPotAppearance) selectedScaryPotAppearance.value = p.scaryPotAppearance;
                if (p.coinType) selectedCoin.value = p.coinType;
                if (p.mindCtrl !== undefined) mindCtrl.value = p.mindCtrl;
                if (p.potReverse !== undefined) potLeft.value = p.potReverse;
                if (p.imitater !== undefined) isImitater.value = p.imitater;
                if (p.easyPlaceMode) easyPlaceMode.value = p.easyPlaceMode;
                if (p.easyPlaceEnabled !== undefined) easyPlaceEnabled.value = p.easyPlaceEnabled;
            }
            if (state.weather) {
                syncedWeather = { ...syncedWeather, ...state.weather };
                const w = syncedWeather;
                if (!w.enabled) weather.value = 'default';
                else if (w.rain && w.storm) weather.value = 'rainStorm';
                else if (w.rain) weather.value = 'rain';
                else if (w.storm) weather.value = 'storm';
                else weather.value = 'sunny';
            }
            nextTick(() => {
                applyingRemoteState = false;
                // 保存收到的状态，watch 不把远端同步当成本地操作。
                saveCheckboxState();
            });
        }

        function sendCustomCode() {
            if (!customCode.value.trim()) {
                customCodeError.value = t('messages.emptyCode');
                return;
            }
            customCodeError.value = '';
            send(customCode.value.trim(), true);  // 不然没法调试了...
        }

        function sendLineupCode() {
            sendAction('applyLineup', { code: lineupCode.value.trim() });
        }

        function getLineupCode() {
            sendAction('getLineup');
        }

        function AddGridItem() {
            sendAction('placeGridItem', {
                row: selectedRow.value,
                col: selectedCol.value,
                gridItemType: selectedGridItem.value,
                potType: selectedScaryPotType.value,
                appearance: selectedScaryPotAppearance.value,
                zombieType: selectedZombieType.value,
                seedType: selectedSeedType.value,
            });
        }

        function setZombies(useNaturalSpawn) {
            sendAction('setZombies', { types: [...selectedSetZbType.value], natural: useNaturalSpawn });
        }

        function onSelectLineUp(newVal) {
            lineupCode.value = newVal;
        }

        onMounted(() => {
            window.addEventListener('beforeunload', releaseSession);
            connect();
        });

        return {
            terrainDraft: terrain.draft,
            terrainLoading: terrain.loading,
            terrainApplying: terrain.applying,
            terrainBusy: terrain.busy,
            terrainDirty: terrain.dirty,
            terrainSelection: terrain.selection,
            terrainBrush: terrain.brush,
            terrainTypes: terrain.types,
            terrainBackgrounds: PGvZData.terrainBackgrounds,
            loadTerrain: terrain.load,
            applyTerrain: terrain.apply,
            terrainPointerDown: terrain.pointerDown,
            terrainPointerMove: terrain.pointerMove,
            terrainPointerUp: terrain.pointerUp,
            terrainCancel: terrain.cancel,
            terrainSelected: terrain.selected,
            terrainCellClick: terrain.cellClick,
            terrainTypeShort,
            terrainCellLabel,
            language,
            languageOptions,
            setLanguage,
            t,
            optionLabel,
            connected,
            sessionRejected,
            connectionState,
            pendingCount,
            hasUnconfirmedRequests,
            takeoverSession,
            unsupportedGameVersion,
            unsupportedGameVersionDetail,
            gameVersion,
            modVersion,
            statusText,
            activeTab,
            speedControls,
            currentSpeedLabel,
            speedPresetSelected,
            combinedSpeed,
            speedControlDisabled,
            applySpeed,
            weather,
            weatherOptions,
            sunValue,
            moneyValue,
            chocolateValue,
            treeHeight,
            level,
            finishedAdventure,
            numSurvivalStage,
            coinX,
            coinY,
            seedTypes,
            zombieTypes,
            setZombieTypes,
            selectRows,
            selectCols,
            packetIdx,
            gridItemTypes,
            easyPlaceModeList,
            scaryPotType,
            scaryPotAppearance,
            coinTypes,
            gameModes,
            lineupCodeMap,
            selectedSeedType,
            selectedZombieType,
            selectedPacketIdx,
            selectedLevel,
            selectedGridItem,
            selectedCoin,
            selectedRow,
            selectedCol,
            selectedScaryPotType,
            selectedScaryPotAppearance,
            isImitater,
            mindCtrl,
            potLeft,
            lastResult,
            resultText,
            customCode,
            customCodeError,
            lineupCode,
            selectedSetZbType,
            selectedScene,
            selectedLineUp,
            easyPlaceMode,
            easyPlaceEnabled,
            switchGroups,
            optionConfig,
            cheatOption,
            scenes,
            currentLineupList,
            dataLabel,
            sendAction,
            setPlacerOption,
            setWeather,
            sendCustomCode,
            sendLineupCode,
            getLineupCode,
            AddGridItem,
            setZombies,
            onSelectLineUp,
        };
    },
});

app.use(ElementPlus);
app.mount('#app');
