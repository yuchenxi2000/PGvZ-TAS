"""
场地放置 — 植物、僵尸、场地物品、掉落物的放置与移除
同时提供轻松放置功能（游戏内点击场地直接放置）
"""
import Lawn
import Sexy
from enum import Enum
from pgvz import *
from .util import main_thread

def IterPortals(board: Lawn.Board):
    for i in range(board.mGridItems.Count):
        gridItem = board.mGridItems[i]
        if not gridItem.mDead and gridItem.mGridItemState != Lawn.GridItemState.PortalClosed and gridItem.mGridItemType in (Lawn.GridItemType.PortalCircle, Lawn.GridItemType.PortalSquare):
            yield gridItem

class PortalPlacer:
    class PortalPlacerState(Enum):
        Normal = 0
        Selected = 1

    def __init__(self):
        self.place_grid_pos = (0, 0)
        self.select_portal_rect = Sexy.TRect(0, 0, 1, 1)
        self.state = self.PortalPlacerState.Normal
    
    def try_place(self, board: Lawn.Board, x: int, y: int):
        if self.state == self.PortalPlacerState.Selected:
            col, row = PixelToGridRaw(board, (x, y))
            if self.place_grid_pos == (col, row):
                self.state = self.PortalPlacerState.Normal
                return
            for portal in IterPortals(board):
                if portal.mGridX == self.place_grid_pos[0] and portal.mGridY == self.place_grid_pos[1]:
                    portal.mGridX = col
                    portal.mGridY = row
                    portal.OpenPortal()
                    self.state = self.PortalPlacerState.Normal
                    return
        else:
            for portal in IterPortals(board):
                mX, mY = GridToPixel(board, (portal.mGridX, portal.mGridY))
                rect = Sexy.TRect(mX, mY, 80, 100)
                if rect.Contains(x, y):
                    self.select_portal_rect = rect
                    self.place_grid_pos = (portal.mGridX, portal.mGridY)
                    self.state = self.PortalPlacerState.Selected
                    return
    
    def isSelected(self):
        return self.state == self.PortalPlacerState.Selected

    def reset(self):
        self.state = self.PortalPlacerState.Normal

class Placer:
    def __init__(self):
        # 轻松放置状态
        self.easyPlaceEnabled = True
        self._active = True
        self.easyPlaceMode = 'plant'
        self.seedType = Lawn.SeedType.Peashooter
        self.zombieType = Lawn.ZombieType.Normal
        self.gridItemType = Lawn.GridItemType.Ladder
        self.coinType = Lawn.CoinType.Silver
        self.mindCtrl = False
        self.potReverse = False
        self.imitater = False
        self._ep_rect = Sexy.TRect(0, 0, 0, 0)
        self.portal_placer = PortalPlacer()
    
    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, value):
        self._active = value
        if not value:
            placer.portal_placer.reset()

    def SetEasyPlaceMode(self, mode):
        self.easyPlaceMode = mode

    def toggle(self):
        self.active = not self.active

    def try_place(self, board: Lawn.Board, x: int, y: int):
        """轻松放置：根据当前模式放置"""
        col, row = PixelToGrid(board, (x, y))
        NRow = 6 if board.StageHas6Rows() else 5
        NCol = 9
        if col < 0 or col >= NCol or row < 0 or row >= NRow:
            return False
        if self.easyPlaceMode != 'portal':
            self.portal_placer.reset()
        if self.easyPlaceMode == 'plant':
            self.PlantOnBoard(row, col, self.seedType, self.imitater)
            return True
        elif self.easyPlaceMode == 'zombie':
            self._ZombieOnBoard(row, col, x, self.zombieType, mind_ctrl=self.mindCtrl, easy_place=True)
            return True
        elif self.easyPlaceMode == 'griditem':
            self.AddGridItemOnBoard(row, col, self.gridItemType)
            return True
        elif self.easyPlaceMode == 'coin':
            self.AddCoinOnBoard(x, y, self.coinType, self.seedType, self.potReverse)
            return True
        elif self.easyPlaceMode == 'mower':
            self._AddLawnMower(board.PixelToGridY(x, y), x)
            return True
        elif self.easyPlaceMode == 'portal':
            self.portal_placer.try_place(board, x, y)
            return True
        return False

    # ===== 以下为网页直接调用的放置/移除方法 =====

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

    def _ZombieOnBoard(self, row: int, col: int, x: int, zombietype: Lawn.ZombieType, mind_ctrl: bool = False, easy_place: bool = False):
        board = GetBoard()
        curwave = board.mCurrentWave
        zombie = board.AddZombieInRow(zombietype, row, curwave)
        if easy_place:
            rect = zombie.mZombieRect
            posX = x - rect.mWidth // 2
        else:
            posX = x
        offsetX = posX - zombie.mPosX
        zombie.mPosX = posX
        zombie.mPosY = zombie.GetPosYBasedOnRow(row)
        zombie.mMindControlled = mind_ctrl
        if zombietype == Lawn.ZombieType.Bungee:
            zombie.mTargetCol = col
            zombie.SetRow(row)
            zombie.mPosX = board.GridToPixelX(col, row)
            zombie.mPosY = zombie.GetPosYBasedOnRow(row)
            zombie.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, row, 7)
        elif zombietype == Lawn.ZombieType.Bobsled:
            # 找到其他三个人
            for iz in range(zombie.mFollowerZombieID.Count):
                zombieFollower = zombie.mFollowerZombieID[iz]
                if zombieFollower is None:
                    continue
                zombieFollower.mPosX += offsetX
                zombieFollower.mPosY = zombieFollower.GetPosYBasedOnRow(row)
                zombieFollower.mMindControlled = mind_ctrl

    @main_thread
    def ZombieOnBoard(self, row: int, col: int, zombietype: Lawn.ZombieType, mind_ctrl: bool = False):
        board = GetBoard()
        if board is None:
            return
        row_range, col_range = self.ConvertRange(row, col)
        for row1 in row_range:
            for col1 in col_range:
                xi = board.GridToPixelX(col1, row1)
                self._ZombieOnBoard(row1, col1, xi, zombietype, mind_ctrl)

    @main_thread
    def RemoveZombieOnBoard(self):
        board = GetBoard()
        if GetBoard() is None:
            return
        for i in range(board.mZombies.Count):
            zombie = board.mZombies[i]
            if zombie.mHasHead and not zombie.IsDeadOrDying():
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
                elif gridItemType in (Lawn.GridItemType.PortalCircle, Lawn.GridItemType.PortalSquare):
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
        if gridItemType == Lawn.GridItemType.Crater and lawnApp.mGameMode in (Lawn.GameMode.ChallengeBeghouled, Lawn.GameMode.ChallengeBeghouledTwist):
            challenge = board.mChallenge
            challenge.BeghouledClearCrater(40)
            challenge.BeghouledStartFalling(Lawn.ChallengeState.BeghouledFalling)
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
    def RemoveTalisman(self):
        board = GetBoard()
        if board is None:
            return
        self.RemoveGridItemOnBoard(-1, -1, Lawn.GridItemType.Talisman)
        self.RemoveGridItemOnBoard(-1, -1, Lawn.GridItemType.TalismanMove)
        board.mSealedCountdown = 0
        for plant in IterAlivePlants():
            plant.SetSealing(False)
            plant.mInTalismanCounter = 0
    
    @main_thread
    def OpenScaryPotterOnBoard(self):
        board = GetBoard()
        if board is None:
            return
        for griditem in IterAliveGridItems():
            if griditem.mGridItemType == Lawn.GridItemType.ScaryPot:
                board.mChallenge.ScaryPotterOpenPot(griditem)

    def _AddLawnMower(self, row: int, x: int):
        board = GetBoard()
        mower = Lawn.LawnMower.GetNewLawnMower()
        mower.LawnMowerInitialize(row)
        mower.mMowerState = Lawn.LawnMowerState.Ready
        offsetY = 35 if board.StageHasRoof() else 0
        mower.mPosX = x
        mower.mPosY = board.GetPosYBasedOnRow(mower.mPosX + 40, row) + 23 + offsetY
        board.mLawnMowers.Add(mower)

    def AddLawnMower(self):
        board = GetBoard()
        if board is None:
            return
        NRow = 6 if board.StageHas6Rows() else 5
        for row in range(NRow):
            self._AddLawnMower(row, Sexy.Constants.BOARD_EXTRA_ROOM - 21)
    
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

placer = Placer()

# 离开战斗界面重置状态
def ScriptResetEasyPlacerState():
    if GetLawnApp().mGameScene != Lawn.GameScenes.Playing:
        placer.active = False
script_manager.Register(ScriptResetEasyPlacerState, runmode=ScriptRunMode.GLOBAL)
