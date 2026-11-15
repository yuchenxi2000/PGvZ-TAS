# 玉米轮盘（CornRoulette）

本文依据本地 `PGvZ-decompilation-1.4.3` 反编译源码静态核对，未在游戏中实测。

## 入口与开放状态

`GameMode.CornRoulette = 151`、`CornRouletteEndless = 152` 分别表示普通版和无尽版。
`ChallengeScreen.gChallengeDefs` 将两者登记在 `ChallengePage.Extra`，但
`ChallengeScreen.UpdateButtons()` 对模式编号 151、152 强制隐藏关卡按钮。
因此，这份 1.4.3 包中已有游戏逻辑，但正常菜单尚未开放入口。

修改器的“关卡修改”提供这两个模式的直接进入入口。四种轮盘专用道具不放入通用
“植物类型”：用户在 1.4.3 中实测使用这些通用卡片入口会崩溃，因此已撤回该入口。
轮盘模式仍由原生流程发放和使用道具。寒冰菇复用已有类型。

它是一种玉米投手版的轮盘对决：玩家与僵尸共享一袋玉米粒、黄油，轮流选择对自己
或对方发射；玉米粒相当于空弹，黄油相当于实弹。此处“空弹”指不扣除轮盘生命，
不代表子弹不执行原有碰撞。对决双方的僵尸模型会在更新中恢复本体血量，胜负由
场上的脑子和墓碑决定。

## 对局与弹药

- 玩家生命以 `IzombieBrain` 表示，僵尸生命以墓碑表示。
- 第一局双方各 2 点生命，每袋 3–4 发，无初始道具；后续局双方各 5 点生命，
  每袋 8–11 发，并重新随机分配双方的 8 个道具槽。
- 对一袋总数 `N`，黄油数从 `max(N / 4, 1)` 到 `floor(N / 2)` 之间随机选择，
  其余为玉米粒；这里的除法是整数除法。
- 装袋时短暂展示袋中玉米粒和黄油数量。下一发按袋内剩余数量随机抽取，
  并非预先保存一个完整发射顺序；每发用掉后从袋中移除，耗尽后自动装新袋。
- 黄油扣 1 点生命，施肥后扣 2 点。玩家受伤时会从墓碑生成僵尸吃脑子；
  僵尸受伤时掉落噬碑藤卡，玩家用卡吃掉墓碑完成伤害结算。
- 玉米粒打自己时保持当前行动方；打对方或发射黄油后通常交换行动方。
- 普通版先赢 2 局通关；两种模式均在累计输 2 局后失败。
  无尽版取消“赢 2 局通关”，不是输局次数无限，也不是连续输 2 局才失败。

实现借用 `mSurvivalStage` 记录已结束局数、`mChallengeScore` 记录胜局数，
所以 `mSurvivalStage - mChallengeScore` 是累计败局数。

## 道具

双方各占 4 个槽：`mSeedBank.mSeedPackets[0..3]` 属于玩家，`[4..7]` 属于 AI。
道具池有 5 种，其中寒冰菇复用已有 `SeedType`，另外 4 种为轮盘专用类型。

| 道具 | 效果 |
|---|---|
| 寒冰菇 `Iceshroom` | 对方下一次本应获得行动权时触发，阻止这次换手；同一方不能叠放。 |
| 巧克力 `CornRouletteChocolate` | 恢复 1 点生命，最多 6 点。 |
| 肥料 `CornRouletteFertilizer` | 下一次黄油伤害变为 2；发射玉米粒不会消耗强化，不能叠加。 |
| 放大镜 `CornRouletteMagnifier` | 查看当前下一发是玉米粒还是黄油；本次选择射击后清除。 |
| 水壶 `CornRouletteWatercan` | 丢弃当前下一发，再抽下一发；不交换行动权，袋空则重新装袋。 |

第一局之后，从僵尸行动转回玩家行动时，双方各尝试补充 2 个随机道具，
只填空槽，满槽不覆盖。连续行动本身不一定触发补充。

## AI 与方法分工

AI 会统计剩余弹药、双方生命和道具，判断必定实弹／空弹、斩杀、治疗、强化、
冻结、验弹、退弹等情形。`mShowBowlingLine` 在这里复用为放大镜验弹标记；
AI 的确定弹种判断会检查该标记或剩余弹药组成，并非每次都直接按隐藏弹种决策。

| 方法组 | 职责 |
|---|---|
| `Start`、`RoundSetup` | 创建双方代表、生命标记，初始化每局。 |
| `LoadProjectiles`、`PickNextShoot` | 装袋与按剩余比例抽下一发。 |
| `MakeChoice`、`DealDamage`、`Update` | 选目标、发射、结算伤害、换手及判定整场胜负。 |
| `GetItem`、`HasItem`、`CountItem`、`RecoverItemes` | 道具查询与补充；`RecoverItemes` 是源码原有拼写。 |
| `ItemUsable`、`UsePacket`、`UseItem` | 可用性检查、消耗卡片和执行效果。 |
| `ActAI` | 僵尸决策。 |
| `DrawBackdrop`、`Draw`、`MouseDownCornRoulette` | 绘制、按钮和展示阶段的点击处理。 |

以上简写方法均带 `CornRoulette` 前缀，最后一个鼠标方法除外。

## 反编译源码导航

相对于 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3`：

| 文件 | 重点 |
|---|---|
| `Lawn/Challenge.cs` | 道具池、`CornRoulettePickNextShoot` 至 `CornRouletteItemUsable` 的完整逻辑。 |
| `Lawn/ChallengeScreen.cs` | 关卡定义及 `UpdateButtons()` 中的隐藏条件。 |
| `Lawn/Board.cs` | 自己／对方按钮、卡槽数量、背景、换局和原有 UI 的特殊处理。 |
| `Lawn/SeedPacket.cs`、`Lawn/SeedBank.cs` | 道具卡点击、图标和道具栏展示。 |
| `Lawn/Plant.cs`、`Lawn/Zombie.cs` | 寒冰菇等待状态、轮盘代表僵尸及吃脑子流程。 |
