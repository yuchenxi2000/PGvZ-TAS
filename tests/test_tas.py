import importlib.util
import pathlib
import sys
import tempfile
import types
import unittest


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


if __name__ == '__main__':
    unittest.main()
