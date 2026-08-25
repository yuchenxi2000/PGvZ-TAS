"""
自定义快捷键功能
配置文件: {storagePath}/keybinds.txt，一行一个 key = value
"""
from pathlib import Path
import Lawn
import Sexy
import System


class KeybindHandler:
    """集中管理快捷键配置、物理按键分发和桌面输入法状态。"""

    CONFIG_NAME = 'keybinds.txt'
    NAME_TO_CHAR = {
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
    DEFAULT_BINDINGS = {
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
    KEYCODE_CHARS = {
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
    LEFT_SHIFT_KEYCODE = 160
    RIGHT_SHIFT_KEYCODE = 161

    def __init__(self, cheat_option, placer, tas_manager, bindings=None):
        self._cheat_option = cheat_option
        self._placer = placer
        self._tas_manager = tas_manager
        self._bindings = dict(bindings) if bindings is not None else self._load_config()
        self._key_reverse_map = self._build_reverse_map()
        self._physical_key_map = self._build_physical_key_map()
        self._physical_input_chars = self._build_physical_input_chars()
        self._can_disable_text_composition = self._all_bindings_are_physical()
        self._dispatching_physical_key = False
        self._desktop_board_ime_disabled = False
        self._tas_key_action_indices = {
            self.CUSTOM_ACTION_CHARS['tas_save']: tas_manager.ACTION_SAVE,
            self.CUSTOM_ACTION_CHARS['tas_undo']: tas_manager.ACTION_UNDO,
            self.CUSTOM_ACTION_CHARS['tas_redo']: tas_manager.ACTION_REDO,
            self.CUSTOM_ACTION_CHARS['tas_advance']: tas_manager.ACTION_ADVANCE,
        }

    @classmethod
    def _parse_value(cls, raw: str) -> 'str | None':
        val = raw.strip()
        if not val:
            return None
        if len(val) == 1:
            return val[0]
        return cls.NAME_TO_CHAR.get(val)

    def _load_config(self) -> 'dict[str, str]':
        bindings = dict(self.DEFAULT_BINDINGS)
        storage = Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath
        config_path = Path(storage) / self.CONFIG_NAME
        if not config_path.is_file():
            return bindings
        try:
            with open(str(config_path), 'r', encoding='utf-8') as config_file:
                lines = config_file.read().splitlines()
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                name, _, raw_val = line.partition('=')
                name = name.strip()
                if name not in self.DEFAULT_BINDINGS:
                    continue
                ch = self._parse_value(raw_val)
                if ch is not None:
                    bindings[name] = ch
        except Exception:
            import traceback
            Sexy.Debug.Log('[keybinds] config load error: ' + traceback.format_exc())
        return bindings

    def _build_reverse_map(self) -> 'dict[str, str]':
        """返回用户按键到游戏默认功能字符的映射。"""
        result = {}
        for name, default_ch in self.DEFAULT_BINDINGS.items():
            configured_ch = self._bindings.get(name, default_ch)
            if configured_ch == default_ch:
                continue
            result[configured_ch] = default_ch
            if configured_ch.isalpha():
                result[configured_ch.swapcase()] = default_ch
        return result

    @classmethod
    def _physical_keys(cls, ch: str) -> 'tuple[tuple[int, bool], ...]':
        """返回字符对应的 ``(MonoGame KeyCode, Shift)`` 组合。"""
        lower = ch.lower()
        if len(ch) == 1 and 'a' <= lower <= 'z':
            keycode = ord(lower.upper())
            return ((keycode, False), (keycode, True))

        result = []
        for keycode, chars in cls.KEYCODE_CHARS.items():
            for shifted, key_ch in enumerate(chars):
                if ch == key_ch:
                    result.append((keycode, bool(shifted)))
        if len(ch) == 1 and '0' <= ch <= '9':
            numpad_keycode = 96 + int(ch)
            result.append((numpad_keycode, False))
            result.append((numpad_keycode, True))
        return tuple(result)

    def _build_physical_key_map(self) -> 'dict[tuple[int, bool], str]':
        """返回物理按键到游戏默认功能字符的映射。"""
        result = {}
        # 游戏原生快捷键也要走 KeyDown，避免被输入法截获。
        for default_ch in self.DEFAULT_BINDINGS.values():
            for physical_key in self._physical_keys(default_ch):
                result[physical_key] = default_ch

        for name, default_ch in self.DEFAULT_BINDINGS.items():
            configured_ch = self._bindings.get(name, default_ch)
            if configured_ch == default_ch:
                continue
            for physical_key in self._physical_keys(configured_ch):
                result[physical_key] = default_ch
        return result

    def _build_physical_input_chars(self) -> 'set[str]':
        """返回已由 KeyDown 处理、应忽略后续 KeyChar 的输入字符。"""
        chars = set()
        for name, default_ch in self.DEFAULT_BINDINGS.items():
            for ch in (default_ch, self._bindings.get(name, default_ch)):
                if self._physical_keys(ch):
                    chars.add(ch.lower() if ch.isalpha() else ch)
        return chars

    def _all_bindings_are_physical(self) -> bool:
        return all(
            self._physical_keys(self._bindings.get(name, default_ch))
            for name, default_ch in self.DEFAULT_BINDINGS.items()
        )

    def _handle_custom_action(self, board: Lawn.Board, ch: str):
        """处理游戏没有原生 KeyChar 入口的快捷键。"""
        if ch == self.CUSTOM_ACTION_CHARS['glove']:
            is_level_glove = board.mApp.mGameScene == Lawn.GameScenes.Playing \
                and board.mApp.mGameMode not in (Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom) \
                and board.HasGlove()
            if is_level_glove and board.CanInteractWithBoardButtons() and board.CanUseGameObject(Lawn.GameObjectType.Glove):
                if board.mChallenge.mGloveCounter > 0:
                    board.mApp.PlaySample(Sexy.Resources.SOUND_BUZZER)
                else:
                    if board.mCursorObject.mCursorType != Lawn.CursorType.Shovel:
                        board.RefreshSeedPacketFromCursor()
                    board.PickUpTool(Lawn.GameObjectType.Glove)
            return True
        if ch == self.CUSTOM_ACTION_CHARS['easy_place']:
            if self._placer.can_toggle(board):
                self._placer.toggle()
            return True
        tas_action_index = self._tas_key_action_indices.get(ch)
        if tas_action_index is not None:
            if self._tas_manager.can_use(board, self._cheat_option.tasEnabled):
                self._tas_manager.run_action(tas_action_index)
            return True
        return False

    @staticmethod
    def _get_desktop_ime_handler(widget_manager: Sexy.WidgetManager):
        ime_handler = widget_manager.mIMEHandler
        if ime_handler is None or str(ime_handler.GetType().Name) != 'SdlIMEHandler':  # type: ignore
            return None
        return ime_handler

    def _disable_desktop_board_ime(self, widget_manager: Sexy.WidgetManager):
        """在 Board 接收物理快捷键期间关闭 SDL 文本组合。"""
        if self._desktop_board_ime_disabled or not self._can_disable_text_composition:
            return
        ime_handler = self._get_desktop_ime_handler(widget_manager)
        if ime_handler is None:
            return
        # MonoGame 启动时 SDL 文本输入可能已开启，但 IMEHandler.Enabled 仍为
        # False。先 Start 同步状态，再 Stop，确保实际关闭 SDL 文本组合。
        ime_handler.StartTextComposition()
        ime_handler.StopTextComposition()
        self._desktop_board_ime_disabled = True

    def _enable_desktop_ime(self, widget_manager: Sexy.WidgetManager):
        """离开 Board 后恢复菜单和文本框原有的文本输入。"""
        if not self._desktop_board_ime_disabled:
            return
        ime_handler = self._get_desktop_ime_handler(widget_manager)
        if ime_handler is not None:
            ime_handler.StartTextComposition()
        self._desktop_board_ime_disabled = False

    def _reset_desktop_ime_composition(self, board: Lawn.Board):
        """无法关闭文本组合时，保留旧的按键后清除组合串回退。"""
        ime_handler = self._get_desktop_ime_handler(board.mWidgetManager)
        if ime_handler is None:
            return
        ime_handler.StartTextComposition()
        ime_handler.StopTextComposition()
        ime_handler.StartTextComposition()

    def sync_desktop_ime_focus(self, widget_manager: Sexy.WidgetManager):
        if isinstance(widget_manager.mFocusWidget, Lawn.Board):
            self._disable_desktop_board_ime(widget_manager)
        else:
            self._enable_desktop_ime(widget_manager)

    def sync_desktop_ime_for_board(self, board: Lawn.Board):
        """在处理类加载晚于 Board 获得焦点时完成首次状态同步。"""
        if board.mWidgetManager.mFocusWidget == board:
            self._disable_desktop_board_ime(board.mWidgetManager)

    def set_focus(self, orig, widget_manager: Sexy.WidgetManager, widget: Sexy.Widget):
        orig(widget_manager, widget)
        self.sync_desktop_ime_focus(widget_manager)

    def got_focus(self, orig, widget_manager: Sexy.WidgetManager):
        orig(widget_manager)
        self.sync_desktop_ime_focus(widget_manager)

    def key_down(self, orig, board: Lawn.Board, the_key: Sexy.KeyCode):
        """用物理键触发快捷键，绕过输入法对 KeyChar 的截获。"""
        orig(board, the_key)
        keycode = int(the_key)
        key_down = board.mWidgetManager.mKeyDown
        shift_down = bool(
            key_down[self.LEFT_SHIFT_KEYCODE]
            or key_down[self.RIGHT_SHIFT_KEYCODE]
        )
        mapped = self._physical_key_map.get((keycode, shift_down))
        if mapped is None:
            return
        self._dispatching_physical_key = True
        try:
            board.KeyChar(Sexy.SexyChar(System.Char(ord(mapped))))  # type: ignore
        finally:
            self._dispatching_physical_key = False
        if not self._can_disable_text_composition and ord('A') <= keycode <= ord('Z'):
            self._reset_desktop_ime_composition(board)

    def key_char(self, orig, board: Lawn.Board, the_char: Sexy.SexyChar):
        ch = str(the_char.value_type)
        if self._dispatching_physical_key:
            # KeyDown 传入的已经是默认功能字符，不能再次经过自定义映射。
            if self._handle_custom_action(board, ch):
                return
            orig(board, the_char)
            return
        # 未关闭文本组合的平台仍可能在 KeyDown 后产生 KeyChar，需避免重复触发。
        normalized_ch = ch.lower() if ch.isalpha() else ch
        if normalized_ch in self._physical_input_chars:
            return
        mapped = self._key_reverse_map.get(ch)
        if mapped is not None:
            ch = mapped
            the_char = Sexy.SexyChar(System.Char(ord(mapped)))  # type: ignore
        if self._handle_custom_action(board, ch):
            return
        orig(board, the_char)
