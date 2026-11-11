# 莴苣伞防护范围

本文依据 PGvZ 1.3.0、1.3.1 的反编译代码，记录 `SeedType.Umbrella` 的防护判定和修改器“全屏莴苣伞”的接入点。

## 原生判定

`Board.FindUmbrellaPlant(gridX, gridY)` 顺序扫描 `mPlants`，只返回未死亡、在场上、未禁用的莴苣伞。原生范围要求目标格在伞所在格的横纵方向各不超过一格，即 3×3。它不根据当前动画状态筛选伞。

这两个版本中，`Board.FindUmbrellaPlant` 有两条调用路径：

- `Zombie.BungeeLanding()` 在蹦极僵尸高度降到 40 以内时，按落点调用该方法。找到伞后播放弹飞音效、触发伞的 `DoSpecial()`，将蹦极僵尸改为上升状态，并设置 `mHitUmbrella`。
- `Projectile.UpdateLobMotion()` 在篮球或僵尸豌豆找到受击植物后，按植物所在格调用该方法。找到伞后仍由原版处理伞的触发、反弹动画、音效和投射物销毁。没有受击植物时不会调用此方法。

## 僵王投车

`Zombie.BossRVAttack()` 选定砸车区域左上角，`Zombie.BossRVLanding()` 在车落下时结算。砸车区域为 2 行 × 3 列。

只有“僵王博士的复仇2”（`GameMode.ChallengeFinalBoss2`）会在落车时寻找莴苣伞。搜索范围是砸车区域向四周各扩一格，即场内的 4 行 × 5 列区域。游戏按 `mPlants` 的顺序选中第一株未死亡的莴苣伞，跳过本次对整个砸车区域的 `Squish()`，并把这株伞置为 `UmbrellaDeathTriggered`。`Plant.UpdateUmbrella()` 随后处理反弹状态并让这株伞死亡。其他模式或范围内没有可用的伞时，游戏直接压扁砸车区域内的植物。

投车判定直接扫描 `mPlants`，因此“全屏莴苣伞”对投车没有影响。

## 修改器接入

`pgvztool/hook.py` 挂钩 `Board.FindUmbrellaPlant`。开关关闭时直接返回原结果；开启时仍优先使用原版找到的邻近伞，仅在原结果为空时扫描整个 `mPlants`。全屏扫描沿用原版对死亡、`NotOnGround()` 和 `IsDisabled()` 的筛选。后续弹飞或反弹仍由原生调用者执行，关闭开关立即恢复 3×3。

开启“植物无敌”时，`Plant.Update` 的钩子在原方法执行前，把莴苣伞的牺牲触发或牺牲反弹状态换成对应的普通状态。原生 `UpdateUmbrella()` 继续处理挡车动画，并在动画结束后恢复待机。

## 反编译源码导航

1.3.0、1.3.1 中的相关位置相同：

| 文件 | 方法与位置 |
|---|---|
| `Lawn/Board.cs` | `FindUmbrellaPlant`，约 10864 行 |
| `Lawn/Zombie.cs` | `UpdateZombieBungee`、`BungeeLanding`，约 2419、2488 行 |
| `Lawn/Zombie.cs` | `BossRVLanding`、`BossRVAttack`，约 9363、9510 行 |
| `Lawn/Plant.cs` | `UpdateUmbrella`，约 7277 行 |
| `Lawn/Projectile.cs` | `UpdateLobMotion` 中的受击植物与莴苣伞判定，约 999–1104 行 |
