"""
泳池无尽经典十二炮自动脚本
如果没有摆阵型，本脚本会自动摆阵型，然后跳到4002flags
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

def SetPE12():
    board = GetBoard()
    # 放植物
    plantList = []
    for i in range(3, 5):
        for j in range(1, 9):
            plantList.append((i, j, Lawn.SeedType.Lilypad, True))
    for i in range(3, 5):
        for j in range(1, 9, 2):
            plantList.append((i, j, Lawn.SeedType.Cobcannon, False))
    for i in [1, 2, 5, 6]:
        plantList.append((i, 5, Lawn.SeedType.Cobcannon, False))
    for i, j in [(1, 3), (1, 4), (2, 2), (2, 4)]:
        plantList.append((i, j, Lawn.SeedType.Wintermelon, False))
        plantList.append((7 - i, j, Lawn.SeedType.Wintermelon, False))
    plantList.append((2, 3, Lawn.SeedType.Umbrella, True))
    plantList.append((5, 3, Lawn.SeedType.Umbrella, True))
    plantList.append((1, 2, Lawn.SeedType.Gloomshroom, False))
    plantList.append((6, 2, Lawn.SeedType.Gloomshroom, False))
    plantList.append((1, 2, Lawn.SeedType.InstantCoffee, False))
    plantList.append((6, 2, Lawn.SeedType.InstantCoffee, False))
    for i in [1, 2, 5, 6]:
        for j in range(2, 5):
            plantList.append((i, j, Lawn.SeedType.Pumpkinshell, True))
    SetPlantOnBoard(plantList)
    # 设置阳光
    board.mSunMoney = 8000
    # 等模仿者变身完成再放梯子，不然变身完成后梯子会消失
    yield from Delay(501)
    # 放梯子
    for row in [1, 2, 5, 6]:
        for col in range(2, 5):
            board.AddALadder(col - 1, row - 1)
    # 设置关卡数
    board.mChallenge.mSurvivalStage = 2000
    # 清理僵尸
    for zombie in IterAliveZombies():
        zombie.DieNoLoot(False)
    # 直接下一关
    board.FadeOutLevel()

def HasAliveZombieInFront(wave: int) -> bool:
    for zombie in IterAliveZombies():
        if zombie.mFromWave == wave and zombie.mPosX > 480:
            return True
    return False

def DealDelayCherryPos(wave: int):
    zombieHealthAbove = 0
    zombieHealthBelow = 0
    for zombie in IterAliveZombies():
        if zombie.mFromWave == wave and (zombie.mZombieType != Lawn.ZombieType.Bungee) and (zombie.mRelatedZombieID is None):
            zombieHealth = zombie.mBodyHealth + zombie.mHelmHealth + int(zombie.mShieldHealth * 0.2) + zombie.mFlyingHealth
            if zombie.mRow <= 2:
                zombieHealthAbove += zombieHealth
            else:
                zombieHealthBelow += zombieHealth
    return 2 if zombieHealthAbove > zombieHealthBelow else 5

# 处理偷家气球
def BlowBalloonZombieBehind():
    for zombie in IterAliveZombies():
        if zombie.mZombieType == Lawn.ZombieType.Balloon and zombie.mPosX < 80:
            Card(Lawn.SeedType.Blover, 2, 1)

def RunPE12():
    board = GetBoard()

    # 根据需要设置僵尸列表。第二个参数为True是自然出怪（调用内部出怪函数），由于自然出怪限制可能实际出怪不会包括所有设置的僵尸
    # SetZombies([
    #     Lawn.ZombieType.Gargantuar,
    #     Lawn.ZombieType.RedeyeGargantuar,
    #     Lawn.ZombieType.Polevaulter,
    #     Lawn.ZombieType.Dancer,
    #     Lawn.ZombieType.Zamboni,
    #     Lawn.ZombieType.DolphinRider,
    #     Lawn.ZombieType.Digger,
    #     Lawn.ZombieType.Pogo,
    #     Lawn.ZombieType.Ladder,
    #     Lawn.ZombieType.Catapult,
    #     Lawn.ZombieType.Bungee,
    # ], False)

    # 选卡
    yield from SelectCards([
        Lawn.SeedType.Iceshroom,
        Lawn.SeedType.InstantCoffee,
        Lawn.SeedType.Doomshroom,
        Lawn.SeedType.Lilypad,
        Lawn.SeedType.Cherrybomb,
        Lawn.SeedType.Blover,
        Lawn.SeedType.Kernelpult,
        Lawn.SeedType.Cobcannon,
        Lawn.SeedType.Pumpkinshell,
        Lawn.SeedType.Sunflower,
    ], selectRose=False)

    # 备份存档
    SurvivalBackupGame()

    # 自动吹气球
    script_manager.RunInThread(BlowBalloonZombieBehind)
    
    # 发炮类
    cob_manager = CobManager()

    for wave in range(1, 21):
        # 关底冰消珊瑚
        if wave == 20:
            yield from Prejudge(-300, wave)
            Card(Lawn.SeedType.Iceshroom, 1, 1)
            Card(Lawn.SeedType.InstantCoffee, 1, 1)
        
        # 每关预判
        yield from Prejudge(-199, wave)

        # 关底炮炸珊瑚
        # if wave in (20, ):
        #     yield from Until(-150)
        #     cob_manager.Fire(4, 7)

        # 每波预判炸
        yield from Until(341 - 373)
        cob_manager.Fire((2, 8.8), (5, 8.8))

        # 旗帜波加樱桃消延迟
        if wave in (10, ):
            yield from Until(399 - 100)
            if board.mZombieCountDown > 200 and board.mCurrentWave == wave:
                pos = DealDelayCherryPos(wave - 1)
                Card(Lawn.SeedType.Cherrybomb, pos, 9)

        # 收尾额外多炸两轮
        if wave in (9, 19, 20):
            for _ in range(3):
                yield from DelayA(601)
                # 检查是否存在前场僵尸
                if HasAliveZombieInFront(wave - 1):
                    cob_manager.Fire((2, 8.8), (5, 8.8))
                else:
                    break
        else:
            # 处理延迟
            yield from Until(401)
            if board.mZombieCountDown > 200 and board.mCurrentWave == wave:
                for pos in [3, 4]:
                    for card in [Lawn.SeedType.Lilypad, Lawn.SeedType.Doomshroom, Lawn.SeedType.InstantCoffee]:
                        Card(card, pos, 9)

def ScriptPE12():
    board = GetBoard()
    if board.mPlants.Count == 0:
        # 如果场上没有植物，先设置阵型，然后直接跳下一关
        yield from SetPE12()
    else:
        # 运行十二炮脚本
        yield from RunPE12()

# PE经典十二炮
script_manager.Register(ScriptPE12, gamemode=Lawn.GameMode.SurvivalEndlessStage3)
