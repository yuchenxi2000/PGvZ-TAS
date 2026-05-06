"""
更好的作弊
不需要的功能直接注释掉代码或者删除即可
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import Lawn
import LawnMod
import Sexy
import Sexy.TodLib
from pyvz import *

# 免费用卡
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.GetCost)
def hook_plant_getcost(orig, plantType: Lawn.SeedType, plantImitaterType: Lawn.SeedType):
    return 0

# 满阳光+无冷却
def CheatSunMoney():
    gvar.gboard.mSunMoney = 9990  # 满阳光
    gvar.glawnapp.mEasyPlantingCheat = True  # 无冷却
script_manager.Register(CheatSunMoney)

# 随意种植
@LawnMod.MonoModUtils.HookTo(Lawn.Board.CanPlantAt)
def hook_board_canplantat(orig, board: Lawn.Board, gridX: int, gridY: int, seedtype: Lawn.SeedType, ismove: bool):
    return Lawn.PlantingReason.Ok

# 更好的自动收集，包括盆栽。PGvZ-TAS自带，只需引入pyvz模块。如果不需要这个功能，把下面一句取消注释。
# auto_collector.Off()

# 植物免疫啃食
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.Update)
def hook_plant_update(orig, plant: Lawn.Plant):
    plant.mPlantHealth = 2147483647
    orig(plant)

# 植物免疫小丑爆炸
@LawnMod.MonoModUtils.HookTo(Lawn.Board.KillAllPlantsInRadius)
def hook_board_KillAllPlantsInRadius(orig, board: Lawn.Board, theX: int, theY: int, theRadius: int):
    return

# 植物不会被毁灭菇炸掉
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.KillAllPlantsNearDoom)
def hook_plant_KillAllPlantsNearDoom(orig, plant: Lawn.Plant):
    return

# 植物免疫压扁
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.Squish)
def hook_plant_Squish(orig, plant: Lawn.Plant):
    if plant.NotOnGround():
        return
    if not plant.IsDisabled():
        if plant.mSeedType in [Lawn.SeedType.Cherrybomb, Lawn.SeedType.Jalapeno, Lawn.SeedType.Doomshroom, Lawn.SeedType.Iceshroom, Lawn.SeedType.PickledPepper]:
            plant.DoSpecial()
            return
        if plant.mSeedType == Lawn.SeedType.Potatomine and plant.mState != Lawn.PlantState.Notready:
            plant.DoSpecial()
            return

# 植物无法被蹦极偷走
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.BungeeStealTarget)
def hook_zombie_BungeeStealTarget(orig, zombie: Lawn.Zombie):
    zombie.PlayZombieReanim(Lawn.GlobalMembersReanimIds.ReanimTrackId_anim_grab, Sexy.TodLib.ReanimLoopType.PlayOnceAndHold, 20, 24.0)

# 玉米炮无冷却
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.UpdateCobCannon)
def hook_plant_UpdateCobCannon(orig, plant: Lawn.Plant):
    if plant.mState == Lawn.PlantState.CobcannonArming:
        plant.mStateCountdown = 0
    orig(plant)

# 天尸不得施法
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.UpdateZombieTalisman)
def hook_zombie_updatezombietalisman(orig, zombie: Lawn.Zombie):
    if zombie.mZombiePhase == Lawn.ZombiePhase.TalismanAttacking:
        zombie.mZombiePhase = Lawn.ZombiePhase.TalismanLeaving
    orig(zombie)

# 女忍者显形
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.UpdateNinja)
def hook_zombie_UpdateNinja(orig, zombie: Lawn.Zombie):
    orig(zombie)
    if zombie.mZombiePhase == Lawn.ZombiePhase.ZombieNormal:
        zombie.mZombiePhase = Lawn.ZombiePhase.NinjaShownByPlantern

# 隐形僵尸关卡僵尸显形。显形方法是偷偷把关卡ID换成其他的。这样不用写一大堆代码
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.Draw)
def hook_zombie_draw(orig, zombie: Lawn.Zombie, graphics: Sexy.Graphics):
    mApp = zombie.mApp
    level_is_invisighoul = (mApp.mGameMode == Lawn.GameMode.ChallengeInvisighoul)
    if level_is_invisighoul:
        mApp.mGameMode = Lawn.GameMode.ChallengeBobsledBonanza
    orig(zombie, graphics)
    if level_is_invisighoul:
        mApp.mGameMode = Lawn.GameMode.ChallengeInvisighoul

# 暴风雨夜移除天气特效，不再闪瞎眼
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.DrawStormNight)
def hook_challenge_drawstormnight(orig, challenge: Lawn.Challenge, graphics: Sexy.Graphics):
    pass
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.IsStormyNightPitchBlack)
def hook_challenge_IsStormyNightPitchBlack(orig, challenge: Lawn.Challenge):
    return False
