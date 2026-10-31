# 格内植物分类、种植检查与僵尸选靶

本文依据本地 PGvZ 1.3.0、1.3.1 反编译源码，记录 `PlantsOnLawn`、
`Board.GetPlantsOnLawn`、`Board.GetTopPlantAt` 及相关种植、攻击机制。
文中列出的核心查询、种植、选靶方法在这两个版本中实现一致。
仓库还支持 1.3.2–1.3.4，但本地没有这些版本的完整反编译目录，本文未核对其实现。
以下描述均指游戏原生逻辑；修改器绕过种植检查的影响见第 8 节。

## 1. 数据模型：查询时生成的四槽结果

场上植物保存在 `Board.mPlants`（`List<Plant>`）中。
`PlantsOnLawn` 是含四个 `Plant` 引用的 C# 结构体，不是每格常驻的缓存，
也不直接保存 `SeedType` 或同格植物列表。
`GetPlantsOnLawn(x, y, ref result)` 每次清空结果，再遍历 `mPlants`，
把符合条件的植物引用放入对应槽位。

| 字段 | 分类规则（普通战斗场景） |
|---|---|
| `mUnderPlant` | 花盆 `Flowerpot`、睡莲 `Lilypad` |
| `mPumpkinPlant` | 南瓜壳 `Pumpkinshell` |
| `mFlyingPlant` | `Plant.IsFlying(effectiveType)` 为真；已核对版本中只有咖啡豆 `InstantCoffee` |
| `mNormalPlant` | 上述分类之外的植物，包括香蒲、魅惑香蒲、火红莲、玉米炮等 |

这里的“飞行”是植物种类分类，与 `NotOnGround()` 的临时离地状态是两套概念。
咖啡豆属于飞行槽，但不因此必然满足 `NotOnGround()`；跳起的窝瓜则会被查询过滤，
不会改归飞行槽。仙人掌等植物也不会因动画或外观变化改归飞行槽。

禅境花园 `GameMode.ChallengeZenGarden` 是一个例外：睡莲归 `mNormalPlant`，
花盆仍归 `mUnderPlant`。分类条件直接比较这个游戏模式，不是比较花园背景或水池地形。

四个槽位每个最多返回一株。源码在赋值前用 `Debug.ASSERT(slot == null)`
检查同槽冲突；`Sexy.Debug.ASSERT` 失败只记录错误日志，随后仍赋值。
因此强制重叠种植时，同槽中**后遍历到的植物覆盖先前结果**，其余植物仍在
`mPlants` 里。这个结构不能用来枚举修改器制造的同槽多株植物。

## 2. `GetPlantsOnLawn` 如何判断一株植物占哪一格

查询坐标是零基的 `(列 x, 行 y)`。流程依次为：

1. 将四个槽位全部置 `null`，包括调用方传入的已有结果。
2. 检查 `0 <= x < Constants.GRIDSIZEX`、`0 <= y < Constants.MAX_GRIDSIZEY`。
   已核对版本的常规常量为 9 列、6 行；这里没有另查当前关卡实际可用行或格子地形。
3. 坚果保龄球关卡中，除铲子教学期间外，直接返回四槽皆空。
4. 按索引顺序遍历 `mPlants`，跳过 `mDead` 的植物。
5. 计算本次分类所用的有效类型：通常是 `mSeedType`；若是普通模仿者
   `Imitater` 且 `mImitaterType != SeedType.None`，改用 `mImitaterType`。
   这一步不修改对象本身的 `mSeedType`，也不适用于随机植物/随机僵尸模仿者。
6. 检查格子归属。普通植物必须满足 `mPlantCol == x && mRow == y`；
   有效类型为玉米炮时，允许查询其左格或右格：
   `mRow == y && mPlantCol <= x && x <= mPlantCol + 1`。
7. 过滤 `NotOnGround()`，但保留“禅境花园中被手套抓住”的植物。
8. 按有效类型填入第 1 节的四槽之一。

因此，未完成变身的模仿睡莲、模仿花盆、模仿南瓜和模仿咖啡豆，已经按目标类型占槽。
但后续调用者若直接比较返回对象的 `mSeedType`，看到的仍可能是 `Imitater`。
“归入睡莲槽”和“已经可以作为睡莲使用”并不等价。

玉米炮的两格查询返回**同一个 `Plant` 对象**，其 `mPlantCol` 始终是左格。
这只是查询时扩展覆盖范围，不是创建两株植物或把右格也保存为独立坐标。
对两格分别查询后做计数、伤害或删除时，需要避免重复处理同一个对象。

查询不按 `mX/mY`、绘制顺序或鼠标碰撞框判断占格，也不排除沉睡、禁用、
残血、处于普通冷却或被符咒封印的植物。墓碑、弹坑、罐子、梯子等也不属于四槽，
它们由其他查询单独处理。

### `NotOnGround()` 的具体条件

`Plant.NotOnGround()` 在下列任一条件成立时返回真：

| 条件 | 相关字段或状态 |
|---|---|
| 被手套抓住 | `mGloveGrabbed` |
| 墓碑吞噬者正在吃墓碑 | `Gravebuster` + `GravebusterEating` |
| 窝瓜已经起跳、下落、落地结束或进入彩蛋准备 | `SquashRising`、`SquashFalling`、`SquashDoneFalling`、`SquashCaidanInReady` |
| 已被压扁或已死亡 | `mSquished`、`mDead` |
| 正随蹦极上升 | `mOnBungeeState == RisingWithBungee` |
| 辣椒火焰阶段 | `mState == JalapenoFwoosh` |
| 魅惑菇、钢地刺或地刺处于特殊效果阶段 | 对应种类 + `Doingspecial` |
| 植物处于死亡状态 | `mState == Dying` |
| 巨型坚果 | `mSeedType == GiantWallnut` |

`GettingGrabbedByBungee` 尚不算离地，仍出现在格内查询结果里；
到 `RisingWithBungee` 才通常从结果消失。种植检查会另外排除部分正在被抓住的底座、
升级材料和修补目标。

禅境花园的手套例外精确写成：

```csharp
if (plant.NotOnGround()
    && (!plant.mGloveGrabbed || mApp.mGameMode != GameMode.ChallengeZenGarden))
    continue;
```

所以这不是全局改变 `NotOnGround()` 的含义，只是这一次格内查询的例外。

## 3. `GetTopPlantAt` 的“最上层”由用途决定

`GetTopPlantAt(x, y, priority)` 先做边界、保龄球模式检查，再调用
`GetPlantsOnLawn`，按照 `TopPlant` 返回第一个非空槽位；找不到就返回 `null`。
它不按屏幕高度或绘制顺序求“最上层”，也不检查指定僵尸能否攻击返回对象。

下表中 F、P、N、U 分别代表飞行、南瓜、普通、底座槽；箭头表示从左到右取首个非空项。

| `TopPlant` | 值 | 返回规则 | 主要用途 |
|---|---:|---|---|
| `EatingOrder` | 0 | P → N → U | 啃食层级、普通僵尸豌豆碰撞、松鼠吃植物 |
| `DiggingOrder` | 1 | N → U | 普通鼠标选植物、融合候选 |
| `BungeeOrder` | 2 | F → N → P → U | 蹦极选格与抓取 |
| `CatapultOrder` | 3 | F → N → P → U | 投篮目标、部分弹丸碰撞 |
| `ZenToolOrder` | 4 | F → P → N → U | 禅境花园工具选取 |
| `Any` | 5 | F → N → P → U | 判断是否有可查询植物等 |
| `OnlyNormalPosition` | 6 | 仅 N | 主体植物、升级材料、拼图目标等 |
| `OnlyFlying` | 7 | 仅 F | 咖啡豆层 |
| `OnlyPumpkin` | 8 | 仅 P | 南瓜修补、保护层检查等 |
| `OnlyUnderPlant` | 9 | 仅 U | 底座查询、花园关联处理 |

`BungeeOrder`、`CatapultOrder`、`Any` 在已核对版本中的返回顺序相同。
`Any` 仍受第 2 节过滤条件约束；返回 `null` 不代表 `mPlants` 中没有对象。
`EatingOrder` 不返回飞行槽，`DiggingOrder` 不返回南瓜和飞行槽。

例如同格有“睡莲 + 沉睡蘑菇 + 南瓜 + 咖啡豆”时，查询结果分别为：

| 查询 | 返回 |
|---|---|
| `EatingOrder` | 南瓜 |
| `DiggingOrder` / `OnlyNormalPosition` | 蘑菇 |
| `BungeeOrder` / `CatapultOrder` / `Any` / `ZenToolOrder` | 咖啡豆 |
| `OnlyUnderPlant` | 睡莲 |

这只说明查询结果，实际操作仍有下文的资格检查和执行逻辑。

## 4. 格内分类怎样参与种植判定

`Board.CanPlantAt(x, y, type, aIsMovePlant=false)` 返回 `PlantingReason`。
它检查的是位置及植物组合是否合法，阳光、卡片冷却、工具是否可用等由外层流程检查。
不能用“普通槽为空”替代这个方法。

### 4.1 检查顺序与提前返回

主要顺序如下；前面的分支可能提前返回，不能把后面的限制理解为始终生效：

1. 边界检查；调用 `Challenge.CanPlantAt` 检查模式区域限制。
   若模式检查失败或传入僵尸种子类型，直接返回模式检查结果。
2. 调用 `GetPlantsOnLawn`。禅境花园要求四槽全空；水族馆还要求水生植物，随后返回。
3. 检查辣椒封印倒计时、格子符咒。
4. 墓碑吞噬者单独要求普通槽为空且格内有墓碑。
   咖啡豆单独要求飞行槽为空、普通槽存在沉睡植物、唤醒倒计时不大于 0，且主体没有正在被蹦极抓住。
5. 其他种类若遇墓碑，飞行植物直接允许，其他种类返回 `NotOnGrave`。
6. 用 `DiggingOrder` 选融合底材；若 `Plant.GetValidFusion(base.mSeedType, type)`
   有有效结果，直接允许。该方法也检查关卡是否启用融合。
7. 计算可用睡莲、花盆支撑，再检查弹坑、罐子、冰道、不可用地块等。
   遇弹坑时也是飞行植物直接允许，其他种类返回 `NotOnCrater`。
8. 处理水生植物、飞行层、地刺、水面支撑、花盆、屋顶支撑、南瓜、升级和修补等规则。

例如，融合成功分支位于弹坑、冰道、地形和普通占位检查之前。
这描述的是源码执行顺序，不等于在任何状态下都能把两个植物叠在一起；
前面的模式限制、符咒和特定种类分支仍可能先拒绝。

### 4.2 各槽的具体作用

| 情形 | 使用四槽的方式 |
|---|---|
| 睡莲、缠绕海草、海蘑菇；搬运中的香蒲/魅惑香蒲 | 要求水池格或浅水格，且 N、U 都空；这一分支不要求 P、F 为空 |
| 普通飞行植物分支 | 要求 F 为空；咖啡豆通常已在前面的专门分支处理 |
| 种花盆 | 要求 N、U、P 为空，不检查 F |
| 种南瓜 | N 不能是玉米炮；P 为空可种，否则检查南瓜修补条件 |
| 普通植物 | N 为空才进入空位种植；N 非空则尝试升级、融合或同种修补 |
| 种香蒲 | 非搬运时优先检查 U 能否升级为香蒲，同时要求 N 为空 |
| 未变身的底座模仿者 | 虽已占 U，但不会立即视为可用睡莲/花盆；普通路径另拒绝 U 的原始类型为 `Imitater` 或 `ImitaterRandomPlant` 的情况 |

水池格通常需要未被蹦极抓住的睡莲 U。种香蒲、在普通香蒲上种南瓜有专门例外；
代码对这里的普通香蒲直接比较 `SeedType.Cattail`，不能自动推广至魅惑香蒲。
睡莲支撑也不允许土豆雷、火红莲种在其上。

屋顶通常需要未被蹦极抓住的花盆 U；普通槽里的火红莲 `Endoflame`
也会被视为屋顶支撑，而火红莲本身可免花盆。
这不会把火红莲改归 U，也不自动免除 N 占位冲突。
地刺、钢地刺另受 `NeedsGround` 限制：不能在水池地块、屋顶场景或已有 U 的格子种植。

正常升级由 `Plant.IsUpgradableTo` 判定；修补还要求未使用搬运模式、购买对应能力、
同种且血量严格小于 `mPlantMaxHealth * 2 / 3`（整数计算），目标没有正在被蹦极抓住。
普通槽修补覆盖坚果、高坚果、火蘑菇 `FireShroom`、大蒜；南瓜在 P 上单独修补。
`mEasyPlantingCheat` 或创意关卡 `EasyUpgrade` 只放宽相应分支，不是全方法无条件允许。

### 4.3 玉米炮的双格与实际替换

`IsValidCobCannonSpot(x, y)` 同时检查左右两格：

- 每格 P 必须为空；通常 N 必须是玉米投手 `Kernelpult`。
- 宽松升级时，N 不是玉米投手的格子改用 `CanPlantAt(..., Kernelpult)` 检查。
- 两格是否有花盆必须一致，使用 `GetFlowerPotAt` 单独判断。
- 搬运玉米炮走 `IsValidCobCannonSpotMovePlant`：两格均须允许放玉米投手，
  并同样要求两格花盆有无一致。

`MouseDownWithPlant` 随后才执行替换：升级/融合会移除原普通植物，
种玉米炮还会移除右格的普通植物；种香蒲会清理查询到的 U 和 N。
所以 `CanPlantAt` 是资格检查，植物的删除、新建和搬运由后续逻辑负责。
香蒲本身属于 N，原睡莲被消耗后不会以 U 继续留在下面。

## 5. 僵尸攻击：先查碰撞，再做资格和层级检查

### 5.1 普通啃食的调用链

```text
Zombie.CheckIfPreyCaught（状态、攻击节拍、魅惑等前置条件）
  → FindPlantTarget(Chew)
      → 遍历 mPlants：未死亡、同行、攻击框与植物框横向重叠达标
      → CanTargetPlant(candidate, Chew)
          → 状态/种类/水面/特殊攻击检查
          → GetTopPlantAt(candidate.mPlantCol, candidate.mRow, EatingOrder)
          → 必要时递归检查更高优先级对象
  → EatPlant(target)（梯子、特殊效果、伤害等）
```

`FindPlantTarget` 返回列表顺序中第一个通过条件的植物，不是先把僵尸坐标转成某格，
再直接吃该格的顶层。一般要求 `GameConstants.GetRectOverlap >= 20`；
矿工僵尸阈值为 5。`GetRectOverlap` 只比较 X 区间，返回有符号的横向重叠长度，
不计算二维相交面积；行由外层单独检查。
玉米炮的 `GetPlantRect()` 是 `(mX, mY, 140, 80)`，与它占两格的逻辑相配合，
但碰撞框与格内归属仍是两个不同判定。

在 `CanTargetPlant` 的普通 Chew 层级分支中：若 `EatingOrder` 返回另一株植物，
并且那株植物也能被当前攻击类型选中，则拒绝当前候选。
因此通常按“南瓜 → 主体 → 底座”挡住下一层；
如果更高优先级植物不能被该僵尸选中，则不会仅凭其存在挡住当前候选。
递归资格检查本身不重新检查攻击框是否与更高层重叠。

`GetTopPlantAt(EatingOrder)` 不返回咖啡豆，但 `FindPlantTarget` 仍遍历全部植物，
`CanTargetPlant` 也没有通用的 `Plant.IsFlying` 排除项。
不能仅据优先级表推断“飞行槽绝不会被啃食”；仍需结合候选状态、其他层资格与碰撞条件。

### 5.2 `CanTargetPlant` 的特殊分支

下列检查位于普通层级判断之前，部分分支直接返回，因而并非所有目标都走层级抑制：

| 条件 | 行为 |
|---|---|
| 保龄球关卡 | 除 `Vault` 外拒绝 |
| `NotOnGround()` | 拒绝 |
| `mInTalismanCounter > 0` | 除 `DriveOver` 外拒绝 |
| 缠绕海草、随机僵尸模仿者 | 直接拒绝 |
| 僵尸不在水中，候选位于水池格 | 拒绝 |
| 矿工处于 `DiggerTunneling` | 只接受实际类型为土豆雷且 `mState == Notready` 的植物，直接返回 |
| `IsSpiky()` 的植物 | 巨人、红眼巨人、冰车直接接受；其他僵尸在水池格接受，在非水池格仅当有花盆时接受，直接返回 |
| `DriveOver` 遇樱桃、辣椒、三叶草、窝瓜、泡椒、毁灭菇、寒冰菇 | 返回 `plant.IsDisabled()`，直接结束资格检查 |
| 梯子僵尸搬梯/放梯阶段 | 没有梯子的坚果、高坚果、南瓜走搭梯目标；`Chew` 拒绝这些搭梯目标，`Ladder` 拒绝其他目标 |

这里大量种类判断使用原始 `mSeedType`，与四槽分类所用的模仿者有效类型不同。
`GettingGrabbedByBungee` 没有通用的攻击免疫；其是否仍可被攻击不能只看蹦极已开始抓取。

跳跃攻击 `Vault` 的层级检查使用 `OnlyNormalPosition`，不是 `EatingOrder`：
若同格 N 是另一株可作为跳跃目标的植物，就拒绝当前候选。
因此跳跃障碍选择与普通啃食层级不同。
`DriveOver`、`Ladder` 不执行 Chew/Vault 的这两段层级抑制。

即使 `CanTargetPlant` 返回真，也不等于必然扣血。例如 `EatPlant` 还能处理已有梯子，
让非矿工停止啃食并转入爬梯；植物的特殊效果和初始无敌状态也由执行阶段继续处理。

### 5.3 巨人砸击、碾压与格内批处理

巨人用 `FindPlantTarget(Chew)` 决定是否开始砸击，在命中动画时再次查询。
除钢地刺特殊处理外，随后调用 `SquishAllInSquare`，不是只伤害查询得到的一株。
`CheckSquish` 也先通过碰撞和资格检查找到触发目标，再调用该方法。

`SquishAllInSquare(x, y, attackType)` 直接遍历 `mPlants`，按
`mPlantCol == x && mRow == y` 处理同格植物，不再按四槽或 `EatingOrder`
逐层筛选，也不逐株重新调用 `CanTargetPlant`。
钢地刺始终跳过，`DriveOver` 还跳过其他 `IsSpiky()` 植物；
具体 `Plant.Squish()` 内部仍会拒绝离地植物，并可能触发爆炸等特殊效果。

注意这里按植物锚点列匹配，没有复用玉米炮覆盖右格的规则。
从 `FindPlantTarget` 获得玉米炮时调用方传的是其左格锚点；
其他直接按场地格坐标调用的路径不能自动认为右格也会匹配该炮。

## 6. 蹦极、投篮与弹丸碰撞

### 蹦极抓取

蹦极选格和 `BungeeStealTarget` 使用 `BungeeOrder`，因此通常先选咖啡豆、
再选主体、南瓜、底座。抓取时另检查 `!NotOnGround()`，并明确拒绝实际类型为玉米炮的对象。
这一阶段不因首选对象不合格就自动依次重试其他槽位。

抓住时设置 `GettingGrabbedByBungee`，对象仍可出现在四槽查询中；
`BungeeLiftTarget` 改为 `RisingWithBungee` 后，它才被通常的格内查询过滤。
若提走的是香蒲或魅惑香蒲，且格内仍有南瓜，会新建睡莲，避免留下无底座的南瓜。
莴苣伞防护另见 [莴苣伞防护范围](umbrella-coverage.md)。

### 投篮与弹丸命中

`Zombie.FindCatapultTarget` 遍历同排、未死亡、未离地、非尖刺植物，
要求目标在自身左侧至少 100 像素，并选较小的植物列；
再用该格 `CatapultOrder` 决定最终瞄准对象。
所以同格有主体和南瓜时，瞄准主体优先；有咖啡豆则咖啡豆更优先。
候选筛选与按槽取最终对象是两个步骤，不是用 `CanTargetPlant(Chew)` 选投篮目标。

`Projectile.FindCollisionTargetPlant` 也先遍历植物寻找同行、横向重叠 `> 8` 的候选，
再按该候选格子重新取目标：

- 普通 `ZombiePea` 使用 `EatingOrder`，通常先打南瓜。
- 其他进入该方法的弹丸使用 `CatapultOrder`；包括 `ZombiePeaMindControl`，
  它不走普通僵尸豌豆的最终返回分支。
- 两类僵尸豌豆都先跳过小喷菇、阳光菇、土豆雷、地刺、钢地刺、睡莲候选；
  花盆候选还能受创意关卡 `AllowZombiePeaAttackFlowerPot` 控制。

这些前置排除作用于遍历候选，最终返回的是同格优先级查询结果。
该方法没有直接复用 `CanTargetPlant`，不能把近战种类免疫直接套给所有弹丸。
完整子弹更新和碰撞流程见 [子弹机制](projectiles.md)。

## 7. 铲子与鼠标选取为何不是只看 `DiggingOrder`

`Board.MouseHitTestPlant` 首先执行 `SpecialPlantHitTest`，
给南瓜边缘和咖啡豆提供专门的鼠标命中区域，然后才按格调用优先级查询：

- 南瓜以 `(mX + 40, mY + 40)` 为中心。格内有 N 时，要求距离在 25–50 内；
  无 N 时内半径为 0；还要求鼠标 `y > mY + 25`。
  因此即使 `DiggingOrder` 不返回南瓜，仍可点击南瓜外缘选中它。
- 实际类型满足 `Plant.IsFlying` 的植物，以 `(mX + 40, mY)` 为中心，距离 `< 15` 可命中。
- 普通场景后备查询用 `DiggingOrder`。若结果为睡莲/花盆且同格还有南瓜，
  会清掉这次后备命中，避免绕过南瓜直接选中底座。
- 禅境花园后备查询用 `ZenToolOrder`，浇水壶还会尝试偏移位置处的可浇水目标。

特殊鼠标命中直接遍历原始对象，使用原始类型和像素位置，不能简单由四槽结果替代。
工具入口 `ToolHitTest` 还会在非花园场景排除墓碑吞噬者。

## 8. 对 TAS、修改器和后续调查的含义

- 查询单格的分类结果用 `GetPlantsOnLawn`；只取某种用途的一个对象用 `GetTopPlantAt`。
  读取种类时区分原始 `mSeedType` 与模仿目标，且两格玉米炮需按对象去重。
- 判断能否正常落卡用 `CanPlantAt`，并保留外层阳光、卡片和工具检查。
  `pgvz/card.py` 的卡片逻辑已调用该原生位置检查。
- 判断僵尸当前近战目标要结合 `FindPlantTarget`、`CanTargetPlant` 和执行阶段；
  某格 `EatingOrder` 的返回值本身不足以证明僵尸下一次攻击会伤害谁。
- `pgvztool/overlay.py` 的 `DrawPlantHpAll` 保留逐格查询：先绘制 `EatingOrder`
  目标，再绘制与之不同的 `CatapultOrder` 目标。若 `EatingOrder` 为空，则特判查询
  `OnlyFlying`，让单独存在的咖啡豆受伤后也能显示橙色血条；它仍可被普通僵尸啃食。
  玉米炮只在左格绘制一次长血条；左格有南瓜时由 `CatapultOrder` 绘制上方血条，
  左格无南瓜而右格有南瓜时也改画上方绿色血条，避免下方长条覆盖南瓜血条。
- 修改器“随意种植”在 `pgvztool/hook.py` 的 Board/Challenge 两个
  `CanPlantAt` hook 中直接返回 `Ok`；`pgvztool/placer.py` 的直接放置路径使用 `AddPlant`。
  这些路径可能制造同槽重叠，但没有把 `PlantsOnLawn` 扩展为多株容器。
- 单次格内查询会遍历全部植物，时间复杂度为 O(场上植物数)。
  僵尸遍历候选时又可能发起格内查询和递归资格检查；大规模读取时不能把它当成常数时间数组访问。
- 四槽结构体只是查询结果。修改其中引用不会自动移动或删除场上植物；
  通过引用访问到的 `Plant` 则仍是原游戏对象。脚本访问和操作游戏对象应在游戏主线程进行。

## 9. 反编译源码导航

本地目录为 `E:\programming\PGvZ\PGvZ-decompilation-1.3.0` 和
`E:\programming\PGvZ\PGvZ-decompilation-1.3.1`。
下表行号对应 1.3.1，后续版本应按方法名重新定位。

| 文件 | 入口（1.3.1 行号） | 核对内容 |
|---|---|---|
| `Lawn/PlantsOnLawn.cs` | 3 | 四字段结构体 |
| `Lawn/TopPlant.cs` | 3 | 查询优先级枚举 |
| `Lawn/Board.cs` | `GetPlantsOnLawn` 6926、`GetTopPlantAt` 6819 | 分类、模仿者、玉米炮覆盖、优先级 |
| `Lawn/Plant.cs` | `IsFlying` 2897、`NotOnGround` 3593 | 飞行层与离地过滤 |
| `Lawn/Board.cs` | `CanPlantAt` 3110、`MouseDownWithPlant` 5973 | 种植资格和实际替换 |
| `Lawn/Challenge.cs` | `CanPlantAt` 1612 | 关卡模式的种植区域约束 |
| `Lawn/Plant.cs` | `IsUpgradableTo` 6926、`GetValidFusion` 6981 | 升级与融合 |
| `Lawn/Board.cs` | `IsValidCobCannonSpot` 11386 及后续两个辅助方法 | 玉米炮双格条件 |
| `Lawn/Zombie.cs` | `CheckIfPreyCaught` 1459、`FindPlantTarget` 2966、`CanTargetPlant` 7033、`EatPlant` 1505 | 近战调用链、资格和伤害执行 |
| `Lawn/Plant.cs`、`Lawn/GameConstants.cs` | `GetPlantRect` 3301、`GetRectOverlap` 722 | 植物框和横向重叠 |
| `Lawn/Zombie.cs` | `CheckSquish` 2984、`SquishAllInSquare` 8033、`UpdateZombieGargantuar` | 碾压和整格砸击 |
| `Lawn/Zombie.cs` | `BungeeStealTarget` 4739、`BungeeLiftTarget` 11459、`FindCatapultTarget` 7191 | 蹦极、投篮 |
| `Lawn/Projectile.cs` | `FindCollisionTargetPlant` 1429 | 弹丸重新选择格内受击层 |
| `Lawn/Board.cs` | `SpecialPlantHitTest` 11071、`MouseHitTestPlant` 13144、`ToolHitTest` 11102 | 特殊命中和工具选取 |
| `Sexy/Debug.cs` | `ASSERT` 29 | 同槽冲突只记录日志，赋值继续 |

已逐方法对比两个版本的 `GetPlantsOnLawn`、`GetTopPlantAt`、`Board.CanPlantAt`、
三个玉米炮位置检查方法、`SpecialPlantHitTest`、`MouseHitTestPlant`、`NotOnGround`、
`IsFlying`、`IsUpgradableTo`、`GetValidFusion`、`GetPlantRect`、`FindPlantTarget`、
`CanTargetPlant`、`SquishAllInSquare`、`BungeeStealTarget`、`BungeeLiftTarget`、
`FindCatapultTarget`、`FindCollisionTargetPlant`，方法体一致。
本文是源码调查结论，未进行游戏内逐项实测。
