# 键盘彩蛋口令

本文依据本地 PGvZ 1.4.3 反编译源码静态核对。

在主菜单或关卡内依次按下对应的字母键即可匹配口令，无需按回车。选卡界面也会把按键交给关卡的判定逻辑。`TypingCheck` 在 `KeyDown` 中比较最近的键码，匹配成功后清空该口令的记录。再次输入口令会切换对应模式。

| 口令 | 智慧树高度要求 | 开启后的效果 |
| --- | ---: | --- |
| `daisies` | ≥ 100 | 符合条件的僵尸倒地时出现雏菊。水路和屋顶不会生成雏菊。 |
| `dance` | ≥ 500 | 普通、路障和铁桶僵尸行走时使用跳舞动画。泳池里可用的游泳动画优先。 |
| `pinata` | ≥ 1000 | 符合条件的僵尸掉头时产生皮纳塔粒子特效。割草机碾过的僵尸跳过该特效。 |
| `mustache`、`moustache` | 无 | 给支持该动画图层的僵尸加上胡子。 |
| `trickedout` | 无 | 普通草坪割草机显示改装外观。 |
| `future` | 无 | 给支持该贴图的僵尸戴上墨镜。 |
| `sukhbir` | 无 | 关卡内会切换 `mSukhbirMode`。该版本的玩法和音效逻辑没有读取此状态，主菜单也未检查该口令。 |

智慧树高度取自 `mPlayerInfo.mChallengeRecords[48]`。匹配前三个口令时，如果高度不足或没有玩家档案，游戏会播放失败蜂鸣声。关卡处于 `Playing` 场景时还会显示 `[CANT_USE_CODE]` 提示。主菜单切换的是 `LawnApp` 的模式字段，新建关卡时 `Board` 会读取这些字段。

源码还注册了带空格的 `tricked out`。`TypingCheck.AddChar()` 把其中的空格映射为 `KeyCode.Unknown`（0），而空格键传入 `KeyCode.Space`（32），所以用普通键盘应输入 `trickedout`。主菜单和关卡还识别 `↑ ↑ ↓ ↓ ← → ← → B A`，匹配后播放 `FoleyType.Drop`。

## 修改器入口

网页“关卡与显示”的“彩蛋”卡片可直接切换六种效果。雏菊、跳舞和糖果无需达到智慧树高度。关卡内调用原生 `Board.Set*Mode()`，主菜单直接设置新关卡会读取的 `LawnApp` 模式。关闭割草机外观时，修改器还将现有普通草坪割草机的动画恢复为 `anim_normal`，因为原生 `EnableSuperMower(false)` 仍会设置 `anim_tricked`。

六个开关同时影响当前关卡和此游戏进程中新建的关卡。修改器加载后，继续旧存档或 TAS 读档会在原生读取成功后，将当前 `cheat_option` 中的全局彩蛋设置应用到该局。主菜单和关卡里的键盘口令通过游戏原生的 `LawnApp` 字段同步更新 `cheat_option`，已连接的网页也会同步刷新彩蛋开关。

点击 `↑ ↑ ↓ ↓ ← → ← → B A` 按钮会调用与原生口令相同的 `LawnApp.PlayFoley(FoleyType.Drop)`。该 Foley 映射到 `SOUND_TAP2`，1.4.3 安装目录的资源是 `Content/sounds/tap2.xnb`，时长约 0.53 秒，取消手持卡片时也会用到。`mMuteSoundsForCutscene` 开启时，`LawnApp.PlayFoley()` 会跳过播放。

## 反编译源码导航

以下路径相对于同级 `PGvZ-decompilation-1.4.3` 目录。

| 文件 | 相关逻辑 |
| --- | --- |
| `Lawn/LawnApp.cs` | 1820–1839 行注册按键序列，`CanDoDaisyMode()`、`CanDoDanceMode()`、`CanDoPinataMode()` 检查门槛。 |
| `Lawn/Challenge.cs` | `TreeOfWisdomGetSize()` 和 `TreeOfWisdomGrow()` 读取和增加智慧树高度。 |
| `Lawn/Board.cs`、`Lawn/GameSelector.cs` | `Board.DoTypingCheck()` 及 `GameSelector.KeyDown()` 分别处理关卡和主菜单口令。 |
| `Lawn/TypingCheck.cs`、`Sexy/KeyCodes.cs` | 按键序列匹配与字符到键码的映射。 |
| `Sexy.TodLib/TodFoley.cs` | `FoleyType.Drop` 到 `SOUND_TAP2` 的映射。 |
| `Lawn/Zombie.cs`、`Lawn/LawnMower.cs` | 雏菊、跳舞、皮纳塔、胡子、墨镜和割草机的表现。 |
