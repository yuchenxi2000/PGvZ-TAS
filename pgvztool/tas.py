"""
TAS 存档/读档/逐帧控制
mMainCounter 全局自增（跨 stage 也是一直递增），因此文件名只含 frame 即可
"""
from pathlib import Path
import uuid
import Sexy
import Lawn
import Lawn.Creative
from pgvz import GetLawnApp, GetBoard, script_manager, ScriptRunMode


class TasManager:
    ACTION_SAVE = 0
    ACTION_UNDO = 1
    ACTION_REDO = 2
    ACTION_ADVANCE = 3
    ACTION_LABELS = ('Save', 'Undo', 'Redo', 'Adv')

    def __init__(self):
        self._saves: 'list[int]' = []   # 每次存档时的 board.mMainCounter
        self._pointer = -1               # -1=live, >=0=存档索引
        self._browse = True              # True=浏览历史中(暂停), False=已取消暂停
        self._pendingFrameAdvance = False
        self._saveDir: 'Path' = None   # type: ignore
        self.last_error = None
        self._cleanup_failed = False
        self.buttons: 'list[Lawn.GameButton]' = None              # type: ignore  # 懒初始化，hook.py 使用

    def can_use(self, board: Lawn.Board, enabled: bool):
        return enabled and board.mApp.mGameScene == Lawn.GameScenes.Playing \
            and board.mApp.mGameMode not in (Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom, Lawn.GameMode.Upsell, Lawn.GameMode.Intro)

    def run_action(self, index: int):
        actions = (self.save, self.undo, self.redo, self.frame_advance)
        if not 0 <= index < len(actions):
            return False
        try:
            result = actions[index]()
            self.last_error = None
            self._cleanup_failed = False
            return result
        except Exception as error:
            self._report_error(error)
            return False

    def _report_error(self, error):
        message = str(error)
        if message == self.last_error:
            return
        self.last_error = message
        try:
            Sexy.Debug.Log(Sexy.DebugType.Error, '[pgvztool.tas] ' + message)
        except Exception:
            pass
        try:
            app = GetLawnApp()
            app.KillDialog(7)
            app.DoDialog(7, True, 'TAS error / TAS 错误', message, 'OK / 确定', 3)
        except Exception:
            pass

    def _init_save_dir(self):
        if self._saveDir is not None:
            return
        storage = Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath
        directory = Path(storage) / 'docs' / 'userdata' / 'tas_saves'
        directory.mkdir(parents=True, exist_ok=True)
        self._saveDir = directory

    def _file_stem(self, lawnApp: Lawn.LawnApp):
        playerId = int(lawnApp.mPlayerInfo.mId)
        gameMode = lawnApp.mGameMode
        if lawnApp.IsDIYMode() or lawnApp.IsOnlineLevelMode():
            creativeLevel = Lawn.Creative.CreativeLevelManager.GetLevelDefine(gameMode)
            if creativeLevel is not None:
                levelKey = f'{int(creativeLevel.mCrc):08X}'
            else:
                levelKey = str(int(gameMode))
            return f'{playerId}_{levelKey}'
        return f'{playerId}_{int(gameMode)}'

    def _file_name(self, lawnApp: Lawn.LawnApp, frame):
        return f'{self._file_stem(lawnApp)}_{frame}.dat'

    def _frame_path(self, frame):
        self._init_save_dir()
        return self._saveDir / self._file_name(GetLawnApp(), frame)

    def _file_path(self, index):
        return self._frame_path(self._saves[index])

    def _temporary_path(self, target, purpose):
        return target.with_name(target.name + '.' + purpose + '-' + uuid.uuid4().hex)

    def _remove_temporary(self, path):
        try:
            if path.exists():
                path.unlink()
        except OSError as error:
            # 已提交后的清理失败不能回滚为“操作失败”；残留文件不会参与扫描。
            try:
                Sexy.Debug.Log(Sexy.DebugType.Error, '[pgvztool.tas] cleanup {}: {}'.format(path, error))
            except Exception:
                pass

    def _write_snapshot(self, board, path):
        board.SaveGame(str(path))
        # 原生 SaveGame 丢弃底层 bool 返回值，失败时也可能没有异常。
        if not path.is_file() or path.stat().st_size == 0:
            raise IOError('TAS snapshot was not written: {}'.format(path))

    def _restore_files(self, staged):
        errors = []
        for original, backup in reversed(staged):
            try:
                backup.replace(original)
            except OSError as error:
                errors.append('{}: {}'.format(backup, error))
        if errors:
            raise IOError('TAS rollback failed; preserved backup files: ' + '; '.join(errors))

    def _stage_files(self, frames):
        staged = []
        try:
            for frame in frames:
                original = self._frame_path(frame)
                if original.is_file():
                    backup = self._temporary_path(original, 'discard')
                    original.replace(backup)
                    staged.append((original, backup))
        except Exception:
            self._restore_files(staged)
            raise
        return staged

    def _truncate(self, from_i):
        """先暂存未来文件；全部成功后提交时间线，最后清理暂存文件。"""
        staged = self._stage_files(self._saves[from_i:])
        self._saves = self._saves[:from_i]
        self._pointer = min(self._pointer, len(self._saves) - 1)
        for _, backup in staged:
            self._remove_temporary(backup)

    def scan_and_load(self):
        self._init_save_dir()
        prefix = self._file_stem(GetLawnApp()) + '_'
        saves = []
        for path in self._saveDir.iterdir():
            name = path.name
            if path.is_file() and name.startswith(prefix) and name.endswith('.dat'):
                try:
                    frame = int(name[len(prefix):-4])
                    if frame >= 0:
                        saves.append(frame)
                except ValueError:
                    pass
        # 扫描成功后再替换状态，目录访问异常不会清空现有历史。
        self._saves = sorted(set(saves))
        self._pointer = len(self._saves) - 1
        self._browse = True
        self._pendingFrameAdvance = False
        self._cleanup_failed = False

    def save(self) -> bool:
        board = GetBoard()
        if board is None:
            return False
        frame = board.mMainCounter
        same_frame = self._pointer >= 0 and frame == self._saves[self._pointer]
        next_pointer = self._pointer if same_frame else self._pointer + 1
        future = [] if same_frame else self._saves[next_pointer:]
        target = self._frame_path(frame)
        temporary = self._temporary_path(target, 'write')
        staged = []
        try:
            self._write_snapshot(board, temporary)
            staged = self._stage_files(future)
            temporary.replace(target)
        except Exception:
            self._restore_files(staged)
            raise
        finally:
            self._remove_temporary(temporary)
        if not same_frame:
            self._saves = self._saves[:next_pointer] + [frame]
            self._pointer = next_pointer
        for _, backup in staged:
            self._remove_temporary(backup)
        self._cleanup_failed = False
        return True

    def _load_and_pause(self, index):
        board = GetBoard()
        if board is None:
            return False
        target = self._file_path(index)
        if not target.is_file() or target.stat().st_size == 0:
            raise IOError('TAS save is missing or empty: {}'.format(target))
        recovery = self._temporary_path(target, 'recovery')
        was_paused = board.mManualPaused
        keep_recovery = False
        try:
            self._write_snapshot(board, recovery)
            try:
                if not board.LoadGame(str(target)):
                    raise IOError('TAS LoadGame failed: {}'.format(target))
            except Exception as load_error:
                try:
                    if not board.LoadGame(str(recovery)):
                        raise IOError('LoadGame returned false')
                    board.mManualPaused = was_paused
                except Exception as recovery_error:
                    keep_recovery = True
                    board.mManualPaused = True
                    raise IOError('TAS load and recovery failed: {}; {}; recovery file: {}'.format(
                        load_error, recovery_error, recovery))
                raise
            # 原生读取成功后才移动指针及切换浏览状态。
            self._pointer = index
            board.mManualPaused = True
            self._browse = True
            self._pendingFrameAdvance = False
            return True
        finally:
            if not keep_recovery:
                self._remove_temporary(recovery)

    def undo(self) -> bool:
        if GetBoard() is None or self._pointer < 0:
            return False
        if not self._browse and not self.save():
            return False
        if self._pointer > 0:
            return self._load_and_pause(self._pointer - 1)
        return False

    def redo(self) -> bool:
        if self._pointer < len(self._saves) - 1:
            return self._load_and_pause(self._pointer + 1)
        return False

    def frame_advance(self):
        board = GetBoard()
        if board is None:
            return
        board.mManualPaused = False
        self._browse = False
        self._pendingFrameAdvance = True

    def _on_tick(self):
        """协程每帧调用：逐帧暂停 + 浏览重置 + 清理过期存档"""
        board = GetBoard()
        if board is None or board.mManualPaused:
            return
        # 逐帧：跑完一帧后暂停
        if self._pendingFrameAdvance:
            board.mManualPaused = True
            self._pendingFrameAdvance = False
            return
        # 首次非暂停 tick → 退出浏览状态
        if self._browse:
            self._browse = False
        # 清理"超车"的过期存档
        if not self._cleanup_failed and not self._browse and self._pointer >= 0:
            current = board.mMainCounter
            while len(self._saves) > self._pointer + 1:
                if self._saves[self._pointer + 1] < current:
                    self._truncate(self._pointer + 1)
                else:
                    break


tas_manager = TasManager()


def _tas_main():
    try:
        tas_manager.scan_and_load()
    except Exception as error:
        tas_manager._report_error(error)
        return
    while True:
        try:
            tas_manager._on_tick()
        except Exception as error:
            tas_manager._cleanup_failed = True
            tas_manager._report_error(error)
        yield

script_manager.Register(_tas_main, runmode=ScriptRunMode.FOREVER)
