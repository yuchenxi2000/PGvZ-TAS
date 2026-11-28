# 主界面「修改器」按钮

PGvZ 1.4.3 的主界面用 `GameSelector` 管理按钮。「在线关卡」是 `DockMainMenuButton`，继承自「作者主页」使用的 `MainMenuButton`，长按时可展开「本地关卡」。两者共用底图、标签和按压动画。

`GameSelector.Update()` 经 `UpdateScreen()`、`UpdateUIPosition()` 调用 `UpdateSmallButtonPosition()`，按当前虚拟屏幕宽度重排按钮。修改器在原生布局完成后，将自己的单击按钮放到「在线关卡」正下方，沿用它与「作者主页」之间的行距。按钮属于当前 `GameSelector` 的子控件，页面滑动时随父控件移动，离开主界面销毁菜单时由游戏清理。

箭靶图标来自 `AtlasResources.IMAGE_BUNGEETARGET`。按钮使用缩小后的 atlas 子图，共用原图纹理，并通过 `mInvScale` 调整纹理采样比例。

`GameSelector.ButtonPress()` 播放原生点击音效。`ButtonDepress()` 中「作者主页」通过 `LawnApp.OpenUrl()` 打开网址，修改器用同一方法打开本机网页，并沿用原生的存档及菜单滑动检查。HTTP 服务绑定成功后通过 `_pgvz_gui_http` 公布实际端口，点击时读取该端口。Windows 版的 `OpenUrl()` 通过 `Process.Start()` 和 `UseShellExecute` 交由系统处理。

没有可用端口时，按钮用 `DoDialog()` 显示 ID 为 `901` 的提示框。`SexyAppBase.DialogButtonDepress()` 将「好的」转为 `LawnApp.ButtonDepress(2901)`，由默认分支调用 `KillDialog(901)`。原生对话框 ID `7` 对应更新确认，其确认分支还会调用 `CheckForUpdates()`。
