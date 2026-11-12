# 砸罐子的鼠标交互、锤击动画与普通关卡开罐

本文依据 PGvZ 1.3.0 的反编译记录，并核对本地 PGvZ 1.3.2 源码，记录鼠标砸罐子时的命中、动画和开罐调用链。

## 原生调用链

1. `Board.MouseHitTest` 只在 `LawnApp.IsScaryPotterLevel()` 为真且 `Challenge.mChallengeState` 不是
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

## 普通关卡为什么不能砸罐子

PGvZ 1.3.2 有三处以 `IsScaryPotterLevel()` 限定的入口：

- `Board.MouseHitTest` 只在砸罐子关卡中返回 `GameObjectType.ScaryPot`。
- `Challenge.MouseDown` 只在砸罐子关卡中调用 `ScaryPotterMalletPot`。
- `Challenge.Update` 只在砸罐子关卡中调用 `ScaryPotterUpdate`，回收锤子并实际开罐。

因此，仅让普通关卡进入锤击方法会留下无法完成的动画；强行更改关卡模式则会影响出怪、
阳光、种子栏和通关规则。`IsScaryPotterLevel()` 还包括冒险 4-5、快速游戏 4-5，
以及带 `CSVaseLevel` 组件的自定义关卡，不能只按小游戏枚举判断。

修改器在 `Challenge.MouseDown` 原生处理未消耗点击后，对普通关卡补充开罐：
仅在正式游戏中、允许交互、左键或触摸、空手或持铲且原生命中为空时，查找点击格子的罐子，
直接调用 `ScaryPotterOpenPot`。卡槽、工具、植物和掉落物保持原生命中优先级，禅境花园和
智慧树不使用这条补充路径。轻松放置仍优先处理点击，需要先退出放置模式再开罐。

`Challenge.MouseDown` 接收到的坐标已在 `Board.MouseDownInternal` 中经过 Camera 转换，
补充路径只乘 `Constants.IS` 还原分辨率缩放，再调用 `PixelToGridX/Y`；不能再次转换 Camera。
普通关卡不借用 `mChallengeState`、`mChallengeGridX/Y` 或 `mReanimChallenge`，避免覆盖其他
小游戏状态，因此始终直接开罐，不依赖“砸罐子无间隔”开关。原生内容掉落、音效和破碎粒子保留。

另一个陷阱是 `ScaryPotterOpenPot` 无条件调用 `ScaryPotterIsCompleted`；当场上没有罐子
且没有敌方僵尸时，普通关卡也会进入 `SpawnLevelAward`，提前设定胜利和生成奖励。
修改器挂钩带有场地物品遍历的 `ScaryPotterIsCompleted`，在非砸罐子关卡中返回 `False`。
这也覆盖网页“砸开罐子”的批量操作；真正的砸罐子关卡继续使用原生通关判定，普通关卡的
其他结算路径不受影响。

## 反编译源码导航

本次核对目录：`/Users/ycx/Documents/ChatGPT/PGvZ-Mac/src/Lawn/`，
`Lawn/LawnApp.cs` 的 `AppVersionNumber` 为 `PGvZ 1.3.2`。

- `Lawn/Board.cs` 的 `Board.MouseHitTest`
- `Lawn/Challenge.cs` 的 `Challenge.MouseDown`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterMalletPot`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterUpdate`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterOpenPot`
- `Lawn/Challenge.cs` 的 `Challenge.ScaryPotterIsCompleted` 与 `Challenge.SpawnLevelAward`
- `Lawn/LawnApp.cs` 的 `LawnApp.IsScaryPotterLevel`
