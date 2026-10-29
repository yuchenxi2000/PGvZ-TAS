import importlib.util
import json
import os
import pathlib
import sys
import tempfile
import types
import unittest
from unittest.mock import patch


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeCreativeLevelManager:
    levels = {}

    @classmethod
    def GetLevelDefine(cls, game_mode):
        return cls.levels.get(game_mode)


class FakeScriptManager:
    def Register(self, script, runmode=None):
        return script


def load_tas_module(context):
    lawn = types.ModuleType('Lawn')
    lawn.__path__ = []
    lawn.LawnApp = type('LawnApp', (), {})
    lawn.Board = type('Board', (), {})
    lawn.GameButton = type('GameButton', (), {})
    lawn.GameScenes = types.SimpleNamespace(Playing=1)
    lawn.GameMode = types.SimpleNamespace(
        ChallengeZenGarden=1,
        TreeOfWisdom=2,
        Upsell=3,
        Intro=4,
    )
    sys.modules['Lawn'] = lawn

    creative = types.ModuleType('Lawn.Creative')
    creative.CreativeLevelManager = FakeCreativeLevelManager
    lawn.Creative = creative
    sys.modules['Lawn.Creative'] = creative

    sexy = types.ModuleType('Sexy')
    sexy.GlobalStaticVars = types.SimpleNamespace(
        gSexyAppBase=types.SimpleNamespace(applicationStoragePath='.'),
    )
    sys.modules['Sexy'] = sexy

    pgvz = types.ModuleType('pgvz')
    pgvz.GetLawnApp = lambda: context['app']
    pgvz.GetBoard = lambda: context.get('board')
    pgvz.script_manager = FakeScriptManager()
    pgvz.ScriptRunMode = types.SimpleNamespace(FOREVER=1)
    sys.modules['pgvz'] = pgvz

    spec = importlib.util.spec_from_file_location(
        'test_tas_pgvztool.tas', ROOT / 'pgvztool' / 'tas.py'
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class TasSaveNameTests(unittest.TestCase):
    def setUp(self):
        self.context = {
            'app': types.SimpleNamespace(
                mGameMode=50000,
                mPlayerInfo=types.SimpleNamespace(mId=7),
                IsDIYMode=lambda: False,
                IsOnlineLevelMode=lambda: True,
            ),
        }
        FakeCreativeLevelManager.levels = {
            50000: types.SimpleNamespace(mCrc=0x89ABCDEF),
        }
        self.tas = load_tas_module(self.context)

    def test_custom_level_replaces_mode_with_game_crc_format(self):
        manager = self.tas.TasManager()

        self.assertEqual(manager._file_name(self.context['app'], 12345), '7_89ABCDEF_12345.dat')

    def test_normal_level_keeps_original_mode_file_name(self):
        self.context['app'].mGameMode = 12
        self.context['app'].IsOnlineLevelMode = lambda: False
        manager = self.tas.TasManager()

        self.assertEqual(manager._file_name(self.context['app'], 12345), '7_12_12345.dat')

    def test_local_custom_level_uses_the_same_crc_format(self):
        self.context['app'].mGameMode = 40000
        self.context['app'].IsDIYMode = lambda: True
        self.context['app'].IsOnlineLevelMode = lambda: False
        FakeCreativeLevelManager.levels[40000] = types.SimpleNamespace(mCrc=0x1234)
        manager = self.tas.TasManager()

        self.assertEqual(manager._file_name(self.context['app'], 12345), '7_00001234_12345.dat')

    def test_custom_level_without_definition_falls_back_to_mode(self):
        FakeCreativeLevelManager.levels = {}
        manager = self.tas.TasManager()

        self.assertEqual(manager._file_name(self.context['app'], 12345), '7_50000_12345.dat')

    def test_scan_only_loads_files_for_current_game_save_name(self):
        manager = self.tas.TasManager()
        with tempfile.TemporaryDirectory() as directory:
            manager._saveDir = pathlib.Path(directory)
            (manager._saveDir / '7_89ABCDEF_20.dat').touch()
            (manager._saveDir / '7_89ABCDEF_5.dat').touch()
            (manager._saveDir / '7_DEADBEEF_10.dat').touch()
            (manager._saveDir / '7_50000_15.dat').touch()

            manager.scan_and_load()

        self.assertEqual(manager._saves, [5, 20])


class FakeSnapshotBoard:
    def __init__(self):
        self.mMainCounter = 0
        self.mManualPaused = True
        self.save_error = None
        self.silent_save_failure = False
        self.bad_load = None
        self.bad_recovery = False
        self.load_calls = []

    def SaveGame(self, filename):
        if self.save_error:
            raise self.save_error
        if not self.silent_save_failure:
            pathlib.Path(filename).write_text(json.dumps({'frame': self.mMainCounter}), encoding='utf-8')

    def LoadGame(self, filename):
        self.load_calls.append(filename)
        if filename == self.bad_load or (self.bad_recovery and '.recovery-' in filename):
            self.mMainCounter = -999  # Native deserialization may already have mutated Board.
            return False
        self.mMainCounter = json.loads(pathlib.Path(filename).read_text(encoding='utf-8'))['frame']
        return True


class TasRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.board = FakeSnapshotBoard()
        self.context = {
            'app': types.SimpleNamespace(mGameMode=12, mPlayerInfo=types.SimpleNamespace(mId=7),
                                         IsDIYMode=lambda: False, IsOnlineLevelMode=lambda: False),
            'board': self.board,
        }
        self.tas = load_tas_module(self.context)
        self.manager = self.tas.TasManager()
        self.manager._saveDir = pathlib.Path(self.directory.name)
        for frame in (100, 200, 300):
            self.board.mMainCounter = frame
            self.manager.save()

    def disk(self):
        return {p.name: p.read_bytes() for p in self.manager._saveDir.iterdir() if p.name.endswith('.dat')}

    def test_save_exception_preserves_index_and_files(self):
        original = self.disk()
        self.board.mMainCounter = 400
        self.board.save_error = OSError('disk full')
        with self.assertRaises(OSError):
            self.manager.save()
        self.assertEqual(self.manager._saves, [100, 200, 300])
        self.assertEqual(self.manager._pointer, 2)
        self.assertEqual(self.disk(), original)

    def test_silent_native_save_failure_is_detected(self):
        self.board.mMainCounter = 400
        self.board.silent_save_failure = True
        with self.assertRaises(OSError):
            self.manager.save()
        self.assertEqual(self.manager._saves, [100, 200, 300])

    def test_same_frame_overwrite_is_atomic(self):
        original = self.disk()
        replace = pathlib.Path.replace
        def fail(source, destination):
            if '.write-' in source.name:
                raise OSError('replace denied')
            return replace(source, destination)
        with patch.object(pathlib.Path, 'replace', fail):
            with self.assertRaises(OSError):
                self.manager.save()
        self.assertEqual(self.disk(), original)
        self.assertEqual(self.manager._pointer, 2)

    def test_branch_staging_failure_restores_future_files(self):
        original = self.disk()
        self.manager._pointer = 0
        self.manager._browse = False
        self.board.mMainCounter = 150
        replace = pathlib.Path.replace
        def fail(source, destination):
            if source.name.endswith('_300.dat'):
                raise OSError('cannot retire future save')
            return replace(source, destination)
        with patch.object(pathlib.Path, 'replace', fail):
            with self.assertRaises(OSError):
                self.manager.save()
        self.assertEqual(self.disk(), original)
        self.assertEqual(self.manager._saves, [100, 200, 300])
        self.assertEqual(self.manager._pointer, 0)

    def test_branch_commit_failure_restores_colliding_future_filename(self):
        original = self.disk()
        self.manager._pointer = 0
        self.board.mMainCounter = 200
        replace = pathlib.Path.replace
        def fail(source, destination):
            if '.write-' in source.name:
                raise OSError('commit denied')
            return replace(source, destination)
        with patch.object(pathlib.Path, 'replace', fail):
            with self.assertRaises(OSError):
                self.manager.save()
        self.assertEqual(self.disk(), original)
        self.assertEqual(self.manager._pointer, 0)

    def test_branch_success_and_cleanup_failure_do_not_resurrect_future(self):
        self.manager._pointer = 0
        self.board.mMainCounter = 150
        unlink = pathlib.Path.unlink
        def fail(source, *args, **kwargs):
            if '.discard-' in source.name:
                raise OSError('cleanup denied')
            return unlink(source, *args, **kwargs)
        with patch.object(pathlib.Path, 'unlink', fail):
            self.assertTrue(self.manager.save())
        self.assertEqual(self.manager._saves, [100, 150])
        self.manager.scan_and_load()
        self.assertEqual(self.manager._saves, [100, 150])

    def test_truncate_failure_preserves_history(self):
        original = self.disk()
        with patch.object(pathlib.Path, 'replace', side_effect=OSError('denied')):
            with self.assertRaises(OSError):
                self.manager._truncate(1)
        self.assertEqual(self.disk(), original)
        self.assertEqual(self.manager._saves, [100, 200, 300])

    def test_undo_redo_commit_pointer_after_success(self):
        self.assertTrue(self.manager.undo())
        self.assertEqual((self.manager._pointer, self.board.mMainCounter), (1, 200))
        self.assertTrue(self.manager.redo())
        self.assertEqual((self.manager._pointer, self.board.mMainCounter), (2, 300))
        self.assertTrue(self.board.mManualPaused)

    def test_failed_load_restores_board_and_keeps_pointer(self):
        self.board.bad_load = str(self.manager._file_path(1))
        with self.assertRaises(OSError):
            self.manager.undo()
        self.assertEqual((self.manager._pointer, self.board.mMainCounter), (2, 300))
        self.assertTrue(self.manager._browse)
        self.assertFalse(any('.recovery-' in p.name for p in self.manager._saveDir.iterdir()))

    def test_failed_recovery_keeps_snapshot_and_pauses(self):
        self.board.bad_load = str(self.manager._file_path(1))
        self.board.bad_recovery = True
        with self.assertRaisesRegex(OSError, 'recovery file'):
            self.manager.undo()
        self.assertEqual(self.manager._pointer, 2)
        self.assertTrue(self.board.mManualPaused)
        self.assertTrue(any('.recovery-' in p.name for p in self.manager._saveDir.iterdir()))

    def test_recovery_write_failure_does_not_start_load(self):
        self.board.save_error = OSError('disk full')
        with self.assertRaises(OSError):
            self.manager.undo()
        self.assertEqual(self.board.load_calls, [])
        self.assertEqual(self.manager._pointer, 2)

    def test_missing_file_does_not_move_pointer(self):
        self.manager._file_path(1).unlink()
        with self.assertRaises(OSError):
            self.manager.undo()
        self.assertEqual(self.manager._pointer, 2)
        self.assertEqual(self.board.load_calls, [])

    def test_live_undo_retains_successful_autosave_if_load_fails(self):
        self.manager._browse = False
        self.board.mManualPaused = False
        self.board.mMainCounter = 350
        self.board.bad_load = str(self.manager._file_path(2))
        with self.assertRaises(OSError):
            self.manager.undo()
        self.assertEqual(self.manager._saves, [100, 200, 300, 350])
        self.assertEqual((self.manager._pointer, self.board.mMainCounter), (3, 350))
        self.assertFalse(self.manager._browse)
        self.assertFalse(self.board.mManualPaused)

    def test_run_action_reports_failure_without_raising_into_hook(self):
        self.board.save_error = OSError('disk full')
        self.assertFalse(self.manager.run_action(self.manager.ACTION_SAVE))
        self.assertEqual(self.manager.last_error, 'disk full')

    def test_scan_failure_preserves_existing_state(self):
        with patch.object(pathlib.Path, 'iterdir', side_effect=OSError('directory denied')):
            with self.assertRaises(OSError):
                self.manager.scan_and_load()
        self.assertEqual(self.manager._saves, [100, 200, 300])

    def test_failed_mkdir_does_not_cache_invalid_directory(self):
        manager = self.tas.TasManager()
        with patch.object(pathlib.Path, 'mkdir', side_effect=OSError('directory denied')):
            with self.assertRaises(OSError):
                manager._init_save_dir()
        self.assertIsNone(manager._saveDir)

    def test_init_save_dir_supports_legacy_mkdir_and_existing_directory(self):
        self.tas.Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath = self.directory.name
        expected = pathlib.Path(self.directory.name) / 'docs' / 'userdata' / 'tas_saves'

        def legacy_mkdir(path, mode=0o777, parents=False):
            # Match IronPython's signature: no exist_ok keyword.
            if parents:
                os.makedirs(str(path), mode)
            else:
                os.mkdir(str(path), mode)

        with patch.object(pathlib.Path, 'mkdir', legacy_mkdir):
            manager = self.tas.TasManager()
            manager._init_save_dir()
            self.assertEqual(manager._saveDir, expected)
            self.assertTrue(expected.is_dir())
            # A fresh manager must also accept the directory left by an earlier run.
            another = self.tas.TasManager()
            another._init_save_dir()
            self.assertEqual(another._saveDir, expected)


if __name__ == '__main__':
    unittest.main()
