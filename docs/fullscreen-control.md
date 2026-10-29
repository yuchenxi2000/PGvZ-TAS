# 全屏按钮与快捷键

本文对比本地 PGvZ 1.2.6、1.3.0 和 1.3.1 的反编译代码，记录全屏入口的变化。

## 主菜单按钮已移除

1.2.6 的 `Lawn.GameSelector` 有 `mFullScreenButton` 字段，在
`InitMainSmallButton()` 中以 ID 127 创建按钮，并在加入管理器、布局和禁用操作中处理
这个控件。`ButtonDepress()` 的 `GameSelectorButtons.FullScreen` 分支调用
`mApp.ToggleFullscreen()`。

1.3.0 和 1.3.1 均已删除该字段及按钮的创建、加入、布局代码，不是通过
`SetVisible(false)` 或移到屏幕外隐藏。`GameSelectorButtons.FullScreen` 枚举仍在，
但点击分支仅保留空的 `break`，因此手动触发 ID 127 也不会切换全屏。

现有本地样本只能确认 1.2.6 时仍存在、1.3.0 时已移除，不能据此确定两个版本之间的
具体移除版本，也未核对 1.3.1 之后的反编译实现。

## 全屏功能保留

1.3.1 的 `Sexy.WidgetManager.KeyDown()` 检查 Return 和 Alt 状态
（`mKeyDown[18]`，合并左右 Alt），随后直接调用 `mApp.ToggleFullscreen()`。
因此 Alt+Enter 是控件分发前处理的全局快捷键，不依赖旧主菜单按钮。

`Sexy.SexyAppBase.ToggleFullscreen()` 委托给 `Sexy.Main.ToggleFullscreen()`，后者
处理显示模式、窗口尺寸、缩放和 `mGameConfig.mFullscreen` 配置。需要直接切换全屏时
可调用 `GetLawnApp().ToggleFullscreen()`，仍须在游戏主线程执行。

`NewOptionsDialog.CheckboxChecked()` 也残留了 ID 14 调用 `ToggleFullscreen()` 的
分支，但构造与 `AddedToManager()` 中没有对应的全屏复选框，并不是一个可以直接
取消隐藏的现成控件。

## 网页快捷操作

修改器的“快捷操作”提供“切换全屏”按钮，通过
`cheat_actions.ToggleFullscreen()` 是同步方法，由 GUI 分发器在游戏主线程调用 `GetLawnApp().ToggleFullscreen()`。
此操作不依赖 Board，可用于主菜单或关卡内；不依赖旧主菜单按钮及其图标资源。

## 源码导航

- `Lawn/GameSelector.cs`：`InitMainSmallButton`、`AddedToManager`、布局方法、`ButtonDepress`。
- `Lawn/GameSelectorButtons.cs`：保留的 `FullScreen` 枚举值。
- `Lawn/NewOptionsDialog.cs`：构造方法、`AddedToManager`、`CheckboxChecked`。
- `Sexy/WidgetManager.cs`：`KeyDown` 中的 Alt+Enter 分支。
- `Sexy/SexyAppBase.cs`、`Sexy/Main.cs`：`ToggleFullscreen`。
