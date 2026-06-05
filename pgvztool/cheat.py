"""
更好的作弊
请配合cheat-gui.html使用
"""
import System
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
        self._plantNoDie = False
        self.zombieNoDie = False
        self.cobNoCooling = False
        self.potatoNoCooling = False
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
        self.drawPlantHp = False
        self.drawZombieHp = False
        self.selectZombieHp = False
        self.shovelNoReset = False
        self.runBackground = False
        self.gloveNoCooling = False
    
    def ShowErrorInGame(self, title: str, msg: str):
        lawnapp = GetLawnApp()
        # ID为7的对话框点击ok按钮会直接关闭
        lawnapp.KillDialog(7)
        lawnapp.DoDialog(7, True, title, msg, '好的', 3)
    
    @property
    def plantNoDie(self):
        return self._plantNoDie
    
    @plantNoDie.setter
    def plantNoDie(self, value):
        if self._plantNoDie != value:
            # 取消篮球、僵尸豌豆的伤害
            if value:
                Lawn.GameConstants.gProjectileDefinition[int(Lawn.ProjectileType.ZombiePea)].mDamage = 0
                Lawn.GameConstants.gProjectileDefinition[int(Lawn.ProjectileType.Basketball)].mDamage = 0
            else:
                Lawn.GameConstants.gProjectileDefinition[int(Lawn.ProjectileType.ZombiePea)].mDamage = 20
                Lawn.GameConstants.gProjectileDefinition[int(Lawn.ProjectileType.Basketball)].mDamage = 75
            self._plantNoDie = value

    def ConvertRange(self, row: int, col: int):
        NRow = 6 if GetBoard().StageHas6Rows() else 5
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
        board = GetBoard()
        if board is None:
            return
        if seedtype == Lawn.SeedType.Imitater and not isImitater:
            return
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                if isImitater:
                    board.AddPlant(col1, row1, Lawn.SeedType.Imitater, seedtype)
                else:
                    board.AddPlant(col1, row1, seedtype, SeedTypeNone)
    
    @main_thread
    def RemovePlantOnBoard(self):
        for plant in IterAlivePlants():
            plant.Die()
    
    @main_thread
    def ZombieOnBoard(self, row: int, col: int, zombietype: Lawn.ZombieType, mind_ctrl: bool = False):
        board = GetBoard()
        if board is None:
            return
        row_range, col_range = self.ConvertRange(row, col)
        curwave = board.mCurrentWave
        for row1 in row_range:
            for col1 in col_range:
                xi = board.GridToPixelX(col1, row1)
                zombie = board.AddZombieInRow(zombietype, row1, curwave)
                offsetX = xi - zombie.mPosX
                zombie.mPosX = xi
                zombie.mMindControlled = mind_ctrl
                if zombietype == Lawn.ZombieType.Bungee:
                    zombie.mTargetCol = col1
                    zombie.SetRow(row1)
                    zombie.mPosX = board.GridToPixelX(col1, row1)
                    zombie.mPosY = zombie.GetPosYBasedOnRow(row1)
                    zombie.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, row1, 7)
                elif zombietype == Lawn.ZombieType.Bobsled:
                    # 找到其他三个人
                    for iz in range(zombie.mFollowerZombieID.Count):
                        zombieFollower = zombie.mFollowerZombieID[iz]
                        if zombieFollower is None:
                            continue
                        zombieFollower.mPosX += offsetX
                        zombieFollower.mMindControlled = mind_ctrl
    
    @main_thread
    def RemoveZombieOnBoard(self):
        if GetBoard() is None:
            return
        for zombie in IterAliveZombies():
            zombie.DieNoLoot(False)
    
    def SetSeedPacket(self, idx: int, seedtype: Lawn.SeedType, isImitater: bool):
        board = GetBoard()
        if board is None:
            return
        seedpacket = board.mSeedBank.mSeedPackets[idx]
        if isImitater:
            seedpacket.SetPacketType(Lawn.SeedType.Imitater, seedtype)
        else:
            seedpacket.SetPacketType(seedtype, SeedTypeNone)
    
    @main_thread
    def AddGridItemOnBoard(self, row: int, col: int, gridItemType: Lawn.GridItemType):
        lawnApp = GetLawnApp()
        board = lawnApp.mBoard
        if board is None:
            return
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                if gridItemType == Lawn.GridItemType.Rake:
                    # 由于函数之前有一个判断，因此只能写这么大一堆代码了
                    newGridItem = Lawn.GridItem.GetNewGridItem()
                    newGridItem.mGridItemType = Lawn.GridItemType.Rake
                    newGridItem.mGridX = col1
                    newGridItem.mGridY = row1
                    newGridItem.mPosX = board.GridToPixelX(newGridItem.mGridX, newGridItem.mGridY)
                    newGridItem.mPosY = board.GridToPixelY(newGridItem.mGridX, newGridItem.mGridY)
                    newGridItem.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, newGridItem.mGridY, 9)
                    board.mGridItems.Add(newGridItem)
                    theReanimation = board.CreateRakeReanim(newGridItem.mPosX, newGridItem.mPosY, 0)
                    newGridItem.mGridItemReanimID = lawnApp.ReanimationGetID(theReanimation)
                    newGridItem.mGridItemState = Lawn.GridItemState.RakeAttracting
                elif gridItemType == Lawn.GridItemType.Crater:
                    crater = board.AddACrater(col1, row1)
                    crater.mGridItemCounter = 18000
                elif gridItemType == Lawn.GridItemType.Gravestone:
                    grave_stone = board.AddAGraveStone(col1, row1)
                    grave_stone.mGridItemCounter = 100  # 否则非存在墓碑场地不更新，墓碑无法钻出
                elif gridItemType == Lawn.GridItemType.Ladder:
                    board.AddALadder(col1, row1)
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
                    board.mGridItems.Add(newGridItem)

    @main_thread
    def AddScaryPotOnBoard(self, row: int, col: int, theScaryPotType: Lawn.ScaryPotType, appearance: Lawn.GridItemState, theZombieType: Lawn.ZombieType, theSeedType: Lawn.SeedType, numSun: int):
        board = GetBoard()
        if board is None:
            return
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
                board.mGridItems.Add(newGridItem)
                if theScaryPotType == Lawn.ScaryPotType.Sun:
                    newGridItem.mSunCount = numSun
    
    @main_thread
    def AddLadderSmart(self):
        board = GetBoard()
        if board is None:
            return
        NRow = 6 if board.StageHas6Rows() else 5
        NCol = 9
        for row1 in range(NRow):
            if board.mPlantRow[row1] != Lawn.PlantRowType.Pool:  # 泳池不要搭梯
                for col1 in range(1, NCol):  # 最后一排不要搭梯
                    plantPumpkin = board.GetTopPlantAt(col1, row1, Lawn.TopPlant.OnlyPumpkin)
                    if plantPumpkin is not None and board.GetLadderAt(col1, row1) is None:  # 没南瓜，或已经有梯子不要搭梯
                        board.AddALadder(col1, row1)

    @main_thread
    def RemoveGridItemOnBoard(self, row: int, col: int, gridItemType: Lawn.GridItemType):
        lawnApp = GetLawnApp()
        board = lawnApp.mBoard
        if board is None:
            return
        # 虽然宝石迷阵里的弹坑并不是场地物品，还是把它移除了吧
        if gridItemType == Lawn.GridItemType.Crater and lawnApp.mGameMode in [Lawn.GameMode.ChallengeBeghouled, Lawn.GameMode.ChallengeBeghouledTwist]:
            challenge = board.mChallenge
            challenge.BeghouledClearCrater(40)
            challenge.BeghouledStartFalling(Lawn.ChallengeState.BeghouledFalling)
            return
        row_range, col_range = self.ConvertRange(row, col)
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == gridItemType and griditem.mGridX in col_range and griditem.mGridY in row_range:
                griditem.GridItemDie()
    
    @main_thread
    def RemoveCoinOnBoard(self, cointype: Lawn.CoinType):
        board = GetBoard()
        if board is None:
            return
        for coin in IterAliveCoins():
            if coin.mType == cointype:
                coin.Die()
    
    @main_thread
    def AddCoinOnBoard(self, x: int, y: int, cointype: Lawn.CoinType, seedtype: Lawn.SeedType, reverse: bool):
        board = GetBoard()
        if board is None:
            return
        coin = board.AddCoin(x, y, cointype, Lawn.CoinMotion.Coin)
        if cointype == Lawn.CoinType.UsableSeedPacket:
            coin.mUsableSeedType = seedtype
        elif cointype == Lawn.CoinType.PresentPlant:
            coin.mPottedPlantSpec.mSeedType = seedtype
            coin.mPottedPlantSpec.mFacing = Lawn.PottedPlant.FacingDirection.Left if reverse else Lawn.PottedPlant.FacingDirection.Right
    
    @main_thread
    def OpenScaryPotterOnBoard(self):
        board = GetBoard()
        if board is None:
            return
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == Lawn.GridItemType.ScaryPot:
                board.mChallenge.ScaryPotterOpenPot(griditem)

    @main_thread
    def AddLawnMower(self):
        board = GetBoard()
        if board is None:
            return
        NRow = 6 if board.StageHas6Rows() else 5
        for row in range(NRow):
            mower = Lawn.LawnMower.GetNewLawnMower()
            mower.LawnMowerInitialize(row)
            mower.mMowerState = Lawn.LawnMowerState.Ready
            mower.mPosX = Sexy.Constants.BOARD_EXTRA_ROOM - 21.0
            board.mLawnMowers.Add(mower)
    
    def StartLawnMower(self):
        board = GetBoard()
        if board is None:
            return
        for i in range(board.mLawnMowers.Count):
            mower = board.mLawnMowers[i]
            if not mower.mDead:
                mower.StartMower()
    
    def RemoveLawnMower(self):
        board = GetBoard()
        if board is None:
            return
        board.mBonusLawnMowersRemaining = 0
        for i in range(board.mLawnMowers.Count):
            mower = board.mLawnMowers[i]
            if not mower.mDead:
                mower.Die()

    @main_thread
    def FailImmediately(self, zombietype: Lawn.ZombieType):
        lawnApp = GetLawnApp()
        board = lawnApp.mBoard
        if board is None:
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
        zombie = board.AddZombie(zombietype, 0)
        zombie.mPosX = board_EDGE
        # 没有这个会崩溃，因为游戏失败对话和暂停貌似会冲突
        lawnApp.KillDialog(19)
        board.ZombiesWon(zombie)
    
    @main_thread
    def GivePottedPlant(self, seedtype: Lawn.SeedType, reverse: bool = False):
        zenGarden = GetLawnApp().mZenGarden
        if zenGarden.IsZenGardenFull(False):
            self.ShowErrorInGame('错误！', '你的花园已经满了，请清理一些盆栽，或者移一些到蘑菇园和水族馆后再试！')
            return
        pottedPlant = Lawn.PottedPlant()
        pottedPlant.InitializePottedPlant(seedtype)
        pottedPlant.mPlantAge = Lawn.PottedPlantAge.Full
        pottedPlant.mFacing = Lawn.PottedPlant.FacingDirection.Left if reverse else Lawn.PottedPlant.FacingDirection.Right
        pottedPlant.mPlantNeed = PottedPlantNeedNone
        pottedPlant.mLastNeedFulfilledTime = System.DateTime.UtcNow
        zenGarden.AddPottedPlant(pottedPlant)
    
    def AddPottedPlantToGivenPos(self, seedtype: Lawn.SeedType, facing: Lawn.PottedPlant.FacingDirection, x: int, y: int, pos: Lawn.GardenType):
        lawnapp = GetLawnApp()
        player = lawnapp.mPlayerInfo
        pottedPlant = player.mPottedPlant[player.mNumPottedPlants]
        pottedPlant.InitializePottedPlant(seedtype)
        pottedPlant.mPlantAge = Lawn.PottedPlantAge.Full
        pottedPlant.mFacing = facing
        pottedPlant.mX = x
        pottedPlant.mY = y
        pottedPlant.mWhichZenGarden = pos
        pottedPlant.mPlantNeed = PottedPlantNeedNone
        pottedPlant.mLastNeedFulfilledTime = System.DateTime.UtcNow
        player.mNumPottedPlants += 1
    
    @main_thread
    def GiveAllPottedPlants(self):
        lawnapp = GetLawnApp()
        player = lawnapp.mPlayerInfo
        # 检查是否所有花园已购买
        # 18: 蘑菇园; 25: 水族馆; 37: 夜晚绿房
        if player.mPurchases[18] == 0 or player.mPurchases[25] == 0 or player.mPurchases[37] == 0:
            self.ShowErrorInGame('错误！', '要放下全部类型盆栽，必须购买所有花园，请去商店里购买后再试！')
            return
        # 先清除所有盆栽
        player.mNumPottedPlants = 0
        # 摆放所有盆栽。外观重复、会出bug的不给。
        seedTypeCount = int(Lawn.SeedType.SeedTypeCount)
        ownedPottedPlant = [[False for _ in range(2)] for _ in range(seedTypeCount)]  # 已拥有的盆栽
        seedTypeList = []
        for iseed in range(seedTypeCount):
            seedType = System.Enum.ToObject(Lawn.SeedType, iseed)
            if seedType in [Lawn.SeedType.Flowerpot, Lawn.SeedType.GiantWallnut, Lawn.SeedType.Sprout, Lawn.SeedType.Leftpeater, Lawn.SeedType.ImitaterRandomPlant, Lawn.SeedType.ImitaterRandomZombie, Lawn.SeedType.HypnoCattail]:
                continue
            seedTypeList.append(seedType)
        facingList = [Lawn.PottedPlant.FacingDirection.Right, Lawn.PottedPlant.FacingDirection.Left]
        gardenNextGrid = [0, 0, 0, 0, 0, 0, 0]
        # 先把水生植物、蘑菇类摆到对应花园，蘑菇类没位置优先摆到夜晚绿房
        garden = Lawn.GardenType.Aquarium
        for seedType in seedTypeList:
            if Lawn.Plant.IsAquatic(seedType):
                for facing in facingList:
                    gridX = gardenNextGrid[int(garden)]
                    if gridX < 8 and not ownedPottedPlant[int(seedType)][int(facing)]:
                        self.AddPottedPlantToGivenPos(seedType, facing, gridX, 0, garden)
                        ownedPottedPlant[int(seedType)][int(facing)] = True
                        gardenNextGrid[int(garden)] += 1
        for garden in [Lawn.GardenType.Mushroom, Lawn.GardenType.Mushroom2]:
            for seedType in seedTypeList:
                if Lawn.Plant.IsNocturnal(seedType):
                    for facing in facingList:
                        gridX = gardenNextGrid[int(garden)]
                        if gridX < 8 and not ownedPottedPlant[int(seedType)][int(facing)]:
                            self.AddPottedPlantToGivenPos(seedType, facing, gridX, 0, garden)
                            ownedPottedPlant[int(seedType)][int(facing)] = True
                            gardenNextGrid[int(garden)] += 1
        garden = Lawn.GardenType.Night
        for seedType in seedTypeList:
            if Lawn.Plant.IsNocturnal(seedType):
                for facing in facingList:
                    grid = gardenNextGrid[int(garden)]
                    if grid < 32 and not ownedPottedPlant[int(seedType)][int(facing)]:
                        self.AddPottedPlantToGivenPos(seedType, facing, grid % 8, grid // 8, garden)
                        ownedPottedPlant[int(seedType)][int(facing)] = True
                        gardenNextGrid[int(garden)] += 1
        for garden in [Lawn.GardenType.Main, Lawn.GardenType.Main2, Lawn.GardenType.Night]:
            for seedType in seedTypeList:
                for facing in facingList:
                    grid = gardenNextGrid[int(garden)]
                    if grid < 32 and not ownedPottedPlant[int(seedType)][int(facing)]:
                        self.AddPottedPlantToGivenPos(seedType, facing, grid % 8, grid // 8, garden)
                        ownedPottedPlant[int(seedType)][int(facing)] = True
                        gardenNextGrid[int(garden)] += 1
        # 刷新外观
        if lawnapp.mGameMode == Lawn.GameMode.ChallengeZenGarden and lawnapp.mGameScene == Lawn.GameScenes.Playing:
            lawnapp.KillBoard()
            lawnapp.PreNewGame(Lawn.GameMode.ChallengeZenGarden, False)

    @main_thread
    def GetFinishedAccount(self):
        lawnapp = GetLawnApp()
        playerinfo = lawnapp.mPlayerInfo
        # 解锁所有关卡
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
        for gamemode in range(1, int(Lawn.GameMode.GameModeCount)):
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
        # 猫尾草皮肤
        playerinfo.mPurchases[38] = 1
        # 刷新显示
        if lawnapp.mGameScene == Lawn.GameScenes.Menu:
            lawnapp.KillGameSelector()
            lawnapp.ShowGameSelector()
    
    def SetSpeed(self, speed: float):
        fast = speed >= 1.0
        factor = round(speed) if fast else round(1.0 / speed)
        Sexy.GlobalStaticVars.gFastMo = fast
        Sexy.GlobalStaticVars.gSlowMo = not fast
        Sexy.GlobalStaticVars.gFastSlowMoNum = factor
    
    def _EnterNewGame(self, gamemode: Lawn.GameMode):
        lawnapp = GetLawnApp()
        # 删除所有对话框
        lawnapp.KillDialog(3)  # 图鉴
        lawnapp.KillDialog(4)  # 商店
        lawnapp.KillDialog(19)  # 暂停
        lawnapp.KillDialog(37)  # 继续
        lawnapp.KillDialog(65)  # 钉耙
        # 删除所有界面
        if lawnapp.mGameScene == Lawn.GameScenes.Playing or lawnapp.mGameScene == Lawn.GameScenes.LevelIntro:
            lawnapp.KillBoard()
        elif lawnapp.mGameScene == Lawn.GameScenes.Menu:
            lawnapp.KillGameSelector()
        elif lawnapp.mGameScene == Lawn.GameScenes.Challenge:
            lawnapp.KillChallengeScreen()
        elif lawnapp.mGameScene == Lawn.GameScenes.Award:
            lawnapp.KillAwardScreen()
        # 加载新游戏
        lawnapp.PreNewGame(gamemode, True)
    
    @main_thread  # 必须在主线程运行，不然会有概率崩溃
    def EnterNewGame(self, gamemode: Lawn.GameMode):
        self._EnterNewGame(gamemode)
    
    @main_thread
    def EnterMoonEndless(self):
        # 会覆盖屋顶无尽存档，先检查是否有存档
        lawnapp = GetLawnApp()
        targetGameMode = Lawn.GameMode.SurvivalEndlessStage5
        prevSave = f'docs/userdata/game{lawnapp.mPlayerInfo.mId}_{int(targetGameMode)}.dat'
        if lawnapp.FileExists(prevSave):
            self.ShowErrorInGame('错误！', '该功能会覆盖屋顶无尽存档，请先删除或重命名！二次进入请直接进屋顶无尽')
            return
        self._EnterNewGame(targetGameMode)
        board = lawnapp.mBoard
        # 设置场景
        board.mBackground = Lawn.BackgroundType.Num6Boss
        board.LoadBackgroundImages()
        # 设置关卡数
        board.mChallenge.mSurvivalStage = -1
        # 直接下一关
        board.FadeOutLevel()
    
    @main_thread
    def CheatSetZombies(self, zb_list, internal_spawn: bool = True):  # type: (list[Lawn.ZombieType], bool) -> None
        board = GetBoard()
        if board is None:
            return
        SetZombies(zb_list, internal_spawn)
    
    @main_thread  # 必须在主线程运行，不然会有概率崩溃
    def LineUpOnBoard(self, linup_code_b64: str):
        board = GetBoard()
        if board is None:
            return
        LineUp.from_str(linup_code_b64).to_board(board)
    
    def UnlockCrazyDaveSeed(self):
        if GetBoard() is None:
            return
        lawnApp = GetLawnApp()
        for i in range(60):
            chosenSeed = lawnApp.mSeedChooserScreen.mChosenSeeds[i]
            if chosenSeed is not None:
                chosenSeed.mCrazyDavePicked = False
    
    @main_thread
    def SetAdventureLevel(self, level: int):
        lawnApp = GetLawnApp()
        lawnApp.mPlayerInfo.mLevel = level
        if lawnApp.mGameScene == Lawn.GameScenes.Menu:
            lawnApp.KillGameSelector()
            lawnApp.ShowGameSelector()
    
    @main_thread
    def RemoveTalisman(self):
        board = GetBoard()
        if board is None:
            return
        cheat_option.RemoveGridItemOnBoard(-1, -1, Lawn.GridItemType.Talisman)
        cheat_option.RemoveGridItemOnBoard(-1, -1, Lawn.GridItemType.TalismanMove)
        board.mSealedCountdown = 0
        for plant in IterAlivePlants():
            plant.SetSealing(False)
            plant.mInTalismanCounter = 0

cheat_option = CheatOption()

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

# 无限阳光
def ScriptInfSun():
    GetBoard().mSunMoney = 9990
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

# 技能无冷却
def ScriptKillNoCooling():
    GetBoard().mAgavePowerfulCountdown = 0
    GetBoard().mEndoflamePowerfulCountdown = 0
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

# 显示植物/僵尸血量

def DrawPlantHp(plant: Lawn.Plant, g: Sexy.Graphics, marginX: int, offsetY: int, color1, color2):
    if plant.mPlantHealth < plant.mPlantMaxHealth:
        # 一格80x80，画60x5
        numGrid = 2 if plant.mSeedType == Lawn.SeedType.Cobcannon else 1
        totalWidth = 80 * numGrid - 2 * marginX
        x = plant.mX + marginX + GetBoard().mX
        y = plant.mY + offsetY + GetBoard().mY
        hpWidth = int(totalWidth * plant.mPlantHealth / plant.mPlantMaxHealth)
        g.SetColor(color1)
        g.FillRect(x, y, hpWidth, 5)
        g.SetColor(color2)
        g.FillRect(x + hpWidth, y, totalWidth - hpWidth, 5)

def DrawZombieHp(zombie: Lawn.Zombie, g: Sexy.Graphics, marginX: int, offsetY: int, color1, color2, color3, color4):
    rect = zombie.GetZombieRect()
    totalWidth = rect.mWidth
    x = rect.mX + marginX + GetBoard().mX
    y = rect.mY + offsetY + GetBoard().mY + 20
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
        hpWidth = int(totalWidth * (zombie.mBodyHealth - threshold) / (zombie.mBodyMaxHealth - threshold))
        hpWidth = 0 if hpWidth < 0 else hpWidth
        if zombie.mHasHead:
            plotHp1 = True
    if zombie.mHasHelm and zombie.mHelmHealth < zombie.mHelmMaxHealth:
        if zombie.mZombieType == Lawn.ZombieType.Monk:  # 特殊处理武僧僵尸
            hpWidth2 = int(totalWidth * zombie.mHelmHealth / zombie.mHelmMaxHealth)
            plotHp2 = True
        else:
            hpWidth = int(totalWidth * zombie.mHelmHealth / zombie.mHelmMaxHealth)
            plotHp1 = True
    # 画飞行物
    if zombie.IsFlying() and zombie.mFlyingHealth < zombie.mFlyingMaxHealth:
        hpWidth = int(totalWidth * zombie.mFlyingHealth / zombie.mFlyingMaxHealth)
        plotHp1 = True
    # 如果有铁门、梯子等画下面
    if zombie.mHasShield and zombie.mShieldHealth < zombie.mShieldMaxHealth:
        hpWidth2 = int(totalWidth * zombie.mShieldHealth / zombie.mShieldMaxHealth)
        plotHp2 = True
    # 开始绘制
    if plotHp1:
        g.SetColor(color1)
        g.FillRect(x, y, hpWidth, 5)
        g.SetColor(color2)
        g.FillRect(x + hpWidth, y, totalWidth - hpWidth, 5)
    if plotHp2:
        g.SetColor(color3)
        g.FillRect(x, y + 10, hpWidth2, 5)
        g.SetColor(color4)
        g.FillRect(x + hpWidth2, y + 10, totalWidth - hpWidth2, 5)
    
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

def HookDrawGame(lawnapp: Lawn.LawnApp, g: Sexy.Graphics):
    board = GetBoard()
    if board is not None:
        g.ClearClipRect()  # 否则无法全部画出
        g.SetColorizeImages(True)
        color1 = Sexy.SexyColor(255, 153, 51, 255).Color  # 橙色
        color2 = Sexy.SexyColor(204, 0, 0, 255).Color  # 深红
        color3 = Sexy.SexyColor(102, 204, 0, 255).Color  # 绿色
        color4 = Sexy.SexyColor(0, 153, 153, 255).Color  # 青色
        color5 = Sexy.SexyColor(255, 51, 255, 255).Color
        color6 = Sexy.SexyColor(127, 0, 255, 255).Color
        color7 = Sexy.SexyColor(255, 0, 127, 255).Color
        color8 = Sexy.SexyColor(153, 0, 76, 255).Color
        # 画植物
        if cheat_option.drawPlantHp:
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
        # 画僵尸
        if cheat_option.drawZombieHp:
            for zombie in IterAliveZombies():
                # 只画精英怪
                if cheat_option.selectZombieHp and zombie.mZombieType not in selectZbList:
                    continue
                DrawZombieHp(zombie, g, 0, 0, color5, color6, color7, color8)
        g.SetColorizeImages(False)

@LawnMod.MonoModUtils.HookTo(Lawn.LawnApp.DrawGame)
def LawnApp__DrawGame(orig, self: Lawn.LawnApp, gameTime):
    Sexy.GlobalStaticVars.g.BeginFrame()
    self.mWidgetManager.DrawScreen()
    mDebugScreenEnabled = LawnMod.DynamicHelper.GetPrivateField[System.Boolean](self, 'mDebugScreenEnabled')
    if mDebugScreenEnabled:
        self.DrawDebugInfo(gameTime)
    HookDrawGame(self, Sexy.GlobalStaticVars.g)
    Sexy.GlobalStaticVars.g.EndFrame()
    Sexy.TodLib.FilterEffect.FilterEffectProcessDeleteQueue()

# 连续铲子
@LawnMod.MonoModUtils.HookTo(Lawn.Board.MouseDownWithTool)
def Board__MouseDownWithTool(orig, board: Lawn.Board, x: int, y: int, clickCnt: int, cursorType: Lawn.CursorType, posScaled: bool, isTouch: bool):
    orig(board, x, y, clickCnt, cursorType, posScaled, isTouch)
    if cheat_option.shovelNoReset and clickCnt >= 0 and cursorType == Lawn.CursorType.Shovel:
        board.mCursorObject.mCursorType = Lawn.CursorType.Shovel


# ========== 状态查询（供手机端网页从游戏同步状态） ==========
def get_cheat_state():
    import json
    state = {}
    # 常规选项直接从 cheat_option 属性读取
    regular_attrs = [
        'wontLose', 'freePlant', 'plantAnyWhere', 'zombieNoDie',
        'cobNoCooling', 'potatoNoCooling', 'disableTalisman', 'disableNinja',
        'visibleGhoul', 'noThunder', 'diamondZenTools', 'noFog',
        'transScaryPot', 'conveyorNoCooling', 'featureThreePeater',
        'butterPult', 'doubleGatlingpea', 'fullAreaGloomshroom',
        'enableGlove', 'zombieStop', 'chomperNoCooling', 'noCover',
        'stopSpawning', 'drawPlantHp', 'drawZombieHp', 'selectZombieHp',
        'shovelNoReset', 'runBackground', 'gloveNoCooling', 'plantNoDie',
    ]
    for attr in regular_attrs:
        state[attr] = getattr(cheat_option, attr, False)
    # 特殊选项（状态不在 cheat_option 上）
    state['autoCollect'] = auto_collector.enabled
    state['infSun'] = script_inf_sun.enabled
    state['skillNoCooling'] = script_skill_nocooling.enabled
    state['noCooldown'] = GetLawnApp().mEasyPlantingCheat
    return json.dumps({"action": "sync", "options": state})
