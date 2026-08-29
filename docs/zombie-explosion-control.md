# 僵尸爆炸行为控制

本文记录 PGvZ 1.2.6 中玩偶匣僵尸和辣椒僵尸的爆炸调用链，供修改对应 Hook 时核对。

## 玩偶匣僵尸

`Zombie.UpdatePlaying()` 会对 `JackInTheBox` 调用
`UpdateZombieJackInTheBox()`。该方法负责从运行阶段切换到弹出阶段，并在倒计结束时
伤害周围目标、生成爆炸效果和杀死自身。跳过整个方法可以阻止进入弹出阶段和完成爆炸，
而通用的僵尸更新与行走仍由外层流程执行。

## 辣椒僵尸

`Zombie.UpdatePlaying()` 会对 `JalapenoHead` 调用
`UpdateZombieJalapenoHead()`。该方法在阶段倒计结束后集中执行音效、火焰效果、整行伤害和
自毁。跳过该方法即可屏蔽整段爆炸逻辑，不需要分别拦截植物和僵尸伤害。

## 开关时序

`Zombie.Update()` 在进入上述类型专用方法之前已递减 `mPhaseCounter`。因此，开启“不爆炸”
时特殊逻辑会被持续跳过；若之后关闭开关，已经到期的僵尸会在下一次更新时立即恢复原有行为。
