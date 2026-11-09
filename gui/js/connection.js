// WebSocket 连接与统一请求结果回传。会话、状态和动作都由后端主线程分发器处理。
window.PGvZConnection = (() => {
    const REQUEST_TIMEOUT_MS = 30000;
    const POLL_TIMEOUT_MS = 5000;
    function create({ isMobile, t, setResult, getInitialState, applySyncState, lineupCode }) {
        const { computed, ref } = Vue;
        const wsParams = new URLSearchParams(location.search);
        const SERVER_URL = wsParams.get('ws') || 'ws://localhost:8080/Py';
        const clientId = (globalThis.crypto && typeof globalThis.crypto.randomUUID === 'function')
            ? globalThis.crypto.randomUUID()
            : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
        const connected = ref(false);
        const sessionRejected = ref(false);
        const gameVersion = ref('');
        const supportedGameVersions = ref([]);
        const unsupportedGameVersion = computed(() => Boolean(gameVersion.value)
            && supportedGameVersions.value.length > 0 && !supportedGameVersions.value.includes(gameVersion.value));
        const modVersion = ref('');
        const connectionState = ref('disconnected');

        let ws = null;
        let pendingCodes = [];
        let heartbeatTimer = null;
        let bootstrapProbeTimer = null;
        let bootstrapStarted = false;
        let requestCounter = 0;
        let resultPollTimer = null;
        let resultPollInFlight = false;
        let resultPollDeadline = null;
        const pendingRequests = new Map();

        function showSessionRejected(showToast = true) {
            sessionRejected.value = true;
            connected.value = false;
            connectionState.value = 'occupied';
            pendingCodes = [];
            stopHeartbeat();
            stopResultPolling();
            resultPollInFlight = false;
            clearRequests();
            setResult(false, 'messages.sessionOccupied');
            if (showToast) ElementPlus.ElMessage.error(t('messages.sessionOccupied'));
        }

        function transmit(code, { allowBeforeReady = false, quiet = false, requestId = null } = {}) {
            if (sessionRejected.value && !allowBeforeReady) {
                showSessionRejected();
                return false;
            }
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                ElementPlus.ElMessage.error(t('messages.notConnected'));
                return false;
            }
            if (connectionState.value === 'error' && !allowBeforeReady) {
                ElementPlus.ElMessage.error(t('messages.notConnected'));
                return false;
            }
            if (!connected.value && !allowBeforeReady) {
                pendingCodes.push({ code, quiet, requestId });
                return true;
            }
            try {
                ws.send(code);
            } catch {
                ElementPlus.ElMessage.error(t('messages.notConnected'));
                return false;
            }
            if (!quiet) setResult(true, 'messages.sent');
            return true;
        }

        function send(code, allowBeforeReady = false) {
            return transmit(code, { allowBeforeReady });
        }

        function submit(kind, details = {}, options = {}) {
            if (sessionRejected.value && !options.allowBeforeReady) {
                showSessionRejected();
                return;
            }
            const id = `${clientId}:${++requestCounter}`;
            let code = PGvZProtocol.requestCode(clientId, id, kind, details);
            if (options.bootstrap) code = `${PGvZProtocol.BOOTSTRAP_CODE}\n${code}`;
            if (options.expectResult !== false) {
                pendingRequests.set(id, { kind, timer: setTimeout(() => requestTimedOut(id), REQUEST_TIMEOUT_MS) });
            }
            if (!transmit(code, { ...options, requestId: id })) finishRequest(id);
            scheduleResultPoll();
        }

        function finishRequest(id) {
            const request = pendingRequests.get(id);
            if (!request) return null;
            if (request.timer !== null) clearTimeout(request.timer);
            pendingRequests.delete(id);
            return request;
        }

        function cancelRequests(ids) {
            if (ids.length && ws && ws.readyState === WebSocket.OPEN) {
                try { ws.send(PGvZProtocol.cancelCode(clientId, ids)); } catch { /* socket closed */ }
            }
        }

        function clearRequests() {
            const ids = [...pendingRequests.keys()];
            ids.forEach(finishRequest);
            cancelRequests(ids);
            stopPollDeadline();
            resultPollInFlight = false;
        }

        function requestTimedOut(id) {
            const request = pendingRequests.get(id);
            if (!request) return;
            const sessionFailed = request.kind === 'connect' || request.kind === 'heartbeat';
            const ids = sessionFailed ? [...pendingRequests.keys()] : [id];
            ids.forEach(finishRequest);
            cancelRequests(ids);
            pendingCodes = pendingCodes.filter(item => !ids.includes(item.requestId));
            if (sessionFailed) {
                pendingCodes = [];
                connected.value = false;
                connectionState.value = 'error';
                stopHeartbeat();
            }
            setResult(false, 'messages.requestTimeout');
            scheduleResultPoll();
        }

        function sendAction(name, args = {}) {
            submit('action', { name, args });
        }

        function applyState(state) {
            submit('apply', { state });
        }

        function refreshState() {
            submit('snapshot');
        }

        function stopResultPolling() {
            if (resultPollTimer !== null) {
                clearTimeout(resultPollTimer);
                resultPollTimer = null;
            }
        }

        function stopPollDeadline() {
            if (resultPollDeadline !== null) {
                clearTimeout(resultPollDeadline);
                resultPollDeadline = null;
            }
        }

        function scheduleResultPoll() {
            stopResultPolling();
            // connect 的结果也要轮询，所以这里不能依赖 connected。
            if (!pendingRequests.size) {
                stopPollDeadline();
                resultPollInFlight = false;
                return;
            }
            if (!bootstrapStarted || !ws || ws.readyState !== WebSocket.OPEN || resultPollInFlight) return;
            resultPollTimer = setTimeout(() => {
                resultPollTimer = null;
                if (ws && ws.readyState === WebSocket.OPEN) {
                    resultPollInFlight = true;
                    try { ws.send(PGvZProtocol.pollCode(clientId)); } catch { /* deadline retries result polling */ }
                    resultPollDeadline = setTimeout(() => {
                        resultPollDeadline = null;
                        resultPollInFlight = false;
                        scheduleResultPoll(); // 只重试取结果，不重放副作用动作。
                    }, POLL_TIMEOUT_MS);
                }
            }, 100);
        }

        function applyStateMessage(message) {
            if (message.action === 'sessionRejected') {
                showSessionRejected();
            } else if (message.action === 'sync' && message.state) {
                setResult(true, 'messages.syncOk');
                applySyncState(message.state);
                markConnected();
                startHeartbeat();
            }
        }

        function applyRequestResults(results) {
            const acknowledged = [];
            for (const result of results) {
                acknowledged.push(result.id);
                if (!finishRequest(result.id)) continue;
                if (!result.ok) {
                    if (result.errortype === 'RequestExpired') setResult(false, 'messages.requestExpired');
                    else setResult(false, '', `${result.errortype}: ${result.error}`);
                    if (result.kind === 'connect') {
                        pendingCodes = [];
                        clearRequests();
                        connectionState.value = 'error';
                        stopHeartbeat();
                    }
                } else if (result.kind === 'connect' || result.kind === 'snapshot' || result.kind === 'heartbeat') {
                    applyStateMessage(result.value);
                } else if (result.kind === 'action' && result.name === 'getLineup') {
                    lineupCode.value = result.value;
                    setResult(true, 'messages.lineupOk');
                } else {
                    setResult(true, 'messages.success');
                }
            }
            if (acknowledged.length && ws && ws.readyState === WebSocket.OPEN) {
                try { ws.send(PGvZProtocol.acknowledgeCode(clientId, acknowledged)); } catch { /* cached results expire */ }
            }
            scheduleResultPoll();
        }

        function markConnected() {
            sessionRejected.value = false;
            connected.value = true;
            connectionState.value = 'connected';
            const queuedCodes = pendingCodes;
            pendingCodes = [];
            queuedCodes.forEach(({ code, quiet, requestId }) => transmit(code, { quiet, requestId }));
        }

        function stopHeartbeat() {
            if (heartbeatTimer !== null) {
                clearInterval(heartbeatTimer);
                heartbeatTimer = null;
            }
        }

        function startHeartbeat() {
            stopHeartbeat();
            heartbeatTimer = setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN && connected.value) {
                    submit('heartbeat', {}, { quiet: true });
                }
            }, 3000);
        }

        function releaseSession() {
            if (ws && ws.readyState === WebSocket.OPEN && connected.value) {
                try {
                    clearRequests();
                    pendingCodes = [];
                    submit('release', {}, { quiet: true, expectResult: false });
                } catch {
                    // 页面关闭期间 WebSocket 可能已经被浏览器释放。
                }
            }
        }

        function stopBootstrapProbe() {
            if (bootstrapProbeTimer !== null) {
                clearTimeout(bootstrapProbeTimer);
                bootstrapProbeTimer = null;
            }
        }

        function requestBootstrapReady() {
            stopBootstrapProbe();
            if (!ws || ws.readyState !== WebSocket.OPEN || bootstrapStarted) return;
            ws.send(PGvZProtocol.BOOTSTRAP_READY_PROBE_CODE);
        }

        function retryBootstrapReady() {
            stopBootstrapProbe();
            bootstrapProbeTimer = setTimeout(requestBootstrapReady, 100);
        }

        function startBootstrap() {
            if (bootstrapStarted || !ws || ws.readyState !== WebSocket.OPEN) return;
            stopBootstrapProbe();
            bootstrapStarted = true;
            const state = isMobile ? undefined : getInitialState();
            submit('connect', { state }, { allowBeforeReady: true, bootstrap: true });
        }

        function connect() {
            const socket = new WebSocket(SERVER_URL);
            ws = socket;
            socket.onopen = () => {
                stopBootstrapProbe();
                bootstrapStarted = false;
                connected.value = false;
                gameVersion.value = '';
                supportedGameVersions.value = [];
                modVersion.value = '';
                connectionState.value = 'connecting';
                requestBootstrapReady();
            };
            socket.onmessage = event => {
                if (ws !== socket) return;
                try {
                    const data = JSON.parse(event.data);
                    if (data.statuscode === 0) {
                        const message = PGvZProtocol.parseResultMessage(data.result);
                        if (message && message.action === 'bootstrapReady') {
                            if (message.ready) {
                                stopBootstrapProbe();
                                socket.send(PGvZProtocol.GAME_VERSION_PROBE_CODE);
                            } else {
                                retryBootstrapReady();
                            }
                        } else if (message && message.action === 'gameVersion') {
                            gameVersion.value = String(message.version || '');
                            modVersion.value = String(message.modVersion || '');
                            supportedGameVersions.value = Array.isArray(message.supportedVersions) ? message.supportedVersions : [];
                            startBootstrap();
                        } else if (message && message.action === 'queued') {
                            scheduleResultPoll();
                        } else if (message && (message.action === 'acknowledged' || message.action === 'cancelled')) {
                            // 仅确认传输层交接，不覆盖业务结果。
                        } else if (message && message.action === 'results') {
                            stopPollDeadline();
                            resultPollInFlight = false;
                            applyRequestResults(message.results);
                        } else {
                            setResult(true, data.result ? '' : 'messages.success', data.result || '');
                        }
                    } else {
                        // 原始调试代码的错误没有请求 ID，不能清空其他动作的等待状态。
                        if (data.errortype) setResult(false, '', `${data.errortype}: ${data.error || ''}`);
                        else setResult(false, 'messages.unknownError');
                    }
                } catch {
                    setResult(false, 'messages.unknownError');
                }
            };
            socket.onclose = () => {
                if (ws !== socket) return;
                stopBootstrapProbe();
                bootstrapStarted = false;
                stopHeartbeat();
                stopResultPolling();
                resultPollInFlight = false;
                clearRequests();
                pendingCodes = [];
                connected.value = false;
                gameVersion.value = '';
                modVersion.value = '';
                if (sessionRejected.value) {
                    connectionState.value = 'occupied';
                    return;
                }
                connectionState.value = 'reconnecting';
                setTimeout(connect, 3000);
            };
            socket.onerror = () => {
                if (ws !== socket) return;
                stopResultPolling();
                stopHeartbeat();
                clearRequests();
                pendingCodes = [];
                connected.value = false;
                connectionState.value = 'error';
            };
        }

        return {
            clientId, connected, sessionRejected, unsupportedGameVersion, supportedGameVersions,
            gameVersion, modVersion, connectionState,
            send, sendAction, applyState, refreshState, connect, releaseSession,
        };
    }

    return { create };
})();
