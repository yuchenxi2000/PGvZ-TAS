// 自定义 Python 仍通过游戏原生调试服务执行，只有用户主动发送时才连接。
window.PGvZDebug = (() => {
    const MIN_PORT = 8080;
    const MAX_PORT = 65535;
    const IMPORT_HELPERS = [
        'from pgvz import *',
        'from pgvztool import *',
        'import Lawn, Sexy, Sexy.TodLib, LawnMod, pgvz.lineup',
    ].join('\n');

    function isValidPort(port) {
        return Number.isInteger(port) && port >= MIN_PORT && port <= MAX_PORT;
    }

    function create(setResult) {
        let socket = null;
        let timer = null;
        let awaiting = null;
        let helpersTried = false;
        let queued = [];

        function disconnect() {
            clearTimeout(timer);
            const previous = socket;
            socket = null;
            awaiting = null;
            helpersTried = false;
            queued = [];
            if (previous) previous.close();
        }

        function fail() {
            disconnect();
            setResult(false, 'messages.debugConnectionFailed');
        }

        function transmit(code) {
            try {
                socket.send(code);
            } catch {
                fail();
            }
        }

        function flush() {
            if (!socket || socket.readyState !== WebSocket.OPEN || awaiting || !queued.length) return;
            if (!helpersTried && queued[0].loadHelpers) {
                helpersTried = true;
                awaiting = 'helpers';
                transmit(IMPORT_HELPERS);
            } else {
                awaiting = 'code';
                transmit(queued.shift().code);
            }
        }

        function send(port, code, loadHelpers) {
            const url = `ws://localhost:${port}/Py`;
            if (socket && socket.url !== url) disconnect();
            queued.push({ code, loadHelpers });
            if (socket) {
                flush();
                return;
            }
            let current;
            try {
                current = new WebSocket(url);
            } catch {
                fail();
                return;
            }
            socket = current;
            timer = setTimeout(() => { if (socket === current) fail(); }, 30000);
            current.onopen = () => {
                if (socket !== current) return;
                clearTimeout(timer);
                flush();
            };
            current.onclose = current.onerror = () => { if (socket === current) fail(); };
            current.onmessage = event => {
                if (socket !== current) return;
                try {
                    const data = JSON.parse(event.data);
                    if (data.eventtype === 'output') return;
                    const response = awaiting;
                    awaiting = null;
                    if (response === 'code') {
                        if (data.statuscode === 0) {
                            setResult(true, data.result ? '' : 'messages.success', data.result || '');
                        } else {
                            setResult(false, data.errortype ? '' : 'messages.unknownError',
                                data.errortype ? `${data.errortype}: ${data.error ?? data.result ?? ''}` : '');
                        }
                    }
                    flush();
                } catch {
                    setResult(false, 'messages.unknownError');
                }
            };
        }

        return { send };
    }

    return { create, isValidPort, MIN_PORT, MAX_PORT };
})();
