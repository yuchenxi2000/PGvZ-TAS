# 修改器通信协议

## 整体架构

```
浏览器 (gui/cheat-gui.html)
    ↕ HTTP (localhost:58080)
cheat-gui.py (内嵌服务器)
    ↕ WebSocket (localhost:8080/Py)
游戏 IronPython 引擎
    ↕ Python 对象
pgvztool/sync.py (SyncRegistry)
    ↕ Serializable
pgvztool 模块 (cheat_option, placer, ...)
```

## HTTP 服务器 (cheat-gui.py)

位于 `cheat-gui.py`，使用 Python 标准库 `http.server`。启动时自动挂在 `localhost:58080`，将所有请求路由到 `gui/` 目录下的文件。根路径 `/` 返回 `gui/cheat-gui.html`。

`Cache-Control: no-cache` 头确保浏览器每次刷新都拉取最新文件（防止手机端缓存不更新）。

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

### sync（状态同步）

由 `sync_reg.serialize()` 生成。`sync_reg` 是 `SyncRegistry` 实例，注册了 `cheat`（`CheatOption`）和 `placer`（`Placer`）两个对象。序列化通过 `Serializable.to_dict()` 自动完成——包括简单属性和脚本单例的 `@property`。

**发送**（手机端连接后拉取）：

```
sync_reg.serialize()
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

所有状态的修改统一走 `sync_reg.apply(json_str)`：

**单个复选框切换**：

```javascript
send(`sync_reg.apply('${JSON.stringify({cheat: {[key]: value}})}')`);
```

**初始化同步全部状态**：

```javascript
send(`sync_reg.apply('${JSON.stringify({
  cheat: cheatOption,           // Vue reactive 对象
  placer: { seedType: ..., ... }
})}')`);
```

Python 端 `SyncRegistry.apply()` 解析 JSON 后，遍历各对象调用 `Serializable.from_dict()`。`from_dict` 通过 `setattr` 写入——普通属性直接赋值，有 setter 的 `@property` 自动走 setter（如 `cheat_option.autoCollect = True` 会调用 `auto_collector.On()`）。

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

GUI 初始状态全为 `false`（除 `autoCollect` 和 `runBackground` 默认为 `true`）。连接建立后，`syncCheatOptions()` 将当前 `cheatOption`（Vue reactive 对象）和 `placer` 状态合并为一次 `sync_reg.apply(...)` 发送。

用户勾选复选框时，`watch(cheatOption)` 检测变化，通过 `setCheatOption(key, value)` 发送：

```javascript
send(`sync_reg.apply('${JSON.stringify({cheat: {[key]: value}})}')`);
```

### 手机端：拉取模式

手机浏览器可能被系统杀死后台页面，导致 GUI 状态丢失。连接建立后，先发 `sync_reg.serialize()` 拉取当前游戏内的完整状态，通过返回的 `sync` 消息同步回来。

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

### 2. GUI 端：注册选项 (gui/cheat-gui.html)

在 `optionConfig` 数组末尾添加 `'xxx'`，在对应 `<el-card>` 中添加 `<el-checkbox>`。

### 3. 通信流程

```
用户勾选复选框
  → Vue watch 检测 cheatOption.xxx 变化
  → setCheatOption('xxx', true)
  → send("sync_reg.apply('" + JSON.stringify({cheat: {xxx: true}}) + "')")
  → WebSocket → IronPython 执行
  → sync_reg.apply('{"cheat":{"xxx":true}}')
  → json.loads → obj.from_dict → setattr(cheat_option, 'xxx', True)
  → 下一帧 hook 函数读取 cheat_option.xxx，执行对应逻辑
```
