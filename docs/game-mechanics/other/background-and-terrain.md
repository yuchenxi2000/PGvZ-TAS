# 场景、格子地形与行类型

依据本地 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3` 静态核对，未在游戏中实测中途切换。
以下说明原生行为；修改器“随意种植”等选项可以绕过部分检查。

## 三个独立字段

| 字段 | 范围 | 主要用途 |
|---|---|---|
| `Board.mBackground` | 整个场地 | 背景图、昼夜、五/六行、屋顶、泳池及部分模式条件 |
| `Board.mGridSquareType[col, row]` | 单个格子 | 种植限制、局部水面、高地高度及碰撞 |
| `Board.mPlantRow[row]` | 整行 | 是否允许出怪、可刷僵尸类型、部分泳池行为与绘制 |

三者都是字段。直接赋值不会调用初始化，也不会自动同步另外两个字段。
`PickBackground()` 在关卡初始化时设置背景、加载背景资源、填写行类型，再据此填写特殊格子，
还会初始化墓碑等内容；不能把它视为无副作用的地形同步接口。

## 修改背景

下列方法直接读取当前 `mBackground`，下一次调用即使用新值：

- `StageIsNight()`：夜间包括黑夜、雾夜、高地、僵王、水族馆、蘑菇园和夜间温室。
- `StageHasPool()`：泳池、雾夜和大泳池；不会扫描格子数组。
- `StageHas6Rows()`：泳池、雾夜、高地和大泳池；不会扫描行类型数组。
- `StageHasRoof()`：屋顶和僵王场景。
- `StageHasFog()`、`StageHasGraveStones()`：还结合游戏模式或创意关卡组件。

因此背景修改会影响格子与像素坐标换算、鼠标选格、新对象定位、屋顶花盆要求、
部分弹道和地形高度计算、自然掉落阳光、植物初始化时的昼夜睡眠判断及阴影绘制等。
例如常规自然阳光流程在 `StageIsNight()` 为真时停止，显式创意关卡组件可覆盖该条件。

`DrawBackdrop()` 根据当前背景选择图片，但赋值本身不会加载资源。
`LoadBackgroundImages()` 负责资源加载，不能代替地形数组和现有对象状态的同步。
背景赋值也不会统一重建遮挡层、割草机、现有墓碑或植物。
已有蘑菇的 `mIsAsleep` 是独立状态，不能把背景赋值当作全场睡眠/唤醒接口。

## 修改格子地形

`GridSquareType` 包括 `None`、`Grass`、`Dirt`、`Pool`、`HighGround`、`Shallow`。

- `CanPlantAt()` 的地形检查分支拒绝 `Dirt`、`None`。
- 水生植物可种在 `Pool` 或 `Shallow`；普通植物在 `Pool` 通常需要睡莲，浅水不走同一限制。
- 地刺、钢地刺受泳池格、屋顶及底座限制。
- `IsPoolSquare()` 直接读取格子是否为 `Pool`，不要求 `StageHasPool()` 为真。
- `GridToPixelY()` 对高地格额外减去高地高度；植物、僵尸和子弹也有高地判定。
- `Projectile.CheckForHighGround()` 可能令不能命中高地的弹丸撞地；
  发射时的 `mOnHighGround` 又是初始化保存的状态，中途改格子不会统一重置已有子弹。
- 符合条件的僵尸在 `CheckForPool()` 中重新检查脚下格子，触发入水或出水。
  潜水、海豚、飞行等类型和过渡状态有专门的排除条件，不能认为所有僵尸立即统一转换。

改格子不会把背景图绘制成相应地形，也不会修改该行的出怪资格。
已有植物不会因为赋值而重新执行 `PlantInitialize()` 或普通种植检查。

### `None` 格子的具体含义

`GridSquareType.None` 是枚举值 0，不代表删除格子或创建会令单位掉落的洞。
当前 1.4.3 的普通种植地形检查将它与 `Dirt` 一起返回 `PlantingReason.NotHere`；
咖啡豆、墓碑吞噬者等提前返回的特殊分支仍按自身条件处理，“随意种植”可绕过检查。
设为 `None` 不会直接移除已有植物、修改行类型或禁用整行出怪；也不是泳池或高地。
画面仍由背景决定，不会因单格设为 `None` 自动画出空洞。

`CanAddGraveStoneAt()` 只接受草地或高地，因此 `None` 不能通过原生墓碑放置检查。
天尸生成固定符咒的候选格同样排除 `None` 和 `Dirt`。
两者并非完全等价：`Zombie.PickBungeeZombieTarget()` 的这条地形过滤仅排除 `Dirt`，
没有排除 `None`，所以不能依靠 `None` 让格子免受蹦极选中。

## 原生浅水关卡

1.4.3 的 `PickBackground()` 将“随机模仿者”（`GameMode.ImitaterRandom = 132`）设为
`BackgroundType.ShallowDay`。该背景初始化前五行为 `PlantRowType.Shallow`，对应九列格子
均为 `GridSquareType.Shallow`；第六行为 `Dirt`。创意关卡也可通过背景配置使用该场景。

`DrawBackdrop()` 中 `ShallowDay` 使用普通白天的 `IMAGE_BACKGROUND1`，所以画面看上去
仍是白天草坪。浅水格允许直接放水生植物，同时不触发普通泳池格的睡莲要求；
`IsPoolSquare()` 只认 `Pool`，不把 `Shallow` 当作普通泳池水面。

## 修改行类型

`PlantRowType` 包括 `Dirt`、`Normal`、`Pool`、`HighGround`、`Shallow`。

- `RowCanHaveZombies()` 通常排除 `Dirt`，重新铺草皮模式存在例外。
- `RowCanHaveZombieType()` 根据泳池/高地行筛选僵尸，结合当前波、背景、模式等条件。
- `PickRowForNewZombie()` 在实际创建僵尸时使用这些条件重新分配各行权重。
- 舞王伴舞位置、部分泳池专属行为、植物阴影、部分弹丸效果也读取行类型。
- 割草机初始化根据屋顶判定和泳池行选择类型；已有割草机不会自动更换动画和类型。

只修改 `mPlantRow[5]` 不会让 `StageHas6Rows()` 返回真；只修改某行为 `Pool` 也不会
让其中所有格子自动成为水面。可能形成种植、选行和画面相互不一致的场地。

## 已生成出怪表与已有对象

新关卡在 `Board.InitLevel()` 中先 `PickBackground()`，再 `InitZombieWaves()`。
后者选择 `mZombieAllowed`，并通过 `PickZombieWaves()` 提前填入本关各波的
`mZombiesInWave`；生存换轮重新执行出怪初始化。详见[出怪种类抽取](../levels/zombie-wave-selection.md)。

直接修改上述三个字段不会重算这两张出怪表。不过 `SpawnZombieWave()` 创建僵尸时
会通过 `AddZombie()` 选择出场行，因此后续刷出的既定僵尸会受新行类型和背景条件影响。
不能由此假定任何已有出怪组合都能在任意新地形中正常运行。

已有对象兼有缓存状态和实时地形查询，不能仅靠三处赋值完成整体迁移：

- 植物初始化时保存像素坐标；直接改地形不会把所有植物重新按格子定位。
- 僵尸后续更新可能响应水面或高地变化，但还受自身类型、阶段、冻结等条件影响。
- 子弹保存发射时的高地状态，后续碰撞又读取当前地形。
- 割草机类型、遮挡动画及其他初始化对象需要分别处理。

即使在选卡期间修改，也已经晚于首次出怪表、地形和部分对象的初始化。
若需要新场景的自然出怪规则，须显式重建出怪表；`InitZombieWaves()` 同时重置当前波号、
首波倒计时等状态，不适合在战斗中当作只更新未来波次的接口。

## 换背景后的植物位置校正

`PlantInitialize()` 通过 `GridToPixelX/Y()` 初始化植物的 `mX/mY`，普通植物随后不会
因为背景或地形字段改变而统一重定位。`Plant.Fire()` 的发射坐标直接使用这些保存的
坐标；子弹初始化的 `mShadowY` 等字段又按当前地形计算。因此跨五/六行、屋顶或高地
修改后，旧植物的发射起点可能与新地形基准不一致。

当前 1.4.3 可复用公开方法 `board.mChallenge.MovePlant(plant, col, row)`，传入植物原来的
`mPlantCol/mRow`，相当于原地重新定位。该方法重算 `mX/mY`、渲染顺序、花盆状态，
同步睡眠/封印动画的位置和顺序、粒子平移，以及龙舌兰特定动画的位置；不会重新初始化
整株植物的血量、攻击计时或睡眠状态。同格调用仍会经过梯子、花盆和火红莲等原生处理。

位置校正应放在新背景及两组地形写入之后。批量处理时应跳过 `NotOnGround()` 的植物，
避免干扰手套抓取、蹦极提走、窝瓜起跳等状态；还需考虑保龄球移动和关卡特殊布置的
自定义偏移，不能把原地移动视作所有模式下都无副作用的通用迁移。该方法在禅境花园
和智慧树模式直接返回；`ZenGarden.MovePlant()` 另有存档和种植特效等副作用。

不要用 `PlantInitialize()` 校正位置：它会重置血量、攻击计时、状态及动画引用等。
`UpdateReanim()` 根据当前条件更新绘制偏移，但不重新计算植物 `mX/mY`，且会调用
`reanimation.Update()` 推进动画，不能把它视作纯位置刷新接口。

校正植物不会迁移已经发射的子弹。僵尸 `UpdateZombiePosition()` 通常按每帧最多一个
单位趋近当前行的新 Y 坐标，蹦极、僵王、墓碑钻出及水族馆等状态有独立分支，
所以中途跨地形转换不能仅凭植物重新定位就保证所有现存对象立刻完全对齐。

## 修改器的地形页

GUI 的“地形”页分别编辑这三个字段，格子按六行九列显示，行类型在右侧与各行对齐。
两组数据共用五种地形画笔；“草地”对格子写入 `Grass`，对行类型写入 `Normal`，其余
类型同名对应，仍独立编辑各自的数组。不提供“无”画笔；已有的 `None` 格子读回时显示为“—”。
矩形选区可跨越地形格子与右侧行类型，松开后一次涂改两部分；点击仍仅设置对应单元格。
未读取时也显示完整编辑器，默认背景为白天，前五行格子为草地、行类型为普通；第六行九格及行类型均为裸地，
可在进入关卡前编辑草稿；无关卡时点击读取返回这套默认设置。
画笔与矩形拖选只修改网页草稿，“实施修改”才在主线程一次性赋值；背景变化时调用
`LoadBackgroundImages()`。它不会调用 `PickBackground()` 或重建出怪、植物、割草机。
两组地形写完后，在有效格子内对存活且未离地的植物调用原生 `Challenge.MovePlant()`
原地校正位置，保留血量、攻击计时和睡眠状态；保龄球关卡跳过，已有子弹不迁移。
只在用户点击“读取当前地形”时读取，不在打开页面、换关或生存换轮时自动读取。
“实施修改”作用于请求执行时的当前 Board，换关后仍可实施保留的草稿，不因关卡变化而报错。
不保存持续设置，不自动向新关卡重放；游戏自身保存当前 Board 或复用 Board 的行为仍按
原生逻辑处理。使用方法见[修改器使用](../../mod/user-guide/install.md#修改器使用)，
消息格式与状态处理见[GUI 协议](../../mod/internals/cheat-gui-protocol.md#地形编辑)。

## 源码导航

- `Lawn/Board.cs`：`PickBackground`、`StageIsNight`、`StageHasPool`、`StageHas6Rows`、
  `StageHasRoof`、`CanPlantAt`、`IsPoolSquare`、`GridToPixelY`、`RowCanHaveZombieType`、
  `PickRowForNewZombie`、`SpawnZombieWave`、`InitZombieWaves`、`LoadBackgroundImages`。
- `Lawn/Plant.cs`：`PlantInitialize`、`Fire`、`UpdateReanim`、`PlantDrawHeightOffset`、`DrawShadow`、`IsOnHighGround`。
- `Lawn/Challenge.cs`：`MovePlant`（原地重新定位及关联特效同步）。
- `Lawn/Zombie.cs`：`CheckForPool`、`CheckForHighGround`、`Update`。
- `Lawn/Projectile.cs`：`ProjectileInitialize`、`CheckForHighGround`。
- `Lawn/LawnMower.cs`：`LawnMowerInitialize`。

坐标的完整说明见[游戏渲染与坐标系统](rendering.md)。
