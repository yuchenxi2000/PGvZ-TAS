# 阳光余额与上限

本文依据本地 PGvZ 1.3.2 反编译源码，记录阳光余额、正常收集上限和修改器的限制。
未核对 1.3.0、1.3.1、1.3.3、1.3.4 的对应实现。用户已实测直接挂钩
`Board.AddSunMoney(int)` 受内联影响，而挂钩 `Coin.ScoreCoin()` 有效；下文其余机制依据静态源码。

## 正常增加阳光的上限

阳光余额存储在 `Board.mSunMoney`，类型为 C# `int`。正常增加余额时调用的
`Board.AddSunMoney(int theAmount)` 直接写死了 `9990`：

```csharp
public void AddSunMoney(int theAmount)
{
    mSunMoney += theAmount;
    if (mSunMoney > 9990)
    {
        mSunMoney = 9990;
    }
}
```

这个上限是方法中的整数字面量，没有对应的可调字段或创意关卡配置。
`Coin.ScoreCoin()` 在阳光收集结算时调用此方法，因此普通、小、大、微型阳光
（分别为 25、15、50、5）均受限制。游戏调试键增加 100 或 999999 阳光也调用此方法。

另一个四参数重载 `AddSunMoney(int theX, int theY, int theSunMoney, CoinMotion)`
只生成场上的阳光物件，不直接增加余额；物件收集结算时仍走上述单参数方法。

## 直接赋值可以超出 9990

`mSunMoney` 是普通字段，不是带限幅 setter 的属性。直接赋值不会经过 `AddSunMoney`：

- 创意关卡 `StartingSun` 通过 `GetInt32()` 读取，初始化 Board 时直接赋给 `mSunMoney`，
  这条路径没有 `9990` 限幅。
- `CheatActions.SetSun()` 直接赋值，没有额外限幅。
- `SeedBank.DrawSun()` 对余额只做 `Math.Max(mSunMoney, 0)`，再转成字符串显示，
  没有把大于 `9990` 的值裁成 `9990`；长数字是否超出背景框需另行实测。
- `TakeSunMoney()` 检查余额与收集途中的阳光之和，然后直接扣款，没有上限检查。

因此，直接设为 `20000` 后可以保留该值并用于扣款；但下一次调用单参数
`AddSunMoney` 时，若加后的余额仍超过 `9990`，就会被截回 `9990`。
例如 `20000 + 25` 的结果是 `9990`，而不是 `20025`。
该方法不是每帧统一限幅，修改器不能只放宽输入框就保证超额阳光正常累积。

C# `int` 的最大值是 `2147483647`，这是存储类型边界，不是可安全累积的游戏上限；
增加阳光和计算收集途中阳光时仍需要给整数加法留出空间。

## 修改器现状

“资源与进度”底部的“去掉阳光上限”（`CheatOption.noSunLimit`）默认关闭，按其他
开关的既有流程同步状态并保存 PC 网页选项。开启后，阳光输入框最大值从 `9990`
改为 `2147483647`；设置为关闭时，立即将游戏内余额及网页输入框中超过 `9990` 的值
截回 `9990`，较小值保持不变。后端在选项 setter 中执行，因此恢复已保存的关闭状态
也会应用限幅；当前没有 Board 时只保存开关状态。网页从远端同步为关闭时同样修正输入值。

`pgvztool/hook.py` 挂钩 `Coin.ScoreCoin()`。开关开启且收集物为阳光时，先记录
余额与阳光面值之和，执行原方法以保留物件回收等行为，再将未受 `9990` 限幅的结果
写回余额，仅在 C# `int` 最大值处截断。关闭开关或收集非阳光物件时，原样执行原方法。
不挂钩已实测被内联的 `Board.AddSunMoney(int)`。

“无限阳光”脚本 `ScriptInfSun()` 仍在每次执行时将余额设为 `9990`。想要自行设置
更高余额或持续收集累积时，应关闭“无限阳光”。

## `Coin.ScoreCoin` 的覆盖范围

它不是所有阳光增减的统一入口。核对本地 1.3.2 源码中的 `mSunMoney` 写入与
`AddSunMoney`、`TakeSunMoney` 调用后，各路径如下：

| 路径 | 是否经过 `ScoreCoin` | 当前开关的效果 |
|---|---|---|
| 各种阳光物件的手动或自动收集 | 是 | 去掉收集结算时的 `9990` 限制 |
| 四参数 `AddSunMoney` 生成的阳光物件 | 收集结算时经过 | 同上 |
| `Board.KeyChar` 原生调试键增加 100 或 999999 | 否，直接调用单参数 `AddSunMoney` | 仍按游戏原生逻辑限幅，可能把超额余额降回 `9990` |
| `LawnApp.ButtonDepress` 的对话框 20 增加 100 | 否，直接调用单参数 `AddSunMoney` | 同上 |
| 种植、小游戏操作、特殊植物行动等扣款 | 否，调用 `TakeSunMoney` | 扣款不做 `9990` 限幅，沿用原逻辑 |
| 原生调试键扣除 100 | 否，直接减余额并截到非负 | 沿用原逻辑 |
| 初始阳光、创意关卡 `StartingSun`、读档 | 否，直接赋值或反序列化 | 本来就不受 `AddSunMoney` 的限幅影响 |
| 网页设置阳光 | 否，`CheatActions.SetSun` 直接赋值 | 开启时输入框允许更高数值 |
| “无限阳光”或游戏原生作弊菜单设置阳光 | 否，直接赋值为 `9990` | 仍会覆盖现有余额 |

因此当前开关解除的是收集结算上限，不保证其他模组直接调用单参数 `AddSunMoney`
或上述原生调试加值时也取消限幅。扩大覆盖范围需另行处理相应调用者。

## 源码导航

本次核对的本地源码位于 `PGvZ-Mac/src/Lawn/`，下列路径相对此目录：

| 文件 | 重点 |
|---|---|
| `Lawn/Board.cs` | `mSunMoney`、单参数及四参数 `AddSunMoney`、`TakeSunMoney`、`CanTakeSunMoney`、初始阳光赋值 |
| `Lawn/Coin.cs` | `GetSunValue`、`ScoreCoin` |
| `Lawn/SeedBank.cs` | `DrawSun` |
| `Lawn/LawnApp.cs` | `ToString(int)` 仅缓存整数的字符串形式 |
| `Lawn/Creative/CSLevelProperty.cs` | `StartingSun` 的读取 |

`Board.mMaxSunPlants` 是在 `AddPlant()` 后采样的向日葵与阳光菇数量历史峰值，
与阳光余额上限无关；统计盲区及其与实时计数的区别见[产阳光植物数量统计](../plants/sun-plant-counts.md)。
