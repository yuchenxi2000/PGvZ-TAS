# TAS（Tool-Assisted Superplay）

## 概述

在关卡中提供类似模拟器的存档/读档/逐帧功能，用于精确控制游戏操作。

不支持的关卡模式：禅境花园、智慧树、购买界面、开场动画。

## 界面

勾选"启用 TAS"后，右下角出现四个竖排按钮和一个帧计数器：

| 按钮 | 功能 |
|---|---|
| Save | 存档当前状态 |
| Undo | 读档回退 |
| Redo | 读档前进 |
| Adv | 逐帧（取消暂停，跑 1 帧后自动暂停） |

四个按钮的默认快捷键依次为 `u` / `i` / `o` / `p`，可通过 `keybinds.txt` 中的 `tas_save` / `tas_undo` / `tas_redo` / `tas_advance` 重新绑定，详见 [keybinds.md](keybinds.md)。

下方显示 `Frame: {mMainCounter}`，方便定位时间点。

和通常的存档/读档不同，这里的 Save 和 Undo 操作一条**存档队列**而不是单个文件。每次 Save 在当前时间点新增一个存档；Undo 沿队列向过去回档，一直点一直往前回；Redo 是"撤销回档"——比如 Undo 两次后又想回到最初，点两次 Redo 即可。

## 核心机制

### 时间线模型

存档按 `mMainCounter`（全局自增帧计数器）排序。指针指向当前在时间线上的位置。

```
S0(100) → S1(200) → S2(350) → [live frame 400]
                       ↑ _pointer = 2
```

### 状态机

| 状态 | 含义 |
|---|---|
| live (`_browse=False`) | 游戏正常运行 |
| 浏览 (`_browse=True`) | undo/redo 后暂停，查看历史状态 |

### 操作行为

**Save**：写入当前 Board 状态到文件。暂停时可存（同帧覆盖）。live 状态下手动取消暂停后存档，如果指针不在队尾，截断未来的存档分支。

**Undo**：
- live 状态：先自动 Save 当前状态，再加载指针指向的存档
- 浏览状态：移动指针到更早的存档，不自动保存

**Redo**：移动指针到下一个存档并加载。到达队尾时无法继续。

**Adv（逐帧）**：取消暂停 → 跑 1 帧 → 自动暂停。同时设置 `_browse = False`，表示开始玩新路线。

## 存档数据

### 存储位置

`{游戏存档根目录}/docs/userdata/tas_saves/`

### 文件格式

正常关卡文件名格式：

```text
{playerId}_{gameMode}_{frame}.dat
```

本地和在线自定义关卡参考游戏 `LawnCommon.GetSavedGameName()` 的文件名实现，拼接上帧数 `frame` 组成文件名：

```text
{playerId}_{crc8}_{frame}.dat
```

复用游戏自身的 `board.SaveGame()` / `board.LoadGame()` 序列化，无需自己实现。

### 生命周期

- **进入关卡**时（`scan_and_load`）：扫描存档目录，加载该玩家+模式下的全部存档，按 frame 排序
- **离开关卡**时：存档文件保留在磁盘上。重新进入同一关卡可继续使用
- **截断**：live 状态下存档时，指针右侧的存档文件和记录被删除

### 存读档失败与恢复

保存先写入同目录的唯一临时文件，确认文件存在且非空后再替换正式文件。同帧覆盖失败时
保留原文件；需要截断未来分支时，先将未来文件改名暂存，全部成功后才提交存档列表和指针。
写入、改名或替换失败时恢复暂存文件，避免提前删除历史。提交成功后的临时文件删除失败只
记日志，不把已完成的保存误报成失败。

读档前先保存当前 Board 的恢复快照。目标缺失、为空或恢复快照写入失败时不会调用
`LoadGame`。目标读取返回 false 或抛出异常时，用恢复快照重新加载，并恢复原暂停状态；
只有目标加载成功才移动指针、进入浏览状态并暂停。如果恢复也失败，保持暂停，保留恢复
文件并在错误消息中给出路径，不能保证此时内存中的 Board 完整。

live 状态的 Undo 包含“自动保存当前状态”和“加载上一存档”两个步骤。若前者成功、后者
失败，保留新自动存档及其对应指针；不会撤销已经成功保存的当前状态。

依据本地 PGvZ 1.3.1 反编译源码，`Board.SaveGame()` 返回 void，丢弃
`GlobalMembersSaveGame.LawnSaveGame()` 的 bool 结果，底层保存失败可能没有异常，因此需检查
新文件。`Board.LoadGame()` 返回 bool，底层读取过程中可能先清理现有对象再失败，因此不能
只回退 Python 中的指针；恢复快照仍通过游戏原生存读档实现，受相同的序列化限制。

临时文件使用 `.dat.write-<id>`、`.dat.discard-<id>`、`.dat.recovery-<id>` 后缀，不参与正常
`.dat` 存档扫描。若文件回滚也失败，错误消息列出保留的备份路径；进程中断也可能留下这些
文件，应先确认是否需要恢复再手动删除。普通存读档错误由 TAS 按钮/快捷键入口捕获并显示
弹窗及日志；自动清理失败后停止反复清理，下一次成功操作或重新启用 TAS 后可重试。

## 实现文件

| 文件 | 内容 |
|---|---|
| `pgvztool/tas.py` | `TasManager` 类 + 协程脚本 |
| `pgvztool/hook.py` | 绘制和点击挂钩，调用 TAS UI 辅助函数 |
| `pgvztool/overlay.py` | 按钮创建/绘制 + 帧计数器绘制 |
| `pgvztool/cheat.py` | `tasEnabled` 开关 |

## 限制

- `LoadGame` 恢复状态时需要 Board 存在，因此 undo/redo 只能在关卡内使用
- 暂停期间脚本不执行（`mManualPaused` 导致 `Board.UpdateGame` 跳过），cleanup 逻辑只在非暂停时运行
- 存档文件不会自动清理，需手动删除 `tas_saves/` 目录
- 游戏存档未序列化 `Challenge.mRandomPortalCounter` 和 `SeedBank.mConveyorBeltBuffer`，因此随机传送门与传送带关卡的 Undo/Redo 可能无法精确恢复这两项状态
- 自定义关卡的 `CSSpeed` 会在一次更新内额外调用 `Board.UpdateGame()`，因此 Adv 目前可能一次前进多个逻辑帧
