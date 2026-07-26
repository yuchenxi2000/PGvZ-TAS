# 安装与故障排查

## 安装

### PC

1. 将 `pgvz/`、`pgvztool/`、`gui/`、`cheat-gui.py` 复制到 mods 目录（位置见下方），或者直接运行 `cp-cheat-mods.bat` 自动完成安装
2. 启动游戏，浏览器打开 `http://localhost:58080`

### 安卓

1. 将所有文件（`pgvz/`、`pgvztool/`、`gui/`、`cheat-gui.py`）复制到 mods 目录（位置见下方）
2. 启动游戏，浏览器打开 `http://localhost:58080`

### mods 目录位置

| 平台 | 路径 |
|---|---|
| PC | `C:\Users\{用户名}\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods` |
| 安卓 | `/storage/emulated/0/Android/data/net.pvz.pgvz.zbcteam/files/mods` |

## 修改器使用

1. **放置植物/僵尸/物品**：先在网页中选择类型和属性，再点击对应按钮放置
2. **轻松放置**：先开启轻松放置；然后和上步相同，选择放置类型，接着轻松放置模式选择要放的是植物/僵尸/其他；最后在游戏内点击玉米饼（Taco）图标（在铲子右边），左键进行放置（可连续放置），右键退出轻松放置模式，手机端重新点击该图标退出轻松放置。选择传送门模式可移动传送门位置
3. **TAS 工具**：勾选"启用 TAS"，右下角出现 Save/Undo/Redo/Adv 四个按钮和帧计数器，详见 [tas.md](tas.md)
4. **自定义快捷键**：在 `user_config.json` 同级目录新建 `keybinds.txt`，详见 [keybinds.md](keybinds.md)

## 故障排查

### 启动黑屏闪退（仅安卓）

安卓系统对应用启动有时间限制。游戏在初始化阶段会逐个加载 `mods/` 目录下所有 `.py` 文件，每个文件作为模组被编译并执行，这个过程在主线程进行。**本修改器只有 `cheat-gui.py` 一个 `.py` 文件，不会导致闪退。** 如果还安装了其他模组（`.py` 脚本），文件数量过多，总加载时间超过系统允许的上限，游戏会被强制杀死。

**解决方法**：删除其他模组的 `.py` 文件。`pgvz/`、`pgvztool/`、`gui/` 是文件夹形式，不会被主线程自动扫描加载，保留即可。Windows 没有这个超时限制。

### 网页打不开

- 确认游戏正在运行，且安装后已重启过游戏
- 确认浏览器地址输入的是 `http://localhost:58080`（注意是 http 不是 https）
- **检查模组是否启用**：打开 `user_config.json`（和 mods 目录同级），确保 `ironpython_enabled` 为 `true`
- **安卓文件损坏**：部分安卓文件管理器在解压或复制时可能损坏文件，尝试重新复制或换一个文件管理器

### 网页能打开但显示连接失败/一直转圈

- **关闭防火墙**，防火墙可能拦截 localhost 的 8080 端口
- **8080 端口被占用**：尝试访问 `http://localhost:58080/?ws=ws://localhost:8081/Py`，如不行则依次尝试 8082、8083，直到连接成功。游戏自带 WebSocket 服务的逻辑是：从 8080 开始尝试监听，如端口被占用则端口号 +1 重试，直到成功。
