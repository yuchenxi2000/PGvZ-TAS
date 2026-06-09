import json
from .cheat import cheat_option, script_inf_sun, script_skill_nocooling
from .placer import placer
from pgvz import GetLawnApp, auto_collector

# ========== 状态查询（供手机端网页从游戏同步状态） ==========
def get_cheat_state():
    state = {}
    # 常规选项直接从 cheat_option 属性读取
    regular_attrs = [
        'wontLose', 'freePlant', 'plantAnyWhere', 'zombieNoDie',
        'cobNoCooling', 'potatoNoCooling', 'disableTalisman', 'disableNinja',
        'visibleGhoul', 'noThunder', 'diamondZenTools', 'noFog',
        'transScaryPot', 'conveyorNoCooling', 'featureThreePeater',
        'butterPult', 'doubleGatlingpea', 'fullAreaGloomshroom',
        'enableGlove', 'zombieStop', 'chomperNoCooling', 'noCover',
        'stopSpawning', 'drawPlantHp', 'drawZombieHp', 'selectZombieHp',
        'shovelNoReset', 'runBackground', 'gloveNoCooling', 'plantNoDie',
        'enableTrashcan',
    ]
    for attr in regular_attrs:
        state[attr] = getattr(cheat_option, attr, False)
    # 特殊选项（状态不在 cheat_option 上）
    state['autoCollect'] = auto_collector.enabled
    state['infSun'] = script_inf_sun.enabled
    state['skillNoCooling'] = script_skill_nocooling.enabled
    state['noCooldown'] = GetLawnApp().mEasyPlantingCheat
    # placer状态
    state['seedType'] = str(placer.seedType)
    state['zombieType'] = str(placer.zombieType)
    state['gridItemType'] = str(placer.gridItemType)
    state['coinType'] = str(placer.coinType)
    state['mindCtrl'] = placer.mindCtrl
    state['potReverse'] = placer.potReverse
    state['imitater'] = placer.imitater
    state['easyPlaceMode'] = placer.easyPlaceMode
    state['easyPlaceEnabled'] = placer.easyPlaceEnabled
    return json.dumps({"action": "sync", "options": state})
