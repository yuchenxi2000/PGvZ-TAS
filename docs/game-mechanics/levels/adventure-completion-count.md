# 冒险模式通关周目计数

本文依据当前支持的 PGvZ 1.3.0、1.3.1 反编译代码，记录 `PlayerInfo.mFinishedAdventure` 的含义和边界。

`mFinishedAdventure` 是 C# `int`，表示已经完成的冒险模式周目数，新档案初始值为 0。玩家通关冒险模式第 50 关后，`LawnApp` 将关卡重置为 1，并对该字段加一。游戏在存档中通过 `SyncInt` 保存该字段，旧格式读取路径使用 `ReadLong`；此处的 `Long` 仍对应 32 位整数。

因此可以直接设置为 `int.MaxValue`，即 `2147483647`。修改器的“冒险已通关周目”输入范围为 0 至此值，默认输入 2。设置后在主菜单刷新关卡选择界面。这个默认值只是输入框初始值，点击按钮时才会修改存档。

`LawnApp.HasFinishedAdventure()` 直接判断 `mFinishedAdventure > 0`，没有另一个专门存储“首周目完成”的布尔值。但模式入口有独立的 `mHasUnlockedMinigames`、`mHasUnlockedPuzzleMode`、`mHasUnlockedSurvivalMode` 标志，关卡开放进度还由 `mMiniGamesUnlocked`、`mMiniGamesUnlockable`、`mVasebreakerUnlocked`、`mIZombieUnlocked` 控制。新档案仅修改通关次数不会更新这些值，所以部分模式仍锁定。

首次自然通关时，`LawnApp` 将小游戏可逐步开放数设为 20，并调用 `PlayerInfo.UnlockFirstMiniGames()` 和 `UnlockPuzzleMode()`，使小游戏初始开放 3 关、砸罐子与我是僵尸各开放 1 关。“冒险已通关周目”只修改 `mFinishedAdventure`，不修改这些独立的模式解锁标志或开放关卡数。

金向日葵奖杯另由 `LawnApp.EarnedGoldTrophy()` 判断：只要已完成至少一周目，并且小游戏、解谜、生存模式的奖杯合计达到 48 枚。这个判断本身不以二周目为门槛；设置 `mFinishedAdventure` 为 2 或更高也不会自动获得奖杯。各模式的奖杯由独立的 `mChallengeRecords` 存储，周目设置不会修改它们。

两个版本的 `Lawn.csproj` 都关闭了溢出检查。若在计数为 `2147483647` 时再次通关冒险模式，`mFinishedAdventure++` 会回绕到负数，使依赖已通关周目数的判断失真。`Board.GetLevelRandSeed()` 也把该字段乘以 101 参与关卡随机种子计算，大数时该计算会回绕；这不妨碍字段存储为 `int.MaxValue`。

## 反编译源码导航

| 文件 | 位置 |
|---|---|
| `Lawn/PlayerInfo.cs` | 字段与模式解锁标志约 22–60 行；`UnlockFirstMiniGames`、`UnlockPuzzleMode` 约 433–445 行；`SyncInt` 约 504 行 |
| `Lawn/LawnApp.cs` | `HasFinishedAdventure` 约 2960 行；`GetNumTrophies`、`EarnedGoldTrophy` 约 3586–3607 行；`TrophiesNeedForGoldSunflower` 约 3841 行；冒险模式通关与解锁约 4184–4223 行 |
| `Lawn/ChallengeScreen.cs` | `gChallengeDefs` 定义奖杯所属页面和模式，约 17–118 行 |
| `Lawn/GameSelector.cs` | 解谜模式入口按标志判断，约 402 行；生存模式入口按通关次数判断，约 435 行 |
| `Lawn/Board.cs` | `GetLevelRandSeed` 使用字段约 12201 行 |
| `Lawn.csproj` | `CheckForOverflowUnderflow` 为 `False` |
