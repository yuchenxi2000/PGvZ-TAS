import Sexy
from .global_var import gvar
from .util import GetBoard

def UntilCountDown(t: int, huge_wave: bool):
    board = GetBoard()
    if not huge_wave:
        while board.mZombieCountDown > t:
            yield
        timePassed = board.mZombieCountDown < t
    else:
        while board.mZombieCountDown > 5:
            yield
        while board.mHugeWaveCountDown > t:
            yield
        timePassed = board.mHugeWaveCountDown < t
    if timePassed:
        gvar.opCanceled = True
        Sexy.Debug.Log(f'warning: UntilCountDown time has passed!')
    else:
        gvar.opCanceled = False

refresh_time = [
    599, 200, 200, 200, 200,
    200, 200, 200, 200, 750,
    200, 200, 200, 200, 200,
    200, 200, 200, 200, 750
]

refresh_point = 0
prev_until_time = 0

def Delay(t: int):
    board = GetBoard()
    prev_time = board.mMainCounter
    while board.mMainCounter - prev_time < t:
        yield
    if board.mMainCounter - prev_time > t:
        gvar.opCanceled = True
        Sexy.Debug.Log(f'warning: Delay time has passed!')
    else:
        gvar.opCanceled = False
    Sexy.Debug.Log(f"Delay: time = {t}")

def Prejudge(rel_time: int, wave: int):
    global refresh_point
    global prev_until_time
    prev_until_time = rel_time
    board = GetBoard()
    if board.mCurrentWave < wave:
        while board.mCurrentWave < wave - 1:
            yield
        huge_wave = wave == 10 or wave == 20
        yield from UntilCountDown(refresh_time[wave - 1], huge_wave)
        if huge_wave:
            if board.mZombieCountDown in [4, 5]:
                count_down = board.mHugeWaveCountDown
            else:
                count_down = board.mHugeWaveCountDown - 5 + 750
        else:
            count_down = board.mZombieCountDown
        refresh_point = board.mMainCounter + count_down
        yield from Delay(rel_time + count_down)
    elif board.mCurrentWave == wave:
        delta_time = (board.mZombieCountDownStart - board.mZombieCountDown)
        refresh_point = board.mMainCounter - delta_time
        yield from Delay(rel_time - delta_time)
    else:
        gvar.opCanceled = True
        Sexy.Debug.Log(f'warning: Prejudge time has passed!')
    Sexy.Debug.Log(f"Prejudge: time = {rel_time} wave = {wave}")
    Sexy.Debug.Log(f"TimeInfo: maincounter = {board.mMainCounter} wave = {board.mCurrentWave} cntdown = {board.mZombieCountDown} hugewavecnt = {board.mHugeWaveCountDown}")

def Until(t: int):
    global refresh_point
    global prev_until_time
    prev_until_time = t
    board = GetBoard()
    yield from Delay(t - (board.mMainCounter - refresh_point))
    Sexy.Debug.Log(f"Until: time = {t}")
    Sexy.Debug.Log(f"TimeInfo: maincounter = {board.mMainCounter} wave = {board.mCurrentWave} cntdown = {board.mZombieCountDown} hugewavecnt = {board.mHugeWaveCountDown}")

# 在非中途退出重进情形下和Delay行为一致，但之前一定要有Prejudge。
# 退出重进时，该函数能保证行为和非中途退出重进情形一致，但Delay不行，因为Delay等待固定时长，而DelayA等到当前计时器和刷新时间refresh_point相差给定时长，也就是参考点是刷新点
def DelayA(t: int):
    global prev_until_time
    yield from Until(prev_until_time + t)
    Sexy.Debug.Log(f"DelayA: time = {t}")
