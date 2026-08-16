import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeGameMode:
    Adventure = 0
    ChallengeIce = 1
    ChallengeZenGarden = 2
    TreeOfWisdom = 3
    ChallengeZombiquarium = 4


class FakeApp:
    def __init__(self):
        self.mGameMode = FakeGameMode.Adventure
        self.whack = False
        self.final_boss = False

    def IsWhackAZombieLevel(self):
        return self.whack

    def IsFinalBossLevel(self):
        return self.final_boss

    def IsIZombieLevel(self):
        return False

    def IsSquirrelLevel(self):
        return False

    def IsScaryPotterLevel(self):
        return False


class FakeBoard:
    def __init__(self, num_waves=40):
        self.mGameID = 1
        self.mLevel = 1
        self.mBoardRandSeed = 2
        self.mChallenge = types.SimpleNamespace(mSurvivalStage=0)
        self.mMainCounter = 0
        self.mCurrentWave = 0
        self.mNumWaves = num_waves
        self.mZombieCountDown = 1800
        self.mZombieCountDownStart = 1800
        self.mHugeWaveCountDown = 0
        self.mZombieHealthToNextWave = -1

    def IsFlagWave(self, wave_index):
        return wave_index % 10 == 9


def load_time_operation():
    lawn = types.ModuleType('Lawn')
    lawn.Board = FakeBoard
    lawn.GameMode = FakeGameMode
    sys.modules['Lawn'] = lawn

    sexy = types.ModuleType('Sexy')
    sexy.Debug = types.SimpleNamespace(Log=lambda message: None)
    sys.modules['Sexy'] = sexy

    package = types.ModuleType('test_pgvz')
    package.__path__ = [str(ROOT / 'pgvz')]
    sys.modules['test_pgvz'] = package

    gvar = types.SimpleNamespace(timePassed=False, doPassedOp=False)
    global_var = types.ModuleType('test_pgvz.global_var')
    global_var.gvar = gvar
    sys.modules['test_pgvz.global_var'] = global_var

    context = {'app': FakeApp(), 'board': FakeBoard()}
    util = types.ModuleType('test_pgvz.util')
    util.GetBoard = lambda: context['board']
    util.GetLawnApp = lambda: context['app']
    sys.modules['test_pgvz.util'] = util

    spec = importlib.util.spec_from_file_location(
        'test_pgvz.time_operation', ROOT / 'pgvz' / 'time_operation.py')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, context, gvar


class WaveClockTests(unittest.TestCase):
    def setUp(self):
        self.time_operation, self.context, self.gvar = load_time_operation()

    def test_first_wave_uses_live_countdown(self):
        board = self.context['board']
        snapshot = self.time_operation.wave_clock.Snapshot(board)
        board.mMainCounter = 1
        board.mZombieCountDown = 1799

        self.time_operation.wave_clock.ObserveUpdate(board, snapshot)

        self.assertEqual(
            self.time_operation.wave_clock.GetThresholdRefreshPoint(board, 1),
            1800,
        )

    def test_normal_threshold_jump_records_deadline(self):
        board = self.context['board']
        board.mCurrentWave = 1
        board.mZombieHealthToNextWave = 100
        board.mMainCounter = 100
        board.mZombieCountDown = 1000
        snapshot = self.time_operation.wave_clock.Snapshot(board)

        board.mMainCounter = 101
        board.mZombieCountDown = 200
        self.time_operation.wave_clock.ObserveUpdate(board, snapshot)

        self.assertEqual(
            self.time_operation.wave_clock.GetThresholdRefreshPoint(board, 2),
            301,
        )

    def test_thirtieth_wave_uses_runtime_huge_countdown(self):
        board = self.context['board']
        board.mCurrentWave = 29
        board.mZombieHealthToNextWave = 0
        board.mMainCounter = 100
        board.mZombieCountDown = 6
        snapshot = self.time_operation.wave_clock.Snapshot(board)

        board.mMainCounter = 101
        board.mZombieCountDown = 5
        board.mHugeWaveCountDown = 820
        self.time_operation.wave_clock.ObserveUpdate(board, snapshot)

        self.assertEqual(
            self.time_operation.wave_clock.GetThresholdRefreshPoint(board, 30),
            921,
        )

    def test_spawn_transition_records_exact_refresh_point(self):
        board = self.context['board']
        board.mCurrentWave = 1
        board.mMainCounter = 300
        board.mZombieCountDown = 1
        snapshot = self.time_operation.wave_clock.Snapshot(board)

        board.mMainCounter = 301
        board.mCurrentWave = 2
        board.mZombieCountDown = 2800
        board.mZombieCountDownStart = 2800
        self.time_operation.wave_clock.ObserveUpdate(board, snapshot)

        self.assertEqual(
            self.time_operation.wave_clock.GetRefreshPoint(board, 2), 301)

        # 下一波倒计时已经从 2800 跳到 200；Prejudge 仍应使用记录的 301，
        # 不能再用 2800 - 200 反推。
        board.mMainCounter = 501
        board.mZombieCountDown = 200
        generator = self.time_operation.Prejudge(300, 2)
        next(generator)
        self.assertEqual(self.time_operation.refresh_point, 301)

    def test_natural_countdown_to_stable_range_records_threshold(self):
        board = self.context['board']
        board.mCurrentWave = 1
        board.mZombieHealthToNextWave = 100
        board.mMainCounter = 100
        board.mZombieCountDown = 201
        snapshot = self.time_operation.wave_clock.Snapshot(board)

        board.mMainCounter = 101
        board.mZombieCountDown = 200
        self.time_operation.wave_clock.ObserveUpdate(board, snapshot)

        self.assertEqual(
            self.time_operation.wave_clock.GetThresholdRefreshPoint(board, 2),
            301,
        )

    def test_invalid_wave_finishes_without_waiting(self):
        board = self.context['board']
        generator = self.time_operation.Prejudge(0, board.mNumWaves + 1)

        with self.assertRaises(StopIteration):
            next(generator)
        self.assertTrue(self.gvar.timePassed)

    def test_nonstandard_spawning_mode_is_rejected(self):
        self.context['app'].whack = True
        generator = self.time_operation.Prejudge(0, 1)

        with self.assertRaises(StopIteration):
            next(generator)
        self.assertTrue(self.gvar.timePassed)


if __name__ == '__main__':
    unittest.main()
