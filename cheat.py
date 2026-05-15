"""
更好的作弊
请配合cheat-gui.html使用
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import Lawn
import LawnMod
import Sexy
import Sexy.TodLib
from pgvz import *

class CheatOption:
    def __init__(self) -> None:
        self.wontLose = False
        self.freePlant = False
        self.plantAnyWhere = False
        self.plantNoDie = False
        self.cobNoCooling = False
        self.disableTalisman = False
        self.disableNinja = False
        self.visibleGhoul = False
        self.noThunder = False
        self.diamondPhonograph = False
        self.noFog = False

    def ConvertRange(self, row: int, col: int):
        NRow = 6 if gvar.gboard.StageHas6Rows() else 5
        if row < 0:
            row_range = range(NRow)
        elif row >= NRow:
            row_range = range(0, 0)
        else:
            row_range = range(row, row + 1)
        NCol = 9
        if col < 0:
            col_range = range(NCol)
        elif col >= 9:
            col_range = range(0, 0)
        else:
            col_range = range(col, col + 1)
        return row_range, col_range

    def PlantOnBoard(self, row: int, col: int, seedtype: Lawn.SeedType, isImitater: bool):
        if seedtype == Lawn.SeedType.Imitater and not isImitater:
            return
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                if isImitater:
                    gvar.gboard.AddPlant(col1, row1, Lawn.SeedType.Imitater, seedtype)
                else:
                    gvar.gboard.AddPlant(col1, row1, seedtype, SeedTypeNone)
    
    def RemovePlantOnBoard(self):
        for plant in IterAlivePlants():
            plant.Die()
    
    def ZombieOnBoard(self, row: int, col: int, zombietype: Lawn.ZombieType):
        row_range, col_range = self.ConvertRange(row, col)
        curwave = gvar.gboard.mCurrentWave
        for row1 in row_range:
            for col1 in col_range:
                xi = gvar.gboard.GridToPixelX(col1, row1)
                zombie = gvar.gboard.AddZombieInRow(zombietype, row1, curwave)
                zombie.mPosX = xi
                zombie.mX = xi
                if zombietype == Lawn.ZombieType.Bungee:
                    zombie.mTargetCol = col1
                    zombie.SetRow(row1)
                    zombie.mPosX = gvar.gboard.GridToPixelX(col1, row1)
                    zombie.mPosY = zombie.GetPosYBasedOnRow(row1)
                    zombie.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, row1, 7)
    
    def RemoveZombieOnBoard(self):
        for zombie in IterAliveZombies():
            zombie.DieNoLoot(False)
    
    def SetSeedPacket(self, idx: int, seedtype: Lawn.SeedType, isImitater: bool):
        seedpacket = gvar.gboard.mSeedBank.mSeedPackets[idx]
        if isImitater:
            seedpacket.SetPacketType(Lawn.SeedType.Imitater, seedtype)
        else:
            seedpacket.SetPacketType(seedtype, SeedTypeNone)
    
    def LadderOnBoard(self, row: int, col: int):
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                gvar.gboard.AddALadder(col1, row1)
    
    def GraveOnBoard(self, row: int, col: int):
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                grave_stone = gvar.gboard.AddAGraveStone(col1, row1)
                grave_stone.mGridItemCounter = 100  # 否则非存在墓碑场地不更新，墓碑无法钻出
    
    def RakeOnBoard(self, row: int, col: int):
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                newGridItem = Lawn.GridItem.GetNewGridItem()
                newGridItem.mGridItemType = Lawn.GridItemType.Rake
                newGridItem.mGridX = col1
                newGridItem.mGridY = row1
                newGridItem.mPosX = gvar.gboard.GridToPixelX(newGridItem.mGridX, newGridItem.mGridY)
                newGridItem.mPosY = gvar.gboard.GridToPixelY(newGridItem.mGridX, newGridItem.mGridY)
                newGridItem.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, newGridItem.mGridY, 9)
                gvar.gboard.mGridItems.Add(newGridItem)
                theReanimation = gvar.gboard.CreateRakeReanim(newGridItem.mPosX, newGridItem.mPosY, 0)
                newGridItem.mGridItemReanimID = gvar.gboard.mApp.ReanimationGetID(theReanimation)
                newGridItem.mGridItemState = Lawn.GridItemState.RakeAttracting
    
    def RemoveGridItemOnBoard(self, griditemtype: Lawn.GridItemType):
        if gvar.glawnapp.mGameMode in [Lawn.GameMode.ChallengeBeghouled, Lawn.GameMode.ChallengeBeghouledTwist]:
            challenge = gvar.gboard.mChallenge
            challenge.BeghouledClearCrater(40)
            challenge.BeghouledStartFalling(Lawn.ChallengeState.BeghouledFalling)
            return
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == griditemtype:
                griditem.GridItemDie()
    
    def OpenScaryPotterOnBoard(self):
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == Lawn.GridItemType.ScaryPot:
                gvar.gboard.mChallenge.ScaryPotterOpenPot(griditem)

    def AddLawnMower(self):
        NRow = 6 if gvar.gboard.StageHas6Rows() else 5
        for row in range(NRow):
            mower = Lawn.LawnMower.GetNewLawnMower()
            mower.LawnMowerInitialize(row)
            mower.mMowerState = Lawn.LawnMowerState.Ready
            mower.mPosX = Sexy.Constants.BOARD_EXTRA_ROOM - 21.0
            gvar.gboard.mLawnMowers.Add(mower)
    
    def StartLawnMower(self):
        for i in range(gvar.gboard.mLawnMowers.Count):
            mower = gvar.gboard.mLawnMowers[i]
            if not mower.mDead:
                mower.StartMower()
    
    def RemoveLawnMower(self):
        gvar.gboard.mBonusLawnMowersRemaining = 0
        for i in range(gvar.gboard.mLawnMowers.Count):
            mower = gvar.gboard.mLawnMowers[i]
            if not mower.mDead:
                mower.Die()

    def FailImmediately(self, zombietype: Lawn.ZombieType):
        if gvar.gboard is None:
            return
        board_EDGE = Sexy.Constants.BOARD_EDGE
        if zombietype in [Lawn.ZombieType.Gargantuar, Lawn.ZombieType.RedeyeGargantuar]:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 50
        elif zombietype == Lawn.ZombieType.Polevaulter:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 50
        elif zombietype in [Lawn.ZombieType.Catapult, Lawn.ZombieType.Football, Lawn.ZombieType.Zamboni]:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 75
        elif zombietype == Lawn.ZombieType.Zamboni:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 75
        elif zombietype in [Lawn.ZombieType.BackupDancer, Lawn.ZombieType.Dancer, Lawn.ZombieType.Snorkel]:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 30
        zombie = gvar.gboard.AddZombie(zombietype, 0)
        zombie.mPosX = board_EDGE
        # 没有这个会崩溃，因为游戏失败对话和暂停貌似会冲突
        gvar.glawnapp.KillDialog(19)
        gvar.gboard.ZombiesWon(zombie)
    
    def GivePottedPlant(self, seedtype: Lawn.SeedType):
        pottedPlant = Lawn.PottedPlant()
        pottedPlant.InitializePottedPlant(seedtype)
        pottedPlant.mPlantAge = Lawn.PottedPlantAge.Full
        gvar.glawnapp.mZenGarden.AddPottedPlant(pottedPlant)

cheat_option = CheatOption()

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

# 满阳光+无冷却
# gvar.gboard.mSunMoney = 9990  # 满阳光
# gvar.glawnapp.mEasyPlantingCheat = True  # 无冷却

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

# 更好的自动收集，包括盆栽。PGvZ-TAS自带，只需引入pgvz模块。关闭只需把下面一句取消注释。
# auto_collector.Off()

# 传送带无冷却 TODO: 目前不太行，等我更新
# 相关函数 Lawn.Challenge.UpdateConveyorBelt, Lawn.SeedBank.UpdateConveyorBelt
# @LawnMod.MonoModUtils.HookTo(Lawn.SeedBank.UpdateConveyorBelt)
# def hook_seedbank_UpdateConveyorBelt(orig, seedbank: Lawn.SeedBank):
#     seedbank.mConveyorBeltCounter = 0
#     for i in range(seedbank.mNumPackets):
#         seedbank.mSeedPackets[i].mOffsetY = 0

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
            if plant.mSeedType in [Lawn.SeedType.Cherrybomb, Lawn.SeedType.Jalapeno, Lawn.SeedType.Doomshroom, Lawn.SeedType.Iceshroom, Lawn.SeedType.PickledPepper]:
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

# 玉米炮无冷却
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.UpdateCobCannon)
def Plant__UpdateCobCannon(orig, plant: Lawn.Plant):
    if plant.mState == Lawn.PlantState.CobcannonArming and cheat_option.cobNoCooling:
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

# 全屏留声机
@LawnMod.MonoModUtils.HookTo(Lawn.ZenGarden.DoFeedingTool)
def ZenGarden__DoFeedingTool(orig, zengarden: Lawn.ZenGarden, x: int, y: int, theToolType: Lawn.GridItemState):
    if theToolType == Lawn.GridItemState.ZenToolPhonograph:
        for i in range(zengarden.mBoard.mPlants.Count):
            plant = zengarden.mBoard.mPlants[i]
            if not plant.mDead and zengarden.mBoard.GetTopPlantAt(plant.mPlantCol, plant.mRow, Lawn.TopPlant.ZenToolOrder) == plant:
                thePottedPlant = zengarden.PottedPlantFromIndex(plant.mPottedPlantIndex)
                if zengarden.GetPlantsNeed(thePottedPlant) == Lawn.PottedPlantNeed.Phonograph:
                    zengarden.PlantFulfillNeed(plant)
    else:
        orig(zengarden, x, y, theToolType)

# 移除迷雾
@LawnMod.MonoModUtils.HookTo(Lawn.Board.DrawFog)
def Board__DrawFog(orig, board: Lawn.Board, graphics: Sexy.Graphics):
    if not cheat_option.noFog:
        orig(board, graphics)
