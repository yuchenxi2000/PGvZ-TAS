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

CUSTOM_ACTION_CHARS = {
    'glove':      '-',
    'easy_place': '=',
    'tas_save':    'u',
    'tas_undo':    'i',
    'tas_redo':    'o',
    'tas_advance': 'p',
}

_DEFAULT = {
    'pause':      ' ',
    'shovel':     '`',
    'glove':      CUSTOM_ACTION_CHARS['glove'],
    'easy_place': CUSTOM_ACTION_CHARS['easy_place'],
    'tas_save':    CUSTOM_ACTION_CHARS['tas_save'],
    'tas_undo':    CUSTOM_ACTION_CHARS['tas_undo'],
    'tas_redo':    CUSTOM_ACTION_CHARS['tas_redo'],
    'tas_advance': CUSTOM_ACTION_CHARS['tas_advance'],
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


_KEYCODE_CHARS = {
    9:   ('\t', '\t'),
    13:  ('\n', '\n'),
    32:  (' ', ' '),
    48:  ('0', ')'), 49: ('1', '!'), 50: ('2', '@'), 51: ('3', '#'), 52: ('4', '$'),
    53:  ('5', '%'), 54: ('6', '^'), 55: ('7', '&'), 56: ('8', '*'), 57: ('9', '('),
    106: ('*', '*'), 107: ('+', '+'), 109: ('-', '-'), 110: ('.', '.'), 111: ('/', '/'),
    186: (';', ':'), 187: ('=', '+'), 188: (',', '<'), 189: ('-', '_'),
    190: ('.', '>'), 191: ('/', '?'), 192: ('`', '~'), 219: ('[', '{'),
    220: ('\\', '|'), 221: (']', '}'), 222: ("'", '"'), 226: ('\\', '|'),
}


def _physical_keys(ch: str) -> 'tuple[tuple[int, bool], ...]':
    """返回字符对应的 ``(MonoGame KeyCode, Shift)`` 组合。"""
    lower = ch.lower()
    if len(ch) == 1 and 'a' <= lower <= 'z':
        keycode = ord(lower.upper())
        return ((keycode, False), (keycode, True))

    result = []
    for keycode, chars in _KEYCODE_CHARS.items():
        for shifted, key_ch in enumerate(chars):
            if ch == key_ch:
                result.append((keycode, bool(shifted)))
    if len(ch) == 1 and '0' <= ch <= '9':
        # 小键盘数字不受主键盘 Shift 字符层影响。
        numpad_keycode = 96 + int(ch)
        result.append((numpad_keycode, False))
        result.append((numpad_keycode, True))
    return tuple(result)


def build_physical_key_map() -> 'dict[tuple[int, bool], str]':
    """返回 ``{(KeyCode, Shift) -> 默认按键字符}`` 映射。

    Board 获得焦点时桌面文本组合会被关闭，因此所有受支持的 ASCII
    快捷键都从 MonoGame KeyDown 分发，不经过输入法。
    """
    result = {}
    # 未被重绑定的游戏原生快捷键也要走 KeyDown。
    for def_ch in _DEFAULT.values():
        for physical_key in _physical_keys(def_ch):
            result[physical_key] = def_ch

    binds = _load_config()
    for name, def_ch in _DEFAULT.items():
        cfg_ch = binds.get(name, def_ch)
        if cfg_ch == def_ch:
            continue
        for physical_key in _physical_keys(cfg_ch):
            result[physical_key] = def_ch
    return result


def build_physical_input_chars() -> 'set[str]':
    """返回已由 KeyDown 处理、应忽略后续 KeyChar 的输入字符。"""
    chars = set()
    binds = _load_config()
    for name, def_ch in _DEFAULT.items():
        for ch in (def_ch, binds.get(name, def_ch)):
            if _physical_keys(ch):
                chars.add(ch.lower() if ch.isalpha() else ch)
    return chars


def can_disable_text_composition() -> bool:
    """所有实际绑定均可物理映射时，Board 可以完全关闭文本组合。"""
    binds = _load_config()
    return all(_physical_keys(binds.get(name, def_ch)) for name, def_ch in _DEFAULT.items())
