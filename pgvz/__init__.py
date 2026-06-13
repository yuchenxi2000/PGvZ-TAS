"""
植物娘大战僵尸键控框架 PGvZ-TAS
by yuchenxi2000
2026.06.13 PGvZ-TAS v1.5.4, PGvZ v1.1.0
"""
from .card import Card, Shovel, SelectCards, LetsRock
from .cob_manager import CobManager, GetCobRecoverTime
from .global_var import gvar
from .script import ScriptManager, ScriptRunMode, ScriptType, ScriptObj, ScriptConf
from .smart import AutoCollect
from .time_operation import Delay, Prejudge, Until, DelayA
from .util import *
from .set_zb import SetZombies
import LawnMod

script_manager = ScriptManager()
# 默认注册一个自动收集（可收集盆栽），要关掉就调用auto_collector.Off()方法
auto_collector = script_manager.Register(AutoCollect, runmode=ScriptRunMode.FOREVER)

# 这个钩子起到补充作用，为了在主界面、选卡界面等仍能运行/管理脚本
@LawnMod.MonoModUtils.HookTo(Lawn.LawnApp.UpdateFrames)
def LawnApp__UpdateFrames(orig, lawnapp: Lawn.LawnApp):
    if lawnapp.mBoard is None:
        # 管理脚本
        script_manager.Manage()
    orig(lawnapp)

# 游戏逻辑钩子，只有这个存在时，才支持开倍速
# 上面的钩子在倍速时无法保证每个游戏逻辑处理帧运行一次
@LawnMod.MonoModUtils.HookTo(Lawn.Board.UpdateGame)
def Board__UpdateGame(orig, board: Lawn.Board):
    # 管理脚本
    script_manager.Manage()
    orig(board)

__all__ = [
    "Card", "Shovel", "SelectCards", "LetsRock",
    "CobManager", "GetCobRecoverTime",
    "gvar",
    "ScriptManager", "ScriptRunMode", "ScriptType", "ScriptObj", "ScriptConf",
    "Delay", "Prejudge", "Until", "DelayA",
    "GetLawnApp", "GetBoard",
    "PixelToGrid", "GridToPixel", "MouseDragGrid", "PixelToGridRaw",
    "SeedTypeNone", "PottedPlantNeedNone", "SetPlantOnBoard", "SurvivalBackupGame",
    "IterAliveZombies", "IterAlivePlants", "IterAliveCoins", "IterAliveGridItems",
    "script_manager", "auto_collector",
    "SetZombies",
]
