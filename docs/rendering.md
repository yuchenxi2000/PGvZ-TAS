# 游戏渲染与坐标系统

## 三种坐标系统

- **屏幕坐标 (Screen)**：原始鼠标/触摸输入。`Board.mX` / `Board.mY` 是 Widget 在屏幕上的偏移。铲子按钮、进度条、种子栏等 UI 元素使用屏幕坐标。
- **场地/世界坐标 (Board/World)**：`Plant.mX/Y`、`Zombie.mPosX/Y`（float）、`Zombie.mX/Y`（int，`= (int)mPosX/Y`）。由 `GridToPixel` 返回。Camera 变换连接屏幕坐标和场地坐标。
- **格子坐标 (Grid)**：离散 `(col, row)`。范围 `col∈[0,8]`，`row∈[0,4]`（5行）或 `row∈[0,5]`（6行）。`PixelToGrid` 将场地坐标转为格子坐标。

## Camera 变换

定义在 `Board.Camera`（反编译 Board.cs:80-132）：

```
ScreenToBoard:  board = (screen - Camera.XY - halfScreen) / Zoom + halfScreen - boardOffsetX
BoardToScreen:  screen = (board - halfScreen + boardOffsetX) * Zoom + halfScreen - boardOffsetX + Camera.XY
```

- `Camera.X`, `Camera.Y`：平移偏移（用于屏幕震动、场景切换）
- `Camera.Zoom`：缩放因子。PC = 1.0，手机 ≈ 0.833
- `boardOffsetX`：`Constants.Board_Offset_AspectRatio_Correction`（随分辨率不同）
- `halfScreen`：`screenWidth/2` 或 `screenHeight/2`

Camera 通过 Graphics 变换栈实现（`g.pushTransform` / `g.popTransform`）。

### 各对象坐标归属

| 对象 | 字段 | 坐标系统 |
|---|---|---|
| Board Widget | `mX`, `mY` | 屏幕 |
| Plant | `mX`, `mY` | 场地 |
| Zombie | `mPosX`, `mPosY` (float) | 场地 |
| Zombie | `mX`, `mY` (int) | 场地（`(int)mPosX/Y`，每帧同步） |
| GridItem | `mPosX`, `mPosY` | 场地 |
| GridItem | `mGridX`, `mGridY` | 格子 |
| Camera | `X`, `Y` | 平移量 |
| Camera | `Zoom` | 缩放 |

`Zombie.mX = (int)Zombie.mPosX`，差值 `mPosX - mX` 为亚像素偏移，由 `GetDrawPos` 用于平滑渲染。PC 上两者数值看起来一样是因为小数部分很小。

## 绘制钩子的层级

```
LawnApp.DrawGame              ← 最顶层（遮挡对话框）
  └─ WidgetManager.DrawScreen
       ├─ 对话框 / SeedChooserScreen
       └─ Board.Draw           ← 中间层：orig 之后绘制（Board 内容已画完，屏幕坐标，对话框未画）
            └─ DrawGameObjects
                 └─ DrawShovel ← 最底层（每加一个新 UI 就要新钩子）
```

**Board.Draw**（Board.cs:4921）是推荐的钩子点：

```csharp
public override void Draw(Graphics g)
{
    if (商店/图鉴打开) return;
    Camera.ApplyTransform(g);   // push：进入场地坐标
    DrawGameObjects(g);         // 画所有内容
    Camera.ResetTransform(g);   // pop：回到屏幕坐标
}
```

`orig(board, g)` 返回后：Camera 已 Reset，Board 所有内容已画完，对话框尚未渲染。当前处于屏幕坐标空间。

**DrawGameObjects** 内部按排序后的渲染列表逐一绘制。TopUi（种子栏、铲子）和 BottomUi（进度条、割草机）会临时 Reset Camera 以屏幕坐标绘制：

```csharp
case RenderObjectType.TopUi:
    Camera.ResetTransform(g);   // 屏幕坐标
    DrawUITop(g);
    Camera.ApplyTransform(g);   // 切回场地坐标
```

当前 `pgvztool/hook.py` 中的 `Board.Draw` 钩子分两个阶段绘制：
1. Camera Apply（场地坐标）→ 画植物/僵尸血量
2. Camera Reset（屏幕坐标）→ 画轻松放置 UI、波数信息
