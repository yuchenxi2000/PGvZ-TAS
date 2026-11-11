# 僵尸种子包 flag 与内部调用边界

本文依据 PGvZ 1.3.0、1.3.1 反编译代码，并与 1.2.6 对比，记录
`Lawn.SeedType.ZombieCardFlag` 和 `Lawn.SeedType.MindControlledCardFlag` 的表示方式、
原生放置路径、1.3.1 对 `SeedType.None` 误判的修复，以及 PGvZ-TAS/PGvZTool
调用相关内部方法时的安全边界。

## 1. 结论

这两个值不是可以单独当作植物种类使用的普通 `SeedType`，而是编码
`ZombieType` 的高位标志：

```text
普通僵尸卡 SeedType = 0x20000000 | int(ZombieType)
魅惑僵尸卡 SeedType = 0x40000000 | int(ZombieType)
```

在 IronPython 中可显式构造对应枚举，避免依赖不同枚举类型之间的按位运算：

```python
import System
import Lawn

def ZombieCard(zombie_type, mind_controlled=False):
    flag = (Lawn.SeedType.MindControlledCardFlag if mind_controlled
            else Lawn.SeedType.ZombieCardFlag)
    return System.Enum.ToObject(Lawn.SeedType, int(flag) | int(zombie_type))
```

它们的用途是让种子包、可用卡片掉落物和光标放置流程承载任意僵尸类型。正确的终点是
`Challenge.IZombiePlaceZombie`，不是 `Board.AddPlant`。

因此，`placer.PlantOnBoard` 使用带 flag 的值时报错是确定行为：

```text
placer.PlantOnBoard
  -> Board.AddPlant
  -> Board.NewPlant
  -> Plant.PlantInitialize
  -> Plant.GetPlantDefinition
  -> GameConstants.gPlantDefs[(int)theSeedtype]
```

`Plant.GetPlantDefinition` 明确要求 `0 <= SeedType < SeedTypeCount`。带 flag 的值至少为
`0x20000000`，会被当作植物定义数组下标，最终越界。旧式我是僵尸卡
`ZombieNormal`～`ZombieImp`（72～86）同样不能传给 `Board.AddPlant`。

## 2. 编码、识别与转换

### 2.1 运行时值

`Challenge.IsZombieSeedType` 先检查两个 flag，再兼容旧式我是僵尸卡枚举。
`Challenge.IZombieSeedTypeToZombieType` 按以下顺序解码：

1. 在 1.3.1 中，若值为 `SeedType.None`，直接返回 `ZombieType.Invalid`；
2. 如果有 `MindControlledCardFlag`，清除该位并返回剩余值对应的 `ZombieType`；
3. 否则如果有 `ZombieCardFlag`，清除该位并返回对应的 `ZombieType`；
4. 否则使用旧式 `ZombieNormal`～`ZombieImp` 到 `ZombieType` 的固定映射。

两个 flag 必须互斥。若同时设置，第一步只会清除魅惑位，普通僵尸卡位仍留在结果中，
得到无效的 `ZombieType`。

除 `None` 特例外，这两个判断仍只检测位是否存在，不校验剩余值是否合法。尤其
`SeedType.None == -1` 的所有二进制位均为 1，在 1.3.0 中会被误判为魅惑僵尸卡；
`IZombieSeedTypeToZombieType(None)` 也会得到数值为 `-1073741825` 的无效枚举，而不是
`ZombieType.Invalid`。1.3.1 在两个方法开头显式排除 `None`，分别返回 `false` 和
`ZombieType.Invalid`。调用者在 1.3.1 中不再需要为 `None` 单独防护，但仍应保证其他
带 flag 值的低位确实是有效的 `ZombieType`。

### 2.2 创意关卡稳定编号

`SeedTypeConvertor` 为 JSON 使用另一套稳定编号：

- `20000 + ZombieTypeConvertor` 编号：普通僵尸卡；
- `30000 + ZombieTypeConvertor` 编号：魅惑僵尸卡；
- `10000 + SeedTypeConvertor` 编号仍表示模仿者植物。

读取后才会转换成上述高位 flag。创意关卡 JSON 不应直接写运行时的
`0x20000000 | ZombieType` 数值。

1.3.1 的 `SeedTypeConvertor.ToInt` 在按 flag 转换前新增了 `SeedType.None` 判断，明确返回
`-1`。在 1.3.0 的现有转换表中，`None` 虽然先被误当作魅惑僵尸卡，但其低位对应的无效
`ZombieType` 最终也会查表失败并返回 `-1`，所以这里主要是消除错误的中间语义和防止转换表
扩展后产生意外结果，当前可观察的 JSON 编号没有变化。

### 2.3 存档名称

`GlobalMembersSaveGame.SeedTypeSaver` 会把普通僵尸卡写成 `+ZombieName`，
把魅惑僵尸卡写成 `-ZombieName`，并为 `ZombieType` 枚举值注册两套组合。

1.3.0 同样会因按位判断把 `SeedType.None` 当作魅惑僵尸卡。清除魅惑位后的值不是有效
`ZombieType`，`Enum.GetName` 返回空值，最终将 `None` 写成只有一个减号的 `"-"`。
读取该名称时，僵尸枚举解析会抛出异常，再由外层同步逻辑回退到 `SeedTypeSaver` 的默认值
`None`，所以通常仍能往返，但存档枚举表包含畸形名称并依赖异常恢复。1.3.1 先判断
`e == SeedType.None`，改由基础枚举保存器写出并读取正常名称 `"None"`。1.3.1 仍可通过
回退逻辑读取 1.3.0 的 `"-"`，1.3.0 也能按普通枚举名称读取 1.3.1 的 `"None"`。

但旧的逐对象 `LoadFromFile` 路径仍有 `SeedTypeLegacy.FromInt` 调用。该函数把读出的整数
直接当作长度 75 的旧枚举映射下标；`SeedPacket`、`CursorObject`、`Coin`、`GridItem` 和
`Challenge.mLastConveyorSeedType` 的这些旧加载路径无法读取高位 flag。当前同步存档路径有
`SeedTypeSaver` 支持，但若复用旧序列化接口，需要单独验证。

## 3. 1.3.x 原生支持链路

给 `SeedPacket` 或 `Coin.mUsableSeedType` 设置僵尸卡后，原生交互链如下：

```text
SeedPacket.MouseDown / Coin.MouseDown
  -> CursorObject.mType = 带 flag 的 SeedType
  -> Board.MouseUpWithPlant
  -> Challenge.IsZombieSeedType
  -> Challenge.IZombieMouseDownWithZombie
  -> Challenge.IZombieSeedTypeToZombieType
  -> Challenge.IZombiePlaceZombie
  -> Board.AddZombieInRow
  -> 魅惑卡额外调用 Zombie.StartMindControlled
```

1.3.0 为这条链路补齐了以下行为：

| 方法 | flag 相关行为 |
|---|---|
| `Board.MouseUpWithPlant` | 非我是僵尸关卡中也会把僵尸卡转交给 `IZombieMouseDownWithZombie` |
| `Board.CanPlantAt` | `Challenge.CanPlantAt` 返回后，僵尸卡直接返回结果，不进入植物占格判断 |
| `Challenge.CanPlantAt` | 我是僵尸关卡中识别任意 flag 卡；蹦极僵尸按转换后的 `ZombieType` 使用特殊区域规则 |
| `Challenge.IZombieMouseDownWithZombie` | 放置转换后的僵尸；魅惑 flag 会调用 `StartMindControlled` |
| `CursorPreview.Draw` | 使用僵尸站位预览，并按魅惑方向和颜色绘制 |
| `CursorObject.Draw`、`Plant.DrawSeedType` | 绘制僵尸缩略图；魅惑卡增加染色和加法混合 |
| `SeedPacket.DrawSmallSeedPacket` | 不再只按关卡模式判断，而是按 `IsZombieSeedType` 绘制僵尸卡 |
| `SeedPacket` 名称逻辑 | 使用 `ZombieDefinition.mZombieName`，避免调用植物名称方法 |
| `Plant.GetRefreshTime` | 通过 `IsZombieSeedType` 对所有僵尸卡返回 0 |
| `SeedTypeConvertor`、`SeedTypeSaver` | 支持创意关卡编号和新式存档名称 |

### 3.1 1.3.1 修复的花园模仿者误分流

1.3.1 更新公告中的“修复在花园中移动模仿者生成僵尸”直接来自 `None` 误判。
花园放置盆栽时会把模仿者创建为 `mSeedType == Imitater`、
`mImitaterType == None`；手套拿起植物后，这两个值会原样复制到光标：

```text
花园手套拿起模仿者
  -> CursorObject.mType = Imitater
  -> CursorObject.mImitaterType = None
  -> Board.GetSeedTypeInCursor 返回 mImitaterType，即 None
  -> Board.MouseUpWithPlant 调用 Challenge.IsZombieSeedType(None)
```

在 1.3.0 中最后一步错误返回 `true`，随后进入 `IZombieMouseDownWithZombie`，尝试把
`None` 转成僵尸并执行僵尸放置，而不是正常移动花园植物。1.3.1 返回 `false`，流程继续执行
普通植物的落点和花园移动逻辑。修复位于通用僵尸卡识别函数，因此也消除了其他光标或空卡槽
把 `None` 误分流到僵尸绘制、预览、费用和放置路径的可能性。

## 4. 修改器和 TAS 框架调用审计

### 4.1 可使用原生僵尸卡流程的入口

| 本项目入口 | 结论 | 说明 |
|---|---|---|
| `placer.SetSeedPacket` | 支持，但受费用限制 | `SeedPacket.SetPacketType` 后由原生鼠标/光标链路放置 |
| `pgvz.card.RawCard` / `Card` | 支持，但受费用限制 | `CanPlantAt`、`SeedPacket.MouseDown`、`Board.MouseUpWithPlant` 均进入原生僵尸分支 |
| `placer.AddCoinOnBoard` + `UsableSeedPacket` | 支持，不读取费用 | 拾取后写入 `CursorObject.mType`，放置后会正确销毁卡片掉落物 |
| `placer.AddScaryPotOnBoard` + `ScaryPotType.Seed` | 支持，不读取费用 | 开罐后生成 `UsableSeedPacket`，再进入相同链路 |
| `Board.CanPlantAt` / `Challenge.CanPlantAt` 两个随意种植 hook | 能识别 flag | 关闭选项时原方法支持；开启时直接返回 `Ok`，只会绕过原生区域限制 |
| `Plant.GetCost` / `Board.GetCurrentPlantCost` 两个免费种植 hook | 可规避缺失费用项 | 开启免费种植时直接返回 0，不进入原生不完整的僵尸费用表 |

### 4.2 不应接收带 flag 值的入口

| 本项目入口 | 风险 |
|---|---|
| `placer.PlantOnBoard` | 确定在 `Plant.GetPlantDefinition` 越界；应改走僵尸卡光标链或直接僵尸放置接口 |
| `pgvz.util.SetPlantOnBoard` | 同样直接调用 `Board.AddPlant` |
| `pgvz.lineup` 的布阵恢复 | 同样直接调用 `Board.AddPlant`，布阵数据模型也只表示植物 |
| `pgvz.card.SelectCards` | 用 `int(seedtype)` 索引 `SeedChooserScreen.mChosenSeeds`；高位 flag 必然越界 |
| `cheat.GivePottedPlant` / `AddPottedPlantToGivenPos` | 初始化本身只保存枚举，但花园绘制、偏移、名称及统计大量按植物数组索引，后续会越界 |
| `placer.AddCoinOnBoard` + `PresentPlant` | `PottedPlantSpec` 后续仍按植物处理，不应使用僵尸卡 |
| `Plant.GetImage`、`GetNameString`、`GetToolTip`、`GetPlantDefinition` | 都直接取得植物定义，不支持 flag |

`pgvztool.hook.Plant__PlantInitialize` 也不能使 `PlantOnBoard` 支持僵尸卡。该 hook 除路灯花
特殊逻辑外仍调用原方法，而原方法随后必然执行 `GetPlantDefinition`。

### 4.3 GUI 当前不能表达组合值

`gui/js/data.js` 的 `seedTypes` 只列普通植物和旧式 15 张我是僵尸卡，没有
“flag + `ZombieType`”组合项。网页中的场地放置、改卡槽、罐子和掉落物按钮都生成
`Lawn.SeedType.<枚举成员>`，因此仅增加两个 flag 枚举名也只能表示普通僵尸（低位为 0），
不能表示旗帜、读报等组合类型。

若以后加入 GUI 支持，数据模型应独立保存 `ZombieType` 和“普通/魅惑”卡片模式，再在
Python 端构造组合枚举；不要把所有组合硬编码成不存在的 `SeedType` 成员名。

## 5. 原生费用表的不完整支持

`Plant.GetCost` 虽然在 1.3.0 中增加了带两个 flag 的 case，但只覆盖旧式我是僵尸卡对应的
15 种僵尸：

```text
Normal, TrafficCone, Polevaulter, Pail, Ladder,
Digger, Bungee, Football, Balloon, Door,
Zamboni, Pogo, Dancer, Gargantuar, Imp
```

其他合法 `ZombieType`（例如 `Flag`、`Newspaper`、`Bobsled`、`RobotTitan`、
`Propeller`）会落入默认分支并调用 `GetPlantDefinition(带 flag 的值)`，造成数组越界。

这个问题不仅在点击卡片时触发。`SeedPacket.GetGraynessAndDarkness` 每次绘制种子包都会调用
`Board.GetCurrentPlantCost`，`SeedPacket.CanPickUp` 和 `MouseDown` 也会再次取费用。因此给
卡槽设置一张不在上述列表内的僵尸卡后，可能立刻在绘制阶段报错。

`CoinType.UsableSeedPacket` 不走这套费用查询：掉落物绘制时关闭费用显示，拾取后光标类型是
`PlantFromUsableCoin`，`IZombieMouseDownWithZombie` 也只对 `PlantFromBank` 扣费。因此可用
卡片掉落物及由罐子开出的可用卡片不受这项费用表缺失影响。

有两个原生/修改器条件可以避开该默认分支：

- 创意关卡的 `CSOverridePlantProperty` 为该精确组合 `SeedType` 设置 `SeedCost`；
- 修改器开启“免费种植”，使 `Plant.GetCost` 或 `Board.GetCurrentPlantCost` hook 直接返回 0。

这只是费用问题的规避方式，不代表所有特殊僵尸都完整支持卡片放置。

## 6. 特殊僵尸仍需实机验证

`Challenge.IZombiePlaceZombie` 对所有类型统一调用 `Board.AddZombieInRow`，只对
`ZombieType.Bungee` 单独设置目标列和坐标。相比 `placer._ZombieOnBoard`，它没有为雪橇车
小队的跟随成员同步新的横坐标；魅惑 flag 也只对返回的主僵尸调用一次
`StartMindControlled`。僵王、雪橇小队、伴舞、内部缓存类型等依赖额外关系或关卡状态的
类型，不能仅凭“成功创建对象”认定行为完整。

建议至少按以下维度验证：

1. 普通和魅惑各一张；
2. 普通关卡、我是僵尸关卡和创意关卡各一次；
3. 卡槽与可用卡片掉落物两条入口；
4. 支持费用表的普通僵尸、蹦极僵尸，以及不支持费用表的旗帜/雪橇/新僵尸各一类；
5. 放置预览、阳光扣除、冷却、存档重进、铲除/死亡和关卡结束。

## 7. 反编译源码导航

本结论主要来自同级 `PGvZ-decompilation-1.3.0` 和
`PGvZ-decompilation-1.3.1` 目录；1.3.1 相关修复集中在下表标注的三个文件：

| 文件 | 重点方法 |
|---|---|
| `Lawn/SeedType.cs` | 两个 flag 的数值 |
| `Lawn/Challenge.cs` | `IsZombieSeedType`、`IZombieSeedTypeToZombieType` 的 1.3.1 `None` 防护，以及 `CanPlantAt`、`IZombieMouseDownWithZombie`、`IZombiePlaceZombie` |
| `Lawn/Board.cs` | `CanPlantAt`、`MouseUpWithPlant`、`AddPlant`、`NewPlant`、`GetCurrentPlantCost` |
| `Lawn/Plant.cs` | `PlantInitialize`、`GetPlantDefinition`、`GetCost`、`GetRefreshTime`、`DrawSeedType` |
| `Lawn/SeedPacket.cs` | 卡片绘制、名称、费用、拾取和 `SetPacketType` |
| `Lawn/CursorObject.cs`、`Lawn/CursorPreview.cs` | 光标与落点预览 |
| `Lawn/SeedTypeConvertor.cs` | 创意关卡 20000/30000 编码及 1.3.1 的 `None -> -1` 防护 |
| `Lawn/GlobalMembersSaveGame.cs` | `SeedTypeSaver` 的 `+`/`-` 名称格式及 1.3.1 的 `None` 正常名称 |
| `Lawn/SeedTypeLegacy.cs` | 旧加载路径的数组下标限制 |
