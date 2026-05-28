import Lawn
import Sexy
from .util import IterAlivePlants, RowColToPixel
from .global_var import gvar

def RawFire(cobCannon: Lawn.Plant, row: int, col: float):
    if gvar.opCanceled:
        return
    board = gvar.gboard
    board.RefreshSeedPacketFromCursor()
    x, y = RowColToPixel(board, row, col)
    cobCannon.CobCannonFire(x, y)
    board.RefreshSeedPacketFromCursor()
    Sexy.Debug.Log(f'cob fire {row} {col}')

def GetCobRecoverTime(cobCannon: Lawn.Plant) -> int:
    state = cobCannon.mState
    if state == Lawn.PlantState.CobcannonArming:
        return 125 + cobCannon.mStateCountdown
    elif state == Lawn.PlantState.CobcannonLoading:
        return int(125 * (1 - cobCannon.mBodyReanimID.mAnimRate) + 0.5) + 1
    elif state == Lawn.PlantState.CobcannonReady:
        return 0
    elif state == Lawn.PlantState.CobcannonFiring:
        return 3125 + int(350 * (1 - cobCannon.mBodyReanimID.mAnimRate) + 0.5)
    else:
        raise RuntimeError

class CobManager:
    def __init__(self) -> None:
        self.cobList = []
    
    def GetCobOnBoard(self):
        self.cobList = []
        for plant in IterAlivePlants():
            if plant.mSeedType == Lawn.SeedType.Cobcannon or (plant.mSeedType == Lawn.SeedType.Imitater and plant.mSeedType == Lawn.SeedType.Cobcannon):
                self.cobList.append(plant)

    def _TryFire(self, row: int, col) -> bool:
        for cob in self.cobList:
            recoverTime = GetCobRecoverTime(cob)
            if recoverTime == 0:
                RawFire(cob, row, col)
                return True
        return False

    def Fire(self, *args):
        self.GetCobOnBoard()
        if len(args) == 2 and isinstance(args[0], int):
            self._TryFire(args[0], args[1])
        elif len(args) == 1:
            if len(args[0]) == 2 and isinstance(args[0][0], int):
                self._TryFire(args[0][0], args[0][1])
            else:
                for row, col in args[0]:
                    self._TryFire(row, col)
        else:
            for row, col in args:
                self._TryFire(row, col)
