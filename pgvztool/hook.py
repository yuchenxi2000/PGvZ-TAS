"""
PGvZTool 钩子集中管理
所有 @HookTo 装饰的函数统一放在此文件中
"""
import Lawn
import LawnMod
import Sexy
import Sexy.TodLib
from pgvz import *
from pgvz.rng import rng_manip
from .cheat import cheat_option
from .placer import placer
from .tas import tas_manager
from .keybinds import KeybindHandler

# 关闭assertion，不然启动带命令行的游戏（Lawn.Console.exe）在输出过多时会卡死
@LawnMod.MonoModUtils.HookTo(Sexy.Debug.ASSERT)
def Debug__ASSERT(orig, value: bool):
    return

# 后台运行。如果直接设置Sexy.Main.RunWhenLocked，切换用户时会失效，因此得挂钩子
@LawnMod.MonoModUtils.HookTo(Lawn.LawnApp.LostFocus)
def LawnApp__LostFocus(orig, lawnapp: Lawn.LawnApp):
    Sexy.Main.RunWhenLocked = cheat_option.runBackground
    orig(lawnapp)

# 免费用卡
# 第二个hook为了让无尽里紫卡阳光仍为0
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.GetCost)
def Plant__GetCost(orig, plantType: Lawn.SeedType, plantImitaterType: Lawn.SeedType):
    if cheat_option.freePlant:
        return 0
    else:
        return orig(plantType, plantImitaterType)
@LawnMod.MonoModUtils.HookTo(Lawn.Board.GetCurrentPlantCost)
def Board__GetCurrentPlantCost(orig, board: Lawn.Board, plantType: Lawn.SeedType, plantImitaterType: Lawn.SeedType):
    if cheat_option.freePlant:
        return 0
    else:
        return orig(board, plantType, plantImitaterType)

# 房主无敌
@LawnMod.MonoModUtils.HookTo(Lawn.Board.ZombiesWon)
def Board__ZombiesWon(orig, board: Lawn.Board, zombie: Lawn.Zombie):
    if cheat_option.wontLose:
        if zombie is not None:
            zombie.DieNoLoot(False)
    else:
        orig(board, zombie)

# 随意种植
@LawnMod.MonoModUtils.HookTo(Lawn.Board.CanPlantAt)
def Board__CanPlantAt(orig, board: Lawn.Board, gridX: int, gridY: int, seedtype: Lawn.SeedType, ismove: bool):
    if cheat_option.plantAnyWhere:
        return Lawn.PlantingReason.Ok
    else:
        return orig(board, gridX, gridY, seedtype, ismove)

# 路灯花变身概率锁定为100%
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.PlantInitialize)
def Plant__PlantInitialize(orig, plant: Lawn.Plant, gridX: int, gridY: int, seedType: Lawn.SeedType, imitaterType: Lawn.SeedType):
    if seedType != Lawn.SeedType.Plantern or not cheat_option.planternAlwaysTransform:
        return orig(plant, gridX, gridY, seedType, imitaterType)

    had_override = 100 in rng_manip.forced_int_by_ceiling
    old_value = rng_manip.forced_int_by_ceiling.get(100)
    rng_manip.forced_int_by_ceiling[100] = 0
    try:
        return orig(plant, gridX, gridY, seedType, imitaterType)
    finally:
        if had_override:
            rng_manip.forced_int_by_ceiling[100] = old_value
        else:
            del rng_manip.forced_int_by_ceiling[100]

@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.CanPlantAt)
def Challenge__CanPlantAt(orig, challenge: Lawn.Challenge, gridX: int, gridY: int, seedtype: Lawn.SeedType):
    if cheat_option.plantAnyWhere:
        return Lawn.PlantingReason.Ok
    else:
        return orig(challenge, gridX, gridY, seedtype)

# 更好的自动收集，包括盆栽。PGvZ-TAS自带，只需引入pgvz模块。关闭只需把下面一句取消注释。
# auto_collector.Off()

# 传送带无冷却
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.UpdateConveyorBelt)
def Challenge__UpdateConveyorBelt(orig, challenge: Lawn.Challenge):
    if cheat_option.conveyorNoCooling:
        challenge.mConveyorBeltCounter = 0
        orig(challenge)
        seedbank = challenge.mBoard.mSeedBank
        for i in range(seedbank.mNumPackets):
            seedbank.mSeedPackets[i].mOffsetY = 0
    else:
        orig(challenge)

# 启用手套
@LawnMod.MonoModUtils.HookTo(Lawn.Board.HasGlove)
def Board__HasGlove(orig, board: Lawn.Board):
    if cheat_option.enableGlove:
        # 我是僵尸模式用手套会崩溃
        return board.mApp.mGameMode not in (Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom, Lawn.GameMode.Upsell, Lawn.GameMode.Intro) and not board.mApp.IsIZombieLevel()
    else:
        return orig(board)

# 手套无冷却
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.MovePlant)
def Challenge__MovePlant(orig, challenge: Lawn.Challenge, plant: Lawn.Plant, gridX: int, gridY: int):
    orig(challenge, plant, gridX, gridY)
    if cheat_option.gloveNoCooling:
        challenge.mGloveCounter = 0

# 僵尸停滞不前
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.UpdateZombieWalking)
def Zombie__UpdateZombieWalking(orig, zombie: Lawn.Zombie):
    if not cheat_option.zombieStop:
        orig(zombie)

# 暂停出怪
@LawnMod.MonoModUtils.HookTo(Lawn.Board.UpdateZombieSpawning)
def Board__UpdateZombieSpawning(orig, board: Lawn.Board):
    if not cheat_option.stopSpawning:
        orig(board)

# 僵尸无敌
# 魅惑不算僵尸死了所以不管
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.TakeDamage)
def Zombie__TakeDamage(orig, zombie: Lawn.Zombie, theDamage: int, theDamageFlags: int):
    if not cheat_option.zombieNoDie:
        orig(zombie, theDamage, theDamageFlags)
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.ApplyBurn)
def Zombie__ApplyBurn(orig, zombie: Lawn.Zombie):
    if not cheat_option.zombieNoDie:
        orig(zombie)
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.DieWithLoot)
def Zombie__DieWithLoot(orig, zombie: Lawn.Zombie):
    if cheat_option.zombieNoDie:
        if zombie.draggedByTangleKelp:
            zombie.draggedByTangleKelp = False
            zombie.mZombieHeight = Lawn.ZombieHeight.InToPool
    else:
        orig(zombie)

# 植物免疫啃食
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.EatPlant)
def Zombie__EatPlant(orig, zombie: Lawn.Zombie, plant: Lawn.Plant):
    Lawn.GameConstants.TICKS_BETWEEN_EATS = 0 if cheat_option.plantNoDie else 4
    orig(zombie, plant)
    Lawn.GameConstants.TICKS_BETWEEN_EATS = 4

# 植物免疫小丑爆炸
@LawnMod.MonoModUtils.HookTo(Lawn.Board.KillAllPlantsInRadius)
def Board__KillAllPlantsInRadius(orig, board: Lawn.Board, theX: int, theY: int, theRadius: int):
    if not cheat_option.plantNoDie:
        orig(board, theX, theY, theRadius)

# 植物不会被毁灭菇炸掉
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.KillAllPlantsNearDoom)
def Plant__KillAllPlantsNearDoom(orig, plant: Lawn.Plant):
    if not cheat_option.plantNoDie:
        orig(plant)

# 植物免疫压扁
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.Squish)
def Plant__Squish(orig, plant: Lawn.Plant):
    if cheat_option.plantNoDie:
        if plant.NotOnGround():
            return
        if not plant.IsDisabled():
            if plant.mSeedType in (Lawn.SeedType.Cherrybomb, Lawn.SeedType.Jalapeno, Lawn.SeedType.Doomshroom, Lawn.SeedType.Iceshroom, Lawn.SeedType.PickledPepper):
                plant.DoSpecial()
                return
            if plant.mSeedType == Lawn.SeedType.Potatomine and plant.mState != Lawn.PlantState.Notready:
                plant.DoSpecial()
                return
    else:
        orig(plant)

# 植物无法被蹦极偷走
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.BungeeStealTarget)
def Zombie__BungeeStealTarget(orig, zombie: Lawn.Zombie):
    if cheat_option.plantNoDie:
        zombie.PlayZombieReanim(Lawn.GlobalMembersReanimIds.ReanimTrackId_anim_grab, Sexy.TodLib.ReanimLoopType.PlayOnceAndHold, 20, 24.0)
    else:
        orig(zombie)

# 植物不能被墓碑顶掉
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.GraveDangerSpawnGraveAt)
def Challenge__GraveDangerSpawnGraveAt(orig, challenge: Lawn.Challenge, x: int, y: int):
    if cheat_option.plantNoDie:
        challenge.mBoard.mEnableGraveStones = True
        grave_stone = challenge.mBoard.AddAGraveStone(x, y)
        if grave_stone is not None:
            grave_stone.AddGraveStoneParticles()
    else:
        orig(challenge, x, y)

# 钢地刺不死
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.SpikeRockTakeDamage)
def Plant__SpikeRockTakeDamage(orig, plant: Lawn.Plant):
    if cheat_option.plantNoDie:
        plant.mApp.ReanimationGet(plant.mBodyReanimID)
        plant.SpikeweedAttack()
    else:
        orig(plant)

# 1. 地刺不死
# 2. 全屏忧郁菇
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.DoRowAreaDamage)
def Plant__DoRowAreaDamage(orig, plant: Lawn.Plant, theDamage: int, theDamageFlags: int):
    if plant.mSeedType == Lawn.SeedType.Spikeweed and cheat_option.plantNoDie:
        damageRangeFlags = plant.GetDamageRangeFlags(Lawn.PlantWeapon.Primary)
        plantAttackRect = plant.GetPlantAttackRect(Lawn.PlantWeapon.Primary)
        for i in range(plant.mBoard.mZombies.Count):
            zombie = plant.mBoard.mZombies[i]
            if zombie.mDead:
                continue
            num = zombie.mRow - plant.mRow
            if zombie.mZombieType == Lawn.ZombieType.Boss:
                num = 0
            if num != 0:
                continue
            if zombie.mOnHighGround != plant.IsOnHighGround() or not zombie.EffectedByDamage(damageRangeFlags):
                continue
            zombieRect = zombie.GetZombieRect()
            if Lawn.GameConstants.GetRectOverlap(plantAttackRect, zombieRect) <= 0:
                continue
            theDamage2 = theDamage
            if zombie.mZombieType in (Lawn.ZombieType.Zamboni, Lawn.ZombieType.Catapult) and Sexy.TodLib.TodCommon.TestBit(theDamageFlags, 5):
                theDamage2 = 1800
            zombie.TakeDamage(theDamage2, theDamageFlags)
            plant.mApp.PlayFoley(Sexy.TodLib.FoleyType.Splat)
        return
    elif plant.mSeedType == Lawn.SeedType.Gloomshroom and cheat_option.fullAreaGloomshroom:
        for i in range(plant.mBoard.mZombies.Count):
            zombie = plant.mBoard.mZombies[i]
            if zombie.mDead:
                continue
            zombie.TakeDamage(theDamage, theDamageFlags)
            plant.mApp.PlayFoley(Sexy.TodLib.FoleyType.Splat)
        return
    orig(plant, theDamage, theDamageFlags)

# 全屏忧郁菇
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.FindTargetZombie)
def Plant__FindTargetZombie(orig, plant: Lawn.Plant, theRow: int, thePlantWeapon: Lawn.PlantWeapon):
    if plant.mSeedType == Lawn.SeedType.Gloomshroom and cheat_option.fullAreaGloomshroom:
        damageRangeFlags = plant.GetDamageRangeFlags(thePlantWeapon)
        for i in range(plant.mBoard.mZombies.Count):
            theZombieItem = plant.mBoard.mZombies[i]
            if theZombieItem.mDead:
                continue
            if not theZombieItem.EffectedByDamage(damageRangeFlags):
                continue
            return theZombieItem
        return None
    return orig(plant, theRow, thePlantWeapon)

# 玉米炮无冷却, 僵尸无敌修改大嘴花，大嘴花无冷却，土豆雷无冷却
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.Update)
def Plant__Update(orig, plant: Lawn.Plant):
    if plant.mState == Lawn.PlantState.CobcannonArming and cheat_option.cobNoCooling:
        plant.mStateCountdown = 0
    elif plant.mState == Lawn.PlantState.ChomperBitingGotOne and cheat_option.zombieNoDie:
        plant.mState = Lawn.PlantState.ChomperBitingMissed
    elif plant.mState == Lawn.PlantState.ChomperDigesting and cheat_option.chomperNoCooling:
        plant.mStateCountdown = 0
    elif plant.mSeedType == Lawn.SeedType.Potatomine and cheat_option.potatoNoCooling:
        plant.mStateCountdown = 0
    orig(plant)

# 天尸不得施法
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.UpdateZombieTalisman)
def Zombie__UpdateZombieTalisman(orig, zombie: Lawn.Zombie):
    if zombie.mZombiePhase == Lawn.ZombiePhase.TalismanAttacking and cheat_option.disableTalisman:
        zombie.mZombiePhase = Lawn.ZombiePhase.TalismanLeaving
    orig(zombie)

# 女忍者显形
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.UpdateNinja)
def Zombie_UpdateNinja(orig, zombie: Lawn.Zombie):
    orig(zombie)
    if zombie.mZombiePhase == Lawn.ZombiePhase.ZombieNormal and cheat_option.disableNinja:
        zombie.mZombiePhase = Lawn.ZombiePhase.NinjaShownByPlantern

# 隐形僵尸关卡僵尸显形。显形方法是偷偷把关卡ID换成其他的。这样不用写一大堆代码
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.Draw)
def Zombie__Draw(orig, zombie: Lawn.Zombie, graphics: Sexy.Graphics):
    mApp = zombie.mApp
    level_is_invisighoul = (mApp.mGameMode == Lawn.GameMode.ChallengeInvisighoul)
    if level_is_invisighoul and cheat_option.visibleGhoul:
        mApp.mGameMode = Lawn.GameMode.ChallengeBobsledBonanza
    orig(zombie, graphics)
    if level_is_invisighoul:
        mApp.mGameMode = Lawn.GameMode.ChallengeInvisighoul

# 暴风雨夜移除天气特效，不再闪瞎眼
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.DrawStormNight)
def Challenge__DrawStormNight(orig, challenge: Lawn.Challenge, graphics: Sexy.Graphics):
    if not cheat_option.noThunder:
        orig(challenge, graphics)
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.IsStormyNightPitchBlack)
def Challenge__IsStormyNightPitchBlack(orig, challenge: Lawn.Challenge):
    if cheat_option.noThunder:
        return False
    else:
        return orig(challenge)

# 去除右侧遮挡
@LawnMod.MonoModUtils.HookTo(Lawn.Board.DrawCoverLayer)
def Board__DrawCoverLayer(orig, board: Lawn.Board, graphics: Sexy.Graphics, theRow: int):
    if not cheat_option.noCover:
        orig(board, graphics, theRow)

def NewGridItemZenTool(plant: Lawn.Plant):
    gridItem = Lawn.GridItem.GetNewGridItem()
    gridItem.mGridItemType = Lawn.GridItemType.ZenTool
    gridItem.mRenderOrder = 800000
    gridItem.mGridX = plant.mPlantCol
    gridItem.mGridY = plant.mRow
    gridItem.mPosX = plant.mX + 40
    gridItem.mPosY = plant.mY + 40
    return gridItem

# BUG FIX: 修复禅境花园里的金盏花没有应用盆栽存档中花色的问题
@LawnMod.MonoModUtils.HookTo(Lawn.ZenGarden.PlacePottedPlant)
def ZenGarden__PlacePottedPlant(orig, zenGarden: Lawn.ZenGarden, pottedPlantIndex: int):
    plant = orig(zenGarden, pottedPlantIndex)
    if plant is None or plant.mSeedType != Lawn.SeedType.Marigold:
        return plant

    pottedPlant = zenGarden.PottedPlantFromIndex(pottedPlantIndex)
    variation = pottedPlant.mDrawVariation
    variationValue = int(variation)
    if int(Lawn.DrawVariation.MarigoldWhite) <= variationValue <= int(Lawn.DrawVariation.MarigoldLightGreen):
        reanimation = zenGarden.mApp.ReanimationTryToGet(plant.mBodyReanimID)
        if reanimation is not None:
            zenGarden.mApp.mReanimatorCache.UpdateReanimationforVariation(reanimation, variation)
    return plant

# 全屏留声机、花肥、杀虫剂
@LawnMod.MonoModUtils.HookTo(Lawn.ZenGarden.MouseDownWithFeedingTool)
def ZenGarden__MouseDownWithFeedingTool(orig, zenGarden: Lawn.ZenGarden, x: int, y: int, theCursorType: Lawn.CursorType, isTouch: bool):
    if cheat_option.diamondZenTools and theCursorType in (Lawn.CursorType.Fertilizer, Lawn.CursorType.BugSpray, Lawn.CursorType.Phonograph):
        for i in range(zenGarden.mBoard.mPlants.Count):
            plant = zenGarden.mBoard.mPlants[i]
            if not plant.mDead and zenGarden.mBoard.GetTopPlantAt(plant.mPlantCol, plant.mRow, Lawn.TopPlant.ZenToolOrder) == plant:
                thePottedPlant = zenGarden.PottedPlantFromIndex(plant.mPottedPlantIndex)
                potPlantNeed = zenGarden.GetPlantsNeed(thePottedPlant)
                if potPlantNeed == Lawn.PottedPlantNeed.Fertilizer and theCursorType == Lawn.CursorType.Fertilizer and zenGarden.mApp.mPlayerInfo.mPurchases[14] > 1000:
                    newGridItem = NewGridItemZenTool(plant)
                    reanimation8 = zenGarden.mApp.AddReanimation(plant.mX, plant.mY, 0, Sexy.TodLib.ReanimationType.ZengardenFertilizer)
                    reanimation8.mLoopType = Sexy.TodLib.ReanimLoopType.PlayOnceAndHold
                    newGridItem.mGridItemReanimID = zenGarden.mApp.ReanimationGetID(reanimation8)
                    newGridItem.mGridItemState = Lawn.GridItemState.ZenToolFertilizer
                    zenGarden.mBoard.mGridItems.Add(newGridItem)
                    zenGarden.mApp.mPlayerInfo.mPurchases[14] -= 1
                elif potPlantNeed == Lawn.PottedPlantNeed.Bugspray and theCursorType == Lawn.CursorType.BugSpray and zenGarden.mApp.mPlayerInfo.mPurchases[15] > 1000:
                    newGridItem = NewGridItemZenTool(plant)
                    reanimation7 = zenGarden.mApp.AddReanimation(plant.mX + 54, plant.mY, 0, Sexy.TodLib.ReanimationType.ZengardenBugspray)
                    reanimation7.mLoopType = Sexy.TodLib.ReanimLoopType.PlayOnceAndHold
                    newGridItem.mGridItemReanimID = zenGarden.mApp.ReanimationGetID(reanimation7)
                    newGridItem.mGridItemState = Lawn.GridItemState.ZenToolBugSpray
                    zenGarden.mBoard.mGridItems.Add(newGridItem)
                    zenGarden.mApp.mPlayerInfo.mPurchases[15] -= 1
                elif potPlantNeed == Lawn.PottedPlantNeed.Phonograph and theCursorType == Lawn.CursorType.Phonograph:
                    newGridItem = NewGridItemZenTool(plant)
                    reanimation6 = zenGarden.mApp.AddReanimation(plant.mX + 20, plant.mY + 34, 0, Sexy.TodLib.ReanimationType.ZengardenPhonograph)
                    reanimation6.mAnimRate = 20.0
                    reanimation6.mLoopType = Sexy.TodLib.ReanimLoopType.Loop
                    newGridItem.mGridItemReanimID = zenGarden.mApp.ReanimationGetID(reanimation6)
                    newGridItem.mGridItemState = Lawn.GridItemState.ZenToolPhonograph
                    zenGarden.mBoard.mGridItems.Add(newGridItem)
        if theCursorType == Lawn.CursorType.Fertilizer:
            zenGarden.mApp.PlayFoley(Sexy.TodLib.FoleyType.Fertilizer)
        elif theCursorType == Lawn.CursorType.BugSpray:
            zenGarden.mApp.PlayFoley(Sexy.TodLib.FoleyType.Bugspray)
        elif theCursorType == Lawn.CursorType.Phonograph:
            zenGarden.mApp.PlayFoley(Sexy.TodLib.FoleyType.Phonograph)
        zenGarden.mBoard.ClearCursor()
    else:
        orig(zenGarden, x, y, theCursorType, isTouch)

# 移除迷雾
@LawnMod.MonoModUtils.HookTo(Lawn.Board.DrawFog)
def Board__DrawFog(orig, board: Lawn.Board, graphics: Sexy.Graphics):
    if not cheat_option.noFog:
        orig(board, graphics)

# 罐子透视
@LawnMod.MonoModUtils.HookTo(Lawn.GridItem.UpdateScaryPot)
def GridItem__UpdateScaryPot(orig, griditem: Lawn.GridItem):
    orig(griditem)
    if cheat_option.transScaryPot:
        griditem.mTransparentCounter = 50

# 三线射手不浪费子弹

# 设置子弹偏移量，否则两个叠一起看不清
def ThreePeaterAddProjectile(plant: Lawn.Plant, theRow: int, offset: int):
    projectileType = Lawn.ProjectileType.Pea
    plant.mApp.PlayFoley(Sexy.TodLib.FoleyType.Throw)
    num2 = plant.mY + 10
    num = plant.mX + 45
    if plant.mBoard.GetFlowerPotAt(plant.mPlantCol, plant.mRow) is not None:
        num2 -= 5
    num2 += offset
    projectile = plant.mBoard.AddProjectile(num, num2, plant.mRenderOrder + -1, theRow, projectileType)
    projectile.mDamageRangeFlags = plant.GetDamageRangeFlags(Lawn.PlantWeapon.Primary)
    projectile.mFromPlant = plant.mSeedType

# 不论上下行有无僵尸，都播放射击动画。否则无法射击
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.LaunchThreepeater)
def Plant__LaunchThreepeater(orig, plant: Lawn.Plant):
    if cheat_option.featureThreePeater:
        theRow = plant.mRow - 1
        theRow2 = plant.mRow + 1
        flag = False
        if plant.FindTargetZombie(plant.mRow, Lawn.PlantWeapon.Primary) is not None:
            flag = True
        elif plant.mBoard.RowCanHaveZombies(theRow) and plant.FindTargetZombie(theRow, Lawn.PlantWeapon.Primary) is not None:
            flag = True
        elif plant.mBoard.RowCanHaveZombies(theRow2) and plant.FindTargetZombie(theRow2, Lawn.PlantWeapon.Primary) is not None:
            flag = True
        if flag:
            reanimation = plant.mApp.ReanimationGet(plant.mHeadReanimID)
            reanimation2 = plant.mApp.ReanimationGet(plant.mHeadReanimID2)
            reanimation3 = plant.mApp.ReanimationGet(plant.mHeadReanimID3)
            # if plant.mBoard.RowCanHaveZombies(theRow2):
            reanimation.StartBlend(10)
            reanimation.mLoopType = Sexy.TodLib.ReanimLoopType.PlayOnceAndHold
            reanimation.mAnimRate = 20.0
            reanimation.SetFramesForLayer(Lawn.GlobalMembersReanimIds.ReanimTrackId_anim_shooting1)
            reanimation2.StartBlend(10)
            reanimation2.mLoopType = Sexy.TodLib.ReanimLoopType.PlayOnceAndHold
            reanimation2.mAnimRate = 20.0
            reanimation2.SetFramesForLayer(Lawn.GlobalMembersReanimIds.ReanimTrackId_anim_shooting2)
            # if plant.mBoard.RowCanHaveZombies(theRow):
            reanimation3.StartBlend(10)
            reanimation3.mLoopType = Sexy.TodLib.ReanimLoopType.PlayOnceAndHold
            reanimation3.mAnimRate = 20.0
            reanimation3.SetFramesForLayer(Lawn.GlobalMembersReanimIds.ReanimTrackId_anim_shooting3)
            plant.mShootingCounter = 35
    else:
        orig(plant)

# 1. 三线射手加强：如果上下行不能出僵尸，子弹设置到本行
# 2. 玉米锁黄油
# 3. 机枪射手8颗豌豆
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.UpdateShooting)
def Plant__UpdateShooting(orig, plant: Lawn.Plant):
    if plant.mSeedType == Lawn.SeedType.Threepeater and cheat_option.featureThreePeater:
        if plant.mShootingCounter - 1 == 1:
            theRow = plant.mRow - 1
            theRow2 = plant.mRow + 1
            aLevelRow = 6 if plant.mBoard.StageHas6Rows() else 5
            reanimation = plant.mApp.ReanimationTryToGet(plant.mHeadReanimID)
            reanimation2 = plant.mApp.ReanimationTryToGet(plant.mHeadReanimID2)
            reanimation3 = plant.mApp.ReanimationTryToGet(plant.mHeadReanimID3)
            if reanimation.mLoopType == Sexy.TodLib.ReanimLoopType.PlayOnceAndHold:
                if theRow2 < aLevelRow:
                    plant.Fire(None, theRow2, Lawn.PlantWeapon.Primary)  # type: ignore
                else:
                    ThreePeaterAddProjectile(plant, plant.mRow, 20)
            if reanimation2.mLoopType == Sexy.TodLib.ReanimLoopType.PlayOnceAndHold:
                plant.Fire(None, plant.mRow, Lawn.PlantWeapon.Primary)  # type: ignore
            if reanimation3.mLoopType == Sexy.TodLib.ReanimLoopType.PlayOnceAndHold:
                if theRow >= 0:
                    plant.Fire(None, theRow, Lawn.PlantWeapon.Primary)  # type: ignore
                else:
                    ThreePeaterAddProjectile(plant, plant.mRow, -20)
            plant.mShootingCounter -= 1
            return
    elif plant.mSeedType == Lawn.SeedType.Kernelpult and cheat_option.butterPult:
        plant.mState = Lawn.PlantState.KernelpultButter
    elif plant.mSeedType == Lawn.SeedType.Gatlingpea and cheat_option.doubleGatlingpea:
        if plant.mShootingCounter - 1 in (18, 26, 35, 43, 51, 60, 68, 76):
            plant.Fire(None, plant.mRow, Lawn.PlantWeapon.Primary)  # type: ignore
            plant.mShootingCounter -= 1
            return
    orig(plant)

# 显示植物/僵尸血量

# 潜水僵尸入水时的血条 Y 轴补偿；正数向下。
# 入水动画的可视位置不会写回 GetZombieRect，需要在游戏内调整此值。
SNORKEL_IN_POOL_HP_OFFSET_Y = 90
# 潜水僵尸在水中啃食时会播放上浮动画，但碰撞箱不会跟随动画。
SNORKEL_EATING_IN_POOL_HP_OFFSET_Y = 70
# 海豚僵尸在水中骑行
DOLPHIN_RIDING_HP_OFFSET_Y = 40
# 海豚僵尸在水中行走
DOLPHIN_WALKING_IN_POOL_HP_OFFSET_Y = 60

def DrawPlantHp(plant: Lawn.Plant, g: Sexy.Graphics, marginX: int, offsetY: int, color1, color2):
    if plant.mPlantHealth < plant.mPlantMaxHealth:
        # 一格80x80，画60x5
        numGrid = 2 if plant.mSeedType == Lawn.SeedType.Cobcannon else 1
        totalWidth = 80 * numGrid - 2 * marginX
        x = plant.mX + marginX
        y = plant.mY + offsetY
        hpWidth = totalWidth * plant.mPlantHealth / plant.mPlantMaxHealth
        g.SetColor(color2)
        g.FillRect(x, y, totalWidth, 5)
        g.SetColor(color1)
        g.FillRect(x, y, int(hpWidth), 5)

def DrawPlantHpAll(board: Lawn.Board, g: Sexy.Graphics):
    g.SetColorizeImages(True)
    color1 = Sexy.SexyColor(255, 153, 51, 255).Color  # 橙色
    color2 = Sexy.SexyColor(204, 0, 0, 255).Color  # 深红
    color3 = Sexy.SexyColor(102, 204, 0, 255).Color  # 绿色
    color4 = Sexy.SexyColor(0, 153, 153, 255).Color  # 青色
    NRow = 6 if board.StageHas6Rows() else 5
    NCol = 9
    for gridX in range(NCol):
        for gridY in range(NRow):
            plant = board.GetTopPlantAt(gridX, gridY, Lawn.TopPlant.EatingOrder)
            if plant is not None:
                DrawPlantHp(plant, g, 10, 60, color1, color2)
                plant2 = board.GetTopPlantAt(gridX, gridY, Lawn.TopPlant.CatapultOrder)
                if plant2 is not None and plant is not plant2:
                    DrawPlantHp(plant2, g, 10, 50, color3, color4)
    g.SetColorizeImages(False)

def DrawZombieHp(zombie: Lawn.Zombie, g: Sexy.Graphics, marginX: int, offsetY: int, color1, color2, color3, color4):
    rect = zombie.GetZombieRect()
    totalWidth = rect.mWidth
    x = rect.mX + marginX
    y = rect.mY + offsetY + 20
    # 对一些僵尸的特殊状态修正y轴偏移，使血条位置和视觉一致
    if zombie.mZombieType == Lawn.ZombieType.Snorkel:
        if zombie.mInPool and zombie.mIsEating:
            y += SNORKEL_EATING_IN_POOL_HP_OFFSET_Y
        elif zombie.mZombiePhase == Lawn.ZombiePhase.SnorkelIntoPool or zombie.mInPool:
            y += SNORKEL_IN_POOL_HP_OFFSET_Y
    elif zombie.mZombieType == Lawn.ZombieType.DolphinRider:
        if zombie.mZombiePhase == Lawn.ZombiePhase.DolphinWalkingInPool:
            y += DOLPHIN_WALKING_IN_POOL_HP_OFFSET_Y
        elif zombie.mZombiePhase == Lawn.ZombiePhase.DolphinRiding:
            y += DOLPHIN_RIDING_HP_OFFSET_Y
    # 两类血量
    hpWidth = 0
    hpWidth2 = 0
    plotHp1 = False
    plotHp2 = False
    # 画头盔/本体
    if zombie.mBodyHealth < zombie.mBodyMaxHealth:
        # 考虑血量临界值
        if zombie.CanLoseBodyParts():
            threshold = int(zombie.mBodyMaxHealth / 3)
        else:
            threshold = 0
        hpWidth = totalWidth * (zombie.mBodyHealth - threshold) / (zombie.mBodyMaxHealth - threshold)
        hpWidth = 0 if hpWidth < 0 else hpWidth
        if zombie.mHasHead:
            plotHp1 = True
    if zombie.mHasHelm and zombie.mHelmHealth < zombie.mHelmMaxHealth:
        if zombie.mZombieType == Lawn.ZombieType.Monk:  # 特殊处理武僧僵尸
            hpWidth2 = totalWidth * zombie.mHelmHealth / zombie.mHelmMaxHealth
            plotHp2 = True
        else:
            hpWidth = totalWidth * zombie.mHelmHealth / zombie.mHelmMaxHealth
            plotHp1 = True
    # 画飞行物
    if zombie.IsFlying() and zombie.mFlyingHealth < zombie.mFlyingMaxHealth:
        hpWidth = totalWidth * zombie.mFlyingHealth / zombie.mFlyingMaxHealth
        plotHp1 = True
    # 如果有铁门、梯子等画下面
    if zombie.mHasShield and zombie.mShieldHealth < zombie.mShieldMaxHealth:
        hpWidth2 = totalWidth * zombie.mShieldHealth / zombie.mShieldMaxHealth
        plotHp2 = True
    # 开始绘制
    if plotHp1:
        g.SetColor(color2)
        g.FillRect(x, y, totalWidth, 5)
        g.SetColor(color1)
        g.FillRect(x, y, int(hpWidth), 5)
    if plotHp2:
        g.SetColor(color4)
        g.FillRect(x, y + 10, totalWidth, 5)
        g.SetColor(color3)
        g.FillRect(x, y + 10, int(hpWidth2), 5)

selectZbList = [
    Lawn.ZombieType.Football,
    Lawn.ZombieType.Zamboni,
    Lawn.ZombieType.Gargantuar,
    Lawn.ZombieType.RedeyeGargantuar,
    Lawn.ZombieType.TallnutHead,
    Lawn.ZombieType.RobotTitan,
    Lawn.ZombieType.RedeyeRobotTitan,
    Lawn.ZombieType.Monk,
    Lawn.ZombieType.FootballPremium,
]

def DrawZombieHpAll(board: Lawn.Board, g: Sexy.Graphics):
    g.SetColorizeImages(True)
    color5 = Sexy.SexyColor(255, 51, 255, 255).Color
    color6 = Sexy.SexyColor(127, 0, 255, 255).Color
    color7 = Sexy.SexyColor(255, 0, 127, 255).Color
    color8 = Sexy.SexyColor(153, 0, 76, 255).Color
    for zombie in IterAliveZombies():
        # 只画精英怪
        if cheat_option.selectZombieHp and zombie.mZombieType not in selectZbList:
            continue
        DrawZombieHp(zombie, g, 0, 0, color5, color6, color7, color8)
    g.SetColorizeImages(False)

# 连续铲子
@LawnMod.MonoModUtils.HookTo(Lawn.Board.MouseDownWithTool)
def Board__MouseDownWithTool(orig, board: Lawn.Board, x: int, y: int, clickCnt: int, cursorType: Lawn.CursorType, posScaled: bool, isTouch: bool):
    orig(board, x, y, clickCnt, cursorType, posScaled, isTouch)
    if cheat_option.shovelNoReset and clickCnt >= 0 and cursorType == Lawn.CursorType.Shovel:
        board.mCursorObject.mCursorType = Lawn.CursorType.Shovel

# 轻松放置：点击处理
@LawnMod.MonoModUtils.HookTo(Lawn.Board.MouseDownInternal)
def Board__MouseDownInternal(orig, board: Lawn.Board, x: int, y: int, theClickCount: int, isTouch: bool):
    if placer.active and theClickCount < 0:
        placer.active = False
        return
    if placer._ep_rect.Contains(x, y) and placer.can_toggle(board):
        placer.toggle()
        return
    if placer.active and theClickCount >= 0:
        # 没有这一行手机会出问题
        x, y = board.mCamera.ScreenToBoardReplace(x, y)  # type: ignore
        if placer.try_place(board, x, y):
            return
    # TAS 按钮点击
    if tas_manager.can_use(board, cheat_option.tasEnabled) and theClickCount >= 0:
        if tas_manager.buttons is not None:
            for i, btn in enumerate(tas_manager.buttons):
                if btn.mX <= x < btn.mX + btn.mWidth and btn.mY <= y < btn.mY + btn.mHeight:  # 必须要这样，不能用IsButtonDown()以及IsMouseOver()，不然手机上按按钮无效
                    tas_manager.run_action(i)
                    return
    orig(board, x, y, theClickCount, isTouch)
    if placer.active and board.mCursorObject.mCursorType not in (Lawn.CursorType.Normal, Lawn.CursorType.Hammer):
        placer.active = False

# 为了让轻松放置UI有卡槽类似的行为，能够被RefreshSeedPacketFromCursor重置
# 能修复一个bug，轻松放置选定状态下，用快捷键选卡槽时轻松放置状态不会重置，导致点击场地后进行轻松放置而不是放置选定卡槽的植物
@LawnMod.MonoModUtils.HookTo(Lawn.Board.RefreshSeedPacketFromCursor)
def Board__RefreshSeedPacketFromCursor(orig, board: Lawn.Board):
    placer.active = False
    orig(board)

EASY_PLACE_UI_SCALE = 0.7

def DrawEasyPlaceUI(board: Lawn.Board, g: Sexy.Graphics):
    if board.mApp.mGameScene == Lawn.GameScenes.Playing and board.mApp.mGameMode not in (Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom, Lawn.GameMode.Upsell, Lawn.GameMode.Intro):
        shovel_rect = board.GetShovelButtonRect()
        btn_w = shovel_rect.mWidth
        btn_h = shovel_rect.mHeight
        btn_y = shovel_rect.mY
        num_ui = int(board.mShowShovel) + int(board.HasGlove())
        btn_x = shovel_rect.mX + 90 * num_ui

        g.DrawImage(Sexy.AtlasResources.IMAGE_SHOVELBANK_ZEN, btn_x, btn_y)
        if placer.active:
            g.SetColorizeImages(True)
            g.SetColor(Sexy.SexyColor(200, 200, 200).Color)
        taco_image = Sexy.AtlasResources.IMAGE_TACO
        taco_x = btn_x - 7
        taco_y = btn_y - 3
        Sexy.TodLib.TodCommon.TodDrawImageCenterScaledF(
            g,
            taco_image,
            float(taco_x),
            float(taco_y),
            EASY_PLACE_UI_SCALE,
            EASY_PLACE_UI_SCALE,
        )
        g.SetColorizeImages(False)

        placer._ep_rect = Sexy.TRect(btn_x, btn_y, btn_w, btn_h)

        # draw selected portal
        if placer.easyPlaceMode == 'portal' and placer.portal_placer.isSelected():
            g.SetColorizeImages(True)
            g.SetColor(Sexy.SexyColor(255, 0, 0).Color)
            g.DrawRect(placer.portal_placer.select_portal_rect)
            g.SetColorizeImages(False)

def DrawWaveInfo(board: Lawn.Board, g: Sexy.Graphics):
    # 在进度条下面画波数信息
    if board.HasProgressMeter():
        meterX = Sexy.Constants.UIProgressMeterPosition.X - Sexy.Constants.Board_Offset_AspectRatio_Correction
        meterY = Sexy.Constants.UIProgressMeterPosition.Y
        flagImage = Sexy.AtlasResources.IMAGE_FLAGMETER
        meterWidth = flagImage.GetCelWidth()
        meterHeight = flagImage.GetCelHeight()
        textX = meterX + meterWidth // 2
        textY = meterY + meterHeight
        g.SetColorizeImages(True)
        waveColor = Sexy.SexyColor(255, 255, 255)
        waveFont = Sexy.Resources.FONT_DWARVENTODCRAFT12
        waveText = f'Wave: {board.mCurrentWave}/{board.mNumWaves}'
        Sexy.TodLib.TodCommon.TodDrawString(g, waveText, textX, textY, waveFont, waveColor, Sexy.TodLib.DrawStringJustification.Center)
        cdStr = f'{board.mZombieCountDown}' if board.mZombieCountDown > 0 else '--'
        hugeStr = f'{board.mHugeWaveCountDown}' if board.mHugeWaveCountDown > 0 else '--'
        cdText = f'CD: {cdStr} | Huge: {hugeStr}'
        Sexy.TodLib.TodCommon.TodDrawString(g, cdText, textX, textY + 16, waveFont, waveColor, Sexy.TodLib.DrawStringJustification.Center)
        g.SetColorizeImages(False)

def DrawSquirrel(board: Lawn.Board, g: Sexy.Graphics):
    if board.mApp.mGameMode == Lawn.GameMode.ChallengeSquirrel:
        g.SetColorizeImages(True)
        for i in range(board.mGridItems.Count):
            gridItem = board.mGridItems[i]
            if not gridItem.mDead and gridItem.mGridItemType == Lawn.GridItemType.Squirrel:
                if gridItem.mGridItemState == Lawn.GridItemState.SquirrelZombie:
                    color = Sexy.SexyColor(255, 51, 255, 255).Color
                else:
                    color = Sexy.SexyColor(204, 0, 0, 255).Color  # 深红
                g.SetColor(color)
                mX, mY = GridToPixel(board, (gridItem.mGridX, gridItem.mGridY))
                margin = 10
                g.DrawRect(Sexy.TRect(mX + margin, mY + margin, 80 - 2 * margin, 100 - 2 * margin))
        g.SetColorizeImages(False)

# 垃圾桶
# 气死了，Board.HasTrashcan竟然被内联优化了，挂不上钩子！逼得写一堆代码
def _HasTrashcan(board: Lawn.Board):
    if cheat_option.enableTrashcan:
        gamemode = board.mApp.mGameMode
        return gamemode not in (Lawn.GameMode.Upsell, Lawn.GameMode.Intro, Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom)
    else:
        return board.mApp.IsRogueConveyorbeltLevel()

@LawnMod.MonoModUtils.HookTo(Lawn.Board.TrashcanHitTest)
def Board__TrashcanHitTest(orig, board: Lawn.Board, x: int, y: int):
    if _HasTrashcan(board):
        return Sexy.TRect(0, 70, 50, 80).Contains(x, y)
    return False

def DrawTrashcan(board: Lawn.Board, g: Sexy.Graphics):
    hasCamera = board.mCameraEnabled and board.mCamera is not None
    if hasCamera:
        board.mCamera.ApplyTransform(g)
    graphics = Sexy.Graphics.GetNew(g)
    graphics.SetScale(0.75)
    if board.IsPlantInCursor() and board.TrashcanHitTest(board.mCursorObject.mX, board.mCursorObject.mY):
        graphics.DrawImage(Sexy.AtlasResources.IMAGE_TRASHCAN, 0.0, 70.0 * Sexy.Constants.S)
        graphics.SetColorizeImages(True)
        graphics.SetColor(Sexy.SexyColor(255, 255, 255, 128, False).Color)
    elif board.IsPlantInCursor():
        flashingColor2 = Sexy.TodLib.TodCommon.GetFlashingColor(board.mMainCounter, 75)
        graphics.SetColorizeImages(True)
        graphics.SetColor(flashingColor2.Color)
    graphics.DrawImage(Sexy.AtlasResources.IMAGE_TRASHCAN, 0.0, 70.0 * Sexy.Constants.S)
    graphics.PrepareForReuse()
    if hasCamera:
        board.mCamera.ResetTransform(g)

keybind_handler = KeybindHandler(cheat_option, placer, tas_manager)

# 场地绘制统一钩子
@LawnMod.MonoModUtils.HookTo(Lawn.Board.Draw)
def Board__Draw(orig, board: Lawn.Board, g: Sexy.Graphics):
    keybind_handler.sync_desktop_ime_for_board(board)
    orig(board, g)
    # 进入Board坐标空间
    board.mCamera.ApplyTransform(g)
    if cheat_option.drawPlantHp:
        DrawPlantHpAll(board, g)
    if cheat_option.drawZombieHp:
        DrawZombieHpAll(board, g)
    if cheat_option.drawSquirrel:
        DrawSquirrel(board, g)
    board.mCamera.ResetTransform(g)
    # 屏幕坐标空间
    if placer.easyPlaceEnabled:
        DrawEasyPlaceUI(board, g)
    if cheat_option.showWaveInfo:
        DrawWaveInfo(board, g)
    if _HasTrashcan(board) and not board.mApp.IsRogueConveyorbeltLevel():
        DrawTrashcan(board, g)
    # TAS 按钮
    if tas_manager.can_use(board, cheat_option.tasEnabled):
        _DrawTasButtons(board, g)
        _DrawTasFrameCounter(board, g)

# TAS 按钮 — 右下角，懒初始化
def _DrawTasButtons(board: Lawn.Board, g: Sexy.Graphics):
    if tas_manager.buttons is None:
        btnH = Sexy.AtlasResources.IMAGE_BUTTON_LEFT.mHeight
        tas_manager.buttons = []  # type: ignore
        for i, label in enumerate(tas_manager.ACTION_LABELS):
            btn = Lawn.GameButton(9000 + i, board)
            btn.mDrawStoneButton = True
            btn.SetLabel(label)
            btn.Resize(0, 0, 70, btnH)
            tas_manager.buttons.append(btn)    # type: ignore
    # 右下角竖排，等距
    gap = 2
    btnH = tas_manager.buttons[0].mHeight   # type: ignore
    button_count = len(tas_manager.buttons)
    totalH = btnH * button_count + gap * (button_count - 1)
    baseX = board.mWidth - 200
    baseY = board.mHeight - totalH - 30
    for i, btn in enumerate(tas_manager.buttons):    # type: ignore
        btn.Resize(baseX, baseY + i * (btnH + gap), 70, btnH)
        btn.Update()
        btn.Draw(g)

def _DrawTasFrameCounter(board: Lawn.Board, g: Sexy.Graphics):
    """右下角显示 mMainCounter"""
    font = Sexy.Resources.FONT_DWARVENTODCRAFT12
    color = Sexy.SexyColor(255, 255, 255)
    text = f'Frame: {board.mMainCounter}'
    x = board.mWidth - 120
    y = board.mHeight - 30
    Sexy.TodLib.TodCommon.TodDrawString(g, text, x, y, font, color, Sexy.TodLib.DrawStringJustification.Right)

# BUG FIX: 猫尾草数量多时，发射子弹会崩游戏，因为Sexy.TodLib.TrailHolder.AllocTrailFromDef在需要扩容时直接返回null而不是触发扩容
@LawnMod.MonoModUtils.HookTo(Sexy.TodLib.TrailHolder.AllocTrailFromDef)
def TrailHolder__AllocTrailFromDef(orig, trailHolder: Sexy.TodLib.TrailHolder, theRenderOrder: int, theDefinition: Sexy.TodLib.TrailDefinition):
    if trailHolder.mTrails.Count == trailHolder.mTrails.Capacity:
        trailHolder.mTrails.Capacity *= 2
    return orig(trailHolder, theRenderOrder, theDefinition)

@LawnMod.MonoModUtils.HookTo(Sexy.WidgetManager.SetFocus)
def WidgetManager__SetFocus(orig, widget_manager: Sexy.WidgetManager, widget: Sexy.Widget):
    keybind_handler.set_focus(orig, widget_manager, widget)

@LawnMod.MonoModUtils.HookTo(Sexy.WidgetManager.GotFocus)
def WidgetManager__GotFocus(orig, widget_manager: Sexy.WidgetManager):
    keybind_handler.got_focus(orig, widget_manager)

@LawnMod.MonoModUtils.HookTo(Lawn.Board.KeyDown)
def Board__KeyDown(orig, board: Lawn.Board, theKey: Sexy.KeyCode):
    keybind_handler.key_down(orig, board, theKey)

@LawnMod.MonoModUtils.HookTo(Lawn.Board.KeyChar)
def Board__KeyChar(orig, board: Lawn.Board, theChar: Sexy.SexyChar):
    keybind_handler.key_char(orig, board, theChar)
