# 莴苣伞防护范围

本文依据当前支持的 PGvZ 1.3.0、1.3.1 反编译代码，记录 `SeedType.Umbrella` 的防护判定和修改器“全屏莴苣伞”的接入点。

## 原生判定

`Board.FindUmbrellaPlant(gridX, gridY)` 顺序扫描 `mPlants`，只返回未死亡、在场上、未禁用的莴苣伞。原生范围要求目标格在伞所在格的横纵方向各不超过一格，即 3×3。它不根据当前动画状态筛选伞。

当前两个版本只有两条调用路径：

- `Zombie.BungeeLanding()` 在蹦极僵尸高度降到 40 以内时，按落点调用该方法。找到伞后播放弹飞音效、触发伞的 `DoSpecial()`，将蹦极僵尸改为上升状态，并设置 `mHitUmbrella`。
- `Projectile.UpdateLobMotion()` 在篮球或僵尸豌豆找到受击植物后，按植物所在格调用该方法。找到伞后仍由原版处理伞的触发、反弹动画、音效和投射物销毁。没有受击植物时不会调用此方法。

## 修改器接入

`pgvztool/hook.py` 挂钩 `Board.FindUmbrellaPlant`。开关关闭时直接返回原结果；开启时仍优先使用原版找到的邻近伞，仅在原结果为空时扫描整个 `mPlants`。全屏扫描沿用原版对死亡、`NotOnGround()` 和 `IsDisabled()` 的筛选。后续弹飞或反弹仍由原生调用者执行，关闭开关立即恢复 3×3。

## 反编译源码导航

两个支持版本中的相关位置相同：

| 文件 | 方法与位置 |
|---|---|
| `Lawn/Board.cs` | `FindUmbrellaPlant`，约 10864 行 |
| `Lawn/Zombie.cs` | `UpdateZombieBungee`、`BungeeLanding`，约 2419、2488 行 |
| `Lawn/Projectile.cs` | `UpdateLobMotion` 中的受击植物与莴苣伞判定，约 999–1104 行 |
