"""修改器叠加绘制：血量、冷却、场地提示、轻松放置和 TAS UI。

挂钩注册和 Camera 变换仍由 hook.py 负责；本模块仅提供绘制辅助函数。
"""
import Lawn
import Sexy
import Sexy.TodLib
from pgvz import GridToPixel, SeedTypeNone
from .cheat import cheat_option
from .placer import placer
from .tas import tas_manager


# 显示植物/僵尸血量

# 潜水僵尸入水时的血条 Y 轴补偿；正数向下。
# 入水动画的可视位置不会写回 GetZombieRect，需要在游戏内调整此值。
SNORKEL_IN_POOL_HP_OFFSET_Y = 90
# 潜水僵尸在水中啃食时会播放上浮动画，但碰撞箱不会跟随动画。
SNORKEL_EATING_IN_POOL_HP_OFFSET_Y = 70
# 海豚僵尸在水中骑行
DOLPHIN_RIDING_HP_OFFSET_Y = 40
# 海豚僵尸在水中行走
DOLPHIN_WALKING_IN_POOL_HP_OFFSET_Y = 60

def DrawPlantHp(plant: Lawn.Plant, g: Sexy.Graphics, marginX: int, offsetY: int, color1, color2):
    if plant.mPlantHealth < plant.mPlantMaxHealth:
        # 一格80x80，画60x5
        numGrid = 2 if plant.mSeedType == Lawn.SeedType.Cobcannon else 1
        totalWidth = 80 * numGrid - 2 * marginX
        x = plant.mX + marginX
        y = plant.mY + offsetY
        hpWidth = totalWidth * plant.mPlantHealth / plant.mPlantMaxHealth
        color_black = Sexy.SexyColor(0, 0, 0, 255).Color
        g.SetColor(color2)
        g.FillRect(x, y, totalWidth, 5)
        g.SetColor(color1)
        g.FillRect(x, y, int(hpWidth), 5)
        g.SetColor(color_black)
        g.DrawRect(x, y, totalWidth, 5)

def DrawPlantHpAll(board: Lawn.Board, g: Sexy.Graphics):
    g.SetColorizeImages(True)
    color1 = Sexy.SexyColor(255, 153, 51, 255).Color  # 橙色
    color2 = Sexy.SexyColor(204, 0, 0, 255).Color  # 深红
    color3 = Sexy.SexyColor(102, 204, 0, 255).Color  # 绿色
    color4 = Sexy.SexyColor(0, 153, 153, 255).Color  # 青色
    NRow = 6 if board.StageHas6Rows() else 5
    NCol = 9
    for gridX in range(NCol):
        for gridY in range(NRow):
            plant = board.GetTopPlantAt(gridX, gridY, Lawn.TopPlant.EatingOrder)
            if plant is None:
                # 只有咖啡豆时 EatingOrder 为空，但咖啡豆仍能被啃食。
                plant = board.GetTopPlantAt(gridX, gridY, Lawn.TopPlant.OnlyFlying)
            if plant is not None:
                if plant.mSeedType != Lawn.SeedType.Cobcannon:
                    DrawPlantHp(plant, g, 10, 60, color1, color2)
                elif gridX == plant.mPlantCol:
                    # 两格查询返回同一门炮，只在左格画；右格有南瓜时也使用上层血条。
                    if board.GetTopPlantAt(gridX + 1, gridY, Lawn.TopPlant.OnlyPumpkin) is not None:
                        DrawPlantHp(plant, g, 10, 50, color3, color4)
                    else:
                        DrawPlantHp(plant, g, 10, 60, color1, color2)
                plant2 = board.GetTopPlantAt(gridX, gridY, Lawn.TopPlant.CatapultOrder)
                if (plant2 is not None and plant is not plant2
                        and (plant2.mSeedType != Lawn.SeedType.Cobcannon
                             or gridX == plant2.mPlantCol)):
                    DrawPlantHp(plant2, g, 10, 50, color3, color4)
    g.SetColorizeImages(False)


PRODUCTION_COOLDOWN_PLANTS = (
    Lawn.SeedType.Sunflower,
    Lawn.SeedType.Twinsunflower,
    Lawn.SeedType.Sunshroom,
    Lawn.SeedType.SunflowerPea,
    Lawn.SeedType.SunflowerWallnut,
    Lawn.SeedType.Marigold,
)


def ProductionCooldown(plant: Lawn.Plant):
    """用单株生产周期作分母，保留游戏随机缩短的效果。"""
    if (plant.mSeedType not in PRODUCTION_COOLDOWN_PLANTS
            or plant.mLaunchRate <= 0 or plant.mLaunchCounter <= 0):
        return None
    app = plant.mApp
    board = plant.mBoard
    if (not plant.IsInPlay() or app.IsIZombieLevel()
            or app.mGameMode in (Lawn.GameMode.Upsell, Lawn.GameMode.Intro)
            or board.HasLevelAwardDropped()
            or (app.mGameMode == Lawn.GameMode.ChallengeLastStand
                and board.mChallenge.mChallengeState != Lawn.ChallengeState.LastStandOnslaught)):
        return None
    if (plant.mSeedType == Lawn.SeedType.Marigold
            and plant.mState == Lawn.PlantState.MarigoldEnding
            and plant.mStateCountdown <= 0):
        return None
    return min(plant.mLaunchCounter, plant.mLaunchRate), plant.mLaunchRate


def PlantCooldown(plant: Lawn.Plant):
    """返回当前冷却剩余帧和本次冷却总帧数；未冷却时返回 None。"""
    state = plant.mState
    seed_type = plant.mSeedType
    remaining = plant.mStateCountdown
    if remaining <= 0:
        return None
    if seed_type == Lawn.SeedType.Cobcannon and state == Lawn.PlantState.CobcannonArming:
        # 初次种植只需 500 帧；发射后的装填需 3000 帧。
        total = 500 if plant.mTargetX == -1 else 3000
    elif seed_type == Lawn.SeedType.Chomper and state == Lawn.PlantState.ChomperDigesting:
        total = 4000
    elif seed_type == Lawn.SeedType.SuperChomper and state == Lawn.PlantState.ChomperDigesting:
        total = 2500
    elif seed_type == Lawn.SeedType.Potatomine and state == Lawn.PlantState.Notready:
        total = 1500
    elif (seed_type == Lawn.SeedType.Magnetshroom
            and state in (Lawn.PlantState.MagnetshroomSucking,
                          Lawn.PlantState.MagnetshroomCharging)):
        total = 1500
    else:
        return None
    return min(remaining, total), total


def DrawPlantCooldowns(board: Lawn.Board, g: Sexy.Graphics, show_plant: bool, show_sun: bool):
    blue = Sexy.SexyColor(51, 153, 255, 255).Color
    dark_blue = Sexy.SexyColor(0, 51, 153, 255).Color
    black = Sexy.SexyColor(0, 0, 0, 255).Color
    g.SetColorizeImages(True)
    for i in range(board.mPlants.Count):
        plant = board.mPlants[i]
        if plant.mDead:
            continue
        if plant.mSeedType in PRODUCTION_COOLDOWN_PLANTS:
            cooldown = ProductionCooldown(plant) if show_sun else None
        else:
            cooldown = PlantCooldown(plant) if show_plant else None
        if cooldown is None:
            continue
        remaining, total = cooldown
        width = 140 if plant.mSeedType == Lawn.SeedType.Cobcannon else 60
        x = plant.mX + 10
        # 血条位于 Y+50（投掷层）或 Y+60（主植物）；此处留至少 5 像素间距。
        y = plant.mY + 40
        g.SetColor(dark_blue)
        g.FillRect(x, y, width, 5)
        g.SetColor(blue)
        g.FillRect(x, y, int(width * remaining / total), 5)
        g.SetColor(black)
        g.DrawRect(x, y, width, 5)
    g.SetColorizeImages(False)

def DrawZombieHp(zombie: Lawn.Zombie, g: Sexy.Graphics, marginX: int, offsetY: int, color1, color2, color3, color4):
    rect = zombie.GetZombieRect()
    totalWidth = rect.mWidth
    x = rect.mX + marginX
    y = rect.mY + offsetY + 20
    # 对一些僵尸的特殊状态修正y轴偏移，使血条位置和视觉一致
    if zombie.mZombieType == Lawn.ZombieType.Snorkel:
        if zombie.mInPool and zombie.mIsEating:
            y += SNORKEL_EATING_IN_POOL_HP_OFFSET_Y
        elif zombie.mZombiePhase == Lawn.ZombiePhase.SnorkelIntoPool or zombie.mInPool:
            y += SNORKEL_IN_POOL_HP_OFFSET_Y
    elif zombie.mZombieType == Lawn.ZombieType.DolphinRider:
        if zombie.mZombiePhase == Lawn.ZombiePhase.DolphinWalkingInPool:
            y += DOLPHIN_WALKING_IN_POOL_HP_OFFSET_Y
        elif zombie.mZombiePhase == Lawn.ZombiePhase.DolphinRiding:
            y += DOLPHIN_RIDING_HP_OFFSET_Y
    # 两类血量
    hpWidth = 0
    hpWidth2 = 0
    plotHp1 = False
    plotHp2 = False
    # 画头盔/本体
    if zombie.mBodyHealth < zombie.mBodyMaxHealth:
        # 考虑血量临界值
        if zombie.CanLoseBodyParts():
            threshold = int(zombie.mBodyMaxHealth / 3)
        else:
            threshold = 0
        hpWidth = totalWidth * (zombie.mBodyHealth - threshold) / (zombie.mBodyMaxHealth - threshold)
        hpWidth = 0 if hpWidth < 0 else hpWidth
        if zombie.mHasHead:
            plotHp1 = True
    if zombie.mHasHelm and zombie.mHelmHealth < zombie.mHelmMaxHealth:
        if zombie.mZombieType == Lawn.ZombieType.Monk:  # 特殊处理武僧僵尸
            hpWidth2 = totalWidth * zombie.mHelmHealth / zombie.mHelmMaxHealth
            plotHp2 = True
        else:
            hpWidth = totalWidth * zombie.mHelmHealth / zombie.mHelmMaxHealth
            plotHp1 = True
    # 画飞行物
    if zombie.IsFlying() and zombie.mFlyingHealth < zombie.mFlyingMaxHealth:
        hpWidth = totalWidth * zombie.mFlyingHealth / zombie.mFlyingMaxHealth
        plotHp1 = True
    # 如果有铁门、梯子等画下面
    if zombie.mHasShield and zombie.mShieldHealth < zombie.mShieldMaxHealth:
        hpWidth2 = totalWidth * zombie.mShieldHealth / zombie.mShieldMaxHealth
        plotHp2 = True
    color_black = Sexy.SexyColor(0, 0, 0, 255).Color
    # 开始绘制
    if plotHp1:
        g.SetColor(color2)
        g.FillRect(x, y, totalWidth, 5)
        g.SetColor(color1)
        g.FillRect(x, y, int(hpWidth), 5)
        g.SetColor(color_black)
        g.DrawRect(x, y, totalWidth, 5)
    if plotHp2:
        g.SetColor(color4)
        g.FillRect(x, y + 10, totalWidth, 5)
        g.SetColor(color3)
        g.FillRect(x, y + 10, int(hpWidth2), 5)
        g.SetColor(color_black)
        g.DrawRect(x, y + 10, totalWidth, 5)

selectZbList = [
    Lawn.ZombieType.Football,
    Lawn.ZombieType.Zamboni,
    Lawn.ZombieType.Gargantuar,
    Lawn.ZombieType.RedeyeGargantuar,
    Lawn.ZombieType.TallnutHead,
    Lawn.ZombieType.RobotTitan,
    Lawn.ZombieType.RedeyeRobotTitan,
    Lawn.ZombieType.Monk,
    Lawn.ZombieType.FootballPremium,
]

def DrawZombieHpAll(board: Lawn.Board, g: Sexy.Graphics):
    g.SetColorizeImages(True)
    color5 = Sexy.SexyColor(255, 51, 255, 255).Color
    color6 = Sexy.SexyColor(127, 0, 255, 255).Color
    color7 = Sexy.SexyColor(255, 0, 127, 255).Color
    color8 = Sexy.SexyColor(153, 0, 76, 255).Color
    mind_color1 = Sexy.SexyColor(51, 204, 102, 255).Color
    mind_color2 = Sexy.SexyColor(0, 102, 51, 255).Color
    mind_color3 = Sexy.SexyColor(51, 204, 255, 255).Color
    mind_color4 = Sexy.SexyColor(0, 102, 153, 255).Color
    for i in range(board.mZombies.Count):
        zombie = board.mZombies[i]
        if not zombie.mHasHead or zombie.IsDeadOrDying():
            continue
        # 只画精英怪
        if cheat_option.selectZombieHp and zombie.mZombieType not in selectZbList:
            continue
        if zombie.mMindControlled:
            DrawZombieHp(zombie, g, 0, 0, mind_color1, mind_color2, mind_color3, mind_color4)
        else:
            DrawZombieHp(zombie, g, 0, 0, color5, color6, color7, color8)
    g.SetColorizeImages(False)

CRATER_COOLDOWN_BAR_WIDTH = 60
CRATER_COOLDOWN_BAR_HEIGHT = 5

def DrawCraterCooldowns(board: Lawn.Board, g: Sexy.Graphics):
    bar_color = Sexy.SexyColor(192, 192, 192, 255).Color
    bar_background = Sexy.SexyColor(128, 128, 128, 255).Color
    max_counter = Lawn.GameConstants.CRATER_TIME

    for i in range(board.mGridItems.Count):
        crater = board.mGridItems[i]
        if (
            crater.mDead
            or crater.mGridItemType != Lawn.GridItemType.Crater
            or crater.mGridItemCounter <= 0
        ):
            continue
        grid_x, grid_y = GridToPixel(board, (crater.mGridX, crater.mGridY))
        bar_x = grid_x + 10
        bar_y = grid_y + 65
        remaining = min(crater.mGridItemCounter, max_counter)
        remaining_width = int(CRATER_COOLDOWN_BAR_WIDTH * remaining / max_counter)

        g.SetColorizeImages(True)
        g.SetColor(bar_background)
        g.FillRect(bar_x, bar_y, CRATER_COOLDOWN_BAR_WIDTH, CRATER_COOLDOWN_BAR_HEIGHT)
        g.SetColor(bar_color)
        g.FillRect(bar_x, bar_y, remaining_width, CRATER_COOLDOWN_BAR_HEIGHT)
        color_black = Sexy.SexyColor(0, 0, 0, 255).Color
        g.SetColor(color_black)
        g.DrawRect(bar_x, bar_y, CRATER_COOLDOWN_BAR_WIDTH, CRATER_COOLDOWN_BAR_HEIGHT)
        g.SetColorizeImages(False)

EASY_PLACE_UI_SCALE = 0.7

def DrawEasyPlaceUI(board: Lawn.Board, g: Sexy.Graphics):
    if board.mApp.mGameScene == Lawn.GameScenes.Playing and board.mApp.mGameMode not in (Lawn.GameMode.ChallengeZenGarden, Lawn.GameMode.TreeOfWisdom, Lawn.GameMode.Upsell, Lawn.GameMode.Intro):
        shovel_rect = board.GetShovelButtonRect()
        glove_rect = board.GetZenButtonRect(Lawn.GameObjectType.Glove)
        btn_w = shovel_rect.mWidth
        btn_h = shovel_rect.mHeight
        btn_y = shovel_rect.mY
        visible_tool_rects = []
        if board.IsCombatToolVisible(Lawn.GameObjectType.Shovel):
            visible_tool_rects.append(shovel_rect)
        if board.IsCombatToolVisible(Lawn.GameObjectType.Glove):
            visible_tool_rects.append(glove_rect)
        if visible_tool_rects:
            slot_gap = max(0, 90 - btn_w)
            btn_x = max(rect.mX + rect.mWidth for rect in visible_tool_rects) + slot_gap
        else:
            btn_x = shovel_rect.mX

        g.DrawImage(Sexy.AtlasResources.IMAGE_SHOVELBANK_ZEN, btn_x, btn_y)
        if placer.active:
            g.SetColorizeImages(True)
            g.SetColor(Sexy.SexyColor(200, 200, 200).Color)
        taco_image = Sexy.AtlasResources.IMAGE_TACO
        taco_x = btn_x - 7
        taco_y = btn_y - 3
        Sexy.TodLib.TodCommon.TodDrawImageCenterScaledF(
            g,
            taco_image,
            float(taco_x),
            float(taco_y),
            EASY_PLACE_UI_SCALE,
            EASY_PLACE_UI_SCALE,
        )
        g.SetColorizeImages(False)

        placer._ep_rect = Sexy.TRect(btn_x, btn_y, btn_w, btn_h)

        # draw selected portal
        if placer.easyPlaceMode == 'portal' and placer.portal_placer.isSelected():
            g.SetColorizeImages(True)
            g.SetColor(Sexy.SexyColor(255, 0, 0).Color)
            g.DrawRect(placer.portal_placer.select_portal_rect)
            g.SetColorizeImages(False)

def DrawSeedPacketNumbers(seedbank: Lawn.SeedBank, g: Sexy.Graphics):
    board = seedbank.mBoard
    if board.mApp.mGameScene != Lawn.GameScenes.Playing or board.mApp.IsSlotMachineLevel():
        return
    if board.mCutScene is not None and board.mCutScene.IsBeforePreloading():
        return

    # SeedBank.Draw 返回时仍保持种子栏的局部坐标，直接沿用其变换与传送带裁剪。
    if board.HasConveyorBeltSeedBank():
        g.SetClipRect(Sexy.Constants.ConveyorBeltClipRect)
    font = Sexy.Resources.FONT_DWARVENTODCRAFT12
    shadow_color = Sexy.SexyColor(0, 0, 0, 220)
    text_color = Sexy.SexyColor(255, 255, 255)
    justification = Sexy.TodLib.DrawStringJustification.LeftVerticalMiddle
    for i in range(seedbank.mNumPackets):
        packet = seedbank.mSeedPackets[i]
        if packet.mPacketType == SeedTypeNone or not packet.BeginDraw(g):
            continue
        text = str(packet.mIndex + 1)
        x = 3
        y = packet.mOffsetY
        Sexy.TodLib.TodCommon.TodDrawString(g, text, x + 1, y + 1, font, shadow_color, justification)
        Sexy.TodLib.TodCommon.TodDrawString(g, text, x, y, font, text_color, justification)
        packet.EndDraw(g)
    if board.HasConveyorBeltSeedBank():
        g.ClearClipRect()

def DrawWaveInfo(board: Lawn.Board, g: Sexy.Graphics):
    # 在进度条下面画波数信息
    if board.HasProgressMeter():
        meterX = Sexy.Constants.UIProgressMeterPosition.X - Sexy.Constants.Board_Offset_AspectRatio_Correction
        meterY = Sexy.Constants.UIProgressMeterPosition.Y
        flagImage = Sexy.AtlasResources.IMAGE_FLAGMETER
        meterWidth = flagImage.GetCelWidth()
        meterHeight = flagImage.GetCelHeight()
        textX = meterX + meterWidth // 2
        textY = meterY + meterHeight
        g.SetColorizeImages(True)
        waveColor = Sexy.SexyColor(255, 255, 255)
        waveFont = Sexy.Resources.FONT_DWARVENTODCRAFT12
        waveText = f'Wave: {board.mCurrentWave}/{board.mNumWaves}'
        Sexy.TodLib.TodCommon.TodDrawString(g, waveText, textX, textY, waveFont, waveColor, Sexy.TodLib.DrawStringJustification.Center)
        cdStr = f'{board.mZombieCountDown}' if board.mZombieCountDown > 0 else '--'
        hugeStr = f'{board.mHugeWaveCountDown}' if board.mHugeWaveCountDown > 0 else '--'
        cdText = f'CD: {cdStr} | Huge: {hugeStr}'
        Sexy.TodLib.TodCommon.TodDrawString(g, cdText, textX, textY + 16, waveFont, waveColor, Sexy.TodLib.DrawStringJustification.Center)
        g.SetColorizeImages(False)

def DrawSquirrel(board: Lawn.Board, g: Sexy.Graphics):
    if board.mApp.mGameMode == Lawn.GameMode.ChallengeSquirrel:
        g.SetColorizeImages(True)
        for i in range(board.mGridItems.Count):
            gridItem = board.mGridItems[i]
            if not gridItem.mDead and gridItem.mGridItemType == Lawn.GridItemType.Squirrel:
                if gridItem.mGridItemState == Lawn.GridItemState.SquirrelZombie:
                    color = Sexy.SexyColor(255, 51, 255, 255).Color
                else:
                    color = Sexy.SexyColor(204, 0, 0, 255).Color  # 深红
                g.SetColor(color)
                mX, mY = GridToPixel(board, (gridItem.mGridX, gridItem.mGridY))
                margin = 10
                g.DrawRect(Sexy.TRect(mX + margin, mY + margin, 80 - 2 * margin, 100 - 2 * margin))
        g.SetColorizeImages(False)

# TAS 按钮 — 右下角，懒初始化
def DrawTasButtons(board: Lawn.Board, g: Sexy.Graphics):
    if tas_manager.buttons is None:
        btnH = Sexy.AtlasResources.IMAGE_BUTTON_LEFT.mHeight
        tas_manager.buttons = []  # type: ignore
        for i, label in enumerate(tas_manager.ACTION_LABELS):
            btn = Lawn.GameButton(9000 + i, board)
            btn.mDrawStoneButton = True
            btn.SetLabel(label)
            btn.Resize(0, 0, 70, btnH)
            tas_manager.buttons.append(btn)    # type: ignore
    # 右下角竖排，等距
    gap = 2
    btnH = tas_manager.buttons[0].mHeight   # type: ignore
    button_count = len(tas_manager.buttons)
    totalH = btnH * button_count + gap * (button_count - 1)
    baseX = board.mWidth - 200
    baseY = board.mHeight - totalH - 30
    for i, btn in enumerate(tas_manager.buttons):    # type: ignore
        btn.Resize(baseX, baseY + i * (btnH + gap), 70, btnH)
        btn.Update()
        btn.Draw(g)

def DrawTasFrameCounter(board: Lawn.Board, g: Sexy.Graphics):
    """右下角显示 mMainCounter"""
    font = Sexy.Resources.FONT_DWARVENTODCRAFT12
    color = Sexy.SexyColor(255, 255, 255)
    text = f'Frame: {board.mMainCounter}'
    x = board.mWidth - 120
    y = board.mHeight - 30
    Sexy.TodLib.TodCommon.TodDrawString(g, text, x, y, font, color, Sexy.TodLib.DrawStringJustification.Right)
