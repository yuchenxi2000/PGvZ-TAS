"""
功能和原版修改器PvZ Toolkit的布阵功能一致
布阵码格式 https://github.com/lmintlcx/pvztoolkit/blob/master/docs/rfc1437.txt
"""
import Lawn
import Sexy
import base64
import zlib
from .util import SeedTypeNone

class LineUpGrid:
    def __init__(self) -> None:
        self.hasLadder = False
        self.coffeeImitater = False
        self.hasCoffee = False
        self.pumpkinImitater = False
        self.hasPumpkin = False
        self.underImitater = False
        self.under = 0
        self.plantSleeping = False
        self.plantImitater = False
        self.plantType = -1
    
    @classmethod
    def from_bytes(cls, data1, data2):
        self = cls()
        self.hasLadder = bool(data1 & 0b1)
        self.coffeeImitater = bool((data1 >> 1) & 0b1)
        self.hasCoffee = bool((data1 >> 2) & 0b1)
        self.pumpkinImitater = bool((data1 >> 3) & 0b1)
        self.hasPumpkin = bool((data1 >> 4) & 0b1)
        self.underImitater = bool((data1 >> 5) & 0b1)
        self.under = (data1 >> 6) & 0b11
        self.plantSleeping = not bool(data2 & 0b1)
        self.plantImitater = bool((data2 >> 1) & 0b1)
        self.plantType = (data2 >> 2) - 1
        return self
    
    def to_bytes(self):  # type: (LineUpGrid) -> tuple[int, int]
        data1 = 0
        data2 = 0
        if self.hasLadder:
            data1 |= 0b1
        if self.coffeeImitater:
            data1 |= 0b10
        if self.hasCoffee:
            data1 |= 0b100
        if self.pumpkinImitater:
            data1 |= 0b1000
        if self.hasPumpkin:
            data1 |= 0b10000
        if self.underImitater:
            data1 |= 0b100000
        data1 |= self.under << 6
        if not self.plantSleeping:
            data2 |= 0b1
        if self.plantImitater:
            data2 |= 0b10
        data2 |= (self.plantType + 1) << 2
        return data1, data2
    
    @classmethod
    def from_board(cls, board: Lawn.Board, row: int, col: int):
        self = cls()
        # 支持植物
        if board.GetGraveStoneAt(col, row) is not None:
            self.under = 3
        else:
            underPlant = board.GetTopPlantAt(col, row, Lawn.TopPlant.OnlyUnderPlant)
            if underPlant is None:
                self.under = 0
            else:
                self.underImitater = underPlant.mImitaterType == Lawn.SeedType.Imitater
                underType = int(underPlant.mSeedType)
                self.under = 1 if underType == Lawn.SeedType.Lilypad else 2
        # 植物本体
        plant = board.GetTopPlantAt(col, row, Lawn.TopPlant.OnlyNormalPosition)
        if plant is not None and plant.mPlantCol == col:  # 行数判断是为了防止玉米炮前一格被认为有植物
            self.plantImitater = plant.mImitaterType == Lawn.SeedType.Imitater
            self.plantType = int(plant.mSeedType)
            self.plantSleeping = plant.mIsAsleep
        else:
            self.plantType = -1
        # 南瓜
        pumpkin = board.GetTopPlantAt(col, row, Lawn.TopPlant.OnlyPumpkin)
        self.hasPumpkin = pumpkin is not None
        if self.hasPumpkin:
            self.pumpkinImitater = pumpkin.mImitaterType == Lawn.SeedType.Imitater
        # 咖啡豆
        coffee = board.GetTopPlantAt(col, row, Lawn.TopPlant.OnlyFlying)
        self.hasCoffee = coffee is not None
        if self.hasCoffee:
            self.coffeeImitater = coffee.mImitaterType == Lawn.SeedType.Imitater
        # 梯子
        self.hasLadder = board.GetLadderAt(col, row) is not None
        return self
    
    def to_board(self, board: Lawn.Board, row: int, col: int):
        # 支持植物
        if self.under == 0:
            pass
        elif self.under == 1:
            board.AddPlant(col, row, Lawn.SeedType.Lilypad, Lawn.SeedType.Imitater if self.underImitater else SeedTypeNone)
        elif self.under == 2:
            board.AddPlant(col, row, Lawn.SeedType.Flowerpot, Lawn.SeedType.Imitater if self.underImitater else SeedTypeNone)
        else:
            grave_stone = board.AddAGraveStone(col, row)
            grave_stone.mGridItemCounter = 100  # 否则非存在墓碑场地不更新，墓碑无法钻出
        # 植物本体
        if self.plantType >= 0:
            plant = board.AddPlant(col, row, Lawn.SeedType(self.plantType), Lawn.SeedType.Imitater if self.plantImitater else SeedTypeNone)
            plant.SetSleeping(self.plantSleeping)
            if plant.mSeedType in [Lawn.SeedType.Sunshroom, Lawn.SeedType.Potatomine]:
                plant.mStateCountdown = 0
        # 南瓜
        if self.hasPumpkin:
            board.AddPlant(col, row, Lawn.SeedType.Pumpkinshell, Lawn.SeedType.Imitater if self.pumpkinImitater else SeedTypeNone)
        # 咖啡豆
        if self.hasCoffee:
            board.AddPlant(col, row, Lawn.SeedType.Pumpkinshell, Lawn.SeedType.Imitater if self.coffeeImitater else SeedTypeNone)
        # 梯子
        if self.hasLadder:
            board.AddALadder(col, row)

class LineUp:
    def __init__(self) -> None:
        self.scene = 0
        self.rake_row = -1
        self.rake_col = -1
        self.grids = []  # type: list[LineUpGrid]
    
    @classmethod
    def from_str(cls, lineup_code_b64: str):
        self = cls()
        lineup_code = bytearray(base64.b64decode(lineup_code_b64.encode("utf-8")))
        for i in range(len(lineup_code)):
            lineup_code[i] ^= 0x54
        last = lineup_code[-1]
        self.rake_row = (last >> 4) - 1
        self.rake_col = 7
        self.scene = last & 0xF
        grid_data = zlib.decompress(lineup_code[:-1])
        assert(len(grid_data) % 2 == 0)
        for i in range(0, len(grid_data), 2):
            data1 = grid_data[i]
            data2 = grid_data[i + 1]
            self.grids.append(LineUpGrid.from_bytes(data1, data2))
        return self

    def to_str(self):  # type: () -> str
        last = 0
        last |= (self.rake_row + 1) << 4
        last |= self.scene
        grid_data_list = []
        for grid in self.grids:
            data1, data2 = grid.to_bytes()
            grid_data_list.append(data1)
            grid_data_list.append(data2)
        lineup_code_unmask = zlib.compress(bytes(grid_data_list)) + bytes([last])
        lineup_code = bytes(b ^ 0x54 for b in lineup_code_unmask)
        lineup_code_b64 = base64.b64encode(lineup_code).decode('utf-8')
        return lineup_code_b64
    
    @classmethod
    def from_board(cls, board: Lawn.Board):
        self = cls()
        # 钉耙
        rake = board.GetRake()
        if rake is not None:
            self.rake_row = rake.mGridY
            self.rake_col = rake.mGridX
        else:
            self.rake_row = -1
        # 场景
        self.scene = int(board.mBackground)
        # 格子
        NRow = 6 if board.StageHas6Rows() else 5
        NCol = 9
        for row in range(NRow):
            for col in range(NCol):
                self.grids.append(LineUpGrid.from_board(board, row, col))
        return self
    
    def to_board(self, board: Lawn.Board):
        # 移除已有植物
        for i in range(board.mPlants.Count):
            plant = board.mPlants[i]
            if not plant.mDead:
                plant.Die()
        # 移除已有钉耙和墓碑
        for i in range(board.mGridItems.Count):
            gridItem = board.mGridItems[i]
            if not gridItem.mDead and gridItem.mGridItemType in [Lawn.GridItemType.Rake, Lawn.GridItemType.Gravestone]:
                gridItem.GridItemDie()
        # 根据布阵码放置植物
        # check current background
        background = Lawn.BackgroundType(self.scene)
        currentBackground = board.mBackground
        if currentBackground != background:
            Sexy.Debug.Log(f'error in lineup code: current background is {currentBackground}, but background in code is {background}!')
        for igrid, grid in enumerate(self.grids):
            row = igrid // 9
            col = igrid % 9
            grid.to_board(board, row, col)
        # 钉耙
        if self.rake_row >= 0:
            newGridItem = Lawn.GridItem.GetNewGridItem()
            newGridItem.mGridItemType = Lawn.GridItemType.Rake
            newGridItem.mGridX = self.rake_col
            newGridItem.mGridY = self.rake_row
            newGridItem.mPosX = board.GridToPixelX(newGridItem.mGridX, newGridItem.mGridY)
            newGridItem.mPosY = board.GridToPixelY(newGridItem.mGridX, newGridItem.mGridY)
            newGridItem.mRenderOrder = Lawn.Board.MakeRenderOrder(Lawn.RenderLayer.GraveStone, newGridItem.mGridY, 9)
            board.mGridItems.Add(newGridItem)
            theReanimation = board.CreateRakeReanim(newGridItem.mPosX, newGridItem.mPosY, 0)
            newGridItem.mGridItemReanimID = board.mApp.ReanimationGetID(theReanimation)
            newGridItem.mGridItemState = Lawn.GridItemState.RakeAttracting
