"""
宝石迷阵系列自动脚本
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import Lawn
import Sexy
from pgvz import *

# 宝石迷阵自动操作类
class Beghouled:
    def __init__(self):
        self.NRow = 5
        self.NCol = 8
        self.data = [[SeedTypeNone for col in range(self.NCol)] for row in range(self.NRow)]
    
    def Fill(self, board: Lawn.Board):
        for i in range(board.mPlants.Count):
            plant = board.mPlants[i]
            if not plant.mDead:
                self.data[plant.mRow][plant.mPlantCol] = plant.mSeedType
    
    def Twist(self, row: int, col: int):
        tmp = self.data[row][col]
        self.data[row][col] = self.data[row + 1][col]
        self.data[row + 1][col] = self.data[row + 1][col + 1]
        self.data[row + 1][col + 1] = self.data[row][col + 1]
        self.data[row][col + 1] = tmp

    def UnTwist(self, row: int, col: int):
        tmp = self.data[row][col]
        self.data[row][col] = self.data[row][col + 1]
        self.data[row][col + 1] = self.data[row + 1][col + 1]
        self.data[row + 1][col + 1] = self.data[row + 1][col]
        self.data[row + 1][col] = tmp

    def isValid(self, row: int, col: int):
        row_range_begin =  0 if row - 2 < 0 else row - 2
        row_range_end = self.NRow - 2 if row + 2 >= self.NRow else row + 1
        col_range_begin = 0 if col - 2 < 0 else col - 2
        col_range_end = self.NCol - 2 if col + 2 >= self.NCol else col + 1
        for j in range(col_range_begin, col_range_end):
            if self.data[row][j] == self.data[row][j + 1] and self.data[row][j] == self.data[row][j + 2] and self.data[row][j] != SeedTypeNone:
                return True
        for i in range(row_range_begin, row_range_end):
            if self.data[i][col] == self.data[i + 1][col] and self.data[i][col] == self.data[i + 2][col] and self.data[i][col] != SeedTypeNone:
                return True
        return False

    def isValidTwist(self, row: int, col: int):
        row_range_begin = 0 if row - 2 < 0 else row - 2
        row_range_end = self.NRow - 2 if row + 3 >= self.NRow else row + 2
        col_range_begin = 0 if col - 2 < 0 else col - 2
        col_range_end = self.NCol - 2 if col + 3 >= self.NCol else col + 2
        for i in range(row, row + 2):
            for j in range(col_range_begin, col_range_end):
                if self.data[i][j] == self.data[i][j + 1] and self.data[i][j] == self.data[i][j + 2] and self.data[i][j] != SeedTypeNone:
                    return True
        for i in range(row_range_begin, row_range_end):
            for j in range(col, col + 2):
                if self.data[i][j] == self.data[i + 1][j] and self.data[i][j] == self.data[i + 2][j] and self.data[i][j] != SeedTypeNone:
                    return True
        return False
    
    def doValidMove(self, board: Lawn.Board):
        # col direction
        for i in range(self.NRow):
            for j in range(self.NCol - 1):
                tmp = self.data[i][j]
                self.data[i][j] = self.data[i][j + 1]
                self.data[i][j + 1] = tmp
                if self.isValid(i, j) or self.isValid(i, j + 1):
                    MouseDragGrid(board, (j, i), (j + 1, i))
                    return
                self.data[i][j + 1] = self.data[i][j]
                self.data[i][j] = tmp
        # row direction
        for i in range(self.NRow - 1):
            for j in range(self.NCol):
                tmp = self.data[i][j]
                self.data[i][j] = self.data[i + 1][j]
                self.data[i + 1][j] = tmp
                if self.isValid(i, j) or self.isValid(i + 1, j):
                    MouseDragGrid(board, (j, i), (j, i + 1))
                    return
                self.data[i + 1][j] = self.data[i][j]
                self.data[i][j] = tmp
    
    def doValidTwist(self, board: Lawn.Board):
        for i in range(self.NRow - 1):
            for j in range(self.NCol - 1):
                self.Twist(i, j)
                if self.isValidTwist(i, j):
                    pixel = GridToPixel(board, (j + 1, i + 1))
                    board.MouseDown(*pixel, 1)
                    return
                self.UnTwist(i, j)


beghouled = Beghouled()
# 宝石迷阵升级植物
def BeghouledUpgradePlant():
    Card(Lawn.SeedType.Repeater, 1, 9)
    Card(Lawn.SeedType.Fumeshroom, 1, 9)
    Card(Lawn.SeedType.Tallnut, 1, 9)

def ScriptBeghouledTwist():
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
    BeghouledUpgradePlant()
    beghouled.Fill(board)
    beghouled.doValidTwist(board)

def ScriptBeghouled():
    board = Sexy.GlobalStaticVars.gLawnApp.mBoard
    BeghouledUpgradePlant()
    beghouled.Fill(board)
    beghouled.doValidMove(board)

# 宝石迷阵
script_manager.Register(ScriptBeghouled, gamemode=Lawn.GameMode.ChallengeBeghouled)
# 宝石迷阵旋风
script_manager.Register(ScriptBeghouledTwist, gamemode=Lawn.GameMode.ChallengeBeghouledTwist)
