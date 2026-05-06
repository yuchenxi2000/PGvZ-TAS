"""
暴风雨夜移除打雷特效
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import LawnMod
import Lawn
import Sexy

# 暴风雨防瞎眼
@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.DrawStormNight)
def hook_challenge_drawstormnight(action, challenge: Lawn.Challenge, graphics: Sexy.Graphics):
    pass

@LawnMod.MonoModUtils.HookTo(Lawn.Challenge.IsStormyNightPitchBlack)
def hook_challenge_IsStormyNightPitchBlack(action, challenge: Lawn.Challenge):
    return False
