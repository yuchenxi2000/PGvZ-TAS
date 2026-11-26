# PGvZ 1.4.3 存档格式

依据本地 `PGvZ-decompilation-1.4.3` 静态核对。下列路径以游戏的 `applicationStoragePath` 为根目录。

| 路径 | 内容 |
| --- | --- |
| `docs/userdata/users.dat` | 玩家档案索引，记录玩家 ID 列表和当前玩家名 |
| `docs/userdata/user{playerId}.dat` | 玩家进度、金币、解锁、成就、禅境花园和部分选项 |
| `docs/userdata/game{playerId}_{gameMode}.dat` | 关卡续玩状态。创意关卡有定义时，用关卡 CRC 的八位大写十六进制表示替代 `gameMode` |
| `docs/userdata/tas_saves/{playerId}_{gameMode}_{frame}.dat` | TAS 快照，使用原生关卡存档的序列化。创意关卡有定义时也用 CRC 替代 `gameMode`。`frame` 是 `Board.mMainCounter` |

## 玩家进度与关卡存档

`user{playerId}.dat`、`game…dat` 和 TAS 快照都是直接写入磁盘的 `BufferNew` 二进制数据，无压缩或加密。新写入的文件以三个小端 `int32` 开头。

| 偏移 | 字段 | 值 |
| --- | --- | --- |
| `0x00` | 文件魔数 | 玩家进度 `99816666`（`0x05F314DA`），关卡与 TAS `14372508`（`0x00DB4E9C`） |
| `0x04` | 存档结构版本 | `20`（`SaveFileVersion.MailboxState`） |
| `0x08` | 格式标记 | `20208888`（`0x01345CF8`，`SAVE_FILE_WP_RAW`） |

文件头之后是按固定顺序写入的枚举名称表。每张表先写 `int32` 项数，再写每个名称。正文的枚举字段用 `int32` 表索引表示。`BufferNew` 字符串先写小端 `int32` 字节数，再写 UTF-16LE 字节，`-1` 表示 `null`。布尔值占一个字节，多字节数值采用小端编码。

玩家进度的正文按 `PlayerInfo.Sync()` 顺序写入。关卡正文先写 `EffectSystem.Sync()`，再写 `Board.Sync()`，包含僵尸、植物、子弹、阳光、波次和帧计数等。两类正文都以小端 `int32` 值 `777` 结束。数组及列表长度会影响后续字段偏移，解析时须按对应版本的 `Sync` 顺序读取。

TAS 文件名里的帧号用于快照排序。读档时，游戏从正文恢复 `mMainCounter`。快照覆盖的字段取决于游戏序列化，详见 [TAS 存档及限制](../../mod/internals/tas.md#存档数据)。

## 玩家档案索引

`users.dat` 使用 `Sexy.Buffer`。按写入顺序是 `int32` 版本 `1`、`int32` 玩家数量、每名玩家的 4 字节 ID、当前玩家名、`int32` 检查值 `555`。这里的玩家名使用 `int32` 字节数加 UTF-8 字节，Windows 下整数为小端。

## 反编译源码导航

| 文件 | 相关入口 |
| --- | --- |
| `Lawn/GlobalMembersSaveGame.cs` | `LawnSaveGame()`、`InitializeGameEnum()`、`EnumSaver.Sync()` |
| `Lawn/Board.cs` | `SaveGame()`、`Sync()` |
| `Lawn/LawnCommon.cs` | `GetSavedGameName()` |
| `Lawn/PlayerInfo.cs`、`Lawn/ProfileMgr.cs` | `SaveDetails()`、`SyncPlayer()`、`ProfileMgr.Save()` |
| `Sexy/BufferNew.cs`、`Sexy/Buffer.cs`、`Sexy/SexyAppBase.cs` | 基础类型编码和磁盘读写 |
