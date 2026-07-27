window.PGvZProtocol = (() => {
    const BOOTSTRAP_CODE = [
        'from pgvz import *',
        'from pgvztool import *',
        'import Lawn',
        'import Sexy',
        'import Sexy.TodLib',
        'import LawnMod',
        'import pgvz.lineup',
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

    return {
        BOOTSTRAP_CODE,
        parseResultMessage,
        pyBool,
    };
})();
