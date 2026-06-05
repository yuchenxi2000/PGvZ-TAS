"""
自动通关老虎机
理论上只需要转出四个三阳光便可通关
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

import LawnMod
import Lawn
import Sexy
from pgvz import *

# 老虎机永远三阳光。必须要用完整的SeedType类型、不能用int。类方法、第一个参数是对象
# 理论上可以通过操纵随机数，或者凭运气达到同样的效果，这里就直接设置卡片了
@LawnMod.MonoModUtils.HookTo(Lawn.SeedPacket.PickNextSlotMachineSeed)
def hook_seedpacket_picknextslotmachineseed(action, seed_packet: Lawn.SeedPacket):
    seed_packet.mSlotMachiningNextSeed = Lawn.SeedType.SlotMachineSun

# 自动转老虎机
def SlotMachinePullHandle():
    board = GetBoard()
    gameConst = Sexy.Constants
    if board.mChallenge.mChallengeState == Lawn.ChallengeState.Normal:
        handleX = int(gameConst.Challenge_SlotMachineHandle_Pos.mX + 0.5 * gameConst.Challenge_SlotMachineHandle_Pos.mWidth)
        handleY = int(gameConst.Challenge_SlotMachineHandle_Pos.mY + 0.5 * gameConst.Challenge_SlotMachineHandle_Pos.mHeight)
        board.MouseDown(handleX, handleY, 1)

# 老虎机
script_manager.Register(SlotMachinePullHandle, gamemode=Lawn.GameMode.ChallengeSlotMachine)
