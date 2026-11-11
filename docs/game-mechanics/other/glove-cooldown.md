# 手套冷却与放置入口

本文依据本地 PGvZ 1.3.2 源码记录战斗手套的冷却调用链，并对照 1.3.1 源码验证同一钩子的适用性。

## 冷却写入时机

手套剩余冷却保存在 `Challenge.mGloveCounter`。`Challenge.Update()` 在场地有手套且计数大于零时每帧减一；按钮使用判定和冷却遮罩也读取该字段。

1.3.2 的实际放置入口是 `Board.MouseUpWithPlant(x, y, theClickCount)`：

1. 校验光标、工具可用性、目标格和种植条件。
2. 普通移动依次调用 `ZenGarden.MovePlant()`、`Challenge.MovePlant()`；融合则创建融合植物并删除原植物，不调用 `Challenge.MovePlant()`。
3. 若目标格不同于原格、场地有手套且不在禅境花园或智慧树模式，写入 `mChallenge.mGloveCounter = mChallenge.GetGloveCounterMax()`。
4. 完成后续种植处理并清理光标。

因此在 `Challenge.MovePlant()` 返回后清零太早，会被第 3 步覆盖，而且不能覆盖融合路径。`Challenge.MovePlant()` 还用于取消手套操作时将植物放回原位，以及传送门交换植物，不能将它等同于手套放置完成。

## 1.3.1 源码核对

1.3.1 与 1.3.2 的 `Board.MouseUpWithPlant(int x, int y, int theClickCount)` 签名及鼠标、触屏调用入口一致，差别在于冷却写入位置：

| 版本 | 普通移动的冷却写入位置 | 手套融合 |
|---|---|---|
| 1.3.1 | `Challenge.MovePlant()` 内部，目标格不同于原格且场地有手套时写入。 | 不调用 `Challenge.MovePlant()`，也没有单独写入冷却。 |
| 1.3.2 | `Board.MouseUpWithPlant()` 内部，在普通移动或融合后统一写入。 | 同样进入统一冷却逻辑。 |

两者的冷却写入都发生在 `Board.MouseUpWithPlant()` 返回之前，因此修复后的钩子在 `orig` 返回后清零，对 1.3.1 的普通手套移动也有效；融合本身不产生冷却，行为仍保持无冷却。

## 鼠标与触屏入口

桌面 `Board.MouseDownInternal()` 在光标携带植物时调用 `MouseUpWithPlant()`，触屏则在 `Board.MouseUpInternal()` 中调用同一入口。名字中的 `MouseUp` 不表示只支持桌面鼠标抬起事件。

`Board.MouseDownWithPlant()` 在本版本仅处理右键取消，不包含放置或冷却写入。不能改为挂钩这个较短的方法来清除放置后的冷却。

## 修改器实现

`pgvztool/hook.py` 挂钩 `Board.MouseUpWithPlant()`，完整执行 `orig` 后，若 `cheat_option.gloveNoCooling` 开启，则将当前 Board 的 `mChallenge.mGloveCounter` 清零。这样普通移动和融合都会在游戏最后一次写入之后归零，也保留原有的放置校验和植物处理。关闭选项时不改写冷却。

冷却最大值仍由游戏决定：自定义关卡 `CSGlove.Cooldown` 优先，其次是肉鸽传送带、地狱生存、高难冒险等模式的默认值。无需修改关卡配置或挂钩可能被内联的 `GetGloveCounterMax()`。
