# 僵尸波次刷新机制与时间操作实现

本文分为两部分：第一部分只说明从游戏反编译代码中确认的僵尸刷新机制；第二部分说明
PGvZ-TAS 如何基于这些机制实现 `Prejudge`、`Until` 和 `DelayA`。

相关游戏方法包括 `Board.UpdateGame`、`Board.UpdateZombieSpawning`、
`Board.SpawnZombieWave`、`Board.IsFlagWave`、`Board.PickZombieWaves` 和
`Challenge.UpdateZombieSpawning`。

## 一、游戏的僵尸刷新机制

### 1. 波次编号

`Board.mCurrentWave` 表示已经刷出的波数，同时也是下一波在
`mZombiesInWave` 中的零基索引。

`Board.SpawnZombieWave()` 按当前的 `mCurrentWave` 生成僵尸，完成后执行：

```csharp
mCurrentWave++;
mTotalSpawnedWaves++;
```

因此两套编号的对应关系是：

| 含义 | 编号 |
|---|---|
| 脚本 API 的第 `wave` 波 | 一基编号，从 1 开始 |
| 游戏内部的波数组索引 | `wave - 1` |
| 第 `wave` 波刷出以后 | `mCurrentWave == wave` |
| 判断第 `wave` 波是否为旗帜波 | `IsFlagWave(wave - 1)` |

总波数保存在 `Board.mNumWaves`。`PickZombieWaves()` 会根据关卡设置不同的总波数，
当前游戏中可见 4、6、8、10、12、20、30、40 和 60 波等配置；底层波次数组上限为
100。因此不能假定所有关卡都是 20 波。

### 2. 每个逻辑帧的刷新顺序

`Board.UpdateGame()` 在实际游戏状态下先增加 `mMainCounter`，然后调用
`UpdateZombieSpawning()`：

```text
mMainCounter += 1
    ↓
UpdateZombieSpawning()
    ↓
更新倒计时、判断刷新阈值、生成下一波
```

标准刷新流程使用两个计时器：

- `mZombieCountDown`：普通主倒计时；
- `mHugeWaveCountDown`：旗帜波警告阶段使用的大波倒计时。

`mZombieCountDownStart` 保存当前这段主倒计时的初始值，用于计算该段倒计时已经经过
多少时间。它不是波次刷出时刻。

### 3. 普通波的血量刷新阈值

标准流程每帧先令 `mZombieCountDown` 减一，然后执行以下判断：

```csharp
int elapsed = mZombieCountDownStart - mZombieCountDown;
if (mZombieCountDown > 5
    && elapsed > 400
    && TotalZombiesHealthInWave(mCurrentWave - 1) <= mZombieHealthToNextWave
    && mZombieCountDown > 200)
{
    mZombieCountDown = 200;
}
```

也就是说，满足以下条件时会触发提前刷新：

1. 当前倒计时已经运行超过 400 帧；
2. 上一波剩余僵尸血量不高于 `mZombieHealthToNextWave`；
3. 主倒计时仍大于 200。

触发后主倒计时不是继续按原值运行，而是直接跳到 200。这里的 200 是标准刷新策略的
阈值倒计时，不是实际波长。若僵尸清理较慢、直到倒计时自然进入 200 才满足血量条件，
则不会发生可见跳变，但此后同样不可能再次提前刷新。

非旗帜波在主倒计时为 5 时调用 `NextWaveComing()`，在主倒计时归零时调用
`SpawnZombieWave()`。因此刷新阈值触发以后，可以用：

```text
刷新点 = 当前 mMainCounter + 当前 mZombieCountDown
```

计算下一波的预计刷出时刻。

### 4. 刷新后的初始主倒计时

一波刷出后，游戏会为下一波设置新的 `mZombieCountDown` 和
`mZombieCountDownStart`。初始值随关卡和下一波类型变化：

| 情形 | 初始主倒计时 | 后续是否可能压到 200 |
|---|---:|---|
| 常规普通波 | `2500 + RandomNumbers.NextNumber(600)` | 是 |
| 下一波是旗帜波 | `4500` | 是 |
| `LittleTrouble`、`ChallengeColumn`、`ChallengeLastStand` 的普通分支 | `750` | 是 |
| 生存模式阶段最后一波刷出后 | `5500` | 不再对应下一波刷新 |

普通波开始时，`mZombieHealthToNextWave` 通常设为本波初始总血量的 50%～65%。下一波是
旗帜波时，该值设为 0，因此一般要把当前波清理完才会触发提前刷新。

### 5. 首波倒计时

首波没有上一波僵尸可用于血量判断，初始化时：

```text
mCurrentWave = 0
mZombieHealthToNextWave = -1
```

首波主倒计时也不是固定值：

- 通常为 1800；
- 首次冒险第二关为 5000；
- 生存模式后续阶段为 600；
- `Challenge.StartLevel()` 或教程状态还可能设为 100、200、99、999、2400、4000、
  4500、5500 等值。

所以首波不能固定使用某个模式下的 599。只有确认主倒计时已经实际开始逐帧递减后，
才能用当时的实时倒计时建立首波刷新点。

### 6. 旗帜波

`Board.IsFlagWave()` 接受零基波号。通常每 10 波一次；首次冒险且总波数不足 10 时，
`GetNumWavesPerFlag()` 返回总波数，使该关最后一波成为旗帜波。首次冒险第一关是例外，
没有旗帜波。

当即将刷出的波是旗帜波时，主倒计时到 5 后不会继续归零，而是：

```csharp
mHugeWaveCountDown = 750;
return;
```

随后主倒计时停在 5，大波倒计时每帧减一。大波倒计时归零的同一帧，游戏先把主倒计时
设为 1，随后再减为 0 并刷新旗帜波。

因此旗帜波的可靠锚点是“大波倒计时刚刚启动”这一事件。事件发生后可以用：

```text
刷新点 = 当前 mMainCounter + 当前 mHugeWaveCountDown
```

计算刷出时刻。旗帜波不能只硬编码为第 10、20 波，也不需要在框架中复制 750；应读取
游戏实际启动的大波倒计时。

### 7. 关闭或接管标准刷新的模式

`Challenge.UpdateZombieSpawning()` 可以阻止 `Board.UpdateZombieSpawning()` 继续执行
标准逻辑：

- 锤僵尸使用独立的 `WhackAZombieSpawning()`；
- Boss、冰冻关、禅境花园、智慧树、水族馆、我是僵尸、松鼠和砸罐子等模式关闭标准
  刷新流程；
- 坚不可摧在进入进攻阶段前暂停标准刷新，进入进攻阶段后恢复标准流程。

这些被挑战逻辑永久接管的模式没有统一的标准刷新阈值，不适用本文后半部分的时间 API
实现。

## 二、PGvZ-TAS 的时间操作实现

### 1. 实现范围

当前实现在 `pgvz/time_operation.py` 中，仅支持使用标准
`Board.UpdateZombieSpawning()` 流程的关卡。

以下约束是有意保留的：

- `Prejudge`、`Until` 和 `DelayA` 的公开调用方式不变；
- 波号仍使用从 1 开始的一基编号；
- `refresh_point` 和 `prev_until_time` 仍为模块级状态；
- 不为并行脚本建立独立时间轴；
- 脚本管理器仍可同时加载多个脚本或动态插入脚本，波次记录不依赖某个脚本提前注册。

永久关闭标准刷新的关卡调用 `Prejudge` 时，会设置 `gvar.timePassed = True` 并记录不支持
警告，不会无限等待。

### 2. 原实现的问题

重构前最后一个仍保留原 `refresh_time` 实现的仓库版本是 Git 短提交哈希
`d013427` 的版本（完整哈希 `d01342710a8ee4f28e2ae2ff6675fabc06c9a0ae`，提交时间
2026-08-15，提交说明 `发布1.10.1并新增工具快捷键`）。

可以用以下命令查看原始版本：

```bash
git show d013427:pgvz/time_operation.py
```

原实现使用固定数组：

```python
refresh_time = [
    599, 200, ..., 750,
    200, 200, ..., 750,
]
```

其中各项表示刷新阈值触发时使用的剩余倒计时，而不是完整波长。该实现存在以下问题：

1. 数组只有 20 项，30、40、60 波关卡会越界；
2. 只把第 10、20 波视为旗帜波；
3. 首波固定为无尽模式使用的 599，不能反映其他关卡的真实首波倒计时；
4. 旗帜波大波倒计时固定为 750，没有读取游戏运行时状态；
5. 非标准刷新模式可能被错误地当作标准旗帜波处理；
6. `wave > mNumWaves` 时可能永久等待。

原来的 `Prejudge` 还有一个独立问题。目标波已经刷出时，它使用：

```python
delta_time = board.mZombieCountDownStart - board.mZombieCountDown
refresh_point = board.mMainCounter - delta_time
```

反推该波的刷新点。但目标波刷出以后，当前计时器已经属于下一波；如果这个计时器曾从
较大值直接跳到 200，上述差值会把倒计时跳变误认为真实经过的帧数。进入下一旗帜波的
大波倒计时阶段时，主倒计时还会停在 5，也无法反映真实经过时间。因此已刷出波次必须
使用事先记录的真实刷新点，不能从当前倒计时反推。

### 3. `WaveClock` 保存的状态

当前实现新增了一个全局 `WaveClock`。它按对局保存两类数据：

```text
thresholds[wave] = (触发时的 mMainCounter, 剩余倒计时, 触发来源)
refresh_points[wave] = 该波实际刷出时的 mMainCounter
```

对局键由以下字段组成：

```text
(mGameID, 游戏模式, mLevel, mBoardRandSeed, mSurvivalStage)
```

加入 `mSurvivalStage` 是为了区分同一个生存模式对局中的不同阶段。记录器独立于脚本
对象存在，因此稍后动态插入的脚本也能读取此前已经记录的阈值和刷新点。

### 4. 记录器的驱动位置

项目原本已经 hook 了 `Board.UpdateGame` 来驱动 `script_manager`。当前实现复用这个 hook：

```python
script_manager.Manage()
snapshot = wave_clock.Snapshot(board)
orig(board)
wave_clock.ObserveUpdate(board, snapshot)
```

快照在所有脚本运行以后、游戏本帧逻辑运行以前取得。`orig(board)` 返回后，记录器比较
更新前后的：

- `mMainCounter`；
- `mCurrentWave`；
- `mZombieCountDown`；
- `mHugeWaveCountDown`。

这样既能看到脚本本帧操作所造成的血量变化，又能准确观察随后发生的刷新阈值和波次
切换。记录逻辑附着在游戏更新 hook 上，不要求 `Prejudge` 或某个脚本一直运行。

### 5. 阈值事件的识别

#### 首波

当 `mCurrentWave == 0`、`mZombieHealthToNextWave == -1`，并且第一次观察到主倒计时与
`mMainCounter` 同步前进时，记录当时的实时主倒计时。由此计算出的首波刷新点为：

```text
触发帧的 mMainCounter + 触发帧的 mZombieCountDown
```

教程或关卡逻辑暂停倒计时时不会记录首波锚点，因为此时主计数器和倒计时没有同步
前进。

#### 标准普通波

记录器先根据主计数器的增量计算正常情况下本帧结束后的倒计时：

```text
expected = before_countdown - (after_main_counter - before_main_counter)
```

若实际倒计时小于 `expected`，说明本帧发生了非线性下降，即刷新阈值触发。记录器保存
游戏实际写入的剩余倒计时。

如果没有发生跳变，但倒计时已经自然进入 200 或更小的稳定区间，并且本帧确实正常
递减，也会补记阈值。代码中的 `STANDARD_REFRESH_COUNTDOWN = 200` 表示
`Board.UpdateZombieSpawning()` 的标准规则，不再按波次重复展开为数组。

#### 旗帜波

是否为旗帜波由 `board.IsFlagWave(wave - 1)` 判断。记录器在以下任一情形记录运行时大波
倒计时：

- `mHugeWaveCountDown` 从 0 变为正数，即本帧刚启动大波倒计时；
- 模组或脚本从已有大波倒计时的存档继续运行，并观察到它正常递减。

因此第 30、40、50、60 波以及不足 10 波关卡的最终旗帜波都使用同一套逻辑。

#### 实际刷出

若 `orig(board)` 返回后 `mCurrentWave` 增加，说明本帧有波次实际刷出。记录器直接把此时
的 `mMainCounter` 保存为该波真实刷新点。由于 `mMainCounter` 在调用
`UpdateZombieSpawning()` 前已经增加，这个值就是刷新发生的逻辑帧，不需要额外加减 1。

### 6. `Prejudge` 的执行流程

`Prejudge(rel_time, wave)` 现在按以下顺序运行：

1. 检查当前关卡是否使用标准刷新逻辑；
2. 检查 `1 <= wave <= board.mNumWaves`；
3. 若 `mCurrentWave > wave`，说明目标时间已经过去；
4. 若 `mCurrentWave == wave`，读取 `refresh_points[wave]`；
5. 若目标波尚未刷出，先等待 `mCurrentWave == wave - 1`，再等待该波的阈值记录；
6. 根据阈值记录计算 `refresh_point`；
7. 等待到 `refresh_point + rel_time`。

计算公式统一为：

```text
refresh_point = trigger_main_counter + trigger_remaining
wait_time = refresh_point + rel_time - current_main_counter
```

若请求的负时间早于阈值触发时刻，`wait_time` 已经为负，现有 `Delay` 会设置
`gvar.timePassed = True`。这与旧 API 的过时操作处理方式一致。

目标波已经刷出、但当前进程没有该波真实刷新点记录时，`Prejudge` 不再进行不可靠的
倒计时反推，而是标记操作已过时并输出缺少记录的警告。

### 7. `Until` 和 `DelayA`

`Until(t)` 与 `DelayA(t)` 的行为没有改变：

- `Prejudge` 先确定当前波的 `refresh_point`；
- `Until(t)` 等待到该刷新点后的相对时间 `t`；
- `DelayA(t)` 通过 `prev_until_time` 把相对延迟换算成下一个 `Until` 时间点。

因此脚本仍应遵循原来的调用方式：先调用 `Prejudge`，再调用 `Until` 或 `DelayA`。

### 8. 中途退出重进

游戏存档会保存 `mGameID`、`mMainCounter`、`mCurrentWave`、主倒计时和大波倒计时等字段。
同一进程内退出并重新进入同一存档时，`WaveClock` 可以通过对局键找到此前记录的真实
刷新点，避免使用当前倒计时反推。

如果游戏进程已经重启，或者模组在某波刷出以后才首次加载，内存中没有该波的真实
刷新点。此时无法从游戏现有字段可靠恢复历史刷新时刻，`Prejudge` 会明确报告缺少记录。

### 9. 验证覆盖

`tests/test_time_operation.py` 使用模拟 Board 状态覆盖了：

- 首波使用运行时倒计时；
- 普通波血量阈值导致的倒计时跳变；
- 普通波自然进入 200 稳定区间；
- 第 30 波使用运行时大波倒计时；
- 波次实际刷出时记录精确刷新点；
- 下一波倒计时跳到 200 后，`Prejudge` 仍使用已记录刷新点；
- 非法波号立即结束；
- 关闭标准刷新逻辑的模式被拒绝。
