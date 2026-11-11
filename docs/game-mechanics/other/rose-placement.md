# 萝丝（钉耙）的选用与放置

在游戏代码中，萝丝的选卡按钮叫 `mRoseButton`，库存对应 `StoreItem.STORE_ITEM_RAKE`，场上的物件类型是 `GridItemType.Rake`。以下流程见本地 PGvZ 1.3.0、1.3.1 源码及已安装的 1.3.2 程序。

## 原版禁用范围

`Board.CanPlaceRake()` 优先允许砸罐子模式。其余模式根据 `StageHasZombieWalkInFromRight()` 排除下列关卡，并额外排除两种宝石迷阵：

- 僵王博士的复仇 1、2，以及冒险和快速游戏的第 50 关。
- 锤僵尸，以及冒险和快速游戏的第 15 关。自定义关卡的 `CSWhackAZombieLevel` 也算锤僵尸。
- 我是僵尸 1–9 和无尽，以及使用 `CSIZombieLevel` 的自定义关卡。
- 冰冻关卡、松鼠、僵尸水族馆、禅境花园和智慧树。
- 宝石迷阵和宝石迷阵旋风。

## 选用和放置流程

- 选卡界面用 `CanPlaceRake()` 初始化和切换萝丝按钮，库存为零时隐藏按钮。`SeedChooserScreen.CloseSeedChooser()` 将选中状态写入 `Board.mDoPlaceRose`。
- 僵王关在 `CutScene.StartLevelIntro()` 就调用 `PlaceLawnItems()`。此时玩家尚未确认选卡，`mDoPlaceRose` 仍为假，而 `mPlacedLawnItems` 已置为真，之后原版不会再次布置场地。开启“解锁萝丝”时，修改器在确认选卡后检查这个标记，已完成布置且选中了萝丝时调用 `Board.PlaceRake()`。已经有萝丝或处于生存换轮选卡时跳过补放。
- 无选卡关卡通过 `CutScene.Update()` 或 `CancelIntro()` 显示原生确认框。若场地已经布置，`LawnMessageBoxDone()` 在确认使用后直接调用 `Board.PlaceRake()`。
- `Board.PlaceRake()` 检查库存和选中状态，非砸罐子模式还会检查 `CanPlaceRake()`。原生选址只取前五行中的普通陆地、浅水和高地，选址成功后才扣库存并创建萝丝。全水行的大泳池等场地没有候选行，解锁后仍不会生成萝丝。
