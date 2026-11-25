# 内置作弊菜单

依据本地 `PGvZ-decompilation-1.4.3` 静态核对。本文以 `ZBCheatDialog` 构造函数实际加入面板的控件为范围。

本文记录游戏原生行为。加载 PGvZ-TAS 后，其中三个复选框接入同一套修改器状态，见[内置作弊菜单同步](../../mod/internals/cheat-gui-protocol.md#内置作弊菜单同步)。

选项里的作弊菜单开关由 `NewOptionsDialog.CheckboxChecked(12)` 处理。打开时创建 `ZBCheatDialog`，初始缩成屏幕左侧的悬浮 `+`；点击可展开，拖动可挪位置。展开后底部的 `+`、`−` 每次调整面板高度 100，最小化按钮将面板缩回悬浮 `+`。在选项里关闭菜单会移除并释放面板，已生效的钩子、设置与全局速度仍保留。

## 自动收集资源

通过 `DynamicHookGen.On.Lawn.Coin.Update` 挂钩每个掉落物的更新。先执行原方法，再检查掉落物是否属于某个 `Board`、类型是否在收集名单内、是否尚未进入收集状态。满足条件就调用 `PlayCollectSound()` 和 `Collect()`，走游戏原有的收集动画、入账或物品领取流程。名单包括四种阳光（`Sun`、`Smallsun`、`Largesun`、`Tinysun`）、银币、金币、钻石、植物礼盒和巧克力。冒险首周目第 1 关还会更新收集提示。

切换时同步写入 `PlayerInfo.mCoinAutoCollect` 并保存玩家配置。加载玩家资料时，由 `LawnApp.mPlayerInfo` 的 setter 恢复开关和钩子。

## 无冷却种植

打开时先调用当前卡槽的 `SeedBank.RefreshAllPackets()`，刷新正在冷却的卡片。随后挂钩 `SeedPacket.WasPlanted()` 和 `SeedPacket.SetPacketType()`，覆盖用卡后的冷却与设置卡种时的初始冷却。两处钩子都先运行原逻辑，再对原逻辑标为 `mRefreshing` 的卡片调用 `Activate()`。

`Activate()` 只将 `mActive` 设为 `true`。卡片可立即使用，即使 `mRefreshing` 仍为真。`CanPickUp()` 仍检查阳光和种植要求，落地流程仍按玩法扣费。传送带用卡后移除卡片的逻辑也照常执行。

勾选状态切换的是 `EnableNoCoolDownPlanting`，但菜单每次新建时用 `mApp.mEasyPlantingCheat` 初始化这个复选框。重新创建菜单后，勾选显示可能与实际钩子状态不同。

PGvZ-TAS 的同名选项 `CheatOption.noCooldown` 直接读写 `mEasyPlantingCheat`。原生 `SeedPacket.MouseDown()` 和 `CanPickUp()` 据此跳过卡片激活、阳光和升级前置检查，点击卡片时也会跳过辣椒封印检查。普通卡槽放置和“我是僵尸”放置流程会跳过扣费。`Board.CanPlantAt()` 会放宽空格的升级植物限制，玉米炮仍须通过两格位置检查。

两个开关打开时，普通卡片都可以跳过等待，实际卡片状态不同。内置菜单开启时会将已经在冷却的卡片刷新为可用，关掉开关后这些卡片仍可用。PGvZ-TAS 只绕过检查，原生更新仍会推进冷却。若在冷却尚未结束时关掉 PGvZ-TAS 开关，卡片会继续等待剩余时间。想保留原生扣费和升级限制，同时实际刷新卡片，可使用内置开关。

## 房主无敌

用钩子替换 `Board.ZombiesWon(Zombie)`。若有触发判负的僵尸，就对该僵尸调用 `DieNoLoot(giveAchievements: false)`。普通僵尸越过左边界时因此会死亡，玩家不会进入原生失败流程。植物、房屋相关对象和其他单位的生命值照常处理。

该钩子也拦截没有具体僵尸的 `ZombiesWon(null)` 调用。例如僵尸水族馆僵尸耗尽或玉米轮盘达到失败条件时，这次判负会被跳过，调用前已经发生的玩法状态变化仍然有效。

## 后台运行

修改 `Main.RunWhenLocked`。窗口失活时，`Main.Update()` 仍可调用 `UpdateApp()`，`LawnApp.LostFocus()` 也会跳过自动打开暂停对话框。输入仍只在窗口激活时处理，失焦时仍会暂停音乐或静音。该开关能覆盖游戏自己的失焦检查，实际运行仍取决于系统是否继续调度游戏更新。

切换时同步写入 `PlayerInfo.mRunWhileLocked` 并保存玩家配置，加载玩家资料时恢复。

## 速度控制

`ChangeGameSpeed()` 写入全局的 `gFastMo`、`gSlowMo` 和 `gFastSlowMoNum`，并更新面板文字。[`LawnApp.UpdateFrames()` 的速度控制](speed-control.md)会在慢速档按计数器跳过部分应用更新。

原生速度标签在面板构造和 `ChangeGameSpeed()` 中使用 `GetGameSpeedString()` 生成文字。原生 `Update()` 不刷新这个标签。

| 按钮 | 实现 |
| --- | --- |
| `0.25x` | 打开 `gSlowMo`，分频值设为 4，每 4 次外层更新执行 1 次应用更新。 |
| `0.5x` | 打开 `gSlowMo`，分频值设为 2，每 2 次外层更新执行 1 次应用更新。 |
| `1x` | 关闭两个全局快慢速标志并把 `gFastSlowMoNum` 置 0，恢复每次外层更新执行 1 次应用更新。 |

## 跳关功能

允许跳关时，圆形按钮切换 `EnableSkipLevel`，开启后才显示并启用“直接过关”。`LawnApp.PreNewGame()` 在设置游戏模式后检查资格。冒险仅限首次通关前，内置五种无尽生存、禅境花园、智慧树、无尽砸罐子、无尽我是僵尸、试玩引导模式 `Upsell`、巨人之怒 1–3 和奇人异尸 1 禁用；判定为禁用时也会关闭 `EnableSkipLevel`。

点击“直接过关”时，若当前有 `Board`，生存玩法先将 `Challenge.mSurvivalStage` 写成 5（轮次从 0 编号）。然后调用 `RemoveAllZombies()` 清理仍活着的僵尸，调用 `FadeOutLevel()` 进入原生结算，最后把 `mBoardFadeOutCounter` 设为 200。正常淡出路径倒计时归零时设置 `mLevelComplete`，随后由 `LawnApp.CheckForGameEnd()` 处理进度和场景切换。

固定轮次 5 依赖原生终轮判断。创意有限生存只有 `mSurvivalStage == mStages - 1` 才算终轮，创意无尽生存始终没有终轮；在允许点“直接过关”的相应创意生存中，仍可能走到换轮流程。

## 放大模式

按钮仅在 `Board.CanSelectGridFocus` 允许时可用。点击后全局速度恢复为 1×，调用 `Board.SelectGridFocus()` 进入放大镜选格状态，最小化菜单并把焦点交回关卡。点中有效格子后，镜头以该格中心平滑放大，放大和恢复期间隐藏悬浮菜单。再次点击或按 Esc／返回恢复原相机位置与缩放，全局速度保持 1×。详见[草坪格子放大模式](grid-focus.md)。

## 反编译源码导航

| 路径 | 入口 |
| --- | --- |
| `Lawn/NewOptionsDialog.cs` | `CheckboxChecked(12)` 创建或移除悬浮菜单。 |
| `Lawn/ZBCheatDialog.cs` | 构造函数、`CheckboxChecked()`、`ButtonDepress()`、`DoCheckGameModeCanSkipLevel()`。 |
| `Lawn/Coin.cs`、`Lawn/SeedPacket.cs`、`Lawn/SeedBank.cs` | 收集路径、卡片状态、卡槽刷新。 |
| `Lawn/Board.cs`、`Lawn/Challenge.cs`、`Lawn/Zombie.cs` | 判负入口及其调用点、结算、镜头聚焦。 |
| `Lawn/LawnApp.cs`、`Sexy/Main.cs` | 玩家配置恢复、全局更新、失焦、关卡结算。 |
