import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_keybinds_module():
    sexy = types.ModuleType('Sexy')
    sys.modules['Sexy'] = sexy
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
        self.binds = dict(self.keybinds._DEFAULT)
        self.keybinds._load_config = lambda: self.binds

    def test_default_map_covers_letters_digits_controls_and_punctuation(self):
        physical = self.keybinds.build_physical_key_map()

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
        physical = self.keybinds.build_physical_key_map()

        self.assertEqual(physical[(ord('1'), True)], ' ')
        self.assertEqual(physical[(ord('1'), False)], '1')
        self.assertIn('!', self.keybinds.build_physical_input_chars())

    def test_common_ascii_bindings_allow_disabling_text_composition(self):
        # _load_config normally parses Enter to a newline before returning.
        self.binds['pause'] = '\n'
        self.binds['seed_1'] = '?'

        self.assertTrue(self.keybinds.can_disable_text_composition())

    def test_unmappable_unicode_binding_keeps_text_composition_fallback(self):
        self.binds['seed_1'] = '中'

        self.assertFalse(self.keybinds.can_disable_text_composition())


if __name__ == '__main__':
    unittest.main()
