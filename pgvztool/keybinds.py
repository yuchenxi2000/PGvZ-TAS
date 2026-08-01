"""
自定义快捷键功能
配置文件: {storagePath}/keybinds.txt，一行一个 key = value
"""
from pathlib import Path
import Sexy

_CONFIG_NAME = 'keybinds.txt'

_NAME_TO_CHAR = {
    'Space': ' ',
    'Tab':   '\t',
    'Enter': '\n',
}

_DEFAULT = {
    'pause':      ' ',
    'shovel':     '`',
    'accelerate': '\t',
    'seed_1':     '1',  'seed_2': '2',  'seed_3': '3',  'seed_4': '4',  'seed_5': '5',
    'seed_6':     '6',  'seed_7': '7',  'seed_8': '8',  'seed_9': '9',  'seed_10': '0',
    'cob_2_1':    'q',  'cob_2_2': 'w', 'cob_2_3': 'e',
    'cob_2_4':    'r',  'cob_2_5': 't', 'cob_2_6': 'y',
    'cob_4_1':    'a',  'cob_4_2': 's', 'cob_4_3': 'd',
    'cob_4_4':    'f',  'cob_4_5': 'g', 'cob_4_6': 'h',
    'cob_6_1':    'z',  'cob_6_2': 'x', 'cob_6_3': 'c',
    'cob_6_4':    'v',  'cob_6_5': 'b', 'cob_6_6': 'n',
}


def _parse_value(raw: str) -> 'str | None':
    val = raw.strip()
    if not val:
        return None
    if len(val) == 1:
        return val[0]
    return _NAME_TO_CHAR.get(val)


def _load_config() -> 'dict[str, str]':
    binds = dict(_DEFAULT)
    storage = Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath
    config_path = Path(storage) / _CONFIG_NAME
    if not config_path.is_file():
        return binds
    try:
        with open(str(config_path), 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            name, _, raw_val = line.partition('=')
            name = name.strip()
            if name not in _DEFAULT:
                continue
            ch = _parse_value(raw_val)
            if ch is not None:
                binds[name] = ch
    except Exception:
        import traceback
        Sexy.Debug.Log('[keybinds] config load error: ' + traceback.format_exc())
    return binds


def build_reverse_map() -> 'dict[str, str]':
    """返回 {用户按键 → 默认按键} 映射字典。
    只有配置值不同于默认值的条目才会出现在映射中。
    字母大小写均作为 key 加入（用户可能按大写或小写）。"""
    binds = _load_config()
    result = {}
    for name, def_ch in _DEFAULT.items():
        cfg_ch = binds.get(name, def_ch)
        if cfg_ch == def_ch:
            continue
        result[cfg_ch] = def_ch
        # 同时加入大小写变体
        if cfg_ch.isalpha():
            result[cfg_ch.swapcase()] = def_ch
    return result


def _physical_keycodes(ch: str) -> 'tuple[int, ...]':
    """返回 ASCII 字母或数字对应的 MonoGame KeyCode。"""
    lower = ch.lower()
    if len(ch) == 1 and 'a' <= lower <= 'z':
        return (ord(lower.upper()),)
    if len(ch) == 1 and '0' <= ch <= '9':
        # 顶排数字和 NumPad0~9。
        return (ord(ch), 96 + int(ch))
    return ()


def build_physical_key_map() -> 'dict[int, str]':
    """返回 {字母/数字 KeyCode -> 默认按键字符} 映射。

    字母和数字的 KeyChar 都可能被输入法截获，但 MonoGame 的 KeyDown
    仍会产生。标点依赖键盘布局和 Shift 状态，因此不在这里猜测。
    """
    result = {}
    # 未被重绑定的游戏原生字母和数字快捷键也要走 KeyDown。
    for def_ch in _DEFAULT.values():
        for keycode in _physical_keycodes(def_ch):
            result[keycode] = def_ch

    binds = _load_config()
    for name, def_ch in _DEFAULT.items():
        cfg_ch = binds.get(name, def_ch)
        if cfg_ch == def_ch:
            continue
        for keycode in _physical_keycodes(cfg_ch):
            result[keycode] = def_ch
    return result
