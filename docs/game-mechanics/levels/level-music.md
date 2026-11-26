# 游戏背景音乐

本文依据本地 PGvZ 1.4.3 Windows 版的反编译代码和安装目录音乐资源静态核对。

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

特殊玩法优先于场景。暴风雨夜（冒险 4-10、对应的快速游戏及同名小游戏）会停止背景音乐。

按场景选曲时，游戏先检查雾夜背景，再检查夜间、泳池、屋顶，最后用白天曲。月夜使用的 `Num6Boss` 同时满足夜间和屋顶判定，先命中夜间。泳池和夜间判定依据背景枚举，地形编辑写入的行类型和格子类型不参与选曲。

`StartGameMusic()` 的传送带分支同时检查冒险和快速游戏，但读取的是 `mPlayerInfo.mLevel` 是否等于 10、20 或 30。判断快速游戏的实际选曲时，需要区分档案进度和 `Quickplay10` 等关卡模式。

### 其他界面

| 界面 | `MusicTune` | 独立音频文件 |
| --- | --- | --- |
| 启动标题画面、主菜单、商店 | `TitleCrazyDaveMainTheme` | `crazydave.ogg` |
| 选卡、图鉴、挑战列表 | `ChooseYourSeeds` | `chooseyourseeds.ogg` |
| 禅境花园、智慧树 | `ZenGarden` | `zengarden.ogg` |
| 动态立绘 | `ZenGardenSH` | `zengarden_sh.ogg` |
| 制作人员名单在视频播放结束后 | `DayGrasswalk` | `day.ogg` |

标题画面首次更新时开始播放主菜单曲。主菜单、商店及部分关卡过场也会请求同一曲目。游戏按曲目编号判断是否继续播放，进入共用曲目的界面时可能沿用当前播放进度。

## 资源和覆盖

大部分经典曲目，包括选卡和禅境花园，优先从 `mainmusic.mo3` 的不同位置播放。部分场景会同步使用鼓点轨和 `mainmusic_hihats.mo3`，在战斗过程中切换配器。模块加载失败时使用独立资源，表中 `.ogg` 是对应的音频文件。主菜单曲、`FinalBoss2` 和动态立绘曲默认走独立音频路径。

创意关卡可通过 `LevelProperty.MusicType` 覆盖上述默认选曲。省略、`null` 或负数沿用默认选曲，`0` 静音。`1` 至 `5` 对应白天、黑夜、泳池、雾夜和屋顶，`6` 至 `12` 依次为选卡、主菜单、禅境花园、Cerebrawl、Loonboon、Ultimate Battle、Brainiac Maniac，`2000` 为 `FinalBoss2`。

### 替换音乐

- Windows 安装包中的 `Content/music/*.xnb` 由 `SongReader` 读取，引用同目录的同名 `.ogg`。关闭游戏后，可备份原 `.ogg`，保留 `.xnb`，用同名 Ogg Vorbis 文件替换对应独立音频，再重新启动游戏。文件替换会影响所有引用该曲目的界面。
- 普通关卡、选卡或禅境花园使用 MO3 时，只替换其 `.ogg` 不会生效。将 `mainmusic.mo3` 暂时移出 `Content/music/` 后再启动，会让这些曲目统一走独立音频路径，同时失去原有的动态鼓点和配器变化。恢复该文件后重启可恢复模块播放。
- 如果要按界面、背景或具体关卡分别设置自定义曲目，模组可以在 `Music.PlayMusic()` 选定实际播放资源时接入，并沿用游戏的音乐接口处理音量、循环、暂停和淡出。对共用曲目编号的界面，还需在界面切换时重新匹配配置，因为 `MakeSureMusicIsPlaying()` 会跳过相同编号。暴风雨夜默认直接调用 `StopAllMusic()`，为它添加音乐需要覆盖该关的选曲分支。

## 反编译源码导航

以下路径相对于同级 `PGvZ-decompilation-1.4.3` 目录。

| 文件 | 相关逻辑 |
| --- | --- |
| `Lawn/Music.cs` | `MusicInit()` 加载资源，`StartGameMusic()` 决定关卡曲目，`PlayMusic()` 选择模块位置和音轨。 |
| `Sexy/XNAMusicInterface.cs` | 加载 MO3 或 XNB `Song`，管理循环、音量、暂停和资源释放。 |
| `Lawn/TitleScreen.cs`、`Lawn/GameSelector.cs`、`Lawn/StoreScreen.cs` | 标题画面、主菜单和商店播放同一曲目。 |
| `Lawn/SeedChooserScreen.cs`、`Lawn/AlmanacDialog.cs`、`Lawn/ChallengeScreen.cs` | 选卡、图鉴和挑战列表播放同一曲目。 |
| `Lawn/LawnApp.cs` | 判断僵王、暴风雨夜、保龄球、砸罐子等特殊玩法。 |
| `Lawn/Board.cs` | `StageIsNight()`、`StageHasPool()` 和 `StageHasRoof()` 判断背景对应的场景。 |
| `Lawn.Creative/CSLevelProperty.cs`、`Lawn/MusicTuneConvertor.cs` | 读取创意关卡的 `MusicType` 并转换编号。 |
