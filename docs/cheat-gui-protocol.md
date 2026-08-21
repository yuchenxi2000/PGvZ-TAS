# 修改器通信协议

## 整体架构

```
浏览器 (gui/index.html + gui/js/)
    ├─ HTTP (localhost:58080) ─────→ cheat-gui.py ─→ gui/ 静态文件
    └─ WebSocket (localhost:8080/Py) → 游戏 IronPython 引擎
                                              ↕ Python 对象
                                    pgvztool/sync.py (SyncRegistry)
                                              ↕ Serializable
                                    cheat_option、placer 等对象
```

## HTTP 服务器 (cheat-gui.py)

位于 `cheat-gui.py`，使用 Python 标准库 `http.server`。启动时自动挂在 `localhost:58080`，将所有请求路由到 `gui/` 目录下的文件。根路径 `/` 返回 `gui/index.html`。

游戏启动时只自动扫描 `mods/` 顶层的 `.py` 文件，因此此时执行的是 `cheat-gui.py`，它只配置模块搜索路径并启动 HTTP 服务。`pgvz/` 和 `pgvztool/` 是 Python 包，不会被游戏自动扫描；网页建立 WebSocket 连接并确认游戏同步初始化完成后，`gui/js/protocol.js` 中的 `BOOTSTRAP_CODE` 才会导入它们并注册相关钩子。

`Cache-Control: no-store, no-cache, must-revalidate` 等响应头用于防止之后的页面加载复用缓存。它不能停止已经在页面内存中运行的旧 JavaScript、重连定时器或 WebSocket；通过 `file://` 直接打开文件时也不存在这些 HTTP 响应头。仍在运行的旧页面由下述 GUI 会话协议拦截。

## WebSocket 服务 (localhost:8080/Py)

由游戏内 `IronPyInteractive` 启动（IronPyInteractive.cs:199-219）。行为类似 **Python 交互式控制台（REPL）**：

- **表达式**（如 `1+1`、`sync_reg.serialize()`）：执行后返回 `repr()` 的字符串结果
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

### JSON 引号问题

JSON 布尔值（`true`/`false`）不是有效的 Python 语法。从 Web 端发送 JSON 数据给 `json.loads()` 解析时，必须将 JSON 字符串整体包裹为 Python 字符串字面量（单引号）：

```javascript
// ✅ 正确：JSON 作为 Python 字符串传入
send(`sync_reg.apply('${JSON.stringify(obj)}')`);

// ❌ 错误：JSON 直接作为 Python 代码，true/false 会触发 UnboundNameException
send(`sync_reg.apply(${JSON.stringify(obj)})`);
```

反之，WebSocket 返回的 `result` 字段是 `repr()` 输出，字符串会被额外包裹一层引号。GUI 解析前需去掉外层引号：

```javascript
let r = data.result;
if ((r.startsWith("'") && r.endsWith("'")) || (r.startsWith('"') && r.endsWith('"'))) {
    r = r.slice(1, -1);
}
const msg = JSON.parse(r);
```

## 应用层协议

### GUI 单客户端会话

官方 GUI 的每个页面实例会生成唯一 `_clientId`，连接后通过 `sync_reg.connect(...)` 申请会话。`SyncRegistry` 只允许一个活动页面，页面每 3 秒调用 `sync_reg.heartbeat(...)` 续租；正常关闭时调用 `sync_reg.release(...)`，异常消失的租约会在 15 秒后过期。

后打开的页面收到 `sessionRejected` 后显示“另一个修改器页面已连接”，不再自动重连抢占。其后用户点击控件时仍会得到相同提示。官方 GUI 发出的每条正常指令前还会调用 `sync_reg.require_client(...)`，在 IronPython 端再次校验会话所有权。

这是 `pgvztool` 的应用层保护，不是 `/Py` WebSocket 服务的安全边界；直接发送未包装 Python 的第三方客户端不受此限制。

### sync（状态同步）

由 `sync_reg.serialize()` 生成。`sync_reg` 是 `SyncRegistry` 实例，注册了 `cheat`（`CheatOption`）和 `placer`（`Placer`）两个对象。序列化通过 `Serializable.to_dict()` 自动完成——包括简单属性和脚本单例的 `@property`。

**发送**（手机端连接并申请 GUI 会话，同时拉取状态）：

```
sync_reg.connect('<clientId>')
```

**返回**：

```json
{
  "action": "sync",
  "state": {
    "cheat": {
      "wontLose": false,
      "freePlant": false,
      "drawPlantHp": true,
      "autoCollect": true,
      "infSun": false,
      "skillNoCooling": false,
      "noCooldown": false,
      "autoRestock": false,
      "mushroomAwake": false,
      ...
    },
    "placer": {
      "seedType": "Peashooter",
      "zombieType": "Normal",
      "easyPlaceMode": "plant",
      "easyPlaceEnabled": true,
      ...
    }
  }
}
```

GUI 收到后分别遍历 `cheat` 和 `placer` 对象更新状态。

### apply（Web → Python 控制）

正常连接后的状态修改统一走 `sync_reg.apply(json_str)`；PC 端的初始完整状态作为 `sync_reg.connect(...)` 的第二个参数传入，由 `connect()` 在取得会话后调用 `apply()`：

**单个复选框切换**：

```javascript
send(`sync_reg.apply('${JSON.stringify({_clientId: clientId, cheat: {[key]: value}})}')`);
```

**PC 端连接时同步全部状态**：

```javascript
const state = JSON.stringify({
  _clientId: clientId,          // 每个页面实例生成的唯一 ID
  cheat: cheatOption,           // Vue reactive 对象
  placer: { seedType: ..., ... }
});
send(`sync_reg.connect('${clientId}', '${state}')`, true);
```

Python 端 `SyncRegistry.apply()` 解析 JSON 后，遍历各对象调用 `Serializable.from_dict()`。`from_dict` 通过 `setattr` 写入——普通属性直接赋值，有 setter 的 `@property` 自动走 setter（如 `cheat_option.autoCollect = True` 会调用 `auto_collector.On()`）。

官方 GUI 的每次 `apply()` 都携带 `_clientId`。存在活动会话时，后端会拒绝客户端 ID 不匹配或缺失的任何修改；即使当前没有活动会话，也会额外拒绝不带 `_clientId`、且同时包含 `cheat` 和 `placer` 的旧版完整同步，防止残留旧页面在游戏重连后用默认值覆盖状态。

### lineup（布阵码）

由 `pgvz/lineup.py:LineUp.from_board(...).to_str()` 生成。

**发送**：

```
'{"action":"lineup","code":"' + pgvz.lineup.LineUp.from_board(board).to_str() + '"}'
```

**返回**：

```json
{
  "action": "lineup",
  "code": "base64-encoded-lineup-string"
}
```

## 状态同步策略

### PC 端：推送模式

GUI 会将修改选项和放置器中的布尔开关保存到 `localStorage` 的 `pgvz-gui-checkbox-state` 项。下次打开时，PC 端先从 `localStorage` 恢复；没有已保存值的选项使用代码中的默认值。连接建立后，`syncCheatOptions()` 将页面实例的 `_clientId`、当前 `cheatOption`（Vue reactive 对象）和 `placer` 状态传给 `sync_reg.connect(...)`，在申请 GUI 会话的同时写入游戏。因此即使游戏是刚启动的新进程，也会恢复上次网页中勾选的状态。

用户勾选复选框时，`watch(cheatOption)` 检测变化，通过 `setCheatOption(key, value)` 发送：

```javascript
send(`sync_reg.apply('${JSON.stringify({_clientId: clientId, cheat: {[key]: value}})}')`);
```

### 手机端：拉取模式

手机浏览器可能被系统杀死后台页面，导致 GUI 内存状态丢失。手机端不读取或写入上述 `localStorage` 项，并始终将游戏内状态视为权威状态。网页不需要预先判断游戏进程是否运行：WebSocket 连接成功本身就表示游戏的 `/Py` 服务正在运行；连接建立后，GUI 通过 `sync_reg.connect(clientId)` 拉取当前游戏内的完整状态。若游戏尚未运行，网页保持重连，直到连接成功后再同步。

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

`Serializable.to_dict()` 会自动发现 `@property` 并包含在序列化中。

### 2. GUI 端：注册选项

在 `gui/js/app.js` 的对应 `switchGroups` 分组中添加 `'xxx'`。`optionConfig` 会自动从所有分组生成，`CheckGroupCard` 也会自动创建复选框，因此不需要再手写一份控件。随后在 `gui/js/i18n.js` 的中英文 `options` 中分别添加显示名称。

### 3. 通信流程

```
用户勾选复选框
  → Vue watch 检测 cheatOption.xxx 变化
  → setCheatOption('xxx', true)
  → send("sync_reg.apply('" + JSON.stringify({_clientId: clientId, cheat: {xxx: true}}) + "')")
  → WebSocket → IronPython 执行
  → sync_reg.apply('{"_clientId":"...","cheat":{"xxx":true}}')
  → json.loads → obj.from_dict → setattr(cheat_option, 'xxx', True)
  → 下一帧 hook 函数读取 cheat_option.xxx，执行对应逻辑
```
