import Lawn
import Sexy
from .util import GridToPixel
from .global_var import gvar

# 种卡
# Lawn.Board.CanPlantAt(int theGridX, int theGridY, SeedType theType, bool aIsMovePlant = false)
# Lawn.SeedPacket.MouseDown(int x, int y, int theClickCount)
# Lawn.Board.MouseDownWithPlant(int x, int y, int theClickCount)
def RawCard(seedpacket: Lawn.SeedPacket, row: int, col) -> bool:
    board = gvar.gboard
    col = int(col + 0.5)
    isImitater = seedpacket.mPacketType == Lawn.SeedType.Imitater
    seedtype = seedpacket.mImitaterType if isImitater else seedpacket.mPacketType
    if board.CanPlantAt(col - 1, row - 1, seedtype, False) == Lawn.PlantingReason.Ok:
        pixel = GridToPixel(board, (col - 1, row - 1))
        seedpacket.MouseDown(*pixel, 1)
        board.MouseUpWithPlant(*pixel, 1)
        board.RefreshSeedPacketFromCursor()
        Sexy.Debug.Log(f'plant seed at {row} {col}, type {seedtype} imitater {isImitater}')
        return True
    return False

def FindSeedPacket(seedtype: Lawn.SeedType, isImitater: bool = False):
    board = gvar.gboard
    seedbank = board.mSeedBank
    for i in range(seedbank.mNumPackets):
        seedpacket = seedbank.mSeedPackets[i]
        if seedpacket.CanPickUp():
            if isImitater:
                if seedpacket.mPacketType == Lawn.SeedType.Imitater and seedpacket.mImitaterType == seedtype:
                    return seedpacket
            else:
                if seedpacket.mPacketType == seedtype:
                    return seedpacket
    return None

def Card(seedtype: Lawn.SeedType, row: int, col, isImitater: bool = False) -> bool:
    seedpacket = FindSeedPacket(seedtype, isImitater=isImitater)
    if seedpacket is not None:
        return RawCard(seedpacket, row, col)
    return False

def Shovel(row: int, col: int, seedtype: Lawn.SeedType = None):  # type: ignore
    board = gvar.gboard
    x = col * 80
    y = board.GridToPixelY(col - 1, row - 1) + 40
    if seedtype == Lawn.SeedType.InstantCoffee:
        y -= 30
    elif seedtype == Lawn.SeedType.Pumpkinshell:
        y += 30
    board.RefreshSeedPacketFromCursor()
    board.MouseDownWithTool(x, y, 1, Lawn.CursorType.Shovel, False, False)
    board.RefreshSeedPacketFromCursor()
    Sexy.Debug.Log(f'shovel plant at {row} {col}, type {seedtype}')

# TODO: unfinished, DO NOT USE
def ChooseSeed(seedtypelist):  # type: (list[Lawn.SeedType]) -> None
    choose_screen = gvar.glawnapp.mSeedChooserScreen
    for i in range(60):
        chosen_seed = choose_screen.mChosenSeeds[i]
        if chosen_seed is None:
            continue
        if chosen_seed.mSeedType in seedtypelist and chosen_seed.mSeedState == Lawn.ChosenSeedState.SEED_IN_CHOOSER:
            choose_screen.ClickedSeedInChooser(chosen_seed)
            Sexy.Debug.Log(f'choose seed success')
