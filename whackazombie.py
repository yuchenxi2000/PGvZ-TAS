"""
自动锤僵尸
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import Lawn
import Sexy
from pgvz import *

# 自动锤僵尸
def WhackZombie():
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
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
