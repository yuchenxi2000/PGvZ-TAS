"""
植物娘大战僵尸键控框架 PGvZ-TAS
by yuchenxi2000
v1.0.0 2026.05.06
"""
from .card import Card, Shovel
from .cob_manager import CobManager, GetCobRecoverTime
from .global_var import gvar
from .script import ScriptManager, ScriptRunMode, ScriptType, ScriptObj, ScriptConf
from .smart import AutoCollect
from .time_operation import Delay, Prejudge, Until
from .util import *
import LawnMod

pgvz_version = (1, 0, 0)

script_manager = ScriptManager()
# 默认注册一个自动收集（可收集盆栽），要关掉就调用auto_collector.Off()方法
auto_collector = script_manager.Register(AutoCollect, runmode=ScriptRunMode.FOREVER)

# 键控钩子。每帧运行一次
@LawnMod.MonoModUtils.As(Lawn.LawnApp.UpdateFrames)
def LawnApp__UpdateFrames(orig, lawnapp: Lawn.LawnApp):
    # 设置全局变量
    gvar.Set(lawnapp)
    # 管理脚本
    script_manager.Manage()
    orig(lawnapp)

LawnMod.MonoModUtils.On.Lawn.LawnApp.UpdateFrames += LawnApp__UpdateFrames  # type: ignore

__all__ = [
    "Card", "Shovel",
    "CobManager", "GetCobRecoverTime",
    "gvar",
    "ScriptManager", "ScriptRunMode", "ScriptType", "ScriptObj", "ScriptConf",
    "Delay", "Prejudge", "Until",
    "PixelToGrid", "GridToPixel", "MouseDragGrid", "SeedTypeNone", "SetPlantOnBoard", 
    "IterAliveZombies", "IterAlivePlants", "IterAliveCoins", "IterAliveGridItems",
    "pgvz_version", "script_manager", "auto_collector",
]
