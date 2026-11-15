# 禅境花园金盏花花色渲染

本文保留旧版禅境花园金盏花全部显示为白色的原因和历史修复，并记录本地 PGvZ 1.4.3
反编译源码核对结果：金盏花改用 Spine 动画后，旧花色着色逻辑已无效，修改器已移除
`ZenGarden.PlacePottedPlant` 花色修复 Hook。本次为静态源码核对，未在游戏中实测。

## 1.4.3：Spine 动画不再应用旧花色

`GameConstants.gLawnReanimationArray` 将 `ReanimationType.Marigold` 配置为
`spanim/marigold`，并设置 `isSpine: true`。`reanim/Marigold` 虽然仍作为旧资源名传入，
但 `ResourceManager.LoadReanimation` 会将定义标记为 `mIsSpine = true`，加载 Spine
骨骼和贴图；它不是一个根据花色自动切回旧绘制器的分支。

旧花色的枚举值、盆栽存档字段和随机生成代码仍然存在：

- `PottedPlant.mDrawVariation` 仍参与存读档；花色枚举仍为 2–12。
- 花园教程赠送金盏花时仍随机设置这些花色值。
- `ReanimatorCache.UpdateReanimationforVariation` 仍只给
  `GetTrackInstanceByName("Marigold_petals").mTrackColor` 赋色。

但是 Spine 动画不再使用旧花瓣轨道绘制：

1. `Reanimation.GetTrackInstanceByName` 在 Spine 下调用 `SpineFindTrackIndex`，后者查找
   的是去掉 `anim_` 前缀后的动画名称，不是旧版花瓣图层；未匹配时返回索引 0。
2. `Reanimation.DrawRenderGroup` 在 `mIsSpine` 为真时直接转入 `DrawSpineGroup`。
3. `DrawSpineGroup` 绘制 Spine 骨骼，并根据 `mColorOverride` 和 Graphics 颜色设置骨骼
   整体 RGBA，没有将旧 `ReanimatorTrackInstance.mTrackColor` 应用到骨骼花瓣。

因此，即使原修复成功调用了 `UpdateReanimationforVariation`，写入轨道实例的颜色也
不会改变新版金盏花的花色。这不表示花色存档数据被删除，也不是原来的“全部白色”
问题已经由同一套着色逻辑修复。当前修改器只移除无效 Hook，不修改存档，也不替换
Spine 动画或实现新的着色方式。

内置公告将金盏花娘化列在 1.4.0；本次没有完整的 1.4.0–1.4.2 源码作逐版对照，
具体实现结论以已核对的 1.4.3 为准。

## 旧版：数据与颜色范围

禅境花园盆栽保存在 `PlayerInfo.mPottedPlant` 中。每个 `PottedPlant` 的
`mDrawVariation` 记录绘制变种；金盏花使用 `DrawVariation.MarigoldWhite` 至
`DrawVariation.MarigoldLightGreen`（枚举值 2 至 12），共 11 种花色。

`ReanimatorCache.UpdateReanimationforVariation` 是游戏应用绘制变种的统一入口。对于上述
金盏花变种，它会把对应颜色写入 `Marigold_petals` 动画轨道。商店、掉落物、手推车等
静态盆栽图标经 `ZenGarden.DrawPottedPlant` 调用 `Plant.DrawSeedType`，会传入
`mDrawVariation`，因此这些位置能够正常显示花色。

## 旧版：场上植物丢失花色的原因

进入禅境花园时，`ZenGarden.ZenGardenInitLevel` 会通过
`ZenGarden.PlacePottedPlant` 把盆栽存档逐个实例化为场上的 `Plant`。旧版
实现会设置金盏花的动画和生长阶段，却没有将 `PottedPlant.mDrawVariation` 应用到新建的
`Plant.mBodyReanimID`。场上的植物由 `Plant.Draw` 直接绘制这份动画，所以花瓣沿用资源的
默认白色。

## 历史模组修复（已移除）

旧修改器曾在 `pgvztool/hook.py` 的 `ZenGarden.PlacePottedPlant` 原方法返回后执行以下处理：

1. 只处理已经长成金盏花的场上植物；幼苗仍按游戏原逻辑绘制。
2. 由盆栽索引重新取得对应的 `PottedPlant`。
3. 确认变种位于金盏花花色范围内。
4. 取得新植物的身体动画，并调用游戏自身的
   `ReanimatorCache.UpdateReanimationforVariation` 应用花色。

选择 `PlacePottedPlant` 而不是更小的动画辅助方法作为钩点，是因为它覆盖首次进入花园、
切换花园、移动或重新加载盆栽等实例化路径，而且方法体较大，不易因运行时内联而绕过
钩子。该修复不修改存档，只恢复已有 `mDrawVariation` 数据的显示。历史问题记录覆盖
游戏 v1.0.1 至 v1.2.6；1.4.3 已不适用，代码已删除，本文保留作为旧版机制说明。

## 升级游戏版本时的核对项

- `ZenGarden.PlacePottedPlant` 是否仍返回新建的场上 `Plant`。
- 场上植物是否仍通过 `Plant.mBodyReanimID` 绘制。
- `ReanimatorCache.UpdateReanimationforVariation` 是否仍负责设置
  `Marigold_petals` 的轨道颜色。
- 金盏花变种枚举范围是否仍为 `MarigoldWhite` 至 `MarigoldLightGreen`。
- 动画是否已切换为 Spine，以及实际绘制路径是否消费旧轨道的 `mTrackColor`；
  仅保留同名方法和枚举不能证明旧修复仍有效。

## 1.4.3 反编译源码导航

以下路径相对于 `E:\programming\PGvZ\PGvZ-decompilation-1.4.3`：

| 文件 | 重点 |
|---|---|
| `Lawn/GameConstants.cs` | 金盏花的 Spine 动画资源配置。 |
| `Sexy/ResourceManager.cs` | `LoadReanimation` 明确启用 Spine。 |
| `Lawn/ZenGarden.cs` | `PlacePottedPlant`、静态盆栽图标和教程随机花色。 |
| `Lawn/PottedPlant.cs`、`Lawn/DrawVariation.cs` | 保留的花色字段、存档和枚举。 |
| `Lawn/ReanimatorCache.cs` | 旧花色仍只写 `Marigold_petals` 的轨道实例颜色。 |
| `Sexy.TodLib/Reanimation.cs` | Spine 轨道查询与实际骨骼绘制未接入旧花色字段。 |
