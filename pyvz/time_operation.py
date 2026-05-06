import Lawn
import Sexy
from .global_var import gvar

def UntilCountDown(t: int, huge_wave: bool):
    board = gvar.gboard
    if not huge_wave:
        while board.mZombieCountDown > t:
            yield
    else:
        while board.mZombieCountDown > 5:
            yield
        while board.mHugeWaveCountDown > t:
            yield

refresh_time = [
    599, 200, 200, 200, 200,
    200, 200, 200, 200, 750,
    200, 200, 200, 200, 200,
    200, 200, 200, 200, 750
]

refresh_point = 0

def Delay(t: int):
    board = gvar.gboard
    prev_time = board.mMainCounter
    while board.mMainCounter - prev_time < t:
        yield
    Sexy.Debug.Log(f"Delay: time = {t}")

def Prejudge(rel_time: int, wave: int):
    global refresh_point
    board = gvar.gboard
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
    Sexy.Debug.Log(f"Prejudge: time = {rel_time} wave = {wave}")
    Sexy.Debug.Log(f"TimeInfo: maincounter = {board.mMainCounter} wave = {board.mCurrentWave} cntdown = {board.mZombieCountDown} hugewavecnt = {board.mHugeWaveCountDown}")

def Until(t: int):
    global refresh_point
    board = gvar.gboard
    yield from Delay(t - (board.mMainCounter - refresh_point))
    Sexy.Debug.Log(f"Until: time = {t}")
    Sexy.Debug.Log(f"TimeInfo: maincounter = {board.mMainCounter} wave = {board.mCurrentWave} cntdown = {board.mZombieCountDown} hugewavecnt = {board.mHugeWaveCountDown}")
