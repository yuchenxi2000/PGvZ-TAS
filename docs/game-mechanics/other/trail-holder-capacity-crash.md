# 拖尾容器扩容与旧版崩溃

PGvZ 1.3.2 起，游戏原生的拖尾容器会自动扩容。PGvZ-TAS 已移除旧版扩容钩子，当前支持的 PGvZ 1.4.3 直接使用游戏原生分配逻辑。

## PGvZ 1.3.2 起的分配与回收

在 1.4.3 的反编译源码 `Sexy.TodLib/TrailHolder.cs` 中，`InitializeHolder()` 为 `mTrails` 预留 128 个位置。`AllocTrailFromDef()` 创建并初始化拖尾后直接调用 `mTrails.Add(trail)`，容量用完时由 .NET 的 `List<Trail>` 自动扩容。

子弹死亡时通常会通过 `AttachmentDie` 结束附件，`EffectSystem.ProcessDeleteQueue` 会从 `mTrails` 移除标记为死亡的拖尾。`Capacity` 表示列表预留的空间，活跃拖尾回收后仍可保留这部分容量供后续分配。

## 旧版容量限制

在 PGvZ 1.2.6 中，香蒲连续产生大量 `ProjectileType.CattailSpike` 时，游戏可能在发射新子弹的瞬间崩溃。每颗香蒲刺在 `Projectile.ProjectileInitialize` 中都会申请一条 `TrailType.Cattail` 拖尾。

```csharp
GlobalMembersAttachment.AttachTrail(
    ref mAttachmentID,
    mApp.mEffectSystem.mTrailHolder.AllocTrail(0, TrailType.Cattail),
    10f,
    10f);
```

所有拖尾共用 `EffectSystem.mTrailHolder.mTrails`。在这一版本中，初始容量同样为 128，`AllocTrailFromDef` 会在 `Count == Capacity` 时直接返回 `null`。

```csharp
if (mTrails.Count == mTrails.Capacity)
{
    return null;
}
```

这个分配边界按容器保留的拖尾总数计算。普通香蒲刺、魅惑香蒲刺和火红莲刺的拖尾都会占用同一个容器的容量。

## 创建者与其他使用者

PGvZ 1.2.6 和 1.4.3 的 `TrailHolder.AllocTrail` 都由以下三种子弹在 `Projectile.ProjectileInitialize` 中调用。

| 子弹类型 | 创建的拖尾 |
|---|---|
| `CattailSpike` | `TrailType.Cattail` |
| `HypnoCattailSpike` | `TrailType.HypnoCattail` |
| `EndoflameSpike` | `TrailType.Endoflame` |

`TrailType.Ice` 在 1.2.6 的资源注册表和存档枚举兼容代码中出现，三处调用均使用表中列出的类型。

其他相关系统的职责如下。

- `EffectSystem` 负责创建、更新、清空容器，并从中删除标记为死亡的拖尾。
- `Attachment` 和 `GlobalMembersAttachment` 查询容器中的拖尾，把拖尾作为附件更新、绘制、分离或销毁。
- `TodLibObjSyncer` 在存读档时同步拖尾列表，并恢复附件对拖尾对象的引用。

## 旧版崩溃调用链

`ProjectileInitialize` 先申请拖尾，再将分配结果交给 `AttachTrail`。

```text
Projectile.ProjectileInitialize
  1. TrailHolder.AllocTrail -> TrailHolder.AllocTrailFromDef
  2. GlobalMembersAttachment.AttachTrail
```

容器满时，`AllocTrailFromDef` 返回 `null`。`AttachTrail` 随即用该值查询并索引拖尾列表。

```csharp
mTrails[mTrails.IndexOf(theTrail)]
```

当 `theTrail` 为 `null` 且列表中没有空元素时，`IndexOf` 返回 `-1`，随后以 `-1` 访问列表并抛出异常。

PGvZ-TAS 过去在低于 1.3.2 的游戏版本中挂钩 `TrailHolder.AllocTrailFromDef`，在原函数运行前将填满的列表容量翻倍。该兼容钩子已从 `pgvztool/hook.py` 移除。
