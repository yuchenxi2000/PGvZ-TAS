"""
Serializable 基类和集中同步管理
"""
import json
import traceback
import Sexy
import System
from pgvz import __game_version__
from pgvz.version import MOD_VERSION


class SessionRejected(RuntimeError):
    """页面没有当前 GUI 会话的所有权。"""
    pass


def _log_apply_error(json_str, object_name, field_name, client_id):
    """输出同步异常，但不让日志失败覆盖原异常。"""
    try:
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


def _broadcast_execution_result(value):
    from System.Reflection import Assembly, BindingFlags

    assembly = Assembly.GetAssembly(Sexy.SexyAppBase)
    interactive = assembly.GetType('LawnMod.IronPyInteractive', True)
    server = interactive.GetField('mWS', BindingFlags.NonPublic | BindingFlags.Static).GetValue(None)
    if server is None or not server.IsListening:
        return

    # 与 PyHub.OnMessage 一样，用原生序列化器包装 Python repr，再发给 /Py 的连接。
    serialize = interactive.GetNestedType('PyHub').GetMethod('ExecutionEventJSON')
    status = System.Enum.Parse(serialize.GetParameters()[0].ParameterType, 'executed')
    message = serialize.Invoke(None, System.Array[System.Object]([status, repr(value), None]))
    server.WebSocketServices['/Py'].Sessions.BroadcastAsync(message, None)


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
    """同步状态与 GUI 会话。除初始化注册外，运行时方法均在游戏主线程调用。"""
    def __init__(self):
        self._objects = {}
        self._active_client_id = None
        self._revision = 0
        # 游戏进程内保留；断线、release 和结果缓存清理都不能重新触发恢复。
        self._initialized_clients = set()
        self._revoked_clients = set()
        self._local_fields = set()

    def register(self, name, obj):
        self._objects[name] = obj

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

    def push_state(self, **groups):
        """在游戏主线程向活动网页推送指定组和字段的当前值，None 表示整组。"""
        if self._active_client_id is None:
            return
        try:
            state = self._read_fields(groups)
            if not state:
                return
            message = self._sync_message(state)
            message['_clientId'] = self._active_client_id
            _broadcast_execution_result(json.dumps(message))
        except Exception:
            # 推送失败不应中断游戏主线程的调用者。
            Sexy.Debug.Log(Sexy.DebugType.Error, '[pgvztool.sync] push failed: ' + traceback.format_exc())

    def set_local_state(self, name, field, value):
        """应用游戏内的手动修改，并保护该字段免受网页的首次恢复覆盖。"""
        setattr(self._objects[name], field, value)
        self._local_fields.add((name, field))
        self.push_state(**{name: field})

    def connect(self, client_id, json_str=None, takeover=False):
        """占用官方 GUI 会话；已有活动页面时拒绝第二个页面。"""
        if not client_id or (not takeover and (
            client_id in self._revoked_clients
            or self._active_client_id not in (None, client_id)
        )):
            Sexy.Debug.Log(
                '[pgvztool.sync] rejected client_id={} active_client_id={}'.format(
                    client_id,
                    self._active_client_id,
                )
            )
            return json.dumps({'action': 'sessionRejected', 'accepted': False})

        previous = self._active_client_id
        self._active_client_id = client_id

        try:
            if client_id not in self._initialized_clients and json_str is not None:
                self.apply(json_str, restoring=True)
            result = self.serialize()
        except Exception:
            self._active_client_id = previous
            raise
        self._initialized_clients.add(client_id)
        self._revoked_clients.discard(client_id)
        if previous is not None and previous != client_id:
            self._revoked_clients.add(previous)
        return result

    def require_client(self, client_id):
        """供官方 GUI 在每条指令前校验会话所有权。"""
        if not client_id or client_id != self._active_client_id:
            raise SessionRejected(
                'another pgvztool GUI session is already active'
            )

    def release(self, client_id):
        if client_id == self._active_client_id:
            self._active_client_id = None

    def apply(self, json_str, *, return_sync=False, restoring=False):
        name = field = client_id = None
        try:
            msg = json.loads(json_str)
            client_id = msg.get('_clientId')
            self.require_client(client_id)
            groups = {}
            for name, obj in self._objects.items():
                data = msg.get(name)
                if isinstance(data, dict):
                    for field, value in data.items():
                        if restoring and (name, field) in self._local_fields:
                            continue
                        obj.from_dict({field: value})
                    groups[name] = data
            if return_sync:
                state = self._read_fields(groups)
                if state:
                    return self._sync_message(state)
        except Exception:
            _log_apply_error(json_str, name, field, client_id)
            raise


sync_reg = SyncRegistry()
