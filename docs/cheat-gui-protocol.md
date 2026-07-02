# 修改器通信协议

## 整体架构

```
浏览器 (gui/cheat-gui.html)
    ↕ HTTP (localhost:58080)
cheat-gui.py (内嵌服务器)
    ↕ WebSocket (localhost:8080/Py)
游戏 IronPython 引擎
    ↕ Python 对象
pgvztool 模块 (cheat_option, placer, ...)
```

## HTTP 服务器 (cheat-gui.py)

位于 `cheat-gui.py`，使用 Python 标准库 `http.server`。启动时自动挂在 `localhost:58080`，将所有请求路由到 `gui/` 目录下的文件。根路径 `/` 返回 `gui/cheat-gui.html`。

`Cache-Control: no-cache` 头确保浏览器每次刷新都拉取最新文件（防止手机端缓存不更新）。

## WebSocket 服务 (localhost:8080/Py)

由游戏内 `IronPyInteractive` 启动（IronPyInteractive.cs:199-219）。行为类似 **Python 交互式控制台（REPL）**：

- **表达式**（如 `1+1`、`get_cheat_state()`）：执行后返回 `repr()` 的字符串结果
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

## 应用层协议

基于 WebSocket 的 REPL 特性，定义了两类 JSON 消息，通过嵌套在 `repr()` 字符串中传递。

### sync（状态同步）

由 `pgvztool/sync_state.py:get_cheat_state()` 生成。将 `CheatOption` 所有属性及 `placer` 状态序列化。

**发送**（手机端连接后拉取，或 PC 端初始化后推送）：

```
get_cheat_state()
```

**返回**：

```json
{
  "action": "sync",
  "options": {
    "wontLose": false,
    "freePlant": false,
    "drawPlantHp": true,
    "autoCollect": true,
    "seedType": "Peashooter",
    "zombieType": "Normal",
    "easyPlaceMode": "plant",
    ...
  }
}
```

GUI 收到后遍历 `options` 的 key，更新 `cheatOption` 响应式对象及 placer 相关状态。

### lineup（布阵码）

由 `pgvz/lineup.py:LineUp.from_board(...).to_str()` 生成。

**发送**（点击"获取布阵码"按钮）：

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

GUI 将 `code` 填入布阵码输入框。

## 状态同步策略

### PC 端：推送模式

GUI 初始状态全为 `false`（除 `autoCollect` 和 `runBackground` 默认为 `true`）。用户勾选复选框时，`watch(cheatOption)` 检测变化，通过 `setCheatOption(key, value)` 发送赋值语句：

```javascript
send(`cheat_option.${key} = ${value ? 'True' : 'False'}`);
```

这是变量赋值，WebSocket 返回 `{"statuscode": 0}`（无 result）。游戏端 `CheatOption` 实例的属性被直接赋值，hook 函数在下一帧读取新值。

### 手机端：拉取模式

手机浏览器可能被系统杀死后台页面，导致 GUI 状态丢失。连接建立后，先发 `get_cheat_state()` 拉取当前游戏内的完整状态，通过 `sync` 消息同步回来。

## 如何新增一个修改选项

### 1. Python 端：定义状态 (pgvztool/cheat.py)

在 `CheatOption.__init__` 中添加属性：

```python
self.xxx = False
```

如果新选项不是简单的布尔开关，可能需要额外的辅助函数或脚本单例。参考已有的 `infSun`（脚本单例 + `On/Off`）或 `noCooldown`（直接设置游戏内部变量）。如果是简单的钩子，钩子函数放在 `pgvztool/hook.py`。

### 2. Python 端：注册同步 (pgvztool/sync_state.py)

在 `regular_attrs` 列表中添加字符串 `'xxx'`。这确保手机端拉取状态时包含该选项。

如果新选项不是 `CheatOption` 的简单属性（如 `autoCollect` 对应 `auto_collector.enabled`），需要在 `get_cheat_state()` 中单独处理。

### 3. GUI 端：注册选项 (gui/cheat-gui.html)

**a)** 在 `optionConfig` 数组末尾添加 `'xxx'`。`reactive()` 初始化时会自动为该键创建响应式属性（默认 `false`）。

**b)** 在对应分类的 `<el-card>` 中添加复选框：

```html
<el-checkbox v-model="cheatOption.xxx">显示标签</el-checkbox>
```

**c)** 如果该选项不走默认的 `setCheatOption`（即不是直接赋值 `cheat_option.xxx = True/False`），需要在 `setCheatOption` 的 switch 中添加对应分支。

### 4. 通信流程（默认分支）

```
用户勾选复选框
  → Vue watch 检测 cheatOption.xxx 变化
  → setCheatOption('xxx', true)
  → default 分支: send("cheat_option.xxx = True")
  → WebSocket → 游戏 IronPython
  → cheat_option.xxx = True
  → 下一帧 hook 函数读取 cheat_option.xxx，执行对应逻辑
```

### 特殊分支

部分选项不走默认路径：

| 选项 | 发送内容 | 原因 |
|---|---|---|
| `autoCollect` | `auto_collector.On()/Off()` | 控制脚本单例的启用/停用 |
| `infSun` | `script_inf_sun.On()/Off()` | 同上 |
| `skillNoCooling` | `script_skill_nocooling.On()/Off()` | 同上 |
| `noCooldown` | `gLawnApp.mEasyPlantingCheat = True/False` | 直接设置游戏内部字段 |

## 轻松放置的状态同步

`placer` 对象的状态也需要同步（`seedType`、`zombieType`、`easyPlaceMode` 等）。这些在 `syncCheatOptions()` 中单独发送，不走 `setCheatOption`。`get_cheat_state()` 中也单独序列化 `placer` 的字段。
