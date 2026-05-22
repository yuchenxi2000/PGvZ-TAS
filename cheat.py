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
from pgvz.lineup import LineUp
from functools import wraps

# 关闭assertion，不然启动带命令行的游戏（Lawn.Console.exe）在输出过多时会卡死
@LawnMod.MonoModUtils.HookTo(Sexy.Debug.ASSERT)
def Debug__ASSERT(orig, value: bool):
    return

# 设置在主线程中运行，不然可能因为线程错误导致崩溃
def main_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def _ScriptFunc():
            func(*args, **kwargs)
            yield
        script_manager.Register(_ScriptFunc, runmode=ScriptRunMode.GLOBAL)
    return wrapper

# 作弊选项，其中成员设置为True就是开启。还包括一些包装好的函数
# 推荐配合cheat-gui.html使用
class CheatOption:
    def __init__(self) -> None:
        self.wontLose = False
        self.freePlant = False
        self.plantAnyWhere = False
        self.plantNoDie = False
        self.zombieNoDie = False
        self.cobNoCooling = False
        self.disableTalisman = False
        self.disableNinja = False
        self.visibleGhoul = False
        self.noThunder = False
        self.diamondZenTools = False
        self.noFog = False
        self.transScaryPot = False
        self.conveyorNoCooling = False
        self.featureThreePeater = False
        self.butterPult = False
        self.doubleGatlingpea = False
        self.fullAreaGloomshroom = False
        self.enableGlove = False
        self.zombieStop = False
        self.chomperNoCooling = False
        self.noCover = False
        self.stopSpawning = False

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

    @main_thread
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
    
    @main_thread
    def RemovePlantOnBoard(self):
        for plant in IterAlivePlants():
            plant.Die()
    
    @main_thread
    def ZombieOnBoard(self, row: int, col: int, zombietype: Lawn.ZombieType, mind_ctrl: bool = False):
        row_range, col_range = self.ConvertRange(row, col)
        curwave = gvar.gboard.mCurrentWave
        for row1 in row_range:
            for col1 in col_range:
                xi = gvar.gboard.GridToPixelX(col1, row1)
                zombie = gvar.gboard.AddZombieInRow(zombietype, row1, curwave)
                zombie.mPosX = xi
                zombie.mX = xi
                zombie.mMindControlled = mind_ctrl
                if zombietype == Lawn.ZombieType.Bungee:
                    zombie.mTargetCol = col1
                    zombie.SetRow(row1)
                    zombie.mPosX = gvar.gboard.GridToPixelX(col1, row1)
                    zombie.mPosY = zombie.GetPosYBasedOnRow(row1)
                    zombie.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, row1, 7)
    
    @main_thread
    def RemoveZombieOnBoard(self):
        for zombie in IterAliveZombies():
            zombie.DieNoLoot(False)
    
    def SetSeedPacket(self, idx: int, seedtype: Lawn.SeedType, isImitater: bool):
        seedpacket = gvar.gboard.mSeedBank.mSeedPackets[idx]
        if isImitater:
            seedpacket.SetPacketType(Lawn.SeedType.Imitater, seedtype)
        else:
            seedpacket.SetPacketType(seedtype, SeedTypeNone)
    
    @main_thread
    def AddGridItemOnBoard(self, row: int, col: int, gridItemType: Lawn.GridItemType):
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                if gridItemType == Lawn.GridItemType.Rake:
                    # 由于函数之前有一个判断，因此只能写这么大一堆代码了
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
                elif gridItemType == Lawn.GridItemType.Crater:
                    crater = gvar.gboard.AddACrater(col1, row1)
                    crater.mGridItemCounter = 18000
                elif gridItemType == Lawn.GridItemType.Gravestone:
                    grave_stone = gvar.gboard.AddAGraveStone(col1, row1)
                    grave_stone.mGridItemCounter = 100  # 否则非存在墓碑场地不更新，墓碑无法钻出
                elif gridItemType == Lawn.GridItemType.Ladder:
                    gvar.gboard.AddALadder(col1, row1)
                elif gridItemType == Lawn.GridItemType.Talisman:
                    Lawn.Zombie.GetNewZombie().CreateTalismanAt(col1, row1)
                elif gridItemType == Lawn.GridItemType.TalismanMove:
                    Lawn.Zombie.GetNewZombie().CreateTalismanMoveAt(col1, row1)
                elif gridItemType in [Lawn.GridItemType.PortalCircle, Lawn.GridItemType.PortalSquare]:
                    newGridItem = Lawn.GridItem.GetNewGridItem()
                    newGridItem.mGridItemType = gridItemType
                    newGridItem.mGridX = col1
                    newGridItem.mGridY = row1
                    newGridItem.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.Particle, newGridItem.mGridY, 0)
                    newGridItem.OpenPortal()
                    gvar.gboard.mGridItems.Add(newGridItem)

    @main_thread
    def AddScaryPotOnBoard(self, row: int, col: int, theScaryPotType: Lawn.ScaryPotType, appearance: Lawn.GridItemState, theZombieType: Lawn.ZombieType, theSeedType: Lawn.SeedType, numSun: int):
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                newGridItem = Lawn.GridItem.GetNewGridItem()
                newGridItem.mGridItemType = Lawn.GridItemType.ScaryPot
                newGridItem.mGridItemState = appearance
                newGridItem.mGridX = col1
                newGridItem.mGridY = row1
                newGridItem.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.Plant, newGridItem.mGridY, 0)
                newGridItem.mSeedType = theSeedType
                newGridItem.mZombieType = theZombieType
                newGridItem.mScaryPotType = theScaryPotType
                gvar.gboard.mGridItems.Add(newGridItem)
                if theScaryPotType == Lawn.ScaryPotType.Sun:
                    newGridItem.mSunCount = numSun
    
    @main_thread
    def AddLadderSmart(self):
        NRow = 6 if gvar.gboard.StageHas6Rows() else 5
        NCol = 9
        for row1 in range(NRow):
            if gvar.gboard.mPlantRow[row1] != Lawn.PlantRowType.Pool:  # 泳池不要搭梯
                for col1 in range(1, NCol):  # 最后一排不要搭梯
                    plantPumpkin = gvar.gboard.GetTopPlantAt(col1, row1, Lawn.TopPlant.OnlyPumpkin)
                    if plantPumpkin is not None and gvar.gboard.GetLadderAt(col1, row1) is None:  # 没南瓜，或已经有梯子不要搭梯
                        gvar.gboard.AddALadder(col1, row1)

    @main_thread
    def RemoveGridItemOnBoard(self, row: int, col: int, gridItemType: Lawn.GridItemType):
        # 虽然宝石迷阵里的弹坑并不是场地物品，还是把它移除了吧
        if gridItemType == Lawn.GridItemType.Crater and gvar.glawnapp.mGameMode in [Lawn.GameMode.ChallengeBeghouled, Lawn.GameMode.ChallengeBeghouledTwist]:
            challenge = gvar.gboard.mChallenge
            challenge.BeghouledClearCrater(40)
            challenge.BeghouledStartFalling(Lawn.ChallengeState.BeghouledFalling)
            return
        row_range, col_range = self.ConvertRange(row, col)
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == gridItemType and griditem.mGridX in col_range and griditem.mGridY in row_range:
                griditem.GridItemDie()
    
    @main_thread
    def RemoveCoinOnBoard(self, cointype: Lawn.CoinType):
        for coin in IterAliveCoins():
            if coin.mType == cointype:
                coin.Die()
    
    @main_thread
    def AddCoinOnBoard(self, x: int, y: int, cointype: Lawn.CoinType, seedtype: Lawn.SeedType, reverse: bool):
        coin = gvar.gboard.AddCoin(x, y, cointype, Lawn.CoinMotion.Coin)
        if cointype == Lawn.CoinType.UsableSeedPacket:
            coin.mUsableSeedType = seedtype
        elif cointype == Lawn.CoinType.PresentPlant:
            coin.mPottedPlantSpec.mSeedType = seedtype
            coin.mPottedPlantSpec.mFacing = Lawn.PottedPlant.FacingDirection.Left if reverse else Lawn.PottedPlant.FacingDirection.Right
    
    @main_thread
    def OpenScaryPotterOnBoard(self):
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == Lawn.GridItemType.ScaryPot:
                gvar.gboard.mChallenge.ScaryPotterOpenPot(griditem)

    @main_thread
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

    @main_thread
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
    
    @main_thread
    def GivePottedPlant(self, seedtype: Lawn.SeedType, reverse: bool = False):
        pottedPlant = Lawn.PottedPlant()
        pottedPlant.InitializePottedPlant(seedtype)
        pottedPlant.mPlantAge = Lawn.PottedPlantAge.Full
        pottedPlant.mFacing = Lawn.PottedPlant.FacingDirection.Left if reverse else Lawn.PottedPlant.FacingDirection.Right
        gvar.glawnapp.mZenGarden.AddPottedPlant(pottedPlant)
    
    @main_thread
    def GetFinishedAccount(self):
        # 解锁所有关卡
        playerinfo = gvar.glawnapp.mPlayerInfo
        playerinfo.mHasUnlockedMinigames = True
        playerinfo.mHasUnlockedPuzzleMode = True
        playerinfo.mHasNewMiniGame = False
        playerinfo.mHasNewVasebreaker = False
        playerinfo.mHasNewIZombie = False
        playerinfo.mHasNewSurvival = False
        playerinfo.mHasUnlockedSurvivalMode = True
        playerinfo.mZenGardenTutorialComplete = True
        playerinfo.mMiniGamesUnlocked = 20
        playerinfo.mVasebreakerUnlocked = 10
        playerinfo.mIZombieUnlocked = 10
        if playerinfo.mFinishedAdventure < 2:
            playerinfo.mFinishedAdventure = 2
        # 完成所有关卡
        lawnapp = gvar.glawnapp
        for gamemode in range(1, 148):
            if 70 <= gamemode < 122:
                continue
            # 当前版本无法完成
            if 138 <= gamemode < 141 or 146 <= gamemode < 148:
                continue
            level = Lawn.GameMode(gamemode)
            if lawnapp.IsSurvivalNormal(level):
                if playerinfo.mChallengeRecords[gamemode - 1] < 5:
                    playerinfo.mChallengeRecords[gamemode - 1] = 5
            elif lawnapp.IsSurvivalHard(level):
                if playerinfo.mChallengeRecords[gamemode - 1] < 10:
                    playerinfo.mChallengeRecords[gamemode - 1] = 10
            elif lawnapp.IsSurvivalHell(level):
                if playerinfo.mChallengeRecords[gamemode - 1] < 10:
                    playerinfo.mChallengeRecords[gamemode - 1] = 10
            elif not lawnapp.IsSurvivalEndless(level) and not lawnapp.IsEndlessScaryPotter(level) and not lawnapp.IsEndlessIZombie(level):
                if playerinfo.mChallengeRecords[gamemode - 1] < 1:
                    playerinfo.mChallengeRecords[gamemode - 1] = 1
        # 为了在图鉴里显示红眼巨人
        if playerinfo.mChallengeRecords[12] < 10:
            playerinfo.mChallengeRecords[12] = 10
        # 紫卡
        for i in range(9):
            playerinfo.mPurchases[i] = 1
        # 花园用具，注意钻石水壶需要填2
        playerinfo.mPurchases[13] = 2
        playerinfo.mPurchases[14] = 1020
        playerinfo.mPurchases[15] = 1020
        for i in range(16, 20):
            playerinfo.mPurchases[i] = 1
        # 蜗牛
        playerinfo.mPurchases[20] = 1
        # 卡槽
        playerinfo.mPurchases[21] = 4
        # 割草机
        playerinfo.mPurchases[22] = 1
        playerinfo.mPurchases[23] = 1
        # 钉耙
        playerinfo.mPurchases[24] = 10
        # 水族馆
        playerinfo.mPurchases[25] = 1
        # 巧克力，最多999
        playerinfo.mPurchases[26] = 1999
        # 不知道什么
        playerinfo.mPurchases[27] = 1
        # 树肥
        playerinfo.mPurchases[28] = 1010
        # （懒得写注释了）
        for i in range(29, 36):
            playerinfo.mPurchases[i] = 1
        # 卡组
        playerinfo.mPurchases[36] = 4
        # 夜晚绿房
        playerinfo.mPurchases[37] = 1
        # 刷新显示
        if gvar.glawnapp.mGameScene == Lawn.GameScenes.Menu:
            gvar.glawnapp.KillGameSelector()
            gvar.glawnapp.ShowGameSelector()
    
    def SetSpeed(self, speed: float):
        fast = speed >= 1.0
        factor = round(speed) if fast else round(1.0 / speed)
        Sexy.GlobalStaticVars.gFastMo = fast
        Sexy.GlobalStaticVars.gSlowMo = not fast
        Sexy.GlobalStaticVars.gFastSlowMoNum = factor
    
    @main_thread  # 必须在主线程运行，不然会有概率崩溃
    def EnterNewGame(self, gamemode: Lawn.GameMode):
        # 删除所有对话框
        gvar.glawnapp.KillDialog(3)  # 图鉴
        gvar.glawnapp.KillDialog(4)  # 商店
        gvar.glawnapp.KillDialog(19)  # 暂停
        gvar.glawnapp.KillDialog(37)  # 继续
        gvar.glawnapp.KillDialog(65)  # 钉耙
        # 删除所有界面
        if gvar.glawnapp.mGameScene == Lawn.GameScenes.Playing or gvar.glawnapp.mGameScene == Lawn.GameScenes.LevelIntro:
            gvar.glawnapp.KillBoard()
        elif gvar.glawnapp.mGameScene == Lawn.GameScenes.Menu:
            gvar.glawnapp.KillGameSelector()
        elif gvar.glawnapp.mGameScene == Lawn.GameScenes.Challenge:
            gvar.glawnapp.KillChallengeScreen()
        elif gvar.glawnapp.mGameScene == Lawn.GameScenes.Award:
            gvar.glawnapp.KillAwardScreen()
        # 加载新游戏
        gvar.glawnapp.PreNewGame(gamemode, True)
    
    @main_thread
    def CheatSetZombies(self, zb_list, internal_spawn: bool = True):  # type: (list[Lawn.ZombieType], bool) -> None
        SetZombies(zb_list, internal_spawn)
    
    @main_thread  # 必须在主线程运行，不然会有概率崩溃
    def LineUpOnBoard(self, linup_code_b64: str):
        LineUp.from_str(linup_code_b64).to_board(gvar.gboard)
    
    def UnlockCrazyDaveSeed(self):
        for i in range(60):
            chosenSeed = gvar.glawnapp.mSeedChooserScreen.mChosenSeeds[i]
            if chosenSeed is not None:
                chosenSeed.mCrazyDavePicked = False
    
    @main_thread
    def SetAdventureLevel(self, level: int):
        gvar.glawnapp.mPlayerInfo.mLevel = level
        if gvar.glawnapp.mGameScene == Lawn.GameScenes.Menu:
            gvar.glawnapp.KillGameSelector()
            gvar.glawnapp.ShowGameSelector()

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

# 无限阳光
def ScriptInfSun():
    gvar.gboard.mSunMoney = 9990
script_inf_sun = script_manager.Register(ScriptInfSun, runmode=ScriptRunMode.FOREVER)
script_inf_sun.Off()

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
        return board.mApp.mGameMode not in [Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom]
    else:
        return orig(board)

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
            if zombie.mZombieType in [Lawn.ZombieType.Zamboni, Lawn.ZombieType.Catapult] and Sexy.TodLib.TodCommon.TestBit(theDamageFlags, 5):
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

# 玉米炮无冷却, 僵尸无敌修改大嘴花
@LawnMod.MonoModUtils.HookTo(Lawn.Plant.Update)
def Plant__Update(orig, plant: Lawn.Plant):
    if plant.mState == Lawn.PlantState.CobcannonArming and cheat_option.cobNoCooling:
        plant.mStateCountdown = 0
    elif plant.mState == Lawn.PlantState.ChomperBitingGotOne and cheat_option.zombieNoDie:
        plant.mState = Lawn.PlantState.ChomperBitingMissed
    elif plant.mState == Lawn.PlantState.ChomperDigesting and cheat_option.chomperNoCooling:
        plant.mStateCountdown = 0
    orig(plant)

# 技能无冷却
def ScriptKillNoCooling():
    gvar.gboard.mAgavePowerfulCountdown = 0
    gvar.gboard.mEndoflamePowerfulCountdown = 0
script_skill_nocooling = script_manager.Register(ScriptKillNoCooling, runmode=ScriptRunMode.FOREVER)
script_skill_nocooling.Off()

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

# 全屏留声机、花肥、杀虫剂
@LawnMod.MonoModUtils.HookTo(Lawn.ZenGarden.MouseDownWithFeedingTool)
def ZenGarden__MouseDownWithFeedingTool(orig, zenGarden: Lawn.ZenGarden, x: int, y: int, theCursorType: Lawn.CursorType, isTouch: bool):
    if cheat_option.diamondZenTools and theCursorType in [Lawn.CursorType.Fertilizer, Lawn.CursorType.BugSpray, Lawn.CursorType.Phonograph]:
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
        if plant.mShootingCounter - 1 in [18, 26, 35, 43, 51, 60, 68, 76]:
            plant.Fire(None, plant.mRow, Lawn.PlantWeapon.Primary)  # type: ignore
            plant.mShootingCounter -= 1
            return
    orig(plant)
