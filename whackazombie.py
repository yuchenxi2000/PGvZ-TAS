"""
自动锤僵尸
"""
import sys
import System
import System.IO
# 貌似手机版不需要设置路径也能正常运行，但这里还是加上以防万一
# Android: IronPython库在 CurrentDirectory/IronPython/Libs
pyLibPath = System.IO.Path.Combine(System.Environment.CurrentDirectory, 'IronPython', 'Libs')
if not System.IO.Directory.Exists(pyLibPath):
    # Windows: IronPython库在游戏主程序同目录下的lib
    pyLibPath = System.IO.Path.Combine(System.IO.Path.GetDirectoryName(System.Environment.ProcessPath), 'lib')
modsDirPath = System.IO.Path.Combine(System.Environment.CurrentDirectory, 'mods')
sys.path.append(pyLibPath)
sys.path.append(modsDirPath)

import Lawn
import Sexy
from pgvz import *

# 自动锤僵尸
def WhackZombie():
    board = GetBoard()
    for zombie in IterAliveZombies():
        if zombie.mPhaseCounter <= 19:
            posX = zombie.mPosX + 0.5 * zombie.mZombieRect.mWidth
            posY = zombie.mPosY + 0.5 * zombie.mZombieRect.mHeight
            board.MouseDown(int(posX), int(posY), 1)
    grave_list = []
    for i in range(board.mGridItems.Count):
        griditem = board.mGridItems[i]
        if griditem.mGridItemType == Lawn.GridItemType.Gravestone:
            grave_list.append((griditem.mGridX, griditem.mGridY))
    grave_list.sort(key=lambda grid: grid[0])
    if len(grave_list) > 0:
        Card(Lawn.SeedType.Gravebuster, grave_list[0][1] + 1, grave_list[0][0] + 1)

# 锤僵尸
script_manager.Register(WhackZombie, gamemode=Lawn.GameMode.ChallengeWhackAZombie)
