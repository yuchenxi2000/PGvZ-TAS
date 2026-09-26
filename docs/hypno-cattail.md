# 魅惑香蒲刺的魅惑判定

本文依据当前支持的 PGvZ 1.3.0、1.3.1 反编译代码，记录魅惑香蒲的子弹命中逻辑和修改器接入点。

## 原版调用链

`Plant.Fire` 为 `SeedType.HypnoCattail` 创建 `ProjectileType.HypnoCattailSpike`。子弹命中后进入 `Projectile.DoImpact(Zombie)`：先调用 `Zombie.TakeDamage`，再在目标僵尸非空时用 `RandomNumbers.NextNumber(20) == 0` 判定是否调用 `Zombie.ApplyMindControl()`，原版概率为 1/20。随机判定命中后，`DoImpact` 无条件提前返回；随机判定未命中则继续执行 `Projectile.Die()`。

## 无法魅惑目标时的帧伤

`Zombie.ApplyMindControl()` 返回 `void`，只有在目标未被魅惑、未死亡或进入死亡过程，且类型不属于 `Boss`、`RobotTitan`、`RedeyeRobotTitan`、`Gargantuar`、`RedeyeGargantuar`、`Zamboni`、`Catapult`、`Bungee` 或带雪橇的 `Bobsled` 小队时，才会调用 `StartMindControlled()`。条件不满足时它直接结束，并不会告知 `Projectile.DoImpact` 魅惑失败。

因此，随机判定命中但目标无法魅惑时，子弹已经造成一次伤害，却因 `DoImpact` 的提前返回没有执行 `Die()`。追踪弹仍保留原目标；只要下一游戏逻辑帧它仍与目标重叠，且目标仍满足 `EffectedByDamage`，`Projectile.UpdateNormalMotion → CheckForCollision → DoImpact` 就会再次造成伤害。原版也可能发生，但后续某次随机判定未命中会销毁子弹；“魅惑香蒲必能魅惑”开启后，每次判定都命中，这条销毁路径不会触发，因而更容易持续出现帧伤。目标脱离碰撞范围、失去受伤资格或子弹离开场地时，重复命中会停止。启用[所有僵尸可被魅惑](zombie-mind-control.md)后，原本免疫魅惑的存活目标也会进入魅惑状态，避免因类型免疫而反复命中。

`HypnoCattailSpike` 的默认伤害为每次命中 20；创意关卡的 `CSOverrideProjectileProperty` 可以覆盖这个数值，护盾、头盔等受伤规则也会影响实际扣血。“帧伤”指每个发生重叠碰撞的**游戏逻辑帧**重复调用伤害，不保证每个显示帧都扣除 20 点生命。

## 修改器接入点

`pgvztool/hook.py` 挂钩 `Projectile.DoImpact`。仅在“魅惑香蒲必能魅惑”开启、子弹类型为 `HypnoCattailSpike` 且目标僵尸非空时，临时将 `rng_manip.forced_int_by_ceiling[20]` 设为 0，调用原方法后在 `finally` 中恢复先前值。这个开关仅保证随机判定成功；独立的“所有僵尸可被魅惑”开关负责绕过 `ApplyMindControl` 的类型限制。其他类型子弹和无目标命中保持原版行为。

## 反编译源码导航

- `Lawn/Plant.cs`：`Fire`。
- `Lawn/Projectile.cs`：`UpdateNormalMotion`、`CheckForCollision`、`DoImpact`、`GetProjectileDamage`。
- `Lawn/Zombie.cs`：`TakeDamage`、`EffectedByDamage`、`ApplyMindControl`。
- `Lawn/GameConstants.cs`：`HypnoCattailSpike` 的默认伤害。
