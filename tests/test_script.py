import importlib.util
import pathlib
import sys
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeGameMode:
    Adventure = 0
    Survival = 1
    GameModeCount = 2


class FakeGameScenes:
    Menu = 0
    LevelIntro = 1
    Playing = 2


class FakeApp:
    def __init__(self):
        self.mGameMode = FakeGameMode.Adventure
        self.mGameScene = FakeGameScenes.Playing
        self.mBoard = object()

    def GetDialog(self, dialog_id):
        return None


def load_script_module():
    lawn = types.ModuleType("Lawn")
    lawn.GameMode = FakeGameMode
    lawn.GameScenes = FakeGameScenes
    sys.modules["Lawn"] = lawn

    sexy = types.ModuleType("Sexy")
    sexy.Debug = types.SimpleNamespace(Log=lambda message: None)
    sys.modules["Sexy"] = sexy

    package = types.ModuleType("test_script_pgvz")
    package.__path__ = [str(ROOT / "pgvz")]
    sys.modules["test_script_pgvz"] = package

    app = FakeApp()
    util = types.ModuleType("test_script_pgvz.util")
    util.GetLawnApp = lambda: app
    sys.modules["test_script_pgvz.util"] = util

    spec = importlib.util.spec_from_file_location(
        "test_script_pgvz.script", ROOT / "pgvz" / "script.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, app


class ScriptManagerTests(unittest.TestCase):
    def setUp(self):
        self.script, self.app = load_script_module()
        self.manager = self.script.ScriptManager()

    def test_script_conf_uses_requested_public_names(self):
        condition = lambda: True
        conf = self.script.ScriptConf(
            runmode=self.script.ScriptRunMode.ONCE,
            runcond=condition,
        )

        self.assertEqual(conf.runmode, self.script.ScriptRunMode.ONCE)
        self.assertIs(conf.runcond, condition)

    def test_register_preserves_gamemode_and_runmode_parameters(self):
        script_obj = self.manager.Register(
            lambda: None,
            gamemode=FakeGameMode.Adventure,
            runmode=self.script.ScriptRunMode.ONCE,
        )

        self.assertEqual(script_obj.conf.runmode, self.script.ScriptRunMode.ONCE)
        self.assertTrue(script_obj.conf.runcond())
        self.assertEqual(
            script_obj.script_type,
            self.script.ScriptType.TICKRUNNER,
        )

        self.app.mGameMode = FakeGameMode.Survival
        self.assertFalse(script_obj.conf.runcond())

    def test_run_in_thread_returns_registered_script_object(self):
        events = []

        def helper_script():
            events.append("started")
            yield

        script_obj = self.manager.RunInThread(helper_script)

        self.assertIsInstance(script_obj, self.script.ScriptObj)
        self.assertEqual(
            script_obj.script_type,
            self.script.ScriptType.COROUTINE,
        )
        self.assertEqual(script_obj.conf.runmode, self.script.ScriptRunMode.ONCE)
        self.assertTrue(script_obj.Run())
        self.assertEqual(events, ["started"])
        self.assertTrue(self.manager.Unregister(script_obj))

    def test_run_in_thread_condition_captures_current_gamemode(self):
        def helper_script():
            yield

        script_obj = self.manager.RunInThread(helper_script)
        self.app.mGameMode = FakeGameMode.Survival

        self.assertTrue(script_obj.Run())
        self.assertIsNone(script_obj.generator)

    def test_run_in_thread_can_insert_task_while_manager_is_running(self):
        events = []
        helper_objects = []

        def helper_script():
            events.append("helper")
            yield

        def launcher_script():
            if not helper_objects:
                helper_objects.append(
                    self.manager.RunInThread(helper_script)
                )

        self.manager.Register(launcher_script)
        self.manager.Manage()
        self.manager.Manage()

        self.assertEqual(len(helper_objects), 1)
        self.assertIsInstance(helper_objects[0], self.script.ScriptObj)
        self.assertEqual(events, ["helper"])

    def test_manager_uses_requested_member_names(self):
        self.assertEqual(self.manager.script_list, [])
        self.assertEqual(self.manager.global_script_list, [])
        self.assertIsNone(self.manager._prev_scene)


if __name__ == "__main__":
    unittest.main()
