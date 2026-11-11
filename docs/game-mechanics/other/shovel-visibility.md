# 铲子显示与可用性

本文依据当前支持的 PGvZ 1.3.0、1.3.1 反编译代码，记录“显示铲子”选项的接入点。

## 原生状态

- `Board.mShowShovel` 是当前 `Board` 的字段，初始化为 `false`，存档会读写它。`CutScene.StartLevelIntro()` 会再次清零；`CutScene.ShowShovel()` 只在其关卡条件满足时设为 `true`。退出再进入时，直接修改旧 `Board` 的字段无法作为常驻选项。
- `Board.HasShovel()` 优先读取 `LawnApp.mCreativeLevel.GetComponent<CSShovel>().Enabled`；只有没有该组件时才读取 `mShowShovel`。因此单改字段不能让显式禁用铲子的自定义关卡获得铲子。
- `Board.IsCombatToolVisible(Shovel)` 在 `HasShovel()` 之外，还限制游戏场景、禅境花园、智慧树和失败对话框。`Board.DrawShovel()`、按钮命中测试和 `CanUseCombatTool()` 都调用它。
- `Board.MouseDownWithTool()` 另有一次独立的 `HasShovel()` 检查。仅让按钮可见，会出现铲子能拿起却不能使用的情况。

## 修改器实现

`cheat_option.showShovel` 是同步并保存在网页本地的布尔选项。修改器直接挂钩 `Board.HasShovel()`：开启时返回 `true`，关闭时调用原方法。这样每次新建或读取 `Board` 都沿用同一开关，也能覆盖显式禁用铲子的自定义关卡；关闭后立即回到关卡原有设置，同时保留 `IsCombatToolVisible()` 的原生场景与交互限制。

`HasShovel()` 是较短的方法，运行时存在被内联的可能；项目已有的 `Board.HasGlove()` 钩子可以正常工作。铲子钩子的实际生效情况仍需在游戏中验证，尤其要分别检查按钮显示与铲除植物。

## 反编译源码导航

两个支持版本的相对路径相同：

| 文件 | 重点 |
|---|---|
| `Lawn/Board.cs` | `HasShovel`、`IsCombatToolVisible`、`DrawShovel`、`MouseDownWithTool`、`BoardHitTest` |
| `Lawn/CutScene.cs` | `StartLevelIntro`、`ShowShovel` |
| `Lawn.Creative/CSShovel.cs` | `Enabled` 的私有 setter |
