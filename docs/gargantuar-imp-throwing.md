# 巨人投掷小鬼机制

本文依据 PGvZ 1.2.6 的反编译代码，记录巨人僵尸触发投掷、创建空中小鬼、计算
投掷轨迹以及小鬼落地的完整过程，并说明修改器如何让三叶草吹走空中小鬼。

## 投掷触发条件

巨人僵尸的投掷逻辑位于 `Zombie.UpdateZombieGargantuar`。游戏首先计算巨人相对场地
投掷基准线的距离：

```text
distance = mPosX - 360 - BOARD_EXTRA_ROOM
```

巨人同时满足以下条件时进入 `GargantuarThrowing` 阶段并播放 `anim_throw`：

- 未被定身且仍有头；
- `mHasObject` 为真，即还持有可投掷的小鬼；
- 本体生命值低于最大值的一半；
- `distance > 40`，尚未走得过于靠近房屋。

## 创建空中小鬼

投掷动画运行到 74% 时，巨人隐藏手中的小鬼和绳子轨道，播放挥动音效，并调用
`Board.AddZombie(ZombieType.Imp, mFromWave)` 创建一个与巨人属于同一波次的小鬼。
创建成功后，小鬼获得以下关键状态：

- 位置从巨人当前位置向房屋方向偏移 133；
- 行数与巨人相同，绘制层位于巨人上一层；
- `mZombiePhase = ZombiePhase.ImpGettingThrown`；
- `mAltitude = 88`；
- 水平速度 `mVelX = 3`；
- 继承巨人的 `mChilledCounter`；
- 播放一次 `anim_thrown` 动画。

巨人的 `mHasObject` 随投掷事件变为假，因此同一个巨人正常情况下只会创建一个小鬼。
投掷动画结束后，巨人恢复 `ZombieNormal` 和行走动画。

## 目标距离与初始垂直速度

非屋顶场景会把 `distance` 的下限限制为 40。屋顶场景先将其减去 180，并把下限改为
-140。若调整后的距离大于 140，游戏还会随机减去 `[0, 100)` 范围内的值。

小鬼的初始垂直速度按以下公式计算：

```text
mVelZ = 0.5 * (distance / mVelX) * THOWN_ZOMBIE_GRAVITY
```

PGvZ 1.2.6 中 `THOWN_ZOMBIE_GRAVITY` 为 0.05。由于屋顶场景允许 `distance` 为负，
小鬼的初始 `mVelZ` 不一定为正。

## 空中运动与落地

`Zombie.UpdateZombieImp` 在 `ImpGettingThrown` 阶段每帧依次执行：

```text
mVelZ -= THOWN_ZOMBIE_GRAVITY
mAltitude += mVelZ
mPosX -= mVelX
```

其中正 `mVelZ` 增加高度，负 `mVelZ` 降低高度。游戏还会根据当前行的地面高度修正
`mPosY`，并把同样的修正量加入 `mAltitude`，以适配屋顶等非水平地形。

当 `mAltitude <= 0` 时，游戏将高度归零，阶段切换为 `ImpLanding` 并播放一次
`anim_land`。落地动画结束后，小鬼才进入 `ZombieNormal` 并开始正常行走。因此
`ImpGettingThrown` 是判断“小鬼仍在空中”的稳定阶段条件，`ImpLanding` 不属于空中。

## 修改器吹飞空中小鬼特性的实现

原版 `Zombie.IsFlying` 只识别气球和螺旋桨相关阶段，不识别 `ImpGettingThrown`，所以
原版 `Plant.BlowAwayFliers` 不会处理巨人刚投出的空中小鬼。

启用“空中小鬼僵尸可吹走”后，`Plant.BlowAwayFliers` 钩子先执行原方法，保留三叶草
的全部原生效果，再遍历场上僵尸。对于类型为 `ZombieType.Imp`、阶段恰好为
`ZombiePhase.ImpGettingThrown` 且仍存活的对象，钩子只设置 `mBlowingAway = true`，
不修改小鬼原有的水平速度、垂直速度、高度或阶段。

通用吹飞标志会在 `Zombie.UpdateZombiePosition` 中让僵尸每帧额外向右移动，并在越过
右侧边界后调用 `DieWithLoot` 将其移除。小鬼原有的抛物线和落地状态仍会继续更新，
但吹飞标志不会在落地时清除，因此被空中三叶草命中的小鬼最终仍会被推出场外。

该选项默认关闭，只影响三叶草发动瞬间处于 `ImpGettingThrown` 阶段的小鬼。已经进入
`ImpLanding` 或 `ZombieNormal` 的小鬼不受影响。开启“僵尸无敌”时不会执行原吹飞
逻辑，也不会设置该标志。
