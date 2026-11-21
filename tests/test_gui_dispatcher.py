"""GUI dispatcher thread-boundary and domain integration regression tests."""
import ast
import enum
import importlib.util
import json
import pathlib
import sys
import threading
import types
import unittest
from unittest.mock import patch


ROOT = pathlib.Path(__file__).resolve().parents[1]


class GuiDispatcherTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.request_counter = 0
        self.main_thread = False
        self.owner_thread = threading.get_ident()
        self.board = types.SimpleNamespace(mSunMoney=0, mChallenge=types.SimpleNamespace(mSurvivalStage=0))
        self.app = types.SimpleNamespace(mPlayerInfo=types.SimpleNamespace(mCoins=0), mBoard=self.board)
        self.lawn = types.ModuleType('Lawn')
        for name, members in {
            'SeedType': {'Peashooter': 0, 'Sunflower': 1},
            'ZombieType': {'Normal': 0, 'Football': 1},
            'GridItemType': {'Ladder': 0, 'ScaryPot': 1},
            'GridItemState': {'ScaryPotLeaf': 0},
            'CoinType': {'Silver': 0},
            'GameMode': {'Adventure': 0},
            'ScaryPotType': {'None': 0, 'Sun': 1, 'Seed': 2, 'Zombie': 3},
            'BackgroundType': {'Num1Day': 0, 'Num6Boss': 5},
            'GridSquareType': {'None': 0, 'Grass': 1, 'Dirt': 2, 'Pool': 3, 'HighGround': 4, 'Shallow': 5},
            'PlantRowType': {'Dirt': 0, 'Normal': 1, 'Pool': 2, 'HighGround': 3, 'Shallow': 4},
        }.items():
            setattr(self.lawn, name, enum.Enum(name, members))
        self.lawn.LawnApp = self.lawn.Board = self.lawn.PlayerInfo = self.lawn.GardenType = self.lawn.GameSelector = object
        self.lawn.PottedPlant = types.SimpleNamespace(FacingDirection=object)
        test = self

        class FakePlacer:
            def __getattr__(self, name):
                def method(instance, *args):
                    test.assertTrue(test.main_thread)
                    test.assertEqual(threading.get_ident(), test.owner_thread)
                    test.calls.append((name, args))
                method.__name__ = name
                return types.MethodType(method, self)

        def get_board():
            self.assertTrue(self.main_thread)
            self.assertEqual(threading.get_ident(), self.owner_thread)
            return self.board

        def get_app():
            self.assertTrue(self.main_thread)
            self.assertEqual(threading.get_ident(), self.owner_thread)
            return self.app

        def set_speed(value):
            self.assertTrue(self.main_thread)
            self.assertEqual(threading.get_ident(), self.owner_thread)
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError('speed must be a number')
            self.calls.append(('SetGlobalSpeed', (value,)))
            return True, value

        self.placer = FakePlacer()
        self.sexy = types.ModuleType('Sexy')
        self.sexy.TodLib = types.SimpleNamespace(FoleyType=types.SimpleNamespace(Drop='Drop'))
        self.sexy.KeyCode = object
        self.sexy.Debug = types.SimpleNamespace(Log=lambda *args: None)
        self.sexy.DebugType = types.SimpleNamespace(Error='error')
        namespace = {
            'Lawn': self.lawn, 'Sexy': self.sexy, 'GetBoard': get_board, 'GetLawnApp': get_app,
            'LineUp': types.SimpleNamespace(from_board=lambda board: types.SimpleNamespace(to_str=lambda: 'lineup-code')),
            'SetZombies': lambda *args: self.calls.append(('CheatSetZombies', args)),
            'none_of': lambda enum_type: getattr(enum_type, 'None'),
        }
        tree = ast.parse((ROOT / 'pgvztool/cheat_actions.py').read_text(encoding='utf-8'))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'CheatActions')
        exec(compile(ast.Module(body=[cls], type_ignores=[]), 'cheat-actions', 'exec'), namespace)
        self.options = types.SimpleNamespace(wontLose=False)
        self.operations = namespace['CheatActions'](self.options)
        tree = ast.parse((ROOT / 'pgvztool/placer.py').read_text(encoding='utf-8'))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'Placer')
        vase = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == 'PlaceGridItem')
        exec(compile(ast.Module(body=[vase], type_ignores=[]), 'vase-placement', 'exec'), namespace)
        self.placer.PlaceGridItem = types.MethodType(namespace['PlaceGridItem'], self.placer)

        pgvz = types.ModuleType('pgvz')
        pgvz.SetGlobalSpeed = set_speed
        pgvz.__game_version__ = '1.3.4'
        version = types.ModuleType('pgvz.version')
        version.MOD_VERSION = 'test'
        package_name = 'test_dispatcher_pgvztool'
        package = types.ModuleType(package_name)
        package.__path__ = [str(ROOT / 'pgvztool')]
        modules = {'Lawn': self.lawn, 'pgvz': pgvz, 'pgvz.version': version,
                   'Sexy': self.sexy, 'System': types.ModuleType('System'), package_name: package}
        for suffix, key, value in (
            ('cheat_actions', 'cheat_actions', self.operations), ('placer', 'placer', self.placer),
        ):
            module = types.ModuleType(package_name + '.' + suffix)
            setattr(module, key, value)
            modules[module.__name__] = module
        with patch.dict(sys.modules, modules):
            spec = importlib.util.spec_from_file_location(package_name + '.sync', ROOT / 'pgvztool/sync.py')
            sync = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = sync
            spec.loader.exec_module(sync)
            self.sync_module = sync
            self.registry = sync.sync_reg
            self.option_namespace = dict(namespace, Serializable=sync.Serializable)

            class State(sync.Serializable):
                def __init__(self):
                    self._value = False

                @property
                def noCooldown(self):
                    test.assertTrue(test.main_thread, 'state getter ran on the network thread')
                    test.assertEqual(threading.get_ident(), test.owner_thread)
                    return self._value

                @noCooldown.setter
                def noCooldown(self, value):
                    test.assertTrue(test.main_thread, 'state setter ran on the network thread')
                    test.assertEqual(threading.get_ident(), test.owner_thread)
                    self._value = value

            self.state = State()
            self.registry.register('cheat', self.state)
            spec = importlib.util.spec_from_file_location(package_name + '.dispatcher', ROOT / 'pgvztool/dispatcher.py')
            self.dispatcher_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.dispatcher_module)
            self.dispatcher = self.dispatcher_module.gui_dispatcher
        self.main_thread = True
        self.registry.connect('client-1')
        self.main_thread = False

    def submit(self, kind, client_id='client-1', request_id=None, **details):
        self.request_counter += 1
        request_id = request_id or 'request-{}'.format(self.request_counter)
        return json.loads(self.dispatcher.submit(json.dumps(dict(
            details, _clientId=client_id, id=request_id, kind=kind,
        ))))

    def dispatch(self, name, args=None, client_id='client-1', request_id=None):
        return self.submit('action', client_id, request_id, name=name, args={} if args is None else args)

    def run_tasks(self):
        self.main_thread = True
        try:
            self.dispatcher.run_pending()
        finally:
            self.main_thread = False

    def results(self, client_id='client-1'):
        results = json.loads(self.dispatcher.poll(client_id))['results']
        self.dispatcher.acknowledge(client_id, json.dumps([result['id'] for result in results]))
        return results

    def test_game_state_is_only_accessed_when_main_thread_task_runs(self):
        queued = self.dispatch('setSun', {'value': 9990})
        self.assertEqual(queued, {'action': 'queued', 'id': 'request-1'})
        self.assertEqual(self.board.mSunMoney, 0)
        self.assertEqual(self.results(), [])
        self.run_tasks()
        self.assertEqual(self.board.mSunMoney, 9990)
        self.assertTrue(self.results()[0]['ok'])

    def terrain_board(self):
        # .NET enums stringify to their member names.
        for enum_type in (self.lawn.BackgroundType, self.lawn.GridSquareType, self.lawn.PlantRowType):
            enum_type.__str__ = lambda member: member.name
        self.board.mGameID = 42
        self.board.mBackground = self.lawn.BackgroundType.Num1Day
        self.board.mGridSquareType = {(col, row): self.lawn.GridSquareType.Grass
                                      for row in range(6) for col in range(9)}
        self.board.mPlantRow = [self.lawn.PlantRowType.Normal] * 6
        self.board.mPlants = types.SimpleNamespace(Count=0)
        self.board.mApp = types.SimpleNamespace(IsWallnutBowlingLevel=lambda: False)
        def load_background():
            self.assertTrue(self.main_thread)
            self.calls.append(('LoadBackgroundImages', self.board.mBackground))
        self.board.LoadBackgroundImages = load_background
        self.dispatch('getTerrain')
        self.run_tasks()
        return self.results()[0]['value']

    def test_terrain_is_read_then_applied_once_on_main_thread_with_correct_axes(self):
        draft = self.terrain_board()
        self.assertEqual(draft['grid'], [['Grass'] * 9 for _ in range(6)])
        draft['background'] = 'Num6Boss'
        draft['grid'][1][7] = 'None'
        draft['grid'][5][0] = 'Shallow'
        draft['rows'][4] = 'Pool'
        self.assertEqual(self.board.mBackground, self.lawn.BackgroundType.Num1Day)
        self.dispatch('applyTerrain', draft)
        self.assertEqual(self.board.mGridSquareType[7, 1], self.lawn.GridSquareType.Grass)

        self.run_tasks()
        result = self.results()[0]
        self.assertTrue(result['ok'], result)
        self.assertEqual(self.board.mGridSquareType[7, 1], getattr(self.lawn.GridSquareType, 'None'))
        self.assertEqual(self.board.mGridSquareType[0, 5], self.lawn.GridSquareType.Shallow)
        self.assertEqual(self.board.mPlantRow[4], self.lawn.PlantRowType.Pool)
        self.assertEqual(self.calls, [('LoadBackgroundImages', self.lawn.BackgroundType.Num6Boss)])
        self.assertEqual(result['value']['grid'], draft['grid'])
        self.board.mGridSquareType[7, 1] = self.lawn.GridSquareType.Grass
        self.run_tasks()
        self.assertEqual(self.board.mGridSquareType[7, 1], self.lawn.GridSquareType.Grass)

    def test_read_terrain_without_board_returns_day_with_five_grass_rows_and_one_dirt_row(self):
        self.board = None
        self.dispatch('getTerrain')
        self.run_tasks()
        result = self.results()[0]
        self.assertTrue(result['ok'], result)
        self.assertEqual(result['value'], {
            'background': 'Num1Day',
            'grid': [['Grass'] * 9 for _ in range(5)] + [['Dirt'] * 9],
            'rows': ['Normal'] * 5 + ['Dirt'],
        })
        self.assertEqual(self.calls, [])

    def test_terrain_repositions_grounded_plants_after_writing_all_terrain(self):
        draft = self.terrain_board()
        draft['background'] = 'Num6Boss'
        draft['grid'][2][3] = 'HighGround'
        draft['rows'][2] = 'HighGround'
        plants = [types.SimpleNamespace(
            mDead=False, mPlantCol=3, mRow=2, mX=0, mY=0,
            mPlantHealth=123, mLaunchCounter=456, mState='attacking',
            mIsAsleep=asleep, NotOnGround=lambda: False,
        ) for asleep in (False, True)]
        plants.extend([
            types.SimpleNamespace(mDead=True),
            types.SimpleNamespace(mDead=False, NotOnGround=lambda: True),
            types.SimpleNamespace(mDead=False, NotOnGround=lambda: False, mPlantCol=-1, mRow=0),
        ])
        class PlantList(list):
            @property
            def Count(self):
                return len(self)
        self.board.mPlants = PlantList(plants)
        moved = []
        def move_plant(plant, col, row):
            self.assertTrue(self.main_thread)
            self.assertEqual(self.board.mBackground, self.lawn.BackgroundType.Num6Boss)
            self.assertEqual(self.board.mPlantRow[2], self.lawn.PlantRowType.HighGround)
            self.assertEqual(self.board.mGridSquareType[3, 2], self.lawn.GridSquareType.HighGround)
            self.assertEqual(self.board.mGridSquareType[8, 5], self.lawn.GridSquareType.Grass)
            self.assertEqual((col, row), (3, 2))
            # 模拟原生 MovePlant 使用新背景和地形重新计算发射坐标。
            plant.mX, plant.mY = 80 * col, 85 * row - 40
            moved.append(plant)
        self.board.mChallenge.MovePlant = move_plant
        self.dispatch('applyTerrain', draft)
        self.assertEqual(moved, [])
        self.run_tasks()
        result = self.results()[0]
        self.assertTrue(result['ok'], result)
        self.assertEqual(len(moved), 2)
        for index, plant in enumerate(plants[:2]):
            self.assertIs(moved[index], plant)
            self.assertEqual((plant.mX, plant.mY), (240, 130))
            self.assertEqual((plant.mPlantHealth, plant.mLaunchCounter, plant.mState), (123, 456, 'attacking'))
            self.assertEqual(plant.mIsAsleep, bool(index))
        self.run_tasks()
        self.assertEqual(len(moved), 2)

    def test_terrain_does_not_snap_bowling_plants_back_to_their_grid(self):
        draft = self.terrain_board()
        self.board.mApp.IsWallnutBowlingLevel = lambda: True
        class RejectPlantAccess:
            @property
            def Count(self):
                raise AssertionError('bowling plants must not be repositioned')
        self.board.mPlants = RejectPlantAccess()
        draft['grid'][0][0] = 'Pool'
        self.dispatch('applyTerrain', draft)
        self.run_tasks()
        self.assertTrue(self.results()[0]['ok'])
        self.assertEqual(self.board.mGridSquareType[0, 0], self.lawn.GridSquareType.Pool)

    def test_terrain_validates_entire_payload_before_any_game_write(self):
        draft = self.terrain_board()
        draft['background'] = 'Num6Boss'
        for field, invalid in (
            ('grid', [['Pool'] * 9] * 5),
            ('grid', [['Pool'] * 8] * 6),
            ('grid', [['INVALID'] * 9] * 6),
            ('rows', ['Pool'] * 5),
            ('rows', ['INVALID'] * 6),
            ('background', 'INVALID'),
        ):
            with self.subTest(field=field, invalid=invalid):
                self.dispatch('applyTerrain', dict(draft, **{field: invalid}))
                self.run_tasks()
                self.assertFalse(self.results()[0]['ok'])
                self.assertEqual(self.board.mBackground, self.lawn.BackgroundType.Num1Day)
                self.assertEqual(self.calls, [])
                self.assertTrue(all(value == self.lawn.GridSquareType.Grass
                                    for value in self.board.mGridSquareType.values()))

    def test_terrain_applies_draft_to_current_board_after_level_or_stage_changes(self):
        draft = self.terrain_board()
        draft['background'] = 'Num6Boss'
        original = self.board
        for change in ('board', 'stage', 'game_id'):
            with self.subTest(change=change):
                self.board = original
                self.board.mGameID = 42
                self.board.mChallenge.mSurvivalStage = 0
                self.board.mBackground = self.lawn.BackgroundType.Num1Day
                self.calls.clear()
                payload = dict(draft)
                if change == 'board':
                    # Apply targets the Board present when the queued request executes.
                    self.board = types.SimpleNamespace(**vars(original), replacement=True)
                elif change == 'stage':
                    self.board.mChallenge.mSurvivalStage = 1
                elif change == 'game_id':
                    self.board.mGameID = 43
                self.dispatch('applyTerrain', payload)
                self.run_tasks()
                self.assertTrue(self.results()[0]['ok'])
                self.assertEqual(self.board.mBackground, self.lawn.BackgroundType.Num6Boss)
                self.assertEqual(self.calls, [('LoadBackgroundImages', self.lawn.BackgroundType.Num6Boss)])

    def test_failed_background_load_does_not_change_terrain_or_background(self):
        draft = self.terrain_board()
        draft['background'] = 'Num6Boss'
        draft['rows'][0] = 'Pool'
        draft['grid'][0][0] = 'Pool'
        self.board.LoadBackgroundImages = lambda: (_ for _ in ()).throw(RuntimeError('load failed'))
        self.dispatch('applyTerrain', draft)
        self.run_tasks()
        self.assertFalse(self.results()[0]['ok'])
        self.assertEqual(self.board.mBackground, self.lawn.BackgroundType.Num1Day)
        self.assertEqual(self.board.mPlantRow[0], self.lawn.PlantRowType.Normal)
        self.assertEqual(self.board.mGridSquareType[0, 0], self.lawn.GridSquareType.Grass)

    def test_grid_only_edit_keeps_background_resources_and_wave_state(self):
        draft = self.terrain_board()
        waves = self.board.mZombiesInWave = object()
        self.board.mCurrentWave = 7
        self.board.mZombieCountDown = 123
        draft['grid'][0][8] = 'HighGround'
        self.dispatch('applyTerrain', draft)
        self.run_tasks()
        self.assertTrue(self.results()[0]['ok'])
        self.assertEqual(self.calls, [])
        self.assertIs(self.board.mZombiesInWave, waves)
        self.assertEqual((self.board.mCurrentWave, self.board.mZombieCountDown), (7, 123))
        self.assertEqual(self.results(), [])

    def test_calls_synchronous_api_once(self):
        self.dispatch('placeZombie', {'row': -1, 'col': 2, 'zombieType': 'Football', 'mindCtrl': True})
        self.run_tasks()
        self.assertEqual(self.calls, [('ZombieOnBoard', (-1, 2, self.lawn.ZombieType.Football, True))])
        self.assertTrue(self.results()[0]['ok'])

    def test_registered_api_methods_match_real_method_signatures(self):
        classes = {}
        for api, filename, class_name in (
            (self.operations, 'cheat_actions.py', 'CheatActions'), (self.placer, 'placer.py', 'Placer'),
        ):
            tree = ast.parse((ROOT / 'pgvztool' / filename).read_text(encoding='utf-8'))
            cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == class_name)
            classes[api] = {node.name: node for node in cls.body if isinstance(node, ast.FunctionDef)}
        for name, (handler, fields) in self.dispatcher._actions.items():
            owner = getattr(handler, '__self__', None)
            if owner not in classes:
                continue
            with self.subTest(action=name):
                method = classes[owner][handler.__name__]
                maximum = len(method.args.args) - 1
                minimum = maximum - len(method.args.defaults)
                self.assertLessEqual(minimum, len(fields))
                self.assertGreaterEqual(maximum, len(fields))

    def test_update_hook_handles_paused_board_before_calling_original(self):
        self.board.mManualPaused = True
        self.board.mAccelerationNumerator = 0
        self.dispatch('setSun', {'value': 456})
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        hook = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name == 'SexyAppBase__DoUpdateFrames')
        hook.decorator_list = []
        namespace = {'gui_dispatcher': self.dispatcher, 'Sexy': types.SimpleNamespace(SexyAppBase=object)}
        exec(compile(ast.Module(body=[hook], type_ignores=[]), 'gui-action-hook', 'exec'), namespace)

        def original(app):
            self.assertIs(app, self.app)
            self.assertEqual(self.board.mSunMoney, 456)
            self.assertTrue(self.board.mManualPaused)
            self.assertEqual(self.board.mAccelerationNumerator, 0)
            return False

        self.main_thread = True
        try:
            self.assertIs(namespace['SexyAppBase__DoUpdateFrames'](original, self.app), False)
        finally:
            self.main_thread = False

    def test_only_named_enum_members_are_accepted(self):
        for value in ('NotAZombie', '__class__', 'name', 0):
            with self.subTest(value=value):
                self.dispatch('placeZombie', {'row': 0, 'col': 0, 'zombieType': value, 'mindCtrl': False})
                self.run_tasks()
                self.assertFalse(self.results()[0]['ok'])
        self.assertEqual(self.calls, [])

    def test_type_and_argument_errors_return_correlated_results(self):
        invalid = [
            ('setSun', {'value': True}), ('setSun', {'value': 2**31}),
            ('setSun', {'value': '9990'}), ('setSun', {}),
            ('setSun', {'value': 1, 'field': 'anything'}), ('__dict__', {}),
            ('removeZombies', {'enemyOnly': 'false'}),
        ]
        for name, args in invalid:
            with self.subTest(name=name, args=args):
                self.dispatch(name, args)
                self.run_tasks()
                result = self.results()[0]
                self.assertTrue(result['id'].startswith('request-'))
                self.assertFalse(result['ok'])
                self.assertTrue(result['error'])
        self.assertEqual(self.board.mSunMoney, 0)

    def test_another_client_is_rejected_on_main_thread_and_gets_own_result(self):
        self.dispatch('setMoney', {'value': 77})
        self.dispatch('winLevel', client_id='another')
        self.run_tasks()
        self.assertEqual(self.calls, [])
        self.assertFalse(self.results('another')[0]['ok'])
        self.assertTrue(self.results()[0]['ok'])
        self.assertEqual(self.app.mPlayerInfo.mCoins, 77)
        with self.assertRaises(ValueError):
            self.dispatch('winLevel', client_id=None)

    def test_rechecks_session_before_execution(self):
        self.dispatch('winLevel')
        self.main_thread = True
        self.registry.release('client-1')
        self.registry.connect('client-2')
        self.main_thread = False
        self.run_tasks()
        self.assertEqual(self.calls, [])
        self.assertFalse(self.results()[0]['ok'])
        self.assertEqual(self.results('client-2'), [])

    def test_lineup_and_speed_results_are_json_data(self):
        self.dispatch('getLineup', request_id='lineup')
        self.dispatch('setSpeed', {'value': 2}, request_id='speed')
        self.run_tasks()
        results = self.results()
        self.assertEqual(results[0]['value'], 'lineup-code')
        self.assertEqual(results[1]['value'], [True, 2])

    def test_missing_board_returns_error_without_stopping_other_actions(self):
        self.board = None
        self.dispatch('getLineup', request_id='missing-board')
        self.dispatch('setMoney', {'value': 123}, request_id='money')
        self.run_tasks()
        results = self.results()
        self.assertFalse(results[0]['ok'])
        self.assertEqual(results[0]['errortype'], 'RuntimeError')
        self.assertTrue(results[1]['ok'])
        self.assertEqual(self.app.mPlayerInfo.mCoins, 123)

    def test_scary_pot_ui_variants_are_mapped_on_the_backend(self):
        for pot_type, count in [('None', 0), ('Sun1', 1), ('Sun2', 2), ('Sun3', 3), ('Seed', 0), ('Zombie', 0)]:
            with self.subTest(pot_type=pot_type):
                self.dispatch('placeGridItem', {
                    'row': -1, 'col': -1, 'gridItemType': 'ScaryPot', 'potType': pot_type,
                    'appearance': 'ScaryPotLeaf', 'zombieType': 'Normal', 'seedType': 'Peashooter',
                })
                self.run_tasks()
                self.assertTrue(self.results()[0]['ok'])
                method, args = self.calls[-1]
                self.assertEqual(method, 'AddScaryPotOnBoard')
                self.assertEqual(args[2], getattr(self.lawn.ScaryPotType, 'Sun' if count else pot_type))
                self.assertEqual(args[-1], count)

    def test_zombie_spawn_mode_and_enemy_only_flags_are_preserved(self):
        self.dispatch('setZombies', {'types': ['Normal', 'Football'], 'natural': True})
        self.dispatch('removeZombies', {'enemyOnly': True}, request_id='remove')
        self.run_tasks()
        self.assertEqual(self.calls, [
            ('CheatSetZombies', ([self.lawn.ZombieType.Normal, self.lawn.ZombieType.Football], True)),
            ('RemoveZombieOnBoard', (True,)),
        ])

    def test_state_read_write_and_snapshot_only_happen_on_main_thread(self):
        self.submit('apply', state={'cheat': {'noCooldown': True}}, request_id='apply')
        self.submit('snapshot', request_id='snapshot')
        self.assertFalse(self.state._value)
        self.assertEqual(self.results(), [])
        self.run_tasks()
        results = self.results()
        self.assertTrue(self.state._value)
        self.assertTrue(results[0]['ok'])
        self.assertTrue(results[1]['value']['state']['cheat']['noCooldown'])

    def test_connect_applies_pc_state_and_reads_mobile_state_on_main_thread(self):
        self.submit('connect', client_id='pc', takeover=True,
                    state={'cheat': {'noCooldown': True}}, request_id='pc')
        self.assertFalse(self.state._value)
        self.run_tasks()
        self.assertTrue(self.results('pc')[0]['value']['state']['cheat']['noCooldown'])
        self.submit('connect', client_id='mobile', takeover=True, request_id='mobile')
        self.run_tasks()
        self.assertTrue(self.results('mobile')[0]['value']['state']['cheat']['noCooldown'])

    def prepare_easter_egg_options(self):
        tree = ast.parse((ROOT / 'pgvztool/cheat.py').read_text(encoding='utf-8'))
        names = {'_get_easter_egg_mode', '_set_easter_egg_mode', '_apply_easter_egg_mode',
                 'RestoreNormalMowerAnimation', 'CheatOption', 'GetEasterEggModes', 'ApplyEasterEggModesToBoard'}
        nodes = [node for node in tree.body if getattr(node, 'name', None) in names or (
            isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id in ('EASTER_EGG_MODES', 'cheat_option'))]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'cheat-options', 'exec'), self.option_namespace)
        self.registry.register('cheat', self.option_namespace['cheat_option'])
        self.app.mEasyPlantingCheat = False
        self.app.mMuteSoundsForCutscene = False
        self.board.mApp = self.app
        self.board.mLawnMowers = []
        self.lawn.LawnMowerType = types.SimpleNamespace(Lawn='lawn')
        self.lawn.GlobalMembersReanimIds = types.SimpleNamespace(ReanimTrackId_anim_normal='anim_normal')
        for name in ('auto_collector', 'script_inf_sun', 'script_skill_nocooling', 'script_mushroom_awake',
                     'script_auto_restock', 'script_freeze_portal'):
            self.option_namespace[name] = types.SimpleNamespace(enabled=False)

        modes = ('DaisyMode', 'DanceMode', 'PinataMode', 'MustacheMode', 'SuperMowerMode', 'FutureMode')

        def native_setter(mode):
            def set_mode(enabled):
                self.assertTrue(self.main_thread)
                self.calls.append(('Set' + mode, enabled))
                setattr(self.board, 'm' + mode, enabled)
                setattr(self.app, 'm' + mode, enabled)
                if mode == 'SuperMowerMode':
                    self.mower_animation = 'anim_tricked'
            return set_mode

        for mode in modes:
            setattr(self.app, 'm' + mode, False)
            setattr(self.board, 'm' + mode, False)
            setattr(self.board, 'Set' + mode, native_setter(mode))
        return modes

    def test_easter_egg_options_read_native_modes_and_restore_mower_animation(self):
        modes = self.prepare_easter_egg_options()
        keys = self.option_namespace['EASTER_EGG_MODES']
        self.app.mBoard = None
        self.submit('apply', state={'cheat': {'danceMode': True}})
        self.submit('snapshot')
        self.run_tasks()
        applied, snapshot = [result['value'] for result in self.results()]
        self.assertEqual(applied['state'], {'cheat': {'danceMode': True}})
        self.assertLess(applied['revision'], snapshot['revision'])
        self.assertEqual(self.calls, [])

        self.app.mBoard = self.board
        self.submit('apply', state={'cheat': dict.fromkeys(keys, True)})
        self.submit('snapshot')
        self.run_tasks()
        self.assertEqual(self.calls, [('Set' + mode, True) for mode in modes])
        snapshot = self.results()[1]['value']['state']['cheat']
        self.assertTrue(all(snapshot[key] for key in keys))

        self.board.mLawnMowers = [types.SimpleNamespace(mDead=False, mMowerType='lawn', mReanimID=1)]

        def set_frames(layer):
            self.calls.append((1, layer))
            self.mower_animation = layer

        self.app.ReanimationTryToGet = lambda anim_id: types.SimpleNamespace(SetFramesForLayer=set_frames,
            IsAnimPlaying=lambda layer: self.mower_animation == layer)
        self.submit('apply', state={'cheat': {'superMowerMode': False}})
        self.submit('apply', state={'cheat': {'superMowerMode': False}})
        self.run_tasks()
        self.assertTrue(all(result['ok'] for result in self.results()))
        self.assertEqual(self.calls[len(modes):], [('SetSuperMowerMode', False), (1, 'anim_normal')])

    def test_easter_egg_hooks_preserve_option_state_on_load_and_push_keyboard_changes(self):
        self.prepare_easter_egg_options()
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        names = {'_sync_easter_eggs_after_key', 'Board__DoTypingCheck', 'GameSelector__KeyDown', 'Board__LoadGame'}
        nodes = [node for node in tree.body if getattr(node, 'name', None) in names]
        for node in nodes:
            node.decorator_list = []
        hooks = dict(self.option_namespace, sync_reg=self.registry)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'easter-egg-hooks', 'exec'), hooks)
        self.main_thread = True
        options = hooks['cheat_option']
        self.app.mDanceMode = True

        def read_old_save(board, path):
            board.mDanceMode = False
            board.mFutureMode = True
            return True

        self.assertTrue(hooks['Board__LoadGame'](read_old_save, self.board, 'old.dat'))
        self.assertTrue(self.board.mDanceMode)
        self.assertFalse(self.board.mFutureMode)
        self.assertTrue(options.danceMode)
        self.assertFalse(options.futureMode)
        self.assertFalse(self.app.mMuteSoundsForCutscene)
        self.assertEqual(self.calls, [('SetDanceMode', True), ('SetFutureMode', False)])
        self.board.mDanceMode = False
        self.assertFalse(hooks['Board__LoadGame'](lambda board, path: False, self.board, 'bad.dat'))
        self.assertFalse(self.board.mDanceMode)

        with patch.object(self.sync_module, '_broadcast_execution_result') as broadcast:
            hooks['Board__DoTypingCheck'](lambda board, key: None, self.board, 'X')
            hooks['Board__DoTypingCheck'](lambda board, key: board.SetFutureMode(True), self.board, 'E')
            hooks['GameSelector__KeyDown'](lambda selector, key: setattr(self.app, 'mDaisyMode', True), object(), 'S')
        self.assertEqual(broadcast.call_count, 2)
        first, second = [json.loads(call.args[0]) for call in broadcast.call_args_list]
        self.assertEqual((second['action'], second['_clientId']), ('sync', 'client-1'))
        self.assertLess(first['revision'], second['revision'])
        self.assertTrue(options.futureMode and options.daisyMode)
        self.assertEqual(first['state'], {'cheat': {'futureMode': True}})
        self.assertEqual(second['state'], {'cheat': {'daisyMode': True}})

    def test_konami_action_plays_native_sound_without_a_board(self):
        self.app.mBoard = None
        self.app.PlayFoley = self.calls.append
        self.dispatch('playKonamiSound')
        self.assertEqual(self.calls, [])
        self.run_tasks()
        self.assertTrue(self.results()[0]['ok'])
        self.assertEqual(self.calls, ['Drop'])

    def test_rejected_connect_is_delivered_without_touching_state(self):
        self.submit('connect', client_id='other', state={'cheat': {'noCooldown': True}})
        self.run_tasks()
        result = self.results('other')[0]
        self.assertTrue(result['ok'])
        self.assertEqual(result['value']['action'], 'sessionRejected')
        self.assertFalse(self.state._value)

    def test_release_is_a_main_thread_control_request_and_cancels_later_work(self):
        self.dispatch('setMoney', {'value': 3})
        self.run_tasks()
        self.submit('release', request_id='release')
        self.dispatch('placeMower', request_id='after-release')
        self.assertEqual(self.registry._active_client_id, 'client-1')
        self.run_tasks()
        self.assertIsNone(self.registry._active_client_id)
        self.assertEqual(self.results(), [])
        self.assertEqual(self.calls, [])

    def test_takeover_blocks_queued_actions_and_late_reconnects_from_previous_owner(self):
        self.submit('connect', client_id='new', takeover=True)
        self.dispatch('winLevel', request_id='old-action')
        self.submit('connect', request_id='old-reconnect')
        self.run_tasks()
        self.assertEqual(self.calls, [])
        old_results = self.results()
        self.assertEqual(old_results[0]['errortype'], 'SessionRejected')
        self.assertEqual(old_results[1]['value']['action'], 'sessionRejected')
        self.assertEqual(self.results('new')[0]['value']['action'], 'sync')
        self.assertEqual(self.registry._active_client_id, 'new')

    def test_takeover_flag_requires_a_boolean(self):
        self.submit('connect', client_id='other', takeover='false')
        self.run_tasks()
        self.assertEqual(self.results('other')[0]['errortype'], 'TypeError')
        self.assertEqual(self.registry._active_client_id, 'client-1')

    def test_business_execution_does_not_hold_the_queue_lock(self):
        def probe():
            self.assertFalse(self.dispatcher._lock.locked())
            thread = threading.Thread(target=lambda: self.submit('snapshot', request_id='worker'))
            thread.start()
            thread.join(timeout=1)
            self.assertFalse(thread.is_alive())
        self.dispatcher._actions['probe'] = (probe, ())
        self.dispatch('probe')
        self.run_tasks()
        self.assertEqual([item['id'] for item in self.results()], ['request-1'])
        self.run_tasks()
        self.assertEqual([item['id'] for item in self.results()], ['worker'])


    def test_failed_connect_restores_previous_session_owner(self):
        self.main_thread = True
        self.registry.release('client-1')
        self.main_thread = False
        with patch.object(self.registry, 'serialize', side_effect=RuntimeError('state unavailable')):
            self.submit('connect')
            self.run_tasks()
        self.assertFalse(self.results()[0]['ok'])
        self.assertIsNone(self.registry._active_client_id)

    def test_option_class_only_contains_initialization_and_properties(self):
        tree = ast.parse((ROOT / 'pgvztool/cheat.py').read_text(encoding='utf-8'))
        cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'CheatOption')
        for method in cls.body:
            if isinstance(method, ast.FunctionDef) and method.name != '__init__':
                self.assertTrue(method.decorator_list, method.name)
                self.assertTrue(all((isinstance(d, ast.Name) and d.id == 'property')
                                    or (isinstance(d, ast.Attribute) and d.attr == 'setter')
                                    for d in method.decorator_list), method.name)

    def test_duplicate_request_executes_once_and_replays_cached_result(self):
        for _ in range(2):
            self.dispatch('placeMower', request_id='same')
        self.run_tasks()
        self.assertEqual(len(self.calls), 1)
        first = self.results()
        self.dispatch('placeMower', request_id='same')
        self.run_tasks()
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.results(), first)
        with self.assertRaises(ValueError):
            self.dispatch('startMower', request_id='same')

    def test_poll_repeats_results_until_client_acknowledges(self):
        self.dispatch('placeMower')
        self.run_tasks()
        first = json.loads(self.dispatcher.poll('client-1'))
        self.assertEqual(json.loads(self.dispatcher.poll('client-1')), first)
        self.dispatcher.acknowledge('other', json.dumps([first['results'][0]['id']]))
        self.assertEqual(json.loads(self.dispatcher.poll('client-1')), first)
        self.results()
        self.assertEqual(json.loads(self.dispatcher.poll('client-1'))['results'], [])

    def test_pending_request_survives_long_background_pause(self):
        with patch.object(self.dispatcher_module.time, 'monotonic', return_value=100):
            self.dispatch('placeMower')
        with patch.object(self.dispatcher_module.time, 'monotonic', return_value=10000):
            self.run_tasks()
            result = self.results()[0]
        self.assertTrue(result['ok'])
        self.assertEqual(len(self.calls), 1)

    def test_only_acknowledged_results_expire_and_background_page_can_collect_later(self):
        with patch.object(self.dispatcher_module.time, 'monotonic', return_value=100):
            self.dispatch('placeMower', request_id='acknowledged')
            self.run_tasks()
            self.results()
            self.dispatch('startMower', request_id='orphan')
            self.run_tasks()
        with patch.object(self.dispatcher_module.time, 'monotonic', return_value=161):
            self.run_tasks()
        self.assertEqual(list(self.dispatcher._records), [('client-1', 'orphan')])
        with patch.object(self.dispatcher_module.time, 'monotonic', return_value=10000):
            self.assertEqual(self.results()[0]['id'], 'orphan')
            self.run_tasks()
        self.assertEqual(self.dispatcher._records, {})
        self.assertEqual(self.dispatcher._pending, [])

    def test_cancelled_pending_request_cannot_run_or_affect_other_clients(self):
        self.dispatch('placeMower', request_id='cancel-me')
        self.dispatcher.cancel('other', '["cancel-me"]')
        self.assertEqual(self.dispatcher._records[('client-1', 'cancel-me')]['status'], 'pending')
        self.dispatcher.cancel('client-1', '["cancel-me"]')
        self.run_tasks()
        self.assertEqual(self.calls, [])
        self.assertEqual(self.results(), [])
        # 即使取消响应丢失后重复提交，也只取回取消结果。
        self.dispatch('placeMower', request_id='cancel-me')
        self.run_tasks()
        self.assertEqual(self.results()[0]['errortype'], 'RequestCancelled')
        self.assertEqual(self.calls, [])

    def test_cancelling_running_request_discards_reply_without_interrupting_game_code(self):
        def operation():
            thread = threading.Thread(target=lambda: self.dispatcher.cancel('client-1', '["running"]'))
            thread.start()
            thread.join(timeout=1)
            self.assertFalse(thread.is_alive())
            self.calls.append(('completed', ()))
        self.dispatcher._actions['operation'] = (operation, ())
        self.dispatch('operation', request_id='running')
        self.run_tasks()
        self.assertEqual(self.calls, [('completed', ())])
        self.assertEqual(self.results(), [])
        self.assertEqual(self.dispatcher._records[('client-1', 'running')]['status'], 'done')


if __name__ == '__main__':
    unittest.main()
