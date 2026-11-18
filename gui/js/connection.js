// WebSocket 连接与统一请求结果回传。会话、状态和动作都由后端主线程分发器处理。
window.PGvZConnection = (() => {
    const HANDSHAKE_TIMEOUT_MS = 30000;
    const RECONNECT_DELAY_MS = 3000;
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
        const pendingCount = ref(0);
        const hasUnconfirmedRequests = ref(false);

        let ws = null;
        let bootstrapProbeTimer = null;
        let bootstrapStarted = false;
        let bootstrapFailed = false;
        let takeoverOnConnect = false;
        let reconnectTimer = null;
        let connectionAttemptTimer = null;
        let leavingPage = false;
        let requestCounter = 0;
        let resultPollTimer = null;
        let resultPollInFlight = false;
        const pendingRequests = new Map();

        function showSessionRejected(showToast = true) {
            stopReconnect();
            stopConnectionAttempt();
            stopBootstrapProbe();
            sessionRejected.value = true;
            connected.value = false;
            connectionState.value = 'occupied';
            stopResultPolling();
            resultPollInFlight = false;
            clearRequests();
            setResult(false, 'messages.sessionOccupied');
            if (showToast) ElementPlus.ElMessage.error(t('messages.sessionOccupied'));
        }

        function transmit(code, { allowBeforeReady = false, quiet = false } = {}) {
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
                ElementPlus.ElMessage.error(t('messages.notReady'));
                return false;
            }
            try {
                ws.send(code);
            } catch {
                retryConnection();
                ElementPlus.ElMessage.error(t('messages.notConnected'));
                return false;
            }
            if (!quiet) setResult(true, 'messages.sent');
            return true;
        }

        function send(code, allowBeforeReady = false) {
            if (allowBeforeReady) bootstrapFailed = false;
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
                pendingRequests.set(id, { kind });
                pendingCount.value = pendingRequests.size;
            }
            if (!transmit(code, options)) finishRequest(id);
            scheduleResultPoll();
        }

        function finishRequest(id) {
            const request = pendingRequests.get(id);
            if (!request) return null;
            pendingRequests.delete(id);
            pendingCount.value = pendingRequests.size;
            return request;
        }

        function cancelRequests(ids) {
            if (ids.length && ws && ws.readyState === WebSocket.OPEN) {
                try { ws.send(PGvZProtocol.cancelCode(clientId, ids)); } catch { /* socket closed */ }
            }
        }

        function clearRequests(cancel = true) {
            const ids = [...pendingRequests.keys()];
            ids.forEach(finishRequest);
            if (cancel) cancelRequests(ids);
            resultPollInFlight = false;
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

        function scheduleResultPoll() {
            stopResultPolling();
            // connect 的结果也要轮询，所以这里不能依赖 connected。
            if (!pendingRequests.size) {
                resultPollInFlight = false;
                return;
            }
            if (!bootstrapStarted || !ws || ws.readyState !== WebSocket.OPEN || resultPollInFlight) return;
            resultPollTimer = setTimeout(() => {
                resultPollTimer = null;
                if (ws && ws.readyState === WebSocket.OPEN) {
                    resultPollInFlight = true;
                    // 后台暂停可能连 poll 都不能处理；收到响应前不再堆积轮询。
                    try { ws.send(PGvZProtocol.pollCode(clientId)); } catch { retryConnection(); }
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
            }
        }

        function applyRequestResults(results) {
            const acknowledged = [];
            for (const result of results) {
                acknowledged.push(result.id);
                if (!finishRequest(result.id)) continue;
                if (!result.ok) {
                    if (result.errortype === 'SessionRejected') {
                        showSessionRejected();
                        break;
                    }
                    setResult(false, '', `${result.errortype}: ${result.error}`);
                    if (result.kind === 'connect') {
                        stopConnectionAttempt();
                        clearRequests();
                        connectionState.value = 'error';
                    }
                } else if (result.kind === 'connect' || result.kind === 'snapshot') {
                    applyStateMessage(result.value);
                    if (sessionRejected.value) break;
                } else if (result.kind === 'action' && result.name === 'getLineup') {
                    lineupCode.value = result.value;
                    setResult(true, 'messages.lineupOk');
                } else {
                    setResult(true, 'messages.success');
                }
            }
            if (acknowledged.length && ws && ws.readyState === WebSocket.OPEN) {
                try { ws.send(PGvZProtocol.acknowledgeCode(clientId, acknowledged)); } catch { retryConnection(); }
            }
            scheduleResultPoll();
        }

        function markConnected() {
            stopConnectionAttempt();
            stopReconnect();
            sessionRejected.value = false;
            connected.value = true;
            connectionState.value = 'connected';
        }

        function releaseSession() {
            leavingPage = true;
            stopReconnect();
            stopConnectionAttempt();
            stopBootstrapProbe();
            stopResultPolling();
            if (ws && ws.readyState === WebSocket.OPEN && bootstrapStarted && !bootstrapFailed) {
                try {
                    clearRequests();
                    submit('release', {}, { allowBeforeReady: true, quiet: true, expectResult: false });
                } catch {
                    // 页面关闭期间 WebSocket 可能已经被浏览器释放。
                }
            }
            clearRequests(false);
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
            transmit(PGvZProtocol.BOOTSTRAP_READY_PROBE_CODE, { allowBeforeReady: true, quiet: true });
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
            const details = takeoverOnConnect ? { state, takeover: true } : { state };
            takeoverOnConnect = false;
            submit('connect', details, { allowBeforeReady: true, bootstrap: true });
        }

        function takeoverSession() {
            if (!sessionRejected.value) return;
            sessionRejected.value = false;
            connectionState.value = 'initializing';
            if (ws && ws.readyState === WebSocket.OPEN && bootstrapStarted) {
                submit('connect', { state: isMobile ? undefined : getInitialState(), takeover: true },
                    { allowBeforeReady: true });
            } else {
                takeoverOnConnect = true;
                connect();
            }
        }

        function stopReconnect() {
            if (reconnectTimer !== null) {
                clearTimeout(reconnectTimer);
                reconnectTimer = null;
            }
        }

        function stopConnectionAttempt() {
            if (connectionAttemptTimer !== null) {
                clearTimeout(connectionAttemptTimer);
                connectionAttemptTimer = null;
            }
        }

        function retryConnection() {
            stopConnectionAttempt();
            stopBootstrapProbe();
            stopResultPolling();
            if ([...pendingRequests.values()].some(request => request.kind === 'action' || request.kind === 'apply')) {
                hasUnconfirmedRequests.value = true;
                setResult(false, 'messages.resultsUnconfirmed');
            }
            // 断线不等于执行失败；既不重放动作，也不假定 cancel 能送达。
            clearRequests(false);
            bootstrapStarted = false;
            connected.value = false;
            gameVersion.value = '';
            modVersion.value = '';
            const previousSocket = ws;
            ws = null; // 旧连接的迟到消息及 close/error 事件不能干扰新连接。
            if (previousSocket) {
                try { previousSocket.close(); } catch { /* retry on a new socket */ }
            }
            if (sessionRejected.value || leavingPage) {
                if (sessionRejected.value) connectionState.value = 'occupied';
                return;
            }
            connectionState.value = 'reconnecting';
            if (reconnectTimer === null) {
                reconnectTimer = setTimeout(() => {
                    reconnectTimer = null;
                    connect();
                }, RECONNECT_DELAY_MS);
            }
        }

        function connect() {
            if (leavingPage) return;
            if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) return;
            stopReconnect();
            stopConnectionAttempt();
            const socket = new WebSocket(SERVER_URL);
            ws = socket;
            connectionState.value = 'connecting';
            // 只限制 WebSocket 握手；打开后允许游戏无限期暂停。
            connectionAttemptTimer = setTimeout(() => {
                connectionAttemptTimer = null;
                retryConnection();
            }, HANDSHAKE_TIMEOUT_MS);
            socket.onopen = () => {
                if (ws !== socket || leavingPage) return;
                stopConnectionAttempt();
                stopBootstrapProbe();
                bootstrapStarted = false;
                bootstrapFailed = false;
                connected.value = false;
                gameVersion.value = '';
                supportedGameVersions.value = [];
                modVersion.value = '';
                connectionState.value = 'initializing';
                setResult(true, 'messages.waiting');
                requestBootstrapReady();
            };
            socket.onmessage = event => {
                if (ws !== socket || leavingPage) return;
                try {
                    const data = JSON.parse(event.data);
                    if (data.statuscode === 0) {
                        const message = PGvZProtocol.parseResultMessage(data.result);
                        if (message && message.action === 'bootstrapReady') {
                            if (message.ready) {
                                stopBootstrapProbe();
                                transmit(PGvZProtocol.GAME_VERSION_PROBE_CODE, { allowBeforeReady: true, quiet: true });
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
                            resultPollInFlight = false;
                            applyRequestResults(message.results);
                        } else {
                            setResult(true, data.result ? '' : 'messages.success', data.result || '');
                        }
                    } else {
                        // 原始调试代码的错误没有请求 ID，不能清空其他动作的等待状态。
                        if (bootstrapFailed) return; // 保留第一次导入错误，忽略已发出轮询的后续错误。
                        // 首次导入失败时分发器可能还不存在，停止轮询且不发送 cancel。
                        if (!connected.value && connectionState.value === 'initializing') {
                            stopConnectionAttempt();
                            stopBootstrapProbe();
                            bootstrapFailed = true;
                            clearRequests(false);
                            stopResultPolling();
                            connectionState.value = 'error';
                        }
                        if (data.errortype) setResult(false, '', `${data.errortype}: ${data.error ?? data.result ?? ''}`);
                        else setResult(false, 'messages.unknownError');
                    }
                } catch {
                    setResult(false, 'messages.unknownError');
                }
            };
            socket.onclose = () => {
                if (ws !== socket) return;
                retryConnection();
            };
            socket.onerror = () => {
                if (ws !== socket) return;
                retryConnection();
            };
        }

        return {
            clientId, connected, sessionRejected, unsupportedGameVersion, supportedGameVersions,
            gameVersion, modVersion, connectionState,
            pendingCount, hasUnconfirmedRequests,
            send, sendAction, applyState, refreshState, connect, releaseSession, takeoverSession,
        };
    }

    return { create };
})();
