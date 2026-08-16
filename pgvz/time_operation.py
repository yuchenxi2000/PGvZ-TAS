import Lawn
import Sexy
from .global_var import gvar
from .util import GetBoard, GetLawnApp


# Board.UpdateZombieSpawning 将普通波的倒计时压到该值后，不会再次提前刷新。
# 这是标准刷新策略的规则，不是逐波的波长表。
STANDARD_REFRESH_COUNTDOWN = 200


def _UsesStandardZombieSpawning() -> bool:
    app = GetLawnApp()
    if app.IsWhackAZombieLevel() or app.IsFinalBossLevel():
        return False
    if app.mGameMode in (
        Lawn.GameMode.ChallengeIce,
        Lawn.GameMode.ChallengeZenGarden,
        Lawn.GameMode.TreeOfWisdom,
        Lawn.GameMode.ChallengeZombiquarium,
    ):
        return False
    if app.IsIZombieLevel() or app.IsSquirrelLevel() or app.IsScaryPotterLevel():
        return False
    return True


class WaveClock:
    def __init__(self) -> None:
        self._games = {}

    def _GameKey(self, board: Lawn.Board):
        return (
            board.mGameID,
            int(GetLawnApp().mGameMode),
            board.mLevel,
            board.mBoardRandSeed,
            board.mChallenge.mSurvivalStage,
        )

    def _State(self, board: Lawn.Board):
        key = self._GameKey(board)
        if key not in self._games:
            self._games[key] = {
                'thresholds': {},
                'refresh_points': {},
            }
        return self._games[key]

    def Snapshot(self, board: Lawn.Board):
        return (
            self._GameKey(board),
            board.mMainCounter,
            board.mCurrentWave,
            board.mZombieCountDown,
            board.mHugeWaveCountDown,
        )

    def _RecordThreshold(self, board: Lawn.Board, wave: int,
                         remaining: int, source: str) -> None:
        self._State(board)['thresholds'][wave] = (
            board.mMainCounter,
            remaining,
            source,
        )

    def ObserveUpdate(self, board: Lawn.Board, snapshot) -> None:
        if not _UsesStandardZombieSpawning():
            return

        (
            before_key,
            before_main,
            before_wave,
            before_count_down,
            before_huge,
        ) = snapshot
        if before_key != self._GameKey(board):
            return

        state = self._State(board)

        # SpawnZombieWave 会增加 mCurrentWave；以这一帧的主计数器记录真实刷新点。
        if board.mCurrentWave > before_wave:
            for wave in range(before_wave + 1, board.mCurrentWave + 1):
                state['refresh_points'][wave] = board.mMainCounter
            return

        if board.mCurrentWave < before_wave or board.mMainCounter < before_main:
            state['thresholds'].clear()
            state['refresh_points'].clear()
            return

        wave = board.mCurrentWave + 1
        if wave < 1 or wave > board.mNumWaves:
            return

        # 只有实际进入 Playing/标准刷新流程时 mMainCounter 和倒计时才会同步前进。
        elapsed = board.mMainCounter - before_main
        if elapsed <= 0:
            return

        huge_wave = board.IsFlagWave(wave - 1)
        if huge_wave:
            huge_started = before_huge <= 0 and board.mHugeWaveCountDown > 0
            huge_advanced = (
                before_huge > 0
                and board.mHugeWaveCountDown == before_huge - elapsed
            )
            if huge_started or huge_advanced:
                self._RecordThreshold(
                    board, wave, board.mHugeWaveCountDown, 'huge_wave')
            return

        expected_count_down = before_count_down - elapsed

        # 首波没有上一波血量阈值。第一次观察到标准倒计时实际前进时，
        # 直接以游戏当前的倒计时建立锚点，避免固定使用无尽模式的 599。
        if wave == 1 and board.mZombieHealthToNextWave == -1:
            if board.mZombieCountDown == expected_count_down:
                if wave not in state['thresholds']:
                    self._RecordThreshold(
                        board, wave, board.mZombieCountDown, 'first_wave')
            return

        # 血量刷新阈值会令倒计时发生非线性下降；如果没有发生跳变，
        # 自然倒数到 200 时也已经进入不会再次提前刷新的区间。
        threshold_triggered = board.mZombieCountDown < expected_count_down
        entered_stable_range = (
            board.mZombieCountDown <= STANDARD_REFRESH_COUNTDOWN
            and board.mZombieCountDown == expected_count_down
        )
        if threshold_triggered or entered_stable_range:
            self._RecordThreshold(
                board, wave, board.mZombieCountDown, 'normal_wave')

    def GetThresholdRefreshPoint(self, board: Lawn.Board, wave: int):
        threshold = self._State(board)['thresholds'].get(wave)
        if threshold is None:
            return None
        trigger_main_counter, remaining, _ = threshold
        return trigger_main_counter + remaining

    def GetRefreshPoint(self, board: Lawn.Board, wave: int):
        return self._State(board)['refresh_points'].get(wave)


wave_clock = WaveClock()

refresh_point = 0
prev_until_time = 0


def Delay(t: int):
    board = GetBoard()
    prev_time = board.mMainCounter
    while board.mMainCounter - prev_time < t:
        yield
    if board.mMainCounter - prev_time > t:
        gvar.timePassed = True
        Sexy.Debug.Log(f'warning: Delay time has passed!')
    else:
        gvar.timePassed = False
    Sexy.Debug.Log(f"Delay: time = {t}")


def _WaitUntilRefreshPoint(rel_time: int, point: int):
    board = GetBoard()
    elapsed = board.mMainCounter - point
    yield from Delay(rel_time - elapsed)


def Prejudge(rel_time: int, wave: int):
    global refresh_point
    global prev_until_time
    prev_until_time = rel_time
    board = GetBoard()
    if not _UsesStandardZombieSpawning():
        gvar.timePassed = True
        Sexy.Debug.Log('warning: Prejudge does not support this spawning mode!')
        return
    if wave < 1 or wave > board.mNumWaves:
        gvar.timePassed = True
        Sexy.Debug.Log(
            f'warning: Prejudge wave {wave} is outside 1..{board.mNumWaves}!')
        return

    if board.mCurrentWave > wave:
        gvar.timePassed = True
        Sexy.Debug.Log(f'warning: Prejudge time has passed!')
        return

    if board.mCurrentWave == wave:
        point = wave_clock.GetRefreshPoint(board, wave)
        if point is None:
            gvar.timePassed = True
            Sexy.Debug.Log(
                f'warning: refresh point of wave {wave} was not recorded!')
            return
        refresh_point = point
        yield from _WaitUntilRefreshPoint(rel_time, refresh_point)
    else:
        while board.mCurrentWave < wave - 1:
            yield

        point = None
        while point is None:
            if board.mCurrentWave >= wave:
                point = wave_clock.GetRefreshPoint(board, wave)
                break
            point = wave_clock.GetThresholdRefreshPoint(board, wave)
            if point is None:
                yield

        if point is None:
            gvar.timePassed = True
            Sexy.Debug.Log(
                f'warning: refresh threshold of wave {wave} was not recorded!')
            return

        refresh_point = point
        yield from _WaitUntilRefreshPoint(rel_time, refresh_point)

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
