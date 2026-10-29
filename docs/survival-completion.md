# 生存模式结算与跳轮

本文依据本地 PGvZ 1.3.1 反编译代码和仓库中的类型存根，记录修改器“直接过关”与“跳到下一轮”的接入方式。

## 终轮判断

`Challenge.mSurvivalStage` 从 0 开始。`Board.IsFinalSurvivalStage()` 先检查创意关卡的
`CSSurvivalLevel` 组件，再处理内置生存模式：

| 类型 | 终轮判断 |
|---|---|
| 自定义有限生存 | `mSurvivalStage == mStages - 1`，必须精确相等 |
| 自定义无尽生存 | `mEndless` 为真，始终不是终轮 |
| 普通生存 | 当前轮结束后的累计旗数至少为 5；每轮 1 旗，终轮 stage 为 4 |
| 困难生存 | 当前轮结束后的累计旗数至少为 10；每轮 2 旗，终轮 stage 为 4 |
| 地狱生存 | `mSurvivalStage >= 4` |
| 内置无尽生存 | 始终不是终轮 |

`LawnApp.IsSurvivalMode()` 包括大泳池生存、肉鸽传送带和带有 `CSSurvivalLevel` 组件的
自定义关卡；`IsSurvivalEndless()` 也包括无尽肉鸽传送带。优先读取创意组件可以保持与
游戏自身的终轮判定一致。

## 结算流程

`Board.FadeOutLevel()` 会调用 `IsSurvivalStageWithRepick()`，由后者检查当前生存轮
是否为终轮。非终轮进入换轮流程；最终由 `LawnApp.CheckForGameEnd()` 增加
`mSurvivalStage` 并调用 `Board.InitSurvivalStage()`，在原 Board 上重新选卡。

修改器的两个操作位于 `CheatActions`，由 GUI 分发器在游戏主线程同步执行，并共用原来的清理僵尸、
关闭暂停对话框和调用 `FadeOutLevel()` 的逻辑：

- “直接过关”：有限生存先设置终轮 stage，自定义生存取 `mStages - 1`，内置有限生存取 4；无尽生存保留原 stage，由游戏进入下一轮。
- “跳到下一轮”：不修改 stage，直接执行原有结算流程。有限生存到达终轮时仍会正常过关，非生存关卡也保持原“直接过关”的行为。

不要手动递增 stage 后再调用 `FadeOutLevel()`，否则游戏后续还会递增一次，跳过一轮。

## 奖杯记录与选卡阶段

生存奖杯取决于 `mChallengeRecords` 中的旗数，而不只是 `IsFinalSurvivalStage()`。
`CheckForGameEnd()` 会调用 `UpdatePlayerProfileForFinishingLevel()`，由后者在终轮调用
`SurvivalSaveScore()`，再通过 `GetSurvivalFlagsCompleted()` 计算旗数并保存记录。
普通生存需要 5 旗，困难、地狱生存需要 10 旗；只设置 stage 4 而不补齐当前轮波数，
会少记当前轮的旗数。

共用结算逻辑应先按目标 stage 调用 `GetNumWavesPerSurvivalStage()`，同时更新
`mNumWaves` 和 `mCurrentWave`。尤其地狱生存在 stage 0–2 每轮 20 波，stage 3–4
每轮 30 波；跳到终轮后不能沿用起始轮的 20 波。
地狱生存完整通关的记录为 12 旗（前三轮各 2 旗、后两轮各 3 旗），达到奖杯所需的
10 旗门槛；不要将通关记录截断为 10。

`GetSurvivalFlagsCompleted()` 在最后一波为旗帜波、`mBoardFadeOutCounter < 0` 且
`mNextSurvivalStageCounter == 0` 时，会减去尚未结算的最后一旗。`FadeOutLevel()`
在非 `Playing` 场景会直接设置 `mLevelComplete`，不会设置淡出计数器。因此终轮操作
应预先设置 `mBoardFadeOutCounter = 600`，在选卡阶段也按已结算最后一旗计分。
保留游戏原有的记录保存时机，避免提前写记录影响首次通关判断和新关卡解锁。

`InitSurvivalStage()` 复用旧 `CutScene`，而 `StartLevelIntro()` 不会重置
`mSeedChoosing`。若旧选卡状态为真，新入场动画会停在 time 0，下一轮的选卡界面
也仍处于屏幕外。操作开始时只要 `mSeedChooserScreen` 存在，就应调用
`CutScene.EndSeedChooser()` 清除选卡标志并移交焦点；随后由原有
`CheckForGameEnd()` 销毁旧选卡界面、创建下一轮界面。不要只销毁界面而保留标志，
也不要调用 `CloseSeedChooser()`，后者要求已选满卡片。

## 源码导航

- `Lawn/Board.cs`：`IsFinalSurvivalStage`、`GetNumWavesPerSurvivalStage`、`GetNumWavesPerFlag`、`IsSurvivalStageWithRepick`、`FadeOutLevel`、`GetSurvivalFlagsCompleted`、`SurvivalSaveScore`、`InitSurvivalStage`。
- `Lawn/LawnApp.cs`：`IsSurvivalMode`、`IsSurvivalNormal`、`IsSurvivalHard`、`IsSurvivalHell`、`IsSurvivalEndless`、`CheckForGameEnd`、`UpdatePlayerProfileForFinishingLevel`。
- `Lawn/CutScene.cs`：`EndSeedChooser`、`StartLevelIntro`、`Update`。
- `Lawn.Creative/CSSurvivalLevel.cs`：`mEndless`、`mStages`。
