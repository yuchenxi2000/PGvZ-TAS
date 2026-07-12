"""
TAS 存档/读档/逐帧控制
mMainCounter 全局自增（跨 stage 也是一直递增），因此文件名只含 frame 即可
"""
from pathlib import Path
import Sexy
import Lawn
from pgvz import GetLawnApp, GetBoard, script_manager, ScriptRunMode


class TasManager:
    def __init__(self):
        self._saves: 'list[int]' = []   # 每次存档时的 board.mMainCounter
        self._pointer = -1               # -1=live, >=0=存档索引
        self._browse = True              # True=浏览历史中(暂停), False=已取消暂停
        self._pendingFrameAdvance = False
        self._saveDir: 'Path' = None   # type: ignore
        self.buttons: 'list[Lawn.GameButton]' = None              # type: ignore  # 懒初始化，hook.py 使用

    def _init_save_dir(self):
        if self._saveDir is not None:
            return
        storage = Sexy.GlobalStaticVars.gSexyAppBase.applicationStoragePath
        self._saveDir = Path(storage) / 'docs' / 'userdata' / 'tas_saves'
        try:
            self._saveDir.mkdir(parents=True)
        except OSError:
            pass

    def _file_name(self, playerId, gameMode, frame):
        return f'{playerId}_{int(gameMode)}_{frame}.dat'

    def _file_path(self, index):
        lawnApp = GetLawnApp()
        self._init_save_dir()
        return self._saveDir / self._file_name(lawnApp.mPlayerInfo.mId, lawnApp.mGameMode, self._saves[index])

    def _truncate(self, from_i):
        """删除 from_i 及之后的存档文件和条目"""
        for i in range(from_i, len(self._saves)):
            fp = self._file_path(i)
            if fp.is_file():
                fp.unlink()
        self._saves = self._saves[:from_i]

    def scan_and_load(self):
        """进入关卡时扫描存档目录，加载该 player+mode 下的全部存档"""
        lawnApp = GetLawnApp()
        self._init_save_dir()
        playerId = lawnApp.mPlayerInfo.mId
        gameMode = lawnApp.mGameMode
        prefix = f'{playerId}_{int(gameMode)}_'
        suffix = '.dat'

        self._saves = []
        for f in self._saveDir.iterdir():
            name = f.name
            if name.startswith(prefix) and name.endswith(suffix):
                try:
                    frame = int(name[len(prefix):-len(suffix)])
                    self._saves.append(frame)
                except ValueError:
                    pass
        self._saves.sort()
        self._pointer = len(self._saves) - 1 if self._saves else -1
        self._browse = True

    def save(self) -> bool:
        board = GetBoard()
        if board is None:
            return False
        frame = board.mMainCounter
        # 同帧覆盖
        if self._pointer >= 0 and frame == self._saves[self._pointer]:
            board.SaveGame(str(self._file_path(self._pointer)))
            return True
        # 指针不在尾端且不在浏览中 → 截断未来
        if self._pointer >= 0 and self._pointer < len(self._saves) - 1 and not self._browse:
            self._truncate(self._pointer + 1)
        # 追加
        self._pointer += 1
        self._saves.insert(self._pointer, frame)
        self._saves = self._saves[:self._pointer + 1]
        board.SaveGame(str(self._file_path(self._pointer)))
        return True

    def _load_and_pause(self, index):
        board = GetBoard()
        if board is None:
            return False
        board.LoadGame(str(self._file_path(index)))
        board.mManualPaused = True
        self._browse = True
        return True

    def undo(self) -> bool:
        board = GetBoard()
        if board is None or self._pointer < 0:
            return False
        # live 状态 → 先存档当前位置，再回到上一个存档
        if not self._browse:
            self.save()
            if self._pointer > 0:
                self._pointer -= 1
                return self._load_and_pause(self._pointer)
            return False
        # 浏览状态 → 回退到更早的存档
        if self._pointer > 0:
            self._pointer -= 1
            return self._load_and_pause(self._pointer)
        return False

    def redo(self) -> bool:
        if self._pointer < len(self._saves) - 1:
            self._pointer += 1
            return self._load_and_pause(self._pointer)
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
        if not self._browse and self._pointer >= 0:
            current = board.mMainCounter
            while len(self._saves) > self._pointer + 1:
                if self._saves[self._pointer + 1] < current:
                    self._truncate(self._pointer + 1)
                else:
                    break


tas_manager = TasManager()


def _tas_main():
    tas_manager.scan_and_load()
    while True:
        tas_manager._on_tick()
        yield

script_manager.Register(_tas_main, runmode=ScriptRunMode.FOREVER)
