const { createApp, ref, reactive, onMounted, computed, watch, nextTick } = Vue;

const savedLanguage = localStorage.getItem('pgvz-gui-language');
const initialLanguage = savedLanguage || ((navigator.language || '').toLowerCase().startsWith('en') ? 'en' : 'zh');
const i18n = PGvZI18n.createI18n(initialLanguage);

const { readCheckboxState, writeCheckboxState, savedBoolean } = PGvZOptions;

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
        const speed = ref(1);
        const speedOptions = [0.1, 0.2, 0.5, 1, 2, 5, 10];
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

        const { switchGroups, optionConfig, cheatOption } = PGvZOptions.createCheatOptions(savedCheatState);

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
        const {
            connected, sessionRejected, legacyGameVersionWarning,
            gameVersion, modVersion, connectionState,
            send, sendAction, applyState, connect, releaseSession,
        } = PGvZConnection.create({
            isMobile, t, setResult, getInitialState, applySyncState, lineupCode,
        });
        const statusText = computed(() => t(`status.${connectionState.value}`));

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
            if (isMobile) return;
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
                saveCheckboxState();
                if (applyingRemoteState) return;
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
            applyingRemoteState = true;
            if (state.cheat) {
                Object.keys(state.cheat).forEach(k => {
                    if (k in cheatOption) cheatOption[k] = state.cheat[k];
                });
            }
            if (state.placer) {
                const p = state.placer;
                if (p.seedType) selectedSeedType.value = p.seedType;
                if (p.zombieType) selectedZombieType.value = p.zombieType;
                if (p.gridItemType) selectedGridItem.value = p.gridItemType;
                if (p.coinType) selectedCoin.value = p.coinType;
                if (p.mindCtrl !== undefined) mindCtrl.value = p.mindCtrl;
                if (p.potReverse !== undefined) potLeft.value = p.potReverse;
                if (p.imitater !== undefined) isImitater.value = p.imitater;
                if (p.easyPlaceMode) easyPlaceMode.value = p.easyPlaceMode;
                if (p.easyPlaceEnabled !== undefined) easyPlaceEnabled.value = p.easyPlaceEnabled;
            }
            if (state.weather) {
                const w = state.weather;
                if (!w.enabled) weather.value = 'default';
                else if (w.rain && w.storm) weather.value = 'rainStorm';
                else if (w.rain) weather.value = 'rain';
                else if (w.storm) weather.value = 'storm';
                else weather.value = 'sunny';
            }
            nextTick(() => {
                applyingRemoteState = false;
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
            language,
            languageOptions,
            setLanguage,
            t,
            optionLabel,
            connected,
            sessionRejected,
            legacyGameVersionWarning,
            gameVersion,
            modVersion,
            statusText,
            activeTab,
            speed,
            speedOptions,
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
