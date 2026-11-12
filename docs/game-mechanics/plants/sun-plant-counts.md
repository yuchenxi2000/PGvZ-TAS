# 产阳光植物数量统计

本文依据本地 PGvZ 1.3.2 反编译源码，说明 `Board.mMaxSunPlants` 的统计方式、
生命周期及其与 `CountSunFlowers()` 的区别。未核对其他支持版本，未做游戏内实测。

## `mMaxSunPlants`：种植时采样的历史峰值

它是 C# `int` 字段。唯一的玩法运行时更新位置在 `Board.AddPlant()`：

```csharp
Plant plant = NewPlant(theGridX, theGridY, theSeedType, theImitaterType);
DoPlantingEffects(theGridX, theGridY, plant, forAquarium: false);
mChallenge.PlantAdded(plant);
int num = CountPlantByType(SeedType.Sunflower)
        + CountPlantByType(SeedType.Sunshroom);
if (num > mMaxSunPlants)
{
    mMaxSunPlants = num;
}
```

`CountPlantByType()` 遍历 `Board.mPlants`，只检查 `!plant.mDead` 和原始
`plant.mSeedType == theSeedType`，不额外检查沉睡、成长阶段或是否正在生产。
因此 `mMaxSunPlants` 的准确含义是：**每次 `AddPlant` 完成创建及通知后采样，
存活向日葵与阳光菇合计数量的历史最高值**。

- 每次添加任意种类植物都会采样，并非只有种向日葵或阳光菇时才更新。
- 铲除、死亡、升级为双子向日葵等造成当前数量减少时，峰值不会降低。
- 它不统计累计种植总数。例如始终只保留一株、反复铲除再种，峰值仍可为 1。
- 它不调用 `Plant.MakesSun()`，双子向日葵、向日葵豌豆、向日葵坚果均不计入。
- 模仿者变身前原始类型为 `Imitater`，不计入；`ImitaterMorph()` 先将旧对象
  `Die()`，再经 `AddPlant()` 创建目标植物，因此变成向日葵或阳光菇后会计入。

## 采样盲区与修改器放置

`Board.NewPlant()` 只分配、初始化植物并加入 `mPlants`，不更新峰值。
例如“我是僵尸”的 `Challenge.IZombiePlacePlants()` 使用 `NewPlant()` 预放植物，
不会因此立即刷新 `mMaxSunPlants`。后续若调用一次 `AddPlant()`，才会把当时仍存活
的向日葵和阳光菇一并统计；期间已消失的植物可能完全没有被记录。

所以该字段不保证等于整个关卡每一帧的真实数量峰值。
修改器 `Placer.PlantOnBoard()` 和框架 `SetPlantOnBoard()` 使用 `AddPlant()`，
会触发此统计；清空旧阵型后也不会主动重置原来的历史峰值。

## 生命周期与保存

- `Board(LawnApp)` 构造函数将它初始化为 0；正常 `LawnApp.NewGame()` 通过
  `MakeNewBoard()` 创建新的 Board，因此开始新局时从 0 起算。
- `InitLevel()` 本身没有重置该字段。生存换轮复用 Board，`InitSurvivalStage()`
  也不清零，因此峰值跨生存轮保留。
- 当前原生存档路径通过 `Board.Sync()` 的 `SyncInt(ref mMaxSunPlants)` 保存与恢复。
  `SaveToFile()` / `LoadFromFile()` 的缓冲区序列化实现也包含该字段。
- 读档恢复的是存档里的历史值，不会重新扫描植物计算峰值。

## 当前是否影响玩法

全源码搜索 `mMaxSunPlants`，仅发现声明、构造初始化、`AddPlant()` 中的比较与更新，
以及上述序列化位置。**未发现其他玩法读取它**，包括种植限制、产阳光逻辑、阳光余额
上限、难度、成就或结算判定。因此在本次核对的实现中，它是被保留并持久化的统计字段，
没有发现修改它能改变玩法的依据。它与[阳光余额上限](../other/sun-money-limit.md)无关。

## `CountSunFlowers()`：实际参与玩法的实时数量

另一个名字相近的 `Board.CountSunFlowers()` 每次调用都遍历 `mPlants`，统计
`!plant.mDead && plant.MakesSun()`，不读取 `mMaxSunPlants`。

| 植物 | `mMaxSunPlants` 的采样口径 | `CountSunFlowers()` 的计数口径 |
|---|---|---|
| 向日葵、阳光菇 | 计入 | 计入 |
| 双子向日葵、向日葵豌豆、向日葵坚果 | 不计入 | 计入，每株算 1 |
| 未变身的模仿者、金盏花 | 不计入 | 不计入 |

两者都没有按产量折算权重，也不因植物暂时沉睡就排除它。
`CountSunFlowers()` 的实际读取点包括：

- `Board.MouseUpWithPlant()` 的教程流程：种植向日葵且实时计数为 2 时提示继续种植，
  计数达到 3 时完成相应的种植教学或补种阳光植物教学。
- `Zombie.PickBungeeZombieTarget()`：当已经瞄准产阳光植物的蹦极数恰好等于
  当前实时计数减 1 时，跳过 `MakesSun()` 为真的候选。这是该条件下避免继续选中
  剩余产阳光植物的逻辑，不依据历史峰值。

## 源码导航

以下路径相对于本地 `PGvZ-Mac/src/Lawn/`：

| 文件 | 重点 |
|---|---|
| `Lawn/Board.cs` | 构造函数、`AddPlant`、`CountPlantByType`、`NewPlant`、`CountSunFlowers`、`MouseUpWithPlant`、`InitSurvivalStage`、序列化 |
| `Lawn/Plant.cs` | `PlantInitialize`、`MakesSun`、`ImitaterMorph` |
| `Lawn/Challenge.cs` | `PlantAdded`、`IZombiePlacePlants` |
| `Lawn/Zombie.cs` | `PickBungeeZombieTarget`、`CountBungeesTargetingSunFlowers` |
| `Lawn/LawnApp.cs` | `NewGame`、`MakeNewBoard` |
| `Lawn/GlobalMembersSaveGame.cs` | `SyncGame` 调用 `Board.Sync` |
