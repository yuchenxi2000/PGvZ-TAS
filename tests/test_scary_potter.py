"""Vases in ordinary levels must not consume other input or finish the level."""
import ast
import pathlib
import types
import unittest
from unittest.mock import Mock


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ScaryPotterTests(unittest.TestCase):
    def setUp(self):
        self.scary_level = False
        self.options = types.SimpleNamespace(scaryPotterNoDelay=False)
        self.app = types.SimpleNamespace(
            IsScaryPotterLevel=lambda: self.scary_level,
            mGameScene='Playing', mGameMode='Adventure', mCrazyDaveMessageIndex=-1,
        )
        self.pot = object()
        self.board = types.SimpleNamespace(
            CanInteractWithBoardButtons=Mock(return_value=True),
            IsScaryPotterDaveTalking=Mock(return_value=False),
            mCursorObject=types.SimpleNamespace(mCursorType='Normal'),
            PixelToGridX=Mock(return_value=3), PixelToGridY=Mock(return_value=2),
            GetScaryPotAt=Mock(return_value=self.pot),
        )
        self.challenge = types.SimpleNamespace(
            mApp=self.app, mBoard=self.board, ScaryPotterOpenPot=Mock(),
            mChallengeState='OtherMinigameState', mReanimChallenge=object(),
            mChallengeGridX=7, mChallengeGridY=4,
        )
        self.hit = types.SimpleNamespace(mObjectType='None', mObject=None)
        self.orig = Mock(return_value=False)
        self.constants = types.SimpleNamespace(IS=0.5)
        lawn = types.SimpleNamespace(
            Challenge=object, HitResult=object,
            GameScenes=types.SimpleNamespace(Playing='Playing'),
            GameMode=types.SimpleNamespace(ChallengeZenGarden='ZenGarden', TreeOfWisdom='Tree'),
            GameObjectType=types.SimpleNamespace(ScaryPot='ScaryPot', **{'None': 'None'}),
            CursorType=types.SimpleNamespace(Normal='Normal', Shovel='Shovel'),
        )
        namespace = {
            'Lawn': lawn, 'Sexy': types.SimpleNamespace(Constants=self.constants),
            'cheat_option': self.options, 'none_of': lambda enum: getattr(enum, 'None'),
        }
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        hooks = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name in ('Challenge__MouseDown', 'Challenge__ScaryPotterIsCompleted')]
        for hook in hooks:
            hook.decorator_list = []
        exec(compile(ast.Module(body=hooks, type_ignores=[]), 'vase-hooks', 'exec'), namespace)
        self.mouse_down = namespace['Challenge__MouseDown']
        self.is_completed = namespace['Challenge__ScaryPotterIsCompleted']

    def click(self, count=1):
        return self.mouse_down(self.orig, self.challenge, 640, 480, count, self.hit)

    def test_normal_and_shovel_click_open_without_overwriting_challenge_state(self):
        before = vars(self.challenge).copy()
        for cursor in ('Normal', 'Shovel'):
            with self.subTest(cursor=cursor):
                self.board.mCursorObject.mCursorType = cursor
                self.assertTrue(self.click())
                self.challenge.ScaryPotterOpenPot.assert_called_with(self.pot)
                self.assertEqual(vars(self.challenge), before)
        self.board.PixelToGridX.assert_called_with(320, 240)
        self.board.PixelToGridY.assert_called_with(320, 240)
        self.board.GetScaryPotAt.assert_called_with(3, 2)

    def test_touch_click_opens_and_empty_cell_falls_through(self):
        self.assertTrue(self.click(count=0))
        self.challenge.ScaryPotterOpenPot.reset_mock()
        self.board.GetScaryPotAt.return_value = None
        self.assertFalse(self.click())
        self.challenge.ScaryPotterOpenPot.assert_not_called()

    def test_existing_hit_targets_keep_priority(self):
        for target in ('Coin', 'Plant', 'SeedPacket', 'Shovel', 'MenuButton'):
            with self.subTest(target=target):
                self.hit.mObjectType = target
                self.assertFalse(self.click())
        self.challenge.ScaryPotterOpenPot.assert_not_called()

    def test_native_consumed_click_keeps_priority(self):
        self.orig.return_value = True
        self.assertTrue(self.click())
        self.board.GetScaryPotAt.assert_not_called()

    def test_right_click_held_seed_and_blocked_board_do_not_open(self):
        self.assertFalse(self.click(count=-1))
        for cursor in ('PlantFromBank', 'PlantFromUsableCoin', 'CobcannonTarget', 'Glove'):
            self.board.mCursorObject.mCursorType = cursor
            self.assertFalse(self.click())
        self.board.mCursorObject.mCursorType = 'Normal'
        # Covers pause, dialogs and level fade-out through the native predicate.
        self.board.CanInteractWithBoardButtons.return_value = False
        self.assertFalse(self.click())
        self.challenge.ScaryPotterOpenPot.assert_not_called()

    def test_intro_and_garden_do_not_open(self):
        self.app.mGameScene = 'LevelIntro'
        self.assertFalse(self.click())
        self.app.mGameScene = 'Playing'
        for mode in ('ZenGarden', 'Tree'):
            self.app.mGameMode = mode
            self.assertFalse(self.click())
        self.challenge.ScaryPotterOpenPot.assert_not_called()

    def test_scary_level_keeps_native_hammer_and_optional_instant_open(self):
        self.scary_level = True
        self.hit.mObjectType = 'ScaryPot'
        self.hit.mObject = self.pot
        self.orig.return_value = True
        self.assertTrue(self.click())
        self.orig.assert_called_once()
        self.challenge.ScaryPotterOpenPot.assert_not_called()
        self.options.scaryPotterNoDelay = True
        self.assertTrue(self.click())
        self.orig.assert_called_once()
        self.challenge.ScaryPotterOpenPot.assert_called_once_with(self.pot)

    def test_last_pot_cannot_complete_ordinary_level_but_scary_rules_are_preserved(self):
        native_completed = Mock(return_value=True)
        self.assertFalse(self.is_completed(native_completed, self.challenge))
        native_completed.assert_not_called()
        # Applies to native OpenPot whether invoked by a click or the bulk GUI action.
        self.scary_level = True
        for completed in (False, True):
            native_completed.return_value = completed
            self.assertEqual(self.is_completed(native_completed, self.challenge), completed)
        self.assertEqual(native_completed.call_count, 2)


if __name__ == '__main__':
    unittest.main()
