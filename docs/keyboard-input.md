# 键盘输入与输入法

本文记录 PGvZ v1.2.6 的键盘事件链，以及修改器为非英文输入法所做的适配。

## 游戏输入链

桌面版在 `Sexy.Main.HandleInput()` 中调用 MonoGame 的 `Keyboard.GetState()`。新按下的物理键依次传给：

```text
Keyboard.GetState
  -> WidgetManager.KeyDown(KeyCode)
  -> 当前焦点 Widget.KeyDown(KeyCode)
  -> Board.KeyDown(KeyCode)（关卡内）
```

这条链传递物理 `KeyCode`，不依赖当前输入法。游戏的字符输入则来自另一条链：

```text
SDL 文本输入/输入法
  -> SdlIMEHandler.TextInput
  -> WidgetManager.KeyChar(SexyChar)
  -> 当前焦点 Widget.KeyChar(SexyChar)
```

中文等输入法会先把字母放入组合串并显示选词框，因此字母不一定立即产生 `KeyChar`。数字还可能被候选词选择逻辑吞掉。游戏原生快捷键主要写在 `Board.KeyChar()` 中，所以也受该问题影响。

## 修改器适配

`pgvztool/keybinds.py` 中的 `KeybindHandler` 统一管理配置、物理映射、输入法状态和功能分发，并将常用 ASCII 字母、数字、控制键和美式键位标点转换为 `(KeyCode, Shift)`。`pgvztool/hook.py` 仅保留项目要求集中声明的 Hook，并将 `Board.KeyDown()` 等事件委托给处理类。

桌面 SDL 后端在 `Board` 获得焦点时关闭文本组合，因此按下字母快捷键前输入法不会建立组合串，也不会显示或闪烁选词框。焦点离开 `Board` 后立即恢复文本组合，用户名等文本框仍可正常输入。由于修改器可能在关卡已经开始后才由网页连接加载，`Board.Draw()` 还负责首次状态同步。

安卓后端不会执行桌面 SDL 的开关操作。安卓软键盘仍走平台文本输入，外接物理键盘能否产生 `KeyDown` 由系统和 MonoGame 后端决定。

## 兼容边界

- 常用 ASCII 键位使用物理映射，不受中英文输入法影响。
- 标点的物理映射采用 MonoGame `Keys.Oem*` 的常见美式布局。若特殊键盘布局仍拦截或改变键位，可切换英文输入法。
- 如果 `keybinds.txt` 使用无法映射的 Unicode 单字符，修改器不会在 `Board` 中完全关闭文本组合，而是保留 `KeyChar` 兼容路径。
- `WidgetManager.SetFocus()` 负责界面切换时同步状态；窗口重新获得焦点时由 `WidgetManager.GotFocus()` 再次同步。

## 反编译参考

- `Sexy/Main.cs`：`Initialize()` 中的 `SdlIMEHandler.TextInput` 注册，以及 `HandleInput()` 的物理键轮询。
- `Sexy/WidgetManager.cs`：`SetFocus()`、`GotFocus()`、`KeyDown()`、`KeyChar()` 和 `HandleGlobalIME()`。
- `Sexy/EditWidget.cs`：文本框获得和失去焦点时的 IME 热区状态。
- `Lawn/Board.cs`：关卡内 `KeyDown()` 与 `KeyChar()` 的原生快捷键逻辑。
