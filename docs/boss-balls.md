# 僵王火球与冰球机制

本文依据 PGvZ 1.2.6 的反编译代码整理僵王博士（Zomboss）火球和冰球的存储、更新、绘制与销毁机制。

## 存储位置

火球和冰球不是 `Projectile`，也不会进入 `Board.mProjectiles`。它们是由僵王对象持有的特殊 `Reanimation`，状态保存在 `Zombie` 的三个字段中：

- `mBossFireBallReanimID`：火球或冰球的 `Reanimation` 引用；
- `mFireballRow`：球所在行；
- `mIsFireBall`：`true` 为火球，`false` 为冰球。

存档时这三个字段都会被同步，`mBossFireBallReanimID` 通过 `mBossFireBallReanimID_Save` 与全局 reanimation 列表互相转换。因为每个 Zombie 只有一个引用字段，原生结构下每个载体同时只能存在一个火球或冰球，但字段和相关方法并没有检查载体的 `mZombieType`。

## 生成和更新

`BossHeadSpit` 随机决定 `mFireballRow` 和 `mIsFireBall`，播放吐球动画；动画到达接触点后，`BossHeadSpitContact` 创建 `ReanimationType.BossFireball` 或 `ReanimationType.BossIceball`，并将其设为 `mIsAttachment = true`。

Attachment reanimation 不会被全局 `EffectSystem.Update` 更新，也不会作为普通 reanimation 进入 Board 渲染列表：

- `Zombie.UpdateBoss` 每帧调用 `UpdateBossFireball`，根据 reanimation `_ground` 轨道速度向左移动球；
- 每帧按 `mFireballRow` 重算屋顶高度，因此球会沿屋顶斜面运动；
- 通过 `SquishAllInSquare(..., ZombieAttackType.DriveOver)` 压掉所在格的植物，并另行碰撞同行割草机；
- 飞出场地左边界后销毁；
- 运动期间随机生成 `FireballTrail` 或 `IceballTrail` 粒子。

`Board.AddBossRenderItem` 把真僵王持有的 reanimation 作为 `BossPart.Fireball` 加入渲染列表，最后由 `Zombie.DrawBossFireBall` 分别绘制普通、叠加和顶层渲染组。仅向 effect system 添加同类 reanimation 不能完整复现原生行为：attachment 不会自行更新或绘制，必须额外驱动更新和绘制。

## 离场载体可行性

`UpdateBossFireball`、`BossDestroyFireball` 和 `BossDestroyIceballInRow` 只使用 Zombie 上述三个球字段，以及从 `mApp`、`mBoard` 取得的 reanimation、植物、割草机和粒子系统；它们不要求 Zombie 是 `ZombieType.Boss`，也不要求 Zombie 位于 `Board.mZombies`。

一种可能方案是为每颗球从 `Zombie.GetNewZombie()` 对象池取得一个载体，只设置当前 `mApp`、`mBoard` 和球字段，且**不调用 `ZombieInitialize`、不加入 `Board.mZombies`**。这比把一个假僵尸放进场地再设置无敌或隐身更安全：载体不会被 Board 更新、绘制、碰撞、计入波次或进入原生存档。一颗球使用一个载体，理论上可以同时存在多个火球和冰球。

> 离场载体本身不属于原生存档对象。如果以后采用此方案，必须在读档前清除这些球，避免读档后保留已失效的 reanimation 引用。

## 原生销毁交互

- `BossDestroyFireball` 只销毁火球，并生成一圈辣椒火焰动画；全屏冰冻效果会调用它。
- `BossDestroyIceballInRow` 只在传入行与 `mFireballRow` 一致时销毁冰球；火爆辣椒的行攻击会调用它。
- 火红莲的技能范围命中球时会同时尝试两种销毁方法。
- 僵王死亡时会清理其持有的球。

## 可能的修改器实现

当前修改器**没有实现**僵王火球和冰球的独立放置。下面仅记录一种可行方向：

1. 每颗球从 `Zombie.GetNewZombie()` 对象池取得一个独立载体，只设置当前 `mApp`、`mBoard` 和三个球字段；
2. 不调用 `ZombieInitialize`，也不把载体加入 `Board.mZombies`；
3. 修改器维护载体列表，每个游戏逻辑帧对其调用 `UpdateBossFireball`，球消失后归还对象池；
4. 另行接入 Board 渲染顺序，绘制普通、叠加和顶层三个 render group；
5. 为冰冻、火爆辣椒行攻击和火红莲技能补做离场球的销毁判定，并处理读档、换关和异常清理。

这个方案能让多个球脱离真僵王存在，但更新、渲染、原生交互和生命周期都要由修改器接管，复杂度及维护成本明显高于普通 `Projectile`，因此暂不落地。
