# 修改器通信协议

## 整体架构

```
浏览器 (gui/index.html + gui/js/)
    ├─ HTTP (localhost:58080) ─────→ cheat-gui.py ─→ gui/ 静态文件
    └─ WebSocket (localhost:8080/Py) → 游戏 IronPython 引擎
                                              ↕ Python 对象
                            gui_dispatcher.submit / poll / acknowledge / cancel
                                              ↕ 请求 / 结果队列
                                    hook.py → 主线程 run_pending
                                              ↕
                      CheatActions / Placer / SyncRegistry
```

## 网页代码分工

- `gui/js/protocol.js`：引导探测代码、固定接口调用的编码、Python 字符串转义和结果解析。
- `gui/js/connection.js`：WebSocket 连接、引导、单客户端会话、待发送指令队列、请求结果轮询、心跳和重连。
- `gui/js/options.js`：开关分组、默认值和复选框状态的本地存储。
- `gui/js/app.js`：Vue 界面、业务操作、状态同步和组装上述模块。

这些文件按 `gui/index.html` 中的脚本顺序加载，不需要构建步骤。连接模块通过回调触发
`app.js` 中的 `getInitialState()` 和 `applySyncState()` 获取初始状态及应用远端状态；
PC 推送、手机拉取的规则不变。

常用按钮调用 `sendAction(name, args)`，开关与放置器选项调用 `applyState(state)`。
`index.html` 和 `app.js` 不访问 `Lawn`、`Sexy` 或游戏字段，也不构造 Python 枚举表达式。
后端分工：

- `cheat.py`：`CheatOption` 持续选项、`WeatherControl` 天气状态及相关逐帧脚本。
- `cheat_actions.py`：`CheatActions` 一次性作弊操作，显式持有 `CheatOption`。
- `placer.py`：同步放置、移除和场地交互，包括罐子内容的换算。
- `sync.py`：状态序列化、状态应用和 GUI 会话，运行时只由主线程访问。
- `dispatcher.py`：`GuiDispatcher` 请求协议、动作映射、跨线程队列和结果交接。
- `hook.py`：调用分发器的主线程入口，集中声明所有修改器挂钩。

`CheatActions` 和 `Placer` 的方法都同步执行，不带调度装饰器。游戏钩子和主线程脚本可
直接调用；WebSocket 代码必须通过分发器提交请求。调试区仍允许发送任意 Python，调用者
同样需要遵守主线程约束。启动就绪与版本探测发生在分发器导入前，仍留在协议模块。

## HTTP 服务器 (cheat-gui.py)

位于 `cheat-gui.py`，使用 Python 标准库 `http.server`。启动时自动挂在 `localhost:58080`，将所有请求路由到 `gui/` 目录下的文件。根路径 `/` 返回 `gui/index.html`。

游戏启动时只自动扫描 `mods/` 顶层的 `.py` 文件，因此此时执行的是 `cheat-gui.py`，它只配置模块搜索路径并启动 HTTP 服务。`pgvz/` 和 `pgvztool/` 是 Python 包，不会被游戏自动扫描；网页建立 WebSocket 连接并确认游戏同步初始化完成后，`gui/js/protocol.js` 中的 `BOOTSTRAP_CODE` 才会导入它们并注册相关钩子。

`Cache-Control: no-store, no-cache, must-revalidate` 等响应头用于防止之后的页面加载复用缓存。它不能停止已经在页面内存中运行的旧 JavaScript、重连定时器或 WebSocket；通过 `file://` 直接打开文件时也不存在这些 HTTP 响应头。仍在运行的旧页面由下述 GUI 会话协议拦截。

## WebSocket 服务 (localhost:8080/Py)

由游戏内 `IronPyInteractive` 启动（IronPyInteractive.cs:199-219）。行为类似 **Python 交互式控制台（REPL）**：

- **表达式**（如 `1+1`、`gui_dispatcher.poll(client_id)`）：执行后返回 `repr()` 的字符串结果
- **语句**（如 `cheat_option.xxx = True`）：执行后无返回值

服务端响应是统一的 JSON 格式：

```json
// 表达式有返回值
{"statuscode": 0, "result": "'repr-string'"}

// 语句无返回值
{"statuscode": 0}

// 异常
{"statuscode": 1, "error": "error message", "errortype": "ExceptionType"}
```

`PyHub` 允许多个 WebSocket 同时连接，所有连接共用同一个 IronPython `ScriptScope`。它本身没有客户端身份、认证或独占机制，因此直接连接 `/Py` 的其他程序可以执行任意 Python，也可以绕过下述 GUI 会话协议。若要拒绝所有来源的第二个 WebSocket 连接，需要修改游戏的 C# `PyHub` 服务端。

### 启动就绪探测

游戏在 `Main.Initialize()` 中先启动 IronPython WebSocket 并执行顶层模组，随后才通过
`base.Initialize()` 进入 `Main.LoadContent()`。场地尺寸等运行时常量由
`SetupForResolution()` 中的 `Constants.Load*()` 设置，因此 WebSocket 可以在这些常量尚未
完成初始化时就接受连接。

GUI 建立 WebSocket 后不会立即发送 `BOOTSTRAP_CODE`，而是先发送只导入 `Sexy` 的
`BOOTSTRAP_READY_PROBE_CODE`，检查：

```python
app = Sexy.GlobalStaticVars.gSexyAppBase
ready = app is not None and app.mLoadingThreadStarted
```

`mLoadingThreadStarted` 由 `Main.LoadContent()` 最后的 `StartLoadingThread()` 设置，晚于
`Constants.Load*()`、`GlobalStaticVars.initialize()` 和 `LawnApp.Init()/Start()`。探测未就绪
时网页每 100 毫秒重试；就绪后才导入 `pgvz` 和 `pgvztool` 并申请 GUI 会话。不能使用
`Constants.Loaded` 作为标志，因为各 `Constants.Load*()` 会在函数前段设置它，后续仍有
大量字段尚未赋值。

完整的异常表现、静态初始化根因、历史版本差异和修复边界见
[启动阶段 `Board` 静态初始化与墓碑关卡数组越界](startup-board-static-initialization.md)。

就绪响应使用 `{"action":"bootstrapReady","ready":...}` 与普通执行结果、状态同步和心跳
区分。自定义代码仍允许在引导失败时直接发送，以便调试。

### 游戏版本警告

启动就绪后，GUI 通过 `Lawn.LawnApp.AppVersionNumber` 获取游戏版本，并单独执行
`mods/pgvz/version.py` 读取 `MOD_VERSION` 和 `SUPPORTED_GAME_VERSIONS`。版本文件只声明
常量，在独立的命名空间执行时不会触发 `pgvz/__init__.py`。探测返回 `gameVersion` 消息，
包含实际游戏版本 `version`、修改器版本 `modVersion` 和支持列表 `supportedVersions`。

网页页眉的两个版本号均来自探测。实际游戏版本不在列表中时，网页显示警告并列出受支持
的版本。高于最高支持版本时提示下载新版修改器，其余不匹配情况提示更新游戏。随后网页
继续尝试导入 `pgvz` 和 `pgvztool`。即使包导入失败，已获取的版本和警告仍会显示。探测
缺少某个版本号时，页眉对应项显示占位符，网页继续引导。

### JSON 编码和 Python 字符串

游戏的 WebSocket 接收的是 Python 代码，因此请求需要先编码成 JSON，再编码成 Python
字符串字面量。`PGvZProtocol.requestCode(clientId, id, kind, details)` 统一处理这些步骤；
`index.html` 和 `app.js` 只调用 `sendAction()`、`applyState()` 等前端接口。

编码器转义反斜杠、单引号和控制字符；JSON 布尔值也不会被误当作 Python 语法。
服务端固定执行 `gui_dispatcher.submit(json_str)`，不能通过请求指定任意 Python 方法或字段。

响应的 `result` 字段是 Python `repr()` 输出。`PGvZProtocol.parseResultMessage()` 先去掉
外层引号、解码一层 Python 字符串转义，再解析 JSON，支持引号、反斜杠、换行和中文。
不能只用 `slice(1, -1)` 去掉引号。

## 应用层协议

### HTTP 静态文件边界

正式和调试入口以 `mods/gui/` 为 URL 根目录。URL 解码后统一斜杠，通过 `abspath()`
规范化路径，再用 `normcase()` 比较目录边界，允许 `gui` 本身及其子路径，拒绝穿越到父目录
或同名前缀的相邻目录。越界的 GET/HEAD 请求返回 403；查询参数不参与文件定位。

目录检查不解析符号链接或 Windows junction，用户可自行通过链接访问其他位置的文件。
路径段末尾的点、空格等由操作系统处理，不添加专门限制。

### GUI 单客户端会话

官方 GUI 的每个页面实例生成唯一 `_clientId`。连接、心跳和释放也作为请求排队，在主线程
调用 `SyncRegistry.connect()`、`heartbeat()` 和 `release()`。只允许一个活动页面，每
3 秒提交一次心跳，租约在 15 秒后过期；初始化同步失败时恢复此前的会话所有权。

后打开的页面收到 `sessionRejected` 后显示“另一个修改器页面已连接”，不再自动重连。
主线程在执行动作、应用选项或读取状态前调用 `require_client()`，因此排队期间失去会话的
请求也不会执行游戏操作。网络线程不读取或修改 `SyncRegistry`。

这是官方 GUI 的应用层保护，不是 `/Py` 服务的安全边界；直接发送任意 Python 的第三方
客户端不受这些调用约定限制。结果队列按页面 ID 隔离，`poll()` 仅交接已生成的 JSON 数据，
因此尚未获准的连接也能领取自己的初始化结果或拒绝消息。

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
| `connect` | PC 携带 `state`；手机省略 | 申请会话，可选恢复选项，返回状态快照或会话拒绝 |
| `apply` | `state` | 验证会话并应用开关、放置器或天气状态 |
| `snapshot` | 无 | 验证会话并读取完整状态 |
| `action` | `name`、`args` | 按白名单转换参数，同步调用业务方法 |
| `heartbeat` | 无 | 续租，返回 `heartbeat` 或 `sessionRejected` |
| `release` | 无 | 释放会话并清理该页面未领取的结果，不等待完成回包 |

动作映射及参数类型定义在 `GuiDispatcher._actions`。分发器只做协议适配，游戏字段访问
留在 `CheatActions`、`Placer` 和框架 API 中。参数名必须匹配，布尔值、整数和枚举名称经过
类型转换后才调用 `handler(*values)`；没有装饰器绕过或第二次排队。

```json
{"action":"queued","id":"client-id:1"}
```

`queued` 只表示入队，界面仍显示“已发送，等待结果”。存在待完成请求时，网页以 100 毫秒
间隔调用 `poll()`；同一时间最多有一次结果轮询在途。首次连接也用这一机制，不能等到
`connected` 为真后才开始轮询。结果格式如下，`value` 为可 JSON 序列化的返回值：

```json
{"action":"results","results":[{"id":"client-id:1","kind":"action","name":"placeZombie","ok":true,"value":null}]}
```

执行异常保留请求 ID、kind 和 name，并返回 `ok: false`、`errortype` 和 `error`。
结果不会在 `poll()` 时删除，网页处理后通过 `acknowledge()` 确认，确认后不再主动回传；
因此轮询响应丢失时仍能重新领取。完成记录（包括已确认记录）保留 60 秒后清理，防止无人
领取的结果永久累积。在这段缓存期内，同一页面重复提交相同 ID 和内容只重新领取结果，
不会重复执行；同一 ID 携带不同内容会报错。页面重连不重放旧操作，也不在缓存过期后自动
重试原动作。

后端等待主线程执行超过 30 秒的请求以 `RequestExpired` 完成，不再执行游戏操作。前端每个
请求从提交开始最多等待 30 秒，超时后停止等待并发送 `cancel()`；尚未执行的请求会取消，
正在执行的游戏调用不能安全中断，只丢弃后续主动回包。因此前端超时不代表动作一定没有
执行，界面提示先确认游戏状态。排队等待引导的本地操作也有超时，过期后不会随连接成功
补发。初始连接失败或连接/心跳超时会清空其余等待操作；断线、会话被拒绝和 socket 错误
会清理相应计时器。正常退出时 `release` 清理未领取结果。

结果轮询响应等待 5 秒后可以重试，重试仅调用 `poll()`。网页在提交后就开始轮询，不依赖
`queued` 回包必达；重复或迟到的结果会确认但不再次更新界面。原始调试代码的异常没有请求
ID，只展示错误，不清空其他业务请求的等待状态。请求过期、取消和结果保留时间以及会话
租约均使用单调时钟计时。

队列使用一个普通 `threading.Lock`。网络线程交接请求、结果或确认信息时、主线程交换请求队列
或提交结果时短暂持锁；会话检查、参数转换、游戏调用和状态序列化期间均不持锁。

### 状态快照和选项应用

`SyncRegistry` 注册 `cheat`（`CheatOption`）、`placer`（`Placer`）和 `weather`
（`WeatherControl`）。`Serializable.to_dict()` 自动读取公开的简单实例属性和 `@property`，
不需要登记字段表。`from_dict()` 按现有属性逐项应用：简单属性直接赋值，.NET 枚举通过
`System.Enum.Parse()` 转换，不额外校验类型或范围。不存在、私有或不支持的属性会跳过；
枚举转换失败、属性只读或赋值时出现类型转换错误，也跳过该项并继续处理其余选项。
未知状态对象和非字典的对象数据同样忽略，不做整份请求预校验。

这些操作都在主线程完成，包括 `noCooldown` 对游戏字段的读写和脚本开关的启停。
会话校验保持不变；其他游戏运行时异常仍按请求 ID 回传。

`connect` 和 `snapshot` 请求的 `value` 是以下消息；连接模块据此更新界面：

```json
{
  "action": "sync",
  "modVersion": "1.15.1",
  "gameVersion": "1.3.4",
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

### 布阵码

`sendAction('getLineup')` 在主线程调用 `cheat_actions.GetLineup()`，返回布阵码字符串。
`sendAction('applyLineup', { code })` 调用 `cheat_actions.LineUpOnBoard(code)`。
前端不访问 `Board`，也不构造包含用户输入的 Python 表达式。

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

GUI 会将修改选项和放置器中的布尔开关保存到 `localStorage` 的 `pgvz-gui-checkbox-state` 项。下次打开时，PC 端先从 `localStorage` 恢复；没有已保存值的选项使用代码中的默认值。连接建立后，连接模块通过 `getInitialState()` 获取 `cheatOption` 和 `placer` 状态，并作为 `connect` 请求的 `state` 交给分发器，由主线程申请会话并恢复选项。因此即使游戏是刚启动的新进程，也会恢复上次网页中勾选的状态。

用户勾选复选框时，`watch(cheatOption)` 检测变化，通过 `setCheatOption(key, value)` 发送：

```javascript
applyState({ cheat: { [key]: value } });
```

### 手机端：拉取模式

手机浏览器可能被系统杀死后台页面，导致 GUI 内存状态丢失。手机端不读取或写入上述 `localStorage` 项，并始终将游戏内状态视为权威状态。网页不需要预先判断游戏进程是否运行：WebSocket 连接成功本身就表示游戏的 `/Py` 服务正在运行；连接建立后，GUI 通过不带 `state` 的 `connect` 请求拉取游戏内的完整状态。若游戏尚未运行，网页保持重连，直到连接成功后再同步。

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

### 3. 通信流程

```
用户勾选复选框
  → Vue watch 检测 cheatOption.xxx 变化
  → setCheatOption('xxx', true)
  → applyState({cheat: {xxx: true}})
  → PGvZProtocol.requestCode(clientId, id, "apply", {state}) 编码固定接口调用
  → WebSocket → IronPython 执行
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
