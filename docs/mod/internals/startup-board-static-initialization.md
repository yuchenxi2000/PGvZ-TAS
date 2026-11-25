# 启动阶段 `Board` 静态初始化与墓碑关卡数组越界

## 现象与结论

已知报告来自 1.4.3 版修改器。进入带墓碑的关卡时，游戏可能抛出：

```text
System.IndexOutOfRangeException: Index was outside the bounds of the array.
   at Lawn.Board.PickSpecialGraveStone()
   at Lawn.Board.PickBackground()
   at Lawn.Board.InitLevel()
```

这不是墓碑关卡随机生成了非法坐标，也不是存档或关卡数据损坏。真正的错误发生在更早的
游戏启动阶段：修改器过早访问 `Lawn.Board`，使其静态初始化在场地尺寸常量仍为默认值 0
时执行。`Board` 静态字段中的墓碑候选格数组因此以错误容量创建，之后
`Constants.Load*()` 虽然会把场地尺寸改成正确值，却不会重新执行 `Board` 的静态初始化或
重建该数组。直到 `PickSpecialGraveStone()` 首次写入候选格时，问题才表现为数组越界。

因此，异常堆栈展示的是**损坏状态首次被使用的位置**，而不是**损坏状态产生的位置**。
普通关卡不调用这条墓碑选择路径，即使玩很久也可能完全看不到异常。

## 游戏的实际启动顺序

当前支持版本的反编译代码中，关键调用顺序为：

```text
Main.Initialize()
├─ IronPyInteractive.Serve()
│  ├─ PyHub.Initialize()
│  │  └─ RunAllModules()                 执行 mods/ 顶层 .py 文件
│  └─ mWS.Start()                        开始接受 /Py WebSocket 连接
└─ base.Initialize()
   └─ Main.LoadContent()
      ├─ SetupForResolution()
      │  └─ Constants.Load*()            设置 GRIDSIZEX、MAX_GRIDSIZEY 等
      ├─ GlobalStaticVars.initialize()
      │  └─ 创建并启动 LawnApp
      ├─ 加载启动画面所需内容
      └─ gSexyAppBase.StartLoadingThread()
         └─ mLoadingThreadStarted = true
```

这里容易产生两个误解：

1. `Constants.Load*()` 不是由 `Constants` 类型的静态初始化自动调用。游戏必须先在
   `SetupForResolution()` 中确定分辨率，再显式调用对应函数。
2. 并不是“所有静态变量都在模组加载后初始化”。CLR 会在某个类型首次需要时执行其类型
   初始化器；顶层模组对 `Board` 的导入、反射或 Hook 注册可以把这个首次访问提前到
   `Constants.Load*()` 之前。

游戏原本的正常流程会在场地尺寸配置完成后才使用 `Board`，所以游戏自身通常不会触发
这个顺序问题。IronPython 服务和顶层模组执行被放在 `base.Initialize()` 之前，才给外部代码
留下了提前访问游戏类型的窗口。

## 为什么旧版修改器更容易触发

1.4.3 版修改器仍以顶层 `cheat.py` 加载，其中直接执行 `from pgvz import *`，随后注册涉及
`Board` 的 Hook。游戏扫描模组时就会执行这些语句，因此可能在
`Main.LoadContent()` 之前触发 `Board` 静态初始化。

后来改用顶层 `cheat-gui.py` 配置路径和启动静态文件 HTTP 服务，
`pgvz/` 与 `pgvztool/` 包由网页连接后的引导代码导入。这避免了顶层模组必然提前访问
`Board`，但还存在一个较小的时间窗口：`IronPyInteractive.Serve()` 已经接受 WebSocket
连接，而 `Main.LoadContent()` 尚未配置常量；如果网页此时立刻执行引导代码，同样可能重现
问题。

网页打开得晚、设备启动得快或没有立即连接时，`Constants.Load*()` 已经执行完成，错误便
不会产生。这解释了为什么同一版修改器可能有人稳定遇到，而其他人长时间测试也无法复现。

## 就绪标志的选择

### 不能使用 `Constants.Loaded`

`Load320x480()` 等 `Constants.Load*()` 函数在靠前位置就把 `Constants.Loaded` 设为
`true`，后面才继续为大量运行时常量赋值。轮询线程可能在函数尚未结束时观察到 `true`，
它不是可靠的“常量加载完成”屏障。

### 不使用 `LawnApp.mLoaded`

等待整个 `LawnApp` 加载完成当然足够安全，但这要等进度条结束后才能进入修改器，明显晚于
本问题实际需要的时间点。

### 使用 `gSexyAppBase.mLoadingThreadStarted`

`Main.LoadContent()` 在完成 `SetupForResolution()`、全局对象初始化和 `LawnApp` 的启动步骤
后，最后调用 `gSexyAppBase.StartLoadingThread()`；该方法将
`mLoadingThreadStarted` 设为 `true`。因此当前支持的游戏版本中，它同时满足：

- 严格晚于 `Constants.Load*()` 返回，场地尺寸常量已经完整赋值；
- 早于后台加载进度结束，用户仍可在显示进度条时进入修改器；
- 属于已有生命周期字段，无需通过固定延时猜测不同设备的启动速度。

这个字段是针对当前反编译实现选定的顺序屏障。适配新的游戏版本时，如果
`Main.LoadContent()` 或 `StartLoadingThread()` 的调用顺序发生变化，必须重新核对，不能只因
字段仍然存在就认为它继续可靠。

## 当前修改器的规避流程

正式入口在主线程配置搜索路径并启动 HTTP 后台线程。HTTP 服务在后台加载，
模组加载线程只导入 `Sexy` 并每 100 毫秒检查游戏就绪标志。观察到
`gSexyAppBase` 已创建且 `mLoadingThreadStarted` 为 `true` 后，加载线程才导入 `pgvztool`，
加载 `pgvz` 并注册 Hook。浏览器通过 `/api/status` 查询这次加载的结果。
调试入口收到首次状态请求后，以相同的就绪条件启动加载。协议详见 [启动就绪探测](cheat-gui-protocol.md#启动就绪探测)。

## 修复边界

当前方案保护正式入口和调试网页引导的初始化顺序，但不能修改游戏已经创建的
错误静态数组，也不能约束其他代码：

- 如果仍安装旧的顶层 `cheat.py`，它会在网页探测之前执行；
- 其他模组、调试器或第三方 WebSocket 客户端也可能提前访问 `Board`；
- 一旦本次进程中的 `Board` 静态初始化已经以错误尺寸完成，稍后再等待或重新连接网页都
  无法恢复，必须重启游戏；
- 从游戏本体层面彻底防御，需要游戏作者让 `Board` 静态初始化不再依赖尚未加载的可变运行
  时常量，例如在常量加载后创建数组、按需检查并重建容量，或把候选数组改为方法内动态
  分配。

因此，在最新版仍看到相同堆栈时，应先检查是否残留旧版顶层模组、是否混用了不同版本的
`gui/` 与 Python 文件，以及是否有其他工具在启动阶段连接 `/Py`，而不能仅根据墓碑函数的
堆栈判断当前 GUI 的等待逻辑失效。

PC 自动安装脚本会检测这个旧版 `cheat.py`，并将其改名为以 `.disabled` 结尾的文件；这样
既保留原文件供检查或恢复，也阻止游戏继续把它当作顶层模组加载。手动安装和安卓版应直接
删除这个旧入口。

## 验证方法

由于错误静态状态会保持到进程结束，每轮验证都应从彻底退出并重新启动游戏开始：

1. 冷启动游戏，进入关卡并观察自动收集是否在打开网页前生效；
2. 另一次冷启动后立即打开网页，确认页面等到加载完成后可操作；
3. 进入会调用 `PickSpecialGraveStone()` 的墓碑关卡，检查有无上述 `IndexOutOfRangeException`；
4. 如需验证探测本身，观察后台加载途中返回 `bootstrapReady: false`，结束后返回 `true`。
