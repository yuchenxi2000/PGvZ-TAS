import ast
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeCoin:
    def __init__(self, board, value):
        self.mBoard = board
        self.value = value
        self.dead = False

    def IsSun(self):
        return self.value is not None

    def GetSunValue(self):
        return self.value


class SunLimitTests(unittest.TestCase):
    def setUp(self):
        self.board = types.SimpleNamespace(mSunMoney=9990, money=0)
        namespace = {'Serializable': object, 'GetBoard': lambda: self.board}
        tree = ast.parse((ROOT / 'pgvztool/cheat.py').read_text(encoding='utf-8'))
        options = next(node for node in tree.body
                       if isinstance(node, ast.ClassDef) and node.name == 'CheatOption')
        options.body = [node for node in options.body
                        if isinstance(node, ast.FunctionDef) and node.name in ('__init__', 'noSunLimit')]
        exec(compile(ast.Module(body=[options], type_ignores=[]), 'sun-options', 'exec'), namespace)
        self.options = namespace['CheatOption']()
        namespace = {
            'cheat_option': self.options,
            'Lawn': types.SimpleNamespace(Coin=FakeCoin),
        }
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        hook = next(node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name == 'Coin__ScoreCoin')
        hook.decorator_list = []
        exec(compile(ast.Module(body=[hook], type_ignores=[]), 'sun-hook', 'exec'), namespace)
        self.hook = namespace['Coin__ScoreCoin']
        self.calls = 0

    def original_score(self, coin):
        # Native ScoreCoin: retire the object, then score sunlight or coins.
        self.calls += 1
        coin.dead = True
        if coin.IsSun():
            coin.mBoard.mSunMoney = min(coin.mBoard.mSunMoney + coin.value, 9990)
        else:
            coin.mBoard.money += 1

    def test_disabled_uses_native_limit(self):
        coin = FakeCoin(self.board, 25)
        self.hook(self.original_score, coin)
        self.assertEqual(self.board.mSunMoney, 9990)
        self.assertTrue(coin.dead)
        self.assertEqual(self.calls, 1)

    def test_all_sun_sizes_accumulate_above_limit_and_keep_retirement(self):
        self.options.noSunLimit = True
        expected = self.board.mSunMoney
        for value in (5, 15, 25, 50):
            coin = FakeCoin(self.board, value)
            self.hook(self.original_score, coin)
            expected += value
            self.assertEqual(self.board.mSunMoney, expected)
            self.assertTrue(coin.dead)
        self.assertEqual(self.calls, 4)

    def test_non_sun_preserves_native_scoring_and_existing_sun(self):
        self.options.noSunLimit = True
        self.board.mSunMoney = 20000
        coin = FakeCoin(self.board, None)
        self.hook(self.original_score, coin)
        self.assertEqual(self.board.mSunMoney, 20000)
        self.assertEqual(self.board.money, 1)
        self.assertTrue(coin.dead)
        self.assertEqual(self.calls, 1)

    def test_int_storage_boundary(self):
        self.options.noSunLimit = True
        self.board.mSunMoney = 2147483640
        self.hook(self.original_score, FakeCoin(self.board, 25))
        self.assertEqual(self.board.mSunMoney, 2147483647)

    def test_turning_off_clamps_immediately_and_restores_native_collection(self):
        self.options.noSunLimit = True
        self.hook(self.original_score, FakeCoin(self.board, 25))
        self.assertEqual(self.board.mSunMoney, 10015)
        self.options.noSunLimit = False
        self.assertEqual(self.board.mSunMoney, 9990)
        self.hook(self.original_score, FakeCoin(self.board, 25))
        self.assertEqual(self.board.mSunMoney, 9990)

    def test_applying_false_again_also_clamps_existing_excess(self):
        self.board.mSunMoney = 20000
        self.options.noSunLimit = False
        self.assertEqual(self.board.mSunMoney, 9990)

    def test_applying_false_preserves_lower_balances(self):
        for balance in (-15, 0, 5000, 9990):
            with self.subTest(balance=balance):
                self.board.mSunMoney = balance
                self.options.noSunLimit = False
                self.assertEqual(self.board.mSunMoney, balance)

    def test_setting_option_without_board(self):
        self.board = None
        self.options.noSunLimit = True
        self.options.noSunLimit = False
        self.assertFalse(self.options.noSunLimit)


if __name__ == '__main__':
    unittest.main()
