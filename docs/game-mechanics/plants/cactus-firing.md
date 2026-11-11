# 仙人掌伸长与射击节奏

本文依据本地 PGvZ 1.3.2 反编译代码，记录仙人掌伸长后的射击间隔。

## 伸长与缩回

`Plant.UpdateCactus()` 在当前射击动作结束后检查目标。矮态下，找到符合
`PlantWeapon.Primary` 判定的目标就开始伸长。气球僵尸和螺旋桨僵尸的飞行阶段可以
通过 `Zombie.IsFlying()` 命中该判定。屋顶斜坡带来的高度差可以命中同排目标的高度
判定，判定依据是僵尸的行基准高度和碰撞框上沿。

伸长动画播完后进入 `CactusHigh`，并把 `mLaunchCounter` 设为 1。同一轮植物更新
中，`UpdateShooter()` 将它减至 0 并尝试开始射击。保持高态期间如果找不到符合
主武器判定的目标，仙人掌会在射击动作结束后开始缩回。

## PGvZ 的连续射击间隔

默认 `mLaunchRate` 为 150。射击倒计时归零时，`Plant.UpdateShooter()` 将其重设为
`mLaunchRate - RandomNumbers.NextNumber(15)`，其中随机值为 0～14。高态且
`IsIZombieLevel()` 为假时，重设后的倒计时再整除 2。持续有目标、姿态稳定时，
相邻两发尖刺的间隔如下。

| 姿态 | 游戏逻辑帧 | 原速下的时间 |
| --- | ---: | ---: |
| 矮态 | 136～150 | 1.36～1.50 秒 |
| 高态 | 68～75 | 0.68～0.75 秒 |
| “我是僵尸”模式高态 | 136～150 | 1.36～1.50 秒 |

射击动作另有 `mShootingCounter`。矮态设为 35，高态设为 23，均在减到 1 时出刺，
因此开始射击后分别需要 34 帧和 22 帧。第一次高态出刺还要等待伸长动画。创意关卡
可以覆盖 `mLaunchRate`，此时以实际值代入倒计时公式。

## 与原版 PvZ 的差异

原版《植物大战僵尸》中，仙人掌伸长后仍按矮态的射击间隔连续出刺。
PGvZ 则在“我是僵尸”以外的模式中将高态的发射倒计时减半。

## 反编译源码导航

- `Lawn/GameConstants.cs` 中的仙人掌 `PlantDefinition`。
- `Lawn/Plant.cs` 中的 `FindTargetZombie()`、`UpdateCactus()`、
  `UpdateShooter()`、`FindTargetAndFire()` 和 `UpdateShooting()`。
- `Lawn/Zombie.cs` 中的 `IsFlying()` 和 `GetPosYBasedOnRow()`。
