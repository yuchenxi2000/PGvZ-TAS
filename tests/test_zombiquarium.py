"""Native aquarium feeding can exceed three brains without bypassing payment."""
import ast
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = types.SimpleNamespace


class ZombiquariumTests(unittest.TestCase):
    def setUp(self):
        tree = ast.parse((ROOT / 'pgvztool/cheat.py').read_text(encoding='utf-8'))
        options = next(node for node in tree.body
                       if isinstance(node, ast.ClassDef) and node.name == 'CheatOption')
        initializer = next(node for node in options.body
                           if isinstance(node, ast.FunctionDef) and node.name == '__init__')
        namespace = {}
        exec(compile(ast.Module(body=[initializer], type_ignores=[]), 'options', 'exec'), namespace)
        self.options = NS()
        namespace['__init__'](self.options)
        self.constants = NS(IS=1, BOARD_EXTRA_ROOM=0)
        self.sun = 50
        self.brains = [(100, 100)] * 3
        self.payments = []
        self.board = NS(TakeSunMoney=self.take_sun)
        self.challenge = NS(mBoard=self.board, ZombiquariumDropBrain=self.drop_brain)
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        hook = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == 'Challenge__ZombiquariumMouseDown')
        hook.decorator_list = []
        namespace = {'cheat_option': self.options, 'Lawn': NS(Challenge=object),
                     'Sexy': NS(Constants=self.constants)}
        exec(compile(ast.Module(body=[hook], type_ignores=[]), 'aquarium-hook', 'exec'), namespace)
        self.hook = namespace[hook.name]

    def take_sun(self, amount):
        self.payments.append(amount)
        if self.sun < amount:
            return False
        self.sun -= amount
        return True

    def drop_brain(self, x, y):
        self.brains.append((x - 15, y - 15))

    def reject_original(self, *args):
        self.fail('enabled feeding must bypass the original three-brain cap')

    def test_disabled_by_default_and_restores_original_with_untouched_coordinates(self):
        self.assertFalse(self.options.zombiquariumNoBrainLimit)
        calls = []
        def original(*args):
            calls.append(args)
            return 'native'
        self.assertEqual(self.hook(original, self.challenge, 301, 201), 'native')
        self.options.zombiquariumNoBrainLimit = True
        self.hook(self.reject_original, self.challenge, 301, 201)
        self.options.zombiquariumNoBrainLimit = False
        self.assertEqual(self.hook(original, self.challenge, 303, 203), 'native')
        self.assertEqual(calls, [(self.challenge, 301, 201), (self.challenge, 303, 203)])
        self.assertEqual(len(self.brains), 4)

    def test_repeated_feeding_exceeds_three_and_ten_brains_with_one_payment_each(self):
        self.options.zombiquariumNoBrainLimit = True
        for _ in range(8):
            self.hook(self.reject_original, self.challenge, 300, 200)
        self.assertEqual(len(self.brains), 11)
        self.assertEqual(self.brains[-1], (285, 185))
        self.assertEqual(self.sun, 10)
        self.assertEqual(self.payments, [5] * 8)

    def test_insufficient_sun_does_not_drop_brain(self):
        self.options.zombiquariumNoBrainLimit = True
        self.sun = 4
        self.hook(self.reject_original, self.challenge, 300, 200)
        self.assertEqual(len(self.brains), 3)
        self.assertEqual(self.sun, 4)
        self.assertEqual(self.payments, [5])

    def test_scaled_click_and_extended_left_boundary_match_native_area(self):
        self.options.zombiquariumNoBrainLimit = True
        self.constants.IS = 1.875
        self.constants.BOARD_EXTRA_ROOM = 40
        self.hook(self.reject_original, self.challenge, 121, 157)
        self.assertEqual(self.brains[-1], (211, 279))
        self.constants.IS = 1
        for x, y in ((40, 90), (720, 430)):
            self.hook(self.reject_original, self.challenge, x, y)
            self.assertEqual(self.brains[-1], (x - 15, y - 15))
        for x, y in ((39, 90), (721, 430), (300, 89), (300, 431)):
            self.hook(self.reject_original, self.challenge, x, y)
        self.assertEqual(len(self.brains), 6)
        self.assertEqual(self.payments, [5] * 3)


if __name__ == '__main__':
    unittest.main()
