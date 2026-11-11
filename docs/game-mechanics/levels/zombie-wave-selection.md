# 自然出怪的种类抽取与随机数控制

本文依据本地 PGvZ 1.3.0、1.3.1 的 `Board.cs`、`Challenge.cs`、
`Sexy/RandomNumbers.cs`，记录自然出怪的种类选择与修改器接入方式。
波次刷出的时机另见[僵尸波次刷新机制](zombie-spawning.md)。

## 游戏的选择流程

`Board.InitZombieWaves()` 先清空 `mZombieAllowed`，按模式确定允许的种类，再调用
`PickZombieWaves()` 填充实际波次。它还重置当前波次、倒计时等状态，因此应在选卡期间
使用，不能当作只修改未来波次的接口。

普通生存调用 `Challenge.InitZombieWavesSurvival()`：

1. 默认允许普通僵尸。
2. 调用 `RandomNumbers.NextNumber(5f)`，取整后为 0 时选报纸，否则选路障。
3. 设置随机种类名额 `min(mSurvivalStage + 1, 9)`；部分场景、地狱模式会调整名额或
   预先加入其他种类。
4. 循环调用 `RandomNumbers.NextNumber(40)`，把返回值当作 `ZombieType`。
   候选必须尚未允许，且通过场景、轮数、模式和类型限制，才会加入允许列表并消耗名额。
5. 继续抽取，直到随机名额用完。

冰车和巨人需要 `GetSurvivalFlagsCompleted() >= 4`，红眼巨人需要至少 10 面旗帜。
泳池无尽在每轮 20 波、每旗 10 波时，每完成一轮累计两面旗帜；4098 旗帜对应的轮数
早已满足冰车门槛。墓碑场景则仍会排除冰车。

随机挑战调用 `InitZombieWavesChallengStageRandom()`，也用整数上限 40 抽取种类，
但没有路障/报纸的浮点二选一，并且有自己的类型限制和巨人类数量上限。

冒险、固定小游戏及自定义关卡可能使用关卡表、固定列表或
`InitZombieWavesSurvivalComponent()`。自定义生存组件抽取的是候选列表的索引，不能
把僵尸枚举编号直接当作索引传入。修改器不把这些流程冒充普通生存抽取流程。

## 原实现失效的两个独立问题

原 `SetZombies()` 把报纸二选一的 0/1 和勾选的僵尸编号放进同一个队列，再依赖
`pgvz/rng.py` 的 `NextNumber()` 和 `NextNumber(Int32)` 钩子按调用顺序消费。

- 游戏二选一实际调用 `NextNumber(Single)`，原钩子没有覆盖这个重载。0/1 因此留在
  整数队列里，被后面的种类抽取消费；1 恰好是旗帜僵尸编号，会占用一个随机名额。
  随机挑战本来就不需要这个前缀。
- `RandomNumbers.NextNumber(Int32)` 很短，可能已被 JIT 内联进出怪调用者。之后再给
  `NextNumber` 装钩子，不会替换调用者里已经内联的代码。此时波次重建和预览刷新仍然
  执行，但候选队列完全没有被使用。其他调用处的随机数钩子正常，并不能排除这个问题。

本地验证用真实 IronPython 3.4、.NET 6 和 MonoMod，先预热标记为可内联的随机数调用者，
再安装整数随机数钩子：重新执行调用者时，钩子调用计数为 0。改写调用处后，多次只选
冰车均能加入允许列表。这个验证使用模拟关卡，没有加载实际游戏或用户存档。

## 当前接入方式

`pgvz/set_zb.py` 的 `InitNaturalZombieWaves()` 在一次操作期间用 `ILHook` 改写
`InitZombieWavesSurvival()` 和 `InitZombieWavesChallengStageRandom()` 中的随机调用：

- 整数委托只在上限为 `ZombieTypesCount` 时，按传入顺序提供勾选的种类。候选仍经过
  原生游戏规则筛选；队列用完以后恢复游戏随机数，补齐剩余名额。
- 浮点委托单独处理上限 5 的路障/报纸二选一，不占用种类抽取队列。
- 波次权重计算、预览动画及其他调用者不消费这些候选。名额不足时，未消费的选择也
  不会泄漏到后续波次随机调用。
- 所有临时 `ILHook` 均在 `finally` 中释放，包括原生初始化失败或第二个钩子安装失败。

直接修改调用者中的调用点，可以避开先前已经内联的随机数代码，不需要给全局浮点
随机数增加常驻钩子。路灯花必定变身等选项继续使用各自的随机数控制。

自然出怪仍不保证任意勾选组合全部出现：类型可能被原生规则拒绝、已由必出组加入，
或超过本轮随机种类名额。强制出怪仍直接设置 `mZombieAllowed` 并调用 `PickZombieWaves()`。

## 源码与测试导航

| 文件 | 关注内容 |
|---|---|
| `Lawn/Board.cs` | `InitZombieWaves`、`PickZombieWaves`、`GetSurvivalFlagsCompleted` |
| `Lawn/Challenge.cs` | 普通生存、随机挑战、自定义生存组件的种类选择 |
| `Sexy/RandomNumbers.cs` | 无参数、`Int32`、`Single` 三种随机数重载 |
| `pgvz/set_zb.py` | 临时调用点改写和预览刷新 |
| `tests/test_set_zb.py` | 4098 旗帜只选冰车、报纸二选一、游戏过滤与异常清理 |
