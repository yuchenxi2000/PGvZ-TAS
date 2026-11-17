# 僵尸水族馆的失败判定与投喂

本文依据本地 PGvZ 1.4.3 反编译源码核对；早期版本 1.3.0、1.3.1 的僵尸列表清空判负逻辑相同。

## 失败条件

水族馆既有专用的僵尸列表清空判负，也可能进入普通僵尸的左边界判负。
“还有健康僵尸”只能排除列表清空，不能排除后一条路径。

### 僵尸列表清空

`Challenge.ZombiquariumUpdate()` 开头直接检查场地僵尸列表是否为空：

```csharp
if (mApp.mBoard.mZombies.Count == 0 && !mBoard.HasLevelAwardDropped())
{
    mBoard.ZombiesWon(null);
    return;
}
```

这里没有检查 `mZombieType`，也没有按潜水僵尸、敌我阵营、血量或死亡阶段筛选。
`Board.mZombies` 是 `List<Zombie>`，因此判断依据是列表内的对象数量，而不是存活潜水僵尸数量。

所以，通过修改器加入的其他种类僵尸，只要仍在 `mZombies` 中，也会阻止这条“僵尸耗尽”失败路径；
死亡但尚未移出列表的对象同样会暂时计入。此结论只针对这条失败判定。

`HasLevelAwardDropped()` 在 `mLevelAwardSpawned` 为真、`mNextSurvivalStageCounter > 0`
或 `mBoardFadeOutCounter >= 0` 时返回真。已生成过关奖励或进入这些结算状态后，列表为空也不会经此路径判负。

### 普通僵尸越过左边界

`Zombie.CheckForBoardEdge()` 仅对僵王或 `mZombieHeight == ZombieHeight.Zombiquarium`
直接返回，没有按水族馆游戏模式整体跳过。其他僵尸达到其种类对应的左边界，且仍有头
或满足无头存活条件时，在非我是僵尸模式下调用 `mBoard.ZombiesWon(this)`。
这条路径不要求场上僵尸耗尽，也不要求生命值降到饥饿阈值。

`Board.ZombiesWon()` 按当前游戏模式选择提示语。水族馆模式一律使用
`[ZOMBIQUARIUM_DEATH_MESSAGE]`，没有根据调用者是列表清空还是越界区分提示。
因此看到水族馆失败提示不能反推所有僵尸已经饿死。

## 随机僵尸卡片全屏放置的风险

`Plant.ImitaterMorph()` 对 `ImitaterRandomZombie` 调用
`Challenge.IZombiePlaceZombie(GetRandomZombieType(), col, row)`；后者经
`AddZombieInRow()` 创建，再将一般僵尸放到 `GridToPixelX(col, row) - 30`。
随机池包含多种非潜水僵尸，并不只选适合水族馆的类型。

`ZombieInitialize()` 的水族馆分支会给在场僵尸设置
`mZombieHeight = Zombiquarium`、`mZombiePhase = ZombiquariumDrift`、本体血量 200。
这说明随机僵尸最初确实会获得水族馆状态，但它们后续仍执行常规检查与各类型行为。

一个明确的状态覆盖路径是：

1. 水族馆背景的地形初始化仍将第 3、4 行（内部索引 2、3）设为泳池格。
2. `Zombie.UpdatePlaying()` 依次执行 `UpdateActions()`、`UpdateZombiePosition()`、
   `CheckIfPreyCaught()`、`CheckForPool()`、`CheckForHighGround()` 和 `CheckForBoardEdge()`。
3. `CheckForPool()` 没有排除水族馆状态。普通、路障、铁桶等能入泳池的种类，在泳池格
   满足位置条件且 `!mInPool` 时，会改成 `mZombieHeight = InToPool`；随后可变为
   `ZombieNormal`。原生潜水僵尸因类型被该方法直接排除，不走这条覆盖路径。
4. 高度状态一旦被覆盖，左边界检查就不再以水族馆状态豁免它。全屏放置包含左侧格子，
   只需其中一只满足左边界条件便会调用失败，即使其本体血量仍高、其他僵尸也都存在。

这是能解释“随机僵尸全屏放置，过一会儿仍有健康僵尸却失败”的源码路径；
尚未捕获用户该次失败时具体触发判负的僵尸。模仿者先经历变身再生成僵尸，
所以放置和失败之间的延迟也不一定是饥饿倒计时。

正常水族馆游动状态下，`UpdateZombiquarium()` 每 100 个僵尸年龄计数造成 10 点伤害，
血量不高于 150 时可寻找饲料，血量低于 100 时有饥饿颜色提示。这些阈值不是直接的
关卡判负条件。高度状态被覆盖后，饥饿扣血、颜色及游动行为也可能不再沿水族馆路径执行。

## 潜水僵尸的生成

`Challenge.ZombiquariumSpawnSnorkel()` 通过
`mBoard.AddZombieInRow(ZombieType.Snorkel, 0, 0)` 创建潜水僵尸，再随机设置其位置。
原生生成类型固定为潜水僵尸，与失败条件是否按类型计数是两回事。

## 投喂与修改器数量开关（1.4.3）

以下根据本地 `PGvZ-decompilation-1.4.3` 的 `Lawn/Challenge.cs` 核对。
原生 `ZombiquariumMouseDown()` 将输入坐标乘以 `Constants.IS` 并取整，
仅允许在 X 为 `80 - BOARD_EXTRA_ROOM` 至 720、Y 为 90 至 430 的区域投喂。
场上存活 `Brain` 少于 3 个且成功扣除 5 阳光后，调用 `ZombiquariumDropBrain()`。
创建方法在投喂位置减去 `(15, 15)` 绘制脑子，保留原生提示清除、渲染顺序和音效。

修改器“特性修改”的“水族馆脑子无上限”（`zombiquariumNoBrainLimit`）默认关闭，
支持选项同步及 PC 保存。钩子位于 `pgvztool/hook.py`，只跳过上述数量检查，
保留区域、缩放、阳光消耗及原生创建方法。关闭开关会恢复原生入口；
不会删除已有脑子，场上数量仍不低于 3 时原生入口会拒绝继续投喂。

水族馆的原生更新逐个处理脑子：每次更新计数器加 1、
Y 加 0.15，Y 达到 500 时删除。饥饿僵尸只追踪计数器至少为 15 的饲料。
通用场地物品列表不提供脑子选项。

## 源码导航

相对于 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3`：

- `Lawn/Challenge.cs`：`ZombiquariumSpawnSnorkel()`、`ZombiquariumUpdate()`、`IZombiePlaceZombie()`。
- `Lawn/Plant.cs`：`ImitaterMorph()`，随机僵尸类型抽取与创建。
- `Lawn/Zombie.cs`：`ZombieInitialize()`、`UpdatePlaying()`、`CheckForPool()`、
  `CheckForBoardEdge()`、`UpdateZombiquarium()`、`ZombiquariumFindClosestBrain()`。
- `Lawn/Board.cs`：`PickBackground()`、`ZombiesWon()`、`HasLevelAwardDropped()`。
