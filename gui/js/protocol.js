window.PGvZProtocol = (() => {
    const BOOTSTRAP_READY_PROBE_CODE = [
        'import sys',
        '_pgvz_bootstrap_ready = sys.modules["cheat-gui"].bootstrap_status()[0]',
        "'{\"action\":\"bootstrapReady\",\"ready\":' + ('true' if _pgvz_bootstrap_ready else 'false') + '}'",
    ].join('\n');

    const BOOTSTRAP_CODE = [
        'import sys',
        '_pgvz_bootstrap_error = sys.modules["cheat-gui"].bootstrap_status()[1]',
        'if _pgvz_bootstrap_error is not None:',
        '    raise RuntimeError(_pgvz_bootstrap_error)',
        'try:',
        '    from pgvz import *',
        '    from pgvztool import *',
        '    import Lawn',
        '    import Sexy',
        '    import Sexy.TodLib',
        '    import LawnMod',
        '    import pgvz.lineup',
        'except Exception:',
        '    import traceback',
        '    raise RuntimeError(traceback.format_exc())',
    ].join('\n');

    const GAME_VERSION_PROBE_CODE = [
        'def _pgvz_gui_probe_game_version():',
        '    import json',
        '    import sys',
        '    version = ""',
        '    try:',
        '        import Lawn',
        '        version = Lawn.LawnApp.AppVersionNumber.split()[1]',
        '    except (ImportError, AttributeError, IndexError):',
        '        pass',
        '    version_module = sys.modules.get("pgvz.version")',
        '    if version_module is not None:',
        '        metadata = vars(version_module)',
        '    else:',
        // 后台加载失败或调试入口尚未导入时，单独读取版本声明。
        '        metadata = {}',
        '        try:',
        '            path = "mods/pgvz/version.py"',
        '            with open(path, "rb") as source:',
        '                exec(compile(source.read(), path, "exec"), metadata)',
        '        except (OSError, ValueError, SyntaxError):',
        '            pass',
        '    return json.dumps({"action": "gameVersion", "version": version,',
        '                       "modVersion": metadata.get("MOD_VERSION", ""),',
        '                       "supportedVersions": metadata.get("SUPPORTED_GAME_VERSIONS", [])})',
        '_pgvz_gui_probe_game_version()',
    ].join('\n');

    function pythonString(value) {
        return "'" + String(value)
            .replace(/\\/g, '\\\\')
            .replace(/'/g, "\\'")
            .replace(/\r/g, '\\r')
            .replace(/\n/g, '\\n')
            .replace(/\t/g, '\\t') + "'";
    }

    function requestCode(clientId, id, kind, details = {}) {
        const request = { ...details, _clientId: clientId, id, kind };
        return `gui_dispatcher.submit(${pythonString(JSON.stringify(request))})`;
    }

    function pollCode(clientId) {
        return `gui_dispatcher.poll(${pythonString(clientId)})`;
    }

    function acknowledgeCode(clientId, ids) {
        return `gui_dispatcher.acknowledge(${pythonString(clientId)}, ${pythonString(JSON.stringify(ids))})`;
    }

    function cancelCode(clientId, ids) {
        return `gui_dispatcher.cancel(${pythonString(clientId)}, ${pythonString(JSON.stringify(ids))})`;
    }

    function unwrapReprString(value) {
        if (typeof value !== 'string') return value;
        if ((value.startsWith("'") && value.endsWith("'")) || (value.startsWith('"') && value.endsWith('"'))) {
            const escapes = { '\\': '\\', "'": "'", '"': '"', n: '\n', r: '\r', t: '\t', b: '\b', f: '\f', v: '\v', a: '\x07' };
            return value.slice(1, -1).replace(/\\(\\|'|"|[nrtbfva]|x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|U[0-9a-fA-F]{8})/g,
                (_, escape) => escape in escapes ? escapes[escape] : String.fromCodePoint(parseInt(escape.slice(1), 16)));
        }
        return value;
    }

    function parseResultMessage(result) {
        if (!result) return null;
        try {
            return JSON.parse(unwrapReprString(result));
        } catch {
            return null;
        }
    }

    return {
        BOOTSTRAP_READY_PROBE_CODE,
        BOOTSTRAP_CODE,
        GAME_VERSION_PROBE_CODE,
        parseResultMessage,
        requestCode,
        pollCode,
        acknowledgeCode,
        cancelCode,
    };
})();
