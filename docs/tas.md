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

下方显示 `Frame: {mMainCounter}`，方便定位时间点。

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

```
{playerId}_{gameMode}_{frame}.dat
```

复用游戏自身的 `board.SaveGame()` / `board.LoadGame()` 序列化，无需自己实现。

### 生命周期

- **进入关卡**时（`scan_and_load`）：扫描存档目录，加载该玩家+模式下的全部存档，按 frame 排序
- **离开关卡**时：存档文件保留在磁盘上。重新进入同一关卡可继续使用
- **截断**：live 状态下存档时，指针右侧的存档文件和记录被删除

## 实现文件

| 文件 | 内容 |
|---|---|
| `pgvztool/tas.py` | `TasManager` 类 + 协程脚本 |
| `pgvztool/hook.py` | 按钮创建/绘制/点击 + 帧计数器绘制 |
| `pgvztool/cheat.py` | `tasEnabled` 开关 |

## 限制

- `LoadGame` 恢复状态时需要 Board 存在，因此 undo/redo 只能在关卡内使用
- 暂停期间脚本不执行（`mManualPaused` 导致 `Board.UpdateGame` 跳过），cleanup 逻辑只在非暂停时运行
- 存档文件不会自动清理，需手动删除 `tas_saves/` 目录
