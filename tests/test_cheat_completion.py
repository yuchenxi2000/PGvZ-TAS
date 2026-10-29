import ast
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeCutScene:
    def __init__(self, choosing):
        self.mSeedChoosing = choosing
        self.time = 100 if choosing else 0

    def EndSeedChooser(self):
        self.mSeedChoosing = False

    def StartLevelIntro(self):
        # The game reuses this object and does not reset mSeedChoosing here.
        self.time = 0

    def Update(self):
        if not self.mSeedChoosing:
            self.time += 10


class FakeBoard:
    def __init__(self, app, stage):
        self.app = app
        self.mChallenge = types.SimpleNamespace(mSurvivalStage=stage)
        self.mNumWaves = self.GetNumWavesPerSurvivalStage()
        self.mCurrentWave = 0
        self.mBoardFadeOutCounter = -1
        self.mNextSurvivalStageCounter = 0
        self.mLevelComplete = False
        self.mCutScene = FakeCutScene(app.mSeedChooserScreen is not None)

    def GetNumWavesPerSurvivalStage(self):
        if self.app.mode == 'normal':
            return 10
        if self.app.mode == 'hell' and self.mChallenge.mSurvivalStage >= 3:
            return 30
        return 20

    def IsFinalSurvivalStage(self):
        if self.app.component is not None:
            return (not self.app.component.mEndless
                    and self.mChallenge.mSurvivalStage == self.app.component.mStages - 1)
        return self.app.mode in ('normal', 'hard', 'hell') and self.mChallenge.mSurvivalStage >= 4

    def FadeOutLevel(self):
        if self.app.mGameScene != 'Playing':
            self.mLevelComplete = True
        elif self.app.IsSurvivalMode() and not self.IsFinalSurvivalStage():
            self.mNextSurvivalStageCounter = 500
        else:
            self.mBoardFadeOutCounter = 600

    def GetSurvivalFlagsCompleted(self):
        # Mirror native score accounting, including the last-flag deduction.
        flags = self.mChallenge.mSurvivalStage * self.GetNumWavesPerSurvivalStage() // 10
        if self.app.mode == 'hell' and self.mChallenge.mSurvivalStage >= 3:
            flags -= 3
        wave = self.mCurrentWave
        if wave % 10 == 0 and wave > 0 and self.mBoardFadeOutCounter < 0 and self.mNextSurvivalStageCounter == 0:
            wave -= 1
        return flags + wave // 10


class FakeComponents:
    def __init__(self, component):
        self.component = component

    def __getitem__(self, component_type):
        return lambda: self.component


class FakeApp:
    def __init__(self, mode='normal', stage=0, choosing=False, component=None):
        self.mode = mode
        self.component = component
        self.mGameMode = mode
        self.mGameScene = 'LevelIntro' if choosing else 'Playing'
        self.mSeedChooserScreen = object() if choosing else None
        self.mCreativeLevel = (types.SimpleNamespace(GetComponent=FakeComponents(component))
                               if component is not None else None)
        self.record = 0
        self.first_completion = False
        self.dialogs = []
        self.mBoard = FakeBoard(self, stage)

    def IsSurvivalMode(self):
        return self.mode != 'izombie'

    def IsSurvivalEndless(self, mode):
        return mode == 'endless'

    def IsIZombieLevel(self):
        return self.mode == 'izombie'

    def KillDialog(self, dialog):
        self.dialogs.append(dialog)

    def finish_native_transition(self):
        board = self.mBoard
        # Finish the countdown; an intro completes immediately but can still
        # receive multiple updates before CheckForGameEnd when using speedup.
        for _ in range(4 if board.mLevelComplete else 600):
            if board.mBoardFadeOutCounter >= 0:
                board.mBoardFadeOutCounter -= 1
            if board.mNextSurvivalStageCounter > 0:
                board.mNextSurvivalStageCounter -= 1
        if board.IsFinalSurvivalStage():
            target = 5 if self.mode == 'normal' else 10
            self.first_completion = self.record < target
            self.record = max(self.record, board.GetSurvivalFlagsCompleted())
        else:
            # CheckForGameEnd kills/recreates the chooser, then InitSurvivalStage
            # calls StartLevelIntro on the existing CutScene.
            board.mChallenge.mSurvivalStage += 1
            self.mSeedChooserScreen = object()
            self.mGameScene = 'LevelIntro'
            board.mCutScene.StartLevelIntro()


def load_actions(app):
    # Load real domain methods without .NET imports or unrelated script registration.
    namespace = {
        'Lawn': types.SimpleNamespace(LawnApp=FakeApp, Board=FakeBoard,
                                     Creative=types.SimpleNamespace(CSSurvivalLevel=object)),
        'GetLawnApp': lambda: app,
        'IterAliveZombies': lambda: [],
    }
    source = ast.parse((ROOT / 'pgvztool/cheat_actions.py').read_text(encoding='utf-8'))
    cls = next(node for node in source.body if isinstance(node, ast.ClassDef) and node.name == 'CheatActions')
    cls.body = [node for node in cls.body if isinstance(node, ast.FunctionDef)
                and node.name in ('__init__', '_WinLevel', 'WinLevel', 'NextStage')]
    exec(compile(ast.Module(body=[cls], type_ignores=[]), 'cheat-actions', 'exec'), namespace)
    return namespace['CheatActions'](types.SimpleNamespace(wontLose=False))


class CheatCompletionTests(unittest.TestCase):
    def run_action(self, app, action):
        cheat = load_actions(app)
        getattr(cheat, action)()
        self.assertEqual(app.record, 0, 'Save records through the native completion flow')

    def test_win_records_full_trophy_score_from_battle_and_chooser(self):
        for mode, score, waves in (('normal', 5, 10), ('hard', 10, 20), ('hell', 12, 30)):
            for choosing in (False, True):
                with self.subTest(mode=mode, choosing=choosing):
                    app = FakeApp(mode=mode, choosing=choosing)
                    self.run_action(app, 'WinLevel')
                    self.assertEqual(app.mBoard.mNumWaves, waves)
                    self.assertEqual(app.mBoard.mCurrentWave, waves)
                    app.finish_native_transition()
                    self.assertEqual(app.record, score)
                    self.assertTrue(app.first_completion)

    def test_next_stage_ends_old_chooser_before_restarting_intro(self):
        app = FakeApp(stage=1, choosing=True)
        self.run_action(app, 'NextStage')
        self.assertFalse(app.mBoard.mCutScene.mSeedChoosing)
        self.assertEqual(app.mBoard.mChallenge.mSurvivalStage, 1)
        app.finish_native_transition()
        self.assertEqual(app.mBoard.mChallenge.mSurvivalStage, 2)
        self.assertIsNotNone(app.mSeedChooserScreen)
        app.mBoard.mCutScene.Update()
        self.assertGreater(app.mBoard.mCutScene.time, 0)

    def test_next_stage_at_final_stage_also_records_trophy(self):
        for mode, score in (('normal', 5), ('hard', 10), ('hell', 12)):
            with self.subTest(mode=mode):
                app = FakeApp(mode=mode, stage=4, choosing=True)
                self.run_action(app, 'NextStage')
                app.finish_native_transition()
                self.assertEqual(app.record, score)

    def test_endless_actions_advance_exactly_one_stage(self):
        for action in ('WinLevel', 'NextStage'):
            for choosing in (False, True):
                with self.subTest(action=action, choosing=choosing):
                    app = FakeApp(mode='endless', stage=37, choosing=choosing)
                    self.run_action(app, action)
                    app.finish_native_transition()
                    self.assertEqual(app.mBoard.mChallenge.mSurvivalStage, 38)
                    self.assertFalse(app.mBoard.mCutScene.mSeedChoosing)

    def test_custom_finite_and_endless_stage_rules(self):
        for endless in (False, True):
            with self.subTest(endless=endless):
                app = FakeApp(mode='custom', choosing=True,
                              component=types.SimpleNamespace(mEndless=endless, mStages=8))
                self.run_action(app, 'WinLevel')
                self.assertEqual(app.mBoard.mChallenge.mSurvivalStage, 0 if endless else 7)
                self.assertEqual(app.mBoard.IsFinalSurvivalStage(), not endless)
                self.assertFalse(app.mBoard.mCutScene.mSeedChoosing)

    def test_no_board_actions_are_noops(self):
        for action in ('WinLevel', 'NextStage'):
            app = FakeApp()
            app.mBoard = None
            self.run_action(app, action)
            self.assertEqual(app.dialogs, [])

    def test_lose_level_restores_option_when_native_call_fails(self):
        names = ('Normal', 'Gargantuar', 'RedeyeGargantuar', 'Polevaulter', 'Catapult',
                 'Football', 'Zamboni', 'BackupDancer', 'Dancer', 'Snorkel')
        zombie_types = types.SimpleNamespace(**{name: name for name in names})
        options = types.SimpleNamespace(wontLose=True)
        zombie = types.SimpleNamespace(mPosX=0)

        def fail(zombie):
            self.assertFalse(options.wontLose)
            raise RuntimeError('native failure')

        board = types.SimpleNamespace(AddZombie=lambda *args: zombie, ZombiesWon=fail)
        app = types.SimpleNamespace(mBoard=board, KillDialog=lambda *args: None,
                                    KillSeedChooserScreen=lambda: None)
        namespace = {
            'Lawn': types.SimpleNamespace(ZombieType=zombie_types),
            'Sexy': types.SimpleNamespace(Constants=types.SimpleNamespace(BOARD_EDGE=0)),
            'GetLawnApp': lambda: app,
        }
        tree = ast.parse((ROOT / 'pgvztool/cheat_actions.py').read_text(encoding='utf-8'))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'CheatActions')
        method = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == 'LoseLevel')
        exec(compile(ast.Module(body=[method], type_ignores=[]), 'lose-level', 'exec'), namespace)
        with self.assertRaisesRegex(RuntimeError, 'native failure'):
            namespace['LoseLevel'](types.SimpleNamespace(options=options))
        self.assertTrue(options.wontLose)


if __name__ == '__main__':
    unittest.main()
