"""GUI 协议分发器。网络线程只交接数据，所有会话、状态与业务调用由主线程执行。"""
import json
import threading
import time

import Lawn
from pgvz import SetGlobalSpeed
from .cheat_actions import cheat_actions
from .placer import placer
from .sync import sync_reg


REQUEST_TIMEOUT_SECONDS = 30.0
RESULT_RETENTION_SECONDS = 60.0


REQUEST_KINDS = ('connect', 'apply', 'snapshot', 'action', 'heartbeat', 'release')


def _integer(value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError('expected an integer')
    if not -2147483648 <= value <= 2147483647:
        raise ValueError('integer is outside the C# int range')
    return value


def _boolean(value):
    if not isinstance(value, bool):
        raise TypeError('expected a boolean')
    return value


def _string(value):
    if not isinstance(value, str):
        raise TypeError('expected a string')
    return value


def _enum(enum_type):
    def convert(value):
        member = getattr(enum_type, _string(value), None)
        if not isinstance(member, enum_type):
            raise ValueError('unknown {} member: {}'.format(enum_type.__name__, value))
        return member
    return convert


def _zombie_list(value):
    if not isinstance(value, list):
        raise TypeError('expected a list of zombie names')
    return [_enum(Lawn.ZombieType)(item) for item in value]


class GuiDispatcher:
    def __init__(self):
        # 此锁只保护跨线程的数据交接；业务执行期间不持锁，也不需要递归锁。
        self._lock = threading.Lock()
        self._records = {}
        self._pending = []
        self._next_order = 0
        seed = _enum(Lawn.SeedType)
        zombie = _enum(Lawn.ZombieType)
        grid_item = _enum(Lawn.GridItemType)
        coin = _enum(Lawn.CoinType)
        mode = _enum(Lawn.GameMode)
        cell = (('row', _integer), ('col', _integer))
        # 参数顺序属于网页 API；后端方法名、C# 枚举和字段只在这里映射。
        self._actions = {
            'setSun': (cheat_actions.SetSun, (('value', _integer),)),
            'setMoney': (cheat_actions.SetMoney, (('value', _integer),)),
            'setChocolate': (cheat_actions.SetChocolate, (('value', _integer),)),
            'setTreeHeight': (cheat_actions.SetTreeHeight, (('value', _integer),)),
            'setAdventureLevel': (cheat_actions.SetAdventureLevel, (('value', _integer),)),
            'setFinishedAdventure': (cheat_actions.SetFinishedAdventure, (('value', _integer),)),
            'winLevel': (cheat_actions.WinLevel, ()),
            'nextStage': (cheat_actions.NextStage, ()),
            'loseLevel': (cheat_actions.LoseLevel, ()),
            'toggleFullscreen': (cheat_actions.ToggleFullscreen, ()),
            'completeAccount': (cheat_actions.CompleteAccount, ()),
            'perfectAccount': (cheat_actions.PerfectAccount, ()),
            'placePlant': (placer.PlantOnBoard, cell + (('seedType', seed), ('imitater', _boolean))),
            'placeZombie': (placer.ZombieOnBoard, cell + (('zombieType', zombie), ('mindCtrl', _boolean))),
            'setSeedPacket': (placer.SetSeedPacket, (('index', _integer), ('seedType', seed), ('imitater', _boolean))),
            'placeGridItem': (placer.PlaceGridItem, cell + (
                ('gridItemType', grid_item), ('potType', _string),
                ('appearance', _enum(Lawn.GridItemState)), ('zombieType', zombie), ('seedType', seed))),
            'dropCoin': (placer.AddCoinOnBoard, (
                ('x', _integer), ('y', _integer), ('coinType', coin), ('seedType', seed), ('reverse', _boolean))),
            'placeIce': (placer.PlaceIceOnBoard, cell),
            'smartLadder': (placer.AddLadderSmart, ()),
            'givePottedPlant': (cheat_actions.GivePottedPlant, (('seedType', seed), ('reverse', _boolean))),
            'giveAllPottedPlants': (cheat_actions.GiveAllPottedPlants, ()),
            'placeMower': (placer.AddLawnMower, ()),
            'startMower': (placer.StartLawnMower, ()),
            'infiniteMowers': (placer.InfiniteLawnMowers, ()),
            'removePlants': (placer.RemovePlantOnBoard, ()),
            'removeZombies': (placer.RemoveZombieOnBoard, (('enemyOnly', _boolean),)),
            'removeCoins': (placer.RemoveCoinOnBoard, (('coinType', coin),)),
            'removeGridItems': (placer.RemoveGridItemOnBoard, cell + (('gridItemType', grid_item),)),
            'removeIce': (placer.RemoveIceOnBoard, cell),
            'removeTalisman': (placer.RemoveTalisman, ()),
            'removeMowers': (placer.RemoveLawnMower, ()),
            'openScaryPots': (placer.OpenScaryPotterOnBoard, ()),
            'setSpeed': (SetGlobalSpeed, (('value', lambda value: value),)),
            'enterLevel': (cheat_actions.EnterNewGame, (('mode', mode),)),
            'setGameMode': (cheat_actions.SetGameMode, (('mode', mode),)),
            'setSurvivalStage': (cheat_actions.SetSurvivalStage, (('value', _integer),)),
            'enterMoonEndless': (cheat_actions.EnterMoonEndless, ()),
            'setZombies': (cheat_actions.CheatSetZombies, (('types', _zombie_list), ('natural', _boolean))),
            'applyLineup': (cheat_actions.LineUpOnBoard, (('code', _string),)),
            'getLineup': (cheat_actions.GetLineup, ()),
        }

    def submit(self, json_str):
        """WebSocket 线程入口：仅解析和排队，不读取会话或游戏对象。"""
        request = json.loads(json_str)
        if not isinstance(request, dict):
            raise TypeError('GUI request must be an object')
        self._client_id(request.get('_clientId'))
        request_id = request.get('id')
        if not isinstance(request_id, str) or not request_id:
            raise ValueError('request ID is required')
        if request.get('kind') not in REQUEST_KINDS:
            raise ValueError('unknown GUI request kind')
        key = request['_clientId'], request_id
        with self._lock:
            self._cleanup_locked()
            record = self._records.get(key)
            if record is not None:
                if record['request'] != request:
                    raise ValueError('request ID was already used with different data')
                # 同一请求只执行一次；重复提交可再次领取缓存结果。
                record['acknowledged'] = False
                record['abandoned'] = False
            else:
                self._next_order += 1
                record = {
                    'request': request, 'created': time.monotonic(), 'finished': None,
                    'status': 'pending', 'result': None, 'order': self._next_order,
                    'acknowledged': False, 'abandoned': False,
                }
                self._records[key] = record
                self._pending.append(record)
        return json.dumps({'action': 'queued', 'id': request_id})

    def _error_result(self, request, error_type, message):
        return {'id': request['id'], 'kind': request['kind'], 'name': request.get('name'),
                'ok': False, 'errortype': error_type, 'error': message}

    def _finish_locked(self, record, result):
        record['status'] = 'done'
        record['finished'] = time.monotonic()
        record['result'] = result
        record['acknowledged'] = record['abandoned']

    def _cleanup_locked(self):
        now = time.monotonic()
        expired = []
        for key, record in self._records.items():
            if record['status'] == 'pending' and now - record['created'] >= REQUEST_TIMEOUT_SECONDS:
                self._finish_locked(record, self._error_result(
                    record['request'], 'RequestExpired', 'request expired before execution'))
            elif record['status'] == 'done' and now - record['finished'] >= RESULT_RETENTION_SECONDS:
                expired.append(key)
        for key in expired:
            del self._records[key]
        self._pending = [record for record in self._pending if record['status'] == 'pending']

    def run_pending(self):
        """只由 hook.py 调用；业务执行期间不持队列锁。"""
        with self._lock:
            self._cleanup_locked()
            pending = self._pending
            self._pending = []
        for record in pending:
            with self._lock:
                self._cleanup_locked()
                if record['status'] != 'pending':
                    continue
                record['status'] = 'running'
            request = record['request']
            result = {'id': request['id'], 'kind': request['kind'], 'name': request.get('name')}
            try:
                result['value'] = self._execute(request)
                json.dumps(result['value'])
                result['ok'] = True
            except Exception as error:
                result.update(ok=False, error=str(error), errortype=type(error).__name__)
            with self._lock:
                self._finish_locked(record, result)
                if request['kind'] == 'release':
                    for other in self._records.values():
                        if other['request']['_clientId'] == request['_clientId'] and other['status'] == 'done':
                            other['acknowledged'] = True

    def poll(self, client_id):
        """结果保留至 ack 或过期；轮询响应丢失不会丢掉已执行动作的结果。"""
        self._client_id(client_id)
        with self._lock:
            self._cleanup_locked()
            records = sorted(self._records.values(), key=lambda record: record['order'])
            results = [record['result'] for record in records
                       if record['request']['_clientId'] == client_id
                       and record['status'] == 'done' and not record['acknowledged']]
        return json.dumps({'action': 'results', 'results': results})

    def _request_ids(self, client_id, json_ids):
        self._client_id(client_id)
        ids = json.loads(json_ids)
        if not isinstance(ids, list) or any(not isinstance(value, str) for value in ids):
            raise TypeError('request IDs must be a list of strings')
        return [(client_id, value) for value in ids]

    def acknowledge(self, client_id, json_ids):
        keys = self._request_ids(client_id, json_ids)
        with self._lock:
            self._cleanup_locked()
            for key in keys:
                record = self._records.get(key)
                if record is not None and record['status'] == 'done':
                    record['acknowledged'] = True
        return json.dumps({'action': 'acknowledged'})

    def cancel(self, client_id, json_ids):
        keys = self._request_ids(client_id, json_ids)
        with self._lock:
            self._cleanup_locked()
            for key in keys:
                record = self._records.get(key)
                if record is None:
                    continue
                record['abandoned'] = True
                if record['status'] == 'pending':
                    self._finish_locked(record, self._error_result(
                        record['request'], 'RequestCancelled', 'request cancelled before execution'))
                elif record['status'] == 'done':
                    record['acknowledged'] = True
                # running 不能安全中断；完成后只保留缓存，不再主动回传。
        return json.dumps({'action': 'cancelled'})

    def _client_id(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError('client ID is required')

    def _execute(self, request):
        client_id = request['_clientId']
        kind = request['kind']
        if kind == 'connect':
            state = request.get('state')
            if state is not None and not isinstance(state, dict):
                raise TypeError('initial state must be an object')
            payload = dict(state, _clientId=client_id) if state is not None else None
            return json.loads(sync_reg.connect(client_id, json.dumps(payload) if payload is not None else None))
        if kind == 'heartbeat':
            return json.loads(sync_reg.heartbeat(client_id))
        if kind == 'release':
            return sync_reg.release(client_id)

        sync_reg.require_client(client_id)
        if kind == 'apply':
            state = request.get('state')
            if not isinstance(state, dict):
                raise TypeError('state must be an object')
            return sync_reg.apply(json.dumps(dict(state, _clientId=client_id)))
        if kind == 'snapshot':
            return json.loads(sync_reg.serialize())

        name = request.get('name')
        if not isinstance(name, str) or name not in self._actions:
            raise ValueError('unknown GUI action: {}'.format(name))
        handler, fields = self._actions[name]
        arguments = request.get('args', {})
        if not isinstance(arguments, dict) or set(arguments) != set(key for key, _ in fields):
            raise ValueError('invalid arguments for {}'.format(name))
        values = [convert(arguments[key]) for key, convert in fields]
        return handler(*values)


gui_dispatcher = GuiDispatcher()
