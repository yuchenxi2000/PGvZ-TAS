// 普通请求和状态同步使用网页同源的 HTTP 接口。
window.PGvZConnection = (() => {
    const ACTIVE_POLL_MS = 100;
    const IDLE_POLL_MS = 1000;
    const RECONNECT_MS = 3000;

    function create({ isMobile, t, setResult, getInitialState, applySyncState, lineupCode, onActionResult }) {
        const { computed, ref } = Vue;
        const clientId = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(16).slice(2)}`;
        const connected = ref(false);
        const gameVersion = ref('');
        const supportedGameVersions = ref([]);
        const unsupportedGameVersion = computed(() => Boolean(gameVersion.value)
            && supportedGameVersions.value.length > 0 && !supportedGameVersions.value.includes(gameVersion.value));
        const modVersion = ref('');
        const connectionState = ref('disconnected');
        const pendingCount = ref(0);
        const hasUnconfirmedRequests = ref(false);

        const pending = new Map();
        const acknowledged = new Set();
        const stateRevisions = new Map();
        let updateRevision = 0;
        let instance = null;
        let generation = 0;
        let timer = null;
        let pollInFlight = false;
        let requestCounter = 0;
        let submissions = Promise.resolve();
        let leaving = false;

        async function api(path, payload, keepalive = false) {
            const options = { mode: 'same-origin', cache: 'no-store' };
            if (payload) Object.assign(options, {
                method: 'POST', keepalive, body: JSON.stringify(payload),
                headers: { 'Content-Type': 'application/json', 'X-PGvZ-Instance': instance },
            });
            const response = await fetch('/api/' + path, options);
            if (!response.ok) {
                const data = await response.json().catch(() => ({}));
                const error = new Error(data.error || `HTTP ${response.status}`);
                error.status = response.status;
                throw error;
            }
            return response.json();
        }

        function makeRequest(kind, details) {
            return { ...details, _clientId: clientId, id: `${clientId}:${++requestCounter}`, kind };
        }

        function clearTimer() {
            clearTimeout(timer);
            timer = null;
        }

        function schedule(fn, delay) {
            clearTimer();
            timer = setTimeout(() => {
                timer = null;
                fn();
            }, delay);
        }

        function clearPending() {
            pending.clear();
            pendingCount.value = 0;
        }

        function handleFailure(error, expectedGeneration) {
            if (leaving || expectedGeneration !== generation) return;
            generation++;
            clearTimer();
            if ([...pending.values()].some(kind => kind === 'action' || kind === 'apply')) {
                hasUnconfirmedRequests.value = true;
                setResult(false, 'messages.resultsUnconfirmed');
            }
            clearPending();
            acknowledged.clear();
            connected.value = false;
            instance = null;
            pollInFlight = false;
            submissions = Promise.resolve();
            updateRevision = 0;
            stateRevisions.clear();
            if (connectionState.value === 'error') return;
            if (error.status && error.status !== 409 && error.status !== 503) {
                connectionState.value = 'error';
                setResult(false, '', error.message);
                return;
            }
            gameVersion.value = '';
            modVersion.value = '';
            supportedGameVersions.value = [];
            connectionState.value = 'reconnecting';
            schedule(connect, RECONNECT_MS);
        }

        async function connect() {
            if (leaving) return;
            connectionState.value = 'initializing';
            const expectedGeneration = generation;
            try {
                const status = await api('status');
                if (leaving || expectedGeneration !== generation) return;
                gameVersion.value = status.version || '';
                modVersion.value = status.modVersion || '';
                supportedGameVersions.value = status.supportedVersions || [];
                if (status.error) {
                    connectionState.value = 'error';
                    setResult(false, '', status.error);
                } else if (!status.ready) {
                    schedule(connect, ACTIVE_POLL_MS);
                } else {
                    instance = status.instance;
                    const state = isMobile ? undefined : getInitialState();
                    submit('connect', { state }, true);
                }
            } catch (error) {
                handleFailure(error, expectedGeneration);
            }
        }

        function submit(kind, details = {}, initializing = false) {
            if (!connected.value && !initializing) {
                ElementPlus.ElMessage.error(t('messages.notReady'));
                return false;
            }
            if (leaving) return false;
            const request = makeRequest(kind, details);
            const expectedGeneration = generation;
            pending.set(request.id, kind);
            pendingCount.value = pending.size;
            setResult(true, initializing ? 'messages.waiting' : 'messages.sent');
            // HTTP 请求可能经不同连接抵达，按页面提交顺序入队。
            submissions = submissions.then(() => {
                if (leaving || expectedGeneration !== generation || !pending.has(request.id)) return;
                return api('request', request);
            }).catch(error => {
                if (pending.has(request.id)) handleFailure(error, expectedGeneration);
            });
            if (pending.size === 1) schedulePoll();
            return true;
        }

        function sendAction(name, args = {}) {
            return submit('action', { name, args });
        }

        function applyState(state) {
            return submit('apply', { state });
        }

        function refreshState() {
            return submit('snapshot');
        }

        function schedulePoll() {
            if (leaving || !instance || pollInFlight) return;
            if (pending.size || acknowledged.size) schedule(poll, ACTIVE_POLL_MS);
            else if (connected.value) schedule(poll, IDLE_POLL_MS);
        }

        async function poll() {
            pollInFlight = true;
            const expectedGeneration = generation;
            const delivered = [...acknowledged];
            try {
                const response = await api('poll', {
                    _clientId: clientId, revision: updateRevision,
                    acknowledged: delivered,
                });
                if (leaving || expectedGeneration !== generation) return;
                delivered.forEach(id => acknowledged.delete(id));
                applyRequestResults(response.results);
                if (connected.value) {
                    for (const message of response.updates) {
                        if (receiveSync(message)) updateRevision = Math.max(updateRevision, message.revision);
                    }
                }
            } catch (error) {
                handleFailure(error, expectedGeneration);
            } finally {
                if (expectedGeneration === generation) {
                    pollInFlight = false;
                    schedulePoll();
                }
            }
        }

        function receiveSync({ state, revision }) {
            if (!Number.isSafeInteger(revision) || revision < 1 || !state
                || typeof state !== 'object' || Array.isArray(state)) return false;
            const changes = Object.create(null);
            for (const [group, fields] of Object.entries(state)) {
                if (!fields || typeof fields !== 'object' || Array.isArray(fields)) continue;
                if (!stateRevisions.has(group)) stateRevisions.set(group, new Map());
                const revisions = stateRevisions.get(group);
                for (const [key, value] of Object.entries(fields)) {
                    if (revision <= (revisions.get(key) ?? 0)) continue;
                    revisions.set(key, revision);
                    (changes[group] ??= Object.create(null))[key] = value;
                }
            }
            if (Object.keys(changes).length) applySyncState(changes);
            return true;
        }

        function applyRequestResults(results) {
            for (const result of results) {
                acknowledged.add(result.id);
                if (!pending.delete(result.id)) continue;
                pendingCount.value = pending.size;
                if (result.errortype === 'SessionRejected' && result.kind !== 'connect') {
                    handleFailure(new Error(result.error), generation);
                    return;
                }
                if (result.ok && result.value?.action === 'sync') {
                    if (receiveSync(result.value) && result.kind === 'connect') {
                        updateRevision = result.value.revision;
                    }
                }
                const errorKey = result.kind === 'action' ? onActionResult(result) : '';
                if (!result.ok) {
                    setResult(false, errorKey || '', `${result.errortype}: ${result.error}`);
                    if (result.kind === 'connect') {
                        connectionState.value = 'error';
                        clearPending();
                    }
                } else if (result.kind === 'connect' || result.kind === 'snapshot') {
                    connected.value = true;
                    connectionState.value = 'connected';
                    setResult(true, 'messages.syncOk');
                } else if (result.kind === 'action' && result.name === 'getLineup') {
                    lineupCode.value = result.value;
                    setResult(true, 'messages.lineupOk');
                } else {
                    setResult(true, 'messages.success');
                }
            }
        }

        function releaseSession() {
            if (leaving) return;
            leaving = true;
            clearTimer();
            if (instance) {
                api('request', makeRequest('release'), true).catch(() => {});
            }
            clearPending();
        }

        return {
            clientId, connected, unsupportedGameVersion, supportedGameVersions,
            gameVersion, modVersion, connectionState, pendingCount, hasUnconfirmedRequests,
            sendAction, applyState, refreshState, connect, releaseSession,
        };
    }

    return { create };
})();
