// 开关分组、默认值和 PC 端持久化；手机端是否恢复由 app.js 决定。
window.PGvZOptions = (() => {
    const CHECKBOX_STATE_STORAGE_KEY = 'pgvz-gui-checkbox-state';

    function readCheckboxState() {
        try {
            const item = localStorage.getItem(CHECKBOX_STATE_STORAGE_KEY);
            if (!item) return null;
            const state = JSON.parse(item);
            return state && typeof state === 'object' ? state : null;
        } catch {
            return null;
        }
    }

    function writeCheckboxState(state) {
        try {
            localStorage.setItem(CHECKBOX_STATE_STORAGE_KEY, JSON.stringify(state));
        } catch {
            // 隐私模式或存储空间不可用时仍允许修改器正常工作。
        }
    }

    function savedBoolean(state, key, fallback) {
        return state && typeof state[key] === 'boolean' ? state[key] : fallback;
    }

    function createCheatOptions(savedCheatState) {
        const switchGroups = {
            common: [
                'autoCollect',
                'runBackground',
                'skipLevelIntro',
                'freePlant',
                'unlockBannedSeeds',
                'noCooldown',
                'plantAnyWhere',
                'infSun',
                'conveyorNoCooling',
                'enableGlove',
                'gloveNoCooling',
                'shovelNoReset',
                'showShovel',
                'enableTrashcan',
                'plantNoDie',
                'zombieNoDie',
                'wontLose',
                'zombieStop',
                'stopSpawning',
                'freezePortal',
                'tasEnabled',
            ],
            features: [
                'disableTalisman',
                'disableNinja',
                'jackInTheBoxNoExplode',
                'jalapenoHeadNoExplode',
                'blowAwayPropeller',
                'blowAwayThrownImp',
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
                'fullAreaUmbrella',
                'planternAlwaysTransform',
                'hypnoCattailAlwaysHypnotize',
                'allZombiesHypnotizable',
                'scaryPotterNoDelay',
            ],
            scene: [
                'noFog',
                'transScaryPot',
                'visibleGhoul',
                'noCover',
                'showSeedPacketNumbers',
                'showCraterCooldown',
                'showWaveInfo',
                'drawPlantHp',
                'drawPlantCooldown',
                'drawSunProductionCooldown',
                'drawZombieHp',
                'selectZombieHp',
                'drawSquirrel',
            ],
        };

        const optionConfig = [...new Set(Object.values(switchGroups).flat())];
        const cheatOption = Vue.reactive({});
        optionConfig.forEach(item => {
            cheatOption[item] = savedBoolean(savedCheatState, item, false);
        });
        cheatOption.autoCollect = savedBoolean(savedCheatState, 'autoCollect', true);
        cheatOption.runBackground = savedBoolean(savedCheatState, 'runBackground', true);
        cheatOption.tasEnabled = savedBoolean(savedCheatState, 'tasEnabled', true);
        return { switchGroups, optionConfig, cheatOption };
    }

    return { readCheckboxState, writeCheckboxState, savedBoolean, createCheatOptions };
})();
