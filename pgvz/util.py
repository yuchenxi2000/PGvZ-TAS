import Lawn
import Sexy
import pathlib

def GetLawnApp() -> Lawn.LawnApp:
    return Sexy.GlobalStaticVars.gLawnApp

def GetBoard() -> Lawn.Board:
    return Sexy.GlobalStaticVars.gLawnApp.mBoard

# 坐标转成行列
def PixelToGrid(board: Lawn.Board, pixel):
    return board.PixelToGridX(*pixel), board.PixelToGridY(*pixel)

# no boundary check
def PixelToGridRaw(board: Lawn.Board, pixel):
    if board.mApp.mGameMode == Lawn.GameMode.ChallengeZenGarden and board.mBackground in (Lawn.BackgroundType.MushroomGarden, Lawn.BackgroundType.Zombiquarium, Lawn.BackgroundType.Greenhouse, Lawn.BackgroundType.GreenhouseNight):
        return board.mApp.mZenGarden.PixelToGridX(*pixel), board.mApp.mZenGarden.PixelToGridY(*pixel)
    theX, theY = pixel
    gridX = (theX - Sexy.Constants.LAWN_XMIN) // 80
    if board.StageHasRoof():
        num2 = 0
        if gridX < 5:
            num2 = (5 - gridX) * 20 - 20
        gridY = (theY - Sexy.Constants.LAWN_YMIN - num2) // 85
    elif board.StageHas6Rows():
        gridY = (theY - Sexy.Constants.LAWN_YMIN) // 85
    else:
        gridY = (theY - Sexy.Constants.LAWN_YMIN) // 100
    return gridX, gridY

# 更安全的版本，原版如果坐标越界会直接崩溃
def SafeGridToPixelY(board, theGridX, theGridY):
    if board.mApp.mGameMode == Lawn.GameMode.ChallengeZenGarden and board.mBackground in (Lawn.BackgroundType.MushroomGarden, Lawn.BackgroundType.Zombiquarium, Lawn.BackgroundType.Greenhouse, Lawn.BackgroundType.GreenhouseNight):
        return board.mApp.mZenGarden.GridToPixelY(theGridX, theGridY)
    if not board.StageHasRoof():
        if not board.StageHas6Rows():
            num = theGridY * Sexy.Constants.New.Board_GridCellSizeY_5Rows + Sexy.Constants.LAWN_YMIN
        else:
            num = theGridY * Sexy.Constants.New.Board_GridCellSizeY_6Rows + Sexy.Constants.LAWN_YMIN
    else:
        num2 = 0
        if theGridX < 5:
            num2 = (5 - theGridX) * 20
        num = theGridY * Sexy.Constants.New.Board_GridCellSizeY_6Rows + Sexy.Constants.LAWN_YMIN + num2 - 10
    if theGridX in range(Sexy.Constants.GRIDSIZEX) and theGridY in range(Sexy.Constants.MAX_GRIDSIZEY) and board.mGridSquareType[theGridX, theGridY] == Lawn.GridSquareType.HighGround:
        num += -Sexy.Constants.HIGH_GROUND_HEIGHT
    return num

# 行列转坐标，得到格子左上角坐标
def GridToPixel(board: Lawn.Board, grid):
    return board.GridToPixelX(*grid), SafeGridToPixelY(board, *grid)

# 得到格子中间坐标（col为浮点数时按比例得到坐标）
def RowColToPixel(board, row, col):  # type: (Lawn.Board, int, int | float) -> tuple[int, int]
    tCol = int(col + 0.5)
    x = int(col * 80.0 + 1e-3)
    y = board.GridToPixelY(tCol - 1, row - 1) + 40
    return x, y

def MouseDragGrid(board: Lawn.Board, grid_from, grid_to):
    pixel_from = GridToPixel(board, grid_from)
    pixel_to = GridToPixel(board, grid_to)
    board.MouseMove(*pixel_from)
    board.MouseDown(*pixel_from, 1)
    board.MouseMove(*pixel_to)
    board.MouseUp(*pixel_to, 1)

# 和Python关键字冲突。用反射绕开
SeedTypeNone: Lawn.SeedType = getattr(Lawn.SeedType, 'None')
PottedPlantNeedNone: Lawn.PottedPlantNeed = getattr(Lawn.PottedPlantNeed, 'None')

def SetPlantOnBoard(plantList: list):
    board = GetBoard()
    # 移除已有植物
    for i in range(board.mPlants.Count):
        plant = board.mPlants[i]
        if not plant.mDead:
            plant.Die()
    # 根据列表放置植物
    for row, col, plant, isImitater in plantList:
        if isImitater:
            board.AddPlant(col - 1, row - 1, Lawn.SeedType.Imitater, plant)
        else:
            board.AddPlant(col - 1, row - 1, plant, SeedTypeNone)

def IterAliveZombies():
    board = GetBoard()
    for i in range(board.mZombies.Count):
        zombie = board.mZombies[i]
        if zombie.mHasHead and not zombie.IsDeadOrDying() and not zombie.mMindControlled:
            yield zombie

def IterAlivePlants():
    board = GetBoard()
    for i in range(board.mPlants.Count):
        plant = board.mPlants[i]
        if not plant.mDead:
            yield plant

def IterAliveCoins():
    board = GetBoard()
    for i in range(board.mCoins.Count):
        coin = board.mCoins[i]
        if not coin.mDead and not coin.mIsBeingCollected:
            yield coin

def IterAliveGridItems():
    board = GetBoard()
    for i in range(board.mGridItems.Count):
        grid_item = board.mGridItems[i]
        if not grid_item.mDead:
            yield grid_item

def SurvivalBackupGame(max_backup: int = 3):
    lawnApp = GetLawnApp()
    board = GetBoard()
    savedGameName = f'docs/userdata/game{lawnApp.mPlayerInfo.mId}_{int(lawnApp.mGameMode)}_{lawnApp.mBoard.mChallenge.mSurvivalStage}.dat'
    board.SaveGame(savedGameName)
    saveToDelete = f'docs/userdata/game{lawnApp.mPlayerInfo.mId}_{int(lawnApp.mGameMode)}_{board.mChallenge.mSurvivalStage - max_backup}.dat'
    saveDir = Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath
    pathSaveToDelete = pathlib.Path(saveDir).joinpath(saveToDelete)
    if pathSaveToDelete.is_file():
        pathSaveToDelete.unlink()
