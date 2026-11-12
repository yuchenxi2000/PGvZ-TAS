"""
持续作弊选项、天气状态及其逐帧脚本
"""
import Lawn
import Lawn.Creative
from pgvz import *
from .sync import Serializable

# 天气控制
class WeatherControl(Serializable):
    def __init__(self) -> None:
        self.enabled = False
        self.rain = False
        self.storm = False

weather = WeatherControl()

# 持续作弊选项；一次性操作见 cheat_actions.py。
class CheatOption(Serializable):
    def __init__(self) -> None:
        self.wontLose = False
        self.freePlant = False
        self._noSunLimit = False
        self._unlockBannedSeeds = False
        self.unlockRake = False
        self.plantAnyWhere = False
        self.plantNoDie = False
        self.zombieNoDie = False
        self.cobNoCooling = False
        self.potatoNoCooling = False
        self.disableTalisman = False
        self.disableNinja = False
        self.jackInTheBoxNoExplode = False
        self.jalapenoHeadNoExplode = False
        self.blowAwayPropeller = False
        self.blowAwayThrownImp = False
        self.visibleGhoul = False
        self.diamondZenTools = False
        self.noFog = False
        self.transScaryPot = False
        self.scaryPotterNoDelay = False
        self.conveyorNoCooling = False
        self.featureThreePeater = False
        self.butterPult = False
        self.doubleGatlingpea = False
        self.fullAreaGloomshroom = False
        self.fullAreaUmbrella = False
        self.planternAlwaysTransform = False
        self.hypnoCattailAlwaysHypnotize = False
        self.allZombiesHypnotizable = False
        self.enableGlove = False
        self.zombieStop = False
        self.chomperNoCooling = False
        self.noCover = False
        self.stopSpawning = False
        self.drawPlantHp = False
        self.drawPlantCooldown = False
        self.drawSunProductionCooldown = False
        self.drawZombieHp = False
        self.selectZombieHp = False
        self.shovelNoReset = False
        self.showShovel = False
        self.runBackground = False
        self.skipLevelIntro = False
        self.gloveNoCooling = False
        self.enableTrashcan = False
        self.showWaveInfo = False
        self.showSeedPacketNumbers = False
        self.showCraterCooldown = False
        self.drawSquirrel = False
        self.tasEnabled = True

    @property
    def noSunLimit(self):
        return self._noSunLimit

    @noSunLimit.setter
    def noSunLimit(self, value):
        self._noSunLimit = value
        if not value:
            board = GetBoard()
            if board is not None and board.mSunMoney > 9990:
                board.mSunMoney = 9990

    # ===== 脚本单例状态（通过 property 暴露给 sync） =====

    @property
    def autoCollect(self):
        return auto_collector.enabled
    @autoCollect.setter
    def autoCollect(self, value):
        auto_collector.On() if value else auto_collector.Off()

    @property
    def unlockBannedSeeds(self):
        return self._unlockBannedSeeds
    @unlockBannedSeeds.setter
    def unlockBannedSeeds(self, value):
        self._unlockBannedSeeds = value
        script_unlock_crazydaveseed.On() if value else script_unlock_crazydaveseed.Off()

    @property
    def infSun(self):
        return script_inf_sun.enabled
    @infSun.setter
    def infSun(self, value):
        script_inf_sun.On() if value else script_inf_sun.Off()

    @property
    def skillNoCooling(self):
        return script_skill_nocooling.enabled
    @skillNoCooling.setter
    def skillNoCooling(self, value):
        script_skill_nocooling.On() if value else script_skill_nocooling.Off()

    @property
    def mushroomAwake(self):
        return script_mushroom_awake.enabled
    @mushroomAwake.setter
    def mushroomAwake(self, value):
        script_mushroom_awake.On() if value else script_mushroom_awake.Off()

    @property
    def autoRestock(self):
        return script_auto_restock.enabled
    @autoRestock.setter
    def autoRestock(self, value):
        script_auto_restock.On() if value else script_auto_restock.Off()

    @property
    def freezePortal(self):
        return script_freeze_portal.enabled

    @freezePortal.setter
    def freezePortal(self, value):
        script_freeze_portal.On() if value else script_freeze_portal.Off()

    @property
    def noCooldown(self):
        return GetLawnApp().mEasyPlantingCheat
    @noCooldown.setter
    def noCooldown(self, value):
        GetLawnApp().mEasyPlantingCheat = value

cheat_option = CheatOption()

# 跳过关卡入场动画。脚本始终运行并记录场景边沿，以支持修改器晚连接、
# 开关动态启用和同一 Board 的生存模式换轮。
_skip_level_intro_state = {
    'board': None,
    'scene': None,
    'enabled': False,
}

def ScriptSkipLevelIntro():
    lawnapp = GetLawnApp()
    board = lawnapp.mBoard
    scene = lawnapp.mGameScene
    enabled = cheat_option.skipLevelIntro
    is_level_intro = board is not None and scene == Lawn.GameScenes.LevelIntro
    entering_intro = is_level_intro and (
        _skip_level_intro_state['board'] is not board
        or _skip_level_intro_state['scene'] != Lawn.GameScenes.LevelIntro
    )
    enabled_during_intro = is_level_intro and enabled and not _skip_level_intro_state['enabled']

    # 先记录状态；CancelIntro 可能弹出 Rose 模态对话框并暂停 Board。
    _skip_level_intro_state['board'] = board
    _skip_level_intro_state['scene'] = scene
    _skip_level_intro_state['enabled'] = enabled

    if not enabled or not (entering_intro or enabled_during_intro):
        return
    if lawnapp.mGameMode in (Lawn.GameMode.Upsell, Lawn.GameMode.Intro):
        return
    cutscene = board.mCutScene
    if cutscene is None or cutscene.mSeedChoosing:
        return
    # 游戏原生会自动取消没有戴夫对话的非滚屏入场，不要重复调用。
    if cutscene.IsNonScrollingCutscene() and cutscene.mCrazyDaveTime == 0:
        return
    cutscene.CancelIntro()

script_manager.Register(ScriptSkipLevelIntro, runmode=ScriptRunMode.GLOBAL)

# 解锁戴夫卡片
def ScriptUnlockCrazyDaveSeed():
    lawnApp = GetLawnApp()
    seedChooser = lawnApp.mSeedChooserScreen
    if seedChooser is None:
        return
    for i in range(65):
        chosenSeed = seedChooser.mChosenSeeds[i]
        if chosenSeed is not None:
            chosenSeed.mCrazyDavePicked = False
script_unlock_crazydaveseed = script_manager.Register(ScriptUnlockCrazyDaveSeed, runmode=ScriptRunMode.FOREVER)
script_unlock_crazydaveseed.Off()

# 无限阳光
def ScriptInfSun():
    GetBoard().mSunMoney = 9990
script_inf_sun = script_manager.Register(ScriptInfSun, runmode=ScriptRunMode.FOREVER)
script_inf_sun.Off()

# 更好的自动收集，包括盆栽。PGvZ-TAS自带，只需引入pgvz模块。关闭只需把下面一句取消注释。
# auto_collector.Off()

# 技能无冷却
def ScriptKillNoCooling():
    GetBoard().mAgavePowerfulCountdown = 0
    GetBoard().mEndoflamePowerfulCountdown = 0
script_skill_nocooling = script_manager.Register(ScriptKillNoCooling, runmode=ScriptRunMode.FOREVER)
script_skill_nocooling.Off()

# 蘑菇清醒
def ScriptMushroomAwake():
    for plant in IterAlivePlants():
        plant.SetSleeping(False)
script_mushroom_awake = script_manager.Register(ScriptMushroomAwake, runmode=ScriptRunMode.FOREVER)
script_mushroom_awake.Off()

# 自动补货
def ScriptAutoRestock():
    playerInfo = GetLawnApp().mPlayerInfo
    if 1000 <= playerInfo.mPurchases[14] <= 1015:
        while playerInfo.mPurchases[14] <= 1015 and playerInfo.mCoins >= 75:
            playerInfo.mPurchases[14] += 5
            playerInfo.mCoins -= 75
    if 1000 <= playerInfo.mPurchases[15] <= 1015:
        while playerInfo.mPurchases[15] <= 1015 and playerInfo.mCoins >= 100:
            playerInfo.mPurchases[15] += 5
            playerInfo.mCoins -= 100
conf_auto_restock = ScriptConf(
    runmode=ScriptRunMode.FOREVER,
    runcond=lambda: GetLawnApp().mGameMode in (
        Lawn.GameMode.ChallengeZenGarden,
        Lawn.GameMode.TreeOfWisdom,
    ),
)
script_auto_restock = script_manager.Register(ScriptAutoRestock, conf=conf_auto_restock)
script_auto_restock.Off()

# 传送门不移动
def ScriptFreezePortal():
    lawnApp = GetLawnApp()
    board = lawnApp.mBoard
    if lawnApp.mGameMode == Lawn.GameMode.ChallengePortalCombat:
        board.mChallenge.mChallengeStateCounter = 6000
        return

    creativeLevel = lawnApp.mCreativeLevel
    if creativeLevel is not None:
        component = creativeLevel.GetComponent[Lawn.Creative.CSSpawnPortal]()
        if component is not None and component.mRandomPortalTime >= 0:
            # Update() 会先减一、再于 <=0 时移动；至少留两帧。
            board.mChallenge.mRandomPortalCounter = max(2, component.mRandomPortalTime)
script_freeze_portal = script_manager.Register(ScriptFreezePortal, runmode=ScriptRunMode.FOREVER)
script_freeze_portal.Off()
