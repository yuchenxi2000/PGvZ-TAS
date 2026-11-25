# 修改器通信协议

## 整体架构

```
浏览器 (gui/index.html + gui/js/)
    ├─ HTTP (localhost:58080) → 静态文件和 JSON API
    │                                  ↕ 请求 / 结果
    │                             GuiDispatcher
    │                                  ↕ 游戏主线程 run_pending()
    │                     CheatActions / Placer / SyncRegistry
    └─ Python 调试（手动发送时）→ 游戏内置 WebSocket /Py
```

- `gui/js/connection.js` 负责 HTTP 请求、页面会话和状态同步。
- `gui/js/debug.js` 负责调试页的自定义 Python 代码。它只在用户发送代码时建立 WebSocket。
- `gui/js/options.js` 定义开关分组、默认值和本地存储，`gui/js/app.js` 负责 Vue 界面与业务交互，
  `gui/js/terrain.js` 负责地形草稿与拖选。
- `pgvztool/gui_http.py` 提供静态文件、启动状态以及 JSON 请求和轮询接口。
- `pgvztool/dispatcher.py` 管理请求队列、动作映射和结果，`pgvztool/sync.py` 管理会话与状态版本。
- `pgvztool/hook.py` 提供主线程执行入口。动作在 `cheat_actions.py`、`placer.py` 和 `speed.py` 中同步执行。

普通按钮调用 `sendAction(name, args)`，开关与放置器选项调用 `applyState(state)`。
HTTP 线程只读已发布的响应数据。读取或修改游戏对象的业务逻辑均由主线程执行。

## 启动就绪探测

游戏在 `Main.Initialize()` 中执行顶层模组，随后才通过 `base.Initialize()` 进入
`Main.LoadContent()`。正式入口 `cheat-gui.py` 在主线程配置搜索路径并启动后台线程。
HTTP 模块加载、版本文件读取和端口监听均在后台进行。模组加载线程每 100 毫秒检查
`Sexy.GlobalStaticVars.gSexyAppBase.mLoadingThreadStarted`。
该标志晚于 `Constants.Load*()`、`GlobalStaticVars.initialize()` 和 `LawnApp.Init()/Start()`。
观察到它之后才导入 `pgvztool`、加载 `pgvz` 和安装钩子。具体顺序见
[启动阶段 Board 静态初始化](startup-board-static-initialization.md)。

`/api/status` 返回本次启动的 `instance`、加载是否结束的 `ready`、`error`（导入失败的完整调用栈）、
`version`、`modVersion` 和 `supportedVersions`。版本声明从 `pgvz/version.py` 独立读取，因此包导入
失败时仍可提示游戏与模组版本是否匹配。网页在 `ready:false` 时继续询问，加载失败时显示错误。
调试入口收到首次状态请求后才启动同一加载流程。

## HTTP 接口

同一个服务在 `127.0.0.1:58080` 提供静态文件和 JSON API。网页使用相对路径访问接口。
`Host` 仅接受 `localhost` 和 `127.0.0.1` 的实际监听端口，并检查请求携带的 `Origin`。
POST 接口要求 JSON 和 `X-PGvZ-Instance`，旧进程的请求到达新进程时返回 HTTP 409。

| 接口 | 用途 |
|---|---|
| `GET /api/status` | 查询启动状态和版本 |
| `POST /api/request` | 提交动作、设置、会话或快照请求，返回入队确认 |
| `POST /api/poll` | 按 `_clientId` 领取结果和 `revision` 之后的状态更新，可附带 `acknowledged` 与 `cancelled` 请求 ID |

`/api/poll` 返回 `results` 和 `updates`。网页有待处理动作时每 100 毫秒轮询一次，
已连接且空闲时每秒轮询一次，同一时刻最多一个轮询在途。

## Python 调试通道

调试页的自定义 Python 通过游戏的 `IronPyInteractive` 服务执行。`FindAvailablePort()` 从
`8080` 开始逐个查找可用端口。网页调试端口默认填 `8080`，接受 `8080` 到 `65535` 的整数。
发送代码时连接输入框指定的本机端口，端口变更后下一次发送会切换连接。
普通 GUI 请求、启动和状态同步都走 HTTP。

PGvZ 1.4.3 的顶层模组由 `RunAllModules()` 创建独立作用域，`PyHub.OnMessage()` 在回调线程
使用共享的交互作用域 `mPyScope`。两条路径共享 `sys.modules`。调试页可在修改器就绪后
向交互作用域导入 `pgvz` 和 `pgvztool` 的辅助接口。调试服务返回 `execution` 事件，
表达式结果是 Python 的 `repr()` 文本，异常正文在 `result`，另有独立的 `output` 日志事件。
Python 调试代码调用游戏对象时仍需遵守主线程约束。

## 应用层协议

### HTTP 静态文件边界

正式和调试入口以 `mods/gui/` 为 URL 根目录。URL 解码后统一斜杠，通过 `abspath()`
规范化路径，再用 `normcase()` 比较目录边界，允许 `gui` 本身及其子路径，拒绝穿越到父目录
或同名前缀的相邻目录。越界的 GET/HEAD 请求返回 403；查询参数不参与文件定位。

目录检查不解析符号链接或 Windows junction，用户可自行通过链接访问其他位置的文件。
路径段末尾的点、空格等由操作系统处理，不添加专门限制。

### GUI 多页面会话

同一设备可同时打开多个页面，每个页面实例生成唯一 `_clientId`。连接和释放在主线程
调用 `SyncRegistry.connect()` 和 `release()`，释放只影响发起该请求的页面。游戏后台暂停、
网页后台挂起和空闲期间，页面可以继续领取其结果。动作在主线程按服务器入队顺序执行，
同一字段连续收到多个修改时，最后执行的值生效。

每个游戏进程只在首个成功连接时应用随请求提交的 PC 恢复设置并生成快照。如果第一个页面
未提交设置，所有页面从游戏当前状态开始。后续连接均读取快照，包括关掉所有页面后再打开。
这一规则也适用于首次连接回包丢失后的重连。

主线程在动作、选项和快照请求执行前校验页面是否已加入。未加入或已释放的页面收到
`SessionRejected`。结果队列按页面 ID 隔离，各页可以领取自己的初始化和动作结果。
网络线程只领取已生成的共享状态更新与页面结果。

### 请求、执行和结果交接

网络线程只调用 `gui_dispatcher.submit(json_str)`、`poll(client_id)`、
`acknowledge(client_id, json_ids)` 和 `cancel(client_id, json_ids)`，后两者仅处理队列元数据。
`submit()` 验证请求外壳后入队，立即返回 `queued`；所有会话、状态和业务调用都在
`run_pending()` 中执行。请求格式如下：

```json
{"_clientId":"client-id","id":"client-id:1","kind":"action","name":"placeZombie","args":{"row":0,"col":2,"zombieType":"Normal","mindCtrl":false}}
```

| kind | 附加数据 | 主线程处理 |
|---|---|---|
| `connect` | PC 携带 `state`，手机省略 | 加入会话并返回状态快照，仅首个成功连接可恢复设置 |
| `apply` | `state` | 验证会话并应用选项，返回请求字段的实际状态 |
| `snapshot` | 无 | 验证会话并读取完整状态 |
| `action` | `name`、`args` | 按白名单转换参数，同步调用业务方法 |
| `release` | 无 | 释放会话并清理该页面未领取的结果，不等待完成回包 |

动作映射及参数类型定义在 `GuiDispatcher._actions`。分发器只做协议适配，游戏字段访问
留在 `CheatActions`、`Placer` 和框架 API 中。参数名必须匹配，布尔值、整数和枚举名称经过
类型转换后才调用 `handler(*values)`；没有装饰器绕过或第二次排队。

```json
{"action":"queued","id":"client-id:1"}
```

`queued` 只表示入队，界面显示“已发送，切回游戏后生效”。存在待完成请求时，网页以 100 毫秒
间隔调用 `poll()`；同一时间最多有一次结果轮询在途。首次连接也用这一机制，不能等到
`connected` 为真后才开始轮询。结果格式如下，`value` 为可 JSON 序列化的返回值：

```json
{"action":"results","results":[{"id":"client-id:1","kind":"action","name":"placeZombie","ok":true,"value":null}],"updates":[]}
```

执行异常保留请求 ID、kind 和 name，并返回 `ok: false`、`errortype` 和 `error`。
结果不会在 `poll()` 时删除，网页处理后通过 `acknowledge()` 确认，确认后不再主动回传；
因此页面后台挂起后仍能领取结果。未确认结果没有时间过期；已确认或放弃的完成记录在
完成至少 60 秒后清理。在这段缓存期内，同一页面重复提交相同 ID 和内容只重新领取结果，
不会重复执行；同一 ID 携带不同内容会报错。页面重连不重放旧操作，也不在缓存过期后自动
重试原动作。

请求排队和结果等待没有 30 秒限制。等待期间不额外显示后台暂停提示，不自动取消
请求、重发操作或重置初始化。首次同步完成前，业务控件禁用；即使调用前端 API 也会拒绝
发送，不建立引导期间的本地待发队列。调试代码仍允许在未初始化时直接发送。

提交按页面顺序发送。网页在提交后开始轮询，结果回包附带请求 ID，重复或迟到的结果会确认，
界面仅应用一次。页面退出时用 `fetch(..., {keepalive: true})` 尽力发送 `release`。
服务器在收到退出请求时同时撤销该页面已排队的动作，并拒绝随后才到达的普通请求。
主线程随后释放该页面的会话。已经开始执行的游戏操作继续完成，其他页面仍可操作。

### 后台暂停等待与连接恢复

手机网页在前台、游戏在后台暂停，或 PC 关闭后台运行时，HTTP 服务可能仍可接收请求，
但游戏主线程暂时不会推进 `run_pending()`。排队中的请求可长期等待，空轮询不触发重连或重发。
手机系统也可能挂起整个游戏进程，此时正在进行的 HTTP 请求可能停住，至恢复后继续。

HTTP 连接失败或服务实例变更时，网页约 3 秒后重新查询状态，并用原有页面 ID 重新申请会话。
旧动作不自动重放，已经提交但没有回包的动作显示为执行结果未确认。
PC 的恢复设置只在每个游戏进程的首个成功连接时应用，手机通过会话快照获取状态。
启动导入和会话初始化错误直接显示，便于排查。

网络线程入队、读取或确认回包时短暂持有队列锁。主线程执行会话校验、参数转换、游戏调用和
状态序列化期间不持此锁。

### 状态快照和选项应用

`SyncRegistry` 注册 `cheat`（`CheatOption`）、`placer`（`Placer`）、`weather`
（`WeatherControl`）和只读的 `speed`。`Serializable.to_dict()` 自动读取公开的简单实例属性和 `@property`，
不需要登记字段表。`from_dict()` 按现有属性逐项应用：简单属性直接赋值，.NET 枚举通过
`System.Enum.Parse()` 转换，不额外校验类型或范围。不存在、私有或不支持的属性会跳过；
枚举转换失败、属性只读或赋值时出现类型转换错误，也跳过该项并继续处理其余选项。
未知状态对象和非字典的对象数据同样忽略，不做整份请求预校验。

这些操作都在主线程完成，包括 `noCooldown` 对游戏字段的读写和脚本开关的启停。
会话校验保持不变；其他游戏运行时异常仍按请求 ID 回传。

`connect` 和 `snapshot` 请求的 `value` 是完整的 `sync` 消息。`apply` 返回相同结构，`state` 仅含请求涉及的可序列化字段，字段值在全部写入完成后从游戏重新读取。没有可返回的字段时，`apply` 的 `value` 为 `null`。

```json
{
  "action": "sync",
  "revision": 1,
  "modVersion": "1.18.0",
  "gameVersion": "1.4.3",
  "state": {
    "cheat": {"freePlant": false, "autoCollect": true, "noCooldown": false},
    "placer": {"seedType": "Peashooter", "easyPlaceEnabled": true},
    "weather": {"enabled": false, "rain": false, "storm": false}
  }
}
```

天气的五档前端选项映射为 `enabled`、`rain` 和 `storm`；`enabled` 为 false 时使用关卡
默认天气。界面通过 `applyState({ cheat: { [key]: value } })` 或
`applyState({ placer: { [key]: value } })` 提交修改，分发器加入会话 ID 后交给同步注册表。

### 模组主动推送状态

游戏主线程中，模组修改已注册状态后调用 `sync_reg.push_state(**groups)`。形参名是注册的状态组，字符串选一个字段，字段名序列选多个字段，`None` 读取整组：

```python
from pgvztool import cheat_option, sync_reg

cheat_option.freePlant = True
sync_reg.push_state(cheat='freePlant')

# 同一条消息可包含多个组，由 API 读取它们在游戏里的当前值。
sync_reg.push_state(cheat=('daisyMode', 'danceMode'), weather=None)
```

未注册的组，以及未知、私有或不可序列化的字段自动跳过。没有活动网页会话时不读取状态，也不缓存推送。已有网页重新连接时，会通过 `connect` 取得完整快照。新增组可沿用 `SyncRegistry.register()`，若要影响官方网页的控件，还需在 `applySyncState()` 接入相应的界面状态。

主线程保存每个字段最近一次更新及其原始 `revision`，包括网页提交的选项及速度变化。
所有活动网页各自按 HTTP 轮询的修订号领取变化，按组和字段比较版本，再与快照、动作回包合并。
部分天气状态沿用之前收到的字段。
远端更新不回发 `apply`。PC 保存收到的复选框状态，手机只更新当前页面。

### 内置作弊菜单同步

PGvZ-TAS 在游戏主线程安装 `ZBCheatDialog` 的 IL 钩子。复选框 5（自动收集资源）、8（房主无敌）和 11（后台运行）分别写入 `cheat.autoCollect`、`cheat.wontLose` 和 `cheat.runBackground`，在状态生效后推送该字段。菜单刷新时也从 `CheatOption` 读取这三个状态，设置复选框时关闭监听回调。

挂钩内置菜单时关闭已有的原生自动收集、房主无敌钩子。玩家资料载入时尝试重新开启原生自动收集的调用也会被拦截。后台运行字段立即写入 `Main.RunWhenLocked`，失焦时仍通过现有钩子应用。三个内置复选框沿用 PGvZ-TAS 的同步和保存规则，PC 由网页保存收到的状态。

`SyncRegistry.set_local_state()` 记录本次游戏进程中经内置菜单操作过的字段。网页第一次连接时，恢复的本地设置跳过这些字段，快照返回游戏中的实际值。之后网页主动发送的 `apply` 照常生效。

内置菜单更新时也检查全局速度字段。网页或脚本改速后，菜单用游戏原有的 `GetGameSpeedString()` 刷新“速度控制 当前”标签。
慢速档小数超出原标签宽度时，显示精确的倒数分数，例如 `1/3x`。测量使用 `StashFont` 实现的
`StringWidth()`，因为 IronPython 在该类型上无法调用 `Font.MeasureString()` 的默认接口实现。

### 彩蛋状态

“关卡与显示”的六个彩蛋开关以 `cheat` 属性同步。`cheat_option` 读取 `LawnApp` 的全局字段，网页写入时同时应用到当前 `Board`，无需通过键盘口令的智慧树高度检查。`Board.LoadGame()` 成功后，挂钩用当前 `cheat_option` 恢复关卡的彩蛋状态，并在应用期间暂时静音。音效按钮使用独立的 `playKonamiSound` 动作，由主线程调用 `LawnApp.PlayFoley(FoleyType.Drop)`。

`Board.DoTypingCheck()` 和 `GameSelector.KeyDown()` 对比原生按键处理前后的彩蛋状态，通过 `push_state()` 发送实际变化的字段。

### 速度控制

连接快照包含只读的 `speed` 组。`global` 和 `board` 各自以 `{numerator, denominator}`
表示实际速度，`board` 另带当前 Board 的 `id`。没有 Board 时 `board` 为 `null`，全局速度字段
无法表示有效值时 `global` 为 `null`。每个比例作为一个字段参与版本合并，分子和分母始终一起更新。
速度使用当前游戏状态，PC 和手机均不保存或恢复这些字段。

`setGlobalSpeed` 接收 `{value}`，`setBoardSpeed` 接收 `{boardId, value}`，其中 `value` 为整数、
小数或分数字符串。全局入口只接受可精确表达的整数倍和整数倒数倍。关卡入口原样写入分数，
小数则通过框架的连分数转换。关卡动作在执行时核对 Board 标识，换关后返回 `SpeedBoardChanged`，
无效速度返回 `InvalidSpeed`。成功回包携带对应字段的 `sync` 消息，沿用推送的版本顺序。

有活动网页时，`DoUpdateFrames()` 在原方法返回后比较两项实际速度与最近发送的状态，按变化字段
推送。原生按钮、脚本和直接写游戏字段的调试代码都通过这条路径更新网页。网页更新当前值和快捷档，
输入草稿由用户编辑，提交中的动作由对应回包确认。相关底层限制见[游戏速度控制机制](../../game-mechanics/other/speed-control.md)。

### 布阵码

`sendAction('getLineup')` 在主线程调用 `cheat_actions.GetLineup()`，返回布阵码字符串。
`sendAction('applyLineup', { code })` 调用 `cheat_actions.LineUpOnBoard(code)`。
前端不访问 `Board`，也不构造包含用户输入的 Python 表达式。

### 地形编辑

“地形”页只在点击“读取当前地形”时用 `sendAction('getTerrain')` 读取当前关卡，可丢弃
草稿并重新读取；打开页面、换关或生存换轮不会自动读取。返回值包含背景枚举名 `background`、行优先的 `grid`（6×9）
及 `rows`（六个行类型名）。后端负责将网页的 `grid[row][col]` 转换为游戏的 `[col, row]`。
页面初始和断线重置后均显示默认草稿：白天、前五行 `Grass` / `Normal`、第六行九格及行类型均为 `Dirt`；未进入关卡
或尚未连接时也显示完整编辑器，并允许本地编辑。无 Board 时手动读取返回同一默认设置。

`terrain.js` 保存一份独立草稿和读取时的基准值。背景选择、单格点击、键盘 Enter/Space
及矩形拖选只更新草稿；拖选期间预览选区，松开指针后填色，取消指针则放弃选区。
两侧共用外层指针捕获和选区，格子列为 0..8、右侧行类型为第 9 列，拖选可跨越两部分，
也可从行类型反向拖至格子。中间间隔不作为单元格，不可在间隔起选；拖入间隔但尚未
到达另一侧时，不选中另一侧。选区行号按对齐后的六行计算。
格子与行类型共用一组画笔：草地、裸地、泳池、高地、浅水。“草地”写格子时为 `Grass`，
写行类型时为 `Normal`，其余同名对应；画格子和画行类型仍独立修改对应数组。
不提供 `None` 画笔，但手动读取到的既有 `None` 格子保留原值并显示为“—”。
“实施修改”调用 `sendAction('applyTerrain', { background, grid, rows })`。
`connection.js` 将已确认、尚未处理的动作结果通过 `onActionResult` 交给编辑器，成功时
采用后端返回的最新快照；失败时保留草稿，断线或失去会话时恢复默认草稿并清除等待状态。

动作执行前，分发器完整验证背景、格子和行类型的枚举名与数组尺寸，再调用业务方法。
`CheatActions` 在请求执行时取得当前 Board 并写入，不绑定读取时的关卡或生存轮次；
换关后仍可将网页草稿实施到当前关卡，不会因关卡已变化而报错。
背景改变时先赋值并调用 `LoadBackgroundImages()`，加载失败则恢复背景且不写地形数组。
成功后写入两组地形，再对有效格子内存活且 `NotOnGround()` 为假的植物调用
`Challenge.MovePlant(plant, plant.mPlantCol, plant.mRow)`，按新地形原地校正坐标与相关特效；
保龄球关卡跳过这一步，避免把滚动植物移回原始格子。血量、攻击计时和睡眠状态保留，
不额外调用 `UpdateReanim()` 推进动画，也不修改已有子弹。
随后返回实际快照，不调用 `PickBackground()`、出怪重建或已有对象重建。

地形不注册到 `SyncRegistry`，不写入 localStorage，也不作为 PC 恢复设置推送；没有逐帧
重设地形的脚本。这是对当前 Board 的一次赋值，后续游戏自身的存档或换轮行为仍按原生
逻辑处理。具体字段的影响见[场景、格子地形与行类型](../../game-mechanics/other/background-and-terrain.md)。

### 统一的主线程入口

`hook.py` 挂钩 `Sexy.SexyAppBase.DoUpdateFrames()`，先调用
`gui_dispatcher.run_pending()`，再原样调用 `orig(app)` 并返回原结果。此入口在 Board 更新
及全局快慢速分帧之前，因此主菜单、选卡界面、TAS 暂停或 Board 速度为零时都能处理请求。
不要将请求队列放到 `Board.UpdateGame()` 驱动的普通脚本中：`Board.Update()` 会在
`mManualPaused` 或 `mAccelerationNumerator == 0` 时提前返回，无法处理暂停中的请求。

入口选择依据本地 PGvZ 1.3.1 源码的 `SexyAppBase.UpdateApp()` →
`LawnApp.DoUpdateFrames()` → `SexyAppBase.DoUpdateFrames()` → `LawnApp.UpdateFrames()`
调用链。`LawnApp.DoUpdateFrames()` 只是一个很短的转发，可能被内联；基类实现包含加载
收尾步骤。原有框架更新钩子及脚本调度规则保持不变。

## 状态同步策略

### PC 端：推送模式

GUI 会将修改选项和放置器中的布尔开关保存到 `localStorage` 的 `pgvz-gui-checkbox-state` 项。
PC 页面启动时先读取保存值；缺失字段使用代码默认值。每次初始化（包括断线重连）都通过
`getInitialState()` 获取 `cheatOption` 和 `placer`，作为 `connect` 的 `state`。每个游戏进程
仅接受首个成功连接随附的恢复设置，后续页面都读取游戏当前状态。
因此首次初始化前长期暂停或断线不会丢失恢复设置，回包丢失也不会导致重复覆盖。

用户修改需要持久化的开关时立即保存，不等待游戏执行。`applySyncState()` 处理成功的
同步结果和有效的推送；远端更新期间 watcher 不保存或发回设置，待 Vue 更新完成后统一保存同步状态。
因此不存在用初始化失败、拒绝或迟到旧连接的快照覆盖 localStorage 的路径。

用户勾选复选框时，`watch(cheatOption)` 检测变化，通过 `setCheatOption(key, value)` 发送：

```javascript
applyState({ cheat: { [key]: value } });
```

### 手机端：拉取模式

手机浏览器可能被系统杀死后台页面，导致 GUI 内存状态丢失。手机端不读取或写入上述
`localStorage` 项，并始终将游戏内状态视为权威状态。HTTP 服务就绪后，GUI 通过不带
`state` 的 `connect` 请求拉取游戏状态。如果 HTTP 服务暂时不可访问，页面会重试。

## 如何新增一个修改选项

### 1. 添加属性 (pgvztool/cheat.py)

在 `CheatOption.__init__` 中添加属性：

```python
self.xxx = False
```

如果新选项对应脚本单例（有 On/Off 方法），在 `CheatOption` 类末尾加 `@property`：

```python
@property
def xxx(self):
    return script_xxx.enabled
@xxx.setter
def xxx(self, value):
    script_xxx.On() if value else script_xxx.Off()
```

`Serializable.to_dict()` 会自动发现公开简单属性及 `@property` 并包含在序列化中，无需登记字段表。

### 2. GUI 端：注册选项

在 `gui/js/options.js` 的对应 `switchGroups` 分组中添加 `'xxx'`。`optionConfig` 会自动从所有分组生成，`CheckGroupCard` 也会自动创建复选框，因此不需要再手写一份控件。随后在 `gui/js/i18n.js` 的中英文 `options` 中分别添加显示名称。

`createCheatOptions(savedCheatState, isMobile)` 在生成完整 `optionConfig` 后按平台过滤显示
分组：手机端隐藏不起作用的“后台运行”，电脑端隐藏原生没有遮挡的“去除立绘遮挡”。
隐藏不移除同步字段。“去除立绘遮挡”属于“常用修改”，前后端均默认开启；手机首次连接
仍拉取游戏当前选项，PC 已保存的显式选项值仍按原有恢复规则处理。

### 3. 通信流程

```
用户勾选复选框
  → Vue watch 检测 cheatOption.xxx 变化
  → setCheatOption('xxx', true)
  → applyState({cheat: {xxx: true}})
  → POST /api/request 提交 JSON
  → gui_dispatcher.submit(...) 将 apply 请求入队
  → hook.py 主线程入口 → SyncRegistry.apply(...)
  → json.loads → obj.from_dict → setattr(cheat_option, 'xxx', True)
  → 下一帧 hook 函数读取 cheat_option.xxx，执行对应逻辑
```

## 如何新增一个一次性动作

1. 在 `CheatActions` 或 `Placer` 中实现同步方法，在 `GuiDispatcher._actions` 登记动作名、
   后端方法及有序参数转换器。业务方法不处理网络、会话、排队或 JSON 包装。
2. 页面用 `sendAction('actionName', { argument: value })` 发送数据，不拼接 Python。
   如需返回数据，业务方法返回可以 JSON 序列化的值，连接模块读取结果的 `value`。
3. 挂钩操作只写在 `hook.py`；业务方法由现有入口在主线程直接调用，不添加 `@main_thread`，
   不通过 `__wrapped__` 绕过调度。主线程脚本可直接调用 `cheat_actions` 或 `placer`。

回归检查：`python -m unittest discover -s tests` 和 `node --test tests/test_gui.js`。
后者使用浏览器和 Vue 的最小模拟，验证协议与模块连接，不替代游戏内的 Hook 和 GUI 实测。
