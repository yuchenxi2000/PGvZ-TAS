// Run with: node --test tests/test_gui.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const root = path.resolve(__dirname, '..');
const storageKey = 'pgvz-gui-checkbox-state';
const html = fs.readFileSync(path.join(root, 'gui/index.html'), 'utf8');
const gameVersionProbe = { action: 'gameVersion', version: '1.3.4', modVersion: '1.16.0', supportedVersions: ['1.3.3', '1.3.4'] };

function reprString(value) {
    return "'" + value.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n') + "'";
}

function terrainSnapshot() {
    return {
        background: 'Num1Day',
        grid: Array.from({ length: 6 }, (_, row) => Array(9).fill(row === 5 ? 'Dirt' : 'Grass')),
        rows: ['Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Dirt'],
    };
}

function terrainPointerTarget() {
    const grid = { left: 0, top: 0, right: 900, bottom: 600, width: 900, height: 600 };
    const rows = { left: 1000, top: 0, right: 1100, bottom: 600, width: 100, height: 600 };
    return {
        querySelector: selector => ({ getBoundingClientRect: () => selector === '.terrain-grid' ? grid : rows }),
        setPointerCapture() {}, releasePointerCapture() {},
    };
}

test('terrain edits stay local, fill reverse rectangles and rows, and submit only on apply', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const sentBeforeOpening = ws.sent.length;
    gui.model.activeTab.value = 'terrain';
    gui.flush();
    assert.equal(ws.sent.length, sentBeforeOpening);
    assert.deepEqual(JSON.parse(JSON.stringify(gui.model.terrainDraft.value)), terrainSnapshot());
    gui.model.loadTerrain();
    const read = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(read.name, 'getTerrain');
    const original = terrainSnapshot();
    ws.message({ action: 'results', results: [{ ...read, ok: true, value: original }] });
    assert.equal(gui.model.terrainLoading.value, false);
    const sentBeforePainting = ws.sent.length;
    const target = terrainPointerTarget();
    const event = (x, y) => ({ currentTarget: target, clientX: x, clientY: y, button: 0, pointerId: 7, preventDefault() {} });
    gui.model.terrainBrush.value = 'Pool';
    gui.model.terrainPointerDown(event(450, 350));
    gui.model.terrainPointerMove(event(150, 150));
    assert.equal(gui.model.terrainSelected('grid', 2, 3), true);
    assert.equal(gui.model.terrainDraft.value.grid[2][3], 'Grass');
    gui.model.terrainPointerUp(event(150, 150));
    for (let r = 0; r < 6; r++) {
        for (let c = 0; c < 9; c++) {
            assert.equal(gui.model.terrainDraft.value.grid[r][c], r >= 1 && r <= 3 && c >= 1 && c <= 4 ? 'Pool' : r === 5 ? 'Dirt' : 'Grass');
        }
    }
    assert.equal(original.grid[2][3], 'Grass');
    gui.model.terrainBrush.value = 'Dirt';
    gui.model.terrainPointerDown(event(1050, 150));
    gui.model.terrainPointerUp(event(1050, 450));
    assert.deepEqual(Array.from(gui.model.terrainDraft.value.rows), ['Normal', 'Dirt', 'Dirt', 'Dirt', 'Dirt', 'Dirt']);
    gui.model.terrainDraft.value.background = 'Num6Boss';
    assert.equal(gui.model.terrainDirty.value, true);
    assert.equal(ws.sent.length, sentBeforePainting);
    gui.model.applyTerrain();
    const apply = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(apply.name, 'applyTerrain');
    assert.deepEqual(apply.args, JSON.parse(JSON.stringify(gui.model.terrainDraft.value)));
    ws.message({ action: 'results', results: [{ ...apply, ok: true, value: apply.args }] });
    assert.equal(gui.model.terrainDirty.value, false);
    assert.equal(gui.model.terrainApplying.value, false);
    assert.equal(JSON.parse(gui.storage.get(storageKey)).terrain, undefined);
});

test('terrain cancels selections, supports keyboard painting, and discards drafts on disconnect', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.loadTerrain();
    const read = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...read, ok: true, value: terrainSnapshot() }] });
    const target = terrainPointerTarget();
    const event = { currentTarget: target, clientX: 50, clientY: 50, button: 0, pointerId: 1, preventDefault() {} };
    gui.model.terrainBrush.value = 'HighGround';
    gui.model.terrainPointerDown(event);
    gui.model.terrainCancel();
    assert.equal(gui.model.terrainDraft.value.grid[0][0], 'Grass');
    gui.model.terrainCellClick({ detail: 0 }, 'grid', 5, 8);
    assert.equal(gui.model.terrainDraft.value.grid[5][8], 'HighGround');
    assert.equal(gui.model.terrainDraft.value.grid[0][0], 'Grass');
    ws.close();
    gui.flush();
    assert.deepEqual(JSON.parse(JSON.stringify(gui.model.terrainDraft.value)), terrainSnapshot());
    assert.equal(gui.model.terrainSelection.value, null);
    assert.equal(gui.model.terrainBusy.value, false);
});

test('terrain action failures preserve the draft and do not retry or replay edits', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.loadTerrain();
    const read = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...read, ok: true, value: terrainSnapshot() }] });
    gui.model.terrainDraft.value.rows[0] = 'Dirt';
    gui.model.applyTerrain();
    const apply = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...apply, ok: false, errortype: 'RuntimeError', error: 'load failed' }] });
    assert.equal(gui.model.terrainBusy.value, false);
    assert.equal(gui.model.terrainDirty.value, true);
    assert.equal(gui.model.terrainDraft.value.rows[0], 'Dirt');
    assert.match(gui.model.resultText.value, /load failed/);
    const sent = ws.sent.length;
    gui.advance(60000);
    assert.equal(ws.sent.length, sent);
});

test('terrain starts with editable defaults before connection and sends no automatic terrain actions', () => {
    const gui = loadGui();
    const draft = gui.model.terrainDraft.value;
    assert.deepEqual(JSON.parse(JSON.stringify(draft)), terrainSnapshot());
    assert.equal(gui.model.terrainDirty.value, false);
    gui.model.terrainBrush.value = 'Pool';
    gui.model.terrainCellClick({ detail: 0 }, 'grid', 0, 0);
    draft.background = 'Num6Boss';
    assert.equal(draft.grid[0][0], 'Pool');
    assert.equal(draft.grid[1][0], 'Grass');
    assert.equal(gui.model.terrainDirty.value, true);
    assert.equal(gui.sockets[0].sent.length, 0);
    const ws = gui.bootstrap();
    assert.equal(gui.model.terrainDraft.value.background, 'Num6Boss');
    const beforeOpening = ws.sent.length;
    gui.model.activeTab.value = 'terrain';
    gui.flush();
    assert.equal(ws.sent.length, beforeOpening);
    gui.model.applyTerrain();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.name, 'applyTerrain');
    assert.equal(request.args.background, 'Num6Boss');
    assert.equal(request.args.grid[0][0], 'Pool');
});

test('one terrain palette paints cells and row types with Grass mapped to Normal', () => {
    const gui = loadGui();
    assert.deepEqual(Array.from(gui.model.terrainTypes, item => item.value), ['Grass', 'Dirt', 'Pool', 'HighGround', 'Shallow']);
    for (const item of gui.model.terrainTypes) {
        gui.model.terrainBrush.value = item.value;
        const oldRow = gui.model.terrainDraft.value.rows[0];
        gui.model.terrainCellClick({ detail: 0 }, 'grid', 0, 0);
        assert.equal(gui.model.terrainDraft.value.grid[0][0], item.value);
        assert.equal(gui.model.terrainDraft.value.rows[0], oldRow);
        gui.model.terrainCellClick({ detail: 0 }, 'rows', 0, 0);
        assert.equal(gui.model.terrainDraft.value.rows[0], item.value === 'Grass' ? 'Normal' : item.value);
        assert.equal(gui.model.terrainDraft.value.grid[0][0], item.value);
    }
    assert.equal(gui.model.terrainTypeShort('grid', 'Grass'), gui.model.terrainTypeShort('rows', 'Normal'));
    // Existing None cells remain representable without offering a None brush.
    assert.equal(gui.model.terrainTypeShort('grid', 'None'), '—');
    assert.equal(gui.sockets[0].sent.length, 0);
});

test('terrain rectangles span cells and row types in either direction without sending edits', () => {
    for (const reverse of [false, true]) {
        const gui = loadGui();
        gui.model.terrainBrush.value = 'Pool';
        const target = terrainPointerTarget();
        const event = (x, y) => ({ currentTarget: target, clientX: x, clientY: y, button: 0, pointerId: 2, preventDefault() {} });
        const from = reverse ? event(1050, 450) : event(750, 150);
        const to = reverse ? event(750, 150) : event(1050, 450);
        gui.model.terrainPointerDown(from);
        gui.model.terrainPointerMove(to);
        assert.equal(gui.model.terrainSelected('grid', 2, 7), true);
        assert.equal(gui.model.terrainSelected('rows', 2, 0), true);
        assert.equal(gui.model.terrainSelected('grid', 2, 6), false);
        assert.equal(gui.model.terrainDraft.value.rows[2], 'Normal');
        gui.model.terrainPointerUp(to);
        for (let r = 0; r < 6; r++) {
            for (let c = 0; c < 9; c++) {
                assert.equal(gui.model.terrainDraft.value.grid[r][c], r >= 1 && r <= 4 && c >= 7 ? 'Pool' : r === 5 ? 'Dirt' : 'Grass');
            }
            assert.equal(gui.model.terrainDraft.value.rows[r], r >= 1 && r <= 4 ? 'Pool' : r === 5 ? 'Dirt' : 'Normal');
        }
        assert.equal(gui.sockets[0].sent.length, 0);
    }
});

test('terrain selection gap does not start a drag or select the other panel early', () => {
    const gui = loadGui();
    const target = terrainPointerTarget();
    const event = x => ({ currentTarget: target, clientX: x, clientY: 150, button: 0, pointerId: 3, preventDefault() {} });
    gui.model.terrainBrush.value = 'HighGround';
    gui.model.terrainPointerDown(event(950));
    assert.equal(gui.model.terrainSelection.value, null);
    gui.model.terrainPointerDown(event(850));
    gui.model.terrainPointerUp(event(950));
    assert.equal(gui.model.terrainDraft.value.grid[1][8], 'HighGround');
    assert.equal(gui.model.terrainDraft.value.rows[1], 'Normal');
    gui.model.terrainPointerDown(event(1050));
    gui.model.terrainPointerMove(event(950));
    assert.equal(gui.model.terrainSelected('grid', 1, 8), false);
    assert.equal(gui.model.terrainSelected('rows', 1, 0), true);
    gui.model.terrainPointerUp(event(950));
    assert.equal(gui.model.terrainDraft.value.rows[1], 'HighGround');
    assert.equal(gui.model.terrainDraft.value.grid[1][7], 'Grass');
});

function loadGui({ mobile = false, saved = {} } = {}) {
    const sockets = [], errors = [], timers = new Map(), listeners = {}, mounted = [], watchers = [], nextTicks = [];
    const storage = new Map([[storageKey, JSON.stringify(saved)]]);
    let model, connection, timerId = 0, now = 0;
    const context = {
        URLSearchParams, navigator: { language: 'en', userAgent: mobile ? 'Android' : 'Windows' },
        location: { search: '' }, crypto: { randomUUID: () => 'client-1' }, document: { documentElement: {} },
        localStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value) },
        ElementPlus: { ElMessage: { error: message => errors.push(message) } },
        addEventListener: (name, handler) => { listeners[name] = handler; },
        setTimeout: (fn, delay) => { timers.set(++timerId, { fn, delay, at: now + delay, interval: false }); return timerId; },
        clearTimeout: id => timers.delete(id),
        setInterval: (fn, delay) => { timers.set(++timerId, { fn, delay, at: now + delay, interval: true }); return timerId; },
        clearInterval: id => timers.delete(id),
    };
    const watchValue = source => typeof source === 'function' ? source() : source.map(item => item.value);
    context.Vue = {
        ref: value => ({ value }), reactive: value => value, computed: fn => ({ get value() { return fn(); } }),
        watch: (source, callback) => watchers.push({ source, callback, previous: watchValue(source) }),
        nextTick: fn => nextTicks.push(fn), onMounted: fn => mounted.push(fn),
        createApp: config => ({ use() {}, mount() { model = config.setup(); mounted.forEach(fn => fn()); } }),
    };
    context.WebSocket = class {
        static OPEN = 1;
        static CONNECTING = 0;
        constructor(url) { this.url = url; this.readyState = 0; this.sent = []; sockets.push(this); }
        send(code) { this.sent.push(code); }
        open() { this.readyState = 1; this.onopen(); }
        message(message) { this.onmessage({ data: JSON.stringify({ statuscode: 0, result: reprString(JSON.stringify(message)) }) }); }
        close() { this.readyState = 3; this.onclose(); }
    };
    context.window = context;
    vm.createContext(context);
    for (const match of html.matchAll(/<script src="\.\/([^\"]+)"/g)) {
        vm.runInContext(fs.readFileSync(path.join(root, 'gui', match[1]), 'utf8'), context, { filename: match[1] });
        if (match[1] === 'js/connection.js') {
            const create = context.PGvZConnection.create;
            context.PGvZConnection.create = options => { connection = create(options); return connection; };
        }
    }
    function flush() {
        for (const watcher of watchers) {
            const value = watchValue(watcher.source);
            if (JSON.stringify(value) !== JSON.stringify(watcher.previous)) {
                const previous = watcher.previous;
                watcher.previous = value;
                watcher.callback(value, previous);
            }
        }
        nextTicks.splice(0).forEach(fn => fn());
    }
    function runTimer(delay, interval = false) {
        const entry = [...timers].find(([, timer]) => timer.delay === delay && timer.interval === interval);
        assert.ok(entry, `expected a ${delay} ms timer`);
        now = Math.max(now, entry[1].at);
        if (!interval) timers.delete(entry[0]);
        else entry[1].at = now + delay;
        entry[1].fn();
    }
    function advance(milliseconds) {
        const target = now + milliseconds;
        for (;;) {
            const entry = [...timers].filter(([, timer]) => timer.at <= target)
                .sort((a, b) => a[1].at - b[1].at)[0];
            if (!entry) break;
            runTimer(entry[1].delay, entry[1].interval);
        }
        now = target;
    }
    function startInitialization(ws = sockets.at(-1)) {
        ws.open();
        ws.message({ action: 'bootstrapReady', ready: true });
        ws.message(gameVersionProbe);
        return JSON.parse(decodeCall(ws.sent.at(-1).split('\n').at(-1)).args[0]);
    }
    function bootstrap(state = {}) {
        const ws = sockets.at(-1);
        const request = startInitialization(ws);
        ws.message({ action: 'queued', id: request.id });
        runTimer(100);
        ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
            action: 'sync', revision: 1, modVersion: '1.15.1', gameVersion: '1.3.4', state,
        } }] });
        flush();
        return ws;
    }
    return { model, connection, context, sockets, errors, timers, storage, listeners, flush,
        runTimer, advance, startInitialization, bootstrap };
}

function decodeCall(code) {
    let call;
    const capture = name => (...args) => { call = { name, args }; };
    const context = {
        gui_dispatcher: { submit: capture('submit'), poll: capture('poll'), acknowledge: capture('acknowledge'), cancel: capture('cancel') },
    };
    // Fixed protocol calls and their quoted string arguments are valid in both languages.
    vm.runInNewContext(code, context);
    return call;
}

test('business UI only uses action and state APIs', () => {
    const app = fs.readFileSync(path.join(root, 'gui/js/app.js'), 'utf8');
    assert.doesNotMatch(html + app, /Lawn\.|Sexy\.|cheat_option|sync_reg\.|placer\.|pyBool/);
    assert.equal((app.match(/\bsend\(/g) || []).length, 1); // debug console only
    assert.doesNotMatch(html, /\bsend\(/);
});

test('header versions and exact support-list warning survive an import error', () => {
    const gui = loadGui();
    const advice = {
        mod: { en: 'Please download a newer version of the mod.', zh: '请下载新版修改器。' },
        game: { en: 'Please update the game.', zh: '请更新游戏。' },
    };
    for (const [version, supportedVersions, update] of [
        ['1.2.6', gameVersionProbe.supportedVersions, 'game'],
        ['1.3.10', gameVersionProbe.supportedVersions, 'mod'],
        ['1.4.0', ['1.3.10', '1.3.4'], 'mod'],
        ['1.3.9', ['1.3.10', '1.3.4'], 'game'],
        ['1.3.4-beta', gameVersionProbe.supportedVersions, 'game'],
        ['1.3.4', gameVersionProbe.supportedVersions, null],
        ['1.3.5', [], null],
        ['', gameVersionProbe.supportedVersions, null],
    ]) {
        const ws = gui.sockets.at(-1);
        ws.open();
        ws.message({ action: 'bootstrapReady', ready: true });
        assert.equal(ws.sent.at(-1), gui.context.PGvZProtocol.GAME_VERSION_PROBE_CODE);
        ws.message({ ...gameVersionProbe, version, supportedVersions });
        assert.match(ws.sent.at(-1), /from pgvz import \*/);
        ws.onmessage({ data: JSON.stringify({ statuscode: 1, errortype: 'ImportError', error: 'missing game API' }) });
        assert.equal(gui.model.connected.value, false);
        assert.equal(gui.model.gameVersion.value, version);
        assert.equal(gui.model.modVersion.value, gameVersionProbe.modVersion);
        assert.equal(gui.model.unsupportedGameVersion.value, Boolean(update));
        const versions = supportedVersions.join(', ');
        gui.model.setLanguage('en');
        assert.equal(gui.model.unsupportedGameVersionDetail.value,
            update ? `This mod supports game versions ${versions}. ${advice[update].en}` : '');
        gui.model.setLanguage('zh');
        assert.equal(gui.model.unsupportedGameVersionDetail.value,
            update ? `此修改器支持的游戏版本为 ${versions}。${advice[update].zh}` : '');
        ws.close();
        assert.equal(gui.model.modVersion.value, '');
        assert.equal(gui.model.unsupportedGameVersion.value, false);
        gui.runTimer(3000);
    }
});

test('PC restores its saved options; mobile connects without pushing them', () => {
    const saved = { cheat: {
        freePlant: true, autoCollect: false, disableTachieCensor: true, marigoldAlwaysThreeDiamonds: true,
    }, placer: { imitater: true } };
    for (const mobile of [false, true]) {
        const gui = loadGui({ mobile, saved });
        const ws = gui.sockets[0];
        ws.open();
        ws.message({ action: 'bootstrapReady', ready: false });
        gui.runTimer(100);
        ws.message({ action: 'bootstrapReady', ready: true });
        ws.message(gameVersionProbe);
        const call = decodeCall(ws.sent.at(-1).split('\n').at(-1));
        assert.equal(call.name, 'submit');
        const request = JSON.parse(call.args[0]);
        assert.equal(request.kind, 'connect');
        assert.equal(request._clientId, 'client-1');
        assert.equal('state' in request, !mobile);
        if (!mobile) {
            assert.equal(request.state.cheat.freePlant, true);
            assert.equal(request.state.cheat.disableTachieCensor, true);
            assert.equal(request.state.cheat.marigoldAlwaysThreeDiamonds, true);
            assert.equal(request.state.placer.scaryPotType, 'Seed');
            assert.equal(request.state.placer.scaryPotAppearance, 'ScaryPotQuestion');
        }
        assert.equal(gui.model.connected.value, false);
        ws.message({ action: 'queued', id: request.id });
        gui.runTimer(100);
        assert.equal(decodeCall(ws.sent.at(-1)).name, 'poll');
        ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
            action: 'sync', revision: 1, gameVersion: '1.3.0', modVersion: '1.15.1', state: {},
        } }] });
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.gameVersion.value, gameVersionProbe.version);
        assert.equal(gui.model.modVersion.value, gameVersionProbe.modVersion);
        assert.equal(gui.model.cheatOption.freePlant, !mobile);
    }
});

test('state updates do not interpolate enum members or Python booleans', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.setPlacerOption('seedType', 'Sunflower');
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.kind, 'apply');
    assert.deepEqual(request.state, { placer: { seedType: 'Sunflower' } });
    gui.model.cheatOption.freePlant = true;
    gui.flush();
    assert.equal(JSON.parse(decodeCall(ws.sent.at(-1)).args[0]).state.cheat.freePlant, true);
});

test('sun limit toggle persists, synchronizes, and controls the sun input range', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const tag = [...html.matchAll(/<el-input-number\b(?:"[^"]*"|[^">])*>/g)]
        .map(match => match[0]).find(tag => tag.includes('v-model="sunValue"'));
    const maxExpression = tag.match(/:max="([^"]+)"/)[1];
    const maxSun = () => vm.runInNewContext(maxExpression, { cheatOption: gui.model.cheatOption });
    assert.equal(maxSun(), 9990);
    gui.model.cheatOption.noSunLimit = true;
    gui.flush();
    assert.equal(maxSun(), 2147483647);
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.deepEqual(request.state, { cheat: { noSunLimit: true } });
    assert.equal(JSON.parse(gui.storage.get(storageKey)).cheat.noSunLimit, true);

    const restored = loadGui({ saved: JSON.parse(gui.storage.get(storageKey)) });
    assert.equal(restored.model.cheatOption.noSunLimit, true);
    assert.equal(gui.model.optionLabel('noSunLimit'), 'Remove Sun Limit');
    gui.model.setLanguage('zh');
    assert.equal(gui.model.optionLabel('noSunLimit'), '去掉阳光上限');

    gui.model.sunValue.value = 20000;
    gui.model.cheatOption.noSunLimit = false;
    gui.flush();
    assert.equal(maxSun(), 9990);
    assert.equal(gui.model.sunValue.value, 9990);
    gui.model.sunValue.value = 5000;
    gui.model.cheatOption.noSunLimit = true;
    gui.flush();
    gui.model.cheatOption.noSunLimit = false;
    gui.flush();
    assert.equal(gui.model.sunValue.value, 5000);
});

test('aquarium brain limit toggle is bilingual, persists, and synchronizes', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const key = 'zombiquariumNoBrainLimit';
    assert.equal(gui.model.cheatOption[key], false);
    assert.ok(gui.model.switchGroups.features.includes(key));
    assert.equal(gui.model.optionLabel(key), 'Unlimited Zombiquarium Brains');
    gui.model.setLanguage('zh');
    assert.equal(gui.model.optionLabel(key), '水族馆脑子无上限');
    gui.model.cheatOption[key] = true;
    gui.flush();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.deepEqual(request.state, { cheat: { [key]: true } });
    const saved = JSON.parse(gui.storage.get(storageKey));
    assert.equal(saved.cheat[key], true);
    assert.equal(loadGui({ saved }).model.cheatOption[key], true);

    const mobile = loadGui({ mobile: true });
    const mobileWs = mobile.bootstrap({ cheat: { [key]: true } });
    assert.equal(mobile.model.cheatOption[key], true);
    const count = mobileWs.sent.length;
    mobile.flush();
    assert.equal(mobileWs.sent.length, count);
});

test('stage easter eggs use bilingual native-mode settings and one sound action', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const options = {
        daisyMode: ['Daisies', '雏菊'],
        danceMode: ['Dancing', '跳舞'],
        pinataMode: ['Candy', '糖果'],
        mustacheMode: ['Mustaches', '胡子'],
        superMowerMode: ['Mower Appearance', '割草机外观'],
        futureMode: ['Sunglasses', '墨镜'],
    };
    assert.deepEqual(Array.from(gui.model.switchGroups.easterEggs), Object.keys(options));
    assert.equal(gui.model.t('tabs.stage'), 'Stage & Display');
    assert.equal(gui.model.t('sections.weatherControl'), 'Weather Control');
    for (const [key, [english]] of Object.entries(options)) {
        assert.equal(gui.model.optionLabel(key), english);
    }
    gui.model.setLanguage('zh');
    assert.equal(gui.model.t('tabs.stage'), '关卡与显示');
    assert.equal(gui.model.t('sections.weatherControl'), '天气控制');
    for (const [key, [, chinese]] of Object.entries(options)) {
        assert.equal(gui.model.optionLabel(key), chinese);
        gui.model.cheatOption[key] = true;
        gui.flush();
        const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
        assert.deepEqual(request.state, { cheat: { [key]: true } });
    }
    const saved = JSON.parse(gui.storage.get(storageKey));
    assert.ok(Object.keys(options).every(key => saved.cheat[key] === true));

    const stage = html.split('name="stage">')[1].split('</el-tab-pane>')[0];
    const columns = stage.split('<div class="card-stack">');
    assert.equal(columns.length, 3);
    assert.match(columns[0], /panel-grid three/);
    assert.match(columns[1], /sections\.sceneCheats[\s\S]+sections\.weatherControl[\s\S]+<\/el-card>\s*<\/div>\s*<el-card[^>]+>\s*<template #header>.*sections\.speedControl/);
    assert.match(columns[2], /sections\.level[\s\S]+switchGroups\.easterEggs[\s\S]+<\/check-group-card>\s*<\/div>\s*<\/section>/);
    const sound = stage.match(/@click="([^"]+)"[^>]*>↑ ↑ ↓ ↓ ← → ← → B A/)[1];
    vm.runInNewContext(sound, { sendAction: gui.model.sendAction });
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.kind, 'action');
    assert.equal(request.name, 'playKonamiSound');
    assert.deepEqual(request.args, {});
});

test('sync merges startup pushes and orders each field across snapshots, pushes and apply results', () => {
    const gui = loadGui();
    const ws = gui.sockets[0];
    const connect = gui.startInitialization(ws);
    const sync = (revision, state) => ({ action: 'sync', revision, state });
    const sendOutput = (msg, name = 'stdout') => ws.onmessage({
        data: JSON.stringify({ eventtype: 'output', name, msg, timestamp: 123 }),
    });
    const push = (revision, state, clientId = 'client-1') => ws.onmessage({
        data: JSON.stringify({ eventtype: 'execution', statuscode: 0, errortype: null, timestamp: 123,
            result: reprString(JSON.stringify({ ...sync(revision, state), _clientId: clientId })) }),
    });

    sendOutput('ordinary game log\n');
    assert.equal(gui.model.connectionState.value, 'initializing');
    push(2, { cheat: { daisyMode: true }, weather: { rain: true } });
    push(3, { placer: { imitater: true } });
    assert.equal(gui.model.cheatOption.daisyMode, false);
    assert.equal(gui.model.isImitater.value, false);
    ws.message({ action: 'results', results: [{ ...connect, ok: true,
        value: sync(1, { cheat: { daisyMode: false, freePlant: true }, placer: { imitater: false },
            weather: { enabled: true, rain: false, storm: false } }) }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.daisyMode, true);
    assert.equal(gui.model.cheatOption.freePlant, true);
    assert.equal(gui.model.isImitater.value, true);
    assert.equal(gui.model.weather.value, 'rain');

    const sent = ws.sent.length;
    push(9, { cheat: { daisyMode: false } }, 'other-page');
    sendOutput(JSON.stringify({ ...sync(9, { cheat: { daisyMode: false } }), _clientId: 'client-1' }));
    push(1, { cheat: { daisyMode: false } });
    push(5, { weather: { storm: true } });
    push(4, { cheat: { freePlant: false } });
    gui.flush();
    assert.equal(gui.model.cheatOption.daisyMode, true);
    assert.equal(gui.model.cheatOption.freePlant, false);
    assert.equal(gui.model.weather.value, 'rainStorm');
    assert.equal(ws.sent.length, sent);
    assert.equal(JSON.parse(gui.storage.get(storageKey)).cheat.daisyMode, true);

    gui.model.cheatOption.danceMode = true;
    gui.flush();
    const apply = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    push(7, { cheat: { danceMode: false, futureMode: true } });
    ws.message({ action: 'results', results: [{ ...apply, ok: true,
        value: sync(6, { cheat: { danceMode: true } }) }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.danceMode, false);
    assert.equal(gui.model.cheatOption.futureMode, true);
    assert.equal(gui.model.cheatOption.freePlant, false);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');

    gui.model.cheatOption.danceMode = true;
    gui.flush();
    const laterApply = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...laterApply, ok: true,
        value: sync(8, { cheat: { danceMode: true } }) }] });
    push(7, { cheat: { danceMode: false } });
    gui.flush();
    assert.equal(gui.model.cheatOption.danceMode, true);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');
});

test('remote synchronization updates UI without echoing its changes', () => {
    const gui = loadGui({ mobile: true });
    const ws = gui.bootstrap();
    gui.connection.refreshState();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    const count = ws.sent.length;
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: { action: 'sync', revision: 2, state: {
        cheat: {
            freePlant: true, noSunLimit: true, disableTachieCensor: true, marigoldAlwaysThreeDiamonds: true,
        }, placer: {
            seedType: 'Sunflower', imitater: true,
            scaryPotType: 'Sun3', scaryPotAppearance: 'ScaryPotZombie',
        },
        weather: { enabled: true, rain: true, storm: false },
    } } }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.freePlant, true);
    assert.equal(gui.model.cheatOption.noSunLimit, true);
    assert.equal(gui.model.cheatOption.disableTachieCensor, true);
    assert.equal(gui.model.cheatOption.marigoldAlwaysThreeDiamonds, true);
    assert.equal(gui.model.selectedSeedType.value, 'Sunflower');
    assert.equal(gui.model.selectedScaryPotType.value, 'Sun3');
    assert.equal(gui.model.selectedScaryPotAppearance.value, 'ScaryPotZombie');
    assert.equal(gui.model.weather.value, 'rain');
    assert.equal(ws.sent.length, count + 1);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');

    gui.model.sunValue.value = 20000;
    gui.connection.refreshState();
    const disable = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    const beforeDisable = ws.sent.length;
    ws.message({ action: 'results', results: [{ ...disable, ok: true, value: {
        action: 'sync', revision: 3, state: { cheat: { noSunLimit: false } },
    } }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.noSunLimit, false);
    assert.equal(gui.model.sunValue.value, 9990);
    assert.equal(ws.sent.length, beforeDisable + 1);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');
});

test('speed controls display actual custom ratios and preserve drafts during external updates', () => {
    const gui = loadGui();
    const model = gui.model;
    const [global, board] = model.speedControls;
    assert.equal(model.currentSpeedLabel(global), '—');
    const ws = gui.bootstrap({ speed: {
        global: { numerator: 1, denominator: 4 }, board: { id: 1, numerator: 3, denominator: 2 },
    } });
    assert.equal(model.currentSpeedLabel(global), '1/4×');
    assert.equal(model.currentSpeedLabel(board), '3/2×');
    assert.equal(model.combinedSpeed.value, '0.375×');
    assert.ok(global.presets.every(preset => !model.speedPresetSelected(global, preset)));

    global.draft = '1/3';
    const sent = ws.sent.length;
    ws.message({ action: 'sync', _clientId: 'client-1', revision: 2,
        state: { speed: { global: { numerator: 2, denominator: 1 } } } });
    gui.flush();
    assert.equal(model.currentSpeedLabel(global), '2×');
    assert.equal(model.speedPresetSelected(global, '2'), true);
    assert.equal(global.draft, '1/3');
    assert.equal(ws.sent.length, sent);

    model.applySpeed(global);
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.name, 'setGlobalSpeed');
    assert.deepEqual(request.args, { value: '1/3' });
    assert.equal(model.currentSpeedLabel(global), '2×');
    assert.equal(model.speedControlDisabled(global), true);
    assert.equal(model.speedControlDisabled(board), false);
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
        action: 'sync', revision: 3, state: { speed: { global: { numerator: 1, denominator: 3 } } },
    } }] });
    gui.flush();
    assert.equal(model.currentSpeedLabel(global), '1/3×');
    assert.equal(model.combinedSpeed.value, '0.5×');
    assert.equal(global.pending, null);
    assert.equal(global.draft, '');
});

test('level speed handles newer board pushes, failed edits and missing boards', () => {
    const gui = loadGui();
    const model = gui.model;
    const [global, board] = model.speedControls;
    model.setLanguage('zh');
    const ws = gui.bootstrap({ speed: { global: { numerator: 1, denominator: 1 }, board: null } });
    assert.equal(model.currentSpeedLabel(board), '未进入关卡');
    assert.equal(model.speedControlDisabled(board), true);
    assert.equal(model.speedControlDisabled(global), false);

    const pushBoard = (revision, value) => ws.message({
        action: 'sync', _clientId: 'client-1', revision, state: { speed: { board: value } },
    });
    pushBoard(2, { id: 1, numerator: 1, denominator: 1 });
    board.draft = '2/3';
    model.applySpeed(board);
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.name, 'setBoardSpeed');
    assert.deepEqual(request.args, { value: '2/3', boardId: 1 });
    pushBoard(4, { id: 2, numerator: 1, denominator: 1 });
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
        action: 'sync', revision: 3, state: { speed: { board: { id: 1, numerator: 2, denominator: 3 } } },
    } }] });
    assert.equal(model.currentSpeedLabel(board), '1×');
    assert.equal(board.current.id, 2);

    board.draft = '2/0';
    model.applySpeed(board);
    const invalid = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...invalid, ok: false, errortype: 'InvalidSpeed', error: 'invalid' }] });
    assert.equal(board.draft, '2/0');
    assert.equal(board.errorKey, 'speed.board.invalid');
    model.setLanguage('en');
    assert.equal(model.t('sections.speedControl'), 'Speed Control');
    assert.match(model.t(board.errorKey), /decimal or fraction/);
    pushBoard(5, null);
    assert.equal(model.currentSpeedLabel(board), 'No active level');
    assert.equal(model.speedControlDisabled(board), true);
    assert.equal(model.combinedSpeed.value, '');
});

test('vase selectors send their options to the easy placer', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    for (const [model, field, value] of [
        ['selectedScaryPotType', 'scaryPotType', 'Sun2'],
        ['selectedScaryPotAppearance', 'scaryPotAppearance', 'ScaryPotLeaf'],
    ]) {
        const tag = [...html.matchAll(/<el-select\b(?:"[^"]*"|[^">])*>/g)]
            .map(match => match[0]).find(tag => tag.includes(`v-model="${model}"`));
        const handler = tag.match(/@change="([^"]+)"/)[1];
        vm.runInNewContext(`(${handler})(value)`, {
            setPlacerOption: gui.model.setPlacerOption, value,
        });
        const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
        assert.equal(request.kind, 'apply');
        assert.deepEqual(request.state, { placer: { [field]: value } });
    }
});

test('easy-place zoom mode has bilingual labels and uses existing state synchronization', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const zoom = gui.model.easyPlaceModeList.find(item => item.value === 'zoom');
    assert.equal(zoom.label, '放大模式');
    assert.equal(zoom.en, 'Zoom Mode');
    gui.model.setPlacerOption('easyPlaceMode', zoom.value);
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.kind, 'apply');
    assert.deepEqual(request.state, { placer: { easyPlaceMode: 'zoom' } });
    gui.connection.refreshState();
    const snapshot = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...snapshot, ok: true, value: {
        action: 'sync', revision: 2, state: { placer: { easyPlaceMode: 'zoom', active: false } },
    } }] });
    gui.flush();
    assert.equal(gui.model.easyPlaceMode.value, 'zoom');
});

test('actions wait for actual completion and poll only while results are pending', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.getLineupCode();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.name, 'getLineup');
    ws.message({ action: 'queued', id: request.id });
    assert.equal(gui.model.lastResult.key, 'messages.sent');
    gui.runTimer(100);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'poll');
    ws.message({ action: 'results', results: [] });
    gui.runTimer(100);
    ws.message({ action: 'results', results: [{ id: request.id, kind: 'action', name: 'getLineup', ok: true, value: 'base64-data' }] });
    assert.equal(gui.model.lineupCode.value, 'base64-data');
    assert.equal(gui.model.lastResult.key, 'messages.lineupOk');
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('action errors are shown and stop polling the failed request', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('setSun', { value: 123 });
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'queued', id: request.id });
    gui.runTimer(100);
    ws.message({ action: 'results', results: [{ id: request.id, name: request.name, ok: false, errortype: 'RuntimeError', error: "can't access Board at C:\\test\n请进入关卡" }] });
    assert.equal(gui.model.lastResult.ok, false);
    assert.match(gui.model.lastResult.text, /can't access Board/);
    assert.match(gui.model.lastResult.text, /请进入关卡/);
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('concurrent actions share one result poll in flight', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('winLevel');
    const first = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'queued', id: first.id });
    gui.runTimer(100);
    gui.model.sendAction('nextStage');
    const second = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'queued', id: second.id });
    assert.equal([...gui.timers.values()].filter(timer => timer.delay === 100).length, 0);
    assert.equal(gui.timers.size, 0); // 等前一次 poll 响应，不启动第二个轮询或超时。
    ws.message({ action: 'results', results: [{ ...first, ok: true, value: null }] });
    gui.runTimer(100);
    ws.message({ action: 'results', results: [{ ...second, ok: true, value: null }] });
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('quoted strings and line breaks remain action data', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const code = "');globalThis.injected=true;#\\quoted\n\t中文";
    gui.model.lineupCode.value = code;
    gui.model.sendLineupCode();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(request.name, 'applyLineup');
    assert.equal(request.args.code, code.trim());
    assert.equal(gui.context.injected, undefined);
});

test('disconnect cancels action polling and reconnect does not replay old actions', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('winLevel');
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'queued', id: request.id });
    ws.close();
    assert.equal([...gui.timers.values()].some(timer => timer.delay === 100), false);
    gui.runTimer(3000);
    const reconnect = gui.bootstrap();
    const requests = reconnect.sent.filter(code => code.includes('gui_dispatcher.submit'))
        .map(code => JSON.parse(decodeCall(code.split('\n').at(-1)).args[0]));
    assert.equal(requests.some(request => request.kind === 'action'), false);
});

test('rejected sessions cannot submit actions; raw debug execution remains available', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('winLevel');
    const action = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...action, ok: false,
        errortype: 'SessionRejected', error: 'session taken over' }] });
    const count = ws.sent.length;
    gui.model.sendAction('winLevel');
    assert.equal(ws.sent.length, count);
    gui.model.customCode.value = 'print(123)';
    gui.model.sendCustomCode();
    assert.equal(ws.sent.at(-1), 'print(123)');
    ws.close();
    assert.equal(gui.timers.size, 0);
});

test('failed initial synchronization clears queued commands and stops polling', () => {
    const gui = loadGui();
    const ws = gui.sockets[0];
    ws.open();
    gui.model.sendAction('winLevel');
    ws.message({ action: 'bootstrapReady', ready: true });
    ws.message(gameVersionProbe);
    const connect = JSON.parse(decodeCall(ws.sent.at(-1).split('\n').at(-1)).args[0]);
    ws.message({ action: 'queued', id: connect.id });
    gui.runTimer(100);
    ws.message({ action: 'results', results: [{ ...connect, ok: false, errortype: 'ValueError', error: 'bad initial option' }] });
    assert.equal(gui.model.connected.value, false);
    assert.equal(gui.model.lastResult.ok, false);
    assert.equal(gui.timers.size, 0);
    assert.equal(ws.sent.some(code => code.includes('winLevel')), false);
});

test('bootstrap import errors show the 1.4.3 result field and stop calls to the unavailable dispatcher', () => {
    const gui = loadGui();
    const ws = gui.sockets[0];
    ws.open();
    gui.model.sendAction('winLevel');
    ws.message({ action: 'bootstrapReady', ready: true });
    ws.message(gameVersionProbe);
    assert.match(ws.sent.at(-1), /except Exception:\n    import traceback\n    raise RuntimeError\(traceback.format_exc\(\)\)/);
    const traceback = "Traceback (most recent call last):\n  File 'mods/pgvztool/hook.py', line 60\nNameError: name 'missing_name' is not defined";
    ws.onmessage({ data: JSON.stringify({ statuscode: 1, errortype: 'RuntimeError', result: traceback }) });
    assert.equal(gui.model.lastResult.text, `RuntimeError: ${traceback}`);
    assert.equal(gui.model.connected.value, false);
    assert.equal(gui.connection.connectionState.value, 'error');
    assert.equal(gui.model.gameVersion.value, gameVersionProbe.version);
    assert.equal(gui.timers.size, 0);
    assert.equal(ws.sent.some(code => /gui_dispatcher\.(poll|cancel)\(/.test(code)), false);
    assert.equal(ws.sent.some(code => code.includes('winLevel')), false);
    ws.onmessage({ data: JSON.stringify({ statuscode: 1,
        errortype: 'IronPython.Runtime.UnboundNameException', result: "name 'gui_dispatcher' is not defined",
    }) });
    assert.equal(gui.model.lastResult.text, `RuntimeError: ${traceback}`);
    gui.model.customCode.value = '1 / 0';
    gui.model.sendCustomCode();
    ws.onmessage({ data: JSON.stringify({ statuscode: 1, errortype: 'ZeroDivisionError', result: 'division by zero' }) });
    assert.equal(gui.model.lastResult.text, 'ZeroDivisionError: division by zero');
});

test('idle pages send no traffic; release uses the request API without changing the banner', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const banner = JSON.stringify(gui.model.lastResult);
    const sent = ws.sent.length;
    gui.advance(300000);
    assert.equal(ws.sent.length, sent);
    assert.equal(gui.timers.size, 0);
    assert.equal(JSON.stringify(gui.model.lastResult), banner);
    gui.listeners.beforeunload();
    const release = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(release.kind, 'release');
    ws.message({ action: 'queued', id: release.id });
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('missing queue acknowledgement still polls; delayed results and lost acknowledgements do not replay actions', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('winLevel');
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    gui.runTimer(100); // queued acknowledgement was lost
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'poll');
    const sent = ws.sent.length;
    gui.advance(300000); // poll response is delayed while the game is in the background
    assert.equal(ws.sent.length, sent);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'poll');
    assert.equal(ws.sent.filter(code => code.includes('winLevel')).length, 1);
    const result = { ...request, ok: true, value: null };
    ws.message({ action: 'results', results: [result] });
    assert.equal(gui.model.lastResult.key, 'messages.success');
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');
    gui.model.lastResult.key = 'later-banner';
    ws.message({ action: 'results', results: [result] }); // ack was lost
    assert.equal(gui.model.lastResult.key, 'later-banner');
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('actions survive a long background pause and complete once the game resumes', () => {
    for (const mobile of [false, true]) {
        const gui = loadGui({ mobile });
        const ws = gui.bootstrap();
        gui.model.sendAction('winLevel');
        const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
        gui.runTimer(100);
        const sent = ws.sent.length;
        gui.advance(600000);
        assert.equal(ws.sent.length, sent);
        assert.equal(gui.sockets.length, 1);
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.pendingCount.value, 1);
        assert.equal(gui.timers.size, 0);
        ws.message({ action: 'results', results: [{ ...request, ok: true, value: null }] });
        assert.equal(gui.model.lastResult.key, 'messages.success');
        assert.equal(gui.model.pendingCount.value, 0);
        assert.equal(ws.sent.filter(code => code.includes('winLevel')).length, 1);
        assert.equal(ws.sent.some(code => code.includes('cancel')), false);
        gui.model.setLanguage('zh');
        assert.equal(gui.model.t('messages.sent'), '已发送，切回游戏后生效');
        gui.model.setLanguage('en');
        assert.equal(gui.model.t('messages.sent'), 'Sent. Takes effect when you switch back to the game');
    }
});

test('unrelated debug errors do not discard concurrent action results', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.getLineupCode();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    gui.runTimer(100);
    ws.onmessage({ data: JSON.stringify({ statuscode: 1, errortype: 'SyntaxError', error: 'debug-only' }) });
    assert.match(gui.model.lastResult.text, /debug-only/);
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: 'lineup-after-debug-error' }] });
    assert.equal(gui.model.lineupCode.value, 'lineup-after-debug-error');
    assert.equal(gui.model.lastResult.key, 'messages.lineupOk');
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('business operations before initialization are rejected without a local send queue', () => {
    const gui = loadGui();
    const ws = gui.sockets[0];
    ws.open();
    gui.model.sendAction('winLevel');
    assert.match(gui.errors.at(-1), /finish initializing/);
    assert.equal(gui.model.pendingCount.value, 0);
    gui.advance(600000);
    gui.bootstrap();
    assert.equal(ws.sent.some(code => code.includes('winLevel')), false);
    assert.equal((html.match(/<el-form :disabled="!connected"/g) || []).length, 4);
});

test('real socket failures report uncertain results and reconnect once without replaying actions', () => {
    for (const socketError of [false, true]) {
        const gui = loadGui();
        const ws = gui.bootstrap();
        gui.model.sendAction('winLevel');
        const pending = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
        if (socketError) ws.onerror();
        else ws.close();
        assert.equal(gui.model.connected.value, false);
        assert.equal(gui.model.hasUnconfirmedRequests.value, true);
        assert.equal(gui.model.lastResult.key, 'messages.resultsUnconfirmed');
        assert.deepEqual([...gui.timers.values()].map(timer => timer.delay), [3000]);
        const count = ws.sent.length;
        gui.model.sendAction('nextStage');
        assert.equal(ws.sent.length, count);
        ws.onerror();
        ws.close();
        assert.deepEqual([...gui.timers.values()].map(timer => timer.delay), [3000]);
        gui.runTimer(3000);
        const recovered = gui.bootstrap();
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.hasUnconfirmedRequests.value, true);
        assert.equal(recovered.sent.some(code => code.includes('winLevel') || code.includes('nextStage')), false);
        ws.message({ action: 'results', results: [{ ...pending, ok: true, value: null }] });
        assert.equal(gui.model.lastResult.key, 'messages.syncOk');
    }
});

test('PC saves changed options immediately while the suspended game waits to apply them; mobile keeps storage untouched', () => {
    for (const mobile of [true, false]) {
        const saved = { cheat: { freePlant: false } };
        const gui = loadGui({ mobile, saved });
        const ws = gui.bootstrap({ cheat: { freePlant: false } });
        gui.model.cheatOption.freePlant = true;
        gui.flush();
        const pending = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
        assert.equal(pending.kind, 'apply');
        assert.equal(JSON.parse(gui.storage.get(storageKey)).cheat.freePlant, !mobile);
        gui.advance(600000);
        assert.equal(gui.sockets.length, 1);
        assert.equal(gui.model.cheatOption.freePlant, true);
        assert.equal(gui.model.pendingCount.value, 1);
        ws.message({ action: 'results', results: [{ ...pending, ok: true, value: null }] });
        assert.equal(gui.model.pendingCount.value, 0);
        assert.equal(gui.model.lastResult.key, 'messages.success');
    }
});

test('only the WebSocket handshake has a timeout; bootstrap probes can wait indefinitely', () => {
    const handshake = loadGui();
    handshake.runTimer(30000);
    assert.equal(handshake.connection.connectionState.value, 'reconnecting');
    handshake.runTimer(3000);
    handshake.bootstrap();
    assert.equal(handshake.model.connected.value, true);
    for (const blockedStage of ['ready', 'version', 'connect']) {
        const gui = loadGui({ saved: { cheat: { freePlant: true } } });
        const ws = gui.sockets[0];
        ws.open();
        if (blockedStage !== 'ready') ws.message({ action: 'bootstrapReady', ready: true });
        if (blockedStage === 'connect') ws.message(gameVersionProbe);
        gui.advance(600000);
        assert.equal(gui.sockets.length, 1);
        assert.equal(ws.readyState, 1);
        assert.equal(gui.connection.connectionState.value, 'initializing');
        assert.equal(JSON.parse(gui.storage.get(storageKey)).cheat.freePlant, true);
        if (blockedStage === 'ready') ws.message({ action: 'bootstrapReady', ready: true });
        if (blockedStage !== 'connect') ws.message(gameVersionProbe);
        const connect = JSON.parse(decodeCall(ws.sent.findLast(code => code.includes('gui_dispatcher.submit')).split('\n').at(-1)).args[0]);
        ws.message({ action: 'results', results: [{ ...connect, ok: true, value: {
            action: 'sync', revision: 1, state: { cheat: { freePlant: true } },
        } }] });
        gui.flush();
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.cheatOption.freePlant, true);
    }
});

test('initialization disconnects preserve PC restoration state and never push saved state on mobile', () => {
    for (const mobile of [false, true]) {
        const saved = { cheat: { freePlant: true, autoCollect: false }, placer: { imitater: true } };
        const gui = loadGui({ mobile, saved });
        for (let attempt = 0; attempt < 3; attempt++) {
            const ws = gui.sockets.at(-1);
            const connect = gui.startInitialization(ws);
            assert.equal('state' in connect, !mobile);
            if (!mobile) {
                assert.equal(connect.state.cheat.freePlant, true);
                assert.equal(connect.state.cheat.autoCollect, false);
                assert.equal(connect.state.placer.imitater, true);
            }
            gui.advance(300000);
            assert.deepEqual(JSON.parse(gui.storage.get(storageKey)), saved);
            ws.close();
            gui.runTimer(3000);
        }
        const ws = gui.bootstrap({ cheat: { freePlant: !mobile } });
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.cheatOption.freePlant, !mobile);
        assert.equal(ws.sent.some(code => code.includes('winLevel')), false);
    }
});

test('leaving the page cancels scheduled retries and rejected recovery sessions do not retry', () => {
    const leaving = loadGui();
    leaving.bootstrap().onerror();
    leaving.listeners.beforeunload();
    assert.equal(leaving.timers.size, 0);
    const occupied = loadGui();
    occupied.bootstrap().onerror();
    occupied.runTimer(3000);
    const ws = occupied.sockets.at(-1);
    ws.open();
    ws.message({ action: 'bootstrapReady', ready: true });
    ws.message(gameVersionProbe);
    const connect = JSON.parse(decodeCall(ws.sent.at(-1).split('\n').at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...connect, ok: true,
        value: { action: 'sessionRejected', accepted: false },
    }] });
    assert.equal(occupied.connection.connectionState.value, 'occupied');
    assert.equal(occupied.timers.size, 0);
    ws.close();
    assert.equal(occupied.timers.size, 0);
});


test('explicit takeover works on an open or closed occupied socket and uses bilingual controls', () => {
    for (const closeSocket of [false, true]) {
        const gui = loadGui();
        let ws = gui.sockets[0];
        const request = gui.startInitialization(ws);
        ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
            action: 'sessionRejected', accepted: false,
        } }] });
        assert.equal(gui.model.sessionRejected.value, true);
        assert.equal(gui.timers.size, 0);
        if (closeSocket) ws.close();
        gui.model.takeoverSession();
        assert.equal(gui.model.connected.value, false);
        if (closeSocket) {
            ws = gui.sockets.at(-1);
            gui.startInitialization(ws);
        }
        const takeover = JSON.parse(decodeCall(ws.sent.at(-1).split('\n').at(-1)).args[0]);
        assert.equal(takeover.kind, 'connect');
        assert.equal(takeover.takeover, true);
        ws.message({ action: 'results', results: [{ ...takeover, ok: true, value: { action: 'sync', revision: 1, state: {} } }] });
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.sessionRejected.value, false);
        gui.model.setLanguage('zh');
        assert.equal(gui.model.t('messages.takeoverSession'), '接管控制权');
        assert.equal(gui.model.t('messages.sessionOccupiedDetail'), '可以继续使用原页面，或接管控制权以使用当前页面');
        gui.model.setLanguage('en');
        assert.equal(gui.model.t('messages.takeoverSession'), 'Take Control');
        assert.equal(gui.model.t('messages.sessionOccupiedDetail'), 'Continue using the other page, or take control to use this page');
    }
});

test('remote PC snapshots save only after successful synchronization and never echo apply requests', () => {
    const saved = { cheat: { freePlant: true } };
    const gui = loadGui({ saved });
    const request = gui.startInitialization();
    const ws = gui.sockets[0];
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
        action: 'sync', revision: 1, state: { cheat: { freePlant: false }, placer: { imitater: true } },
    } }] });
    assert.deepEqual(JSON.parse(gui.storage.get(storageKey)), saved);
    const sent = ws.sent.length;
    gui.flush();
    const stored = JSON.parse(gui.storage.get(storageKey));
    assert.equal(stored.cheat.freePlant, false);
    assert.equal(stored.placer.imitater, true);
    assert.equal(ws.sent.length, sent);
});

test('page exit during bootstrap ignores late responses and does not acquire a new session', () => {
    for (const stage of ['handshake', 'ready', 'connect']) {
        const gui = loadGui();
        const ws = gui.sockets[0];
        if (stage !== 'handshake') ws.open();
        if (stage === 'connect') {
            ws.message({ action: 'bootstrapReady', ready: true });
            ws.message(gameVersionProbe);
        }
        gui.listeners.beforeunload();
        const sent = ws.sent.length;
        ws.open();
        ws.message({ action: 'bootstrapReady', ready: true });
        ws.message(gameVersionProbe);
        gui.advance(600000);
        assert.equal(ws.sent.length, sent);
        assert.equal(gui.model.pendingCount.value, 0);
        assert.equal(gui.timers.size, 0);
    }
});

test('lost takeover replies do not automatically repeat a forced takeover on reconnection', () => {
    const gui = loadGui();
    const ws = gui.sockets[0];
    const request = gui.startInitialization();
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
        action: 'sessionRejected', accepted: false,
    } }] });
    gui.model.takeoverSession();
    const takeover = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(takeover.takeover, true);
    ws.close();
    gui.runTimer(3000);
    const reconnect = gui.startInitialization();
    assert.equal('takeover' in reconnect, false);
    assert.equal('state' in reconnect, true);
    assert.equal(gui.sockets.length, 2);
});
