// WebSocket 连接与统一请求结果回传。会话、状态和动作都由后端主线程分发器处理。
window.PGvZConnection = (() => {
    function create({ isMobile, t, setResult, getInitialState, applySyncState, lineupCode }) {
        const { ref } = Vue;
        const wsParams = new URLSearchParams(location.search);
        const SERVER_URL = wsParams.get('ws') || 'ws://localhost:8080/Py';
        const clientId = (globalThis.crypto && typeof globalThis.crypto.randomUUID === 'function')
            ? globalThis.crypto.randomUUID()
            : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
        const connected = ref(false);
        const sessionRejected = ref(false);
        const legacyGameVersionWarning = ref(false);
        const gameVersion = ref('');
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
        const pendingRequests = new Set();

        function showSessionRejected(showToast = true) {
            sessionRejected.value = true;
            connected.value = false;
            connectionState.value = 'occupied';
            pendingCodes = [];
            stopHeartbeat();
            stopResultPolling();
            resultPollInFlight = false;
            pendingRequests.clear();
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
            if (!connected.value && !allowBeforeReady) {
                pendingCodes.push(code);
                return true;
            }
            ws.send(code);
            if (!quiet) setResult(true, 'messages.sent');
            return true;
        }

        function send(code, allowBeforeReady = false) {
            return transmit(code, { allowBeforeReady });
        }

        function submit(kind, details = {}, options = {}) {
            const id = `${clientId}:${++requestCounter}`;
            let code = PGvZProtocol.requestCode(clientId, id, kind, details);
            if (options.bootstrap) code = `${PGvZProtocol.BOOTSTRAP_CODE}\n${code}`;
            if (transmit(code, options) && options.expectResult !== false) pendingRequests.add(id);
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
            if (!pendingRequests.size || !bootstrapStarted || !ws || ws.readyState !== WebSocket.OPEN || resultPollInFlight) return;
            resultPollTimer = setTimeout(() => {
                resultPollTimer = null;
                if (ws && ws.readyState === WebSocket.OPEN) {
                    resultPollInFlight = true;
                    ws.send(PGvZProtocol.pollCode(clientId));
                }
            }, 100);
        }

        function applyStateMessage(message) {
            if (message.action === 'sessionRejected') {
                showSessionRejected();
            } else if (message.action === 'sync' && message.state) {
                setResult(true, 'messages.syncOk');
                modVersion.value = String(message.modVersion || '');
                gameVersion.value = String(message.gameVersion || '');
                applySyncState(message.state);
                markConnected();
                startHeartbeat();
            }
        }

        function applyRequestResults(results) {
            for (const result of results) {
                if (!pendingRequests.delete(result.id)) continue;
                if (!result.ok) {
                    setResult(false, '', `${result.errortype}: ${result.error}`);
                    if (result.kind === 'connect') {
                        pendingCodes = [];
                        pendingRequests.clear();
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
            scheduleResultPoll();
        }

        function markConnected() {
            sessionRejected.value = false;
            connected.value = true;
            connectionState.value = 'connected';
            const queuedCodes = pendingCodes;
            pendingCodes = [];
            queuedCodes.forEach(code => transmit(code));
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
                            legacyGameVersionWarning.value = PGvZProtocol.isLegacyGameVersion(message.version);
                            startBootstrap();
                        } else if (message && message.action === 'queued') {
                            scheduleResultPoll();
                        } else if (message && message.action === 'results') {
                            resultPollInFlight = false;
                            applyRequestResults(message.results);
                        } else {
                            setResult(true, data.result ? '' : 'messages.success', data.result || '');
                        }
                    } else {
                        if (resultPollInFlight) {
                            resultPollInFlight = false;
                            pendingRequests.clear();
                            stopResultPolling();
                        }
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
                pendingRequests.clear();
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
                connected.value = false;
                connectionState.value = 'error';
            };
        }

        return {
            clientId, connected, sessionRejected, legacyGameVersionWarning,
            gameVersion, modVersion, connectionState,
            send, sendAction, applyState, refreshState, connect, releaseSession,
        };
    }

    return { create };
})();
