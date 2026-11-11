# 传送门移动机制

本文依据当前支持的 PGvZ 1.3.0、1.3.1 反编译代码，记录传送门自动移动的两条路径，以及修改器“传送门不移动”的实现。

## 原生倒计时

- 传送门战斗 `GameMode.ChallengePortalCombat` 在 `Challenge.PortalStart()` 放置四个传送门。`Challenge.UpdatePortalCombat()` 每次更新将 `mChallengeStateCounter` 减一；减到 `500` 时提示，减到 `0` 或以下时调用 `MoveAPortal()`，然后重置为 `6000`。
- 含 `CSSpawnPortal` 的自定义关卡会在 `Challenge.Init()` 放置组件列出的传送门，初始 `mRandomPortalCounter` 为 `RandomPortalTime * 3 / 2`。当 `RandomPortalTime >= 0` 时，`Challenge.Update()` 每次减一，减到 `0` 或以下时调用 `MoveAPortal()` 并按组件值重置倒计时。负数本来就不会自动移动。
- `MoveAPortal()` 从现有传送门中随机选一个，关闭原位置，并在新位置开启同类型传送门。它最多按四个传送门分配数组。

## 修改器实现

`ScriptFreezePortal` 是默认暂停的 `FOREVER` 逐帧脚本，由 `cheat_option.freezePortal` 开关控制。框架在原生 `Board.UpdateGame()` 之前推进脚本，因此每帧把传送门战斗倒计时恢复到 `6000`，或把自定义关卡的随机移动倒计时恢复到至少 `2`，随后原生更新只会减一而不会进入移动分支。关闭选项后，游戏从当前倒计时继续运行；退出并重新进入关卡时，脚本按同一个开关继续生效。

自定义关卡若设置 `RandomPortalTime` 为 `0` 或 `1`，直接回填组件值仍会在同一帧触发移动，因此必须至少回填 `2`。这个开关只抑制游戏自动移动；玩家用放置器主动移动传送门不受影响。

## 反编译源码导航

| 文件 | 重点 |
|---|---|
| `Lawn/Challenge.cs` | `Init`、`Update`、`PortalStart`、`UpdatePortalCombat`、`MoveAPortal` |
| `Lawn.Creative/CSSpawnPortal.cs` | `Portals` 与 `RandomPortalTime` 解析、校验 |
