import enum
import importlib.util
import json
import pathlib
import sys
import types
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]


class SyncTests(unittest.TestCase):
    def setUp(self):
        pgvz = types.ModuleType('pgvz')
        pgvz.__game_version__ = '1.3.4'
        version = types.ModuleType('pgvz.version')
        version.MOD_VERSION = 'test'
        sexy = types.ModuleType('Sexy')
        sexy.Debug = types.SimpleNamespace(Log=lambda *args: None)
        sexy.DebugType = types.SimpleNamespace(Error='Error')
        system = types.ModuleType('System')

        class Choice(enum.Enum):
            A = 1
            B = 2
            def GetType(self):
                return types.SimpleNamespace(IsEnum=True, enum_type=type(self))
            def __str__(self):
                return self.name

        def parse_enum(enum_type, value):
            try:
                return enum_type.enum_type[value]
            except (KeyError, TypeError):
                # Model a .NET conversion exception, which need not be a Python ValueError.
                raise RuntimeError('invalid enum value')

        system.Enum = types.SimpleNamespace(Parse=parse_enum)
        spec = importlib.util.spec_from_file_location('sync_test', ROOT / 'pgvztool/sync.py')
        self.module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'pgvz': pgvz, 'pgvz.version': version, 'Sexy': sexy, 'System': system}):
            spec.loader.exec_module(self.module)

        self.Choice = Choice
        class State(self.module.Serializable):
            def __init__(self):
                self.flag = False
                self.count = 1
                self.choice = Choice.A
                self._guarded = 1
                self._private = False
                self.nested = object()

            @property
            def guarded(self):
                return self._guarded

            @guarded.setter
            def guarded(self, value):
                self._guarded = int(value)

            @property
            def readonly(self):
                return 7

        self.state = State()
        self.other = State()
        self.registry = self.module.SyncRegistry()
        self.registry.register('first', self.state)
        self.registry.register('second', self.other)
        self.registry.connect('client')

    def apply(self, **objects):
        self.registry.apply(json.dumps(dict(objects, _clientId='client')))

    def test_serializes_public_attributes_and_properties_without_registration(self):
        self.state.added_later = 'included automatically'
        self.assertEqual(self.state.to_dict(), {
            'flag': False, 'count': 1, 'choice': 'A', 'guarded': 1,
            'readonly': 7, 'added_later': 'included automatically',
        })

    def test_applies_simple_attributes_properties_and_enum(self):
        self.apply(first={'flag': True, 'count': 10, 'choice': 'B', 'guarded': '5'})
        self.assertTrue(self.state.flag)
        self.assertEqual(self.state.count, 10)
        self.assertIs(self.state.choice, self.Choice.B)
        self.assertEqual(self.state.guarded, 5)

    def test_push_reads_current_selected_fields_from_registered_groups(self):
        class OnDemand(self.module.Serializable):
            def __init__(self):
                self.status = 'available'

            @property
            def unrelated(self):
                raise AssertionError('unselected property was read')

        self.registry.register('demand', OnDemand())
        self.state.choice = self.Choice.B
        with patch.object(self.module, '_broadcast_execution_result') as broadcast:
            self.registry.push_state(first=('choice', '_private', 'unknown'), demand='status', second=None)
            self.registry.push_state(unknown=None)
            self.registry.release('client')
            self.registry.push_state(demand=None)
        broadcast.assert_called_once()
        event = json.loads(broadcast.call_args.args[0])
        self.assertEqual((event['action'], event['_clientId']), ('sync', 'client'))
        self.assertEqual(event['state'], {
            'first': {'choice': 'B'}, 'demand': {'status': 'available'}, 'second': self.other.to_dict(),
        })

    def test_apply_returns_current_values_only_for_requested_fields(self):
        message = json.dumps({'_clientId': 'client', 'first': {'guarded': '5', 'choice': 'Missing'},
                              'second': {'flag': True}, 'unknown': {'count': 4}})
        result = self.registry.apply(message, return_sync=True)
        self.assertEqual(result['action'], 'sync')
        self.assertEqual(result['state'], {'first': {'guarded': 5, 'choice': 'A'}, 'second': {'flag': True}})

    def test_simple_fields_have_no_extra_type_or_range_validation(self):
        self.apply(first={'flag': 'direct assignment', 'count': -1})
        self.assertEqual(self.state.flag, 'direct assignment')
        self.assertEqual(self.state.count, -1)

    def test_unknown_private_and_unsupported_fields_are_ignored(self):
        original = self.state.nested
        self.apply(first={'missing': 1, '_private': True, 'nested': 'overwrite', 'from_dict': 'overwrite'},
                   unknown={'flag': True})
        self.assertFalse(hasattr(self.state, 'missing'))
        self.assertFalse(self.state._private)
        self.assertIs(self.state.nested, original)
        self.assertTrue(callable(self.state.from_dict))

    def test_failed_enum_conversion_does_not_block_other_options(self):
        for value in ('Missing', [], None):
            with self.subTest(value=value):
                self.state.flag = False
                self.apply(first={'choice': value, 'flag': True}, second={'count': 3})
                self.assertIs(self.state.choice, self.Choice.A)
                self.assertTrue(self.state.flag)
                self.assertEqual(self.other.count, 3)

    def test_readonly_or_unassignable_property_is_ignored(self):
        self.state.from_dict({'guarded': 'bad number', 'readonly': 99, 'flag': True})
        self.assertEqual(self.state.guarded, 1)
        self.assertEqual(self.state.readonly, 7)
        self.assertTrue(self.state.flag)

    def test_non_object_state_is_ignored(self):
        self.apply(first=[], second={'flag': True})
        self.assertFalse(self.state.flag)
        self.assertTrue(self.other.flag)

    def test_foreign_client_cannot_apply_state(self):
        with self.assertRaises(RuntimeError):
            self.registry.apply(json.dumps({'_clientId': 'other', 'first': {'flag': True}}))
        self.assertFalse(self.state.flag)

    def test_failed_initial_snapshot_restores_session_owner(self):
        self.registry.release('client')
        with patch.object(self.registry, 'serialize', side_effect=RuntimeError('snapshot unavailable')):
            with self.assertRaises(RuntimeError):
                self.registry.connect('new')
        self.assertIsNone(self.registry._active_client_id)
        self.assertNotIn('new', self.registry._initialized_clients)

    def test_restoration_runs_once_even_after_lost_reply_release_and_long_pause(self):
        self.registry.release('client')
        payload = json.dumps({'_clientId': 'pc', 'first': {'flag': True}})
        self.registry.connect('pc', payload)  # 首次结果丢失。
        self.assertTrue(self.state.flag)
        self.state.flag = False  # 游戏中后续修改不能被重连时的旧设置覆盖。
        self.registry.release('pc')
        with patch('time.monotonic', return_value=100000):
            result = json.loads(self.registry.connect('pc', payload))
        self.assertFalse(self.state.flag)
        self.assertFalse(result['state']['first']['flag'])

    def test_new_game_registry_restores_same_page_again(self):
        registry = self.module.SyncRegistry()
        registry.register('first', self.state)
        payload = json.dumps({'_clientId': 'client', 'first': {'flag': True}})
        registry.connect('client', payload)
        self.assertTrue(self.state.flag)

    def test_background_pause_does_not_expire_ownership(self):
        with patch('time.monotonic', return_value=100000):
            result = json.loads(self.registry.connect('other'))
        self.assertEqual(result['action'], 'sessionRejected')
        self.assertEqual(self.registry._active_client_id, 'client')

    def test_takeover_revokes_old_page_even_after_new_page_releases(self):
        result = json.loads(self.registry.connect('new', takeover=True))
        self.assertEqual(result['action'], 'sync')
        with self.assertRaises(self.module.SessionRejected):
            self.registry.require_client('client')
        self.registry.release('client')  # 旧页面迟到退出不释放新会话。
        self.assertEqual(self.registry._active_client_id, 'new')
        self.registry.release('new')
        self.assertEqual(json.loads(self.registry.connect('client'))['action'], 'sessionRejected')
        self.assertEqual(json.loads(self.registry.connect('client', takeover=True))['action'], 'sync')

    def test_failed_takeover_keeps_previous_owner_and_can_retry_restoration(self):
        payload = json.dumps({'_clientId': 'new', 'first': {'flag': True}})
        with patch.object(self.registry, 'serialize', side_effect=RuntimeError('snapshot unavailable')):
            with self.assertRaises(RuntimeError):
                self.registry.connect('new', payload, takeover=True)
        self.assertEqual(self.registry._active_client_id, 'client')
        self.assertNotIn('client', self.registry._revoked_clients)
        self.assertNotIn('new', self.registry._initialized_clients)
        self.state.flag = False
        self.registry.connect('new', payload, takeover=True)
        self.assertTrue(self.state.flag)


if __name__ == '__main__':
    unittest.main()
