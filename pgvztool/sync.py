"""
Serializable 基类和集中同步管理
"""
import json
import time
import traceback
import Sexy
import System


_SESSION_LEASE_SECONDS = 15.0


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
                elif _get_dotnet_enum_type(curr) is not None:
                    setattr(self, k, System.Enum.Parse(curr.GetType(), v))
                elif isinstance(curr, (int, float, str)):
                    setattr(self, k, v)
                # 其他类型跳过


class SyncRegistry:
    def __init__(self):
        self._objects = {}
        self._active_client_id = None
        self._active_client_seen_at = 0.0

    def register(self, name, obj):
        self._objects[name] = obj

    def serialize(self) -> str:
        data = {}
        for name, obj in self._objects.items():
            data[name] = obj.to_dict()
        return json.dumps({"action": "sync", "state": data})

    def _session_is_active(self):
        return (
            self._active_client_id is not None
            and time.time() - self._active_client_seen_at <= _SESSION_LEASE_SECONDS
        )

    def _session_result(self, accepted):
        return json.dumps({
            'action': 'heartbeat' if accepted else 'sessionRejected',
            'accepted': accepted,
        })

    def connect(self, client_id, json_str=None):
        """占用官方 GUI 会话；已有活动页面时拒绝第二个页面。"""
        if not client_id:
            return self._session_result(False)

        if (
            self._session_is_active()
            and self._active_client_id != client_id
        ):
            Sexy.Debug.Log(
                '[pgvztool.sync] rejected client_id={} active_client_id={}'.format(
                    client_id,
                    self._active_client_id,
                )
            )
            return self._session_result(False)

        self._active_client_id = client_id
        self._active_client_seen_at = time.time()

        if json_str is not None:
            self.apply(json_str)
        return self.serialize()

    def heartbeat(self, client_id):
        if client_id == self._active_client_id:
            self._active_client_seen_at = time.time()
            return self._session_result(True)
        return self._session_result(False)

    def require_client(self, client_id):
        """供官方 GUI 在每条指令前校验会话所有权。"""
        if client_id != self._active_client_id:
            raise RuntimeError(
                'another pgvztool GUI session is already active'
            )
        self._active_client_seen_at = time.time()

    def release(self, client_id):
        if client_id == self._active_client_id:
            self._active_client_id = None
            self._active_client_seen_at = 0.0

    def apply(self, json_str):
        name = None
        field = None
        client_id = None
        try:
            msg = json.loads(json_str)
            client_id = msg.get('_clientId')
            if (
                self._session_is_active()
                and client_id != self._active_client_id
            ):
                Sexy.Debug.Log(
                    '[pgvztool.sync] ignored apply from client_id={} active_client_id={}'.format(
                        client_id or '<unknown>',
                        self._active_client_id,
                    )
                )
                return
            is_full_sync = (
                isinstance(msg.get('cheat'), dict)
                and isinstance(msg.get('placer'), dict)
            )
            if is_full_sync and not client_id:
                Sexy.Debug.Log(
                    '[pgvztool.sync] ignored legacy full sync without client_id'
                )
                return
            for name, obj in self._objects.items():
                if name in msg and isinstance(msg[name], dict):
                    # 逐字段应用，便于在同步失败时定位具体属性。
                    for field, value in msg[name].items():
                        obj.from_dict({field: value})
        except Exception:
            _log_apply_error(json_str, name, field, client_id)
            raise


sync_reg = SyncRegistry()
