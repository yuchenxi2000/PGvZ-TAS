# 螺旋桨僵尸与三叶草吹飞机制

本文依据 PGvZ 1.2.6 的反编译代码，记录螺旋桨僵尸受到三叶草影响后的原生行为，
以及 `pgvztool/hook.py` 将其改为真正吹出场的实现原理。

## 原生行为

三叶草发动特殊能力时，`Plant.DoSpecial` 调用 `Plant.BlowAwayFliers`。这个方法遍历
全场僵尸，对所有仍存活、处于飞行状态且不在 `BalloonPopping` 阶段的僵尸执行吹飞
处理；传入的坐标和行数在当前实现中没有用于筛选僵尸。

普通飞行僵尸会直接设置 `Zombie.mBlowingAway = true`。螺旋桨僵尸则走一套独立状态：

1. `mPhaseCounter` 被设置为 150，阶段变为 `PropellerBlownAway`；
2. `Zombie.UpdateZombieFlyer` 在该阶段每帧将 `mPosX` 增加 2；
3. 倒计时结束后进入 `PropellerTeeter`，播放一次 `anim_teeter`；
4. 动画结束后播放循环的 `anim_idle`，阶段恢复为 `BalloonFlying`。

因此原生效果只是暂时把螺旋桨僵尸向右推开，僵尸对象并未死亡或重新生成，随后会恢复
飞行并再次向房屋方向前进。再次受到三叶草影响会重新开始这套状态转换。

## 通用吹飞标志

`Zombie.UpdateZombiePosition` 每帧检查 `mBlowingAway`。该标志为真时，僵尸会额外向右
移动 10；当上一帧同步得到的 `mX` 大于 850 时，游戏调用 `DieWithLoot` 将其移除。这是
普通飞行僵尸被三叶草真正吹出场的原生路径。

## 修改器实现

启用“螺旋桨僵尸可吹走”后，修改器挂钩 `Plant.BlowAwayFliers`，在关闭“僵尸无敌”时
先调用原方法，以保留吹雾、音效、移除符咒和解除封印等全部原生效果。随后再次遍历
僵尸，只为已经被原方法置为 `PropellerBlownAway` 的螺旋桨僵尸设置
`mBlowingAway = true`。该选项默认关闭；关闭时完全保留游戏原生返场行为。

以阶段作为筛选条件，可以排除死亡僵尸、已经落地的螺旋桨僵尸和正在执行
`BalloonPopping` 的对象，并让原方法继续负责判断其是否可被当前这次三叶草影响。设置
标志后，螺旋桨僵尸沿用普通飞行僵尸的出界移除机制；通常会在 150 帧专用倒计时结束
前离场，因此不会再进入返场流程。

开启“僵尸无敌”时，钩子不会调用原方法，也不会设置 `mBlowingAway`，从而避免三叶草
移除僵尸；此行为优先于“螺旋桨僵尸可吹走”选项。
