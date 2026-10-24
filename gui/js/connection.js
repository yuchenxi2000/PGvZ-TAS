// WebSocket 引导、GUI 会话、心跳和重连；界面状态同步通过回调交给 app.js。
window.PGvZConnection = (() => {
    function create({ isMobile, t, setResult, syncCheatOptions, applySyncState, lineupCode }) {
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

        function showSessionRejected(showToast = true) {
            sessionRejected.value = true;
            connected.value = false;
            connectionState.value = 'occupied';
            pendingCodes = [];
            setResult(false, 'messages.sessionOccupied');
            if (showToast) {
                ElementPlus.ElMessage.error(t('messages.sessionOccupied'));
            }
        }

        function send(code, allowBeforeReady = false) {
            if (sessionRejected.value && !allowBeforeReady) {
                showSessionRejected();
                return;
            }
            if (!ws || ws.readyState !== WebSocket.OPEN) {
                ElementPlus.ElMessage.error(t('messages.notConnected'));
                return;
            }
            if (!connected.value && !allowBeforeReady) {
                pendingCodes.push(code);
                return;
            }
            ws.send(allowBeforeReady
                ? code
                : `sync_reg.require_client('${clientId}')\n${code}`
            );
            setResult(true, 'messages.sent');
        }

        function markConnected() {
            sessionRejected.value = false;
            connected.value = true;
            connectionState.value = 'connected';
            const queuedCodes = pendingCodes;
            pendingCodes = [];
            queuedCodes.forEach(code => send(code));
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
                    ws.send(`sync_reg.heartbeat('${clientId}')`);
                }
            }, 3000);
        }

        function releaseSession() {
            if (ws && ws.readyState === WebSocket.OPEN && connected.value) {
                try {
                    ws.send(`sync_reg.release('${clientId}')`);
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
            if (isMobile) {
                send(`${PGvZProtocol.BOOTSTRAP_CODE}\nsync_reg.connect('${clientId}')`, true);
            } else {
                // 保证新游戏进程中先完成导入，再恢复网页保留的状态。
                syncCheatOptions(true);
            }
        }

        function connect() {
            ws = new WebSocket(SERVER_URL);
            ws.onopen = () => {
                stopBootstrapProbe();
                bootstrapStarted = false;
                connected.value = false;
                gameVersion.value = '';
                modVersion.value = '';
                connectionState.value = 'connecting';
                requestBootstrapReady();
            };
            ws.onmessage = event => {
                try {
                    const data = JSON.parse(event.data);
                    if (data.statuscode === 0) {
                        const msg = PGvZProtocol.parseResultMessage(data.result);
                        if (msg && msg.action === 'bootstrapReady') {
                            if (msg.ready) {
                                stopBootstrapProbe();
                                ws.send(PGvZProtocol.GAME_VERSION_PROBE_CODE);
                            } else {
                                retryBootstrapReady();
                            }
                            return;
                        }
                        if (msg && msg.action === 'heartbeat') {
                            return;
                        }
                        if (msg && msg.action === 'sessionRejected') {
                            stopHeartbeat();
                            showSessionRejected();
                            return;
                        }
                        if (msg && msg.action === 'gameVersion') {
                            legacyGameVersionWarning.value = PGvZProtocol.isLegacyGameVersion(msg.version);
                            startBootstrap();
                            return;
                        }
                        if (data.result) {
                            setResult(true, '', data.result);
                        } else {
                            setResult(true, 'messages.success');
                        }

                        if (msg && msg.action === 'sync' && msg.state) {
                            setResult(true, 'messages.syncOk');
                            modVersion.value = String(msg.modVersion || '');
                            gameVersion.value = String(msg.gameVersion || '');
                            applySyncState(msg.state);
                            markConnected();
                            startHeartbeat();
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
                stopBootstrapProbe();
                bootstrapStarted = false;
                stopHeartbeat();
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
            ws.onerror = () => {
                connected.value = false;
                connectionState.value = 'error';
            };
        }

        return {
            clientId, connected, sessionRejected, legacyGameVersionWarning,
            gameVersion, modVersion, connectionState,
            send, connect, releaseSession,
        };
    }

    return { create };
})();
