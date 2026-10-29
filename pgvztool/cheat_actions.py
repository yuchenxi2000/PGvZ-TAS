"""一次性作弊操作。方法同步执行，调用者必须位于游戏主线程。"""
import System
import Lawn
import Lawn.Creative
import Sexy
from pgvz import *
from pgvz.lineup import LineUp
from .cheat import cheat_option


class CheatActions:
    def __init__(self, options):
        self.options = options

    def _Board(self):
        board = GetBoard()
        if board is None:
            raise RuntimeError('this action requires an active Board')
        return board

    def SetSun(self, value: int):
        self._Board().mSunMoney = value

    def SetMoney(self, value: int):
        GetLawnApp().mPlayerInfo.mCoins = value

    def SetGameMode(self, mode: Lawn.GameMode):
        GetLawnApp().mGameMode = mode

    def SetSurvivalStage(self, value: int):
        self._Board().mChallenge.mSurvivalStage = value

    def GetLineup(self) -> str:
        return LineUp.from_board(self._Board()).to_str()

    def ShowErrorInGame(self, title: str, msg: str):
        lawnapp = GetLawnApp()
        # ID为7的对话框点击ok按钮会直接关闭
        lawnapp.KillDialog(7)
        lawnapp.DoDialog(7, True, title, msg, '好的', 3)

    def ToggleFullscreen(self):
        GetLawnApp().ToggleFullscreen()

    def _WinLevel(self, lawnApp: Lawn.LawnApp, board: Lawn.Board):
        if lawnApp.mSeedChooserScreen is not None:
            # StartLevelIntro 不会清除旧的选卡标志，换轮前必须先结束选卡。
            board.mCutScene.EndSeedChooser()
        if lawnApp.IsSurvivalMode():
            # 地狱生存后两轮波数会变化，按目标 stage 补齐本轮波数。
            board.mNumWaves = board.GetNumWavesPerSurvivalStage()
            board.mCurrentWave = board.mNumWaves
            if board.IsFinalSurvivalStage():
                # 非 Playing 时 FadeOutLevel 直接结束，不会设置此计数器。
                # 结算时保持非负，避免 GetSurvivalFlagsCompleted 少算最后一旗。
                board.mBoardFadeOutCounter = 600
        if not lawnApp.IsIZombieLevel():
            for zombie in IterAliveZombies():
                zombie.DieNoLoot(False)
        lawnApp.KillDialog(19)
        board.FadeOutLevel()

    def WinLevel(self):
        lawnApp = GetLawnApp()
        board = lawnApp.mBoard
        if board is None:
            return
        if lawnApp.IsSurvivalMode():
            creativeLevel = lawnApp.mCreativeLevel
            survival = (creativeLevel.GetComponent[Lawn.Creative.CSSurvivalLevel]()
                        if creativeLevel is not None else None)
            if survival is not None:
                if not survival.mEndless:
                    board.mChallenge.mSurvivalStage = survival.mStages - 1
            elif not lawnApp.IsSurvivalEndless(lawnApp.mGameMode):
                # 普通、困难和地狱生存的终轮均为 stage 4（从 0 开始）。
                board.mChallenge.mSurvivalStage = 4
        self._WinLevel(lawnApp, board)

    def NextStage(self):
        lawnApp = GetLawnApp()
        board = lawnApp.mBoard
        if board is None:
            return
        self._WinLevel(lawnApp, board)

    def LoseLevel(self, zombietype: Lawn.ZombieType = Lawn.ZombieType.Normal):
        lawnApp = GetLawnApp()
        board = lawnApp.mBoard
        if board is None:
            return
        board_EDGE = Sexy.Constants.BOARD_EDGE
        if zombietype in (Lawn.ZombieType.Gargantuar, Lawn.ZombieType.RedeyeGargantuar):
            board_EDGE = Sexy.Constants.BOARD_EDGE - 50
        elif zombietype == Lawn.ZombieType.Polevaulter:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 50
        elif zombietype in (Lawn.ZombieType.Catapult, Lawn.ZombieType.Football, Lawn.ZombieType.Zamboni):
            board_EDGE = Sexy.Constants.BOARD_EDGE - 75
        elif zombietype == Lawn.ZombieType.Zamboni:
            board_EDGE = Sexy.Constants.BOARD_EDGE - 75
        elif zombietype in (Lawn.ZombieType.BackupDancer, Lawn.ZombieType.Dancer, Lawn.ZombieType.Snorkel):
            board_EDGE = Sexy.Constants.BOARD_EDGE - 30
        zombie = board.AddZombie(zombietype, 0)
        zombie.mPosX = board_EDGE
        # 关闭选卡界面，避免失败过场仍可点击图鉴。
        lawnApp.KillSeedChooserScreen()
        # 没有这个会崩溃，因为游戏失败对话和暂停貌似会冲突
        lawnApp.KillDialog(19)
        prevState = self.options.wontLose
        self.options.wontLose = False
        try:
            board.ZombiesWon(zombie)
        finally:
            self.options.wontLose = prevState

    def GivePottedPlant(self, seedtype: Lawn.SeedType, reverse: bool = False):
        zenGarden = GetLawnApp().mZenGarden
        if zenGarden.IsZenGardenFull(False):
            self.ShowErrorInGame('错误！', '你的花园已经满了，请清理一些盆栽，或者移一些到蘑菇园和水族馆后再试！')
            return
        pottedPlant = Lawn.PottedPlant()
        pottedPlant.InitializePottedPlant(seedtype)
        pottedPlant.mPlantAge = Lawn.PottedPlantAge.Full
        pottedPlant.mFacing = Lawn.PottedPlant.FacingDirection.Left if reverse else Lawn.PottedPlant.FacingDirection.Right
        pottedPlant.mPlantNeed = none_of(Lawn.PottedPlantNeed)
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
        pottedPlant.mPlantNeed = none_of(Lawn.PottedPlantNeed)
        pottedPlant.mLastNeedFulfilledTime = System.DateTime.UtcNow
        player.mNumPottedPlants += 1

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
            if seedType in (Lawn.SeedType.Flowerpot, Lawn.SeedType.GiantWallnut, Lawn.SeedType.Sprout, Lawn.SeedType.Leftpeater, Lawn.SeedType.ImitaterRandomPlant, Lawn.SeedType.ImitaterRandomZombie, Lawn.SeedType.HypnoCattail):
                continue
            seedTypeList.append(seedType)
        facingList = (Lawn.PottedPlant.FacingDirection.Right, Lawn.PottedPlant.FacingDirection.Left)
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
        for garden in (Lawn.GardenType.Mushroom, Lawn.GardenType.Mushroom2):
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
        for garden in (Lawn.GardenType.Main, Lawn.GardenType.Main2, Lawn.GardenType.Night):
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

    def _GetTrophy(self, lawnapp: Lawn.LawnApp, playerinfo: Lawn.PlayerInfo, gamemode: Lawn.GameMode, idx: int):
        if lawnapp.IsSurvivalNormal(gamemode):
            if playerinfo.mChallengeRecords[idx] < 5:
                playerinfo.mChallengeRecords[idx] = 5
        elif lawnapp.IsSurvivalHard(gamemode):
            if playerinfo.mChallengeRecords[idx] < 10:
                playerinfo.mChallengeRecords[idx] = 10
        elif lawnapp.IsSurvivalHell(gamemode):
            if playerinfo.mChallengeRecords[idx] < 10:
                playerinfo.mChallengeRecords[idx] = 10
        elif not lawnapp.IsSurvivalEndless(gamemode) and not lawnapp.IsEndlessScaryPotter(gamemode) and not lawnapp.IsEndlessIZombie(gamemode):
            if playerinfo.mChallengeRecords[idx] < 1:
                playerinfo.mChallengeRecords[idx] = 1

    def GetTrophy(self, gamemode: Lawn.GameMode):
        lawnapp = GetLawnApp()
        playerinfo = lawnapp.mPlayerInfo
        idx = int(gamemode) - 1
        # 冒险模式完成次数在另一个地方
        if idx < 0:
            if playerinfo.mFinishedAdventure < 2:
                playerinfo.mFinishedAdventure = 2
            return
        # 获得奖杯
        self._GetTrophy(lawnapp, playerinfo, gamemode, idx)
        # 处于选关卡界面时刷新界面
        if lawnapp.mGameScene == Lawn.GameScenes.Challenge:
            page = lawnapp.mChallengeScreen.mPageIndex
            lawnapp.KillChallengeScreen()
            lawnapp.ShowChallengeScreen(page)

    def _CompleteAccount(self):
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
            # 当前版本无法完成（大泳池的困难和地狱难度）
            if 146 <= gamemode < 148:
                continue
            level = Lawn.GameMode(gamemode)
            self._GetTrophy(lawnapp, playerinfo, level, gamemode - 1)
        # 为了在图鉴里显示红眼巨人
        if playerinfo.mChallengeRecords[12] < 10:
            playerinfo.mChallengeRecords[12] = 10
        store_purchases = [
            (Lawn.StoreItem.STORE_ITEM_PLANT_GATLINGPEA, 1),         # 紫卡：机枪豌豆
            (Lawn.StoreItem.STORE_ITEM_PLANT_TWINSUNFLOWER, 1),      # 紫卡：双子向日葵
            (Lawn.StoreItem.STORE_ITEM_PLANT_GLOOMSHROOM, 1),        # 紫卡：忧郁菇
            (Lawn.StoreItem.STORE_ITEM_PLANT_CATTAIL, 1),            # 紫卡：猫尾草
            (Lawn.StoreItem.STORE_ITEM_PLANT_WINTERMELON, 1),        # 紫卡：冰瓜
            (Lawn.StoreItem.STORE_ITEM_PLANT_GOLD_MAGNET, 1),        # 紫卡：吸金磁
            (Lawn.StoreItem.STORE_ITEM_PLANT_SPIKEROCK, 1),          # 紫卡：地刺王
            (Lawn.StoreItem.STORE_ITEM_PLANT_COBCANNON, 1),          # 紫卡：玉米加农炮
            (Lawn.StoreItem.STORE_ITEM_PLANT_IMITATER, 1),           # 模仿者
            (Lawn.StoreItem.STORE_ITEM_GOLD_WATERINGCAN, 2),         # 花园用具：钻石水壶，购买状态需要填2
            (Lawn.StoreItem.STORE_ITEM_FERTILIZER, 1020),            # 花园用具：花肥
            (Lawn.StoreItem.STORE_ITEM_BUG_SPRAY, 1020),             # 花园用具：杀虫剂
            (Lawn.StoreItem.STORE_ITEM_PHONOGRAPH, 1),               # 花园用具：留声机
            (Lawn.StoreItem.STORE_ITEM_GARDENING_GLOVE, 1),          # 花园用具：园艺手套
            (Lawn.StoreItem.STORE_ITEM_MUSHROOM_GARDEN, 1),          # 花园：蘑菇园
            (Lawn.StoreItem.STORE_ITEM_WHEEL_BARROW, 1),             # 花园用具：手推车
            (Lawn.StoreItem.STORE_ITEM_STINKY_THE_SNAIL, 1),         # 蜗牛
            (Lawn.StoreItem.STORE_ITEM_PACKET_UPGRADE, 4),           # 卡槽
            (Lawn.StoreItem.STORE_ITEM_POOL_CLEANER, 1),             # 泳池割草机
            (Lawn.StoreItem.STORE_ITEM_ROOF_CLEANER, 1),             # 屋顶割草机
            (Lawn.StoreItem.STORE_ITEM_RAKE, 10),                    # 钉耙
            (Lawn.StoreItem.STORE_ITEM_AQUARIUM_GARDEN, 1),          # 花园：水族馆
            (Lawn.StoreItem.STORE_ITEM_CHOCOLATE, 1999),             # 巧克力，最多999
            (Lawn.StoreItem.STORE_ITEM_TREE_OF_WISDOM, 1),           # 智慧树
            (Lawn.StoreItem.STORE_ITEM_TREE_FOOD, 1010),             # 树肥
            (Lawn.StoreItem.STORE_ITEM_FIRSTAID, 1),                 # 坚果急救术
            (Lawn.StoreItem.STORE_ITEM_GARLICFIRSTAID, 1),           # 大蒜急救术
            (Lawn.StoreItem.STORE_ITEM_PLANT_SUPER_CHOMPER, 1),      # 超级大嘴花
            (Lawn.StoreItem.STORE_ITEM_PLANT_PICKLED_PEPPER, 1),     # 泡椒
            (Lawn.StoreItem.STORE_ITEM_PLANT_FIRE_SHROOM, 1),        # 火蘑菇
            (Lawn.StoreItem.STORE_ITEM_PLANT_AGAVE, 1),              # 龙舌兰
            (Lawn.StoreItem.STORE_ITEM_AGAVE_SKILL, 1),              # 龙舌兰技能
            (Lawn.StoreItem.STORE_ITEM_CARD_GROUP_UPGRADE, 4),       # 卡组
            (Lawn.StoreItem.STORE_ITEM_GREENHOUSE_NIGHT, 1),         # 花园：夜晚绿房
            (Lawn.StoreItem.STORE_ITEM_CATTAIL_DRIVER_HYPNO, 1),     # 猫尾草皮肤
            (Lawn.StoreItem.STORE_ITEM_FUMESHROOM_GNOME, 1),         # 菲米爱的互动小屋
        ]
        for store_item, purchase_count in store_purchases:
            playerinfo.mPurchases[int(store_item)] = purchase_count

    def _RefreshAccountDisplay(self):
        lawnapp = GetLawnApp()
        # 刷新显示
        if lawnapp.mGameScene == Lawn.GameScenes.Menu:
            almanac_dialog = lawnapp.GetDialog(3)
            lawnapp.KillGameSelector()
            lawnapp.ShowGameSelector()
            # 图鉴的返回监听器指向旧主菜单，需要改绑并恢复图鉴焦点
            if almanac_dialog is not None:
                almanac_dialog.mListener = lawnapp.mGameSelector  # type: ignore
                lawnapp.mWidgetManager.SetFocus(almanac_dialog)
        elif lawnapp.mGameScene == Lawn.GameScenes.Challenge:
            page = lawnapp.mChallengeScreen.mPageIndex
            lawnapp.KillChallengeScreen()
            lawnapp.ShowChallengeScreen(page)

    def SetTreeHeight(self, height: int):
        lawnapp = GetLawnApp()
        tree_is_open = lawnapp.mGameMode == Lawn.GameMode.TreeOfWisdom and lawnapp.mGameScene == Lawn.GameScenes.Playing
        if tree_is_open:
            # 先移除旧动画；TreeOfWisdomLeave 可能结算正在使用的树肥，必须在写入目标高度前调用。
            lawnapp.mBoard.mChallenge.TreeOfWisdomLeave()
        lawnapp.mPlayerInfo.mChallengeRecords[48] = height
        if tree_is_open:
            lawnapp.mBoard.mChallenge.TreeOfWisdomInit()

    def SetChocolate(self, count: int):
        count = max(0, min(999, int(count)))
        GetLawnApp().mPlayerInfo.mPurchases[int(Lawn.StoreItem.STORE_ITEM_CHOCOLATE)] = 1000 + count

    def CompleteAccount(self):
        self._CompleteAccount()
        self._RefreshAccountDisplay()

    def PerfectAccount(self):
        self._CompleteAccount()
        GetLawnApp().mPlayerInfo.mCoins = 999999
        self.SetTreeHeight(2147483647)
        self.GiveAllPottedPlants()
        self._RefreshAccountDisplay()

    def EnterNewGame(self, gamemode: Lawn.GameMode):
        lawnapp = GetLawnApp()
        if lawnapp.mGameScene == Lawn.GameScenes.Loading:
            return
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

    def EnterMoonEndless(self):
        # 会覆盖屋顶无尽存档，先检查是否有存档
        lawnapp = GetLawnApp()
        targetGameMode = Lawn.GameMode.SurvivalEndlessStage5
        prevSave = f'docs/userdata/game{lawnapp.mPlayerInfo.mId}_{int(targetGameMode)}.dat'
        if lawnapp.FileExists(prevSave):
            self.ShowErrorInGame('错误！', '该功能会覆盖屋顶无尽存档，请先删除或重命名！二次进入请直接进屋顶无尽')
            return
        self.EnterNewGame(targetGameMode)
        board = lawnapp.mBoard
        # 设置场景
        board.mBackground = Lawn.BackgroundType.Num6Boss
        board.LoadBackgroundImages()
        # 设置关卡数
        board.mChallenge.mSurvivalStage = -1
        # 直接下一关
        board.FadeOutLevel()

    def CheatSetZombies(self, zb_list: 'list[Lawn.ZombieType]', internal_spawn: bool = True) -> None:
        board = GetBoard()
        if board is None:
            return
        SetZombies(zb_list, internal_spawn)

    def LineUpOnBoard(self, linup_code_b64: str):
        board = GetBoard()
        if board is None:
            return
        LineUp.from_str(linup_code_b64).to_board(board)

    def SetAdventureLevel(self, level: int):
        lawnApp = GetLawnApp()
        lawnApp.mPlayerInfo.mLevel = level
        if lawnApp.mGameScene == Lawn.GameScenes.Menu:
            lawnApp.KillGameSelector()
            lawnApp.ShowGameSelector()

    def SetFinishedAdventure(self, count: int):
        lawnApp = GetLawnApp()
        lawnApp.mPlayerInfo.mFinishedAdventure = max(0, min(2147483647, int(count)))
        if lawnApp.mGameScene == Lawn.GameScenes.Menu:
            lawnApp.KillGameSelector()
            lawnApp.ShowGameSelector()


cheat_actions = CheatActions(cheat_option)
