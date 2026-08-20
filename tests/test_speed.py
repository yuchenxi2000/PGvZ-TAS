import importlib.util
import math
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeGlobalStaticVars:
    gFastMo = False
    gSlowMo = False
    gFastSlowMoNum = 0
    gSlowMoCounter = 0


class FakeBoard:
    def __init__(self):
        self.mAccelerationNumerator = 1
        self.mAccelerationDenominator = 1
        self.mAccelerationFrameIndex = 0


def load_speed_module():
    lawn = types.ModuleType('Lawn')
    lawn.Board = FakeBoard
    sys.modules['Lawn'] = lawn

    sexy = types.ModuleType('Sexy')
    sexy.GlobalStaticVars = FakeGlobalStaticVars
    sys.modules['Sexy'] = sexy

    package = types.ModuleType('test_speed_pgvz')
    package.__path__ = [str(ROOT / 'pgvz')]
    sys.modules['test_speed_pgvz'] = package

    context = {'board': FakeBoard()}
    util = types.ModuleType('test_speed_pgvz.util')
    util.GetBoard = lambda: context['board']
    sys.modules['test_speed_pgvz.util'] = util

    spec = importlib.util.spec_from_file_location(
        'test_speed_pgvz.speed', ROOT / 'pgvz' / 'speed.py'
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, context


class GlobalSpeedTests(unittest.TestCase):
    def setUp(self):
        self.speed, _ = load_speed_module()
        FakeGlobalStaticVars.gFastMo = False
        FakeGlobalStaticVars.gSlowMo = False
        FakeGlobalStaticVars.gFastSlowMoNum = 0
        FakeGlobalStaticVars.gSlowMoCounter = 7

    def test_get_global_speed_uses_game_defaults_and_priority(self):
        self.assertEqual(self.speed.GetGlobalSpeedExact(), (True, 1))
        self.assertEqual(self.speed.GetGlobalSpeed(), 1.0)

        FakeGlobalStaticVars.gSlowMo = True
        self.assertEqual(self.speed.GetGlobalSpeedExact(), (False, 4))
        self.assertEqual(self.speed.GetGlobalSpeed(), 0.25)

        FakeGlobalStaticVars.gFastMo = True
        FakeGlobalStaticVars.gFastSlowMoNum = 3
        self.assertEqual(self.speed.GetGlobalSpeedExact(), (False, 3))
        self.assertAlmostEqual(self.speed.GetGlobalSpeed(), 1.0 / 3.0)

        FakeGlobalStaticVars.gSlowMo = False
        FakeGlobalStaticVars.gFastSlowMoNum = 0
        self.assertEqual(self.speed.GetGlobalSpeedExact(), (True, 20))
        self.assertEqual(self.speed.GetGlobalSpeed(), 20.0)

    def test_get_global_speed_rejects_invalid_raw_factor(self):
        FakeGlobalStaticVars.gFastMo = True
        FakeGlobalStaticVars.gFastSlowMoNum = -1
        with self.assertRaises(ValueError):
            self.speed.GetGlobalSpeedExact()

    def test_exact_fast_speed_sets_raw_state(self):
        result = self.speed.SetGlobalSpeedExact(True, 5)

        self.assertEqual(result, (True, 5))
        self.assertTrue(FakeGlobalStaticVars.gFastMo)
        self.assertFalse(FakeGlobalStaticVars.gSlowMo)
        self.assertEqual(FakeGlobalStaticVars.gFastSlowMoNum, 5)
        self.assertEqual(FakeGlobalStaticVars.gSlowMoCounter, 0)

    def test_exact_slow_speed_sets_raw_state(self):
        result = self.speed.SetGlobalSpeedExact(False, 4)

        self.assertEqual(result, (False, 4))
        self.assertFalse(FakeGlobalStaticVars.gFastMo)
        self.assertTrue(FakeGlobalStaticVars.gSlowMo)
        self.assertEqual(FakeGlobalStaticVars.gFastSlowMoNum, 4)

    def test_float_conversion_uses_original_rounding_rule(self):
        self.assertEqual(self.speed.SetGlobalSpeed(1.6), (True, 2))
        self.assertEqual(self.speed.SetGlobalSpeed(0.3), (False, 3))
        self.assertEqual(self.speed.SetGlobalSpeed(1.0), (True, 1))

    def test_global_speed_range_is_inclusive(self):
        self.assertEqual(self.speed.SetGlobalSpeed(0.01), (False, 100))
        self.assertEqual(self.speed.SetGlobalSpeed(100), (True, 100))

    def test_global_speed_rejects_invalid_values(self):
        for value in (0.009, 101, float('nan'), float('inf')):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    self.speed.SetGlobalSpeed(value)
        with self.assertRaises(TypeError):
            self.speed.SetGlobalSpeed('2')
        with self.assertRaises(TypeError):
            self.speed.SetGlobalSpeedExact(1, 2)
        with self.assertRaises(ValueError):
            self.speed.SetGlobalSpeedExact(True, 0)


class BoardSpeedTests(unittest.TestCase):
    def setUp(self):
        self.speed, self.context = load_speed_module()

    def test_get_board_speed_returns_raw_and_float_values(self):
        board = self.context['board']
        board.mAccelerationNumerator = 6
        board.mAccelerationDenominator = 4

        self.assertEqual(self.speed.GetBoardSpeedExact(), (6, 4))
        self.assertEqual(self.speed.GetBoardSpeed(), 1.5)

        other_board = FakeBoard()
        other_board.mAccelerationNumerator = 2
        other_board.mAccelerationDenominator = 3
        self.assertEqual(self.speed.GetBoardSpeedExact(other_board), (2, 3))
        self.assertAlmostEqual(self.speed.GetBoardSpeed(other_board), 2.0 / 3.0)

    def test_get_board_speed_rejects_zero_denominator(self):
        board = self.context['board']
        board.mAccelerationNumerator = 1
        board.mAccelerationDenominator = 0

        self.assertEqual(self.speed.GetBoardSpeedExact(), (1, 0))
        with self.assertRaises(ValueError):
            self.speed.GetBoardSpeed()

    def test_exact_speed_preserves_requested_fraction(self):
        board = self.context['board']
        board.mAccelerationFrameIndex = 3

        result = self.speed.SetBoardSpeedExact(6, 4)

        self.assertEqual(result, (6, 4))
        self.assertEqual(board.mAccelerationNumerator, 6)
        self.assertEqual(board.mAccelerationDenominator, 4)
        self.assertEqual(board.mAccelerationFrameIndex, 0)

    def test_exact_speed_accepts_range_boundaries(self):
        self.assertEqual(self.speed.SetBoardSpeedExact(1, 100), (1, 100))
        self.assertEqual(self.speed.SetBoardSpeedExact(100, 1), (100, 1))

    def test_float_speed_uses_continued_fraction(self):
        self.assertEqual(self.speed.SetBoardSpeed(1.5), (3, 2))

        numerator, denominator = self.speed.SetBoardSpeed(
            math.sqrt(2.0),
            max_error=1e-6,
        )
        self.assertLess(
            abs(float(numerator) / denominator - math.sqrt(2.0)),
            1e-6,
        )

    def test_missing_board_raises(self):
        self.context['board'] = None
        with self.assertRaises(RuntimeError):
            self.speed.SetBoardSpeedExact(1, 1)
        with self.assertRaises(RuntimeError):
            self.speed.GetBoardSpeedExact()

    def test_exact_speed_rejects_invalid_fraction(self):
        for numerator, denominator in ((0, 1), (1, 0), (1, 101), (101, 1)):
            with self.subTest(numerator=numerator, denominator=denominator):
                with self.assertRaises(ValueError):
                    self.speed.SetBoardSpeedExact(numerator, denominator)
        with self.assertRaises(TypeError):
            self.speed.SetBoardSpeedExact(1.0, 2)
        with self.assertRaises(OverflowError):
            self.speed.SetBoardSpeedExact(499999, 5000)

    def test_float_speed_rejects_invalid_error(self):
        for error in (0, -1e-6, float('nan'), float('inf')):
            with self.subTest(error=error):
                with self.assertRaises(ValueError):
                    self.speed.SetBoardSpeed(1.5, max_error=error)

    def test_failed_approximation_does_not_modify_board(self):
        board = self.context['board']
        board.mAccelerationNumerator = 2
        board.mAccelerationDenominator = 3
        board.mAccelerationFrameIndex = 1

        with self.assertRaises(OverflowError):
            self.speed.SetBoardSpeed(math.sqrt(2.0), max_error=1e-20)

        self.assertEqual(board.mAccelerationNumerator, 2)
        self.assertEqual(board.mAccelerationDenominator, 3)
        self.assertEqual(board.mAccelerationFrameIndex, 1)


if __name__ == '__main__':
    unittest.main()
