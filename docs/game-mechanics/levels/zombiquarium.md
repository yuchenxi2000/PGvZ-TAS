# 僵尸水族馆的失败判定

本文依据本地 PGvZ 1.3.0、1.3.1 反编译源码。尚未核对 1.3.2–1.3.4 的实现。

## 失败条件

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
死亡但尚未移出列表的对象同样会暂时计入。此结论只针对这条失败判定，不保证其他类型僵尸在水族馆中的动画和行为正常。

`HasLevelAwardDropped()` 在 `mLevelAwardSpawned` 为真、`mNextSurvivalStageCounter > 0`
或 `mBoardFadeOutCounter >= 0` 时返回真。已生成过关奖励或进入这些结算状态后，列表为空也不会经此路径判负。

## 潜水僵尸的生成

`Challenge.ZombiquariumSpawnSnorkel()` 通过
`mBoard.AddZombieInRow(ZombieType.Snorkel, 0, 0)` 创建潜水僵尸，再随机设置其位置。
原生生成类型固定为潜水僵尸，与失败条件是否按类型计数是两回事。

## 源码导航

相对于 `E:\programming\PGvZ\PGvZ-decompilation-1.3.1`：

- `Lawn/Challenge.cs:4887`：`ZombiquariumSpawnSnorkel()`。
- `Lawn/Challenge.cs:4965`：`ZombiquariumUpdate()`，检查僵尸列表并触发失败。
- `Lawn/Board.cs:207`：`mZombies` 列表定义。
- `Lawn/Board.cs:9001`：`HasLevelAwardDropped()`。
