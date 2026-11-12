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

function loadGui({ mobile = false, saved = {} } = {}) {
    const sockets = [], errors = [], timers = new Map(), listeners = {}, mounted = [], watchers = [], nextTicks = [];
    const storage = new Map([[storageKey, JSON.stringify(saved)]]);
    let model, connection, timerId = 0;
    const context = {
        URLSearchParams, navigator: { language: 'en', userAgent: mobile ? 'Android' : 'Windows' },
        location: { search: '' }, crypto: { randomUUID: () => 'client-1' }, document: { documentElement: {} },
        localStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value) },
        ElementPlus: { ElMessage: { error: message => errors.push(message) } },
        addEventListener: (name, handler) => { listeners[name] = handler; },
        setTimeout: (fn, delay) => { timers.set(++timerId, { fn, delay, interval: false }); return timerId; },
        clearTimeout: id => timers.delete(id),
        setInterval: (fn, delay) => { timers.set(++timerId, { fn, delay, interval: true }); return timerId; },
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
        if (!interval) timers.delete(entry[0]);
        entry[1].fn();
    }
    function bootstrap() {
        const ws = sockets.at(-1);
        ws.open();
        ws.message({ action: 'bootstrapReady', ready: true });
        ws.message(gameVersionProbe);
        const request = JSON.parse(decodeCall(ws.sent.at(-1).split('\n').at(-1)).args[0]);
        ws.message({ action: 'queued', id: request.id });
        runTimer(100);
        ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
            action: 'sync', modVersion: '1.15.1', gameVersion: '1.3.4', state: {},
        } }] });
        flush();
        return ws;
    }
    return { model, connection, context, sockets, errors, timers, storage, listeners, flush, runTimer, bootstrap };
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
    const saved = { cheat: { freePlant: true, autoCollect: false }, placer: { imitater: true } };
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
            assert.equal(request.state.placer.scaryPotType, 'Seed');
            assert.equal(request.state.placer.scaryPotAppearance, 'ScaryPotQuestion');
        }
        assert.equal(gui.model.connected.value, false);
        ws.message({ action: 'queued', id: request.id });
        gui.runTimer(100);
        assert.equal(decodeCall(ws.sent.at(-1)).name, 'poll');
        ws.message({ action: 'results', results: [{ ...request, ok: true, value: {
            action: 'sync', gameVersion: '1.3.0', modVersion: '1.15.1', state: {},
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

test('remote synchronization updates UI without echoing its changes', () => {
    const gui = loadGui({ mobile: true });
    const ws = gui.bootstrap();
    gui.connection.refreshState();
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    const count = ws.sent.length;
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: { action: 'sync', state: {
        cheat: { freePlant: true, noSunLimit: true }, placer: {
            seedType: 'Sunflower', imitater: true,
            scaryPotType: 'Sun3', scaryPotAppearance: 'ScaryPotZombie',
        },
        weather: { enabled: true, rain: true, storm: false },
    } } }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.freePlant, true);
    assert.equal(gui.model.cheatOption.noSunLimit, true);
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
        action: 'sync', state: { cheat: { noSunLimit: false } },
    } }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.noSunLimit, false);
    assert.equal(gui.model.sunValue.value, 9990);
    assert.equal(ws.sent.length, beforeDisable + 1);
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'acknowledge');
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
    assert.equal([...gui.timers.values()].filter(timer => timer.delay === 5000).length, 1);
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
    gui.runTimer(3000, true);
    const heartbeat = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    ws.message({ action: 'results', results: [{ ...heartbeat, ok: true, value: { action: 'sessionRejected', accepted: false } }] });
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

test('heartbeat and release use the same request API without changing the result banner', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    const banner = JSON.stringify(gui.model.lastResult);
    gui.runTimer(3000, true);
    const heartbeat = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(heartbeat.kind, 'heartbeat');
    ws.message({ action: 'queued', id: heartbeat.id });
    gui.runTimer(100);
    ws.message({ action: 'results', results: [{ ...heartbeat, ok: true, value: { action: 'heartbeat', accepted: true } }] });
    assert.equal(JSON.stringify(gui.model.lastResult), banner);
    gui.listeners.beforeunload();
    const release = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    assert.equal(release.kind, 'release');
    ws.message({ action: 'queued', id: release.id });
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
});

test('missing queue acknowledgement still polls results and lost polls retry without replaying actions', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('winLevel');
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    gui.runTimer(100); // queued acknowledgement was lost
    assert.equal(decodeCall(ws.sent.at(-1)).name, 'poll');
    gui.runTimer(5000); // poll response was lost
    gui.runTimer(100);
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

test('request timeout cancels pending work and ignores late results', () => {
    const gui = loadGui();
    const ws = gui.bootstrap();
    gui.model.sendAction('winLevel');
    const request = JSON.parse(decodeCall(ws.sent.at(-1)).args[0]);
    gui.runTimer(100);
    gui.runTimer(30000);
    assert.equal(gui.model.lastResult.ok, false);
    assert.equal(gui.model.lastResult.key, 'messages.requestTimeout');
    const cancel = decodeCall(ws.sent.at(-1));
    assert.equal(cancel.name, 'cancel');
    assert.deepEqual(JSON.parse(cancel.args[1]), [request.id]);
    ws.message({ action: 'results', results: [{ ...request, ok: true, value: null }] });
    assert.equal(gui.model.lastResult.key, 'messages.requestTimeout');
    assert.equal(ws.sent.filter(code => code.includes('winLevel')).length, 1);
    assert.equal([...gui.timers.values()].filter(timer => !timer.interval).length, 0);
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

test('queued actions time out before bootstrap and are never flushed later', () => {
    const gui = loadGui();
    const ws = gui.sockets[0];
    ws.open();
    gui.model.sendAction('winLevel');
    gui.runTimer(30000);
    assert.equal(gui.model.lastResult.key, 'messages.requestTimeout');
    gui.bootstrap();
    assert.equal(ws.sent.some(code => code.includes('winLevel')), false);
});

test('heartbeat timeout clears all pending requests and socket errors clear timers', () => {
    for (const socketError of [false, true]) {
        const gui = loadGui();
        const ws = gui.bootstrap();
        gui.runTimer(3000, true);
        gui.model.sendAction('winLevel');
        if (socketError) ws.onerror();
        else gui.runTimer(30000);
        assert.equal(gui.model.connected.value, false);
        assert.equal(gui.timers.size, 0);
        const count = ws.sent.length;
        gui.model.sendAction('nextStage');
        assert.equal(ws.sent.length, count);
        assert.equal(gui.timers.size, 0);
    }
});
