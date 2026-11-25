// Run with: node --test tests/test_gui.js
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { test } = require('node:test');

const root = path.resolve(__dirname, '..');
const storageKey = 'pgvz-gui-checkbox-state';
const html = fs.readFileSync(path.join(root, 'gui/index.html'), 'utf8');
const readyStatus = {
    ready: true, instance: 'instance-1', version: '1.3.4', modVersion: '1.16.0', supportedVersions: ['1.3.3', '1.3.4'],
};

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
    const http = gui.bootstrap();
    const sentBeforeOpening = http.sent.length;
    gui.model.activeTab.value = 'terrain';
    gui.flush();
    assert.equal(http.sent.length, sentBeforeOpening);
    assert.deepEqual(JSON.parse(JSON.stringify(gui.model.terrainDraft.value)), terrainSnapshot());
    gui.model.loadTerrain();
    const read = http.sent.at(-1);
    assert.equal(read.name, 'getTerrain');
    const original = terrainSnapshot();
    http.message({ action: 'results', results: [{ ...read, ok: true, value: original }] });
    assert.equal(gui.model.terrainLoading.value, false);
    const sentBeforePainting = http.sent.length;
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
    assert.equal(http.sent.length, sentBeforePainting);
    gui.model.applyTerrain();
    const apply = http.sent.at(-1);
    assert.equal(apply.name, 'applyTerrain');
    assert.deepEqual(apply.args, JSON.parse(JSON.stringify(gui.model.terrainDraft.value)));
    http.message({ action: 'results', results: [{ ...apply, ok: true, value: apply.args }] });
    assert.equal(gui.model.terrainDirty.value, false);
    assert.equal(gui.model.terrainApplying.value, false);
    assert.equal(JSON.parse(gui.storage.get(storageKey)).terrain, undefined);
});

test('terrain cancels selections, supports keyboard painting, and discards drafts on disconnect', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
    gui.model.loadTerrain();
    const read = http.sent.at(-1);
    http.message({ action: 'results', results: [{ ...read, ok: true, value: terrainSnapshot() }] });
    const target = terrainPointerTarget();
    const event = { currentTarget: target, clientX: 50, clientY: 50, button: 0, pointerId: 1, preventDefault() {} };
    gui.model.terrainBrush.value = 'HighGround';
    gui.model.terrainPointerDown(event);
    gui.model.terrainCancel();
    assert.equal(gui.model.terrainDraft.value.grid[0][0], 'Grass');
    gui.model.terrainCellClick({ detail: 0 }, 'grid', 5, 8);
    assert.equal(gui.model.terrainDraft.value.grid[5][8], 'HighGround');
    assert.equal(gui.model.terrainDraft.value.grid[0][0], 'Grass');
    http.fail();
    gui.flush();
    assert.deepEqual(JSON.parse(JSON.stringify(gui.model.terrainDraft.value)), terrainSnapshot());
    assert.equal(gui.model.terrainSelection.value, null);
    assert.equal(gui.model.terrainBusy.value, false);
});

test('terrain action failures preserve the draft and do not retry or replay edits', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
    gui.model.loadTerrain();
    const read = http.sent.at(-1);
    http.message({ action: 'results', results: [{ ...read, ok: true, value: terrainSnapshot() }] });
    gui.model.terrainDraft.value.rows[0] = 'Dirt';
    gui.model.applyTerrain();
    const apply = http.sent.at(-1);
    http.message({ action: 'results', results: [{ ...apply, ok: false, errortype: 'RuntimeError', error: 'load failed' }] });
    assert.equal(gui.model.terrainBusy.value, false);
    assert.equal(gui.model.terrainDirty.value, true);
    assert.equal(gui.model.terrainDraft.value.rows[0], 'Dirt');
    assert.match(gui.model.resultText.value, /load failed/);
    const sent = http.sent.length;
    gui.advance(60000);
    assert.equal(http.sent.length, sent);
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
    assert.equal(gui.http.sent.length, 0);
    const http = gui.bootstrap();
    assert.equal(gui.model.terrainDraft.value.background, 'Num6Boss');
    const beforeOpening = http.sent.length;
    gui.model.activeTab.value = 'terrain';
    gui.flush();
    assert.equal(http.sent.length, beforeOpening);
    gui.model.applyTerrain();
    const request = http.sent.at(-1);
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
    assert.equal(gui.http.sent.length, 0);
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
        assert.equal(gui.http.sent.length, 0);
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

function loadGui({ mobile = false, saved = {}, clientId = 'client-1' } = {}) {
    const sockets = [], errors = [], timers = new Map(), listeners = {}, mounted = [], watchers = [], nextTicks = [];
    const requests = [];
    let deferSubmit = false;
    const storage = new Map([[storageKey, JSON.stringify(saved)]]);
    let model, connection, timerId = 0, now = 0;
    const context = {
        URLSearchParams, navigator: { language: 'en', userAgent: mobile ? 'Android' : 'Windows' },
        location: { search: '' }, crypto: { randomUUID: () => clientId }, document: { documentElement: {} },
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
        constructor(url) { this.url = url; this.readyState = 0; this.sent = []; sockets.push(this); }
        send(code) { this.sent.push(code); }
        open() { this.readyState = 1; this.onopen(); }
        message(data) { this.onmessage({ data: JSON.stringify(data) }); }
        close() { this.readyState = 3; this.onclose(); }
    };
    context.recordRequest = (url, options, resolve, reject) => {
        const request = {
            url, options, payload: options.body && JSON.parse(options.body), pending: true,
            respond(body, status = 200) {
                this.pending = false;
                resolve(status, body);
            },
            fail() {
                this.pending = false;
                reject();
            },
        };
        requests.push(request);
        if (url === '/api/request' && (!deferSubmit || options.keepalive)) {
            request.respond({ action: 'queued', id: request.payload.id });
        }
    };
    context.window = context;
    vm.createContext(context, { microtaskMode: 'afterEvaluate' });
    vm.runInContext(`
        window.fetch = (url, options) => new Promise((resolve, reject) => recordRequest(url, options,
            (status, body) => resolve({ status, ok: status < 400, json: () => Promise.resolve(body) }),
            () => reject(new TypeError('Failed to fetch'))));
    `, context);
    for (const match of html.matchAll(/<script src="\.\/([^\"]+)"/g)) {
        vm.runInContext(fs.readFileSync(path.join(root, 'gui', match[1]), 'utf8'), context, { filename: match[1] });
        if (match[1] === 'js/connection.js') {
            const create = context.PGvZConnection.create;
            context.PGvZConnection.create = options => { connection = create(options); return connection; };
        }
    }
    function settle() {
        vm.runInContext('', context);
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
        settle();
    }
    function runTimer(delay, interval = false) {
        const entry = [...timers].find(([, timer]) => timer.delay === delay && timer.interval === interval);
        assert.ok(entry, `expected a ${delay} ms timer`);
        now = Math.max(now, entry[1].at);
        if (!interval) timers.delete(entry[0]);
        else entry[1].at = now + delay;
        entry[1].fn();
        settle();
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
    function lastRequest(endpoint, pending = false) {
        settle();
        const request = requests.findLast(item => item.url === '/api/' + endpoint && (!pending || item.pending));
        assert.ok(request, `expected an HTTP request to /api/${endpoint}`);
        return request;
    }
    function beginPoll() {
        const current = requests.findLast(item => item.url === '/api/poll' && item.pending);
        if (current) return current;
        const delay = timers.values().next().value?.delay;
        runTimer(delay);
        return lastRequest('poll', true);
    }
    const http = {
        get sent() {
            settle();
            return requests.filter(item => item.url === '/api/request').map(item => item.payload);
        },
        message({ action, results = [], updates = [], ...fields }) {
            if (action === 'sync') updates = [{ action, ...fields }];
            beginPoll().respond({ results, updates });
            settle();
        },
        fail() {
            beginPoll().fail();
            settle();
        },
    };
    function respondStatus(status = readyStatus) {
        lastRequest('status', true).respond(status);
        settle();
    }
    function startInitialization() {
        respondStatus();
        return http.sent.at(-1);
    }
    function bootstrap(state = {}) {
        const request = startInitialization();
        http.message({ action: 'results', results: [{ ...request, ok: true, value: {
            action: 'sync', revision: 1, state,
        } }] });
        flush();
        return http;
    }
    return { model, connection, context, http, requests, sockets, errors, timers, storage, listeners, flush, settle,
        runTimer, advance, startInitialization, bootstrap, respondStatus, lastRequest, beginPoll,
        deferSubmissions: value => { deferSubmit = value; },
    };
}

test('business UI only uses action and state APIs', () => {
    const app = fs.readFileSync(path.join(root, 'gui/js/app.js'), 'utf8');
    assert.doesNotMatch(html + app, /Lawn\.|Sexy\.|cheat_option|sync_reg\.|placer\.|pyBool/);
    assert.equal((app.match(/\bdebug\.send\(/g) || []).length, 1);
    assert.doesNotMatch(html, /\bsend\(/);
});

test('state updates do not interpolate enum members or Python booleans', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
    gui.model.setPlacerOption('seedType', 'Sunflower');
    const request = http.sent.at(-1);
    assert.equal(request.kind, 'apply');
    assert.deepEqual(request.state, { placer: { seedType: 'Sunflower' } });
    gui.model.cheatOption.freePlant = true;
    gui.flush();
    assert.equal(http.sent.at(-1).state.cheat.freePlant, true);
});

test('sun limit toggle persists, synchronizes, and controls the sun input range', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
    const tag = [...html.matchAll(/<el-input-number\b(?:"[^"]*"|[^">])*>/g)]
        .map(match => match[0]).find(tag => tag.includes('v-model="sunValue"'));
    const maxExpression = tag.match(/:max="([^"]+)"/)[1];
    const maxSun = () => vm.runInNewContext(maxExpression, { cheatOption: gui.model.cheatOption });
    assert.equal(maxSun(), 9990);
    gui.model.cheatOption.noSunLimit = true;
    gui.flush();
    assert.equal(maxSun(), 2147483647);
    const request = http.sent.at(-1);
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
    const http = gui.bootstrap();
    const key = 'zombiquariumNoBrainLimit';
    assert.equal(gui.model.cheatOption[key], false);
    assert.ok(gui.model.switchGroups.features.includes(key));
    assert.equal(gui.model.optionLabel(key), 'Unlimited Zombiquarium Brains');
    gui.model.setLanguage('zh');
    assert.equal(gui.model.optionLabel(key), '水族馆脑子无上限');
    gui.model.cheatOption[key] = true;
    gui.flush();
    const request = http.sent.at(-1);
    assert.deepEqual(request.state, { cheat: { [key]: true } });
    const saved = JSON.parse(gui.storage.get(storageKey));
    assert.equal(saved.cheat[key], true);
    assert.equal(loadGui({ saved }).model.cheatOption[key], true);

    const mobile = loadGui({ mobile: true });
    const mobileHttp = mobile.bootstrap({ cheat: { [key]: true } });
    assert.equal(mobile.model.cheatOption[key], true);
    const count = mobileHttp.sent.length;
    mobile.flush();
    assert.equal(mobileHttp.sent.length, count);
});

test('stage easter eggs use bilingual native-mode settings and one sound action', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
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
        const request = http.sent.at(-1);
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
    const request = http.sent.at(-1);
    assert.equal(request.kind, 'action');
    assert.equal(request.name, 'playKonamiSound');
    assert.deepEqual(request.args, {});
});

test('remote synchronization updates UI without echoing its changes', () => {
    const gui = loadGui({ mobile: true });
    const http = gui.bootstrap();
    gui.connection.refreshState();
    const request = http.sent.at(-1);
    const count = http.sent.length;
    http.message({ action: 'results', results: [{ ...request, ok: true, value: { action: 'sync', revision: 2, state: {
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
    assert.equal(http.sent.length, count);

    gui.model.sunValue.value = 20000;
    gui.connection.refreshState();
    const disable = http.sent.at(-1);
    const beforeDisable = http.sent.length;
    http.message({ action: 'results', results: [{ ...disable, ok: true, value: {
        action: 'sync', revision: 3, state: { cheat: { noSunLimit: false } },
    } }] });
    gui.flush();
    assert.equal(gui.model.cheatOption.noSunLimit, false);
    assert.equal(gui.model.sunValue.value, 9990);
    assert.equal(http.sent.length, beforeDisable);
});

test('speed controls display actual custom ratios and preserve drafts during external updates', () => {
    const gui = loadGui();
    const model = gui.model;
    const [global, board] = model.speedControls;
    assert.equal(model.currentSpeedLabel(global), '—');
    const http = gui.bootstrap({ speed: {
        global: { numerator: 1, denominator: 4 }, board: { id: 1, numerator: 3, denominator: 2 },
    } });
    assert.equal(model.currentSpeedLabel(global), '1/4×');
    assert.equal(model.currentSpeedLabel(board), '3/2×');
    assert.equal(model.combinedSpeed.value, '0.375×');
    assert.ok(global.presets.every(preset => !model.speedPresetSelected(global, preset)));

    global.draft = '1/3';
    const sent = http.sent.length;
    http.message({ action: 'sync', _clientId: 'client-1', revision: 2,
        state: { speed: { global: { numerator: 2, denominator: 1 } } } });
    gui.flush();
    assert.equal(model.currentSpeedLabel(global), '2×');
    assert.equal(model.speedPresetSelected(global, '2'), true);
    assert.equal(global.draft, '1/3');
    assert.equal(http.sent.length, sent);

    model.applySpeed(global);
    const request = http.sent.at(-1);
    assert.equal(request.name, 'setGlobalSpeed');
    assert.deepEqual(request.args, { value: '1/3' });
    assert.equal(model.currentSpeedLabel(global), '2×');
    assert.equal(model.speedControlDisabled(global), true);
    assert.equal(model.speedControlDisabled(board), false);
    http.message({ action: 'results', results: [{ ...request, ok: true, value: {
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
    const http = gui.bootstrap({ speed: { global: { numerator: 1, denominator: 1 }, board: null } });
    assert.equal(model.currentSpeedLabel(board), '未进入关卡');
    assert.equal(model.speedControlDisabled(board), true);
    assert.equal(model.speedControlDisabled(global), false);

    const pushBoard = (revision, value) => http.message({
        action: 'sync', _clientId: 'client-1', revision, state: { speed: { board: value } },
    });
    pushBoard(2, { id: 1, numerator: 1, denominator: 1 });
    board.draft = '2/3';
    model.applySpeed(board);
    const request = http.sent.at(-1);
    assert.equal(request.name, 'setBoardSpeed');
    assert.deepEqual(request.args, { value: '2/3', boardId: 1 });
    pushBoard(4, { id: 2, numerator: 1, denominator: 1 });
    http.message({ action: 'results', results: [{ ...request, ok: true, value: {
        action: 'sync', revision: 3, state: { speed: { board: { id: 1, numerator: 2, denominator: 3 } } },
    } }] });
    assert.equal(model.currentSpeedLabel(board), '1×');
    assert.equal(board.current.id, 2);

    board.draft = '2/0';
    model.applySpeed(board);
    const invalid = http.sent.at(-1);
    http.message({ action: 'results', results: [{ ...invalid, ok: false, errortype: 'InvalidSpeed', error: 'invalid' }] });
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
    const http = gui.bootstrap();
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
        const request = http.sent.at(-1);
        assert.equal(request.kind, 'apply');
        assert.deepEqual(request.state, { placer: { [field]: value } });
    }
});

test('easy-place zoom mode has bilingual labels and uses existing state synchronization', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
    const zoom = gui.model.easyPlaceModeList.find(item => item.value === 'zoom');
    assert.equal(zoom.label, '放大模式');
    assert.equal(zoom.en, 'Zoom Mode');
    gui.model.setPlacerOption('easyPlaceMode', zoom.value);
    const request = http.sent.at(-1);
    assert.equal(request.kind, 'apply');
    assert.deepEqual(request.state, { placer: { easyPlaceMode: 'zoom' } });
    gui.connection.refreshState();
    const snapshot = http.sent.at(-1);
    http.message({ action: 'results', results: [{ ...snapshot, ok: true, value: {
        action: 'sync', revision: 2, state: { placer: { easyPlaceMode: 'zoom', active: false } },
    } }] });
    gui.flush();
    assert.equal(gui.model.easyPlaceMode.value, 'zoom');
});

test('quoted strings and line breaks remain action data', () => {
    const gui = loadGui();
    const http = gui.bootstrap();
    const code = "');globalThis.injected=true;#\\quoted\n\t中文";
    gui.model.lineupCode.value = code;
    gui.model.sendLineupCode();
    const request = http.sent.at(-1);
    assert.equal(request.name, 'applyLineup');
    assert.equal(request.args.code, code.trim());
    assert.equal(gui.context.injected, undefined);
});

const sync = (revision, state) => ({ action: 'sync', revision, state });
const completed = (request, value = null) => ({ ...request, ok: true, value });

test('HTTP startup waits for readiness and preserves PC restore and mobile pull', () => {
    for (const mobile of [false, true]) {
        const saved = { cheat: { freePlant: true, autoCollect: false }, placer: { imitater: true } };
        const gui = loadGui({ mobile, saved });
        gui.respondStatus({ ...readyStatus, ready: false });
        assert.equal(gui.http.sent.length, 0);
        gui.runTimer(100);
        const request = gui.startInitialization();
        assert.equal(request.kind, 'connect');
        assert.equal(request._clientId, 'client-1');
        assert.equal('state' in request, !mobile);
        if (!mobile) {
            assert.equal(request.state.cheat.freePlant, true);
            assert.equal(request.state.cheat.autoCollect, false);
            assert.equal(request.state.placer.imitater, true);
        }
        assert.equal(gui.model.connected.value, false);
        assert.equal(gui.lastRequest('request').options.headers['X-PGvZ-Instance'], readyStatus.instance);
        gui.http.message({ results: [completed(request, sync(1, { cheat: { freePlant: !mobile } }))] });
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.gameVersion.value, readyStatus.version);
        assert.equal(gui.model.modVersion.value, readyStatus.modVersion);
        assert.equal(gui.model.cheatOption.freePlant, !mobile);
        assert.equal(gui.sockets.length, 0);
        assert.ok(gui.requests.every(item => item.options.mode === 'same-origin'));
    }
});

test('startup failure shows the full traceback and exact supported versions without touching the queue', () => {
    const traceback = 'Traceback (most recent call last):\nNameError: name missing_name is not defined';
    for (const [version, supportedVersions, advice] of [
        ['1.2.6', readyStatus.supportedVersions, 'Please update the game.'],
        ['1.3.10', readyStatus.supportedVersions, 'Please download a newer version of the mod.'],
        ['1.4.0', ['1.3.10', '1.3.4'], 'Please download a newer version of the mod.'],
        ['1.3.9', ['1.3.10', '1.3.4'], 'Please update the game.'],
        ['1.3.4-beta', readyStatus.supportedVersions, 'Please update the game.'],
        ['1.3.4', readyStatus.supportedVersions, ''],
        ['1.3.5', [], ''],
        ['', readyStatus.supportedVersions, ''],
    ]) {
        const gui = loadGui();
        gui.model.sendAction('winLevel');
        gui.respondStatus({ ...readyStatus, version, supportedVersions, error: traceback });
        assert.match(gui.errors.at(-1), /finish initializing/);
        assert.equal(gui.model.lastResult.text, traceback);
        assert.equal(gui.model.connected.value, false);
        assert.equal(gui.model.gameVersion.value, version);
        assert.equal(gui.model.modVersion.value, readyStatus.modVersion);
        assert.equal(gui.model.unsupportedGameVersion.value, Boolean(advice));
        assert.equal(gui.model.unsupportedGameVersionDetail.value,
            advice ? `This mod supports game versions ${supportedVersions.join(', ')}. ${advice}` : '');
        assert.equal(gui.timers.size, 0);
        assert.equal(gui.requests.length, 1);
    }
});

test('poll merges initialization, action results and game changes by field revision', () => {
    const gui = loadGui();
    const connect = gui.startInitialization();
    gui.http.message({
        results: [completed(connect, sync(1, {
            cheat: { daisyMode: false, freePlant: true }, weather: { enabled: true, rain: false, storm: false },
        }))],
        updates: [sync(2, { cheat: { daisyMode: true } }), sync(3, { weather: { rain: true } })],
    });
    gui.flush();
    assert.equal(gui.model.cheatOption.daisyMode, true);
    assert.equal(gui.model.cheatOption.freePlant, true);
    assert.equal(gui.model.weather.value, 'rain');
    assert.equal(gui.http.sent.length, 1);

    gui.model.cheatOption.danceMode = true;
    gui.flush();
    const action = gui.http.sent.at(-1);
    const poll = gui.beginPoll();
    assert.equal(poll.payload.revision, 3);
    assert.deepEqual(poll.payload.acknowledged, [connect.id]);
    poll.respond({
        results: [completed(action, sync(5, { cheat: { danceMode: true } }))],
        updates: [sync(4, { cheat: { freePlant: false, danceMode: false } }),
            sync(6, { weather: { storm: true } })],
    });
    gui.settle();
    gui.flush();
    assert.equal(gui.model.cheatOption.freePlant, false);
    assert.equal(gui.model.cheatOption.danceMode, true);
    assert.equal(gui.model.weather.value, 'rainStorm');
    assert.equal(gui.http.sent.length, 2);
    assert.equal(JSON.parse(gui.storage.get(storageKey)).cheat.freePlant, false);
});

test('failed session initialization preserves saved settings and stops polling after acknowledgement', () => {
    const saved = { cheat: { freePlant: true } };
    const gui = loadGui({ saved });
    const request = gui.startInitialization();
    gui.http.message({ results: [{ ...request, ok: false, errortype: 'ValueError', error: 'bad setting' }] });
    assert.equal(gui.model.connectionState.value, 'error');
    assert.match(gui.model.lastResult.text, /bad setting/);
    const receipt = gui.beginPoll();
    assert.deepEqual(receipt.payload.acknowledged, [request.id]);
    receipt.respond({ results: [], updates: [] });
    gui.flush();
    assert.equal(gui.timers.size, 0);
    assert.deepEqual(JSON.parse(gui.storage.get(storageKey)), saved);
    assert.equal(gui.http.sent.length, 1);
});

test('submissions stay ordered and share one poll even if a submit reply stalls', () => {
    const gui = loadGui();
    gui.bootstrap();
    gui.deferSubmissions(true);
    gui.model.sendAction('winLevel');
    gui.model.sendAction('nextStage');
    assert.equal(gui.model.pendingCount.value, 2);
    const first = gui.lastRequest('request', true);
    assert.equal(first.payload.name, 'winLevel');
    const poll = gui.beginPoll();
    const count = gui.requests.length;
    gui.advance(600000);
    assert.equal(gui.requests.length, count);
    assert.equal(gui.model.connected.value, true);
    first.respond({ action: 'queued', id: first.payload.id });
    const second = gui.lastRequest('request', true);
    assert.equal(second.payload.name, 'nextStage');
    second.respond({ action: 'queued', id: second.payload.id });
    poll.respond({ results: [completed(first.payload)], updates: [] });
    gui.settle();
    assert.equal(gui.model.pendingCount.value, 1);
    gui.http.message({ results: [{ ...second.payload, ok: false, errortype: 'RuntimeError', error: 'No board' }] });
    assert.equal(gui.model.pendingCount.value, 0);
    assert.match(gui.model.lastResult.text, /No board/);
    const receiptPoll = gui.beginPoll();
    assert.deepEqual(receiptPoll.payload.acknowledged, [second.payload.id]);
    receiptPoll.respond({ results: [], updates: [] });
    gui.settle();
    assert.equal(gui.timers.values().next().value.delay, 1000);
});

test('pending operations survive empty polls during a long game pause without replay', () => {
    for (const mobile of [false, true]) {
        const gui = loadGui({ mobile, saved: { cheat: { freePlant: false } } });
        gui.bootstrap({ cheat: { freePlant: false } });
        gui.model.cheatOption.freePlant = true;
        gui.flush();
        const request = gui.http.sent.at(-1);
        assert.equal(JSON.parse(gui.storage.get(storageKey)).cheat.freePlant, !mobile);
        for (let i = 0; i < 3; i++) gui.http.message({});
        const blockedPoll = gui.beginPoll();
        const count = gui.requests.length;
        gui.advance(600000);
        assert.equal(gui.requests.length, count);
        assert.equal(gui.model.pendingCount.value, 1);
        blockedPoll.respond({ results: [completed(request)], updates: [] });
        gui.settle();
        assert.equal(gui.model.pendingCount.value, 0);
        assert.equal(gui.model.lastResult.key, 'messages.success');
        gui.http.message({ results: [completed(request)] });
        assert.deepEqual(gui.beginPoll().payload.acknowledged, [request.id]);
        assert.equal(gui.http.sent.filter(item => item.kind === 'apply').length, 1);
        assert.equal(gui.sockets.length, 0);
    }
});

test('network failure or a stale game instance reconnects without replaying actions', () => {
    for (const instanceChanged of [false, true]) {
        const gui = loadGui();
        gui.bootstrap();
        gui.model.sendAction('winLevel');
        const poll = gui.beginPoll();
        if (instanceChanged) poll.respond({ error: 'The game instance changed' }, 409);
        else poll.fail();
        gui.settle();
        assert.equal(gui.model.connected.value, false);
        assert.equal(gui.model.hasUnconfirmedRequests.value, true);
        assert.equal(gui.model.lastResult.key, 'messages.resultsUnconfirmed');
        assert.deepEqual([...gui.timers.values()].map(timer => timer.delay), [3000]);
        gui.runTimer(3000);
        gui.bootstrap();
        assert.equal(gui.model.connected.value, true);
        assert.equal(gui.model.hasUnconfirmedRequests.value, true);
        assert.deepEqual(gui.http.sent.map(request => request.kind), ['connect', 'action', 'connect']);
    }
});

test('two pages stay connected and apply shared changes without sending them back', () => {
    const first = loadGui();
    const second = loadGui({ clientId: 'client-2' });
    first.bootstrap({ cheat: { freePlant: false } });
    second.bootstrap({ cheat: { freePlant: false } });

    first.model.cheatOption.freePlant = true;
    first.flush();
    const request = first.http.sent.at(-1);
    const update = sync(2, { cheat: { freePlant: true } });
    first.http.message({ results: [completed(request, update)], updates: [update] });
    second.http.message({ updates: [update] });
    second.flush();
    assert.equal(first.model.connected.value, true);
    assert.equal(second.model.connected.value, true);
    assert.equal(second.model.cheatOption.freePlant, true);
    assert.equal(second.http.sent.length, 1);
    assert.equal(second.http.sent[0]._clientId, 'client-2');
    assert.equal('takeover' in second.http.sent[0], false);

    first.listeners.beforeunload();
    second.model.cheatOption.freePlant = false;
    second.flush();
    assert.equal(first.http.sent.at(-1).kind, 'release');
    assert.equal(second.http.sent.at(-1).kind, 'apply');
    assert.equal(second.model.connected.value, true);
});

test('page exit releases a ready session and ignores late startup replies', () => {
    const gui = loadGui();
    gui.startInitialization();
    gui.listeners.beforeunload();
    const request = gui.lastRequest('request');
    assert.equal(request.payload.kind, 'release');
    assert.equal(request.options.keepalive, true);
    assert.equal(gui.model.pendingCount.value, 0);
    assert.equal(gui.timers.size, 0);

    const loading = loadGui();
    loading.listeners.beforeunload();
    loading.respondStatus();
    assert.equal(loading.http.sent.length, 0);
    assert.equal(loading.timers.size, 0);
});

test('debug WebSocket opens on demand and its errors do not affect HTTP results', () => {
    const gui = loadGui();
    gui.bootstrap();
    gui.model.getLineupCode();
    const action = gui.http.sent.at(-1);
    assert.equal(gui.sockets.length, 0);
    gui.model.customCode.value = '1 / 0';
    gui.model.sendCustomCode();
    const socket = gui.sockets[0];
    socket.open();
    assert.match(socket.sent.at(-1), /from pgvztool import/);
    socket.message({ eventtype: 'execution', statuscode: 0, result: null });
    assert.equal(socket.sent.at(-1), '1 / 0');
    socket.message({ eventtype: 'execution', statuscode: -1, errortype: 'ZeroDivisionError', result: 'division by zero' });
    assert.match(gui.model.lastResult.text, /division by zero/);
    socket.close();
    assert.equal(gui.model.connected.value, true);
    assert.equal(gui.model.pendingCount.value, 1);
    gui.http.message({ results: [completed(action, 'lineup')] });
    assert.equal(gui.model.lineupCode.value, 'lineup');
});

test('custom Python remains available before HTTP initialization finishes', () => {
    const gui = loadGui();
    gui.model.customCode.value = '1 + 2';
    gui.model.sendCustomCode();
    const socket = gui.sockets[0];
    socket.open();
    assert.deepEqual(socket.sent, ['1 + 2']);
    socket.message({ eventtype: 'execution', statuscode: 0, result: '3' });
    assert.equal(gui.model.lastResult.text, '3');
    assert.equal(gui.http.sent.length, 0);
});

test('the Debug tab validates the entered port and switches connections on the next send', () => {
    const gui = loadGui();
    const { model, sockets } = gui;
    gui.context.location.search = '?ws=ws://localhost:9000/Py';
    assert.match(html, /<el-input-number v-model="debugPort" :min="debugPortMin" :max="debugPortMax"/);
    assert.equal(model.debugPort.value, 8080);
    assert.equal(model.debugPortMin, 8080);
    assert.equal(model.debugPortMax, 65535);
    assert.equal(model.t('fields.debugPort'), 'Python debug port');
    model.setLanguage('zh');
    assert.equal(model.t('fields.debugPort'), 'Python 调试端口');
    model.customCode.value = '1 + 2';
    for (const port of [null, 8079, 8080.5, 65536]) {
        model.debugPort.value = port;
        assert.match(model.debugPortError.value, /8080–65535/);
        model.sendCustomCode();
    }
    assert.equal(sockets.length, 0);

    model.debugPort.value = 8080;
    model.sendCustomCode();
    assert.equal(sockets[0].url, 'ws://localhost:8080/Py');
    sockets[0].open();
    assert.deepEqual(sockets[0].sent, ['1 + 2']);

    model.debugPort.value = 65535;
    model.customCode.value = '2 + 3';
    model.sendCustomCode();
    assert.equal(sockets[0].readyState, 3);
    assert.equal(sockets[1].url, 'ws://localhost:65535/Py');
    sockets[1].open();
    assert.deepEqual(sockets[1].sent, ['2 + 3']);
    sockets[1].message({ eventtype: 'execution', statuscode: 0, result: '5' });
    sockets[0].message({ eventtype: 'execution', statuscode: 0, result: '3' });
    assert.equal(model.lastResult.text, '5');
    model.sendCustomCode();
    assert.equal(sockets.length, 2);
});
