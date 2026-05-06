"""
自动通关老虎机
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import LawnMod
import Lawn
import Sexy
from pyvz import *

# 老虎机永远三阳光。必须要用完整的SeedType类型、不能用int。类方法、第一个参数是对象
@LawnMod.MonoModUtils.HookTo(Lawn.SeedPacket.PickNextSlotMachineSeed)
def hook_seedpacket_picknextslotmachineseed(action, seed_packet: Lawn.SeedPacket):
    seed_packet.mSlotMachiningNextSeed = Lawn.SeedType.SlotMachineSun

# 自动转老虎机
def SlotMachinePullHandle():
    board = gvar.gboard
    gameConst = Sexy.Constants
    if board.mChallenge.mChallengeState == Lawn.ChallengeState.Normal:
        handleX = int(gameConst.Challenge_SlotMachineHandle_Pos.mX + 0.5 * gameConst.Challenge_SlotMachineHandle_Pos.mWidth)
        handleY = int(gameConst.Challenge_SlotMachineHandle_Pos.mY + 0.5 * gameConst.Challenge_SlotMachineHandle_Pos.mHeight)
        board.MouseDown(handleX, handleY, 1)

# 老虎机
script_manager.Register(SlotMachinePullHandle, gamemode=Lawn.GameMode.ChallengeSlotMachine)
