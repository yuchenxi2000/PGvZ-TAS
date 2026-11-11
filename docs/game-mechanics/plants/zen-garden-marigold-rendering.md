# 禅境花园金盏花花色渲染

本文档记录游戏从 v1.0.1 到 v1.2.6 一直存在的一个 bug：禅境花园中金盏花的所有变种都显示为白色。修改器内已通过 Hook 方式进行修复。

## 数据与颜色范围

禅境花园盆栽保存在 `PlayerInfo.mPottedPlant` 中。每个 `PottedPlant` 的
`mDrawVariation` 记录绘制变种；金盏花使用 `DrawVariation.MarigoldWhite` 至
`DrawVariation.MarigoldLightGreen`（枚举值 2 至 12），共 11 种花色。

`ReanimatorCache.UpdateReanimationforVariation` 是游戏应用绘制变种的统一入口。对于上述
金盏花变种，它会把对应颜色写入 `Marigold_petals` 动画轨道。商店、掉落物、手推车等
静态盆栽图标经 `ZenGarden.DrawPottedPlant` 调用 `Plant.DrawSeedType`，会传入
`mDrawVariation`，因此这些位置能够正常显示花色。

## 场上植物丢失花色的原因

进入禅境花园时，`ZenGarden.ZenGardenInitLevel` 会通过
`ZenGarden.PlacePottedPlant` 把盆栽存档逐个实例化为场上的 `Plant`。当前支持游戏版本的
实现会设置金盏花的动画和生长阶段，却没有将 `PottedPlant.mDrawVariation` 应用到新建的
`Plant.mBodyReanimID`。场上的植物由 `Plant.Draw` 直接绘制这份动画，所以花瓣沿用资源的
默认白色。

## 模组修复

`pgvztool/hook.py` 在 `ZenGarden.PlacePottedPlant` 原方法返回后执行以下处理：

1. 只处理已经长成金盏花的场上植物；幼苗仍按游戏原逻辑绘制。
2. 由盆栽索引重新取得对应的 `PottedPlant`。
3. 确认变种位于金盏花花色范围内。
4. 取得新植物的身体动画，并调用游戏自身的
   `ReanimatorCache.UpdateReanimationforVariation` 应用花色。

选择 `PlacePottedPlant` 而不是更小的动画辅助方法作为钩点，是因为它覆盖首次进入花园、
切换花园、移动或重新加载盆栽等实例化路径，而且方法体较大，不易因运行时内联而绕过
钩子。该修复不修改存档，只恢复已有 `mDrawVariation` 数据的显示。

## 升级游戏版本时的核对项

- `ZenGarden.PlacePottedPlant` 是否仍返回新建的场上 `Plant`。
- 场上植物是否仍通过 `Plant.mBodyReanimID` 绘制。
- `ReanimatorCache.UpdateReanimationforVariation` 是否仍负责设置
  `Marigold_petals` 的轨道颜色。
- 金盏花变种枚举范围是否仍为 `MarigoldWhite` 至 `MarigoldLightGreen`。
