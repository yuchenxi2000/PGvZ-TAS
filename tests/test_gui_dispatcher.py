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
        }.items():
            setattr(self.lawn, name, enum.Enum(name, members))
        self.lawn.LawnApp = self.lawn.Board = self.lawn.PlayerInfo = self.lawn.GardenType = object
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
        namespace = {
            'Lawn': self.lawn, 'GetBoard': get_board, 'GetLawnApp': get_app,
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
        sexy = types.ModuleType('Sexy')
        sexy.Debug = types.SimpleNamespace(Log=lambda *args: None)
        sexy.DebugType = types.SimpleNamespace(Error='error')
        package_name = 'test_dispatcher_pgvztool'
        package = types.ModuleType(package_name)
        package.__path__ = [str(ROOT / 'pgvztool')]
        modules = {'Lawn': self.lawn, 'pgvz': pgvz, 'pgvz.version': version,
                   'Sexy': sexy, 'System': types.ModuleType('System'), package_name: package}
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
            self.registry = sync.sync_reg

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

    def submit(self, kind, client_id='client-1', request_id='request-1', **details):
        return json.loads(self.dispatcher.submit(json.dumps(dict(
            details, _clientId=client_id, id=request_id, kind=kind,
        ))))

    def dispatch(self, name, args=None, client_id='client-1', request_id='request-1'):
        return self.submit('action', client_id, request_id, name=name, args={} if args is None else args)

    def run_tasks(self):
        self.main_thread = True
        try:
            self.dispatcher.run_pending()
        finally:
            self.main_thread = False

    def results(self, client_id='client-1'):
        return json.loads(self.dispatcher.poll(client_id))['results']

    def test_game_state_is_only_accessed_when_main_thread_task_runs(self):
        queued = self.dispatch('setSun', {'value': 9990})
        self.assertEqual(queued, {'action': 'queued', 'id': 'request-1'})
        self.assertEqual(self.board.mSunMoney, 0)
        self.assertEqual(self.results(), [])
        self.run_tasks()
        self.assertEqual(self.board.mSunMoney, 9990)
        self.assertTrue(self.results()[0]['ok'])
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
                self.assertEqual(result['id'], 'request-1')
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
        self.submit('connect', state={'cheat': {'noCooldown': True}}, request_id='pc')
        self.assertFalse(self.state._value)
        self.run_tasks()
        self.assertTrue(self.results()[0]['value']['state']['cheat']['noCooldown'])
        self.submit('connect', request_id='mobile')
        self.run_tasks()
        self.assertTrue(self.results()[0]['value']['state']['cheat']['noCooldown'])

    def test_rejected_connect_is_delivered_without_touching_state(self):
        self.submit('connect', client_id='other', state={'cheat': {'noCooldown': True}})
        self.run_tasks()
        result = self.results('other')[0]
        self.assertTrue(result['ok'])
        self.assertEqual(result['value']['action'], 'sessionRejected')
        self.assertFalse(self.state._value)

    def test_heartbeat_and_release_are_main_thread_control_requests(self):
        self.submit('heartbeat', request_id='heartbeat')
        self.run_tasks()
        self.assertTrue(self.results()[0]['value']['accepted'])
        self.dispatch('setMoney', {'value': 3})
        self.run_tasks()
        self.submit('release', request_id='release')
        self.run_tasks()
        self.assertIsNone(self.registry._active_client_id)
        self.assertEqual(self.results(), [])

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


if __name__ == '__main__':
    unittest.main()
