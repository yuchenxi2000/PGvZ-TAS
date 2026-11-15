# 草坪格子放大模式

依据本地 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3` 静态核对。

## 原生入口与行为

内置修改器 `Lawn/ZBCheatDialog.cs` 的按钮 13 为“放大模式”。它检查 `Board.CanSelectGridFocus`，调用 `Board.SelectGridFocus()` 后关闭修改器对话框，将焦点交还 Board。

`CanSelectGridFocus` 要求正在游戏中、不是禅境花园或智慧树、相机已启用且存在、没有处于放大状态，并且 `CanInteractWithBoardButtons()` 允许交互。

`SelectGridFocus()` 刷新原有光标，设置 `CursorObject.mMagnifier` 并更新光标。随后 `Board.MouseDownInternal()` 在处理普通场地点击之前调用 `HandleGridFocusClick()`：

- 输入为屏幕坐标。游戏先通过 Camera 转为场地坐标，再按 `Constants.IS` 换算并检测格子边界；屋顶、泳池和移动端沿用原生定位。
- 选中有效格子后，保存原相机位置和缩放，以格子中心调用 `FocusWorldSmooth()`，目标缩放为 `3 * Constants.BoardCameraScaleMultiplier`，动画为 150 帧 `EaseInOut`。
- `IsGridFocusActive` 在放大及恢复动画期间均为真，原生绘制隐藏主要 UI。
- 放大时再次点击（包括右键），或按 Esc/返回，调用 `LeaveGridFocus()` 恢复原相机参数；恢复动画结束后清除放大状态。右键或返回也可取消尚未完成的选格。

## 修改器接入

轻松放置的 `zoom` 模式在处理点击时，通过缓存的反射信息调用 internal 的 `CanSelectGridFocus` 和 `SelectGridFocus`，然后将原始屏幕坐标交给 `MouseDownInternal` 原方法。没有重写相机参数或格子检测逻辑，也不单独挂钩这些短方法。

`CursorObject.mMagnifier` 同样是 `internal` 字段，IronPython 直接访问会报没有该属性。选格状态通过 `BindingFlags.Instance | BindingFlags.NonPublic` 获取并缓存 `FieldInfo`，使用 `GetValue(cursor)` 读取；`Board.IsGridFocusActive` 也通过缓存的非公开属性反射读取。

进入原生选格前显式退出轻松放置选中态，原生入口仍会刷新原有光标。检测到 `IsGridFocusActive` 或 `mMagnifier` 时，后续点击直接交还游戏，不被放置器或 TAS 按钮抢占；轻松放置图标在放大及恢复动画期间隐藏。Esc 和移动端返回仍走原生退出路径。

主要源码位置：`Lawn/Board.cs` 的 `CanSelectGridFocus`、`SelectGridFocus`、`HandleGridFocusClick`、`LeaveGridFocus`、`KeyDown`、`BackButtonPress`、`Update` 和 `DrawGameObjects`。
