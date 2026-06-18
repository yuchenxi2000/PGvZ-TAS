"""
月夜无尽经典十炮自动脚本
如果没有摆阵型，本脚本会自动摆阵型，然后跳到4002flags
进屋顶无尽关卡，该脚本会自动设置场景为月夜，摆阵型，然后开始自动打无尽
如果你想从头开始手动布阵，请使用修改器的“进入月夜无尽”功能，摆完阵型再使用该脚本
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
from pgvz import *

def SetME10():
    board = GetBoard()
    # 设置场景
    board.mBackground = Lawn.BackgroundType.Num6Boss
    board.LoadBackgroundImages()
    # 放植物
    plantList = []
    for i in range(1, 6):
        for j in range(1, 8):
            plantList.append((i, j, Lawn.SeedType.Flowerpot, True))
    for i in range(1, 6):
        for j in [1, 6]:
            plantList.append((i, j, Lawn.SeedType.Cobcannon, False))
    plantList.append((2, 4, Lawn.SeedType.Umbrella, True))
    plantList.append((5, 4, Lawn.SeedType.Umbrella, True))
    plantList.append((1, 3, Lawn.SeedType.Gloomshroom, False))
    plantList.append((4, 3, Lawn.SeedType.Gloomshroom, False))
    plantList.append((3, 3, Lawn.SeedType.Twinsunflower, False))
    for i in range(1, 6):
        plantList.append((i, 5, Lawn.SeedType.Wintermelon, False))
    for i, j in [(1, 4), (2, 3), (3, 4), (4, 4), (5, 3)]:
        plantList.append((i, j, Lawn.SeedType.Wintermelon, False))
    for i in range(1, 6):
        for j in range(3, 6):
            plantList.append((i, j, Lawn.SeedType.Pumpkinshell, True))
    SetPlantOnBoard(plantList)
    # 设置阳光
    board.mSunMoney = 8000
    # 等模仿者变身完成再放梯子，不然变身完成后梯子会消失
    yield from Delay(501)
    # 放梯子
    for row in range(1, 6):
        for col in range(3, 6):
            board.AddALadder(col - 1, row - 1)
    # 设置关卡数
    board.mChallenge.mSurvivalStage = 2000
    # 清理僵尸
    for zombie in IterAliveZombies():
        zombie.DieNoLoot(False)
    # 直接下一关
    board.FadeOutLevel()

# 处理偷家气球
def BlowBalloonZombieBehind():
    while True:
        hasBalloon = False
        for zombie in IterAliveZombies():
            if zombie.mZombieType == Lawn.ZombieType.Balloon and zombie.mPosX < 80:
                hasBalloon = True
                break
        if hasBalloon:
            Card(Lawn.SeedType.Flowerpot, 5, 9)
            Card(Lawn.SeedType.Blover, 5, 9)
            yield from Delay(100)
            Shovel(5, 9)
        else:
            yield

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
            if zombie.mRow <= 1:
                zombieHealthAbove += zombieHealth
            elif zombie.mRow >= 3:
                zombieHealthBelow += zombieHealth
    return 2 if zombieHealthAbove > zombieHealthBelow else 4

def RunME10():
    board = GetBoard()

    # 选卡
    yield from SelectCards([
        Lawn.SeedType.Iceshroom,
        Lawn.SeedType.Doomshroom,
        Lawn.SeedType.Cherrybomb,
        Lawn.SeedType.Blover,
        Lawn.SeedType.Kernelpult,
        Lawn.SeedType.Cobcannon,
        Lawn.SeedType.Pumpkinshell,
        Lawn.SeedType.Wallnut,
        Lawn.SeedType.Flowerpot,
        Lawn.SeedType.Imitater,
    ], Lawn.SeedType.Flowerpot, selectRose=False)

    # 备份存档
    SurvivalBackupGame()

    # 自动吹气球
    script_manager.RunInThread(BlowBalloonZombieBehind)
    
    # 发炮类
    cob_manager = CobManager()

    for wave in range(1, 21):
        # 关底冰消空降
        if wave == 20:
            yield from Prejudge(-100, wave)
            Card(Lawn.SeedType.Flowerpot, 1, 8)
            Card(Lawn.SeedType.Iceshroom, 1, 8)
            yield from DelayA(100)
            Shovel(1, 8)
        
        # 每关预判
        yield from Prejudge(700 - 200 - 373, wave)

        # 每波预判炸
        cob_manager.Fire((2, 9), (4, 9))

        # 旗帜波加樱桃消延迟
        if wave in (10, ):
            yield from Until(699 - 100)
            if board.mZombieCountDown > 200 and board.mCurrentWave == wave:
                pos = DealDelayCherryPos(wave - 1)
                Card(Lawn.SeedType.Flowerpot, pos, 9)
                Card(Lawn.SeedType.Cherrybomb, pos, 9)
                yield from DelayA(100)
                Shovel(pos, 9)
        
        # 收尾额外多炸两轮
        if wave in (9, 19, 20):
            for _ in range(3):
                yield from DelayA(701)
                # 检查是否存在前场僵尸
                if HasAliveZombieInFront(wave - 1):
                    cob_manager.Fire((2, 9), (4, 9))
                else:
                    break
        else:
            # 处理延迟
            yield from Until(501)
            if board.mZombieCountDown > 200 and board.mCurrentWave == wave:
                for pos in [2, 3]:
                    for card in [Lawn.SeedType.Flowerpot, Lawn.SeedType.Doomshroom]:
                        Card(card, pos, 9)

def ScriptME10():
    # 检查植物是不是只有花盆
    hasOnlyFlowerpot = True
    for plant in IterAlivePlants():
        if plant.mSeedType != Lawn.SeedType.Flowerpot:
            hasOnlyFlowerpot = False
            break
    if hasOnlyFlowerpot:
        # 如果场上没有植物，先设置阵型，然后直接跳下一关
        yield from SetME10()
    else:
        # 运行十二炮脚本
        yield from RunME10()

script_me10 = script_manager.Register(ScriptME10, gamemode=Lawn.GameMode.SurvivalEndlessStage5)
