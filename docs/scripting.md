# PGvZ-TAS 脚本编写指南

本文介绍如何为植物娘大战僵尸（PGvZ）编写自动操作脚本。读者不需要预先了解原版
植物大战僵尸的 PyVZ 或 AvZ 框架；熟悉这些框架的读者可以直接阅读
[面向 PyVZ、AvZ 用户的快速上手](#七面向-pyvzavz-用户的快速上手)。

PGvZ-TAS 只支持项目声明的最新游戏版本。PGvZ 与原版 PvZ 的关系和已知机制差异见
[PGvZ 与 PvZ 的异同](pgvz-vs-pvz.md)。

本文的 API 参考仅覆盖 `from pgvz import *` 引入的公开接口。游戏内部的 C# API 不在
本文中逐项列出；需要使用内部能力时，请参考[进阶教程](#八进阶教程)。

## 阅读导航

- 了解适用的游戏机制：[PGvZ 与 PvZ 的异同](pgvz-vs-pvz.md)
- 第一次编写脚本：[快速开始](#一快速开始) → [脚本如何运行](#二脚本如何运行) →
  [脚本运行](#四脚本运行)
- 查询框架接口：[公开 API 说明](#三公开-api-说明)
- 排查问题：[脚本调试](#五脚本调试)
- 从完整代码学习：[示例脚本](#六示例脚本)
- 迁移原版框架脚本：[面向 PyVZ、AvZ 用户的快速上手](#七面向-pyvzavz-用户的快速上手)
- 编写复杂功能：[进阶教程](#八进阶教程)
- 外部资料：[参考网址](#九参考网址)

## 一、快速开始

### 1. 脚本文件模板

游戏使用 IronPython 运行模组。桌面版脚本应先把 IronPython 标准库和 `mods/` 加入
模块搜索路径，然后分别导入游戏类型和 PGvZ-TAS API：

```python
import sys
import System
import System.IO

# Android：IronPython 标准库通常位于 CurrentDirectory/IronPython/Libs。
py_lib_path = System.IO.Path.Combine(
    System.Environment.CurrentDirectory,
    'IronPython',
    'Libs',
)
if not System.IO.Directory.Exists(py_lib_path):
    # Windows：标准库通常位于游戏主程序同目录的 lib。
    py_lib_path = System.IO.Path.Combine(
        System.IO.Path.GetDirectoryName(System.Environment.ProcessPath),
        'lib',
    )

mods_dir_path = System.IO.Path.Combine(
    System.Environment.CurrentDirectory,
    'mods',
)
if py_lib_path not in sys.path:
    sys.path.append(py_lib_path)
if mods_dir_path not in sys.path:
    sys.path.append(mods_dir_path)

import Lawn
from pgvz import *
```

Android 上有时不手动设置路径也能导入，但为了让同一脚本兼容桌面版和手机版，建议保留
这段初始化代码。

`from pgvz import *` 不会导入 `Lawn`、`Sexy`、`System` 或 `LawnMod`。脚本用到哪个游戏
或 .NET 命名空间，就要单独 `import` 哪个命名空间。

### 2. 第一个自动操作脚本

下面的脚本在泳池无尽第一波刷新前 100 帧尝试种下一株向日葵。进入关卡前需要手动把
向日葵选入卡槽。

```python
import Lawn
from pgvz import *

def ScriptDemo():
    yield from Prejudge(-100, 1)
    Card(Lawn.SeedType.Sunflower, 1, 1)

script_demo = script_manager.Register(
    ScriptDemo,
    gamemode=Lawn.GameMode.SurvivalEndlessStage3,
    runmode=ScriptRunMode.ONCE,
)
```

这里有四个关键点：

1. 脚本是一个无参数函数。
2. `Prejudge` 会等待，所以必须写成 `yield from Prejudge(...)`。
3. 函数中出现 `yield` 或 `yield from` 后，它就是按时间顺序运行的生成器脚本。
4. 定义函数并不会自动运行；必须通过 `script_manager.Register` 注册。

### 3. 行列和时间的基本约定

- `Card`、`Shovel`、`SetPlantOnBoard` 使用从 1 开始的 `(row, col)`，即第一行第一列写作
  `(1, 1)`。
- `PixelToGrid`、`GridToPixel` 和 `MouseDragGrid` 使用游戏内部的零基 `(col, row)`，即
  左上角格子写作 `(0, 0)`。
- `CobManager.Fire` 使用一基行号；落点列可以是浮点数，例如 `(2, 8.8)`。
- 时间操作的单位是游戏逻辑帧，不是渲染帧或现实毫秒。
- `Prejudge(t, wave)` 和 `Until(t)` 的 `t` 都以目标波实际刷新点为 0；负数表示刷新前，
  正数表示刷新后。

坐标系统的完整说明见[坐标与绘制](rendering.md)。波次刷新点的来源和支持范围见
[僵尸波次刷新机制](zombie-spawning.md)。

## 二、脚本如何运行

### 1. 生成器脚本与逐帧脚本

框架根据函数是否为生成器，自动选择两种执行方式。

生成器脚本用于按时间顺序执行操作：

```python
def TimedScript():
    yield from Prejudge(-200, 1)
    Card(Lawn.SeedType.Iceshroom, 1, 1)
    yield from DelayA(100)
    Shovel(1, 1)
```

每个游戏逻辑帧，框架只把生成器推进到下一个 `yield`。以下公开函数会等待，调用时必须
使用 `yield from`：

- `Delay`
- `Prejudge`
- `Until`
- `DelayA`
- `SelectCards`
- `LetsRock`

如果一个本应阻塞的脚本暂时没有调用这些函数，应在函数中保留一个 `yield`，否则它会被
识别为逐帧脚本。

逐帧脚本是不含 `yield` 的普通函数。框架会在每个可运行的游戏逻辑帧调用一次，适合
自动收集、状态监视和小游戏自动操作：

```python
def TickScript():
    for zombie in IterAliveZombies():
        # 每帧检查一次当前存活僵尸。
        pass

script_tick = script_manager.Register(TickScript)
```

脚本在游戏主线程、当前逻辑帧的游戏更新之前运行。不要在脚本中使用 `sleep`、等待输入、
网络请求等阻塞主线程的操作。

### 2. 注册与生命周期

常用注册形式如下：

```python
script_obj = script_manager.Register(
    ScriptFunc,
    gamemode=Lawn.GameMode.SurvivalEndlessStage3,
    runmode=ScriptRunMode.FOREVER,
)
```

`ScriptRunMode` 的含义：

| 模式 | 生命周期 |
|---|---|
| `FOREVER` | 离开当前关卡后保留注册；下次进入满足条件的关卡时从函数开头重新开始。默认值。 |
| `ONCE` | 当前战斗或选卡流程结束后卸载，适合临时脚本。 |
| `GLOBAL` | 不受 Board 和游戏场景限制，注册后立即开始；主要用于框架和修改器内部任务。普通关卡脚本不建议使用。 |

传入 `gamemode` 后，脚本只在该 `Lawn.GameMode` 下运行。不传时不限制模式。需要组合多个
条件时使用 `ScriptConf`，详见[自定义运行条件](#1-自定义运行条件)。

`Register` 返回一个 `ScriptObj`：

```python
script_obj.Off()  # 暂停；生成器保留当前位置。
script_obj.On()   # 从暂停位置继续。
script_manager.Unregister(script_obj)  # 从普通脚本列表中卸载。
```

在当前关卡已经开始运行后，需要立即插入一个辅助任务时，使用：

```python
helper_script = script_manager.RunInThread(HelperScript)
```

它会立即启动任务，并把任务限制在调用时的游戏模式。这里的 “Thread” 是框架沿用的名称；
任务仍由主线程逐帧推进，不会创建操作系统线程。返回值是新建的 `ScriptObj`，可以用
`Off()`、`On()` 或 `Unregister()` 控制这个动态任务。

### 3. 框架在什么场景推进脚本

普通脚本只会在以下条件同时满足时运行：

- 当前存在 `Board`；
- 场景处于选卡/关卡导入或正在游戏；
- 没有“继续游戏”对话框。

离开战斗界面后，生成器会按运行模式卸载或重置。倍速时脚本仍按每个游戏逻辑帧运行，
而不是只按画面刷新频率运行。全局快慢速和 Board 分数速度的执行层级、分帧算法及叠加
关系见[游戏速度控制机制](speed-control.md)。

### 4. 同时加载多个脚本

脚本管理器可以注册多个脚本，也可以用 `RunInThread` 动态插入辅助脚本。各脚本拥有各自
的生成器执行位置，但部分框架状态是共享的：

- `Prejudge`、`Until` 和 `DelayA` 当前使用模块级刷新参考点；
- `gvar.timePassed` 和 `gvar.doPassedOp` 是全局状态；
- 多个脚本会操作同一个游戏 Board。

因此不要让多个定时脚本交错执行不同波次的 `Prejudge` → `Until`/`DelayA` 序列。适合
并行的任务应尽量是独立逐帧监视器，或只使用 `Delay` 的辅助生成器。

## 三、公开 API 说明

以下名称均由 `from pgvz import *` 导入。参数中的 `Lawn.SeedType`、`Lawn.GameMode` 等
是游戏类型，需要另外执行 `import Lawn`；本文不枚举游戏内部类型及其成员。

### 1. 游戏对象与版本信息

#### `GetLawnApp()`

返回当前全局 `LawnApp`。它在主菜单和关卡内都存在。

#### `GetBoard()`

返回当前 `Board`。不在关卡内时可能为 `None`，逐帧辅助函数应先判断。

#### 版本常量

| 名称 | 含义 |
|---|---|
| `MOD_VERSION` | 当前 PGvZ-TAS 模组版本。 |
| `PROJECT_VERSION` | 项目版本，当前与 `MOD_VERSION` 相同。 |
| `TOOL_VERSION` | 修改器版本，当前与 `MOD_VERSION` 相同。 |
| `SUPPORTED_GAME_VERSIONS` | 当前支持的 PGvZ 游戏版本元组。 |
| `__version__` | `PROJECT_VERSION` 的标准模块别名。 |
| `__supported_game_versions__` | `SUPPORTED_GAME_VERSIONS` 的标准模块别名。 |

### 2. 速度控制

速度 API 位于 `pgvz/speed.py`，所有设置都限制在闭区间 `0.01` 至 `100`：

| API | 说明 |
|---|---|
| `GetGlobalSpeedExact()` | 返回游戏实际采用的全局 `(is_fast, factor)`。 |
| `GetGlobalSpeed()` | 以浮点数返回实际全局速度。 |
| `SetGlobalSpeedExact(is_fast, factor)` | 全局精确速度；`is_fast=True` 表示 `factor` 倍，否则表示 `1/factor` 倍。 |
| `SetGlobalSpeed(speed)` | 按整数倍/整数倒数倍规则转换浮点数并设置全局速度。 |
| `GetBoardSpeedExact(board=None)` | 原样返回 Board 的 `(numerator, denominator)`。 |
| `GetBoardSpeed(board=None)` | 以浮点数返回 Board 当前配置的速度。 |
| `SetBoardSpeedExact(numerator, denominator, board=None)` | 直接设置 Board 分子和分母，不约分，并重置分帧相位。 |
| `SetBoardSpeed(speed, max_error=1e-6, board=None)` | 用连分数把浮点速度转换为误差小于 `max_error` 的 Board 分数。 |

四个设置函数都返回实际写入的精确表示。全局设置返回 `(is_fast, factor)`，Board 设置返回
`(numerator, denominator)`：

```python
SetGlobalSpeedExact(False, 5)       # 全局 1/5 倍。
actual_global = SetGlobalSpeed(1.6) # 返回 (True, 2)。
current_global = GetGlobalSpeed()   # 返回 2.0。

SetBoardSpeedExact(3, 2)            # 当前关卡精确 3/2 倍。
actual_board = SetBoardSpeed(1.414, max_error=1e-5)
current_ratio = GetBoardSpeedExact() # 返回实际分子和分母。
```

不在关卡内调用 Board 速度 API 会抛出 `RuntimeError`。非法类型、超出速度范围、无效误差
或可能使游戏的 C# `int` 计算溢出的分数也会抛出异常。Board 精确 getter 会原样返回字段；
如果分母为零，浮点 getter 会抛出 `ValueError`。完整算法、两套速度的作用层级和叠加关系
见[游戏速度控制机制](speed-control.md)。

相关常量为 `MIN_GAME_SPEED`、`MAX_GAME_SPEED` 和 `DEFAULT_BOARD_SPEED_ERROR`。

### 3. 卡片、铲子与选卡

#### `Card(seedtype, row, col, isImitater=False) -> bool`

从当前卡槽中寻找可用卡片，并尝试在一基 `(row, col)` 种植。

- `seedtype` 是要种植的实际植物类型。
- `isImitater=True` 表示寻找模仿该植物的模仿者卡。
- 成功种植返回 `True`；没有可用卡片或当前位置不可种植时返回 `False`。
- 时间点已经过去且操作被取消时返回 `False`。

#### `Shovel(row, col, seedtype=None)`

在一基 `(row, col)` 使用铲子。可用 `seedtype` 调整同格多层植物的点击位置；普通情况
可以省略。

#### `SelectCards(seedList, *args, waitTime=200, selectRose=True)`

在选卡界面选择 `seedList`，等待 `waitTime` 个逻辑帧后开始关卡。它是生成器函数，必须
使用 `yield from`。

模仿者的目标类型作为额外位置参数传入：

```python
yield from SelectCards(
    [
        Lawn.SeedType.Iceshroom,
        Lawn.SeedType.Imitater,
        # 其余卡片……
    ],
    Lawn.SeedType.Iceshroom,
    selectRose=False,
)
```

`selectRose` 控制选卡界面的额外钉耙/玫瑰刺客选项。卡片数量仍必须满足当前关卡的选卡
要求。

#### `LetsRock()`

等待当前选卡动画完成并关闭选卡界面。通常由 `SelectCards` 自动调用；单独使用时也必须
写成 `yield from LetsRock()`。

### 4. 时间操作

#### `Delay(t)`

从调用时刻起等待 `t` 个逻辑帧。它只使用当前 `mMainCounter`，不以波次刷新点为基准。

#### `Prejudge(rel_time, wave)`

等待到一基第 `wave` 波的刷新点加 `rel_time`：

```text
目标时刻 = 第 wave 波实际刷新点 + rel_time
```

`Prejudge(-200, 10)` 表示第 10 波刷新前 200 帧。它同时建立随后 `Until` 和 `DelayA`
使用的刷新参考点。

当前实现通过运行时观察游戏的标准僵尸刷新流程记录刷新点，支持 20 波以上关卡和实际
旗帜波，但不支持由挑战逻辑完全接管刷新的关卡。完整范围见
[僵尸波次刷新机制](zombie-spawning.md)。

#### `Until(t)`

等待到最近一次 `Prejudge` 所建立的刷新点加 `t`。`Until` 自身不接收波号，因此前面
必须在同一控制流程中调用 `Prejudge`：

```python
yield from Prejudge(-200, wave)
yield from Until(100)
```

#### `DelayA(t)`

把上一次 `Prejudge`、`Until` 或 `DelayA` 的目标相对时间增加 `t`，并等待到新目标。
它适合在同一波内按相对间隔连续安排操作：

```python
yield from Prejudge(-200, wave)
Card(Lawn.SeedType.Iceshroom, 1, 1)
yield from DelayA(100)  # 到刷新点 -100。
Shovel(1, 1)
```

`DelayA` 前必须先有 `Prejudge`。与 `Delay` 相比，它以刷新点为最终参考，在同一进程内
退出并重新进入存档时更容易保持原时间语义。

#### `gvar`

时间操作的共享状态对象：

| 成员 | 含义 |
|---|---|
| `gvar.timePassed` | 目标时间已过去、波号无效或当前模式不受支持时为 `True`。 |
| `gvar.doPassedOp` | 为 `False` 时，部分框架操作会取消已经错过的动作；设为 `True` 可保留传统框架“立即补做”的行为。默认 `False`。 |
| `gvar.opCanceled` | 只读属性，等于 `timePassed and not doPassedOp`。 |

### 5. 玉米炮

#### `CobManager()`

创建玉米炮管理器。`Fire` 会重新扫描场上的存活玉米炮，并按扫描顺序使用已经恢复的炮：

```python
cob_manager = CobManager()

cob_manager.Fire(2, 8.8)
cob_manager.Fire((2, 8.8), (5, 8.8))
cob_manager.Fire([(2, 8.8), (5, 8.8)])
```

`Fire` 不会等待炮恢复；没有足够的可用炮时，对应落点不会发射。行号一基，列坐标允许
浮点数。

#### `GetCobRecoverTime(cobCannon) -> int`

返回指定玉米炮距离可发射还需要的逻辑帧数。参数应是场上的玉米炮植物对象；不是玉米炮
或处于未知状态时可能抛出异常。

### 6. 僵尸列表

#### `SetZombies(zb_list, internal_spawn=True)`

重新生成当前关卡的出怪列表，并刷新选卡界面的僵尸预览。

- `zb_list` 是 `Lawn.ZombieType` 列表。
- `internal_spawn=True` 通过游戏的内部出怪初始化流程和受控随机输入生成波次，游戏规则
  仍可能过滤某些组合。
- `internal_spawn=False` 直接设置允许出现的类型，再调用游戏的波次选择流程。

该函数会重建波次列表，应在关卡正式刷新僵尸以前调用。设置 PGvZ 新增僵尸时，应使用
当前游戏提供的对应枚举值。

### 7. 坐标与鼠标辅助

| API | 说明 |
|---|---|
| `PixelToGrid(board, pixel)` | 将场地像素 `(x, y)` 转为零基 `(col, row)`。 |
| `PixelToGridRaw(board, pixel)` | 不做边界检查的转换，并处理部分禅境花园背景。越界输入由调用者负责。 |
| `GridToPixel(board, grid)` | 将零基 `(col, row)` 转为格子左上角场地坐标。 |
| `MouseDragGrid(board, grid_from, grid_to)` | 在两个零基格子之间模拟鼠标拖动。 |

屏幕坐标、场地坐标和格子坐标不是同一套坐标，涉及摄像机或绘制时请先阅读
[坐标与绘制](rendering.md)。

### 8. 场上对象与阵型辅助

#### `IterAliveZombies()`

迭代有头、未死亡、未进入死亡过程且未被魅惑的僵尸。若脚本需要头已掉落或被魅惑的
对象，应自行编写不同的筛选逻辑。

#### `IterAlivePlants()`

迭代所有 `mDead == False` 的植物。

#### `IterAliveCoins()`

迭代尚未死亡且未处于收集过程的掉落物。

#### `IterAliveGridItems()`

迭代尚未死亡的场地物品。

#### `SetPlantOnBoard(plantList)`

先移除场上全部植物，再按列表直接放置新阵型。列表元素格式为：

```python
(row, col, seedtype, is_imitater)
```

`row`、`col` 一基。`is_imitater=True` 会以模仿者身份放置目标 `seedtype`。这是直接修改
阵型的工具，不会模拟正常选卡、冷却、阳光消耗或种植检查。

#### `SurvivalBackupGame(max_backup=3)`

保存当前生存模式阶段，并删除超过 `max_backup` 个阶段的旧备份。它依赖当前 Board、
玩家和生存阶段信息，只应在生存模式关卡内调用。

### 9. 枚举辅助

#### `none_of(enumType)`

C# 枚举经常包含名为 `None` 的成员，但 `None` 是 Python 关键字，不能写成
`Lawn.SomeEnum.None`。使用：

```python
empty_value = none_of(Lawn.SomeEnum)
```

#### `SeedTypeNone`

等价于 `none_of(Lawn.SeedType)`，用于需要“无植物”枚举值的场景。

### 10. 脚本管理 API

#### `ScriptManager`

脚本调度器类。框架已经创建并驱动全局实例 `script_manager`；用户脚本通常不应再创建
独立实例，因为独立实例不会自动接入游戏更新循环。

#### `script_manager`

框架预先创建的全局 `ScriptManager`。通常只使用以下方法：

| 方法 | 说明 |
|---|---|
| `Register(script_func, gamemode=None, runmode=FOREVER, conf=None)` | 注册脚本并返回 `ScriptObj`。传入 `conf` 时忽略 `gamemode` 和单独的 `runmode` 配置。 |
| `Unregister(script_obj) -> bool` | 卸载普通脚本；成功返回 `True`。 |
| `RunInThread(script_func) -> ScriptObj` | 在当前游戏模式中立即启动临时辅助任务，并返回它的控制对象。 |

不要自行调用 `Manage()`；它已经由框架的游戏更新钩子驱动。

#### `ScriptObj`

`Register` 返回的脚本对象。常用方法是 `On()` 和 `Off()`。`Start()`、`Reset()` 属于较低层
的生命周期控制，直接调用后需要自行保证脚本管理器状态一致。

#### `ScriptRunMode`、`ScriptType`

`ScriptRunMode` 控制脚本生命周期。`ScriptType.COROUTINE` 表示生成器脚本，
`ScriptType.TICKRUNNER` 表示逐帧脚本；类型由框架自动判断，一般不需要手动设置。

#### `ScriptConf(runmode, runcond)`

保存运行模式和运行条件的高级配置对象，示例见[自定义运行条件](#1-自定义运行条件)。

### 11. 默认自动收集

#### `auto_collector`

框架启动时默认注册的自动收集 `ScriptObj`。它会收集普通掉落物和盆栽，但跳过可用卡片
以及关底奖励。可以随时关闭或重新开启：

```python
auto_collector.Off()
auto_collector.On()
```

## 四、脚本运行

### 1. 作为独立模组自动加载

把 `.py` 文件直接放在游戏的 `mods/` 目录。游戏启动时会扫描并执行 `mods/` 下的 `.py`
文件。

游戏不会自动扫描 Python 包目录中的模块。把脚本放进带 `__init__.py` 的文件夹后，还需
显式导入该包或其中的模块。

Android 会限制应用启动阶段耗时；自动加载的独立 `.py` 文件过多可能导致启动超时。
安装和加载机制详见[安装说明](install.md)。

### 2. 运行时从修改器加载

可以把脚本组织为 `mods/scripts/` 包，再在修改器网页的“自定义”区域执行：

```python
import scripts.pe12
```

导入仓库提供的全部示例：

```python
from scripts import *
```

模块首次导入时会执行顶层的 `script_manager.Register(...)`。Python 会缓存已经导入的
模块，重复执行同一条 `import` 通常不会重复注册。

### 3. 停用和卸载

假设模块导出了 `script_pe12`：

```python
script_pe12.Off()                         # 暂停
script_pe12.On()                          # 恢复
script_manager.Unregister(script_pe12)    # 卸载
```

暂停适合临时关闭；卸载后若要重新注册，通常需要重新执行注册代码或重新加载模块。

## 五、脚本调试

### 1. 查看日志

桌面版可运行带命令行窗口的 `Lawn.Console.exe`。脚本中使用：

```python
import Sexy

Sexy.Debug.Log('script reached wave 10')
```

某些游戏构建的 `Lawn.Console.exe` 本身无法启动，这是游戏版本问题；遇到这种情况应换用
可运行控制台的对应游戏构建，或通过修改器“自定义”区域分段执行代码排查。

### 2. 使用类型存根

仓库的 `typings/` 包含游戏程序集的 `.pyi` 类型存根。把该目录加入 VS Code Pylance 等
类型检查器的搜索路径后，可以获得类型补全和参数提示。存根只用于编辑器，不需要复制到
游戏运行环境。更多说明见 [`typings/README.md`](../typings/README.md)。

IronPython 对现代类型注解的支持有限。涉及 `list[int]`、`tuple[int, int]` 或联合类型时，
建议把整个注解写成字符串，或者干脆省略运行脚本中的注解：

```python
def FindTargets() -> 'list[Lawn.Zombie]':
    return []
```

### 3. 缩小问题范围

调试时建议依次检查：

1. 模块是否真的被导入，注册语句是否执行；
2. `ScriptObj.enabled` 是否为 `True`；
3. 当前游戏模式是否满足 `gamemode` 或 `ScriptConf`；
4. 当前是否存在 Board、是否处于可运行场景；
5. 目标函数是否因为缺少 `yield` 被识别成逐帧脚本；
6. 阻塞函数前是否遗漏 `yield from`；
7. `gvar.timePassed` 是否表明目标时间已经过去；
8. 行列是否混用了一基 `(row, col)` 和零基 `(col, row)`。

可在关键分支输出当前帧、波次和自定义状态，但相关游戏字段的含义应以当前 PGvZ 版本的
实现为准。

### 4. 常见故障

| 现象 | 常见原因 |
|---|---|
| 函数每帧重复执行 | 函数中没有 `yield`，被识别为逐帧脚本。 |
| 时间到了没有种植或发炮 | 卡片/炮不可用，或者目标时间已过去且 `gvar.doPassedOp=False`。 |
| `Until`、`DelayA` 时间异常 | 前面没有先调用 `Prejudge`，或被另一脚本覆盖了共享刷新参考点。 |
| 脚本在某关卡完全不运行 | `gamemode`/`ScriptConf` 不匹配，或该场景不满足脚本管理器条件。 |
| 钩住的小方法没有效果 | 运行时可能已经内联该方法；应选择更大的调用者验证。 |

## 六、示例脚本

仓库的 `scripts/` 目录包含以下示例：

| 文件 | 类型 | 内容 |
|---|---|---|
| `pe12.py` | 生成器脚本 | 泳池无尽经典十二炮；展示选卡、波次时间、炮管理、存档备份和辅助任务。 |
| `me10.py` | 生成器脚本 | 月夜无尽经典十炮；展示自定义阵型、场景处理和同波连续时间操作。 |
| `beghouled.py` | 逐帧脚本 | 宝石迷阵与旋风模式；展示场面读取、搜索有效操作和鼠标拖动。 |
| `whackazombie.py` | 逐帧脚本 | 锤僵尸；展示每帧筛选目标和关卡专用操作。 |
| `slotmachine.py` | 逐帧脚本＋钩子 | 自动拉老虎机，并演示修改关卡内部行为。 |

使用方法和各脚本的导出对象见[示例脚本说明](../scripts/README.md)。

建议按以下顺序阅读：

1. 先看 `whackazombie.py`，理解逐帧脚本和注册；
2. 再看 `pe12.py` 的 `RunPE12`，理解 `Prejudge`、`Until`、`DelayA`；
3. 查看 `me10.py`，理解阵型初始化和动态辅助任务；
4. 最后查看 `slotmachine.py`，学习钩子，并先阅读进阶教程的风险说明。

示例中的阵型、波数和时机服务于对应关卡，不应直接当作其他关卡的通用配置。

## 七、面向 PyVZ、AvZ 用户的快速上手

PGvZ-TAS 的许多术语和接口形状与原版框架相近。游戏内容的异同统一见
[PGvZ 与 PvZ 的异同](pgvz-vs-pvz.md)；框架接口可先用下表建立对应关系：

| 熟悉的概念 | PGvZ-TAS 对应方式 |
|---|---|
| PyVZ/PvZ 主对象 | `GetLawnApp()` |
| 场地/MainObject | `GetBoard()` |
| `Card`、`Shovel` | 同名公开函数，使用 PGvZ 的 `Lawn.SeedType`。 |
| 选卡 | `yield from SelectCards(...)` |
| 出怪设置 | `SetZombies(...)`，使用 PGvZ 的 `Lawn.ZombieType`。 |
| 炮列表/PaoOperator | `CobManager`；`Fire` 在调用时扫描可用炮。 |
| `LeftClick`、`RightClick` 等鼠标操作 | 不提供框架封装；场地内可直接调用 `GetBoard().MouseDown(...)`、`MouseUp(...)`、`MouseMove(...)` 等游戏内部方法。 |
| 波次预判 | `yield from Prejudge(time, wave)` |
| 波内绝对时间 | 先 `Prejudge`，再 `yield from Until(time)`。 |
| 相对延迟 | `yield from Delay(t)`；需要保持波次参考时优先 `DelayA(t)`。 |
| AvZ 的脚本入口 | 任意无参数函数，再用 `script_manager.Register` 注册。 |
| Runner/每帧检查 | 不含 `yield` 的逐帧函数，或用 `RunInThread` 插入辅助任务。 |

当前 PGvZ 版本的鼠标输入使用第三个参数区分按键：左键为 `1`，右键为 `-1`，中键为
`3`。例如，完整模拟一次场地左键或右键点击可以写成：

```python
board = GetBoard()

# 左键点击。
board.MouseDown(x, y, 1)
board.MouseUp(x, y, 1)

# 右键点击。
board.MouseDown(x, y, -1)
board.MouseUp(x, y, -1)
```

许多场地操作在 `MouseDown` 时已经触发，只需要模拟按下时可以省略 `MouseUp`；若要
还原一次完整点击，按下和抬起应使用相同的按键参数。这里的 `x`、`y` 是 Board 的鼠标
输入坐标，不是 `(row, col)` 或 `(col, row)` 格子编号。

这些方法虽然属于游戏内部 API，但鼠标输入接口相对稳定。PyVZ 的 `LeftClick(x, y)`、
`RightClick(x, y)` 分别只需改成一行 `board.MouseDown(x, y, 1)`、
`board.MouseDown(x, y, -1)`，因此框架不额外封装。`Board.MouseDown` 只负责 Board 内的输入；
点击主菜单、对话框等其他 Widget 时，应调用相应界面的输入路径，不能把它当成全局鼠标
点击。

迁移脚本时主要检查以下框架差异：

1. **代码按生成器顺序执行。** 所有等待函数必须 `yield from`；脚本不能依赖 AvZ 的
   任意顺序时间点插入语义。
2. **错过操作默认跳过。** 时间点已过去时，部分操作会由 `gvar.opCanceled` 取消；确实
   需要立即补做时才设置 `gvar.doPassedOp = True`。
3. **时间参考点共享。** 并行定时脚本不要交错建立不同波次的刷新参考点。
4. **坐标要重新确认。** 高层种铲接口是一基 `(row, col)`，底层格子工具是零基
   `(col, row)`。
5. **可以直接使用游戏对象，但不代表所有成员都稳定。** PGvZ-TAS 只适配最新游戏版本；直接
   使用的内部成员应随版本重新核对。

推荐的迁移步骤：

1. 先只移植注册、选卡和一波最简单操作；
2. 为脚本涉及的 PGvZ 新增内容补充相应枚举和处理分支；
3. 根据[已知游戏差异](pgvz-vs-pvz.md)调整受影响的操作，并用日志验证关键时机；
4. 把每波流程整理成 `Prejudge` → `Until`/`DelayA`；
5. 最后加入场面分支、收尾判断和辅助逐帧任务；
6. 分别测试正常进入、中途退出重进、倍速和关底切换。

## 八、进阶教程

### 1. 自定义运行条件

单个 `gamemode` 不够时，可以把任意无参数判断函数传给 `ScriptConf`：

```python
def RunCond():
    app = GetLawnApp()
    board = GetBoard()
    return (
        board is not None
        and app.mGameMode in (
            Lawn.GameMode.ChallengeZenGarden,
            Lawn.GameMode.TreeOfWisdom,
        )
    )

conf = ScriptConf(
    runmode=ScriptRunMode.FOREVER,
    runcond=RunCond,
)
script_obj = script_manager.Register(MyScript, conf=conf)
```

当 `runcond()` 返回 `False` 时，生成器状态会被重置。在同一次关卡加载周期中，条件
重新成立不会自动重启已经重置的生成器；它会在下一次脚本加载周期从函数开头开始。因此
协程脚本的运行条件应在一局内保持稳定，频繁变化的条件更适合放进逐帧脚本自身。判断
函数每帧都可能执行，应保持快速、无副作用。

### 2. 主流程与辅助任务

复杂脚本适合拆为：

- 一个生成器主流程，负责选卡、波次和严格时序；
- 若干逐帧辅助任务，负责气球、漏怪、场面状态等监视；
- 普通纯函数，负责目标选择和数据统计。

```python
def WatchSomething():
    # 不含 yield：每帧运行。
    pass

def MainScript():
    script_manager.RunInThread(WatchSomething)
    for wave in range(1, GetBoard().mNumWaves + 1):
        yield from Prejudge(-200, wave)
        # 主时序操作……
```

辅助任务应避免调用 `Prejudge`、`Until` 或 `DelayA`，以免覆盖主流程的共享时间参考点。

### 3. 中途退出和重新进入

时间框架会在游戏运行时记录标准刷新关卡的真实刷新点。同一游戏进程内退出并重新进入
同一存档时，记录仍可使用；重启游戏后，已经发生的历史刷新点无法从当前倒计时可靠
恢复。

为了提高重进安全性：

- 每一波先调用 `Prejudge`；
- 波内连续等待使用 `Until` 或 `DelayA`，避免用多个与刷新点无关的 `Delay`；
- 分支判断要结合僵尸所属波次，不要只判断场上是否存在任意僵尸；
- 生存模式在合适时机调用 `SurvivalBackupGame`；
- 普通关卡尽量在关卡结束后退出，生存模式尽量回到选卡界面后退出。

详细限制和恢复策略见[僵尸波次刷新机制与时间操作实现](zombie-spawning.md)。

### 4. 使用类型存根和反编译结果

公开 API 无法覆盖所有关卡需求。需要调用游戏内部能力时：

1. 先在 `typings/` 中确认类型、方法名和参数；
2. 再用 ILSpy 查看当前支持游戏版本的反编译代码，确认实际逻辑和调用顺序；
3. 优先封装成脚本自己的小函数，不要把内部访问散落在整份脚本中；
4. 游戏升级后重新核对这些封装。

类型存根只描述接口形状，不保证某个成员在当前运行路径一定安全，也不能说明具体游戏
机制。检查 PGvZ 的新增内容或已知差异时，应以当前支持版本的反编译结果为准。

### 5. IronPython 与 .NET 注意事项

- C# 枚举的 `None` 成员使用 `none_of(EnumType)`。
- IronPython 会在运行时选择 C# 重载；参数数量或 Python 类型不合适时可能选择失败。
- `.NET List`、数组和枚举对象不是普通 CPython 对象，但通常支持索引和迭代。
- 现代 Python 类型注解尽量用字符串包裹，避免 IronPython 把 `list[int]` 当作 .NET 泛型
  解析。
- 游戏对象通常只应在游戏主线程访问；注册脚本已经在主线程执行，不要另开线程修改
  Board。

### 6. 挂钩游戏方法

游戏自带的 `LawnMod` 可以挂钩 C# 方法。项目主要使用两种形式：

1. `LawnMod.MonoModUtils.HookTo` 装饰器：模块导入时注册，适合常驻钩子；
2. `LawnMod.MonoModUtils.As` 配合 `LawnMod.MonoModUtils.On`：可以通过 `+` 添加、通过
   `-` 移除，但重复添加同一个函数会导致重复执行。

包装函数的第一个参数是原方法 `orig`。实例方法随后是实例对象和原参数；静态方法没有
实例对象。是否以及何时调用 `orig` 会改变原游戏逻辑，必须阅读目标方法的当前反编译
实现后再决定。

钩子在模块导入时生效。小方法可能被运行时内联，导致挂钩看似成功但实际没有调用；遇到
这种情况应沿调用链选择更大的调用者。不要重复挂钩框架已经处理的核心更新方法。

具体写法可参考 `pgvz/__init__.py` 和 `pgvztool/hook.py`。挂钩属于高风险能力，异常、错误
签名或跳过必要的 `orig` 都可能直接使游戏崩溃。

### 7. 性能与状态安全

- 每帧脚本和钩子应尽快返回，避免在一帧内进行大量无界搜索。
- 修改游戏集合时，优先使用框架提供的存活对象迭代器；若要删除大量对象，先确认游戏
  集合在删除时的行为。
- 不要把上一关的 Board、植物或僵尸对象长期保存在全局变量中；换关后重新获取。
- 对话框、选卡界面和 Board 都可能为 `None`，访问前根据场景判断。
- 先在单一关卡和正常速度下验证，再测试倍速、暂停、切换关卡和中途重进。

## 九、参考网址

### PGvZ-TAS 项目内资料

- [安装与加载机制](install.md)
- [示例脚本说明](../scripts/README.md)
- [PGvZ 与 PvZ 的异同](pgvz-vs-pvz.md)
- [游戏速度控制机制](speed-control.md)
- [僵尸波次刷新机制与时间操作实现](zombie-spawning.md)
- [坐标系统与绘制](rendering.md)
- [TAS 功能](tas.md)
- [类型存根说明](../typings/README.md)

### 原版 PvZ 自动操作框架

以下资料用于学习原版自动操作框架的接口、术语和脚本组织方式：

- [PyVZ 脚本教程](https://pvz.tools/scripts/)
- [AvZ（AsmVsZombies）](https://github.com/vector-wlc/AsmVsZombies)

### IronPython、模组和反编译工具

- [IronPython 官方文档](https://ironpython.net/documentation/)
- [IronPython 与 .NET 集成](https://ironpython.net/documentation/dotnet/dotnet.html)
- [游戏的 `MonoModUtils` 实现](https://github.com/rspforhp/PVZdotnet-ready-to-mod/blob/master/LawnModExtension/MonoModUtils.cs)
- [MonoMod 官方文档](https://monomod.dev/)
- [ILSpy](https://github.com/icsharpcode/ILSpy)
- [PythonNetStubGenerator.Tool](https://www.nuget.org/packages/PythonNetStubGenerator.Tool/)
