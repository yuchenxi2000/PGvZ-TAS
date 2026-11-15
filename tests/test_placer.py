"""Easy placement shares native vase creation and grid-focus interaction."""
import ast
import enum
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PlacerTests(unittest.TestCase):
    def setUp(self):
        self.lawn = types.SimpleNamespace()
        for name, members in {
            'SeedType': ['Peashooter', 'Sunflower'],
            'ZombieType': ['Normal', 'Football'],
            'GridItemType': ['Ladder', 'ScaryPot', 'Rake', 'Crater', 'Gravestone'],
            'GridItemState': ['ScaryPotQuestion', 'ScaryPotLeaf', 'ScaryPotZombie'],
            'ScaryPotType': ['None', 'Seed', 'Zombie', 'Sun'],
            'CoinType': ['Silver'],
            'RenderLayer': ['Plant'],
            'CursorType': ['Normal', 'Hammer'],
        }.items():
            setattr(self.lawn, name, enum.Enum(name, members))
        items = []
        self.board = types.SimpleNamespace(
            StageHas6Rows=lambda: False,
            mGridItems=types.SimpleNamespace(Add=items.append),
            canFocus=True, focusActive=False,
            # IronPython does not expose the game's internal mMagnifier field.
            mCursorObject=types.SimpleNamespace(_magnifier=False),
        )
        self.items = items
        self.lawn.Board = types.SimpleNamespace(MakeRenderOrder=lambda *args: args)
        self.lawn.GridItem = types.SimpleNamespace(
            GetNewGridItem=lambda: types.SimpleNamespace(mSunCount=0),
        )
        namespace = {
            'Lawn': self.lawn, 'Enum': enum.Enum, 'Serializable': object,
            'Sexy': types.SimpleNamespace(TRect=lambda *args: None),
            'GetBoard': lambda: self.board,
            'GetLawnApp': lambda: types.SimpleNamespace(mBoard=self.board),
            'PixelToGrid': lambda board, pos: pos,
            'none_of': lambda enum_type: getattr(enum_type, 'None'),
            '_grid_focus_can_select': types.SimpleNamespace(GetValue=lambda board, _: board.canFocus),
            '_grid_focus_active': types.SimpleNamespace(GetValue=lambda board, _: board.focusActive),
            '_grid_focus_magnifier': types.SimpleNamespace(GetValue=lambda cursor: cursor._magnifier),
            '_grid_focus_select': types.SimpleNamespace(Invoke=lambda board, _: self.select_focus(board)),
        }
        tree = ast.parse((ROOT / 'pgvztool/placer.py').read_text(encoding='utf-8'))
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        exec(compile(ast.Module(body=classes, type_ignores=[]), 'placer', 'exec'), namespace)
        self.placer = namespace['Placer']()
        namespace['placer'] = self.placer
        self.namespace = namespace
        self.placer.easyPlaceMode = 'griditem'
        self.placer.gridItemType = self.lawn.GridItemType.ScaryPot

    def select_focus(self, board):
        # The placer must leave placement mode before calling native selection.
        self.assertFalse(self.placer.active)
        board.mCursorObject._magnifier = True

    def mouse_hook(self):
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                        and node.name == 'Board__MouseDownInternal')
        function.decorator_list = []
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'mouse-hook', 'exec'), self.namespace)
        self.placer._ep_rect = types.SimpleNamespace(Contains=lambda x, y: False)
        # Native grid-focus input must never pass through the placement conversion.
        def reject_conversion(*args):
            self.fail('grid focus received pre-converted coordinates')
        self.board.mCamera = types.SimpleNamespace(ScreenToBoardReplace=reject_conversion)
        return self.namespace['Board__MouseDownInternal']

    def test_zoom_enters_native_selection_with_untouched_screen_coordinates(self):
        hook = self.mouse_hook()
        self.placer.easyPlaceMode = 'zoom'
        calls = []
        def original(board, x, y, count, is_touch):
            calls.append((x, y, count, is_touch, board.mCursorObject._magnifier))
            board.focusActive = True
            board.mCursorObject._magnifier = False
        hook(original, self.board, 803, 401, 1, True)
        self.assertEqual(calls, [(803, 401, 1, True, True)])
        self.assertTrue(self.board.focusActive)
        self.assertFalse(self.placer.active)
        self.assertEqual(self.items, [])

    def test_zoom_unavailable_does_not_arm_magnifier_or_pass_through_click(self):
        hook = self.mouse_hook()
        self.placer.easyPlaceMode = 'zoom'
        self.board.canFocus = False
        calls = []
        hook(lambda *args: calls.append(args), self.board, 803, 401, 1, False)
        self.assertEqual(calls, [])
        self.assertFalse(self.board.mCursorObject._magnifier)
        self.assertTrue(self.placer.active)

    def test_native_focus_and_pending_selection_keep_left_right_and_touch_clicks(self):
        hook = self.mouse_hook()
        # Even changing placement mode or toggling it on cannot steal the exit click.
        for active, pending in ((True, False), (False, True)):
            for count, is_touch in ((1, False), (-1, False), (1, True), (0, True)):
                with self.subTest(active=active, pending=pending, count=count, touch=is_touch):
                    self.board.focusActive = active
                    self.board.mCursorObject._magnifier = pending
                    calls = []
                    hook(lambda *args: calls.append(args), self.board, 803, 401, count, is_touch)
                    self.assertEqual(calls, [(self.board, 803, 401, count, is_touch)])
                    self.assertTrue(self.placer.active)
                    self.assertEqual(self.items, [])

    def test_zoom_hides_easy_place_ui_until_native_return_animation_finishes(self):
        tree = ast.parse((ROOT / 'pgvztool/overlay.py').read_text(encoding='utf-8'))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                        and node.name == 'DrawEasyPlaceUI')
        self.namespace['Sexy'].Graphics = object
        exec(compile(ast.Module(body=[function], type_ignores=[]), 'easy-place-ui', 'exec'), self.namespace)
        self.board.focusActive = True
        # No Graphics calls or normal UI positioning are needed while focus is active.
        self.namespace['DrawEasyPlaceUI'](self.board, None)

    def test_easy_place_creates_vases_with_selected_content_and_appearance(self):
        self.placer.seedType = self.lawn.SeedType.Sunflower
        self.placer.zombieType = self.lawn.ZombieType.Football
        for content, native_type, sun_count in (
            ('None', 'None', 0), ('Seed', 'Seed', 0), ('Zombie', 'Zombie', 0),
            ('Sun1', 'Sun', 1), ('Sun2', 'Sun', 2), ('Sun3', 'Sun', 3),
        ):
            for appearance in self.lawn.GridItemState:
                with self.subTest(content=content, appearance=appearance):
                    self.placer.scaryPotType = content
                    self.placer.scaryPotAppearance = appearance
                    count = len(self.items)
                    self.assertTrue(self.placer.try_place(self.board, 3, 2))
                    self.assertEqual(len(self.items), count + 1)
                    vase = self.items[-1]
                    self.assertEqual(vase.mGridItemType, self.lawn.GridItemType.ScaryPot)
                    self.assertEqual((vase.mGridX, vase.mGridY), (3, 2))
                    self.assertEqual(vase.mGridItemState, appearance)
                    self.assertEqual(vase.mScaryPotType, getattr(self.lawn.ScaryPotType, native_type))
                    self.assertEqual(vase.mSeedType, self.lawn.SeedType.Sunflower)
                    self.assertEqual(vase.mZombieType, self.lawn.ZombieType.Football)
                    self.assertEqual(vase.mSunCount, sun_count)

    def test_default_vase_matches_gui_defaults(self):
        self.assertTrue(self.placer.try_place(self.board, 0, 0))
        self.assertEqual(self.items[0].mScaryPotType, self.lawn.ScaryPotType.Seed)
        self.assertEqual(self.items[0].mGridItemState, self.lawn.GridItemState.ScaryPotQuestion)

    def test_other_grid_items_still_use_their_native_placement(self):
        ladders = []
        self.board.AddALadder = lambda col, row: ladders.append((col, row))
        self.placer.gridItemType = self.lawn.GridItemType.Ladder
        self.assertTrue(self.placer.try_place(self.board, 4, 1))
        self.assertEqual(ladders, [(4, 1)])
        self.assertEqual(self.items, [])

    def test_click_outside_board_does_not_create_vase(self):
        for col, row in [(-1, 0), (9, 0), (0, -1), (0, 5)]:
            self.assertFalse(self.placer.try_place(self.board, col, row))
        self.assertEqual(self.items, [])


if __name__ == '__main__':
    unittest.main()
