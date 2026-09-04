# Windows 控制台版游戏

桌面端脚本可以通过游戏控制台查看 `Sexy.Debug.Log()` 等调试输出。Windows 程序
根据 PE 文件头中的 `Subsystem` 字段决定是否为进程连接
控制台。因此，在 `cmd`、PowerShell 或 Windows Terminal 中直接运行 GUI 子系统的
`Lawn.exe`，通常仍然只会显示游戏窗口。

## 一、问题来源与版本差异

游戏历史版本使用过不同的 .NET 发布方式，控制台版不一定可用：

- 有些版本保留外置 `Lawn.dll`。这类版本的 `Lawn.Console.exe` 是控制台启动器，和
  `Lawn.dll` 放在一起时可以正常启动。
- 有些版本把游戏程序集和运行时打包进单个 `Lawn.exe`，但附带的
  `Lawn.Console.exe` 仍是依赖外置 `Lawn.dll` 的小型启动器。由于发布目录没有
  `Lawn.dll`，运行时会报告：

  ```text
  The application to execute does not exist: ...\Lawn.dll
  ```

这个问题来自游戏的发布配置，不是 PGvZ-TAS 或脚本造成的。受影响版本中的单文件
`Lawn.exe` 已包含完整游戏，仅仅被标记为 Windows GUI 子系统。仓库工具会复制这个
文件，并把副本的子系统标记由 `WINDOWS_GUI`（2）改为 `WINDOWS_CUI`（3），不会解包
游戏或修改原文件。

## 二、判断是否需要生成

先直接运行游戏目录中的 `Lawn.Console.exe`：

1. 如果游戏和控制台都正常打开，直接使用该文件。
2. 如果提示找不到 `Lawn.dll`，并且游戏目录确实没有该 DLL，则使用下一节的工具。
3. 如果报错内容不同，不要盲目转换；先确认 `Lawn.exe` 本身能够正常启动。

## 三、使用仓库工具生成

工具位于 [`tools/make-console-game.ps1`](../tools/make-console-game.ps1)。生成的文件必须
和 `Lawn.exe`、`Content/` 等游戏文件放在同一目录。

1. 完全退出游戏。
2. 如果游戏安装在 `C:\Program Files` 下，以管理员身份打开 PowerShell；其他可写目录
   通常不需要管理员权限。
3. 切换到 PGvZ-TAS 仓库根目录并运行：

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\tools\make-console-game.ps1
   ```

默认读取：

```text
C:\Program Files\ZBC\PlantGirlsVsZombies\Lawn.exe
```

并在同一目录生成：

```text
Lawn.Console.Fixed.exe
```

非默认安装位置使用 `-GameDirectory`：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\make-console-game.ps1 `
  -GameDirectory 'D:\Games\PlantGirlsVsZombies'
```

如果目标文件已经存在，工具默认拒绝覆盖。确认游戏已关闭后可使用 `-Force` 重新生成：

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\make-console-game.ps1 -Force
```

运行生成的 `Lawn.Console.Fixed.exe`，即可同时打开游戏窗口和控制台窗口。

## 四、注意事项

- 工具只生成副本，不会修改 `Lawn.exe`。不要用生成文件替换或删除原始游戏程序。
- 游戏更新后，单文件程序中的游戏代码也会变化，必须从新版 `Lawn.exe` 重新生成，不能
  沿用旧的 `Lawn.Console.Fixed.exe`。
- 修改后的副本与发行方提供的文件哈希不同，安全软件可能将其视为未知程序。
- 如果工具提示源文件的 `Subsystem` 不是 2，说明该程序不是预期的 GUI 构建，工具会
  保持文件不变并停止。
