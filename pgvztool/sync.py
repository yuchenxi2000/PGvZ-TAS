"""
Serializable 基类和集中同步管理
"""
import json


def _serialize(v):
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        return v
    if hasattr(v, 'real'):   # C# enum
        return str(v)
    return None              # 不序列化的类型


class Serializable:
    def to_dict(self) -> dict:
        result = {}
        # 实例属性
        for k, v in vars(self).items():
            if k.startswith('_') or callable(v):
                continue
            val = _serialize(v)
            if val is not None:
                result[k] = val
        # @property（类级别定义的属性描述符）
        for k in dir(type(self)):
            if k.startswith('_'):
                continue
            attr = getattr(type(self), k, None)
            if isinstance(attr, property) and attr.fget is not None:
                val = _serialize(getattr(self, k))
                if val is not None:
                    result[k] = val
        return result

    def from_dict(self, data):
        for k, v in data.items():
            if hasattr(self, k) and not k.startswith('_'):
                curr = getattr(self, k)
                if isinstance(curr, bool):
                    setattr(self, k, v)
                elif hasattr(curr, 'real'):       # C# enum
                    setattr(self, k, getattr(type(curr), v))
                elif isinstance(curr, (int, float, str)):
                    setattr(self, k, v)
                # 其他类型跳过


class SyncRegistry:
    def __init__(self):
        self._objects = {}

    def register(self, name, obj):
        self._objects[name] = obj

    def serialize(self) -> str:
        data = {}
        for name, obj in self._objects.items():
            data[name] = obj.to_dict()
        return json.dumps({"action": "sync", "state": data})

    def apply(self, json_str):
        msg = json.loads(json_str)
        for name, obj in self._objects.items():
            if name in msg and isinstance(msg[name], dict):
                obj.from_dict(msg[name])


sync_reg = SyncRegistry()
