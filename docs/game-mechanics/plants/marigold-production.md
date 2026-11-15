# 金盏花产出与三颗钻石

本文依据本地 PGvZ 1.4.3 反编译源码静态核对，未在游戏中实测。

## 概率与产出

`Plant.UpdateProductionPlant()` 在金盏花生产触发时调用
`RandomNumbers.NextNumber(20000)`，返回值范围为 0–19999：

| 随机值 | 概率 | 产出 |
|---|---|---|
| 0–1999 | 10% | 1 枚金币。 |
| 2000 | 0.005%，即 1/20000 | 3 颗钻石。 |
| 2001–19999 | 89.995% | 1 枚银币。 |

三种结果分别选择 `anim_producing2`、`anim_producing3`、`anim_producing`；
钻石结果还播放新增的 `PlantVoice.VoiceType.Diamond`。

选定结果后，将掉落种类暂存于 `mGravebusterDrop`，进入
`PlantState.MarigoldProducing`，设置 `mStateCountdown = 190`。
倒计时结束后调用 `Board.AddCoinForDropLootType(..., CoinMotion.FromPlant)`，
才真正生成掉落物，并将状态设回 `Notready`。概率是每次生产触发的概率，
不能解读成每个游戏帧的概率。

`DropLootType.ThreeDiamonds = 12` 是组合掉落类型，不是新面额的 `CoinType`。
`Board.AddCoinForDropLootType` 分别在 X 偏移 -20、-40、-60 处创建
3 个普通 `CoinType.Diamond`。全局检索这份源码，金盏花是选择该组合掉落的业务路径。

## 其他边界

- 新生产状态让产出与动画分阶段执行；生产状态中不继续递减下一轮的 `mLaunchCounter`。
- 金盏花末波的原有停产逻辑仍在，但新生产状态也参与末波状态判断；
  不宜仅凭仍存在 `MarigoldEnding` 就假定边界行为与旧版完全一致。
- `ChallengeBigTime` 还会额外生成一枚银币，这是独立于上述随机结果的分支。
- 图鉴立绘的移动端遮挡与生产机制无关，见 [1.4.3 代码核对](../other/game-1.4.3-changes.md)。

## 修改器开关

“特性修改”中的“金盏花必产三颗钻石”对应
`CheatOption.marigoldAlwaysThreeDiamonds`，默认关闭，支持 GUI 同步与 PC 选项保存。
钩子位于 `pgvztool/hook.py` 的 `Plant__UpdateProductionPlant`：原生生产状态机照常运行，
进入生产状态后将待掉落类型改为三颗钻石，并选择钻石动画和语音；结算前再次设置待掉落
类型，因此中途开启也能影响尚未结算的生产。已经掉在场上的物品不变。

关闭后下一次生产恢复原生随机结果；此前已选定的待掉落结果不会回溯。未额外修改末波
停产规则、生产间隔或其他植物。该组合未加入“掉落物类型”，因为它不是 `CoinType`。

## 反编译源码导航

相对于 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3`：

| 文件 | 重点 |
|---|---|
| `Lawn/Plant.cs` | `UpdateProductionPlant()` 的概率、动画、状态和延迟掉落。 |
| `Lawn/Board.cs` | `AddCoinForDropLootType()` 的 `ThreeDiamonds` 分支及新增运动参数。 |
| `Lawn/DropLootType.cs`、`Lawn/PlantState.cs`、`Lawn/PlantVoice.cs` | 新枚举成员。 |
