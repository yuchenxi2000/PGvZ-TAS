import Lawn
import Sexy
import pathlib

# 坐标转成行列
def PixelToGrid(board: Lawn.Board, pixel):
    return board.PixelToGridX(*pixel), board.PixelToGridY(*pixel)

# 行列转坐标，得到格子左上角坐标
def GridToPixel(board: Lawn.Board, grid):
    return board.GridToPixelX(*grid), board.GridToPixelY(*grid)

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

def SetPlantOnBoard(plantList: list):
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
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
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
    for i in range(board.mZombies.Count):
        zombie = board.mZombies[i]
        if zombie.mHasHead and not zombie.IsDeadOrDying() and not zombie.mMindControlled:
            yield zombie

def IterAlivePlants():
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
    for i in range(board.mPlants.Count):
        plant = board.mPlants[i]
        if not plant.mDead:
            yield plant

def IterAliveCoins():
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
    for i in range(board.mCoins.Count):
        coin = board.mCoins[i]
        if not coin.mDead and not coin.mIsBeingCollected:
            yield coin

def IterAliveGridItems():
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
    for i in range(board.mGridItems.Count):
        grid_item = board.mGridItems[i]
        if not grid_item.mDead:
            yield grid_item

def SurvivalBackupGame(max_backup: int = 3):
    savedGameName = f'docs/userdata/game{Sexy.GlobalStaticVars.gLawnApp.mPlayerInfo.mId}_{int(Sexy.GlobalStaticVars.gLawnApp.mGameMode)}_{Sexy.GlobalStaticVars.gLawnApp.mBoard.mChallenge.mSurvivalStage}.dat'
    Sexy.GlobalStaticVars.gLawnApp.mBoard.SaveGame(savedGameName)
    saveToDelete = f'docs/userdata/game{Sexy.GlobalStaticVars.gLawnApp.mPlayerInfo.mId}_{int(Sexy.GlobalStaticVars.gLawnApp.mGameMode)}_{Sexy.GlobalStaticVars.gLawnApp.mBoard.mChallenge.mSurvivalStage - max_backup}.dat'
    saveDir = Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath
    pathSaveToDelete = pathlib.Path(saveDir).joinpath(saveToDelete)
    if pathSaveToDelete.is_file():
        pathSaveToDelete.unlink()
