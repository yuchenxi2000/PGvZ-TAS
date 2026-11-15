# PGvZ 1.4.3 代码核对与版本归属

本文依据本地 `PGvZ-decompilation-1.4.3`，并对比本地完整旧源码 1.3.1 和仓库已有
1.3.x 类型存根。静态分析之外的用户实测反馈单独注明；没有完整的 1.3.4、1.4.0–1.4.2 源码作逐版对比，
因此不能将全部差异标为“1.4.3 首次新增”。

该包 `LawnApp.AppVersionNumber` 为 `PGvZ 1.4.3`，程序集文件版本为 `1.4.3.0`，
信息版本仍为 `1.4.3-alpha`。`GameUpdate.mUpdates` 内置公告最新的非空条目是 1.4.0，
还有一个无正文的 1.4.1 条目，没有单独列出 1.4.2、1.4.3 的公告。

## 已写入但未开放的内容

- [玉米轮盘普通版与无尽版](../levels/corn-roulette.md)：模式编号 151、152，
  完整包含弹药、道具、AI、生命和胜负结算，但关卡菜单强制隐藏入口。
- 经典横向卡槽：新增卡面绘制、卡槽宽度与 X 坐标、传送带横向偏移、选卡界面和
  滑入滑出处理，以及 `ApplyInterfaceLayout()`。但 `PlayerInfo.mClassicSeedChooser`
  的 getter 固定返回 `false`；setter 仍写入 `_classicSeedChooser`，存档也保存该字段。
  当前给属性赋 `true` 不能真正启用功能，不能称其为已开放的界面选项。
  对应 `GameConstants.ENABLE_CLASSIC_SEED_CHOOSER` 是值为 `false` 的编译期常量，
  不存在可直接修改的运行时开关；若要启用，需要进一步改写 getter 或调用逻辑。
  用户测试直接挂钩 getter 后未见布局生效；修改器已撤回试验性开关和挂钩，等待官方开放。
- 主菜单左侧新增画廊按钮，但点击仅显示 `ART_GALLERY_COMING_SOON` 对话框。

## 金盏花与立绘遮挡

金盏花娘化明确列在内置 1.4.0 公告中。1.4.3 的生产实现增加独立生产状态、
三种动画、钻石语音与每次生产 1/20000 概率掉落三颗钻石，详见
[金盏花生产机制](../plants/marigold-production.md)。无法仅凭当前对比确定这些生产细节
各自在 1.4.x 的哪一补丁首次出现。

金盏花已改用 Spine 动画，旧花色代码写入的轨道实例颜色不再参与骨骼绘制。
修改器已移除失效的花园花色修复 Hook，详见保留的
[花色渲染与历史修复文档](../plants/zen-garden-marigold-rendering.md)。

`LawnApp.ShouldCensorTachie()` 仅依据操作系统返回结果：Android、iOS 为 `true`，
其他平台为 `false`，不是玩家设置。当前调用位于 `AlmanacDialog` 的静态立绘查看流程，
只对魅惑菇、金盏花设置 `IMAGE_TACHIE_PATCH`：

| 植物 | 补丁偏移 |
|---|---|
| 魅惑菇 `Hypnoshroom` | `(1523, 1485)` |
| 金盏花 `Marigold` | `(1656, 1264)` |

`TachieWidget.DrawPage()` 通过 `Graphics.DrawImageWithOpaquePatch()` 合成立绘。
这条路径不能推导为“所有植物、所有动画都受到遮挡”。

修改器手机端“常用修改”的“去除立绘遮挡”对应 `CheatOption.disableTachieCensor`，默认开启。
它控制图鉴立绘，与关卡无关；电脑版原生没有这层遮挡，因此网页隐藏该开关。
当前直接挂钩 `LawnApp.ShouldCensorTachie()`：开启时返回 `false`，关闭时调用原方法；
切换后需要关闭并重新打开立绘，因为补丁在创建立绘时设置。用户已确认该挂钩有效，
没有改写绘制路径。

## 内置公告明确归属于 1.4.0 的其他变化

| 内容 | 源码确认 |
|---|---|
| 邮箱系统 | 主菜单新增左侧页面和邮箱入口、未见邮件数；按冒险进度补发 7 封僵尸信。支持已读、删除和领取奖励。 |
| 更新奖励改走邮箱 | 配置为 3 巧克力、10 钻石、3 盆栽礼物；`GameUpdate.ApplyVersion()` 依据历史最高游戏版本处理，不是每次启动都发。 |
| 植物僵尸回归 | `WarAndPeas` 恢复豌豆、坚果头，第二关加入辣椒、机枪、窝瓜、高坚果头；僵尸头部改用 `*Original` 动画资源。 |
| [草坪放大](grid-focus.md) | 原生作弊菜单新增“放大模式”，选择格子后镜头平滑放大到 3 倍乘场景缩放系数，并隐藏主要 UI；点击或返回可恢复。 |
| 花园容量修复 | 是否购买夜间花园参与容量计算；批量领取可传所需空间，并检查总盆栽数不超过 200。 |
| 暂停动画修复 | 暂停对话框内报纸僵尸动画的坐标补上 UI 缩放。 |
| 困难冒险调整 | 公告明确写明移除屋顶困难冒险的螺旋桨僵尸。 |

邮箱基础设施还支持十盆栽奖励，但 `DeliverAdventureReward()` 在当前源码中没有调用点，
不能将其当成已接入的通关奖励发放路径。

## 其他累计差异与适配注意

- 修改器的“出怪”勾选列表补齐六种植物僵尸，复用现有自然／强制出怪操作。
  此次只增加勾选项；自然出怪仍保留游戏原有筛选，生存模式的原生候选抽取会排除
  这些类型。需要直接使用选中类型时可用强制出怪。
- 新增原生联网版本检查：启动后异步获取版本号，10 秒超时，发现更高版本后提示前往下载。
- 用户存档版本增加 `OptionClassicSeedChooser = 18`、`ClassicConveyorOffset = 19`、
  `MailboxState = 20`。邮箱、最高运行版本等加入保存；`PlayerInfo.SaveDetails()` 改为返回
  实际保存结果，邮件领取、删除等操作在失败时恢复相关内存状态。
- 轮盘在 `SeedType` 72–75 插入四个道具，旧的 `ZombieNormal` 至 `ZombieImp` 数值由
  72–86 移至 76–90。依赖这些旧式数值的外部脚本需要核对，枚举名称和 flag 表示也应区分。
- `Board.AddCoinForDropLootType()` 新增可选掉落运动参数；`Coin.CoinInitialize()` 新增
  可选盆栽对象参数，`Coin.Draw()` 新增图标绘制参数，服务于掉落复用及邮箱奖励展示。
- 相对 1.3.1 可见裂荚射手动画、发射位置及火豌豆缩放处理变化；裂荚娘化已明确属于
  1.3.2，不应整体算作 1.4.3 新植物。
- 动态鼓点属于 1.3.2，安卓版鼓点报错修复属于 1.3.4；它们解释了本地两份完整源码间
  大量音乐引擎差异，不应计入 1.4.x 的新增列表。

## 反编译源码导航

以下路径相对于 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3`：

| 文件 | 重点 |
|---|---|
| `Lawn/GameUpdate.cs` | 内置逐版本公告、更新奖励和最高版本处理。 |
| `Lawn/GameSelector.cs` | 左侧菜单、画廊占位和邮箱入口。 |
| `Lawn/LocalMailbox.cs`、`Lawn/LocalMail.cs`、`Lawn/MailScreen.cs` | 邮件投递、保存、奖励和 UI。 |
| `Lawn/LawnApp.cs`、`Lawn/GameUpdateChecker.cs` | 遮挡平台条件、界面切换、联网更新检查。 |
| `Lawn/AlmanacDialog.cs`、`Lawn/TachieWidget.cs`、`Sexy/Graphics.cs` | 立绘遮挡对象、位置和合成。 |
| `Lawn/PlayerInfo.cs`、`Lawn/SaveFileVersion.cs` | 固定关闭的经典卡槽属性及新增存档字段。 |
| `Lawn/Board.cs`、`Lawn/ZBCheatDialog.cs` | 草坪格子放大功能。 |
