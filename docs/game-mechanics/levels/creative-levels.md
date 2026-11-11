# 自定义关卡与在线关卡

本文记录 PGvZ v1.3.0 中 `Lawn.Creative` 自定义关卡系统的文件位置、JSON
格式、运行方式，以及本地关卡和在线关卡之间的区别。内容来自当前版本类型存根与反编译代码；
服务器发布和审核流程不在游戏客户端中，因此不在本文范围内。

## 1. 两类关卡不是同一个目录

| 项目 | 本地关卡（DIY） | 在线关卡 |
|---|---|---|
| 游戏页面 | “本地关卡” | “在线关卡” |
| 数据来源 | 玩家放置的 `*.json` | `levels.pgvz.top` 下载 |
| `GameMode` 范围 | `40000` 至 `49999` | `50000` 起 |
| 本地位置 | `docs/levels/` | `docs/cache/online-levels-v2/` |
| 是否需要联网 | 否 | 浏览目录及首次下载时需要 |
| 完成记录 | 不记录为已通关挑战 | 按服务器 `LevelId` 记录 |
| 关卡存档标识 | JSON 内容 CRC | JSON 内容 CRC |

两类关卡最终都交给 `CreativeLevelManager.LoadLevel()` 解析，使用相同的 JSON
组件格式。区别主要发生在关卡从哪里取得、如何分配临时 `GameMode`、是否记录完成状态，
以及是否使用下载缓存。

### 1.1 存储根目录

上述路径都相对于游戏的 `applicationStoragePath`，不是相对于 TAS 仓库，也不一定是
游戏当前工作目录。

PC 版启动时会读取游戏可执行文件同级的 `config.json`：

- 若配置了 `storage_path`，先展开其中的环境变量，再将结果作为存储根目录；
- 若没有配置，则使用游戏可执行文件所在目录。

因此完整路径分别为：

```text
<applicationStoragePath>/docs/levels
<applicationStoragePath>/docs/cache/online-levels-v2
```

如果不知道实际的存储根目录，可以先查找已经生成的 `online-levels-v2` 文件夹。假设找到：

```text
D:/PGvZData/docs/cache/online-levels-v2
```

那么本地关卡目录就是：

```text
D:/PGvZData/docs/levels
```

## 2. 本地关卡的加载流程

游戏打开“本地关卡”页面，或者在该页面点击 `Reload` 时，执行以下操作：

1. 清除先前注册的本地 `GameMode`；
2. 创建 `<applicationStoragePath>/docs/levels`；
3. 只枚举该目录顶层的 `*.json`，不递归子目录；
4. 按文件路径进行不区分大小写的顺序排序；
5. 依次读取文件，移除可选的 UTF-8 BOM；
6. 从 `40000` 开始为成功加载的文件分配连续 `GameMode`；
7. 解析或校验失败的文件显示错误，但不占用编号。

这意味着仅进入“在线关卡”页面不会创建 `docs/levels`。目录不存在时可以进入一次
“本地关卡”页面，也可以手动创建。

本地关卡的数字 `GameMode` 取决于文件排序，并不是稳定身份。重命名或插入文件可能改变
其编号。游戏使用 JSON 原始内容的 CRC 生成关卡存档名，避免单纯依靠临时编号；但这也意味着
修改空格、换行或字段顺序都可能产生新的 CRC，使旧存档不再自动匹配。

## 3. 在线关卡的加载与缓存

### 3.1 目录与分页

进入“在线关卡”页面时，游戏请求：

```text
https://levels.pgvz.top/api/v2/levels
```

当前客户端每页请求 20 项，使用游标翻页。目录项包含关卡 ID、中英文标题、作者、难度、
标签、是否无尽、推荐信息、发布时间、图标信息和关卡压缩包信息。

当前反编译版本在请求中传递 `clientVersion=99999`。目录模型虽然包含
`MinClientVersion`，但客户端没有在本地再次检查该字段。

目录响应上限为 1 MiB，HTTP 超时为 30 秒。客户端只接受
`https://levels.pgvz.top` 同源的图标和关卡资源地址。

### 3.2 下载时机

目录页面只取得元数据和图标。玩家选择关卡并在详情对话框点击开始后，游戏才下载关卡主体。
当前页面第 `n` 项临时映射为 `GameMode = 50000 + n`；换页或刷新后，同一个数字可能代表
不同关卡，因此完成记录使用稳定的服务器 `LevelId`，存档使用 JSON CRC。

### 3.3 缓存结构

```text
docs/cache/online-levels-v2/
├─ icons/
│  └─ <图标 SHA-256>.png
└─ payloads/
   └─ <压缩包 SHA-256>.zlib
```

- 图标上限为 2 MiB，客户端最多保留 100 个图标文件；
- 关卡压缩包及解压结果各自不得超过 4 MiB；
- `payloads` 保存的是 zlib 压缩数据，不是可直接编辑的 JSON；
- 命中缓存时仍会重新检查文件大小、压缩包哈希、解压后大小和内容哈希；
- 校验失败的缓存会被删除，然后重新下载；
- 下载成功后，解压出的 JSON 仍由 `CreativeLevelManager` 按本地关卡的同一套规则解析。

在线关卡完成时，非无尽关卡按 `LevelId` 增加完成次数；本地 DIY 关卡不会写入普通挑战完成记录。
客户端只有浏览、下载、缓存和游玩代码，没有上传或发布关卡的实现。

## 4. JSON 根结构

最小结构如下：

```json
{
  "Version": 3,
  "Components": [
    {
      "Type": "LevelProperty",
      "Name": "Example Level"
    }
  ]
}
```

规则如下：

- `Version` 必须是整数，当前只接受 `1`、`2`、`3`，新关卡建议使用 `3`；
- `Components` 必须是数组；
- 至少需要一个 `Type: "LevelProperty"`；
- `Type` 和其他字段名区分大小写；
- 所有组件先初始化，之后再统一执行 `Check()`，所以互斥检查不依赖排列顺序；
- 未注册的 `Type` 会被静默跳过，不会主动报“未知组件”；
- 重复组件不会报错，但运行时 `GetComponent<T>()` 只返回第一个，应避免重复；
- 数组辅助函数名称虽然包含 `FromString`，实际输入仍然是 JSON 数组，不是字符串。

## 5. `CS*` 组件的注册方式

`Lawn.Creative` 中的 `CS*` 是实现 `IComponent` 的组件类，不是独立的关卡方法。注册时游戏
移除类名开头的 `CS`，将剩余部分作为 JSON 的 `Type`：

```text
CSLevelProperty  -> "Type": "LevelProperty"
CSSeedBank       -> "Type": "SeedBank"
CSVaseLevel      -> "Type": "VaseLevel"
```

组件主要负责读取参数和检查配置。玩法本身仍在原来的 `Board`、`Challenge`、`Plant`、
`Zombie`、`Projectile` 和 `CutScene` 等类中执行。这些流程通过
`mCreativeLevel.GetComponent<CS...>()` 判断组件是否存在，再替换默认数值或进入已有小游戏分支。

因此，自定义关卡不是一套独立的 `Board` 实现，而是对原有关卡流程的组合和覆盖。

## 6. 类型编号与坐标

JSON 中的植物、僵尸、场景、子弹和音乐编号经过对应的 `*Convertor` 转换，不应直接假设它们
等于当前 C# 枚举的底层值。

常用编号：

| 类别 | 编号示例 |
|---|---|
| 植物 | `0` 豌豆射手、`1` 向日葵、`3` 坚果、`5` 寒冰射手、`47` 玉米加农炮 |
| 僵尸 | `0` 普通、`1` 旗帜、`2` 路障、`4` 铁桶、`23` 巨人、`24` 小鬼 |
| 场景 | `0` 白天、`1` 黑夜、`2` 泳池、`3` 雾夜、`4` 屋顶、`5` 僵王场景 |
| 子弹 | `0` 豌豆、`1` 寒冰豌豆、`6` 火球、`10` 玉米粒、`11` 玉米炮弹、`12` 黄油 |
| 音乐 | `0` 无、`1` 白天、`2` 黑夜、`3` 泳池、`4` 雾夜、`5` 屋顶 |

植物卡还有三段偏移编码：

```text
普通植物卡：植物编号
模仿者植物卡：植物编号 + 10000
僵尸卡：僵尸编号 + 20000
魅惑僵尸卡：僵尸编号 + 30000
```

新角色使用保留的高编号段。例如当前转换表中，特殊植物从 `2000` 开始，特殊僵尸也从
各自类别的 `2000` 开始。需要完整映射时，以当前游戏版本的
`SeedTypeConvertor`、`ZombieTypeConvertor`、`BackgroundTypeConvertor`、
`ProjectileTypeConvertor` 和 `MusicTuneConvertor` 为准。

场地坐标从零开始：`x` 为 `0..8`，`y` 为 `0..5`。普通五行场景通常只使用
`y=0..4`；第六行是否有效取决于场景。

## 7. 基础组件

### 7.1 `LevelProperty`：必需的关卡属性

| 字段 | 默认值 | 作用 |
|---|---:|---|
| `Name` | `null` | 通用名称 |
| `ChineseName` / `EnglishName` | `null` | 按语言覆盖名称 |
| `Icon` | `-1` | 内置图标编号 |
| `IconImage` | `null` | Base64 编码图片；加载后优先用于本地关卡图标 |
| `Background` | `0` | 场景编号 |
| `MusicType` | `null` | 音乐编号；负数恢复为默认选择 |
| `InitPlantColumn` | `0` | 屋顶开局自动放置花盆的列数 |
| `EasyUpgrade` | `false` | 升级植物不要求底层植物等宽松种植规则 |
| `NumWaves` | `40` | 每阶段波数 |
| `WavesPerFlag` | `10` | 每个旗帜包含的波数 |
| `StartingSun` | `50` | 初始阳光 |
| `StartingWave` | `0` | 开始时的当前波次，下标从零开始 |
| `StartingTime` | `1800` | 第一波倒计时，单位为游戏更新次数 |
| `AllowedZombies` | `null` | 允许参与随机选取的僵尸编号；空时默认普通、路障、铁桶 |
| `SpawnFlagZombie` | `true` | 旗帜波是否加入旗帜僵尸 |
| `MaxPlainZombiesPerFlag` | `8` | 旗帜波最多预先加入的普通僵尸数量 |

`InitPlantColumn` 必须在 `0..9` 内，波数、旗帜间隔、开始波次和开始倒计时不得为负数。

### 7.2 卡槽和开局对象

| `Type` | 主要字段与作用 |
|---|---|
| `SeedBank` | 普通卡槽。`NumPackets` 为 `-1..10`，`-1` 使用模式默认值；`BannedCards` 是植物卡编号；`ReverseBanning=true` 时列表变成白名单；`LockedCards` 配合 `UserChoose=false` 固定卡槽。 |
| `ConveyorBelt` | 传送带。`AllowedPlants` 为 `[[卡片编号, 权重], ...]`，`InitCards` 为开局卡片，`PrepareTimeMultiplier` 调整补卡间隔且必须大于零。不能与 `SeedBank` 共存。 |
| `DefaultPlantOnLawn` | `Plants` 为 `[[卡片编号, x, y], ...]`，在入场阶段放置固定植物。 |
| `SpawnSkySun` | `SpawnFromSky` 控制天空阳光；`MinTime`、`MaxTime`、`RandomRangeTime` 和 `IncrementPerSun` 控制间隔；`SunType` 的 `0/1/2` 分别为小/普通/大阳光。 |

### 7.3 工具与通用开关

| `Type` | 作用 |
|---|---|
| `Glove` | `Enabled` 控制手套，`Cooldown` 覆盖冷却且不得为负数。 |
| `Shovel` | `Enabled` 控制铲子。 |
| `Pause` | `Enabled` 控制关卡内暂停按钮。 |
| `Trashcan` | `Enabled` 控制垃圾桶。 |
| `PlantSkill` | `Enabled` 控制龙舌兰和终焰的主动技能。 |
| `Fusion` | `Enabled` 控制融合种植机制。 |
| `ExtendedPoolZombies` | `Enabled` 控制扩展泳池类僵尸能否进入泳池行。 |
| `ColumnPlanting` | 无字段；存在时启用整列种植。 |
| `Speed` | `ExtraUpdateTimes` 指定每次 `Challenge.Update()` 额外调用 `Board.UpdateGame()` 的次数，至少为 `1`。 |

`Enabled` 类型组件只要省略字段就默认为 `true`。若只想显式关闭某项行为，需要保留组件并写
`"Enabled": false`。

## 8. 波次与僵尸组件

### 8.1 自动和手动点数

`AutoZombiePoint` 自动覆盖每波的出怪点数：

```text
基础点数 = floor(有效波次 × PointIncrementPerWave) + StartingPoints
旗帜波点数 = 基础点数 × FlagPointMultiplier
最终点数 = 上述点数 × PointMultiplier
```

默认值为：

```json
{
  "Type": "AutoZombiePoint",
  "StartingPoints": 1,
  "PointIncrementPerWave": 0.333334,
  "FlagPointMultiplier": 2.5,
  "PointMultiplier": 1.0
}
```

生存模式中的有效波次会加上之前阶段的波数。起始点数和两个倍率不得为负数。

`ManualZombiePoint` 使用 `Density` 数组逐波指定点数：

```json
{
  "Type": "ManualZombiePoint",
  "Density": [1, 1, 2, 2, 3, 3, 4, 4, 5, 8]
}
```

数组长度不得小于 `LevelProperty.NumWaves`。它与 `AutoZombiePoint` 互斥。

### 8.2 固定出怪和波次推进

| `Type` | 格式与作用 |
|---|---|
| `MustHaveZombie` | `Zombies` 为 `[[波次, [僵尸编号...]], ...]`，在波次生成阶段强制加入；`ZombiesInRow` 为 `[[波次, 僵尸编号, 行], ...]`，在实际刷新时固定行。波次从零开始。 |
| `ManualZombieCountDown` | `Zombies` 为 `[[波次, 下一波倒计时, 血量推进阈值], ...]`；第三项可省略，默认 `0`。它覆盖当前波生成后的推进条件。 |
| `BungeeBlitz` | 存在时启用蹦极闪电战的生成、落地和投放分支；`ShowHugeFlagAdvice` 控制大波提示。 |
| `InvisibleZombie` | 无字段；存在时使用隐形僵尸的绘制和影子规则。 |

### 8.3 属性覆盖

`OverridePlantProperty.Properties` 是对象数组。每项的 `SeedType` 可以是单个编号或编号数组，
可覆盖：

```text
SeedCost、RefreshTime、LaunchRate、PlantHealth
```

`OverrideZombieProperty.Properties` 的 `ZombieType` 同样可以是单个编号或数组，可覆盖：

```text
BodyHealth、HelmHealth、ShieldHealth、FlyingHealth、ZombieValue、
FirstAllowedWave、PickWeight、CanGoInPool、CanGoOnHighGround、
ScaleZombie、ScaleHealth
```

`OverrideProjectileProperty.Properties` 的 `ProjectileType` 可以是单个编号或数组，目前可覆盖
`Damage`。组件顶层的 `AllowZombiePeaAttackFlowerPot` 控制僵尸豌豆是否将花盆作为碰撞目标。

示例：

```json
{
  "Type": "OverridePlantProperty",
  "Properties": [
    {
      "SeedType": [0, 5],
      "SeedCost": 25,
      "RefreshTime": 300,
      "PlantHealth": 600
    }
  ]
}
```

## 9. 场地与天气组件

| `Type` | 主要字段与作用 |
|---|---|
| `SpawnFog` | `Column` 指定雾的左边界列，默认 `3`。 |
| `SpawnGraveStone` | `CountPerColumn` 是最多九项的逐列墓碑数量；`AllowGraveStoneOnDirt` 允许在泥地生成。每列数量必须在 `0..6`。 |
| `SpawnLadder` | `Ladders` 为 `[[0, x, y], ...]`。第一项目前只接受 `0`。 |
| `SpawnPortal` | `Portals` 为 `[[类型, x, y], ...]`，`0` 为圆形、`1` 为方形；还可设置 `RandomPortalTime`、`FixSpawnZombieView`、`FixPlantAttackView`。负数随机移动时间表示不随机移动。 |
| `Weather` | `HasRain` 和 `HasStorm` 控制下雨及雷暴。启用雷暴时不能同时使用 `RainingSeeds` 或 `VaseLevel`。 |

## 10. 特殊玩法组件

许多特殊玩法组件是“存在即启用”的模式标记。加入组件后，`LawnApp` 的
`IsSurvivalMode()`、`IsIZombieLevel()`、`IsScaryPotterLevel()` 等判断会把当前 JSON 关卡
当作对应模式，之后复用原有 `Challenge` 逻辑。

| `Type` | 主要字段与作用 |
|---|---|
| `RainingSeeds` | 天降卡片。`AllowedPlants` 为 `[[植物编号, 权重], ...]`；`MinPrepareTime`、`MaxPrepareTime` 控制掉落间隔。不能与 `VaseLevel` 共存。 |
| `SlotMachineLevel` | 拉霸机。`TargetSunCount` 是获胜目标；`AllowedPlants` 的短格式是 `[植物编号, 固定权重]`，完整格式是 `[植物编号, 初始权重, 最终权重, 植物数量起点, 植物数量终点]`。不能与 `SeedBank`、`ConveyorBelt`、`ManualZombiePoint` 共存。 |
| `SurvivalLevel` | 生存模式。`Endless`、`Stages`、`MaxRandomZombieTypeCount` 控制阶段；`Zombies` 可为各僵尸设置价值、出现波次和动态权重；`MustHaveZombieGroup` 设置必选组；`AcceleratedPricing` 启用加速涨价。 |
| `VaseLevel` | 砸罐子。`MinColumn`、`MaxColumn` 限定列；`PlantVases`、`ZombieVases` 为 `[[类型, 数量], ...]`；`NumPlantVases`、`NumZombieVases` 调整罐子外观类型数量。 |
| `IZombieLevel` | 我是僵尸。`Limit` 控制随机放置植物使用的最大列数；`PlantInSquare` 为 `[[植物, x, y], ...]`；`PlantInRow` 为 `[[植物, 数量, 行], ...]`，行写 `-1` 时可覆盖全部行。 |
| `WhackAZombieLevel` | 锤僵尸。可设置初始/最低墓碑数、出怪间隔、六阶段的双出/三出概率，以及各僵尸的阶段权重、是否参与三出和末波。 |
| `WallnutBowlingLevel` | 无字段；存在时启用坚果保龄球规则。通常还需要配置 `ConveyorBelt` 提供坚果。 |

系统只显式检查少数组件冲突，并没有统一的“主模式只能有一个”限制。若同时加入多个大型玩法
组件，多个独立的 `Challenge.Update()` 分支可能在同一帧运行。除非已经检查过相应调用链，
建议一个关卡只选一个主要特殊玩法组件，再组合场地、属性覆盖和工具组件。

## 11. 可运行的普通关卡示例

将下列内容保存为：

```text
<applicationStoragePath>/docs/levels/00-example.json
```

```json
{
  "Version": 3,
  "Components": [
    {
      "Type": "LevelProperty",
      "Name": "Example Level",
      "ChineseName": "示例关卡",
      "EnglishName": "Example Level",
      "Background": 0,
      "NumWaves": 20,
      "WavesPerFlag": 10,
      "StartingSun": 150,
      "StartingWave": 0,
      "StartingTime": 1800,
      "AllowedZombies": [0, 2, 4]
    },
    {
      "Type": "SeedBank",
      "NumPackets": 8,
      "UserChoose": true
    },
    {
      "Type": "AutoZombiePoint",
      "StartingPoints": 1,
      "PointIncrementPerWave": 0.333334,
      "FlagPointMultiplier": 2.5,
      "PointMultiplier": 1.0
    },
    {
      "Type": "SpawnSkySun",
      "SpawnFromSky": true,
      "SunType": 1
    }
  ]
}
```

返回主菜单并进入“本地关卡”，或者点击页面中的 `Reload`。成功后关卡名称应显示为
“示例关卡”。如果没有显示，查看页面上的文件名和 `Check error(...)` 提示。

## 12. 常见问题

### 12.1 进入在线关卡后没有 `docs/levels`

这是正常行为。在线关卡只创建 `docs/cache/online-levels-v2`。进入“本地关卡”页面才会创建
`docs/levels`，也可以在同一个 `docs` 目录下手动创建 `levels`。

### 12.2 JSON 放进去但列表为空

依次检查：

1. 是否放在实际 `applicationStoragePath`，而不是另一个游戏副本或 TAS 仓库；
2. 是否直接位于 `docs/levels` 顶层；
3. 扩展名是否为 `.json`；
4. 根节点是否有有效的 `Version`、`Components` 和 `LevelProperty`；
5. `Type` 大小写是否完全正确；
6. 是否进入了“本地关卡”而不是“在线关卡”。

### 12.3 修改关卡后续关失败

关卡存档名包含 JSON 原始内容的 CRC。编辑配置后 CRC 改变，游戏会把它视为另一份关卡存档。
这不是根据文件名迁移存档。

### 12.4 在线关卡反复重新下载

检查 `docs/cache/online-levels-v2/payloads` 是否可写，以及代理、安全软件或文件同步工具是否修改
缓存。客户端会在文件大小、SHA-256、zlib 解压大小或解压后 SHA-256 任一项不匹配时删除缓存。

### 12.5 在线目录能打开，但关卡不能开始

目录和关卡主体是两次请求。能看到列表只说明目录请求成功；点击开始后仍可能因为资源地址、
下载超时、4 MiB 大小限制、哈希、zlib 解压或 JSON 组件校验失败而停止。页面会显示
`OnlineLevel.LastError` 或 `CreativeLevelManager.mError` 的错误信息。

## 13. 反编译源码导航

继续核对当前游戏实现时，优先查看同级反编译目录中的以下文件：

| 文件 | 内容 |
|---|---|
| `Lawn.Creative/CreativeLevel.cs` | 组件注册、根 JSON 解析、版本和组件校验 |
| `Lawn.Creative/CreativeLevelManager.cs` | 本地目录枚举、关卡注册、CRC |
| `Lawn.Creative/CS*.cs` | 每个组件的字段、默认值和检查条件 |
| `Lawn/OnlineLevelManager.cs` | 在线目录、下载、缓存、哈希和解压 |
| `Lawn/OnlineLevel*.cs` | 在线目录数据模型和入口 |
| `Lawn/ChallengeScreen.cs` | 本地/在线页面、临时 `GameMode` 和进入关卡流程 |
| `Lawn/LawnApp.cs` | 模式判断、完成记录及 `mCreativeLevel` 绑定 |
| `Lawn/Board.cs`、`Lawn/Challenge.cs` | 波次、卡槽、特殊玩法的主要执行逻辑 |
| `Lawn/*Convertor.cs` | JSON 稳定编号到当前枚举的映射 |

