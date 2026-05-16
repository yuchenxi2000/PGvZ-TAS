import Lawn
import Sexy
from .util import IterAliveCoins
from .global_var import gvar

# 自动收集
def AutoCollect():
    board = gvar.gboard
    if board is None:
        return
    num3 = 30 if gvar.glawnapp.IsWhackAZombieLevel() else 0
    cursor_obj = board.mCursorObject.mCursorType
    if cursor_obj == Lawn.CursorType.Normal or cursor_obj == Lawn.CursorType.Hammer:
        for coin in IterAliveCoins():
            # 避免一直点掉落的卡片，真的很吵！
            if coin.mType == Lawn.CoinType.UsableSeedPacket:
                continue
            # 计算点击位置，根据Lawn.Coin.MouseHitTest
            num = -60 if coin.mType == Lawn.CoinType.AwardPresent or coin.IsPresentWithAdvice() or coin.mType == Lawn.CoinType.PresentPlant else 0
            mX = coin.mPosX + coin.mWidth / Sexy.Constants.BoardCameraScaleMultiplier / 2.0
            mY = coin.mPosY + coin.mHeight / Sexy.Constants.BoardCameraScaleMultiplier / 2.0 + num + num3 / 2.0
            board.RefreshSeedPacketFromCursor()
            board.MouseDown(int(mX), int(mY), 1)
            if board is not None:
                board.RefreshSeedPacketFromCursor()
            return
