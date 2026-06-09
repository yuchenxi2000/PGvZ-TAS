import Lawn
import Sexy
from .util import RowColToPixel, SeedTypeNone, GetBoard, GetLawnApp
from .global_var import gvar

# 种卡
# Lawn.Board.CanPlantAt(int theGridX, int theGridY, SeedType theType, bool aIsMovePlant = false)
# Lawn.SeedPacket.MouseDown(int x, int y, int theClickCount)
# Lawn.Board.MouseDownWithPlant(int x, int y, int theClickCount)
def RawCard(seedpacket: Lawn.SeedPacket, row: int, col) -> bool:
    if gvar.opCanceled:
        return False
    board = GetBoard()
    isImitater = seedpacket.mPacketType == Lawn.SeedType.Imitater
    seedtype = seedpacket.mImitaterType if isImitater else seedpacket.mPacketType
    if board.CanPlantAt(col - 1, row - 1, seedtype, False) == Lawn.PlantingReason.Ok:
        pixel = RowColToPixel(board, row, col)
        seedpacket.MouseDown(*pixel, 1)
        board.MouseUpWithPlant(*pixel, 1)
        board.RefreshSeedPacketFromCursor()
        Sexy.Debug.Log(f'plant seed at {row} {col}, type {seedtype} imitater {isImitater}')
        return True
    return False

def FindSeedPacket(seedtype: Lawn.SeedType, isImitater: bool = False):
    board = GetBoard()
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
    if gvar.opCanceled:
        return
    board = GetBoard()
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

def LetsRock():
    seedChooserScreen = GetLawnApp().mSeedChooserScreen
    if seedChooserScreen is None:
        raise StopIteration
    while seedChooserScreen.mSeedsInFlight > 0 \
        or seedChooserScreen.mChooseState == Lawn.SeedChooserState.ViewLawn \
            or seedChooserScreen.mSeedsInBank < GetBoard().mSeedBank.mNumPackets:
        yield
    seedChooserScreen.CloseSeedChooser()

def SelectCards(seedList: list, *args, waitTime: int = 200, selectRose: bool = True):
    # imitater type
    if len(args) == 0:
        imitaterType = SeedTypeNone
    if len(args) == 1:
        imitaterType = args[0]
    elif len(args) >= 2:
        Sexy.Debug.Log(f'SelectCards: argument error')
        raise StopIteration
    # return if can't choose seeds
    if not GetBoard().ChooseSeedsOnCurrentLevel():
        raise StopIteration
    # cannot choose seed in fight
    if GetLawnApp().mGameScene != Lawn.GameScenes.LevelIntro:
        raise StopIteration
    seedChooserScreen = GetLawnApp().mSeedChooserScreen
    # wait until chooser screen appears
    while not seedChooserScreen.mMouseVisible:
        yield
    # rose (rake)
    if not seedChooserScreen.mRoseButton.mDisabled and selectRose != seedChooserScreen.mRoseButton.mChecked:
        seedChooserScreen.ButtonDepress(111)
    # find seed position
    seedsToChoose = []  # type: list[Lawn.SeedType]
    seedsToKeep = []  # type: list[Lawn.SeedType]
    for seedtype in seedList:
        chosenSeed = seedChooserScreen.mChosenSeeds[int(seedtype)]
        if chosenSeed.mSeedState in (Lawn.ChosenSeedState.SEED_IN_CHOOSER, Lawn.ChosenSeedState.SEED_FLYING_TO_CHOOSER):
            seedsToChoose.append(seedtype)
        elif chosenSeed.mSeedState in (Lawn.ChosenSeedState.SEED_IN_BANK, Lawn.ChosenSeedState.SEED_FLYING_TO_BANK):
            if seedtype == Lawn.SeedType.Imitater and chosenSeed.mImitaterType != imitaterType:
                seedsToChoose.append(seedtype)
            else:
                seedsToKeep.append(seedtype)
        elif seedtype == Lawn.SeedType.Imitater:
            seedsToChoose.append(seedtype)
        else:
            Sexy.Debug.Log(f'SelectCards: cannot choose seed {seedtype}!')
    # drop seeds in bank but not in list
    for i in range(54):
        chosenSeed = seedChooserScreen.mChosenSeeds[i]
        seedtype = Lawn.SeedType(i)
        if chosenSeed.mSeedState in (Lawn.ChosenSeedState.SEED_IN_BANK, Lawn.ChosenSeedState.SEED_FLYING_TO_BANK):
            if seedtype in seedsToKeep:
                continue
            while seedChooserScreen.mSeedsInFlight > 0:
                yield
            Sexy.Debug.Log(f'drop {seedtype}')
            seedChooserScreen.ClickedSeedInBank(chosenSeed)
    # choose seeds in list but not in bank
    for seedtype in seedsToChoose:
        chosenSeed = seedChooserScreen.mChosenSeeds[int(seedtype)]
        while seedChooserScreen.mSeedsInFlight > 0:
            yield
        Sexy.Debug.Log(f'choose {seedtype}')
        if chosenSeed.mSeedType == Lawn.SeedType.Imitater:
            chosenSeed.mSeedState = Lawn.ChosenSeedState.SEED_IN_CHOOSER
            chosenSeed.mImitaterType = imitaterType
            chosenSeed.mX, chosenSeed.mY = seedChooserScreen.GetSeedPositionInChooser(53, chosenSeed.mX, chosenSeed.mY)  # type: ignore
            seedChooserScreen.ClickedSeedInChooser(chosenSeed)
            seedChooserScreen.UpdateImitaterButton()
        else:
            seedChooserScreen.ClickedSeedInChooser(chosenSeed)
            # 什么乱七八糟的不推荐变灰植物来挡我视线，西内
            if GetLawnApp().GetDialog(16) is not None:
                GetLawnApp().KillDialog(16)
                seedChooserScreen.ClickedSeedInChooser(chosenSeed)
    # 等待一段时间，然后开始游戏
    for _ in range(waitTime):
        if GetLawnApp().mGameScene != Lawn.GameScenes.Playing:
            yield
    # 开始游戏
    yield from LetsRock()
