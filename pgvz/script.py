import enum
import inspect
import Lawn
import Sexy
from .util import GetBoard, GetLawnApp

class ScriptType(enum.Enum):
    COROUTINE = 0
    TICKRUNNER = 1

class ScriptRunMode(enum.Enum):
    FOREVER = 0
    ONCE = 1
    GLOBAL = 2

class ScriptConf:
    def __init__(self, runmode: ScriptRunMode, canRunFunc) -> None:
        self.runmode = runmode
        self.canRunFunc = canRunFunc

class ScriptObj:
    def __init__(self, scriptGenFunc, conf: ScriptConf) -> None:
        self.scriptGenFunc = scriptGenFunc
        self.conf = conf
        self.scriptGen = None
        self.enabled = True
        if inspect.isgeneratorfunction(scriptGenFunc):
            # 协程，需要每帧调用next函数
            self.scriptType = ScriptType.COROUTINE
        else:
            # 每帧运行的函数
            self.scriptType = ScriptType.TICKRUNNER
    
    def On(self):
        self.enabled = True
    
    def Off(self):
        self.enabled = False
    
    def Start(self):
        if self.scriptType == ScriptType.COROUTINE:
            self.scriptGen = self.scriptGenFunc()
    
    def Reset(self):
        self.scriptGen = None
    
    def Run(self) -> bool:
        if not self.enabled:
            return True
        if not self.conf.canRunFunc():
            self.Reset()
            return True
        if self.scriptType == ScriptType.COROUTINE:
            if self.scriptGen is None:
                return False
            try:
                next(self.scriptGen)
                return True
            except StopIteration:
                return False
        elif self.scriptType == ScriptType.TICKRUNNER:
            self.scriptGenFunc()
            return True
        else:
            return False

class ScriptManager:
    def __init__(self) -> None:
        self.loaded = False
        self.scriptList = []
        self.globalScriptList = []
        self.prev_scene: Lawn.GameScenes = None  # type: ignore
    
    def Register(self, scriptGenFunc, gamemode: Lawn.GameMode = None, runmode: ScriptRunMode = ScriptRunMode.FOREVER, conf: ScriptConf = None) -> ScriptObj:  # type: ignore
        if conf is not None:
            runconf = conf
        else:
            if gamemode is None or gamemode == Lawn.GameMode.GameModeCount:
                runconf = ScriptConf(runmode, lambda: True)
            else:
                runconf = ScriptConf(runmode, lambda: GetLawnApp().mGameMode == gamemode)
        scriptObj = ScriptObj(scriptGenFunc, runconf)
        if runconf.runmode == ScriptRunMode.GLOBAL:
            scriptObj.Start()
            self.globalScriptList.append(scriptObj)
        else:
            self.scriptList.append(scriptObj)
        Sexy.Debug.Log(f'registered script func: {scriptGenFunc}')
        return scriptObj
    
    def Unregister(self, scriptObj: ScriptObj) -> bool:
        try:
            self.scriptList.remove(scriptObj)
            return True
        except ValueError:
            return False

    def RunInThread(self, scriptGenFunc):
        board = GetBoard()
        gamemode = GetLawnApp().mGameMode
        conf = ScriptConf(ScriptRunMode.ONCE, lambda: GetLawnApp().mGameMode == gamemode)
        scriptObj = ScriptObj(scriptGenFunc, conf)
        scriptObj.Start()
        self.scriptList.append(scriptObj)
    
    def Manage(self):
        lawnapp = GetLawnApp()
        # run global scripts
        finishedGlobalScripts = []
        for scriptObj in self.globalScriptList:
            if not scriptObj.Run():
                finishedGlobalScripts.append(scriptObj)
        for scriptObj in finishedGlobalScripts:
            self.globalScriptList.remove(scriptObj)
        # 退出战斗界面时卸载被设置为只运行一次的脚本
        leaveFight = self.prev_scene == Lawn.GameScenes.Playing and lawnapp.mGameScene != Lawn.GameScenes.Playing
        backToMain = self.prev_scene == Lawn.GameScenes.LevelIntro and lawnapp.mGameScene not in (Lawn.GameScenes.Playing, Lawn.GameScenes.LevelIntro)
        if leaveFight or backToMain:
            if self.loaded:
                tmpList = []
                for scriptObj in self.scriptList:
                    if scriptObj.conf.runmode == ScriptRunMode.FOREVER:
                        tmpList.append(scriptObj)
                    else:
                        Sexy.Debug.Log(f'unload script func: {scriptObj.scriptGenFunc}')
                self.scriptList = tmpList
                self.loaded = False
        # 只有在存在Board（关卡内）、在Playing状态下、并且没有继续游戏的对话框时，才能运行脚本
        gamescene_ok = lawnapp.mGameScene in (Lawn.GameScenes.Playing, Lawn.GameScenes.LevelIntro)
        if lawnapp.mBoard is not None and gamescene_ok and lawnapp.GetDialog(37) is None:
            if self.loaded:
                # run all scripts
                for scriptObj in self.scriptList:
                    scriptObj.Run()
            else:
                # load all scripts
                for scriptObj in self.scriptList:
                    scriptObj.Start()
                    Sexy.Debug.Log(f'load script func: {scriptObj.scriptGenFunc}')
                self.loaded = True
        self.prev_scene = lawnapp.mGameScene
