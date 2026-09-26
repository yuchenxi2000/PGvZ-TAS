# 僵尸魅惑的目标限制

本文依据当前支持的 PGvZ 1.3.0、1.3.1 反编译代码，记录 `Zombie.ApplyMindControl()` 的目标筛选和“所有僵尸可被魅惑”选项。

## 原版行为

`Zombie.ApplyMindControl()` 对已经魅惑、死亡或正在死亡的目标直接返回；它还排除 `Boss`、`RobotTitan`、`RedeyeRobotTitan`、`Gargantuar`、`RedeyeGargantuar`、`Zamboni`、`Catapult`、`Bungee` 和仍带雪橇的 `Bobsled` 小队。通过检查后，它调用 `StartMindControlled()`，生成魅惑粒子，检查关卡奖励，并刷新动画速度。`StartMindControlled()` 设置 `mMindControlled = true`，还会处理舞王/伴舞及其他僵尸的关联引用。

魅惑香蒲子弹和魅惑香蒲落地时的范围效果都会调用 `ApplyMindControl()`。魅惑菇被啃食的路径则直接调用 `StartMindControlled()`，不经过上述类型筛选。

## 修改器实现

“所有僵尸可被魅惑”是“特性修改”中的独立开关。`pgvztool/hook.py` 挂钩 `Zombie.ApplyMindControl()`：先执行原方法；若它没有转换存活目标且开关已开启，则补做与原方法一致的魅惑效果。已经魅惑、死亡或正在死亡的僵尸仍按原版处理。此开关适用于所有调用 `ApplyMindControl()` 的效果，与“魅惑香蒲必能魅惑”的概率开关互不依赖。

雪橇小队仍在载具上时，钩子会一起转换队长和队员，并在调用 `StartMindControlled()` 后恢复队员与队长的关联，避免原方法断开引用后破坏雪橇队的更新逻辑。

“显示僵尸血量”绘制时直接遍历 `Board.mZombies`，对存活且有头的僵尸显示血条，包括 `mMindControlled = true` 的友方僵尸。友方血条用绿色表示本体、青色表示第二层护具，与敌方的紫红色区分；“血量只显示精英怪”仍按僵尸类型筛选双方。框架的 `IterAliveZombies()` 刻意排除魅惑僵尸，其语义不因血条显示而改变。

“场地移除”的“杀死僵尸（敌方）”调用 `Placer.RemoveZombieOnBoard(enemy_only=True)`，按 `mMindControlled` 跳过友方；不带参数的原按钮仍清除双方。两者都沿用存活且有头的筛选和 `DieNoLoot(False)`，并通过 `@main_thread` 在游戏主线程执行。

该选项解除的是**魅惑状态的类型限制**。僵王、投石车、巨人等的专属技能仍由原版 AI 控制；游戏没有为这些原本免疫魅惑的类型定义完整的友方技能行为，因此它们进入魅惑状态后，部分技能仍可能影响植物或召唤敌方僵尸。

## 反编译源码导航

- `Lawn/Zombie.cs`：`ApplyMindControl`、`StartMindControlled`、`IsBobsledTeamWithSled`、`GetBobsledPosition`、`UpdateActions`、`UpdateBoss`。
- `Lawn/Projectile.cs`：`DoImpact` 中的魅惑香蒲刺命中路径。
- `Lawn/Plant.cs`：`Update` 中的魅惑香蒲落地范围效果。
