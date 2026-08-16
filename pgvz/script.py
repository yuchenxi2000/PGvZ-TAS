import enum
import inspect
import Lawn
import Sexy
from .util import GetLawnApp

class ScriptType(enum.Enum):
    COROUTINE = 0
    TICKRUNNER = 1

class ScriptRunMode(enum.Enum):
    FOREVER = 0
    ONCE = 1
    GLOBAL = 2

class ScriptConf:
    def __init__(self, runmode: ScriptRunMode, runcond) -> None:
        self.runmode = runmode
        self.runcond = runcond

class ScriptObj:
    def __init__(self, script_func, conf: ScriptConf) -> None:
        self.script_func = script_func
        self.conf = conf
        self.generator = None
        self.enabled = True
        if inspect.isgeneratorfunction(script_func):
            # 协程，需要每帧调用next函数
            self.script_type = ScriptType.COROUTINE
        else:
            # 每帧运行的函数
            self.script_type = ScriptType.TICKRUNNER
    
    def On(self):
        self.enabled = True
    
    def Off(self):
        self.enabled = False
    
    def Start(self):
        if self.script_type == ScriptType.COROUTINE:
            self.generator = self.script_func()
    
    def Reset(self):
        self.generator = None
    
    def Run(self) -> bool:
        if not self.enabled:
            return True
        if not self.conf.runcond():
            self.Reset()
            return True
        if self.script_type == ScriptType.COROUTINE:
            if self.generator is None:
                return False
            try:
                next(self.generator)
                return True
            except StopIteration:
                return False
        elif self.script_type == ScriptType.TICKRUNNER:
            self.script_func()
            return True
        else:
            return False

class ScriptManager:
    def __init__(self) -> None:
        self.loaded = False
        self.script_list = []
        self.global_script_list = []
        self._prev_scene: 'Lawn.GameScenes | None' = None
    
    def Register(self, script_func, gamemode: 'Lawn.GameMode | None' = None, runmode: ScriptRunMode = ScriptRunMode.FOREVER, conf: 'ScriptConf | None' = None) -> ScriptObj:
        if conf is not None:
            runconf = conf
        else:
            if gamemode is None or gamemode == Lawn.GameMode.GameModeCount:
                runconf = ScriptConf(runmode, lambda: True)
            else:
                runconf = ScriptConf(runmode, lambda: GetLawnApp().mGameMode == gamemode)
        scriptObj = ScriptObj(script_func, runconf)
        if runconf.runmode == ScriptRunMode.GLOBAL:
            scriptObj.Start()
            self.global_script_list.append(scriptObj)
        else:
            self.script_list.append(scriptObj)
        Sexy.Debug.Log(f'registered script func: {script_func}')
        return scriptObj
    
    def Unregister(self, scriptObj: ScriptObj) -> bool:
        try:
            self.script_list.remove(scriptObj)
            return True
        except ValueError:
            return False

    def RunInThread(self, script_func) -> ScriptObj:
        gamemode = GetLawnApp().mGameMode
        conf = ScriptConf(ScriptRunMode.ONCE, lambda: GetLawnApp().mGameMode == gamemode)
        scriptObj = ScriptObj(script_func, conf)
        scriptObj.Start()
        self.script_list.append(scriptObj)
        return scriptObj
    
    def Manage(self):
        lawnapp = GetLawnApp()
        # run global scripts
        finishedGlobalScripts = []
        for scriptObj in self.global_script_list:
            if not scriptObj.Run():
                finishedGlobalScripts.append(scriptObj)
        for scriptObj in finishedGlobalScripts:
            self.global_script_list.remove(scriptObj)
        # 退出战斗界面时卸载被设置为只运行一次的脚本
        leaveFight = self._prev_scene == Lawn.GameScenes.Playing and lawnapp.mGameScene != Lawn.GameScenes.Playing
        backToMain = self._prev_scene == Lawn.GameScenes.LevelIntro and lawnapp.mGameScene not in (Lawn.GameScenes.Playing, Lawn.GameScenes.LevelIntro)
        if leaveFight or backToMain:
            if self.loaded:
                tmpList = []
                for scriptObj in self.script_list:
                    if scriptObj.conf.runmode == ScriptRunMode.FOREVER:
                        tmpList.append(scriptObj)
                    else:
                        Sexy.Debug.Log(f'unload script func: {scriptObj.script_func}')
                self.script_list = tmpList
                self.loaded = False
        # 只有在存在Board（关卡内）、在Playing状态下、并且没有继续游戏的对话框时，才能运行脚本
        gamescene_ok = lawnapp.mGameScene in (Lawn.GameScenes.Playing, Lawn.GameScenes.LevelIntro)
        if lawnapp.mBoard is not None and gamescene_ok and lawnapp.GetDialog(37) is None:
            if self.loaded:
                # run all scripts
                for scriptObj in self.script_list:
                    scriptObj.Run()
            else:
                # load all scripts
                for scriptObj in self.script_list:
                    scriptObj.Start()
                    Sexy.Debug.Log(f'load script func: {scriptObj.script_func}')
                self.loaded = True
        self._prev_scene = lawnapp.mGameScene
