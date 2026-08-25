import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_keybinds_module():
    sexy = types.ModuleType('Sexy')
    sexy.WidgetManager = type('WidgetManager', (), {})
    sexy.Widget = type('Widget', (), {})
    sexy.KeyCode = type('KeyCode', (), {})
    sexy.SexyChar = type('SexyChar', (), {})
    sys.modules['Sexy'] = sexy
    lawn = types.ModuleType('Lawn')
    lawn.Board = type('Board', (), {})
    sys.modules['Lawn'] = lawn
    sys.modules['System'] = types.ModuleType('System')
    spec = importlib.util.spec_from_file_location(
        'test_keybinds_pgvztool.keybinds',
        ROOT / 'pgvztool' / 'keybinds.py',
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class KeybindPhysicalMapTests(unittest.TestCase):
    def setUp(self):
        self.keybinds = load_keybinds_module()
        self.binds = dict(self.keybinds.KeybindHandler.DEFAULT_BINDINGS)
        self.tas_manager = types.SimpleNamespace(
            ACTION_SAVE=0,
            ACTION_UNDO=1,
            ACTION_REDO=2,
            ACTION_ADVANCE=3,
        )

    def make_handler(self):
        return self.keybinds.KeybindHandler(None, None, self.tas_manager, self.binds)

    def test_default_map_covers_letters_digits_controls_and_punctuation(self):
        physical = self.make_handler()._physical_key_map

        self.assertEqual(physical[(ord('Q'), False)], 'q')
        self.assertEqual(physical[(ord('Q'), True)], 'q')
        self.assertEqual(physical[(ord('1'), False)], '1')
        self.assertEqual(physical[(97, False)], '1')
        self.assertEqual(physical[(97, True)], '1')
        self.assertEqual(physical[(32, False)], ' ')
        self.assertEqual(physical[(9, False)], '\t')
        self.assertEqual(physical[(192, False)], '`')
        self.assertEqual(physical[(189, False)], '-')
        self.assertEqual(physical[(187, False)], '=')

    def test_shifted_ascii_binding_uses_shift_specific_key(self):
        self.binds['pause'] = '!'
        handler = self.make_handler()
        physical = handler._physical_key_map

        self.assertEqual(physical[(ord('1'), True)], ' ')
        self.assertEqual(physical[(ord('1'), False)], '1')
        self.assertIn('!', handler._physical_input_chars)

    def test_common_ascii_bindings_allow_disabling_text_composition(self):
        # _load_config normally parses Enter to a newline before returning.
        self.binds['pause'] = '\n'
        self.binds['seed_1'] = '?'

        self.assertTrue(self.make_handler()._can_disable_text_composition)

    def test_unmappable_unicode_binding_keeps_text_composition_fallback(self):
        self.binds['seed_1'] = '中'

        self.assertFalse(self.make_handler()._can_disable_text_composition)

    def test_runtime_state_is_owned_by_each_handler(self):
        first = self.make_handler()
        second = self.make_handler()

        first._dispatching_physical_key = True
        first._desktop_board_ime_disabled = True

        self.assertFalse(second._dispatching_physical_key)
        self.assertFalse(second._desktop_board_ime_disabled)


if __name__ == '__main__':
    unittest.main()
