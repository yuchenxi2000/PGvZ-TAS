"""
隐形僵尸显形
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import LawnMod
import Lawn
import Sexy

# 隐形僵尸显形。mApp是抽象类GameObject的成员、Zombie继承GameObject、要访问mApp只需任何一个对象.mApp
# 显形方法还是偷偷把关卡ID换成其他的。主要是这样不用写一大堆代码
@LawnMod.MonoModUtils.HookTo(Lawn.Zombie.Draw)
def hook_zombie_draw(action, zombie: Lawn.Zombie, graphics: Sexy.Graphics):
    mApp = zombie.mApp
    level_is_invisighoul = (mApp.mGameMode == Lawn.GameMode.ChallengeInvisighoul)
    if level_is_invisighoul:
        mApp.mGameMode = Lawn.GameMode.ChallengeBobsledBonanza
    action(zombie, graphics)
    if level_is_invisighoul:
        mApp.mGameMode = Lawn.GameMode.ChallengeInvisighoul
