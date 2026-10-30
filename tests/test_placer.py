"""Easy placement uses the same vase options and creation path as GUI actions."""
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
        }.items():
            setattr(self.lawn, name, enum.Enum(name, members))
        items = []
        self.board = types.SimpleNamespace(
            StageHas6Rows=lambda: False,
            mGridItems=types.SimpleNamespace(Add=items.append),
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
        }
        tree = ast.parse((ROOT / 'pgvztool/placer.py').read_text(encoding='utf-8'))
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        exec(compile(ast.Module(body=classes, type_ignores=[]), 'placer', 'exec'), namespace)
        self.placer = namespace['Placer']()
        self.placer.easyPlaceMode = 'griditem'
        self.placer.gridItemType = self.lawn.GridItemType.ScaryPot

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
