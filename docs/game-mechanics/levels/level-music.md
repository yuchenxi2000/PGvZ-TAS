# 关卡背景音乐

本文依据本地 PGvZ 1.4.3 的反编译代码和安装目录音乐资源静态核对。

## 默认选曲

`Music.StartGameMusic()` 为战斗关卡选择 10 首背景音乐，其中 5 首按场景选择，5 首用于指定玩法。以下文件位于安装目录的 `Content/music/`。

| 场景或玩法 | 曲目 | 独立音频文件 |
| --- | --- | --- |
| 白天草地及其他默认场景 | Grasswalk | `day.ogg` |
| 黑夜、月夜、高地、僵尸水族馆 | Moongrains | `night.ogg` |
| 泳池、大泳池 | Watery Graves | `pool.ogg` |
| 雾夜 | Rigor Mormist | `fog.ogg` |
| 屋顶 | Graze the Roof | `roof.ogg` |
| 砸罐子、我是僵尸 | Cerebrawl | `cerebrawl.ogg` |
| 坚果保龄球、锤僵尸、小僵尸大麻烦、蹦极闪电战、僵尸快跑 | Loonboon | `loonboon.ogg` |
| 冒险第 10、20、30 关，排山倒海系列 | Ultimate Battle | `conveyor.ogg` |
| 冒险 5-10、僵王博士的复仇 | Brainiac Maniac | `boss.ogg` |
| 僵尸博士的复仇2（`ChallengeFinalBoss2`） | `FinalBoss2` | `boss2.ogg` |

特殊玩法优先于场景。暴风雨夜（冒险 4-10、对应的快速游戏及同名小游戏）会停止背景音乐。禅境花园和智慧树共享 `zengarden.ogg`，选卡使用 `chooseyourseeds.ogg`，主菜单使用 `crazydave.ogg`，动态立绘界面使用 `zengarden_sh.ogg`。

按场景选曲时，游戏先检查雾夜背景，再检查夜间、泳池、屋顶，最后用白天曲。月夜使用的 `Num6Boss` 同时满足夜间和屋顶判定，先命中夜间。泳池和夜间判定依据背景枚举，地形编辑写入的行类型和格子类型不参与选曲。

`StartGameMusic()` 的传送带分支同时检查冒险和快速游戏，但读取的是 `mPlayerInfo.mLevel` 是否等于 10、20 或 30。判断快速游戏的实际选曲时，需要区分档案进度和 `Quickplay10` 等关卡模式。

## 资源和覆盖

经典曲目优先从 `mainmusic.mo3` 的不同位置播放。部分场景会同步使用鼓点轨和 `mainmusic_hihats.mo3`，在战斗过程中切换配器。模块加载失败时使用独立资源，表中 `.ogg` 是对应的音频文件。`FinalBoss2` 始终使用独立资源。

创意关卡可通过 `LevelProperty.MusicType` 覆盖上述默认选曲。省略、`null` 或负数沿用默认选曲，`0` 静音。`1` 至 `5` 对应白天、黑夜、泳池、雾夜和屋顶，`6` 至 `12` 依次为选卡、主菜单、禅境花园、Cerebrawl、Loonboon、Ultimate Battle、Brainiac Maniac，`2000` 为 `FinalBoss2`。

## 反编译源码导航

以下路径相对于同级 `PGvZ-decompilation-1.4.3` 目录。

| 文件 | 相关逻辑 |
| --- | --- |
| `Lawn/Music.cs` | `MusicInit()` 加载资源，`StartGameMusic()` 决定关卡曲目，`PlayMusic()` 选择模块位置和音轨。 |
| `Lawn/LawnApp.cs` | 判断僵王、暴风雨夜、保龄球、砸罐子等特殊玩法。 |
| `Lawn/Board.cs` | `StageIsNight()`、`StageHasPool()` 和 `StageHasRoof()` 判断背景对应的场景。 |
| `Lawn.Creative/CSLevelProperty.cs`、`Lawn/MusicTuneConvertor.cs` | 读取创意关卡的 `MusicType` 并转换编号。 |
