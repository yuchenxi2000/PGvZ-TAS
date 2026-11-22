# 战斗界面道具布局

依据本地 PGvZ 1.4.3 反编译源码静态核对。下文的坐标使用 Board 局部的界面坐标，常规战斗时加上 `Board.mX/mY` 即得到游戏逻辑屏幕坐标。

## 原生道具的位置入口

| 道具 | 矩形入口 | 原生调用方 |
|---|---|---|
| 铲子 | `Board.GetShovelButtonRect()` | `DrawShovel()`、`MouseHitTest()`、铲子教学箭头、经典布局下的手套基准位置 |
| 手套 | `Board.GetZenButtonRect(GameObjectType.Glove)` | `DrawZenButtons()` 以该矩形绘制底座、图标和冷却遮罩，`MouseHitTest()` 用它检测点击 |

两个入口每次返回现算的 `TRect`。修改器在非经典战斗场景挂钩这两个入口，由游戏继续处理绘制和命中。手套挂钩按 `Glove` 类型过滤，花园道具也调用同一个方法。铲子教学箭头只在进入教学状态时读取铲子的 X，教学阶段沿用原生矩形。

`GetCombatToolRects()` 统一计算三者的位置。一个或两个道具在中间居中排列，三个同时显示时，铲子和手套在中间，轻松放置在菜单右侧。轻松放置的绘制和点击都按当前状态计算矩形，切换开关后无需等待绘制刷新点击区。点击其他道具或菜单、暂停、加速时，原生交互优先于轻松放置。

## 其他界面元素的占位

| 元素 | 位置与尺寸 |
|---|---|
| 菜单、暂停、加速 | 分别读 `Board.mMenuButton`、`mPauseButton`、`mAccelerateButton` 的 `mX/mY/mWidth/mHeight`。结合按钮存在性、`mBtnNoDraw` 和原生绘制分支。禁用的按钮仍可能绘出。 |
| 非经典阳光栏 | `SeedBank.DrawSun()` 的图内起点为 `(UISunBankPositionX - Board_Offset_AspectRatio_Correction, seedBank.mX)`，还要叠加 `SeedBank.BeginDraw()` 的平移。使用 `IMAGE_DAN_SUNBANK` 尺寸。`BeginDraw()` 检查种子栏可见性，传送带关卡不画独立阳光栏。 |
| 非经典进度条 | `Board.DrawProgressMeter()` 在 `HasProgressMeter()` 为真时绘制。底图起点是 `(UIProgressMeterPosition.X - Board_Offset_AspectRatio_Correction, UIProgressMeterPosition.Y)`，尺寸取 `IMAGE_FLAGMETER.GetCelWidth()/GetCelHeight()`。旗帜、僵尸头像和文本也要计入绘制范围。 |
| 经典布局 | 阳光显示位于横向种子栏内，横排要避开实际种子栏宽度及老虎机等玩法的独立控件。进度条底图位于底部，起点是 `(700 - 格宽, BOARD_HEIGHT - 格高)`。 |

`Board.DrawUIBottom()` 和 `DrawUITop()` 按界面模式和雾场景选择右上按钮的绘制批次。布局始终预留阳光栏和进度条的位置，避免传送带或进度条显示状态变化引起道具跳位。

## 三个道具的空间

当前版本实际加载 `Constants.Load480x800()` 和 `AtlasResources_600x1000`。常规非经典战斗中，种子栏平移归零时，阳光栏占 `[19, 162)`，进度条底图占 `[350, 587)`，中间有 188 逻辑像素。三个 70 像素的底座共需 210 像素，间距为零也差 22。铲子图标绘在 `x - 7`，战斗手套的 96 像素图标绘在 `x - 4`，排版还应为这些可能伸出底座的图像留空间。

- 菜单的 Board 局部右边缘固定为 `800`。1000 像素逻辑画幅下，右侧净宽是 `1000 - Board.mX - 800`。`MakeNewBoard()` 将 `Board.mX` 设为 `100`，关卡介绍滚回战斗位置时也以 `100` 为终点。暂停和加速的右边缘都不超过菜单右边缘，500p 布局与普通布局的逻辑宽度相同。常态净宽为 100，70 像素的轻松放置底座居中后左右各留 15。
- `Board.Update()` 的原生震动最多让 `Board.mX` 向左移 4，右侧净宽只会增大。纵向震动可让 `Board.mY` 到 `-6`，所以按钮的局部 `y=3` 在逻辑画面里的顶边可到 `-3`。贴合逻辑画幅的窗口可能短暂裁掉顶部几像素。若其他模组改变 `Board.mX` 或菜单几何，当前居中公式没有宽度校验，完整容纳底座至少需要 70 逻辑像素。
- 若需要三个靠在一起，可以缩放底座及图标并同步缩放命中矩形，或腾出更宽的中间区域。仅缩小玉米卷图标不会缩小其底座。500p 下暂停、加速在第二行，进度条可作为整体右移的候选。例如右移 70 后，进度条底图变为 `[420, 657)`，中间增至 258，菜单从 `700` 开始。这是静态几何示例，需在游戏中检查旗帜、文字及触屏命中。若使用非 500p 的非经典组合，暂停默认从 `610` 开始且和进度条同一行，底图右侧名义上只余 23，单靠把进度条右移很难腾出足够位置。
- 经典布局应独立计算横向种子栏两侧的空位。例如宽卡槽使种子栏右边缘达到 `609` 时，到菜单左边缘 `700` 只有 91 像素，菜单右侧另有 100 像素，两段各能容纳一个原尺寸底座。此时还要在当前界面上寻找其他可用位置，或缩小按钮。

如果移动进度条，应让底图、填充、旗帜、头像、文字一起平移，并同步修改器的 `DrawWaveInfo()`。如果移动阳光栏，应一并核对收集阳光的动画目标 `Board_SunCoin_CollectTarget`。

## 源码入口

| 文件 | 相关实现 |
|---|---|
| `Lawn/Board.cs` | 构造函数、`GetShovelButtonRect`、`GetZenShovelButtonRect`、`GetZenButtonRect`、`MouseHitTest`、`DrawShovel`、`DrawZenButtons`、`DrawProgressMeter`、`HasProgressMeter`、`DrawUIBottom`、`DrawUITop`、`DrawTopRightUI` |
| `Lawn/SeedBank.cs`、`Lawn/GameObject.cs` | `DrawSun`、`Move`、`BeginDraw` |
| `Lawn/LawnApp.cs`、`Sexy/WidgetManager.cs` | `MakeNewBoard`、`ApplyInterfaceLayout`、`DrawScreen` |
| `Sexy/Constants.cs`、`Sexy/AtlasResources_600x1000.cs` | `Load480x800`、阳光栏、进度条、道具底座及图标资源 |
