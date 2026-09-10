# 关卡入场动画与自动跳过

## 原生流程

当新关卡创建 `Board` 时，`LawnApp.NewGame()` 依次初始化关卡、将场景设为
`GameScenes.LevelIntro`、创建 `SeedChooserScreen`，然后调用
`Board.mCutScene.StartLevelIntro()`。生存模式换轮由
`Board.InitSurvivalStage()` 在同一个 `Board` 上重复这个流程。

`CutScene.Update()` 在 `LevelIntro` 期间推进镜头、戴夫对话、选卡界面、草坪物件和
开战动画。`Board.ChooseSeedsOnCurrentLevel()` 区分普通选卡关与传送带、固定卡片等
无选卡关卡。

## `CancelIntro()` 的边界

`CutScene.CancelIntro()` 是游戏原生的安全快进入口，会先完成资源预载和路边僵尸
生成，并在需要时补齐割草机、花盆、睡莲、雾、墓碑以及戴夫对话的必要
状态。

- 普通选卡关会跳到选卡界面出现前约两个更新步。
- 无选卡关会跳到入场流程末尾，随后进入 `Playing`。
- 无选卡关可放置 Rose 且商店库存大于零时，会保留原生选择对话框。该对话框
  是模态的，会暂停 `Board`，因此必须在调用 `CancelIntro()` 前标记本次进入已处理。
- `GameMode.Upsell` 的戴夫流程不支持这种快进，直接调用可以使对话循环无法退出。
  `GameMode.Intro` 是片头而不是普通关卡入场，两者都必须排除。

不要只写 `mCutsceneTime`、直接切换 `GameScenes.Playing` 或绕过 `StartPlaying()`；这些方法会
跳过上述收尾逻辑。

## 修改器实现

`pgvztool.cheat.ScriptSkipLevelIntro` 使用 `ScriptRunMode.GLOBAL` 常驻监视：

1. 记录上一次看到的 `Board`、场景和开关状态。
2. 只在新进入 `LevelIntro` 或开关在入场期间由关变开时处理。
3. 在调用 `CancelIntro()` 前更新监视状态，避免 Rose 对话框暂停后重复调用。
4. 通过场景边沿而不是只比较 `Board` 引用，因此同一 `Board` 上的生存模式换轮
   也会再次触发。
5. 没有戴夫对话的非滚屏关卡已由 `StartLevelIntro()` 自动取消入场，监视器不会重复调用。

全局脚本在现有 `Board.UpdateGame` 钩子中由 `ScriptManager.Manage()` 在游戏主线程
推进，不需要为 `CutScene` 另外注册 Hook。
