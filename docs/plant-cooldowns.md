# 植物冷却机制与冷却条绘制

本文依据当前支持的 PGvZ 1.3.0、1.3.1 游戏源码，记录植物的各种冷却机制以及 PGvZ-TAS 修改器的绘制细节。下文的倒计时数值均以游戏帧为单位。

## 植物状态冷却

以下植物通过 `Plant.mStateCountdown` 记录准备、消化或充能时间。`Plant.Update` 每帧递减该字段，随后根据 `mState` 处理状态转换。因此判断冷却时必须同时检查植物类型和状态；其他状态也会复用 `mStateCountdown`。

| 植物 | 冷却状态 | 起始倒计时 | 结束条件 |
|---|---|---:|---|
| 玉米炮（`Cobcannon`） | `CobcannonArming` | 初次种植 500，发射后 3000 | 归零后进入 `CobcannonLoading`，装填动画完成才进入 `CobcannonReady` |
| 大嘴花（`Chomper`） | `ChomperDigesting` | 4000 | 归零后播放吞咽动画，再回到 `Ready` |
| 超级大嘴花（`SuperChomper`） | `ChomperDigesting` | 2500 | 同上 |
| 土豆雷（`Potatomine`） | `Notready` | 1500 | 归零后播放出土动画，再进入 `PotatoArmed` |
| 磁力菇（`Magnetshroom`） | `MagnetshroomSucking`、`MagnetshroomCharging` | 吸走金属时设置 1500 | 吸取动画结束后进入充能状态，倒计时归零才回到 `Ready` |
| 吸金磁（`GoldMagnet`） | `MagnetshroomCharging` | 吸取动画结束后随机设置 200–300 | 倒计时归零后回到 `Ready`；再次吸取还需要金币目标，并通过每帧的随机判定 |

`PlantInitialize` 将玉米炮的 `mTargetX` 设为 `-1`；`CobCannonFire` 在首次发射时将其改为目标 X 减 47，之后不重置。因此本局可以用它区分首次准备和发射后的装填。磁力菇从开始吸取时就倒数，进入 `MagnetshroomCharging` 时已消耗一部分时间；吸金磁则是在吸取动画结束后才开始充能。

这些倒计时归零后，植物仍可能需要完成动画才能再次行动。`mStateCountdown` 还用于阳光菇成长、地刺攻击、花盆和睡莲的初始无敌等过程；这些状态不能直接按上表解释为重复使用的冷却。

## 生产类植物（`UpdateProductionPlant`）的生产冷却

向日葵（`Sunflower`）、双子向日葵（`Twinsunflower`）、阳光菇（`Sunshroom`）、向日葵豌豆（`SunflowerPea`）和向日葵坚果（`SunflowerWallnut`）生产阳光；金盏花（`Marigold`）生产金币。六者都通过 `UpdateProductionPlant` 递减 `Plant.mLaunchCounter`，默认 `mLaunchRate` 均为 2500。创意关卡可以覆盖单株的 `mLaunchRate`。

五种产阳光植物的首次 `mLaunchCounter` 在 `PlantInitialize` 中随机设为 300 至 `mLaunchRate / 2`；金盏花不属于 `MakesSun()`，首次随机值为 0 至 `mLaunchRate`。每次产出后，六者都将下一轮倒计时随机设为 `mLaunchRate - 150` 至 `mLaunchRate`。所以首次生产与后续生产都不一定从完整周期开始。向日葵豌豆还会依据同一倒计时的余数发射豌豆。

`Plant.IsInPlay()` 会排除禅境花园和智慧树；`UpdateProductionPlant` 还会排除“我是僵尸”（包括带 `CSIZombieLevel` 组件的创意关卡）、`Upsell`、`Intro` 和已掉落关卡奖励的场景。坚不可摧模式只在 `LastStandOnslaught` 阶段推进生产倒计时。

阳光菇小形态和大形态均调用 `UpdateProductionPlant`；成长动画期间不调用，生产计时暂停。白天沉睡时，计时器也保持当前值。其 `mStateCountdown = 12000` 是成长时间，与生产冷却无关。金盏花在最后一波进入 `MarigoldEnding`，6000 帧后停止生产；届时 `mLaunchCounter` 可能仍有剩余。普通射手也使用 `mLaunchCounter`，但由 `UpdateShooter` 更新，不能仅凭字段名称判断为生产冷却。

## 修改器实现细节

“显示植物CD”读取状态冷却，但只覆盖玉米炮、大嘴花、超级大嘴花、土豆雷和磁力菇。磁力菇从 `MagnetshroomSucking` 起显示，分母固定为 1500。吸金磁的充能仅 200–300 帧，当前不绘制，以免频繁闪烁。玉米炮根据 `mTargetX` 选择 500 或 3000 作为分母。玉米炮、大嘴花、超级大嘴花和土豆雷的现有无冷却选项会在游戏更新前将对应的 `mStateCountdown` 置零，显示逻辑读取更新后的值。

“显示阳光生产CD”读取上述六种生产植物的 `mLaunchCounter`，金盏花的产金币冷却也归入此开关。每株始终以自己的 `mLaunchRate` 为绘制分母，条长为 `mLaunchCounter / mLaunchRate`，直接体现游戏随机缩短的周期。显示判断复用 `IsInPlay()`、`IsIZombieLevel()` 等生产入口条件：游戏不会在某种关卡模式中推进生产时，不显示冻结的条；阳光菇成长和白天沉睡等临时暂停仍保留当前条长。金盏花停止生产后，即使倒计时尚未清零，也不再绘制。

两个开关都在 `Board.Draw` 的 `orig` 之后、Camera 场地变换之内绘制。剩余倒计时为蓝色，总长底色为深蓝色，外框为黑色；位置为植物的 `(mX + 10, mY + 40)`。血条位于 `mY + 50` 或 `mY + 60`，不会重叠。玉米炮宽 140 像素，其余宽 60 像素，条高均为 5 像素。禅境花园 `ChallengeZenGarden` 中的盆栽虽然也实例化为场上的 `Plant`，但不按普通战斗规则生产；此模式跳过冷却条绘制。

龙舌兰和火红莲的主动技能冷却保存在 `Board` 上，游戏已在技能图标绘制剩余时间；修改器不重复绘制。普通攻击间隔和一次性植物的爆发延迟也不属于上述两个开关。

## 源码导航

- `Lawn/Plant.cs`：`PlantInitialize`、`Update`、`IsInPlay`、`MakesSun`、`UpdateProductionPlant`、`UpdateSunShroom`、`UpdateMagnetShroom`、`MagnetShroomAttactItem`、`UpdateGoldMagnetShroom`、`UpdateChomper`、`UpdateSuperChomper`、`UpdatePotato`、`UpdateCobCannon`、`CobCannonFire`。
- `Lawn/LawnApp.cs`：`IsIZombieLevel`，包括创意关卡中的“我是僵尸”组件。
- `Lawn/Board.cs`：`HasLevelAwardDropped`，用于判断关卡奖励是否已掉落。
- `Lawn/GameConstants.cs`：相关植物的 `PlantDefinition`。
- `pgvztool/hook.py`：修改器的 `PlantCooldown`、`ProductionCooldown` 和 `DrawPlantCooldowns`。
