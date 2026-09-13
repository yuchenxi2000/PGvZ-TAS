# 普通子弹机制

本文依据 PGvZ 1.2.6 的反编译代码，记录普通子弹（`Projectile`）的存储、创建、运动、碰撞、绘制和回收机制。这里的 `ProjectileType.Fireball` 是火炬树桩转化出的火豌豆，不是[僵王火球](boss-balls.md)。

## 存储与生命周期

普通子弹存放在 `Board.mProjectiles`。游戏通过 `Board.AddProjectile` 创建子弹：

```python
projectile = board.AddProjectile(x, y, render_order, row, projectile_type)
```

该方法从对象池取得一个 `Projectile`，调用 `ProjectileInitialize`，再将其加入 `mProjectiles`。此后：

- `Board.UpdateGameObjects` 每个游戏逻辑帧调用 `Projectile.Update`；
- `Board.DrawGameObjects` 将存活子弹及其阴影加入统一渲染列表；
- `Projectile.Die` 设置 `mDead` 并清理或淡出附件；
- `Board.ProcessDeleteQueue` 从列表移除死亡子弹并调用 `PrepareForReuse`，将对象归还对象池；
- Board 存读档会同步 `mProjectiles` 中的子弹及其目标、附件和 reanimation 引用。

## 坐标与基础状态

`ProjectileInitialize(x, y, render_order, row, type)` 将 `x`、`y` 写入 `mPosX`、`mPosY`，并同步到整数坐标 `mX`、`mY`。它们是图片和碰撞使用的左上基准；`row` 写入 `mRow`，表示主要碰撞行。

初始化器还会：

- 将 `mMotionType` 设为 `Straight`；
- 将 `mVelX`、`mVelY`、`mVelZ` 和 `mAccZ` 清零；
- 将 `mDamageRangeFlags` 清零，但 `ZombiePeaMindControl` 会改为 `1`；
- 根据坐标与行计算 `mShadowY`、`mOnHighGround`；
- 设置默认 `40×40` 碰撞尺寸，再按类型调整；
- 为寒冰豌豆、烟雾、香蒲刺、火红莲刺等类型建立粒子、拖尾或附属 reanimation。

`mRenderOrder` 由调用方传入。植物通常传入自身渲染顺序减一；子弹经过若干帧后，`Update` 会将其改为对应行的 `RenderLayer.Projectile`。最终 Boss 关会统一改用第 5 行的子弹渲染顺序。

## 更新与运动

`Projectile.Update` 递增 `mProjectileAge`，然后调用 `UpdateMotion`。`UpdateMotion` 根据 `mMotionType` 分派到抛射或普通运动，处理屋顶地形造成的纵坐标变化，最后把浮点位置同步到 `mX/mY`。

### 普通运动

| `ProjectileMotion` | 原生行为 |
|---|---|
| `Straight` | 大多数类型每帧向右移动 `3.33`；三种符咒子弹每帧向右移动 `15` |
| `Backwards` | 每帧向左移动 `3.33` |
| `Threepeater` | 向右移动 `3.33`，同时按 `mVelY` 换行，纵向速度每帧乘 `0.97` |
| `Puff` | 按直线方向移动，并在年龄达到 75 帧时销毁 |
| `Star` | 完全使用 `mVelX/mVelY`，可向五个原生方向飞行 |
| `Bee` / `BeeBackwards` | 向右/左移动 `3.33`，前 60 帧每帧向上偏移 `0.5` |
| `FloatOver` | 缓慢向右漂移，并使用 `mVelZ` 调整纵坐标与旋转 |
| `Homing` | 使用 `mTargetZombieID` 追踪目标，速度方向逐渐转向目标并归一化为 `2` |
| `EndoflameHoming` | 与普通追踪类似，但会补偿不同行的地形高度；目标失效时调用 `EndoflameRetarget` |
| `YAwareStraight` | 水平移动方式与直线弹相同，碰撞时额外检查实际纵向范围 |

### 抛射运动

`Lobbed` 使用 `mVelX/mVelY` 更新平面位置，使用 `mVelZ` 和 `mAccZ` 更新高度。卷心菜、玉米粒、黄油、西瓜和冰西瓜由植物发射时通常按 120 帧飞行时间计算水平速度，并使用 `mVelZ = -7 + 高度差 / 120`、`mAccZ = 0.115`。

篮球同样使用 `Lobbed`，但水平速度为负，目标是植物。玉米加农炮弹是特殊抛射物：上升到 `mPosZ < -700` 后切换为下降状态，并移动到 `mCobTargetX/mCobTargetRow` 指定的落点。

## 类型与原生附加状态

`ProjectileType.ProjectilesCount` 是计数哨兵，不是有效子弹。其他类型的原生创建路径如下：

| 类型 | 原生附加状态 |
|---|---|
| `Pea`、`Snowpea` | 直线运动；寒冰豌豆初始化寒冰拖尾 |
| `Cabbage`、`Melon`、`Wintermelon`、`Kernel`、`Butter` | 植物发射后改为 `Lobbed` 并设置弹道；黄油命中时施加黄油状态，瓜类造成溅射伤害 |
| `Puff`、`PuffGreen` | 植物发射后改为 `Puff`；初始化烟雾拖尾 |
| `Star` | 星星果发射后改为 `Star`，五颗子弹分别设置方向速度 |
| `Spike` | 仙人掌发射后改为 `YAwareStraight` |
| `Basketball` | 投石车僵尸设置向左的 `Lobbed` 弹道 |
| `ZombiePea` | 普通豌豆头僵尸设置 `Backwards`，向左攻击植物 |
| `ZombiePeaMindControl` | 被魅惑的豌豆头僵尸使用，向右攻击普通僵尸 |
| `CattailSpike`、`HypnoCattailSpike` | 香蒲发射后改为 `Homing`，设置初速度和目标僵尸；初始化对应拖尾。共享拖尾容器的原版容量问题见[拖尾容器容量耗尽崩溃修复](trail-holder-capacity-crash.md) |
| `EndoflameSpike` | 火红莲发射后改为 `EndoflameHoming`，设置目标并初始化附属 reanimation |
| `Talisman`、`TalismanMove`、`TalismanSeal` | 保持直线运动；通用碰撞检查明确跳过这三类 |
| `Cobbig` | 使用由起点、最高点和指定落点共同控制的特殊 `Lobbed` 弹道 |

`mFromPlant` 记录来源植物。豌豆、寒冰豌豆等由部分射手发出时，`Draw` 会根据 `IsFromRepeatess` 将图片缩小为一半。

## 两种转化型火球

### 火炬树桩火豌豆

`ProjectileType.Fireball` 不是独立初始化类型。`ProjectileInitialize` 收到该类型时会触发断言，因为火焰外观依赖转化过程创建的附件。

原生流程是让 `Pea` 或 `Snowpea` 穿过火炬树桩，再调用 `ConvertToFireball(grid_x)`：它修改类型、记录火炬树桩列、播放音效，并创建循环播放的 `ReanimationType.FirePea` 附件。无参数重载 `ConvertToFireball()` 由 `LoadingComplete` 用来恢复火焰外观。

### 火红莲火球

`ProjectileType.EndoflameFireball` 由 `EndoflameSpike` 穿过火炬树桩时调用 `ConvertToEndoflameFireball(grid_x)` 得到。初始化 `EndoflameSpike` 时已经创建 `mProjectileReanimID`；转化方法将该 reanimation 切换到 `anim_burning`。直接初始化 `EndoflameFireball` 不会建立这项可视状态。

## 碰撞、伤害与销毁

普通植物子弹通过 `FindCollisionTarget` 查找同一逻辑行、符合 `mDamageRangeFlags` 的僵尸。追踪弹只检查 `mTargetZombieID`；`YAwareStraight` 还要求子弹与僵尸的纵向矩形相交。

`ZombiePea` 会先通过 `FindCollisionTargetPlant` 攻击植物，也可以命中被魅惑僵尸。符咒子弹不进入通用命中处理。

命中后 `DoImpact` 从 `GameConstants.gProjectileDefinition` 取得基础伤害，应用冰冻、黄油、火焰、溅射等类型效果，生成命中特效并调用 `Die`。子弹飞出水平边界、烟雾弹达到寿命、星星飞出纵向边界或撞上无法越过的高地时也会销毁。

当前 23 种有效类型的基础伤害由全局定义表给出：普通豌豆类多为 20，卷心菜和黄油为 40，瓜类为 80，篮球为 75，玉米加农炮弹为 300，三种符咒为 0。
