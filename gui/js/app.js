const { createApp, ref, reactive, onMounted, computed, watch, nextTick } = Vue;

const savedLanguage = localStorage.getItem('pgvz-gui-language');
const initialLanguage = savedLanguage || ((navigator.language || '').toLowerCase().startsWith('en') ? 'en' : 'zh');
const i18n = PGvZI18n.createI18n(initialLanguage);

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
        const wsParams = new URLSearchParams(location.search);
        const SERVER_URL = wsParams.get('ws') || 'ws://localhost:8080/Py';
        const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
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

        const connected = ref(false);
        const connectionState = ref('disconnected');
        const statusText = computed(() => t(`status.${connectionState.value}`));
        const activeTab = ref('player');
        const speed = ref(1);
        const speedOptions = [0.1, 0.2, 0.5, 1, 2, 5, 10];

        const sunValue = ref(9990);
        const moneyValue = ref(999999);
        const treeHeight = ref(1000);
        const level = ref(1);
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
        const isImitater = ref(false);
        const mindCtrl = ref(false);
        const potLeft = ref(false);
        const lastResult = reactive({ ok: true, key: 'messages.waiting', text: '' });
        const resultText = computed(() => lastResult.key ? t(lastResult.key) : lastResult.text);
        const customCode = ref('');
        const customCodeError = ref('');
        const lineupCode = ref('');
        const selectedSetZbType = ref([]);
        const selectedScene = ref('pool');
        const selectedLineUp = ref('');
        const easyPlaceMode = ref('plant');
        const easyPlaceEnabled = ref(true);

        const switchGroups = {
            common: [
                'autoCollect',
                'runBackground',
                'freePlant',
                'noCooldown',
                'plantAnyWhere',
                'infSun',
                'conveyorNoCooling',
                'enableGlove',
                'gloveNoCooling',
                'shovelNoReset',
                'enableTrashcan',
                'plantNoDie',
                'zombieNoDie',
                'wontLose',
                'zombieStop',
                'stopSpawning',
                'tasEnabled',
            ],
            features: [
                'disableTalisman',
                'disableNinja',
                'diamondZenTools',
                'autoRestock',
                'mushroomAwake',
                'cobNoCooling',
                'chomperNoCooling',
                'potatoNoCooling',
                'skillNoCooling',
                'featureThreePeater',
                'butterPult',
                'doubleGatlingpea',
                'fullAreaGloomshroom',
                'planternAlwaysTransform',
            ],
            scene: [
                'noFog',
                'transScaryPot',
                'visibleGhoul',
                'noThunder',
                'noCover',
                'showWaveInfo',
                'drawPlantHp',
                'drawZombieHp',
                'selectZombieHp',
                'drawSquirrel',
            ],
        };

        const optionConfig = [...new Set(Object.values(switchGroups).flat())];
        const cheatOption = reactive({});
        optionConfig.forEach(item => {
            cheatOption[item] = false;
        });
        cheatOption.autoCollect = true;
        cheatOption.runBackground = true;
        cheatOption.tasEnabled = true;

        const scenes = computed(() => [
            { label: t('scene.day'), value: 'day' },
            { label: t('scene.night'), value: 'night' },
            { label: t('scene.pool'), value: 'pool' },
            { label: t('scene.fog'), value: 'fog' },
            { label: t('scene.roof'), value: 'roof' },
            { label: t('scene.moon'), value: 'moon' },
        ]);

        const currentLineupList = computed(() => lineupCodeMap[selectedScene.value] || []);

        let ws = null;
        let applyingRemoteState = false;

        function dataLabel(item) {
            if (language.value === 'zh') return item.label;
            return item.en || item.label;
        }

        function setResult(ok, key, text = '') {
            lastResult.ok = ok;
            lastResult.key = key;
            lastResult.text = text;
        }

        function send(code) {
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                ElementPlus.ElMessage.error(t('messages.notConnected'));
                return;
            }
            ws.send(code);
            setResult(true, 'messages.sent');
        }

        function setCheatOption(key, value) {
            send(`sync_reg.apply('${JSON.stringify({ cheat: { [key]: value } })}')`);
        }

        function syncCheatOptions() {
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
            send(`sync_reg.apply('${JSON.stringify({ cheat: cheatOption, placer: placerUpdates })}')`);
        }

        watch(
            () => ({ ...cheatOption }),
            (newVal, oldVal) => {
                if (applyingRemoteState) return;
                for (const key in newVal) {
                    if (newVal[key] !== oldVal[key]) {
                        setCheatOption(key, newVal[key]);
                    }
                }
            },
            { deep: true }
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
            nextTick(() => {
                applyingRemoteState = false;
            });
        }

        function connect() {
            ws = new WebSocket(SERVER_URL);
            ws.onopen = () => {
                connected.value = true;
                connectionState.value = 'connected';
                if (isMobile) {
                    send(`${PGvZProtocol.BOOTSTRAP_CODE}\nsync_reg.serialize()`);
                } else {
                    send(PGvZProtocol.BOOTSTRAP_CODE);
                    syncCheatOptions();
                }
            };
            ws.onmessage = event => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.statuscode === 0) {
                        if (data.result) {
                            setResult(true, '', data.result);
                        } else {
                            setResult(true, 'messages.success');
                        }

                        const msg = PGvZProtocol.parseResultMessage(data.result);
                        if (msg && msg.action === 'sync' && msg.state) {
                            setResult(true, 'messages.syncOk');
                            applySyncState(msg.state);
                            return;
                        }
                        if (msg && msg.action === 'lineup' && msg.code) {
                            setResult(true, 'messages.lineupOk');
                            lineupCode.value = msg.code;
                            return;
                        }
                    } else {
                        if (data.errortype) {
                            setResult(false, '', data.errortype);
                        } else {
                            setResult(false, 'messages.unknownError');
                        }
                    }
                } catch {
                    setResult(true, '', event.data);
                }
            };
            ws.onclose = () => {
                connected.value = false;
                connectionState.value = 'reconnecting';
                setTimeout(connect, 3000);
            };
            ws.onerror = () => {
                connected.value = false;
                connectionState.value = 'error';
            };
        }

        function sendCustomCode() {
            if (!customCode.value.trim()) {
                customCodeError.value = t('messages.emptyCode');
                return;
            }
            customCodeError.value = '';
            send(customCode.value.trim());
        }

        function sendLineupCode() {
            send(`cheat_option.LineUpOnBoard('${lineupCode.value.trim()}')`);
        }

        function getLineupCode() {
            send(`'{"action":"lineup","code":"' + pgvz.lineup.LineUp.from_board(Sexy.GlobalStaticVars.gLawnApp.mBoard).to_str() + '"}'`);
        }

        function AddGridItem() {
            if (selectedGridItem.value === 'ScaryPot') {
                let numSun;
                let potType;
                switch (selectedScaryPotType.value) {
                    case 'None':
                        numSun = 0;
                        potType = 'none_of(Lawn.ScaryPotType)';
                        break;
                    case 'Sun1':
                        numSun = 1;
                        potType = 'Lawn.ScaryPotType.Sun';
                        break;
                    case 'Sun2':
                        numSun = 2;
                        potType = 'Lawn.ScaryPotType.Sun';
                        break;
                    case 'Sun3':
                        numSun = 3;
                        potType = 'Lawn.ScaryPotType.Sun';
                        break;
                    default:
                        numSun = 0;
                        potType = `Lawn.ScaryPotType.${selectedScaryPotType.value}`;
                        break;
                }
                send(`placer.AddScaryPotOnBoard(${selectedRow.value}, ${selectedCol.value}, ${potType}, Lawn.GridItemState.${selectedScaryPotAppearance.value}, Lawn.ZombieType.${selectedZombieType.value}, Lawn.SeedType.${selectedSeedType.value}, ${numSun})`);
            } else {
                send(`placer.AddGridItemOnBoard(${selectedRow.value}, ${selectedCol.value}, Lawn.GridItemType.${selectedGridItem.value})`);
            }
        }

        function setZombies(useNaturalSpawn) {
            const zombies = selectedSetZbType.value.map(v => `Lawn.ZombieType.${v}`).join(', ');
            const forceArg = useNaturalSpawn ? '' : ', False';
            send(`cheat_option.CheatSetZombies([${zombies}]${forceArg})`);
        }

        function onSelectLineUp(newVal) {
            lineupCode.value = newVal;
        }

        onMounted(() => {
            connect();
        });

        return {
            language,
            languageOptions,
            setLanguage,
            t,
            optionLabel,
            connected,
            statusText,
            activeTab,
            speed,
            speedOptions,
            sunValue,
            moneyValue,
            treeHeight,
            level,
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
            send,
            syncCheatOptions,
            pyBool: PGvZProtocol.pyBool,
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
