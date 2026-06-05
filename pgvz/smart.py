import Lawn
from .util import IterAliveCoins, GetBoard

# 自动收集
# 手机版采用模拟点击方法自动收集会出现一部分区域能自动收集一部分不能，于是改成调用内部函数
def AutoCollect():
    board = GetBoard()
    if board is None:
        return
    for coin in IterAliveCoins():
        # 避免一直点掉落的卡片，真的很吵！
        if coin.mType == Lawn.CoinType.UsableSeedPacket:
            continue
        coin.MouseDown(0, 0, 1)
