window.PGvZProtocol = (() => {
    const BOOTSTRAP_READY_PROBE_CODE = [
        'import Sexy',
        "'{\"action\":\"bootstrapReady\",\"ready\":' + ('true' if Sexy.GlobalStaticVars.gSexyAppBase is not None and Sexy.GlobalStaticVars.gSexyAppBase.mLoadingThreadStarted else 'false') + '}'",
    ].join('\n');

    const BOOTSTRAP_CODE = [
        'from pgvz import *',
        'from pgvztool import *',
        'import Lawn',
        'import Sexy',
        'import Sexy.TodLib',
        'import LawnMod',
        'import pgvz.lineup',
    ].join('\n');

    const GAME_VERSION_PROBE_CODE = [
        'import Lawn',
        "'{\"action\":\"gameVersion\",\"version\":\"' + Lawn.LawnApp.AppVersionNumber + '\"}'",
    ].join('\n');

    function pyBool(value) {
        return value ? 'True' : 'False';
    }

    function unwrapReprString(value) {
        if (typeof value !== 'string') return value;
        if ((value.startsWith("'") && value.endsWith("'")) || (value.startsWith('"') && value.endsWith('"'))) {
            return value.slice(1, -1);
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

    function isLegacyGameVersion(versionLabel) {
        const match = String(versionLabel || '').match(/(\d+)\.(\d+)\.(\d+)/);
        if (!match) return false;
        const major = Number(match[1]);
        const minor = Number(match[2]);
        return major < 1 || (major === 1 && minor < 3);
    }

    return {
        BOOTSTRAP_READY_PROBE_CODE,
        BOOTSTRAP_CODE,
        GAME_VERSION_PROBE_CODE,
        isLegacyGameVersion,
        parseResultMessage,
        pyBool,
    };
})();
