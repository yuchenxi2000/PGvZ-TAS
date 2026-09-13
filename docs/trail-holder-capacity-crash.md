# 拖尾容器容量耗尽崩溃修复

本文依据 PGvZ 1.2.6 的反编译代码，记录 `TrailHolder` 容量耗尽时游戏崩溃的原因，以及 `pgvztool/hook.py` 中现有修复的工作方式。大量香蒲子弹是这个问题的常见触发方式，但底层缺陷不属于香蒲专用逻辑。这里的“香蒲”对应 `SeedType.Cattail`，旧代码注释中也称“猫尾草”。

## 现象与真正的容量限制

香蒲连续产生大量 `ProjectileType.CattailSpike` 时，游戏可能在发射新子弹的瞬间崩溃。问题并非 `Board.mProjectiles` 无法容纳更多子弹，而是每颗香蒲刺在 `Projectile.ProjectileInitialize` 中都会申请一条 `TrailType.Cattail` 拖尾：

```csharp
GlobalMembersAttachment.AttachTrail(
    ref mAttachmentID,
    mApp.mEffectSystem.mTrailHolder.AllocTrail(0, TrailType.Cattail),
    10f,
    10f);
```

所有拖尾共用 `EffectSystem.mTrailHolder.mTrails`。`TrailHolder.InitializeHolder` 将这个 `List<Trail>` 的初始 `Capacity` 设为 128，但原版 `AllocTrailFromDef` 在 `Count == Capacity` 时直接返回 `null`：

```csharp
if (mTrails.Count == mTrails.Capacity)
{
    return null;
}
```

因此，128 是拖尾容器的原版分配边界，不是香蒲子弹的固定数量上限。其他仍由容器保留的拖尾也会占用名额，所以不一定恰好在第 129 颗香蒲子弹时触发。

## 创建者与其他使用者

PGvZ 1.2.6 定义了 `Ice`、`Cattail`、`Endoflame` 和 `HypnoCattail` 四种 `TrailType`，但全局检索反编译代码后，实际调用 `TrailHolder.AllocTrail` 创建拖尾的运行时路径只有以下三处，全部位于 `Projectile.ProjectileInitialize`：

| 子弹类型 | 创建的拖尾 |
|---|---|
| `CattailSpike` | `TrailType.Cattail` |
| `HypnoCattailSpike` | `TrailType.HypnoCattail` |
| `EndoflameSpike` | `TrailType.Endoflame` |

`TrailType.Ice` 在资源注册表和存档枚举兼容代码中出现，但当前版本没有找到调用 `AllocTrail` 创建它的路径。

除此之外，以下系统也会使用 `TrailHolder`，但不会在正常游戏流程中分配新拖尾：

- `EffectSystem` 负责创建、更新、清空容器，并从中删除标记为死亡的拖尾；
- `Attachment` 和 `GlobalMembersAttachment` 查询容器中的拖尾，把拖尾作为附件更新、绘制、分离或销毁；
- `TodLibObjSyncer` 在存读档时同步拖尾列表，并恢复附件对拖尾对象的引用。

所以更准确的描述是：**游戏的共享拖尾容器存在固定容量缺陷，大量香蒲刺通常最容易令其暴露；魅惑香蒲刺、火红莲刺或三者的组合也能占满同一容器。**

## 崩溃调用链

触发路径如下：

```text
Projectile.ProjectileInitialize
  -> TrailHolder.AllocTrail
  -> TrailHolder.AllocTrailFromDef
  -> GlobalMembersAttachment.AttachTrail
```

容器满时，`AllocTrailFromDef` 返回 `null`。`AttachTrail` 没有处理分配失败，而是立即执行：

```csharp
mTrails[mTrails.IndexOf(theTrail)]
```

当 `theTrail` 为 `null` 且列表中没有空元素时，`IndexOf` 返回 `-1`，随后以 `-1` 访问列表并抛出异常。崩溃因此发生在拖尾绑定阶段，而不是香蒲子弹的追踪、碰撞或伤害逻辑中。

## 修改器中的修复

`pgvztool/hook.py` 挂钩 `TrailHolder.AllocTrailFromDef`。调用原函数前，如果列表正好填满，就把容量扩大为原来的两倍：

```python
if trailHolder.mTrails.Count == trailHolder.mTrails.Capacity:
    trailHolder.mTrails.Capacity *= 2
return orig(trailHolder, theRenderOrder, theDefinition)
```

这样进入原函数时 `Count < Capacity`，原有的 `Trail` 初始化、随机持续时间计算和入表逻辑仍由游戏执行。正常初始化的 `TrailHolder` 容量从 128 开始，因此翻倍不会遇到零容量仍为零的问题。

该修复挂在通用拖尾分配入口，所以同时覆盖普通香蒲刺、魅惑香蒲刺和火红莲刺，也会覆盖以后经由该入口创建的其他拖尾。它不是香蒲专用的子弹数量补丁。

## 生命周期与修复边界

子弹死亡时，通常会通过 `AttachmentDie` 结束其附件；死亡拖尾随后由 `EffectSystem.ProcessDeleteQueue` 从 `mTrails` 移除。因此修复没有禁止拖尾回收，也没有让 `Count` 永久增长。

`Capacity` 只是列表已预留的存储空间，扩容后即使活跃拖尾减少，它也可能维持在较大的值。这是 .NET `List<T>` 的正常行为。修复只移除错误的 128 条拖尾硬边界，不限制普通子弹数量、不关闭拖尾效果，也不改变子弹的游戏逻辑。
