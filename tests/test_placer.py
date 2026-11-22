"""Easy placement layout, input, native vase creation, and grid focus."""
import ast
import enum
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = types.SimpleNamespace


class Rect:
    def __init__(self, x, y, width, height):
        self.mX, self.mY, self.mWidth, self.mHeight = x, y, width, height

    def Contains(self, x, y):
        return self.mX <= x < self.mX + self.mWidth and self.mY <= y < self.mY + self.mHeight


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
            'GameObjectType': ['Shovel', 'Glove', 'WateringCan'],
            'GameScenes': ['Playing', 'LevelIntro'],
            'GameMode': ['Adventure', 'ChallengeZenGarden', 'TreeOfWisdom', 'Upsell', 'Intro'],
        }.items():
            setattr(self.lawn, name, enum.Enum(name, members))
        items = []
        self.visible_tools = set()
        self.board = types.SimpleNamespace(
            StageHas6Rows=lambda: False,
            mGridItems=types.SimpleNamespace(Add=items.append),
            mApp=NS(mGameScene=self.lawn.GameScenes.Playing, mGameMode=self.lawn.GameMode.Adventure,
                    mPlayerInfo=NS(mClassicSeedChooser=False)),
            mCutScene=NS(IsInShovelTutorial=lambda: False),
            mX=100,
            mMenuButton=NS(mX=700, mY=3, mWidth=100, mHeight=45, mBtnNoDraw=False),
            mPauseButton=NS(mX=700, mY=48, mWidth=45, mHeight=45, mBtnNoDraw=False),
            mAccelerateButton=NS(mX=755, mY=48, mWidth=45, mHeight=45, mBtnNoDraw=False),
            CanInteractWithBoardButtons=lambda: True,
            IsCombatToolVisible=self.visible_tools.__contains__,
            canFocus=True, focusActive=False,
            # IronPython does not expose the game's internal mMagnifier field.
            mCursorObject=NS(_magnifier=False, mCursorType=self.lawn.CursorType.Normal),
        )
        self.items = items
        self.lawn.Board = types.SimpleNamespace(MakeRenderOrder=lambda *args: args)
        self.lawn.GridItem = types.SimpleNamespace(
            GetNewGridItem=lambda: types.SimpleNamespace(mSunCount=0),
        )
        namespace = {
            'Lawn': self.lawn, 'Enum': enum.Enum, 'Serializable': object,
            'Sexy': NS(
                TRect=Rect, Graphics=object,
                Constants=NS(UIShovelButtonPosition=NS(Y=3), ZenGardenButton_Glove_Offset=NS(X=-4),
                             Board_Offset_AspectRatio_Correction=100, UISunBankPositionX=119,
                             UIProgressMeterPosition=NS(X=450), BackBufferSize=NS(Y=1000)),
                AtlasResources=NS(IMAGE_SHOVELBANK_ZEN=NS(mWidth=70, mHeight=72),
                                  IMAGE_SHOVEL_PLANTGIRL=NS(mWidth=76), IMAGE_GLOVE_PLANTGIRL=NS(mWidth=96),
                                  IMAGE_DAN_SUNBANK=NS(mWidth=143)),
            ),
            'tas_manager': NS(can_use=lambda *args: False), 'cheat_option': NS(tasEnabled=False),
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

        self.load_functions('overlay.py', '_is_battle_ui_scene', 'GetCombatToolRects',
                            'GetEasyPlaceRect', 'IsNativeBattleButtonAt', 'DrawEasyPlaceUI')

    def load_functions(self, file, *names):
        tree = ast.parse((ROOT / 'pgvztool' / file).read_text(encoding='utf-8'))
        statements = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in names:
                node.decorator_list = []
                statements.append(node)
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                if node.targets[0].id in ('COMBAT_TOOL_GAP', 'EASY_PLACE_UI_SCALE'):
                    statements.append(node)
        exec(compile(ast.Module(body=statements, type_ignores=[]), file, 'exec'), self.namespace)

    def select_focus(self, board):
        # The placer must leave placement mode before calling native selection.
        self.assertFalse(self.placer.active)
        board.mCursorObject._magnifier = True

    def mouse_hook(self):
        self.load_functions('hook.py', 'Board__MouseDownInternal')
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
        self.board.focusActive = True
        # The native view hides the button, so no Graphics calls should be made.
        self.namespace['DrawEasyPlaceUI'](self.board, None)

    def test_layout_keeps_visible_tools_in_the_middle_except_for_the_third_tool(self):
        tool_type = self.lawn.GameObjectType
        layout = self.namespace['GetCombatToolRects']
        for shovel in (False, True):
            for glove in (False, True):
                for easy_place in (False, True):
                    with self.subTest(shovel=shovel, glove=glove, easy_place=easy_place):
                        self.visible_tools.clear()
                        if shovel:
                            self.visible_tools.add(tool_type.Shovel)
                        if glove:
                            self.visible_tools.add(tool_type.Glove)
                        self.placer.easyPlaceEnabled = easy_place
                        rects = layout(self.board)
                        self.assertEqual(set(rects), {name for shown, name in (
                            (shovel, 'shovel'), (glove, 'glove'), (easy_place, 'easy_place'),
                        ) if shown})
                        footprints = []
                        for name, left, right in (('shovel', -7, 70), ('glove', -4, 92), ('easy_place', 0, 70)):
                            if name not in rects:
                                continue
                            x = rects[name].mX
                            if name == 'easy_place' and shovel and glove:
                                self.assertGreater(x, 800)
                                self.assertLess(x + right, 900)
                            else:
                                footprints.append((x + left, x + right))
                        self.assertTrue(all(162 < left < right < 350 for left, right in footprints))
                        for first, second in zip(footprints, footprints[1:]):
                            self.assertLess(first[1], second[0])

    def test_native_rect_hooks_share_layout_and_keep_tutorial_position(self):
        self.load_functions('hook.py', 'Board__GetShovelButtonRect', 'Board__GetZenButtonRect')
        tool_type = self.lawn.GameObjectType
        self.visible_tools.update((tool_type.Shovel, tool_type.Glove))
        rects = self.namespace['GetCombatToolRects'](self.board)
        shovel, glove = self.namespace['Board__GetShovelButtonRect'], self.namespace['Board__GetZenButtonRect']
        original = lambda *args: 'native'
        self.assertEqual(shovel(original, self.board).mX, rects['shovel'].mX)
        self.assertEqual(glove(original, self.board, tool_type.Glove).mX, rects['glove'].mX)
        self.assertEqual(glove(original, self.board, tool_type.WateringCan), 'native')
        self.board.mCutScene.IsInShovelTutorial = lambda: True
        self.assertEqual(shovel(original, self.board), 'native')

    def test_easy_place_click_follows_layout_changes_without_waiting_for_draw(self):
        hook = self.mouse_hook()
        tool_type = self.lawn.GameObjectType
        self.visible_tools.update((tool_type.Shovel, tool_type.Glove))
        layout = self.namespace['GetCombatToolRects']
        calls = []
        original = lambda *args: calls.append(args)
        overflow = layout(self.board)['easy_place']
        hook(original, self.board, overflow.mX + 10, 20, 1, True)
        self.assertFalse(self.placer.active)

        self.visible_tools.remove(tool_type.Glove)
        hook(original, self.board, overflow.mX + 10, 20, 1, True)
        self.assertFalse(self.placer.active)
        self.assertEqual(calls, [(self.board, overflow.mX + 10, 20, 1, True)])
        middle = layout(self.board)['easy_place']
        hook(original, self.board, middle.mX + 10, 20, 1, False)
        self.assertTrue(self.placer.active)

    def test_easy_place_draw_uses_the_same_rect_as_input(self):
        tool_type = self.lawn.GameObjectType
        self.visible_tools.update((tool_type.Shovel, tool_type.Glove))
        sexy = self.namespace['Sexy']
        sexy.AtlasResources.IMAGE_TACO = object()
        sexy.TodLib = NS(TodCommon=NS(TodDrawImageCenterScaledF=lambda *args: None))
        self.placer.active = False
        draws = []
        graphics = NS(DrawImage=lambda *args: draws.append(args), SetColorizeImages=lambda _: None)
        for expected_x in (815, 262):
            self.namespace['DrawEasyPlaceUI'](self.board, graphics)
            self.assertEqual(draws.pop(), (sexy.AtlasResources.IMAGE_SHOVELBANK_ZEN, expected_x, 3))
            self.visible_tools.discard(tool_type.Glove)

    def test_native_buttons_keep_their_clicks_while_easy_place_is_active(self):
        hook = self.mouse_hook()
        tool_type = self.lawn.GameObjectType
        self.visible_tools.update((tool_type.Shovel, tool_type.Glove))
        layout = self.namespace['GetCombatToolRects'](self.board)
        for button in (layout['shovel'], layout['glove'], self.board.mMenuButton,
                       self.board.mPauseButton, self.board.mAccelerateButton):
            calls = []
            hook(lambda *args: calls.append(args), self.board, button.mX, button.mY, 1, False)
            self.assertEqual(calls, [(self.board, button.mX, button.mY, 1, False)])

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
