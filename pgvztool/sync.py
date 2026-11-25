"""
Serializable 基类和集中同步管理
"""
import json
import threading
import Sexy
import System
from pgvz import __game_version__
from pgvz.version import MOD_VERSION


class SessionRejected(RuntimeError):
    """页面尚未加入或已退出 GUI 会话。"""
    pass


def _log_apply_error(json_str, object_name, field_name, client_id):
    """输出同步异常，但不让日志失败覆盖原异常。"""
    try:
        import traceback
        message = (
            '[pgvztool.sync] apply failed\n'
            'client_id: {}\n'
            'object: {}\n'
            'field: {}\n'
            'payload: {}\n'
            'traceback:\n{}'
        ).format(
            client_id or '<unknown>',
            object_name or '<unknown>',
            field_name or '<unknown>',
            json_str,
            traceback.format_exc(),
        )
        Sexy.Debug.Log(Sexy.DebugType.Error, message)
    except Exception:
        pass


def _get_dotnet_enum_type(v):
    try:
        enum_type = v.GetType()
        return enum_type if enum_type.IsEnum else None
    except Exception:
        return None


def _serialize(v):
    if _get_dotnet_enum_type(v) is not None:
        return str(v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, str):
        return v
    return None              # 不序列化的类型


class Serializable:
    def to_dict(self, fields=None) -> dict:
        attributes = vars(self)
        cls = type(self)
        if fields is None:
            fields = list(attributes)
            fields.extend(k for k in dir(cls) if isinstance(getattr(cls, k, None), property))
        result = {}
        for k in fields:
            if k.startswith('_'):
                continue
            descriptor = getattr(cls, k, None)
            if k not in attributes and not (isinstance(descriptor, property) and descriptor.fget is not None):
                continue
            value = _serialize(getattr(self, k))
            if value is not None:
                result[k] = value
        return result

    def from_dict(self, data):
        for k, v in data.items():
            if k.startswith('_'):
                continue
            curr = getattr(self, k, None)
            enum_type = _get_dotnet_enum_type(curr)
            if enum_type is not None:
                try:
                    v = System.Enum.Parse(enum_type, v)
                except Exception:
                    # 无法转换的枚举值跳过，不影响其余选项。
                    continue
            elif not isinstance(curr, (bool, int, float, str)):
                continue
            try:
                setattr(self, k, v)
            except (AttributeError, TypeError, ValueError):
                # 属性不存在、只读或无法赋值时跳过。
                continue


class SyncRegistry:
    """同步状态与 GUI 会话。网络线程只能读取已序列化的状态更新。"""
    def __init__(self):
        self._objects = {}
        self._read_only_groups = set()
        self._clients = set()
        self._revision = 0
        self._update_lock = threading.Lock()
        self._updates = {}
        self._initial_sync_done = False
        self._local_fields = set()

    def register(self, name, obj, *, read_only=False):
        self._objects[name] = obj
        if read_only:
            self._read_only_groups.add(name)
        else:
            self._read_only_groups.discard(name)

    @property
    def has_active_client(self):
        return bool(self._clients)

    def _sync_message(self, state):
        self._revision += 1
        return {
            'action': 'sync', 'state': state, 'revision': self._revision,
            'modVersion': MOD_VERSION, 'gameVersion': __game_version__,
        }

    def serialize(self) -> str:
        data = {name: obj.to_dict() for name, obj in self._objects.items()}
        return json.dumps(self._sync_message(data))

    def _read_fields(self, groups):
        patch = {}
        for name, fields in groups.items():
            obj = self._objects.get(name)
            if obj is None:
                continue
            if isinstance(fields, str):
                fields = (fields,)
            values = obj.to_dict() if fields is None else obj.to_dict(fields)
            if values:
                patch[name] = values
        return patch

    def read_state(self, **groups):
        state = self._read_fields(groups)
        return self._sync_message(state) if state else None

    def push_state(self, **groups):
        """在游戏主线程保存指定字段的当前值，供活动网页领取。"""
        if not self._clients:
            return
        try:
            self.publish_state(self.read_state(**groups))
        except Exception:
            import traceback
            Sexy.Debug.Log(Sexy.DebugType.Error, '[pgvztool.sync] push failed: ' + traceback.format_exc())

    def publish_state(self, message):
        """在游戏主线程发布已生成的同步消息，保留动作回包的修订号。"""
        if message is None:
            return
        with self._update_lock:
            for group, fields in message['state'].items():
                for field, value in fields.items():
                    self._updates[group, field] = message['revision'], value

    def poll_updates(self, client_id, after_revision):
        """按原修订号返回各字段最新的值，避免覆盖更新的动作回包。"""
        with self._update_lock:
            if client_id not in self._clients:
                return []
            updates = {}
            for (group, field), (revision, value) in self._updates.items():
                if revision > after_revision:
                    updates.setdefault(revision, {}).setdefault(group, {})[field] = value
        return [{'action': 'sync', 'revision': revision, 'state': updates[revision]}
                for revision in sorted(updates)]

    def set_local_state(self, name, field, value):
        """应用游戏内的手动修改，并保护该字段免受网页的首次恢复覆盖。"""
        setattr(self._objects[name], field, value)
        self._local_fields.add((name, field))
        self.push_state(**{name: field})

    def connect(self, client_id, json_str=None):
        """加入会话并读取快照；每个游戏进程只有一次初始设置恢复。"""
        if not client_id:
            raise ValueError('client ID is required')
        if not self._initial_sync_done and json_str is not None:
            self._apply(json_str, restoring=True)
        result = self.serialize()
        with self._update_lock:
            self._clients.add(client_id)
        self._initial_sync_done = True
        return result

    def require_client(self, client_id):
        """供官方 GUI 在每条指令前校验该页面的会话。"""
        if client_id not in self._clients:
            raise SessionRejected('this pgvztool GUI page is not connected')

    def release(self, client_id):
        with self._update_lock:
            self._clients.discard(client_id)
            if not self._clients:
                self._updates.clear()

    def apply(self, json_str, *, return_sync=False):
        return self._apply(json_str, return_sync=return_sync)

    def _apply(self, json_str, *, return_sync=False, restoring=False):
        name = field = client_id = None
        try:
            msg = json.loads(json_str)
            client_id = msg.get('_clientId')
            if not restoring:
                self.require_client(client_id)
            groups = {}
            for name, obj in self._objects.items():
                data = msg.get(name)
                if name not in self._read_only_groups and isinstance(data, dict):
                    for field, value in data.items():
                        if restoring and (name, field) in self._local_fields:
                            continue
                        obj.from_dict({field: value})
                    groups[name] = data
            if return_sync:
                return self.read_state(**groups)
        except Exception:
            _log_apply_error(json_str, name, field, client_id)
            raise


sync_reg = SyncRegistry()
