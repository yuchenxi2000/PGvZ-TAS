# 砸罐子的鼠标间隔与锤击动画

本文依据 PGvZ 1.3.0 反编译代码，记录鼠标砸罐子时的命中、动画和开罐调用链。

## 原生调用链

1. `Board.MouseHitTest` 只在 `Challenge.mChallengeState` 不是
   `ChallengeState.ScaryPotterMalleting` 时把鼠标下的罐子返回为
   `GameObjectType.ScaryPot`。
2. `Challenge.MouseDown` 收到罐子命中后调用
   `ScaryPotterMalletPot`。
3. `ScaryPotterMalletPot` 记录罐子格子，创建 `Hammer` 动画，把状态设为
   `ScaryPotterMalleting`。
4. `ScaryPotterUpdate` 等待动画 `mLoopCount > 0`，再调用
   `ScaryPotterOpenPot`，销毁锤子动画并把状态恢复为 `Normal`。

因此，鼠标间隔是用挑战状态锁住命中，并以锤击动画播放完毕为解锁条件。

## 修改器实现

`pgvztool/hook.py` 挂钩较大的 `Challenge.MouseDown`。“砸罐子无间隔”
开启时，对有效罐子点击直接调用 `ScaryPotterOpenPot`；不创建锤子动画，
也不进入 `ScaryPotterMalleting`状态。开罐本身的内容生成、破碎粒子、声音和
通关检查仍由原生 `ScaryPotterOpenPot` 处理。

不应只放宽 `Board.MouseHitTest` 的状态判断。原生挑战对象只有一组
`mChallengeGridX/Y` 和一个 `mReanimChallenge`；动画未结束时再砸罐会覆盖
待打开罐子的坐标和动画引用，可导致前一个罐子没有打开且动画无法回收。

## 反编译源码导航

- `Lawn/Board.cs` 的 `Board.MouseHitTest`
- `Lawn/Challenge.cs` 的 `Challenge.MouseDown`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterMalletPot`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterUpdate`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterOpenPot`
