# 游戏速度控制机制

PGvZ 中存在两套相互独立的速度控制：`LawnApp.UpdateFrames()` 使用全局快慢速变量控制整个
应用更新，`Board.Update()` 使用分子/分母控制当前关卡内部的游戏逻辑更新。两者可以同时
生效，但作用层级和生命周期不同。

本文依据当前支持游戏版本的反编译代码整理，主要涉及：

- `Lawn/LawnApp.cs`：`LawnApp.UpdateFrames()`
- `Lawn/Board.cs`：`Board.Update()`、`AccelerationIncrease()`、`AccelerationDecrease()`
- `Lawn/ZBCheatDialog.cs`：`ChangeGameSpeed()`
- `Sexy/GlobalStaticVars.cs`：全局快慢速字段
- `pgvz/speed.py`：公开速度 API、范围校验和连分数转换

## 两套控制的区别

| 项目 | 全局速度 | 关卡内速度 |
|---|---|---|
| 状态 | `gFastMo`、`gSlowMo`、`gFastSlowMoNum`、`gSlowMoCounter` | `mAccelerationNumerator`、`mAccelerationDenominator`、`mAccelerationFrameIndex` |
| 执行位置 | `LawnApp.UpdateFrames()` | `Board.Update()` |
| 作用范围 | 整个应用的 Widget 更新，包括菜单和 Board | 当前 Board 中由内层循环驱动的游戏逻辑 |
| 可表达速度 | 正整数倍或正整数倒数倍 | 非负有理数 `Numerator / Denominator` |
| 生命周期 | 静态全局状态，换关后保留，重启游戏后重置 | Board 实例状态，换关后随 Board 销毁 |
| 公开 API | `GetGlobalSpeedExact()`、`GetGlobalSpeed()`、`SetGlobalSpeedExact()`、`SetGlobalSpeed()` | `GetBoardSpeedExact()`、`GetBoardSpeed()`、`SetBoardSpeedExact()`、`SetBoardSpeed()` |

## 公开 API 与范围

速度 getter 和 setter 都由 `from pgvz import *` 导出：

| API | 输入方式 | 返回值 |
|---|---|---|
| `GetGlobalSpeedExact()` | 读取全局快慢速变量 | 游戏实际采用的 `(is_fast, factor)` |
| `GetGlobalSpeed()` | 读取并换算全局快慢速变量 | 浮点速度 |
| `SetGlobalSpeedExact(is_fast, factor)` | 直接指定全局快/慢模式和整数因子 | `(is_fast, factor)` |
| `SetGlobalSpeed(speed)` | 浮点数转换为整数倍或整数倒数倍 | 实际 `(is_fast, factor)` |
| `GetBoardSpeedExact(board=None)` | 读取 Board 原始字段 | `(numerator, denominator)` |
| `GetBoardSpeed(board=None)` | 读取并计算 Board 比例 | 浮点速度 |
| `SetBoardSpeedExact(numerator, denominator, board=None)` | 直接指定 Board 分子和分母 | 原样 `(numerator, denominator)` |
| `SetBoardSpeed(speed, max_error=1e-6, board=None)` | 连分数近似浮点速度 | 实际 `(numerator, denominator)` |

所有设置的实际速度必须位于闭区间 `[0.01, 100]`。`SetBoardSpeedExact()` 不会约分，以便
调用者直接控制游戏字段；两个浮点入口返回实际转换结果，调用者不应假设输入的小数能够被
底层机制原样表示。

## 全局速度

### 更新层级

正常调用链为：

```text
SexyAppBase.UpdateApp()
  → DoUpdateFrames()
    → LawnApp.UpdateFrames()
      → SexyAppBase.UpdateFrames()
        → WidgetManager.UpdateFrame()
```

`LawnApp.UpdateFrames()` 在调用基类更新前决定本次执行多少次。其逻辑可简化为：

```python
update_count = 1

if gSlowMo:
    gSlowMoCounter += 1
    if gSlowMoCounter >= (gFastSlowMoNum or 4):
        gSlowMoCounter = 0
    else:
        update_count = 0
elif gFastMo:
    update_count = gFastSlowMoNum or 20

for _ in range(update_count):
    base.UpdateFrames()
```

因此：

- `gFastMo = True, gFastSlowMoNum = N`：每次外层更新执行 `N` 次应用更新，即 `N` 倍速；
- `gSlowMo = True, gFastSlowMoNum = N`：每 `N` 次外层更新只执行一次应用更新，即 `1/N` 倍速；
- `gFastSlowMoNum == 0` 时，快慢速的游戏默认值分别为 `20` 和 `1/4`；
- 两个开关都关闭时为正常 `1` 倍速。

因为这一层包围 `WidgetManager.UpdateFrame()`，它不仅影响关卡逻辑，也影响菜单、界面、场景
切换以及 Board 外部的其他 Widget 更新。但它并不包围 `LawnApp.UpdateFrames()` 中的所有
代码：加载画面走提前返回分支，`UpdatePlayTimeStats()` 也在快慢速循环之外，不能简单理解为
进程内每一项计时都会按相同比例变化。

### 全局公开 API

精确入口直接接受快慢速模式和整数因子：

```python
SetGlobalSpeedExact(True, 5)   # 5 倍。
SetGlobalSpeedExact(False, 5)  # 1/5 倍。
```

设置时会同步写入 `gFastMo`、`gSlowMo` 和 `gFastSlowMoNum`，并把 `gSlowMoCounter` 重置为
`0`，使新的慢速周期从确定相位开始。

`GetGlobalSpeedExact()` 按照 `LawnApp.UpdateFrames()` 的真实判断顺序读取状态：慢速优先于
快速；启用慢速或快速但 `gFastSlowMoNum == 0` 时，分别返回游戏默认的 `(False, 4)` 或
`(True, 20)`；两个开关都关闭时返回规范化的一倍速 `(True, 1)`。`GetGlobalSpeed()` 再把
该结果换算成浮点数。

浮点入口沿用旧网页修改器的转换规则：

```python
is_fast = speed >= 1.0
factor = round(speed) if is_fast else round(1.0 / speed)
SetGlobalSpeedExact(is_fast, factor)
```

因此这套表示只能精确表达：

```text
..., 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, ...
```

传入其他小数会先换算再取整。例如 `SetGlobalSpeed(1.6)` 返回 `(True, 2)`，不能作为精确的
`8/5` 速度使用。当前网页提供的 `0.1、0.2、0.5、1、2、5、10` 都能被这套表示精确表达。

`SetGlobalSpeed(1)` 的实际效果是正常速度，但按照原转换规则会写入 `(True, 1)`，而不是
同时关闭快慢速开关。

游戏内置的 `ZBCheatDialog.ChangeGameSpeed()` 也使用这套全局变量，提供 `1/4、1/2、1、2、
3、4、5、10` 倍等固定选项。

## 关卡内分数速度

### 状态和默认值

每个新 Board 的默认状态为：

```text
mAccelerationNumerator   = 1
mAccelerationDenominator = 1
mAccelerationFrameIndex  = 0
```

目标速度为：

```text
speed = mAccelerationNumerator / mAccelerationDenominator
```

这三个字段属于 Board。进入新关卡创建新 Board 后会恢复 `1/1`，不会继承上一关的设置。

### 分数帧分配算法

一次 `Board.Update()` 不一定执行一次 `Board.UpdateGame()`。设：

- `N = mAccelerationNumerator`
- `D = mAccelerationDenominator`
- `k = mAccelerationFrameIndex`

本次执行的游戏逻辑帧数为：

```text
steps(k) = floor(N × (k + 1) / D) - floor(N × k / D)
```

随后 `k` 加一并对 `D` 取模。连续 `D` 次 Board 更新执行的总帧数为：

```text
Σ steps(k), k=0..D-1
= floor(N × D / D) - floor(0)
= N
```

因此算法不是长期近似，而是在每个长度为 `D` 的周期内精确分配 `N` 个游戏逻辑帧：

| 设置 | 每个周期的 `steps` 序列 | 平均速度 |
|---|---|---|
| `1/2` | `0, 1` | `0.5` |
| `2/3` | `0, 1, 1` | `0.666…` |
| `3/2` | `1, 2` | `1.5` |
| `5/3` | `1, 2, 2` | `1.666…` |
| `2/1` | 每次都是 `2` | `2` |

小于 `1` 时，一部分 Board 更新会跳过游戏逻辑；大于且不为整数时，不同 Board 更新会交替
执行不同数量的游戏逻辑帧。分配方式类似误差累积，但反编译实现直接使用上述两个整数除法
结果之差。

### 精确设置 API

使用 `SetBoardSpeedExact()` 可以原样写入分子和分母：

```python
SetBoardSpeedExact(3, 2)
```

得到 `3/2 = 1.5` 倍关卡逻辑速度。函数先临时把分母设为 `1`，再写分子、清零
`mAccelerationFrameIndex`，最后启用新分母，避免写入过程中出现非法分母或新分数沿用旧
相位。它不自动约分，例如 `SetBoardSpeedExact(6, 4)` 会原样保留 `6/4`。

API 会强制以下约束：

- 分子和分母都必须是正整数；暂停不通过速度 API 表达；
- `numerator / denominator` 必须在 `[0.01, 100]` 内；
- 必须满足 `numerator × denominator <= 2147483647`，保证游戏在计算周期末尾的乘法不会
  超出 C# `int`；
- 不在关卡内且没有显式传入 Board 时抛出 `RuntimeError`。

`GetBoardSpeedExact()` 原样返回 Board 字段，便于诊断速度 API 以外的代码写入的状态，不对
范围和正负数做校验。`GetBoardSpeed()` 计算浮点比例；原始分母为 `0` 时抛出 `ValueError`。

底层游戏代码仍允许直接把分子设为 `0`。此时 `Board.Update()` 会进入与手动暂停相同的提前返回分支，不执行
`UpdateGame()`，但仍会更新正在收集的掉落物以及鼠标预览和光标对象，因此它并不等价于
停止整个应用更新。公开速度 API 为避免混用暂停与速度语义，不接受分子 `0`。

### 浮点数与连分数转换

`SetBoardSpeed(speed, max_error=1e-6)` 使用连分数收敛分数。设第 `k` 项系数为 `aₖ`，分子
和分母递推为：

```text
pₖ = aₖpₖ₋₁ + pₖ₋₂
qₖ = aₖqₖ₋₁ + qₖ₋₂
```

每得到一个正收敛分数就检查：

```text
abs(pₖ / qₖ - speed) < max_error
```

第一个满足严格误差条件的分数会交给 `SetBoardSpeedExact()`。转换最多展开 64 项；如果在
满足误差以前出现 `pₖ × qₖ > 2147483647`，或双精度浮点展开结束仍未满足要求，会抛出
`OverflowError`，且不会修改 Board。`max_error` 必须是有限正数。

例如 `SetBoardSpeed(1.5)` 精确得到 `(3, 2)`；无理数则会继续展开，直到误差小于调用者
给定的值。

### 游戏内加速按钮

关卡右上角的加速按钮调用 `AccelerationIncrease()` 或 `AccelerationDecrease()`：

- 正向循环：`1 → 2 → 3 → 1`；
- 反向循环：`1 → 3 → 2 → 1`；
- 每次都会把分母设回 `1`，并把 `mAccelerationFrameIndex` 清零。

所以按钮本身只提供 `1、2、3` 三档整数速度，但 Board 的底层算法支持任意合法分数。直接
设置分数后再点击加速按钮，会丢失自定义分母。绘制逻辑只为 `1/1、2/1、3/1` 和暂停提供
专用图标；其他比例会显示问号图标和格式化后的分数值。

## 两套速度叠加

全局速度在外层决定执行多少次 `WidgetManager.UpdateFrame()`，关卡内速度在每次
`Board.Update()` 内决定执行多少次 `Board.UpdateGame()`。因此对核心关卡逻辑而言，长期
平均速度近似为两者乘积：

```text
effective_game_speed = global_speed × N / D
```

但两套设置不能完全互换：

- 全局速度会影响菜单、Widget 和 Board 外围更新；
- 关卡内速度只包围 `UpdateGridItems()`、`UpdateGame()`、`Challenge.Update()` 等内层关卡
  逻辑，Board 中位于该循环外的按钮、镜头、提示和部分特效更新仍按 Board 更新频率运行；
- `pgvz` 在 `Board.UpdateGame` 钩子中推进普通脚本，所以两套加速最终产生的每个游戏逻辑帧
  都会推进一次脚本；被分数速度跳过或暂停的 Board 更新不会推进该钩子；
- 全局速度换关后仍然存在，Board 分数速度换关后恢复默认值。

选择速度入口时，如果希望菜单和场景切换也一起变化，使用全局速度；如果只希望精确控制
当前关卡、尤其需要 `2/3`、`3/2` 等分数速度，使用 Board 分子/分母。
