"""GUI 协议分发器。网络线程只交接数据，所有会话、状态与业务调用由主线程执行。"""
import json
import threading

import Lawn
from pgvz import SetGlobalSpeed
from .cheat_actions import cheat_actions
from .placer import placer
from .sync import sync_reg


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
        self._results = {}
        self._pending = []
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
        with self._lock:
            self._pending.append(request)
        return json.dumps({'action': 'queued', 'id': request_id})

    def run_pending(self):
        """只由 hook.py 调用；交换队列后立即释放锁，在主线程同步执行。"""
        with self._lock:
            pending = self._pending
            self._pending = []
        for request in pending:
            result = {
                'id': request['id'], 'kind': request['kind'],
                'name': request.get('name'),
            }
            try:
                result['value'] = self._execute(request)
                # 保证跨线程回传的是 JSON 数据，不将游戏对象交给网络线程。
                json.dumps(result['value'])
                result['ok'] = True
            except Exception as error:
                result.update(ok=False, error=str(error), errortype=type(error).__name__)
            client_id = request['_clientId']
            with self._lock:
                if request['kind'] == 'release':
                    self._results.pop(client_id, None)
                else:
                    self._results.setdefault(client_id, []).append(result)

    def poll(self, client_id):
        """网络线程只取回该页面的结果；连接尚未获准时也可领取拒绝消息。"""
        self._client_id(client_id)
        with self._lock:
            results = self._results.pop(client_id, [])
        return json.dumps({'action': 'results', 'results': results})

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
