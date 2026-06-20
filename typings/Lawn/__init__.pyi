import typing, clr, abc
from Sexy import Widget, TRect, Insets, WidgetContainer, FlagsMod, WidgetManager, Graphics, Image, ScrollWidget, DialogListener, Font, DialogButton, TPoint, SexyColor, ButtonListener, AchievementId, KeyCode, SexyChar, Buffer, _Touch, ButtonWidget, Main, SexyAppBase, Dialog, UI_ORIENTATION, MusicInterface, ResourceManager, ScreenScales, SoundManager, Constants, SexyVector2, MemoryImage, LayoutFlags, BufferNew, HyperlinkWidget, TriVertex
from System.Collections.Generic import List_1, LinkedListNode_1, LinkedList_1, Dictionary_2, IEnumerable_1
from Microsoft.Xna.Framework import Color, Vector2, GameTime
from System import Array_1, IEquatable_1, TimeSpan, DateTime, IComparable, Exception
from Sexy.TodLib import Reanimation, TodWeightedGridArray, TodWeightedArray, TodParticleSystem, TodSmoothArray, ParticleEffect, TodCurves, DrawStringJustification, FilterEffectType, ParticleParams, ReanimationParams, TodStringListFormat, TrailParams, EffectSystem, TodFoley, FoleyType, ReanimationType, ReanimLoopType, Attachment, DataArray_1
from Microsoft.Xna.Framework.Content import ContentManager
from Microsoft.Xna.Framework.Graphics import Texture2D, SpriteFont, GraphicsDevice
from System.Collections.Concurrent import ConcurrentQueue_1
from Microsoft.Xna.Framework.GamerServices import SignedInEventArgs, Gamer
from System.Collections import IDictionary
from System.Reflection import MethodBase

class Achievement:
    def __init__(self, aImageId: int, aName: str, aDesc: str) -> None: ...
    mDesc : str
    mImageId : int
    mName : str


class AchievementsWidget(Widget):
    def __init__(self, theApp: LawnApp) -> None: ...
    BackButtonRect : TRect
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...


class AdviceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ClickOnSun : AdviceType # 0
    ClickedOnSun : AdviceType # 1
    ClickedOnCoin : AdviceType # 2
    SeedRefresh : AdviceType # 3
    CantAffordPlant : AdviceType # 4
    PlantGravebustersOnGraves : AdviceType # 5
    PlantLilypadOnWater : AdviceType # 6
    PlantTanglekelpOnWater : AdviceType # 7
    PlantSeashroomOnWater : AdviceType # 8
    PlantPotatoMineOnLily : AdviceType # 9
    PlantWrongArtType : AdviceType # 10
    PlantNeedPot : AdviceType # 11
    PlantNotOnGrave : AdviceType # 12
    PlantNotOnCrater : AdviceType # 13
    CantPlantThere : AdviceType # 14
    PlantNotOnWater : AdviceType # 15
    PlantingNeedsGround : AdviceType # 16
    BeghouledDragToMatch3 : AdviceType # 17
    BeghouledMatch3 : AdviceType # 18
    BeghouledMatch4 : AdviceType # 19
    BeghouledSaveSun : AdviceType # 20
    BeghouledUseCrater1 : AdviceType # 21
    BeghouledUseCrater2 : AdviceType # 22
    PlantNotPassedLine : AdviceType # 23
    PlantOnlyOnRepeaters : AdviceType # 24
    PlantOnlyOnMelonpult : AdviceType # 25
    PlantOnlyOnSunflower : AdviceType # 26
    PlantOnlyOnSpikeweed : AdviceType # 27
    PlantOnlyOnKernelpult : AdviceType # 28
    PlantOnlyOnMagnetshroom : AdviceType # 29
    PlantOnlyOnFumeshroom : AdviceType # 30
    PlantOnlyOnLilypad : AdviceType # 31
    PlantNeedsRepeater : AdviceType # 32
    PlantNeedsMelonpult : AdviceType # 33
    PlantNeedsSunflower : AdviceType # 34
    PlantNeedsSpikeweed : AdviceType # 35
    PlantNeedsKernelpult : AdviceType # 36
    PlantNeedsMagnetshroom : AdviceType # 37
    PlantNeedsFumeshroom : AdviceType # 38
    PlantNeedsLilypad : AdviceType # 39
    SlotMachinePull : AdviceType # 40
    HugeWave : AdviceType # 41
    ShovelRefresh : AdviceType # 42
    PortalRelocating : AdviceType # 43
    SlotMachineCollectSun : AdviceType # 44
    DestroyPotsToFinisihLevel : AdviceType # 45
    UseShovelOnPots : AdviceType # 46
    AlmostThere : AdviceType # 47
    ZombiquariumClickTrophy : AdviceType # 48
    ZombiquariumCollectSun : AdviceType # 49
    ZombiquariumClickToFeed : AdviceType # 50
    ZombiquariumBuySnorkel : AdviceType # 51
    IZombiePlantsNotReal : AdviceType # 52
    IZombieNotPassedLine : AdviceType # 53
    IZombieLeftOfLine : AdviceType # 54
    SlotMachineSpinAgain : AdviceType # 55
    IZombieEatAllBrains : AdviceType # 56
    PeashooterDied : AdviceType # 57
    StinkySleeping : AdviceType # 58
    BeghouledNoMoves : AdviceType # 59
    PlantSunflower5 : AdviceType # 60
    PlantingNeedSleeping : AdviceType # 61
    ClickToContinue : AdviceType # 62
    SurviveFlags : AdviceType # 63
    UnlockedMode : AdviceType # 64
    NeedWheelbarrow : AdviceType # 65
    AchievementEarned : AdviceType # 66
    PlantOnlyOnChomper : AdviceType # 67
    PlantNeedsChomper : AdviceType # 68
    PlantEndoflameOnLily : AdviceType # 69
    CelSealed : AdviceType # 70
    JalapenoSealed : AdviceType # 71
    PickledPepperSealed : AdviceType # 72
    AdviceTypeCount : AdviceType # 73
    None_ : AdviceType # -1


class AlmanacDialog(LawnDialog):
    def __init__(self, theApp: LawnApp, theListener: AlmanacListener) -> None: ...
    FullRect : TRect
    gZombieDefeated : Array_1[bool]
    mApp : LawnApp
    mApp : LawnApp
    mBackgroundInsets : Insets
    mButtonDelay : int
    mButtonHeight : int
    mButtonHorzSpacing : int
    mButtonMode : int
    mButtonSidePadding : int
    mClip : bool
    mCloseButton : GameButton
    mColors : List_1[Color]
    mComponentImage : Image
    mContentInsets : Insets
    mDescriptionScrollWidget : ScrollWidget
    mDescriptionWidget : DescriptionWidget
    mDialogFooter : str
    mDialogHeader : str
    mDialogLines : str
    mDialogListener : DialogListener
    mDisabled : bool
    mDoFinger : bool
    mDragging : bool
    mDragMouseX : int
    mDragMouseY : int
    mDrawStandardBack : bool
    mFullViewCountdown : int
    mHalfDeltaHeight : int
    mHalfDeltaWidth : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeaderFont : Font
    mHeight : int
    mId : int
    mIndexButton : GameButton
    mInFullView : bool
    mIsDown : bool
    mIsModal : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLawnNoButton : LawnStoneButton
    mLawnYesButton : LawnStoneButton
    mLinesFont : Font
    mLineSpacingOffset : int
    mListener : AlmanacListener
    mMinWidth : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNoButton : DialogButton
    mNumButtons : int
    mOpenPage : AlmanacPage
    mParent : WidgetContainer
    mPlant : Plant
    mPlantGalleryWidget : PlantGalleryWidget
    mPlantsScrollWidget : ScrollWidget
    mPriority : int
    mReanim : Array_1[Reanimation]
    mReanimation : ReanimationWidget
    mResult : int
    mSelectedSeed : SeedType
    mSelectedZombie : ZombieType
    mShowTachieButton : GameButton
    mSpaceAfterHeader : int
    mTabNext : Widget
    mTabPrev : Widget
    mTallBottom : bool
    mTextAlign : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVerticalCenterText : bool
    mViewPlantsRect : TRect
    mViewZombiesRect : TRect
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mYesButton : DialogButton
    mZombie : Zombie
    mZombieGalleryWidget : ZombieGalleryWidget
    mZombiesScrollWidget : ScrollWidget
    mZOrder : int
    ZombieOffsets : Array_1[TPoint]
    @staticmethod
    def AlmanacInitForPlayer() -> None: ...
    @staticmethod
    def AlmanacPlayerDefeatedZombie(theZombieType: ZombieType) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def ClearPlantsAndZombies(self) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawIndex(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def DrawPaper(self, g: Graphics, theRect: TRect, theColor: SexyColor) -> None: ...
    def DrawPlants(self, g: Graphics) -> None: ...
    def DrawZombies(self, g: Graphics) -> None: ...
    def KeyChar(self, theChar: str) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def PlantSelected(self, theSeedType: SeedType) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def SetPage(self, thePage: AlmanacPage) -> None: ...
    def SetupPlant(self) -> None: ...
    def SetupZombie(self) -> None: ...
    def ShowPlant(self, theSeedType: SeedType) -> None: ...
    def ShowZombie(self, theZombieType: ZombieType) -> None: ...
    def Update(self) -> None: ...
    def UpdateScreen(self) -> None: ...
    def UpdateUIPosition(self) -> None: ...
    def ZombieHasDescription(self, theZombieType: ZombieType) -> bool: ...
    def ZombieHasSilhouette(self, theZombieType: ZombieType) -> bool: ...
    def ZombieSelected(self, theZombieType: ZombieType) -> None: ...


class AlmanacListener(typing.Protocol):
    @abc.abstractmethod
    def BackFromAlmanac(self) -> None: ...


class AlmanacPage(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Index : AlmanacPage # 0
    Plants : AlmanacPage # 1
    Zombies : AlmanacPage # 2


class AlmanacZombieData:
    def __init__(self, mType: ZombieType, mX: int, mY: int) -> None: ...
    mType : ZombieType
    mX : int
    mY : int


class AlmanacZombieDataContainer(abc.ABC):
    mData : Array_1[AlmanacZombieData]


class AwardScreen(Widget, ButtonListener, StoreListener, AlmanacListener):
    def __init__(self, theApp: LawnApp, theAwardType: AwardType, theShowAchievements: bool) -> None: ...
    FullRect : TRect
    mAchievementAnimTime : int
    mAchievementItems : List_1[AwardScreen.AchievementScreenItem]
    mApp : LawnApp
    mAwardType : AwardType
    mClip : bool
    mColors : List_1[Color]
    mContinueButton : GameButton
    mCreditsButton : NewLawnButton
    mDisabled : bool
    mDoFinger : bool
    mFadeInCounter : int
    mHalfDeltaHeight : int
    mHalfDeltaWidth : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMenuButton : GameButton
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mShowingAchievements : bool
    mShowMenuButtonAfterAchievements : bool
    mShowStartButtonAfterAchievements : bool
    mStartButton : GameButton
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AchievementsContinuePressed(self) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def BackFromAlmanac(self) -> None: ...
    def BackFromStore(self) -> None: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, id: int) -> None: ...
    def ButtonMouseEnter(self, id: int) -> None: ...
    def ButtonMouseLeave(self, id: int) -> None: ...
    def ButtonMouseMove(self, id: int, x: int, y: int) -> None: ...
    def ButtonMouseTick(self, id: int) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawAchievements(self, g: Graphics) -> None: ...
    def DrawAwardSeed(self, g: Graphics) -> None: ...
    def DrawBottom(self, g: Graphics, theTitle: str, theAward: str, theMessage: str) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def IsPaperNote(self) -> bool: ...
    def KeyChar(self, theChar: str) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def StartButtonPressed(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateScreen(self) -> None: ...
    def UpdateUIPosition(self) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, id: int, id2: int) -> None:...


    class AchievementScreenItem:
        def __init__(self) -> None: ...
        mDestY : int
        mEndAnimTime : int
        mId : AchievementId
        mStartAnimTime : int
        mStartY : int
        mY : int



class AwardScreens(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AwardScreenStart : AwardScreens # 100
    AwardScreenMenu : AwardScreens # 101


class AwardType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ForLevel : AwardType # 0
    CreditsZombieNote : AwardType # 1
    HelpZombieNote : AwardType # 2
    AchievementOnly : AwardType # 3
    PreCreditsZombieNote : AwardType # 4


class BackgroundType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Num1Day : BackgroundType # 0
    Num2Night : BackgroundType # 1
    Num3Pool : BackgroundType # 2
    Num4Fog : BackgroundType # 3
    Num5Roof : BackgroundType # 4
    Num6Boss : BackgroundType # 5
    MushroomGarden : BackgroundType # 6
    Greenhouse : BackgroundType # 7
    Zombiquarium : BackgroundType # 8
    TreeOfWisdom : BackgroundType # 9
    GreenhouseNight : BackgroundType # 10
    ShallowDay : BackgroundType # 11
    HighGround : BackgroundType # 12
    BigPool : BackgroundType # 13


class BeghouledBoardState:
    mSeedType : Array_1[SeedType]
    @staticmethod
    def GetNewBeghouledBoardState() -> BeghouledBoardState: ...
    def PrepareForReuse(self) -> None: ...


class BeghouledUpgrade(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Repeater : BeghouledUpgrade # 0
    Fumeshroom : BeghouledUpgrade # 1
    Tallnut : BeghouledUpgrade # 2
    BeghouledUpgradeCount : BeghouledUpgrade # 3


class Board(Widget, AlmanacListener, ButtonListener):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, theApp: LawnApp) -> None: ...
    aGridArray : Array_1[TodWeightedGridArray]
    aPickArray : Array_1[TodWeightedArray]
    aZombieWeightArray : Array_1[TodWeightedArray]
    FIRST_MINIGAME_UNLOCK_LEVEL : int
    FullRect : TRect
    gShownMoreSunTutorial : bool
    LevelLimit : int
    mAccelerateButton : GameButton
    mAccelerationDenominator : int
    mAccelerationFrameIndex : int
    mAccelerationNumerator : int
    mAdvice : MessageWidget
    mAgavePowerfulCountdown : int
    mAgaveSkillDrawType : int
    mApp : LawnApp
    mBackground : BackgroundType
    mBoardFadeOutCounter : int
    mBoardRandSeed : int
    mBonusLawnMowersRemaining : int
    mCamera : Board.Camera
    mCameraEnabled : bool
    mCatapultPlantsUsed : bool
    mChallenge : Challenge
    mChocolateCollected : int
    mClip : bool
    mCobCannonCursorDelayCounter : int
    mCobCannonMouseX : int
    mCobCannonMouseY : int
    mCoinBankFadeCount : int
    mCoins : List_1[Coin]
    mCoinsCollected : int
    mCollectedCoinStreak : int
    mColors : List_1[Color]
    mCoverLayerAnimIDs : Array_1[Reanimation]
    mCoverLayerAnimIDs_Save : Array_1[int]
    mCurrentWave : int
    mCursorObject : CursorObject
    mCursorPreview : CursorPreview
    mCutScene : CutScene
    mDaisyMode : bool
    mDanceMode : bool
    mDebugTextMode : DebugTextMode
    mDiamondsCollected : int
    mDisabled : bool
    mDoFinger : bool
    mDoomsUsed : int
    mDoPlaceRose : bool
    mDrawCount : int
    mDroppedFirstCoin : bool
    mEffectCounter : int
    mEnableGraveStones : bool
    mEndoflamePowerfulCountdown : int
    mEndoflameSkillDrawType : int
    mFinalBossKilled : bool
    mFinalWaveSoundCounter : int
    mFlagRaiseCounter : int
    mFogBlownCountDown : int
    mFogOffset : float
    mFutureMode : bool
    mFwooshCountDown : int
    mFwooshID : Array_1[Reanimation]
    mFwooshID_Save : Array_1[int]
    mGameID : int
    mGargantuarsKillsByCornCob : int
    mGravesCleared : int
    mGridCelFog : Array_1[int]
    mGridCelLook : Array_1[int]
    mGridCelOffset : Array_1[int]
    mGridItems : List_1[GridItem]
    mGridSquareType : Array_1[GridSquareType]
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mHelpDisplayed : Array_1[bool]
    mHelpIndex : AdviceType
    mHugeWaveCountDown : int
    mIceMinX : Array_1[int]
    mIceParticleID : Array_1[ParticleSystemID]
    mIceTimer : Array_1[int]
    mIceTrapCounter : int
    mIgnoreMouseUp : bool
    mIgnoreNextMouseUp : bool
    mIgnoreNextMouseUpSeedPacket : bool
    mIntervalDrawCountStart : int
    mIntervalDrawTime : int
    mIsCheatDown : bool
    mIsDown : bool
    mIsOver : bool
    mKilledYeti : bool
    mLastBungeeWave : int
    mLastToolX : int
    mLastToolY : int
    mLastWMUpdateCount : int
    mLawnMowers : List_1[LawnMower]
    mLevel : int
    mLevelAwardSpawned : bool
    mLevelComplete : bool
    mLevelFadeCount : int
    mLevelStr : str
    mMainCounter : int
    mManualPaused : bool
    mMaxSunPlants : int
    mMenuButton : GameButton
    mMinFPS : float
    mMouseInsets : Insets
    mMouseVisible : bool
    mMushroomAndCoffeeBeansOnly : bool
    mMushroomsUsed : bool
    mMustacheMode : bool
    mNextSurvivalStageCounter : int
    mNoFungusAmongUsAchievementTracker : bool
    mNomNomNomAchievementTracker : bool
    mNumSunsFallen : int
    mNumWaves : int
    mNutsUsed : bool
    mOutOfMoneyCounter : int
    mParent : WidgetContainer
    mPauseButton : GameButton
    mPaused : bool
    mPeaShooterUsed : bool
    mPinataMode : bool
    mPlanternOrBloverUsed : bool
    mPlantRow : Array_1[PlantRowType]
    mPlants : List_1[Plant]
    mPlantsEaten : int
    mPlantsShoveled : int
    mPlayTimeActiveLevel : int
    mPlayTimeInactiveLevel : int
    mPoolSparklyParticleID : TodParticleSystem
    mPoolSparklyParticleID_Save : int
    mPottedPlantsCollected : int
    mPreloadTime : int
    mPrevBoardResult : BoardResult
    mPrevMouseX : int
    mPrevMouseY : int
    mPriority : int
    mProgressMeterWidth : int
    mProjectiles : List_1[Projectile]
    mRiseFromGraveCounter : int
    mRowPickingArray : Array_1[TodSmoothArray]
    mScoreNextMowerCounter : int
    mSealedCountdown : int
    mSeedBank : SeedBank
    mShakeAmountX : int
    mShakeAmountY : int
    mShakeCounter : int
    mShowShovel : bool
    mSodPosition : int
    mSpecialGraveStoneX : int
    mSpecialGraveStoneY : int
    mStartDrawTime : int
    mStoreButton : GameButton
    mSukhbirMode : bool
    mSunCountDown : int
    mSunMoney : int
    mSuperMowerMode : bool
    mTabNext : Widget
    mTabPrev : Widget
    mTimeStopCounter : int
    mTotalSpawnedWaves : int
    mTriggeredLawnMowers : int
    mTutorialParticleID : TodParticleSystem
    mTutorialParticleID_Save : int
    mTutorialState : TutorialState
    mTutorialTimer : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWaveRowGotLawnMowered : Array_1[int]
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mWinds : List_1[Wind]
    mWindSum : Vector2
    mX : int
    mY : int
    mZombieAllowed : Array_1[bool]
    mZombieCountDown : int
    mZombieCountDownStart : int
    mZombieHealthToNextWave : int
    mZombieHealthWaveStart : int
    mZombies : List_1[Zombie]
    mZombiesInWave : Array_1[ZombieType]
    mZombiesRow1 : List_1[Zombie]
    mZombiesRow2 : List_1[Zombie]
    mZombiesRow3 : List_1[Zombie]
    mZombiesRow4 : List_1[Zombie]
    mZombiesRow5 : List_1[Zombie]
    mZombiesRow6 : List_1[Zombie]
    mZOrder : int
    PUZZLE_UNLOCK_LEVEL : int
    TRIALMODE_LEVEL_LIMIT : int
    def AccelerationDecrease(self) -> None: ...
    def AccelerationIncrease(self) -> None: ...
    def AddACrater(self, theGridX: int, theGridY: int) -> GridItem: ...
    def AddAGraveStone(self, theGridX: int, theGridY: int) -> GridItem: ...
    def AddALadder(self, theGridX: int, theGridY: int) -> GridItem: ...
    def AddBossRenderItem(self, theRenderList: Array_1[RenderItem], theCurRenderItem: clr.Reference[int], theBossZombie: Zombie) -> None: ...
    def AddCoin(self, theX: int, theY: int, theCoinType: CoinType, theCoinMotion: CoinMotion) -> Coin: ...
    def AddCoinForDropLootType(self, theX: int, theY: int, theDropLootType: DropLootType) -> None: ...
    def AddGraveStones(self, theGridX: int, theCount: int) -> None: ...
    def AddPlant(self, theGridX: int, theGridY: int, theSeedType: SeedType, theImitaterType: SeedType) -> Plant: ...
    def AddProjectile(self, theX: int, theY: int, aRenderOrder: int, theRow: int, projectileType: ProjectileType) -> Projectile: ...
    def AddWind(self, windType: WindType) -> None: ...
    def AreEnemyZombiesOnScreen(self) -> bool: ...
    def AttachCamera(self, theCamera: Board.Camera) -> None: ...
    def AwardCloseShave(self) -> bool: ...
    def BackButtonPress(self) -> bool: ...
    def BackFromAlmanac(self) -> None: ...
    @staticmethod
    def BoardInitForPlayer() -> None: ...
    def BungeeDropZombie(self, theBungeeDropGrid: BungeeDropGrid, theZombieType: ZombieType) -> None: ...
    def BungeeIsTargetingCell(self, theCol: int, theRow: int) -> bool: ...
    def ButtonDepress(self, id: int) -> None: ...
    def ButtonDownTick(self, id: int) -> None: ...
    def ButtonMouseEnter(self, theId: int) -> None: ...
    def ButtonMouseLeave(self, theId: int) -> None: ...
    def ButtonMouseMove(self, id: int, x: int, y: int) -> None: ...
    def ButtonMouseTick(self, id: int) -> None: ...
    def CanAddBobSled(self) -> bool: ...
    def CanAddGraveStoneAt(self, theGridX: int, theGridY: int) -> bool: ...
    def CanCancelAgaveSkill(self) -> bool: ...
    def CanCancelEndoflameSkill(self) -> bool: ...
    def CanDropLoot(self) -> bool: ...
    def CanDropPresentMinigames(self) -> bool: ...
    def CanDropPresentPuzzleMode(self) -> bool: ...
    def CanInteractWithBoardButtons(self) -> bool: ...
    def CanPlaceRake(self) -> bool: ...
    def CanPlantAt(self, theGridX: int, theGridY: int, theType: SeedType, aIsMovePlant: bool = ...) -> PlantingReason: ...
    def CanTakeSunMoney(self, theAmount: int) -> bool: ...
    def CanUseGameObject(self, theGameObject: GameObjectType) -> bool: ...
    @staticmethod
    def CanZombieSpawnOnLevel(theZombieType: ZombieType, theLevel: int) -> bool: ...
    def CheckForPostGameAchievements(self) -> bool: ...
    def ChooseSeedsOnCurrentLevel(self) -> bool: ...
    def ClearAdvice(self, theHelpIndex: AdviceType) -> None: ...
    def ClearAdviceImmediately(self) -> None: ...
    def ClearCursor(self) -> None: ...
    def ClearFogAroundPlant(self, thePlant: Plant, theSize: int) -> None: ...
    def CompleteEndLevelSequenceForSaving(self) -> None: ...
    def CountCoinByType(self, theCoinType: CoinType) -> int: ...
    def CountCoinsBeingCollected(self) -> int: ...
    def CountEmptyPotsOrLilies(self, theSeedType: SeedType) -> int: ...
    def CountPlantByType(self, theSeedType: SeedType) -> int: ...
    def CountSunBeingCollected(self) -> int: ...
    def CountSunFlowers(self) -> int: ...
    def CountUntriggerLawnMowers(self) -> int: ...
    def CountZombiesOnScreen(self) -> int: ...
    def CreateRakeReanim(self, rakeX: float, rakeY: float, renderOrder: int) -> Reanimation: ...
    def DeselectSeedPacket(self) -> None: ...
    def DetachCamera(self) -> None: ...
    def DisplayAdviceAgain(self, theAdvice: str, theMessageStyle: MessageStyle, theHelpIndex: AdviceType) -> None: ...
    def Dispose(self) -> None: ...
    def DisposeBoard(self) -> None: ...
    def DoFusionEvent(self, theGridX: int, theGridY: int, theSeedType: SeedType, theImitaterType: SeedType) -> None: ...
    def DoFwoosh(self, theRow: int) -> None: ...
    def DoFwooshLine(self, theX: int) -> None: ...
    def DoPlantingEffects(self, theGridX: int, theGridY: int, thePlant: Plant, forAquarium: bool) -> None: ...
    def DoPlantingSound(self, thePlant: Plant) -> None: ...
    def DoSleepingSound(self, thePlant: Plant) -> None: ...
    def DoTypingCheck(self, theKey: KeyCode) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawAgaveInfo(self, g: Graphics) -> None: ...
    def DrawBackdrop(self, g: Graphics) -> None: ...
    def DrawCelHighlight(self, g: Graphics, theCol: int, theRow: int) -> None: ...
    def DrawCoverLayer(self, g: Graphics, theRow: int) -> None: ...
    def DrawCursorOnBackground(self, g: Graphics) -> None: ...
    def DrawCursorOverlay(self, g: Graphics) -> None: ...
    def DrawEndoflameInfo(self, g: Graphics) -> None: ...
    def DrawFadeOut(self, g: Graphics) -> None: ...
    def DrawFog(self, g: Graphics) -> None: ...
    def DrawGameObjects(self, g: Graphics) -> None: ...
    def DrawHouseDoorBottom(self, g: Graphics) -> None: ...
    def DrawHouseDoorTop(self, g: Graphics) -> None: ...
    def DrawIce(self, g: Graphics, y: int) -> None: ...
    def DrawLevel(self, g: Graphics) -> None: ...
    def DrawProgressMeter(self, g: Graphics) -> None: ...
    def DrawShovel(self, g: Graphics) -> None: ...
    def DrawTopRightUI(self, g: Graphics, theDrawElements: Board.TopRightUIDrawMode = ...) -> None: ...
    def DrawUIBottom(self, g: Graphics) -> None: ...
    def DrawUICoinBank(self, g: Graphics) -> None: ...
    def DrawUITop(self, g: Graphics) -> None: ...
    def DrawZenButtons(self, g: Graphics) -> None: ...
    def DrawZenWheelBarrowButton(self, g: Graphics, theOffsetY: int) -> None: ...
    def DropLootPiece(self, thePosX: int, thePosY: int, theDropFactor: int) -> None: ...
    def DropLootPieceWithResult(self, theDropFactor: int) -> DropLootType: ...
    def DropLootTypeToCoinType(self, theDropLootType: DropLootType) -> CoinType: ...
    def FadeOutLevel(self) -> None: ...
    def FindLawnMowerInRow(self, theRow: int) -> LawnMower: ...
    def FindUmbrellaPlant(self, theGridX: int, theGridY: int) -> Plant: ...
    def FreezeEffectsForCutscene(self, theFreeze: bool) -> None: ...
    def GetAgaveSkillRect(self) -> TRect: ...
    def GetBossZombie(self) -> Zombie: ...
    def GetBottomLawnMower(self) -> LawnMower: ...
    def GetCelPosition(self, theCol: int, theRow: int) -> Array_1[TPoint]: ...
    def GetCraterAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetCurrentPlantCost(self, theSeedType: SeedType, theImitaterType: SeedType) -> int: ...
    def GetEndoflameSkillRect(self) -> TRect: ...
    def GetFlowerPotAt(self, theGridX: int, theGridY: int) -> Plant: ...
    def GetGraveStoneAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetGraveStoneCount(self) -> int: ...
    def GetGridItemAt(self, theGridItemType: GridItemType, theGridX: int, theGridY: int) -> GridItem: ...
    def GetIceZPos(self, theRow: int) -> int: ...
    def GetIntroducedZombieType(self) -> ZombieType: ...
    def GetLadderAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetLevelRandSeed(self) -> int: ...
    def GetLiveGargantuarCount(self) -> int: ...
    def GetNumSeedsInBank(self) -> int: ...
    def GetNumWavesPerFlag(self) -> int: ...
    def GetNumWavesPerSurvivalStage(self) -> int: ...
    def GetPlantsOnLawn(self, theGridX: int, theGridY: int, thePlantOnLawn: clr.Reference[PlantsOnLawn]) -> None: ...
    def GetPosYBasedOnRow(self, thePosX: float, theRow: int) -> float: ...
    def GetPumpkinAt(self, theGridX: int, theGridY: int) -> Plant: ...
    def GetRake(self) -> GridItem: ...
    def GetScaryPotAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetSeedPacketPositionY(self, theIndex: int) -> int: ...
    def GetSeedTypeInCursor(self) -> SeedType: ...
    def GetShovelButtonRect(self) -> TRect: ...
    def GetSquirrelAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetSurvivalFlagsCompleted(self) -> int: ...
    def GetTalismanAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetTopPlantAt(self, theGridX: int, theGridY: int, thePriority: TopPlant) -> Plant: ...
    def GetWinningZombie(self) -> Zombie: ...
    def GetZenButtonRect(self, theObjectType: GameObjectType) -> TRect: ...
    def GetZenShovelButtonRect(self) -> TRect: ...
    def GetZenToolAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetZombiesInRow(self, aRow: int) -> List_1[Zombie]: ...
    def GridToPixelX(self, theGridX: int, theGridY: int) -> int: ...
    def GridToPixelY(self, theGridX: int, theGridY: int) -> int: ...
    def HasConveyorBeltSeedBank(self) -> bool: ...
    def HasFusion(self) -> bool: ...
    def HasGlove(self) -> bool: ...
    def HasLevelAwardDropped(self) -> bool: ...
    def HasProgressMeter(self) -> bool: ...
    def HasTrashcan(self) -> bool: ...
    def HasValidCobCannonSpot(self) -> bool: ...
    def HighlightPlantsForMouse(self, theMouseX: int, theMouseY: int) -> None: ...
    def InitCoverLayer(self) -> None: ...
    def InitLawnMowers(self) -> None: ...
    def InitLevel(self) -> None: ...
    def InitSurvivalStage(self) -> None: ...
    def InitZombieWaves(self) -> None: ...
    def InitZombieWavesForLevel(self, aForLevel: int) -> None: ...
    def IsFinalScaryPotterStage(self) -> bool: ...
    def IsFinalSurvivalStage(self) -> bool: ...
    def IsFlagWave(self, theWaveNumber: int) -> bool: ...
    def IsFungus(self, aCheckSeed: SeedType) -> bool: ...
    def IsIceAt(self, theGridX: int, theGridY: int) -> bool: ...
    @staticmethod
    def IsInModRange(number: int, mod: int) -> bool: ...
    def IsLastStandFinalStage(self) -> bool: ...
    def IsLastStandStageWithRepick(self) -> bool: ...
    def IsPlantInCursor(self) -> bool: ...
    def IsPlantInGoldWateringCanRange(self, theMouseX: int, theMouseY: int, thePlant: Plant) -> bool: ...
    def IsPoolSquare(self, theGridX: int, theGridY: int) -> bool: ...
    def IsScaryPotterDaveTalking(self) -> bool: ...
    def IsSurvivalStageWithRepick(self) -> bool: ...
    def IsValidCobCannonSpot(self, theGridX: int, theGridY: int) -> bool: ...
    def IsValidCobCannonSpotHelper(self, theGridX: int, theGridY: int) -> bool: ...
    def IsValidCobCannonSpotMovePlant(self, theGridX: int, theGridY: int) -> bool: ...
    @staticmethod
    def IsZombieTypePoolOnly(theZombieType: ZombieType) -> bool: ...
    def IsZombieWaveDistributionOk(self) -> bool: ...
    def IterateCoins(self, theCoin: clr.Reference[Coin]) -> bool: ...
    def IterateGridItems(self, theGridItem: clr.Reference[GridItem], index: clr.Reference[int]) -> bool: ...
    def IterateLawnMowers(self, theLawnMower: clr.Reference[LawnMower]) -> bool: ...
    def IterateParticles(self, theParticle: clr.Reference[TodParticleSystem], index: clr.Reference[int]) -> bool: ...
    def IteratePlants(self, thePlant: clr.Reference[Plant], index: clr.Reference[int]) -> bool: ...
    def IterateProjectiles(self, theProjectile: clr.Reference[Projectile], index: clr.Reference[int]) -> bool: ...
    def IterateReanimations(self, theReanimation: clr.Reference[Reanimation], index: clr.Reference[int]) -> bool: ...
    def IterateZombies(self, theZombie: clr.Reference[Zombie], index: clr.Reference[int]) -> bool: ...
    def KeyChar(self, theChar: SexyChar) -> None: ...
    def KeyDown(self, theKey: KeyCode) -> None: ...
    def KeyUp(self, theKey: KeyCode) -> None: ...
    def KillAllPlantsInRadius(self, theX: int, theY: int, theRadius: int) -> None: ...
    def KillAllZombiesInRadius(self, theRow: int, theX: int, theY: int, theRadius: int, theRowRange: int, theBurn: bool, theDamageRangeFlags: int) -> int: ...
    def LeftFogColumn(self) -> int: ...
    def LoadBackgroundImages(self) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadGame(self, theFilePath: str) -> bool: ...
    @staticmethod
    def MakeRenderOrder(theRenderLayer: RenderLayer, theRow: int, theLayerOffset: int) -> int: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseDownCobcannonFire(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseDownInternal(self, x: int, y: int, theClickCount: int, isTouch: bool) -> None: ...
    def MouseDownWithPlant(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseDownWithTool(self, x: int, y: int, theClickCount: int, theCursorType: CursorType, posScaled: bool, isTouch: bool) -> None: ...
    def MouseDrag(self, x: int, y: int) -> None: ...
    def MouseHitTest(self, x: int, y: int, theHitResult: clr.Reference[HitResult], posScaled: bool, isTouch: bool = ...) -> bool: ...
    def MouseHitTestPlant(self, x: int, y: int, theHitResult: clr.Reference[HitResult], posScaled: bool) -> bool: ...
    def MouseMove(self, x: int, y: int) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseUpInternal(self, x: int, y: int, theClickCount: int, isTouch: bool) -> None: ...
    def MouseUpWithPlant(self, x: int, y: int, theClickCount: int) -> None: ...
    def Move(self, theNewX: int, theNewY: int) -> None: ...
    def NeedSaveGame(self) -> bool: ...
    def NewPlant(self, theGridX: int, theGridY: int, theSeedType: SeedType, theImitaterType: SeedType) -> Plant: ...
    def NextWaveComing(self) -> None: ...
    def NumberZombiesInWave(self, theWaveIndex: int) -> int: ...
    def OffsetYForPlanting(self, theY: clr.Reference[int], theSeedType: SeedType) -> None: ...
    def Pause(self, thePause: bool) -> None: ...
    def PickBackground(self) -> None: ...
    def PickGraveRisingZombieType(self, theZombiePoints: int) -> ZombieType: ...
    def PickRowForNewZombie(self, theZombieType: ZombieType) -> int: ...
    def PickSpecialGraveStone(self) -> None: ...
    def PickUpTool(self, theObjectType: GameObjectType) -> None: ...
    def PickZombieType(self, theZombiePoints: int, theWaveIndex: int, theZombiePicker: ZombiePicker) -> ZombieType: ...
    def PickZombieWaves(self) -> None: ...
    def PixelToGridX(self, theX: int, theY: int) -> int: ...
    def PixelToGridXKeepOnBoard(self, theX: int, theY: int) -> int: ...
    def PixelToGridY(self, theX: int, theY: int) -> int: ...
    def PixelToGridYKeepOnBoard(self, theX: int, theY: int) -> int: ...
    def PlaceRake(self) -> None: ...
    def PlantingPixelToGridX(self, theX: int, theY: int, theSeedType: SeedType) -> int: ...
    def PlantingPixelToGridY(self, theX: int, theY: int, theSeedType: SeedType) -> int: ...
    def PlantingRequirementsMet(self, theSeedType: SeedType) -> bool: ...
    def PlantUsesAcceleratedPricing(self, theSeedType: SeedType) -> bool: ...
    def ProcessDeleteQueue(self) -> None: ...
    def ProgressMeterHasFlags(self) -> bool: ...
    def PutInMissingZombies(self, theWaveNumber: int, theZombiePicker: ZombiePicker) -> None: ...
    def PutZombieInWave(self, theZombieType: ZombieType, theWaveNumber: int, theZombiePicker: ZombiePicker) -> None: ...
    def PuzzleSaveStreak(self) -> None: ...
    def RefreshSeedPacketFromCursor(self) -> None: ...
    def RemoveAllZombies(self) -> None: ...
    def RemoveCutsceneZombies(self) -> None: ...
    def RemoveParticleByType(self, theEffectType: ParticleEffect) -> None: ...
    def RemoveZombiesForRepick(self) -> None: ...
    def ResetFPSStats(self) -> None: ...
    def RowCanHaveZombies(self, theRow: int) -> bool: ...
    def RowCanHaveZombieType(self, theRow: int, theZombieType: ZombieType) -> bool: ...
    def SaveGame(self, theFilePath: str) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def SeedNotRecommendedForLevel(self, theSeedType: SeedType) -> int: ...
    def SetDaisyMode(self, theEnableDaisy: bool) -> None: ...
    def SetDanceMode(self, theEnableDance: bool) -> None: ...
    def SetFutureMode(self, theEnableFuture: bool) -> None: ...
    def SetMustacheMode(self, theEnableMustache: bool) -> None: ...
    def SetPinataMode(self, theEnablePinata: bool) -> None: ...
    def SetSukhbirMode(self, theEnableSukhbir: bool) -> None: ...
    def SetSuperMowerMode(self, theEnableSuperMower: bool) -> None: ...
    def SetTutorialState(self, theTutorialState: TutorialState) -> None: ...
    def SetupBungeeDrop(self, theBungeeDropGrid: BungeeDropGrid) -> None: ...
    def ShakeBoard(self, theShakeAmountX: int, theShakeAmountY: int) -> None: ...
    def ShowCoinBank(self) -> None: ...
    def SortZombieRowLists(self) -> None: ...
    def SpawnZombiesFromGraves(self) -> None: ...
    def SpawnZombiesFromPool(self) -> None: ...
    def SpawnZombiesFromSky(self) -> None: ...
    def SpawnZombieWave(self) -> None: ...
    def SpecialPlantHitTest(self, x: int, y: int) -> Plant: ...
    def StageHas6Rows(self) -> bool: ...
    def StageHasBigPool(self) -> bool: ...
    def StageHasFog(self) -> bool: ...
    def StageHasGraveStones(self) -> bool: ...
    def StageHasNinja(self) -> bool: ...
    def StageHasPool(self) -> bool: ...
    def StageHasRoof(self) -> bool: ...
    def StageHasZombieWalkInFromRight(self) -> bool: ...
    def StageIsDayWithoutPool(self) -> bool: ...
    def StageIsNight(self) -> bool: ...
    def StartLevel(self) -> None: ...
    def StopAllZombieSounds(self) -> None: ...
    def SurvivalSaveScore(self) -> None: ...
    def TakeSunMoney(self, theAmount: int) -> bool: ...
    def ToolHitTest(self, x: int, y: int, posScaled: bool, isTouch: bool) -> HitResult: ...
    def TotalZombiesHealthInWave(self, theWaveIndex: int) -> int: ...
    def TouchBegan(self, touch: _Touch) -> None: ...
    def TouchEnded(self, touch: _Touch) -> None: ...
    def TouchMoved(self, touch: _Touch) -> None: ...
    def TrashcanHitTest(self, x: int, y: int) -> bool: ...
    def TryToSaveGame(self) -> None: ...
    def TutorialArrowRemove(self) -> None: ...
    def TutorialArrowShow(self, x: int, y: int) -> None: ...
    def Update(self) -> None: ...
    def UpdateCoverLayer(self) -> None: ...
    def UpdateCursor(self) -> None: ...
    def UpdateFog(self) -> None: ...
    def UpdateFwoosh(self) -> None: ...
    def UpdateGame(self) -> None: ...
    def UpdateGameObjects(self) -> None: ...
    def UpdateGridItems(self) -> None: ...
    def UpdateIce(self) -> None: ...
    def UpdateLayers(self) -> None: ...
    def UpdateLevelEndSequence(self) -> None: ...
    def UpdateMousePosition(self) -> None: ...
    def UpdateProgressMeter(self) -> None: ...
    def UpdateSunSpawning(self) -> None: ...
    def UpdateTutorial(self) -> None: ...
    def UpdateWinds(self) -> None: ...
    def UpdateZombieSpawning(self) -> None: ...
    def ZombieGet(self, theZombieID: Zombie) -> Zombie: ...
    def ZombieGetID(self, theZombie: Zombie) -> Zombie: ...
    def ZombieHitTest(self, theMouseX: int, theMouseY: int) -> Zombie: ...
    @staticmethod
    def ZombiePickerInit(theZombiePicker: ZombiePicker) -> None: ...
    @staticmethod
    def ZombiePickerInitForWave(theZombiePicker: ZombiePicker) -> None: ...
    def ZombieSwitchRow(self, aZombie: Zombie, aRow: int) -> None: ...
    def ZombiesWon(self, aZombie: Zombie) -> None: ...
    def ZombieTryToGet(self, theZombieID: Zombie) -> Zombie: ...
    # Skipped AddSunMoney due to it being static, abstract and generic.

    AddSunMoney : AddSunMoney_MethodGroup
    class AddSunMoney_MethodGroup:
        @typing.overload
        def __call__(self, theAmount: int) -> None:...
        @typing.overload
        def __call__(self, theX: int, theY: int, theSunMoney: int, theCoinMotion: CoinMotion) -> None:...

    # Skipped AddToZombieList due to it being static, abstract and generic.

    AddToZombieList : AddToZombieList_MethodGroup
    class AddToZombieList_MethodGroup:
        @typing.overload
        def __call__(self, aZombie: Zombie) -> None:...
        @typing.overload
        def __call__(self, aZombie: Zombie, row: int) -> None:...

    # Skipped AddZombie due to it being static, abstract and generic.

    AddZombie : AddZombie_MethodGroup
    class AddZombie_MethodGroup:
        @typing.overload
        def __call__(self, theZombieType: ZombieType, theFromWave: int) -> Zombie:...
        @typing.overload
        def __call__(self, theZombieType: ZombieType, theFromWave: int, theCover: bool) -> Zombie:...

    # Skipped AddZombieInRow due to it being static, abstract and generic.

    AddZombieInRow : AddZombieInRow_MethodGroup
    class AddZombieInRow_MethodGroup:
        @typing.overload
        def __call__(self, theZombieType: ZombieType, theRow: int, theFromWave: int) -> Zombie:...
        @typing.overload
        def __call__(self, theZombieType: ZombieType, theRow: int, theFromWave: int, theCover: bool) -> Zombie:...

    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, id: int, id2: int) -> None:...

    # Skipped DisplayAdvice due to it being static, abstract and generic.

    DisplayAdvice : DisplayAdvice_MethodGroup
    class DisplayAdvice_MethodGroup:
        @typing.overload
        def __call__(self, theAdvice: str, theMessageStyle: MessageStyle, theHelpIndex: AdviceType) -> None:...
        @typing.overload
        def __call__(self, theAdvice: str, theMessageStyle: MessageStyle, theHelpIndex: AdviceType, theIcon: Image) -> None:...

    # Skipped GrantAchievement due to it being static, abstract and generic.

    GrantAchievement : GrantAchievement_MethodGroup
    class GrantAchievement_MethodGroup:
        @typing.overload
        def __call__(self, theAchievement: AchievementId) -> bool:...
        @typing.overload
        def __call__(self, theAchievement: AchievementId, show: bool) -> bool:...

    # Skipped Resize due to it being static, abstract and generic.

    Resize : Resize_MethodGroup
    class Resize_MethodGroup:
        @typing.overload
        def __call__(self, theRect: TRect) -> None:...
        @typing.overload
        def __call__(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None:...


    class Camera:
        def __init__(self, theBoard: Board, theScreenWidth: int, theScreenHeight: int) -> None: ...
        @property
        def OperationCountdown(self) -> int: ...
        @OperationCountdown.setter
        def OperationCountdown(self, value: int) -> int: ...
        @property
        def OperationMaxCountdown(self) -> int: ...
        @OperationMaxCountdown.setter
        def OperationMaxCountdown(self, value: int) -> int: ...
        @property
        def X(self) -> float: ...
        @X.setter
        def X(self, value: float) -> float: ...
        @property
        def Y(self) -> float: ...
        @Y.setter
        def Y(self, value: float) -> float: ...
        @property
        def Zoom(self) -> float: ...
        @Zoom.setter
        def Zoom(self, value: float) -> float: ...
        def ApplyTransform(self, g: Graphics) -> None: ...
        def BoardToScreen(self, boardX: int, boardY: int) -> TPoint: ...
        def FocusWorldSmooth(self, focusWorldX: float, focusWorldY: float, zoom: float, countdown: int, theCurve: TodCurves) -> None: ...
        def Reset(self) -> None: ...
        def ResetTransform(self, g: Graphics) -> None: ...
        def ScreenToBoard(self, screenX: int, screenY: int) -> TPoint: ...
        def SetPosition(self, x: float, y: float, scale: float) -> None: ...
        def SetPositionSmooth(self, x: float, y: float, scale: float, countdown: int, theCurve: TodCurves) -> None: ...
        def Update(self) -> None: ...
        def ZoomAtSmooth(self, focusWorldX: float, focusWorldY: float, zoom: float, countdown: int, theCurve: TodCurves) -> None: ...
        # Skipped ScreenToBoardReplace due to it being static, abstract and generic.

        ScreenToBoardReplace : ScreenToBoardReplace_MethodGroup
        class ScreenToBoardReplace_MethodGroup:
            def __call__(self, screenX: clr.Reference[float], screenY: clr.Reference[float]) -> None:...
            # Method ScreenToBoardReplace(screenX : Int32&, screenY : Int32&) was skipped since it collides with above method



    class TopRightUIDrawMode(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        MenuButton : Board.TopRightUIDrawMode # 1
        StoreButton : Board.TopRightUIDrawMode # 2
        PauseButton : Board.TopRightUIDrawMode # 4
        AccelerateButton : Board.TopRightUIDrawMode # 8
        All : Board.TopRightUIDrawMode # 15



class BoardResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : BoardResult # 0
    Won : BoardResult # 1
    Lost : BoardResult # 2
    Restart : BoardResult # 3
    Quit : BoardResult # 4
    QuitApp : BoardResult # 5
    Cheat : BoardResult # 6


class BossPart(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    BackLeg : BossPart # 0
    FrontLeg : BossPart # 1
    Main : BossPart # 2
    BackArm : BossPart # 3
    Fireball : BossPart # 4


class BoxedLabel(Label):
    def __init__(self, boxImage: Image, margins: TRect, text: str, font: Font, color: Color, scale: float = ..., just: DrawStringJustification = ...) -> None: ...
    FullRect : TRect
    mClip : bool
    mColor : Color
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mDrawStringJustification : DrawStringJustification
    mFont : Font
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mImageBox : Image
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMargins : TRect
    mMouseInsets : Insets
    mMouseVisible : bool
    mOriginalColor : Color
    mParent : WidgetContainer
    mPriority : int
    mScale : float
    mTabNext : Widget
    mTabPrev : Widget
    mText : str
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def SetTransparency(self, c: float) -> None: ...


class BungeeDropGrid:
    def __init__(self) -> None: ...
    mGridArray : Array_1[TodWeightedGridArray]
    mGridArrayCount : int


class ButtonIds(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Close : ButtonIds # 0
    Plant : ButtonIds # 1
    Zombie : ButtonIds # 2
    Index : ButtonIds # 3


class CardGroup:
    def __init__(self) -> None: ...
    mCardInfo : Array_1[CardInfo]


class CardGroupWidget(Widget):
    def __init__(self, theApp: LawnApp, theListener: SeedChooserScreen) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mCols : int
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mListener : SeedChooserScreen
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mSelectedGroupId : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def DrawGroup(self, g: Graphics, theGroupId: int, theDrawBack: bool) -> None: ...
    def DrawGroups(self, g: Graphics) -> None: ...
    def GetCardGroupPosition(self, theGroup: int, theX: clr.Reference[int]) -> None: ...
    def GetCardPositionInGroup(self, theCardIndex: int, theCardCount: int) -> int: ...
    def MouseUp(self, x: int, y: int, theBtnNum: int) -> None: ...
    # Skipped GetCardGroup due to it being static, abstract and generic.

    GetCardGroup : GetCardGroup_MethodGroup
    class GetCardGroup_MethodGroup:
        @typing.overload
        def __call__(self) -> CardGroup:...
        @typing.overload
        def __call__(self, theGroup: int) -> CardGroup:...



class CardInfo:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, theSeedType: SeedType, theImitater: bool) -> None: ...
    @typing.overload
    def __init__(self, theSeedType: SeedType, theImitaterType: SeedType) -> None: ...
    mImitater : bool
    mSeedType : SeedType
    def Deconstruct(self, theSeedType: clr.Reference[SeedType], theImitaterType: clr.Reference[SeedType]) -> None: ...
    # Skipped Init due to it being static, abstract and generic.

    Init : Init_MethodGroup
    class Init_MethodGroup:
        @typing.overload
        def __call__(self) -> None:...
        @typing.overload
        def __call__(self, theSeedType: SeedType, theImitaterType: SeedType) -> None:...



class Challenge(StoreListener):
    def __init__(self) -> None: ...
    gArtChallengeStarfruit : Array_1[SeedType]
    gArtChallengeSunFlower : Array_1[SeedType]
    gArtChallengeWallnut : Array_1[SeedType]
    mApp : LawnApp
    mBeghouledEated : Array_1[bool]
    mBeghouledMatchesThisMove : int
    mBeghouledMouseCapture : bool
    mBeghouledMouseDownX : int
    mBeghouledMouseDownY : int
    mBeghouledPurcasedUpgrade : Array_1[bool]
    mBoard : Board
    mChallengeGridX : int
    mChallengeGridY : int
    mChallengeScore : int
    mChallengeState : ChallengeState
    mChallengeStateCounter : int
    mCloudCounter : Array_1[int]
    mConveyorBeltCounter : int
    mGloveCounter : int
    mLastConveyorSeedType : SeedType
    mName : str
    mRainCounter : int
    mReanimChallenge : Reanimation
    mReanimChallenge_Save : int
    mReanimCloud : Array_1[Reanimation]
    mReanimCloud_Save : Array_1[int]
    mScaryPotterPots : int
    mShowBowlingLine : bool
    mSlotMachineRollCount : int
    mSurvivalStage : int
    mTreeOfWisdomTalkIndex : int
    def AdvanceCrazyDaveDialog(self) -> None: ...
    def BackFromStore(self) -> None: ...
    def BeghouledBoardHasMatch(self, theBoardState: BeghouledBoardState) -> bool: ...
    def BeghouledCancelMatchFlashing(self) -> None: ...
    def BeghouledCanClearCrater(self) -> bool: ...
    def BeghouledCheckForPossibleMoves(self, theBoardState: BeghouledBoardState) -> bool: ...
    def BeghouledCheckStuckState(self) -> None: ...
    def BeghouledClearCrater(self, theCount: int) -> None: ...
    def BeghouledCreatePlants(self, theOldBoardState: BeghouledBoardState, theNewBoardState: BeghouledBoardState) -> None: ...
    def BeghouledDragCancel(self) -> None: ...
    def BeghouledDragStart(self, x: int, y: int) -> None: ...
    def BeghouledDragUpdate(self, x: int, y: int) -> None: ...
    def BeghouledFallIntoSquare(self, x: int, y: int, theBoardState: BeghouledBoardState) -> None: ...
    def BeghouledFillHoles(self, theBoardState: BeghouledBoardState, theAllowMatches: bool) -> None: ...
    def BeghouledFlashAMatch(self) -> None: ...
    def BeghouledFlashFromBoardState(self, theBoardState: BeghouledBoardState, theSwap1X: int, theSwap1Y: int, theSwap2X: int, theSwap2Y: int) -> bool: ...
    def BeghouledFlashPlant(self, x: int, y: int, theSwap1X: int, theSwap1Y: int, theSwap2X: int, theSwap2Y: int) -> None: ...
    def BeghouledGetPlantAt(self, x: int, y: int, theBoardState: BeghouledBoardState) -> SeedType: ...
    def BeghouledHorizontalMatchLength(self, x: int, y: int, theBoardState: BeghouledBoardState) -> int: ...
    def BeghouledIsValidMove(self, x1: int, y1: int, x2: int, y2: int, theBoardState: BeghouledBoardState) -> bool: ...
    def BeghouledMakePlantsFall(self, theBoardState: BeghouledBoardState) -> None: ...
    def BeghouledMakeStartBoard(self) -> None: ...
    def BeghouledPacketClicked(self, theSeedPacket: SeedPacket) -> None: ...
    def BeghouledPickSeed(self, theGridX: int, theGridY: int, theBoardState: BeghouledBoardState, theAllowMatches: bool) -> SeedType: ...
    def BeghouledPopulateBoard(self) -> None: ...
    def BeghouledRemoveHorizontalMatch(self, x: int, y: int, theBoardState: BeghouledBoardState) -> None: ...
    def BeghouledRemoveMatches(self, theBoardState: BeghouledBoardState) -> None: ...
    def BeghouledRemoveVerticalMatch(self, x: int, y: int, theBoardState: BeghouledBoardState) -> None: ...
    def BeghouledScore(self, x: int, y: int, theNumPlants: int, theIsHorizontal: bool) -> None: ...
    def BeghouledShuffle(self) -> None: ...
    def BeghouledStartFalling(self, theChallengeState: ChallengeState) -> None: ...
    def BeghouledTwistFlashMatch(self, theBoardState: BeghouledBoardState, theGridX: int, theGridY: int) -> bool: ...
    def BeghouledTwistMouseDown(self, x: int, y: int) -> None: ...
    def BeghouledTwistMoveCausesMatch(self, theGridX: int, theGridY: int, theBoardState: BeghouledBoardState) -> bool: ...
    def BeghouledTwistSquareFromMouse(self, theMouseX: int, theMouseY: int, theGridX: clr.Reference[int], theGridY: clr.Reference[int]) -> bool: ...
    def BeghouledTwistValidMove(self, theGridX: int, theGridY: int, theBoardState: BeghouledBoardState) -> bool: ...
    def BeghouledUpdateCraters(self) -> None: ...
    def BeghouledVerticalMatchLength(self, x: int, y: int, theBoardState: BeghouledBoardState) -> int: ...
    def CanPlantAt(self, theGridX: int, theGridY: int, theType: SeedType) -> PlantingReason: ...
    def CanTargetZombieWithPortals(self, thePlant: Plant, theZombie: Zombie) -> bool: ...
    def CheckForCompleteArtChallenge(self, theGridX: int, theGridY: int) -> None: ...
    def ClearCursor(self) -> None: ...
    def DrawArtChallenge(self, g: Graphics) -> None: ...
    def DrawBackdrop(self, g: Graphics) -> None: ...
    def DrawBeghouled(self, g: Graphics) -> None: ...
    def DrawRain(self, g: Graphics) -> None: ...
    def DrawSlotMachine(self, g: Graphics) -> None: ...
    def DrawStormFlash(self, g: Graphics, theTime: int, theMaxAmount: int) -> None: ...
    def DrawStormNight(self, g: Graphics) -> None: ...
    def DrawWeather(self, g: Graphics) -> None: ...
    def GetArtChallengeSeed(self, theGridX: int, theGridY: int) -> SeedType: ...
    def GetGloveCounterMax(self) -> int: ...
    def GetOtherPortal(self, thePortal: GridItem) -> GridItem: ...
    def GetPortalAt(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetPortalDistanceToMower(self, theGridY: int) -> int: ...
    def GetPortalToLeft(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GetPortalToRight(self, theGridX: int, theGridY: int) -> GridItem: ...
    def GraveDangerSpawnGraveAt(self, x: int, y: int) -> None: ...
    def GraveDangerSpawnRandomGrave(self) -> None: ...
    def InitLevel(self) -> None: ...
    def InitZombieWaves(self) -> None: ...
    def InitZombieWavesChallengStageRandom(self) -> None: ...
    def InitZombieWavesFromList(self, theZombieList: Array_1[ZombieType], theListLength: int) -> None: ...
    def InitZombieWavesSurvival(self) -> None: ...
    def IsStormyNightPitchBlack(self) -> bool: ...
    @staticmethod
    def IsZombieSeedType(theSeedType: SeedType) -> bool: ...
    def IZombieDrawPlant(self, g: Graphics, thePlant: Plant) -> None: ...
    def IZombieEatBrain(self, theZombie: Zombie) -> bool: ...
    def IZombieGetBrainTarget(self, theZombie: Zombie) -> GridItem: ...
    def IZombieInitLevel(self) -> None: ...
    def IZombieMouseDownWithZombie(self, x: int, y: int, theClickCount: int) -> None: ...
    def IZombiePlacePlantInSquare(self, theSeedType: SeedType, theGridX: int, theGridY: int) -> None: ...
    def IZombiePlacePlants(self, theSeedType: SeedType, theCount: int, theGridY: int) -> None: ...
    def IZombiePlaceZombie(self, theZombieType: ZombieType, theGridX: int, theGridY: int) -> Zombie: ...
    def IZombiePlantDropRemainingSun(self, thePlant: Plant) -> None: ...
    def IZombieScoreBrain(self, theBrain: GridItem) -> None: ...
    @staticmethod
    def IZombieSeedTypeToZombieType(theSeedType: SeedType) -> ZombieType: ...
    def IZombieSetPlantFilterEffect(self, thePlant: Plant, theFilterEffect: FilterEffectType) -> None: ...
    def IZombieSetupPlant(self, thePlant: Plant) -> None: ...
    def IZombieSquishBrain(self, theBrain: GridItem) -> None: ...
    def IZombieStart(self) -> None: ...
    def IZombieUpdate(self) -> None: ...
    def LastStandCompletedStage(self) -> None: ...
    def LastStandUpate(self) -> None: ...
    def LoadBeghouledBoardState(self, theBoardState: BeghouledBoardState) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def MouseDown(self, x: int, y: int, theClickCount: int, theHitResult: HitResult) -> bool: ...
    def MouseDownWhackAZombie(self, x: int, y: int) -> None: ...
    def MouseDownWithZenTool(self, x: int, y: int, theCursorType: CursorType, isTouch: bool) -> bool: ...
    def MouseMove(self, x: int, y: int) -> bool: ...
    def MouseUp(self, x: int, y: int) -> bool: ...
    def MoveAPortal(self) -> None: ...
    def MovePlant(self, thePlant: Plant, theGridX: int, theGridY: int) -> None: ...
    def PlantAdded(self, thePlant: Plant) -> None: ...
    def PlayBossEnter(self) -> None: ...
    def PortalCombatRowSpawnWeight(self, theGridY: int) -> float: ...
    def PortalStart(self) -> None: ...
    def PuzzleIsAwardStage(self) -> bool: ...
    def PuzzleNextStageClear(self) -> None: ...
    def PuzzlePhaseComplete(self, theGridX: int, theGridY: int) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def ScaryPotterChangePotType(self, thePotType: GridItemState, theCount: int) -> None: ...
    def ScaryPotterCountPots(self) -> int: ...
    def ScaryPotterCountSunInPot(self, theScaryPot: GridItem) -> int: ...
    def ScaryPotterDontPlaceInCol(self, theCol: int, theGridArray: Array_1[TodWeightedGridArray], theGridArrayCount: int) -> None: ...
    def ScaryPotterFillColumnWithPlant(self, theCol: int, theSeedType: SeedType, theGridArray: Array_1[TodWeightedGridArray], theGridArrayCount: int) -> None: ...
    def ScaryPotterIsCompleted(self) -> bool: ...
    def ScaryPotterJackExplode(self, aPosX: int, aPosY: int) -> None: ...
    def ScaryPotterMalletPot(self, theScaryPot: GridItem) -> None: ...
    def ScaryPotterOpenPot(self, theScaryPot: GridItem) -> None: ...
    def ScaryPotterPlacePot(self, theScaryPotType: ScaryPotType, theZombieType: ZombieType, theSeedType: SeedType, theCount: int, theGridArray: Array_1[TodWeightedGridArray], theGridArrayCount: int) -> None: ...
    def ScaryPotterPopulate(self) -> None: ...
    def ScaryPotterStart(self) -> None: ...
    def ScaryPotterUpdate(self) -> None: ...
    def ShovelAddWallnuts(self) -> None: ...
    def SlotMachineGetHandleRect(self) -> TRect: ...
    def SlotMachineRect(self) -> TRect: ...
    def SpawnLevelAward(self, theGridX: int, theGridY: int) -> None: ...
    def SpawnZombieWave(self) -> None: ...
    def SquirrelChew(self, theSquirrel: GridItem) -> None: ...
    def SquirrelCountUncaught(self) -> int: ...
    def SquirrelFound(self, theSquirrel: GridItem) -> None: ...
    def SquirrelPeek(self, theSquirrel: GridItem) -> None: ...
    def SquirrelStart(self) -> None: ...
    def SquirrelUpdate(self) -> None: ...
    def SquirrelUpdateOne(self, theSquirrel: GridItem) -> None: ...
    def StartLevel(self) -> None: ...
    def TreeOfWisdomBabble(self) -> None: ...
    def TreeOfWisdomBackFromStore(self) -> None: ...
    def TreeOfWisdomCanFeed(self) -> bool: ...
    def TreeOfWisdomDraw(self, g: Graphics) -> None: ...
    def TreeOfWisdomFertilize(self) -> None: ...
    def TreeOfWisdomGetSize(self) -> int: ...
    def TreeOfWisdomGiveWisdom(self) -> None: ...
    def TreeOfWisdomGrow(self) -> None: ...
    def TreeOfWisdomHitTest(self, theX: int, theY: int, theHitResult: clr.Reference[HitResult]) -> bool: ...
    def TreeOfWisdomInit(self) -> None: ...
    def TreeOfWisdomLeave(self) -> None: ...
    def TreeOfWisdomMouseOn(self, theX: int, theY: int, posScaled: bool) -> bool: ...
    def TreeOfWisdomNextGarden(self) -> None: ...
    def TreeOfWisdomOpenStore(self) -> None: ...
    def TreeOfWisdomPrevGarden(self) -> None: ...
    def TreeOfWisdomSayRepeat(self) -> None: ...
    def TreeOfWisdomTool(self, aMouseX: int, aMouseY: int) -> None: ...
    def TreeOfWisdomToolUpdate(self, theZenTool: GridItem) -> None: ...
    def TreeOfWisdomUpdate(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateBeghouled(self) -> None: ...
    def UpdateBeghouledPlant(self, thePlant: Plant) -> bool: ...
    def UpdateConveyorBelt(self) -> None: ...
    def UpdatePortal(self, thePortal: GridItem) -> None: ...
    def UpdatePortalCombat(self) -> None: ...
    def UpdateRain(self) -> None: ...
    def UpdateRainingSeeds(self) -> None: ...
    def UpdateSlotMachine(self) -> None: ...
    def UpdateStormyNight(self) -> None: ...
    def UpdateZombieSpawning(self) -> bool: ...
    def WhackAZombiePlaceGraves(self, theGraveCount: int) -> None: ...
    def WhackAZombieSpawning(self) -> None: ...
    def WhackAZombieUpdate(self) -> None: ...
    def ZombieAtePlant(self, theZombie: Zombie, thePlant: Plant) -> None: ...
    def ZombiquariumDropBrain(self, x: int, y: int) -> None: ...
    def ZombiquariumMouseDown(self, x: int, y: int) -> None: ...
    def ZombiquariumPacketClicked(self, theSeedPacket: SeedPacket) -> None: ...
    def ZombiquariumSpawnSnorkel(self) -> Zombie: ...
    def ZombiquariumUpdate(self) -> None: ...


class ChallengeDefinition:
    def __init__(self, mode: GameMode, index: int, page: ChallengePage, row: int, col: int, name: str) -> None: ...
    mChallengeIconIndex : int
    mChallengeMode : GameMode
    mChallengeName : str
    mCol : int
    mPage : ChallengePage
    mRow : int
    def ToString(self) -> str: ...


class ChallengePage(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Survival : ChallengePage # 0
    Challenge : ChallengePage # 1
    Limbo : ChallengePage # 2
    Puzzle : ChallengePage # 3
    Extra : ChallengePage # 4
    Challenge2 : ChallengePage # 5
    MaxChallengePages : ChallengePage # 6


class ChallengeScreen(Widget, ButtonListener):
    def __init__(self, theApp: LawnApp, thePage: ChallengePage) -> None: ...
    FullRect : TRect
    gChallengeDefs : Array_1[ChallengeDefinition]
    mApp : LawnApp
    mBackButton : NewLawnButton
    mChallengeButton : Array_1[ButtonWidget]
    mChallengeExtraButton : Array_1[ButtonWidget]
    mChallengeScreenWidget : ChallengeScreenWidget
    mCheatEnableChallenges : bool
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHalfDeltaHeight : int
    mHalfDeltaWidth : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLockShakeX : float
    mLockShakeY : float
    mMouseInsets : Insets
    mMouseVisible : bool
    mPageButton : Array_1[ButtonWidget]
    mPageIndex : ChallengePage
    mParent : WidgetContainer
    mPriority : int
    mScrollWidget : ScrollWidget
    mTabNext : Widget
    mTabPrev : Widget
    mUnlockChallengeIndex : int
    mUnlockState : UnlockingState
    mUnlockStateCounter : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AccomplishmentsNeeded(self, aChallengeIndex: int) -> int: ...
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, id: int) -> None: ...
    def ButtonMouseEnter(self, id: int) -> None: ...
    def ButtonMouseLeave(self, id: int) -> None: ...
    def ButtonMouseMove(self, id: int, x: int, y: int) -> None: ...
    def ButtonMouseTick(self, id: int) -> None: ...
    def ChallengeModeRecordsTime(self, theGameMode: GameMode) -> bool: ...
    def Draw(self, g: Graphics) -> None: ...
    @staticmethod
    def GetChallengeDefFromMode(mode: GameMode) -> ChallengeDefinition: ...
    def IsIZombieLevel(self, theGameMode: GameMode) -> bool: ...
    def IsScaryPotterLevel(self, theGameMode: GameMode) -> bool: ...
    def MoreTrophiesNeeded(self, aChallengeIndex: int) -> int: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def SetUnlockChallengeIndex(self, thePage: ChallengePage, aIsIZombie: bool) -> None: ...
    def ShowPageButtons(self) -> bool: ...
    def Update(self) -> None: ...
    def UpdateButtons(self) -> None: ...
    def UpdateScreen(self) -> None: ...
    def UpdateToolTip(self) -> None: ...
    def UpdateUIPosition(self) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, id: int, id2: int) -> None:...



class ChallengeScreenValues(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ChallengeScreen_Back : ChallengeScreenValues # 100
    ChallengeScreen_Mode : ChallengeScreenValues # 200
    ChallengeScreen_Page : ChallengeScreenValues # 300


class ChallengeScreenWidget(Widget):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def SetSize(self, width: int, height: int) -> None: ...


class ChallengeState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : ChallengeState # 0
    BeghouledMoving : ChallengeState # 1
    BeghouledFalling : ChallengeState # 2
    BeghouledNoMatches : ChallengeState # 3
    SlotMachineRolling : ChallengeState # 4
    StormFlash1 : ChallengeState # 5
    StormFlash2 : ChallengeState # 6
    StormFlash3 : ChallengeState # 7
    ZenFading : ChallengeState # 8
    ScaryPotterMalleting : ChallengeState # 9
    LastStandOnslaught : ChallengeState # 10
    TreeJustGrew : ChallengeState # 11
    TreeGiveWisdom : ChallengeState # 12
    TreeWaitingToBabble : ChallengeState # 13
    TreeBabbling : ChallengeState # 14
    ZenPlantInteracting : ChallengeState # 15


class ChosenSeed:
    def __init__(self) -> None: ...
    mCrazyDavePicked : bool
    mEndX : int
    mEndY : int
    mImitaterType : SeedType
    mRefreshCounter : int
    mRefreshing : bool
    mSeedIndexInBank : int
    mSeedState : ChosenSeedState
    mSeedType : SeedType
    mStartX : int
    mStartY : int
    mTimeEndMotion : int
    mTimeStartMotion : int
    mX : int
    mY : int


class ChosenSeedState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SEED_FLYING_TO_BANK : ChosenSeedState # 0
    SEED_IN_BANK : ChosenSeedState # 1
    SEED_FLYING_TO_CHOOSER : ChosenSeedState # 2
    SEED_IN_CHOOSER : ChosenSeedState # 3
    SEED_PACKET_HIDDEN : ChosenSeedState # 4


class Coin(GameObject):
    def __init__(self) -> None: ...
    LoadedSeedType : SeedType
    mApp : LawnApp
    mBoard : Board
    mCoinAge : int
    mCoinMotion : CoinMotion
    mCollectionDistance : float
    mCollectX : float
    mCollectY : float
    mDead : bool
    mDisappearCounter : int
    mFadeCount : int
    mGroundY : int
    mHasBouncyArrow : bool
    mHeight : int
    mHitGround : bool
    mIsBeingCollected : bool
    mNeedsBouncyArrow : bool
    mPosScaled : bool
    mPosX : float
    mPosY : float
    mPottedPlantSpec : PottedPlant
    mPrevTransX : float
    mPrevTransY : float
    mRenderOrder : int
    mRow : int
    mScale : float
    mScored : bool
    mTimesDropped : int
    mType : CoinType
    mUsableSeedType : SeedType
    mVelX : float
    mVelY : float
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    @staticmethod
    def CoinFreeTextures() -> None: ...
    def CoinGetsBouncyArrow(self) -> bool: ...
    def CoinInitialize(self, theX: int, theY: int, theCoinType: CoinType, theCoinMotion: CoinMotion) -> None: ...
    def Collect(self) -> None: ...
    def Die(self) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DroppedUsableSeed(self) -> None: ...
    def FanOutCoins(self, theCoinType: CoinType, theNumCoins: int) -> None: ...
    @staticmethod
    def GetCoinValue(theType: CoinType) -> int: ...
    def GetColor(self) -> SexyColor: ...
    def GetDisappearTime(self) -> int: ...
    def GetFinalSeedPacketType(self) -> SeedType: ...
    def GetSunScale(self) -> float: ...
    def GetSunValue(self) -> int: ...
    def IsLevelAward(self) -> bool: ...
    def IsMoney(self) -> bool: ...
    def IsPresentWithAdvice(self) -> bool: ...
    def IsSun(self) -> bool: ...
    def Loaded(self) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseHitTest(self, theX: int, theY: int, theHitResult: clr.Reference[HitResult]) -> bool: ...
    def PlayCollectSound(self) -> None: ...
    def PlayGroundSound(self) -> None: ...
    def PlayLaunchSound(self) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def ScoreCoin(self) -> None: ...
    def StartFade(self) -> None: ...
    def TryAutoCollectAfterLevelAward(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateCollected(self) -> None: ...


class CoinID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : CoinID # 0


class CoinMotion(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    FromSky : CoinMotion # 0
    FromSkySlow : CoinMotion # 1
    FromPlant : CoinMotion # 2
    Coin : CoinMotion # 3
    LawnmowerCoin : CoinMotion # 4
    FromPresent : CoinMotion # 5
    FromBoss : CoinMotion # 6


class CoinType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : CoinType # 0
    Silver : CoinType # 1
    Gold : CoinType # 2
    Diamond : CoinType # 3
    Sun : CoinType # 4
    Smallsun : CoinType # 5
    Largesun : CoinType # 6
    FinalSeedPacket : CoinType # 7
    Trophy : CoinType # 8
    Shovel : CoinType # 9
    Almanac : CoinType # 10
    Carkeys : CoinType # 11
    WateringCan : CoinType # 12
    Taco : CoinType # 13
    Note : CoinType # 14
    UsableSeedPacket : CoinType # 15
    PresentPlant : CoinType # 16
    AwardMoneyBag : CoinType # 17
    AwardPresent : CoinType # 18
    AwardBagDiamond : CoinType # 19
    Chocolate : CoinType # 20
    AwardChocolate : CoinType # 21
    PresentMinigames : CoinType # 22
    PresentPuzzleMode : CoinType # 23
    Bacon : CoinType # 24
    AwardSliverSunflower : CoinType # 25
    AwardGoldSunflower : CoinType # 26
    Tinysun : CoinType # 27
    Award10PottedPlants : CoinType # 28


class ComicReaderWidget(Widget):
    def __init__(self, imagesGroups: Array_1[str], imageNames: Array_1[str], thumbnails: Array_1[Image], pageCount: int) -> None: ...
    FullRect : TRect
    mAlwaysShowPageNumber : bool
    mClip : bool
    mCloseButton : GameButton
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mImageLoadGroups : Array_1[str]
    mImageNames : Array_1[str]
    mImageTransform : ComicReaderWidget.ImageTransform
    mIsDown : bool
    mIsDragging : bool
    mIsOver : bool
    mLastFocusedWidget : Widget
    mLastLoadedImageGroups : Dictionary_2[str, Image]
    mLastWMUpdateCount : int
    mMouseDownPos : TPoint
    mMouseInsets : Insets
    mMouseVisible : bool
    mNextImageTransform : ComicReaderWidget.ImageTransform
    mOwnedThumbnailLoadGroup : str
    mPageEasings : Array_1[int]
    mPageNumberRect : TRect
    mParent : WidgetContainer
    mPrevImageTransform : ComicReaderWidget.ImageTransform
    mPriority : int
    mProgressBar : ComicReaderWidget.ComicProgressBar
    mShowToolbar : bool
    mTabNext : Widget
    mTabPrev : Widget
    mThumbnails : Array_1[Image]
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    PAGE_APPEAR_EASING_TICKS : int
    SCROLL_PAGE_EASING_TICKS : int
    @property
    def mImage(self) -> Image: ...
    @property
    def mNextImage(self) -> Image: ...
    @property
    def mPrevImage(self) -> Image: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawComic(self, g: Graphics) -> None: ...
    def DrawPageNumber(self, g: Graphics, doDrawBox: bool) -> None: ...
    def DrawToolbar(self, g: Graphics) -> None: ...
    def MouseDown(self, x: int, y: int, theBtnNum: int, theClickCount: int) -> None: ...
    def MouseDrag(self, x: int, y: int) -> None: ...
    def MouseUp(self, x: int, y: int, theBtnNum: int, theClickCount: int) -> None: ...
    def MouseWheel(self, theDelta: int) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def ToggleToolbar(self) -> None: ...
    def TryLoadPage(self, mLoadGroup: str, mImageName: str) -> Image: ...
    def UnloadPage(self, mLoadGroup: str) -> None: ...
    def Update(self) -> None: ...
    def UpdateEasings(self) -> None: ...
    # Skipped SwitchPage due to it being static, abstract and generic.

    SwitchPage : SwitchPage_MethodGroup
    class SwitchPage_MethodGroup:
        @typing.overload
        def __call__(self, newPageNumber: int) -> None:...
        @typing.overload
        def __call__(self, newPageNumber: int, preserveEasings: bool) -> None:...


    class ComicProgressBar(Widget):
        def __init__(self) -> None: ...
        FullRect : TRect
        mClip : bool
        mColors : List_1[Color]
        mDisabled : bool
        mDoFinger : bool
        mHasAlpha : bool
        mHasFocus : bool
        mHasTransparencies : bool
        mHeight : int
        mIsDown : bool
        mIsDragging : bool
        mIsOver : bool
        mLastWMUpdateCount : int
        mMouseInsets : Insets
        mMouseVisible : bool
        mPageCount : int
        mParent : WidgetContainer
        mPriority : int
        mProgressBarHeight : int
        mTabNext : Widget
        mTabPrev : Widget
        mUpdateCnt : int
        mUpdateIterator : LinkedListNode_1[Widget]
        mUpdateIteratorModified : bool
        mVisible : bool
        mWantsFocus : bool
        mWidgetFlagsMod : FlagsMod
        mWidgetManager : WidgetManager
        mWidgets : LinkedList_1[Widget]
        mWidth : int
        mX : int
        mY : int
        mZOrder : int
        SELECTOR_SIZE : TPoint
        @property
        def ProgressInPixel(self) -> float: ...
        @ProgressInPixel.setter
        def ProgressInPixel(self, value: float) -> float: ...
        def Draw(self, g: Graphics) -> None: ...
        def GetPageNumber(self) -> int: ...
        def MouseDown(self, x: int, y: int, theMagicCode: int) -> None: ...
        def MouseDrag(self, x: int, y: int) -> None: ...
        def MouseUp(self, x: int, y: int, theMagicCode: int) -> None: ...
        def SetPageNumber(self, num: int) -> None: ...
        def SyncSelector(self) -> None: ...


    class ImageTransform(IEquatable_1[ComicReaderWidget.ImageTransform]):
        def __init__(self, mTransX: float = ..., mTransY: float = ..., mScale: float = ...) -> None: ...
        @property
        def mScale(self) -> float: ...
        @mScale.setter
        def mScale(self, value: float) -> float: ...
        @property
        def mTransX(self) -> float: ...
        @mTransX.setter
        def mTransX(self, value: float) -> float: ...
        @property
        def mTransY(self) -> float: ...
        @mTransY.setter
        def mTransY(self, value: float) -> float: ...
        def Deconstruct(self, mTransX: clr.Reference[float], mTransY: clr.Reference[float], mScale: clr.Reference[float]) -> None: ...
        def GetHashCode(self) -> int: ...
        def __eq__(self, left: ComicReaderWidget.ImageTransform, right: ComicReaderWidget.ImageTransform) -> bool: ...
        def __ne__(self, left: ComicReaderWidget.ImageTransform, right: ComicReaderWidget.ImageTransform) -> bool: ...
        def ToString(self) -> str: ...
        def UpdateTransform(self, theX: int, theY: int, theWidth: int, theHeight: int, imageWidth: int, imageHeight: int) -> None: ...
        # Skipped Equals due to it being static, abstract and generic.

        Equals : Equals_MethodGroup
        class Equals_MethodGroup:
            @typing.overload
            def __call__(self, other: ComicReaderWidget.ImageTransform) -> bool:...
            @typing.overload
            def __call__(self, obj: typing.Any) -> bool:...




class Comics(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    CartoonJalapeno : Comics # 0
    CartoonScaredyshroom : Comics # 1
    CartoonChomper : Comics # 2
    CartoonRepeater : Comics # 3
    CartoonGarlic : Comics # 4
    CartoonKernelpult : Comics # 5
    CartoonLilypad : Comics # 6
    CartoonCattail : Comics # 7
    CartoonSunflower : Comics # 8
    CartoonPlantern : Comics # 9
    CartoonGravebuster : Comics # 10
    CartoonBejeweled : Comics # 11
    CartoonSpikeweed : Comics # 12
    CartoonAgave : Comics # 13
    CartoonRose : Comics # 14
    CartoonPumpkin : Comics # 15
    CartoonSpikerock : Comics # 16
    CartoonImitater : Comics # 17
    CartoonSun : Comics # 18
    CartoonHypnoshroom : Comics # 19
    ComicsCount : Comics # 20


class ComicSelector(LawnDialog):
    def __init__(self, theApp: LawnApp, theListener: AlmanacListener) -> None: ...
    COMIC_SELECTOR_ID : int
    FullRect : TRect
    mApp : LawnApp
    mBackgroundInsets : Insets
    mButtonDelay : int
    mButtonHeight : int
    mButtonHorzSpacing : int
    mButtonMode : int
    mButtonSidePadding : int
    mClip : bool
    mCloseButton : GameButton
    mColors : List_1[Color]
    mComicButtons : Array_1[GameButton]
    mComicWidget : Widget
    mComponentImage : Image
    mContentInsets : Insets
    mDialogFooter : str
    mDialogHeader : str
    mDialogLines : str
    mDialogListener : DialogListener
    mDisabled : bool
    mDoFinger : bool
    mDragging : bool
    mDragMouseX : int
    mDragMouseY : int
    mDrawStandardBack : bool
    mHalfDeltaHeight : int
    mHalfDeltaWidth : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeaderFont : Font
    mHeight : int
    mId : int
    mIsDown : bool
    mIsModal : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLawnNoButton : LawnStoneButton
    mLawnYesButton : LawnStoneButton
    mLinesFont : Font
    mLineSpacingOffset : int
    mListener : AlmanacListener
    mMinWidth : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNoButton : DialogButton
    mNumButtons : int
    mParent : WidgetContainer
    mPriority : int
    mReanimation : ReanimationWidget
    mResult : int
    mSpaceAfterHeader : int
    mTabNext : Widget
    mTabPrev : Widget
    mTallBottom : bool
    mTextAlign : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVerticalCenterText : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mYesButton : DialogButton
    mZOrder : int
    def BackButtonPress(self) -> bool: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def LoadComicThumbnails(self, theComic: Comics) -> Array_1[Image]: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def Update(self) -> None: ...
    def UpdateScreen(self) -> None: ...
    def UpdateUIPosition(self) -> None: ...

    class ComicImportData(abc.ABC):
        mComics : Dictionary_2[Comics, ComicSelector.ComicImportDataEntry]


    class ComicImportDataEntry(IEquatable_1[ComicSelector.ComicImportDataEntry]):
        def __init__(self, mComicId: Comics, mName: str, mCoverImage: Image, mPageCount: int, mLoadGroupPrefix: str, mImagePrefix: str, mSeedType: SeedType) -> None: ...
        @property
        def mComicId(self) -> Comics: ...
        @mComicId.setter
        def mComicId(self, value: Comics) -> Comics: ...
        @property
        def mCoverImage(self) -> Image: ...
        @mCoverImage.setter
        def mCoverImage(self, value: Image) -> Image: ...
        @property
        def mImagePrefix(self) -> str: ...
        @mImagePrefix.setter
        def mImagePrefix(self, value: str) -> str: ...
        @property
        def mLoadGroupPrefix(self) -> str: ...
        @mLoadGroupPrefix.setter
        def mLoadGroupPrefix(self, value: str) -> str: ...
        @property
        def mName(self) -> str: ...
        @mName.setter
        def mName(self, value: str) -> str: ...
        @property
        def mPageCount(self) -> int: ...
        @mPageCount.setter
        def mPageCount(self, value: int) -> int: ...
        @property
        def mSeedType(self) -> SeedType: ...
        @mSeedType.setter
        def mSeedType(self, value: SeedType) -> SeedType: ...
        def Deconstruct(self, mComicId: clr.Reference[Comics], mName: clr.Reference[str], mCoverImage: clr.Reference[Image], mPageCount: clr.Reference[int], mLoadGroupPrefix: clr.Reference[str], mImagePrefix: clr.Reference[str], mSeedType: clr.Reference[SeedType]) -> None: ...
        def GetHashCode(self) -> int: ...
        def __eq__(self, left: ComicSelector.ComicImportDataEntry, right: ComicSelector.ComicImportDataEntry) -> bool: ...
        def __ne__(self, left: ComicSelector.ComicImportDataEntry, right: ComicSelector.ComicImportDataEntry) -> bool: ...
        def ToString(self) -> str: ...
        # Skipped Equals due to it being static, abstract and generic.

        Equals : Equals_MethodGroup
        class Equals_MethodGroup:
            @typing.overload
            def __call__(self, other: ComicSelector.ComicImportDataEntry) -> bool:...
            @typing.overload
            def __call__(self, obj: typing.Any) -> bool:...




class ContinueDialogs(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ContinueDialog_Continue : ContinueDialogs # 0
    ContinueDialog_NewGame : ContinueDialogs # 1


class CrazyDaveState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Off : CrazyDaveState # 0
    Entering : CrazyDaveState # 1
    Leaving : CrazyDaveState # 2
    Idling : CrazyDaveState # 3
    Talking : CrazyDaveState # 4
    HandingTalking : CrazyDaveState # 5
    HandingIdling : CrazyDaveState # 6


class CreditScreen(Widget, ButtonListener):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mCreditsHeight : int
    mCreditsY : float
    mDidInitialDraw : bool
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMainMenuButton : LawnStoneButton
    mMouseInsets : Insets
    mMouseVisible : bool
    mNames : Array_1[str]
    mNeedToStartPlaying : bool
    mNumSections : int
    mParent : WidgetContainer
    mPriority : int
    mReplayButton : NewLawnButton
    mRoles : Array_1[str]
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVideoFinished : bool
    mVideoLoading : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def AppGotFocus(self) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, id: int) -> None: ...
    def ButtonMouseEnter(self, id: int) -> None: ...
    def ButtonMouseLeave(self, id: int) -> None: ...
    def ButtonMouseMove(self, id: int, x: int, y: int) -> None: ...
    def ButtonMouseTick(self, id: int) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawCredits(self, g: Graphics) -> None: ...
    def GetCreditsHeight(self) -> int: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def RestartScroll(self) -> None: ...
    def TouchBegan(self, touch: _Touch) -> None: ...
    def TouchEnded(self, touch: _Touch) -> None: ...
    def TouchMoved(self, touch: _Touch) -> None: ...
    def Update(self) -> None: ...
    def VideoFinished(self) -> None: ...
    def VideoLoaded(self, succeeded: bool) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, id: int, id2: int) -> None:...



class CursorObject(GameObject):
    def __init__(self) -> None: ...
    mApp : LawnApp
    mBoard : Board
    mCobCannonPlantID : Plant
    mCobCannonPlantID_Save : int
    mCoinID : Coin
    mCoinID_Save : int
    mCursorType : CursorType
    mDuplicatorPlantID : Plant
    mDuplicatorPlantID_Save : int
    mGlovePlantID : Plant
    mGlovePlantID_Save : int
    mHammerDownCounter : int
    mHeight : int
    mImitaterType : SeedType
    mPosScaled : bool
    mPrevTransX : float
    mPrevTransY : float
    mReanimCursorID : Reanimation
    mReanimCursorID_Save : int
    mRenderOrder : int
    mRow : int
    mSeedBankIndex : int
    mType : SeedType
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    def Die(self) -> None: ...
    def DrawGroundLayer(self, g: Graphics) -> None: ...
    def DrawToolIconImage(self, g: Graphics, image: Image) -> None: ...
    def DrawTopLayer(self, g: Graphics) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def Update(self) -> None: ...


class CursorPreview(GameObject):
    def __init__(self) -> None: ...
    mApp : LawnApp
    mBoard : Board
    mGridX : int
    mGridY : int
    mHeight : int
    mPosScaled : bool
    mPrevTransX : float
    mPrevTransY : float
    mRenderOrder : int
    mRow : int
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    def Draw(self, g: Graphics) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def Update(self) -> None: ...


class CursorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : CursorType # 0
    PlantFromBank : CursorType # 1
    PlantFromUsableCoin : CursorType # 2
    PlantFromGlove : CursorType # 3
    PlantFromDuplicator : CursorType # 4
    PlantFromWheelBarrow : CursorType # 5
    Shovel : CursorType # 6
    Hammer : CursorType # 7
    CobcannonTarget : CursorType # 8
    WateringCan : CursorType # 9
    Fertilizer : CursorType # 10
    BugSpray : CursorType # 11
    Phonograph : CursorType # 12
    Chocolate : CursorType # 13
    Glove : CursorType # 14
    MoneySign : CursorType # 15
    Wheeelbarrow : CursorType # 16
    TreeFood : CursorType # 17


class CutScene(LawnMessageBoxListener):
    def __init__(self) -> None: ...
    mApp : LawnApp
    mBoard : Board
    mBossTime : int
    mCrazyDaveCountDown : int
    mCrazyDaveDialogStart : int
    mCrazyDaveLastTalkIndex : int
    mCrazyDaveTime : int
    mCutsceneTime : int
    mFogTime : int
    mGraveStoneTime : int
    mLawnMowerTime : int
    mPlacedLawnItems : bool
    mPlacedZombies : bool
    mPreloaded : bool
    mPreUpdatingBoard : bool
    mReadySetPlantTime : int
    mSeedChoosing : bool
    mSodTime : int
    mUpsellHideBoard : bool
    mZombiesWonReanimID : Reanimation
    mZombiesWonReanimID_Save : int
    def AddFlowerPots(self) -> None: ...
    def AddGraveStoneParticles(self) -> None: ...
    def AddLilypad(self) -> None: ...
    def AddUpsellZombie(self, theZombieType: ZombieType, thePixelX: int, theGridY: int) -> None: ...
    def AdvanceCrazyDaveDialog(self, theJustSkipping: bool) -> None: ...
    def AnimateBoard(self) -> None: ...
    def CalcPosition(self, theTimeStart: int, theTimeEnd: int, thePositionStart: int, thePositionEnd: int) -> int: ...
    def CancelIntro(self) -> None: ...
    def CanGetPacketUpgrade(self) -> bool: ...
    def CanGetSecondPacketUpgrade(self) -> bool: ...
    def CanZombieGoInGridSpot(self, theZombieType: ZombieType, theGridX: int, theGridY: int, theZombieGrid: Array_1[bool]) -> bool: ...
    def ClearUpsellBoard(self) -> None: ...
    def Dispose(self) -> None: ...
    def DrawIntro(self, g: Graphics) -> None: ...
    def DrawUpsell(self, g: Graphics) -> None: ...
    def EndSeedChooser(self) -> None: ...
    def FindAndPlaceZombie(self, theZombieType: ZombieType, theZombieGrid: Array_1[bool]) -> None: ...
    def FindPlaceForStreetZombies(self, theZombieType: ZombieType, theZombieGrid: Array_1[bool], thePosX: clr.Reference[int], thePosY: clr.Reference[int]) -> None: ...
    def Is2x2Zombie(self, theZombieType: ZombieType) -> bool: ...
    def IsAfterSeedChooser(self) -> bool: ...
    def IsBeforePreloading(self) -> bool: ...
    def IsCutSceneOver(self) -> bool: ...
    def IsInShovelTutorial(self) -> bool: ...
    def IsNonScrollingCutscene(self) -> bool: ...
    def IsScrolledLeftAtStart(self) -> bool: ...
    def IsShowingCrazyDave(self) -> bool: ...
    def IsSurvivalRepick(self) -> bool: ...
    def LawnMessageBoxDone(self, theResult: int) -> None: ...
    def LoadIntroBoard(self) -> None: ...
    def LoadUpsellBoardFog(self) -> None: ...
    def LoadUpsellBoardPool(self) -> None: ...
    def LoadUpsellBoardRoof(self) -> None: ...
    def LoadUpsellChallengeScreen(self) -> None: ...
    def MouseDown(self, x: int, y: int) -> None: ...
    def ParseDelayTimeFromMessage(self) -> int: ...
    def ParseTalkTimeFromMessage(self) -> int: ...
    def PlaceAZombie(self, theZombieType: ZombieType, theGridX: int, theGridY: int) -> None: ...
    def PlaceLawnItems(self) -> None: ...
    def PlaceStreetZombies(self) -> None: ...
    def PreloadResources(self) -> None: ...
    def ShouldRunUpsellBoard(self) -> bool: ...
    def ShowShovel(self) -> None: ...
    def ShowZombieWalking(self) -> bool: ...
    def StartLevelIntro(self) -> None: ...
    def StartSeedChooser(self) -> None: ...
    def StartZombiesWon(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateIntro(self) -> None: ...
    def UpdateUpsell(self) -> None: ...
    def UpdateZombiesWon(self) -> None: ...
    def ZombieWonClick(self) -> None: ...


class DamageFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    BypassesShield : DamageFlags # 1
    HitsShieldAndBody : DamageFlags # 2
    Freeze : DamageFlags # 4
    DoesntCauseFlash : DamageFlags # 8
    DoesntLeaveBody : DamageFlags # 16
    Spike : DamageFlags # 32


class DamageRangeFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ground : DamageRangeFlags # 0
    Flying : DamageRangeFlags # 1
    Submerged : DamageRangeFlags # 2
    Dog : DamageRangeFlags # 3
    OffGround : DamageRangeFlags # 4
    Dying : DamageRangeFlags # 5
    Underground : DamageRangeFlags # 6
    OnlyMindcontrolled : DamageRangeFlags # 7


class DebugTextMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : DebugTextMode # 0
    ZombieSpawn : DebugTextMode # 1
    Music : DebugTextMode # 2
    Memory : DebugTextMode # 3
    Collision : DebugTextMode # 4


class DescriptionWidget(Widget):
    def __init__(self) -> None: ...
    FullRect : TRect
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    SCROLLBAR_PAD : int
    def Draw(self, g: Graphics) -> None: ...
    def SetText(self, theText: clr.Reference[str]) -> None: ...


class DrawVariation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : DrawVariation # 0
    Imitater : DrawVariation # 1
    MarigoldWhite : DrawVariation # 2
    MarigoldMagenta : DrawVariation # 3
    MarigoldOrange : DrawVariation # 4
    MarigoldPink : DrawVariation # 5
    MarigoldLightBlue : DrawVariation # 6
    MarigoldRed : DrawVariation # 7
    MarigoldBlue : DrawVariation # 8
    MarigoldViolet : DrawVariation # 9
    MarigoldLavender : DrawVariation # 10
    MarigoldYellow : DrawVariation # 11
    MarigoldLightGreen : DrawVariation # 12
    ZenGarden : DrawVariation # 13
    ZenGardenWater : DrawVariation # 14
    SproutNoFlower : DrawVariation # 15
    ImitaterLess : DrawVariation # 16
    Aquarium : DrawVariation # 17
    Bigidle : DrawVariation # 18


class DropLootType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : DropLootType # 0
    Silver : DropLootType # 1
    Gold : DropLootType # 2
    Diamond : DropLootType # 3
    Sun : DropLootType # 4
    Smallsun : DropLootType # 5
    Largesun : DropLootType # 6
    PresentPlant : DropLootType # 7
    Chocolate : DropLootType # 8
    PresentMinigames : DropLootType # 9
    PresentPuzzleMode : DropLootType # 10
    ThreeSun : DropLootType # 11


class FogLayers(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Fog : FogLayers # 0
    PlanternShine : FogLayers # 1
    Coin : FogLayers # 2
    Rain : FogLayers # 3


class GameButton:
    def __init__(self, theId: int, parent: Widget) -> None: ...
    mApp : LawnApp
    mBtnNoDraw : bool
    mButtonImage : Image
    mButtonOffsetX : int
    mButtonOffsetY : int
    mChecked : bool
    mColors : Array_1[SexyColor]
    mDisabled : bool
    mDisabledImage : Image
    mDisabledRect : TRect
    mDownImage : Image
    mDownRect : TRect
    mDrawStoneButton : bool
    mFont : Font
    mFrameNoDraw : bool
    mHeight : int
    mId : int
    mInverted : bool
    mIsDown : bool
    mIsOver : bool
    mLabelJustify : int
    mNormalRect : TRect
    mOverAlpha : float
    mOverAlphaFadeInSpeed : float
    mOverAlphaSpeed : float
    mOverImage : Image
    mOverOverlayImage : Image
    mOverRect : TRect
    mParentWidget : Widget
    mTextOffsetX : int
    mTextOffsetY : int
    mTextPushOffsetX : int
    mTextPushOffsetY : int
    mWidth : int
    mX : int
    mY : int
    @property
    def mLabel(self) -> str: ...
    @mLabel.setter
    def mLabel(self, value: str) -> str: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawButtonImage(self, g: Graphics, theImage: Image, theRect: TRect, x: int, y: int) -> None: ...
    def HaveButtonImage(self, theImage: Image, theRect: TRect) -> bool: ...
    def IsButtonDown(self) -> bool: ...
    def IsMouseOver(self) -> bool: ...
    @staticmethod
    def MakeButton(theId: int, theListener: ButtonListener, theText: str) -> LawnStoneButton: ...
    @staticmethod
    def MakeNewButton(theId: int, theListener: ButtonListener, theText: str, theFont: Font, theImageNormal: Image, theImageOver: Image, theImageDown: Image) -> NewLawnButton: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def SetDisabled(self, isDisabled: bool) -> None: ...
    def SetFont(self, theFont: Font) -> None: ...
    def SetLabel(self, theLabel: str) -> None: ...
    def Update(self) -> None: ...
    # Skipped DrawStoneButton due to it being static, abstract and generic.

    DrawStoneButton : DrawStoneButton_MethodGroup
    class DrawStoneButton_MethodGroup:
        @typing.overload
        def __call__(self, g: Graphics, x: int, y: int, theWidth: int, theHeight: int, isDown: bool, isHighLighted: bool, theLabel: str) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, x: int, y: int, theWidth: int, theHeight: int, isDown: bool, isHighLighted: bool, theLabel: str, theFont: Font, fontScale: float, isChecked: bool = ...) -> None:...


    class ButtonColours(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Label : GameButton.ButtonColours # 0
        LabelHilite : GameButton.ButtonColours # 1
        DarkOutline : GameButton.ButtonColours # 2
        LightOutline : GameButton.ButtonColours # 3
        MediumOutline : GameButton.ButtonColours # 4
        Bkg : GameButton.ButtonColours # 5
        ColorCount : GameButton.ButtonColours # 6


    class ButtonLabelJustify(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Center : GameButton.ButtonLabelJustify # 0
        Right : GameButton.ButtonLabelJustify # 1
        Left : GameButton.ButtonLabelJustify # -1



class GameConstants:
    def __init__(self) -> None: ...
    AchievementInfo : Array_1[Achievement]
    ART_CHALLEGE_SIZE_X : int
    ART_CHALLEGE_SIZE_Y : int
    BAR_FADE_TIME : int
    BEGHOULED_DELAY_BEFORE_HINT_FLASH : int
    BEGHOULED_DELAY_BEFORE_HINT_FLASH_AGAIN : int
    BEGHOULED_WINNING_SCORE : int
    BLINK_RATE : int
    BLINK_RATE_WALLNUT : int
    BOARD_SHAKE_TIME : int
    BOBSLED_CRASH_TIME : int
    BOSS_BALL_OFFSET_Y : float
    BOSS_FLASH_HEALTH_FRACTION : int
    BUNGEE_ZOMBIE_HEIGHT : int
    BURST_FADE_IN_TIME : int
    BURST_FADE_OUT_TIME : int
    BURST_FOG_FADE_OUT_DELAY : int
    BURST_MIN_TIME : int
    BURST_TIME_AFTER_START_TO_QUEUE_DRUMS : int
    BUTTON_SIZE : int
    BUTTONS_PER_ROW : int
    CHILLED_SPEED_FACTOR : float
    CHOMP_TIME : int
    CLIP_HEIGHT_LIMIT : float
    CLIP_HEIGHT_OFF : float
    CLOUD_MOVE_TIME : int
    CLOUD_WAIT_TIME : int
    CONVEYOR_PACKET_MIN_OFFSET : int
    CONVEYOR_PACKET_OFFSET_Y : int
    CONVEYOR_SPEED : int
    CRATER_TIME : int
    CRAVE_DAVE_BLINK_RATE : int
    DOG_WALKING_DISTANCE : int
    DOLPHIN_JUMP_TIME : int
    DRUMS_FADE_OUT_TIME : int
    DRUMS_FOG_FADE_OUT_TIME : int
    FINAL_LEVEL : int
    FLAG_RAISE_TIME : int
    FOG_BLOW_RETURN_TIME : int
    FOG_CUTSCENE_TIME : int
    gBossZombieList : Array_1[ZombieType]
    gBossZombieList2 : Array_1[ZombieType]
    gCoverInfos : Array_1[GameConstants.CoverInfo]
    gFinalBoss2RainingSeeds : Array_1[SeedType]
    gFlowerCenter : Array_1[LawnFPoint]
    gGameButtonColors : Array_1[SexyColor]
    gLawnParticleArray : Array_1[ParticleParams]
    gLawnReanimationArray : Array_1[ReanimationParams]
    gLawnStringFormatCount : int
    gLawnStringFormats : Array_1[TodStringListFormat]
    gLawnTrailArray : Array_1[TrailParams]
    gPlantDefs : Array_1[PlantDefinition]
    gProjectileDefinition : Array_1[ProjectileDefinition]
    GRAVE_BUSTER_EAT_TIME : int
    gUserVersion : int
    gUserVersionTilApr09 : int
    gUserVersionTilApril08 : int
    gUserVersionTilFeb08 : int
    gUserVersionTilJan09 : int
    gUserVersionTilJuly07 : int
    gUserVersionTilMay08 : int
    gUserVersionTilNov08 : int
    gUserVersionTilSep08 : int
    gZombieAllowedLevels : Array_1[ZombieAllowedLevels]
    gZombieDefs : Array_1[ZombieDefinition]
    gZombieWaves : Array_1[int]
    I_ZOMBIE_LEVEL_COUNT : int
    ICE_CHALLANGE_DELAY : int
    ITEM_GAP : int
    IZOMBIE_ACHIEVEMENT : int
    IZOMBIE_WINNING_SCORE : int
    LAST_STAND_FLAGS : int
    LAWN_FONT_AVE_MS_TO_LOAD : int
    LAWN_IMAGE_AVE_MS_TO_LOAD : int
    LAWN_MOWER_COIN_DELAY : int
    LAWN_MOWER_COIN_END : int
    LAWN_MOWER_COIN_START : int
    LAWN_PARTICLE_AVE_MS_TO_LOAD : int
    LAWN_REANIM_AVE_MS_TO_LOAD : int
    LAWN_SONG_AVE_MS_TO_LOAD : int
    LAWN_SOUND_AVE_MS_TO_LOAD : int
    LEAF_WAIT_TIME : int
    LEVELS_PER_AREA : int
    MAX_CHALLENGE_MODES : int
    MAX_CREDIT_SECTIONS : int
    MAX_MAGNET_ITEMS : int
    MAX_MESSAGE_LENGTH : int
    MAX_POTTED_PLANTS : int
    MAX_PURCHASES : int
    MAX_RENDER_ITEMS : int
    MAX_SCARY_POTS : int
    MAX_ZOMBIE_FOLLOWERS : int
    MAX_ZOMBIE_TYPES : int
    MAX_ZOMBIE_WAVES : int
    MAX_ZOMBIES_IN_WAVE : int
    MENU_BUTTON_TOP_OFFSET : int
    MIN_MESSAGE_TIME : int
    MINI_GAME_COUNT : int
    MORE_GAMES_LIST_OFFSET : int
    MUSIC_ROW_FACTOR : int
    MUSIC_SLIDER_THRESHOLD : float
    NO_IMAGE_ID : int
    NUM_ALMANAC_REANIMS : int
    NUM_ALMANAC_SEEDS : int
    NUM_ALMANAC_ZOMBIES : int
    NUM_ALMANAC_ZOMBIES_PERF_TEST : int
    NUM_BACKUP_DANCERS : int
    NUM_CHALLENGE_MODES : int
    NUM_CLOUDS : int
    NUM_FLAMES_IN_FWOOSH : int
    NUM_FLOWERS : int
    NUM_FOG_ROWS : int
    NUM_LEVELS : int
    NUM_MOTION_TRAIL_FRAMES : int
    NUM_PLACEHOLDER_INTS : int
    NUM_SQUIRRELS : int
    NUM_TREE_CLOUDS : int
    PARTNER_PREVIEW_MAX_DRIFT : int
    POGO_BOUNCE_TIME : int
    PRESENT_OFFSET_Y : int
    PRICE_MULTIPLIER : int
    PROGRESS_METER_COUNTER : int
    QUICKPLAY_SLIDE_COUNT : int
    REANIMATOR_LOAD_TASK_FACTOR : int
    RENDER_GROUP_ARMS : int
    RENDER_GROUP_BOSS_BACK_ARM : int
    RENDER_GROUP_BOSS_BACK_LEG : int
    RENDER_GROUP_BOSS_FIREBALL_ADDITIVE : int
    RENDER_GROUP_BOSS_FIREBALL_TOP : int
    RENDER_GROUP_BOSS_FRONT_LEG : int
    RENDER_GROUP_OVER_SHIELD : int
    RENDER_GROUP_PUMPKIN_BACK : int
    RENDER_GROUP_SHIELD : int
    RENDER_GROUP_TREE_BACKGROUND : int
    RENDER_GROUP_TREE_GRASS : int
    RENDER_GROUP_TREE_TOP : int
    RENDER_GROUP_TREE_TRUNK : int
    ROOF_SLOPE_PER_ROW : int
    ROOF_SLOPE_PER_ROW_OFF : int
    SEEDBANK_MAX : int
    SLIDE_COUNT : int
    SLIDE_OFF_TIME : int
    SLOT_MACHINE_COST : int
    SLOT_MACHINE_TIME : int
    SLOT_MACHINE_WINNING_SCORE : int
    SOUND_EFFECT_VOLUME_FACTOR : float
    STINKY_COIN_OFFSET_Y : float
    STINKY_RENDER_ORDER_OFFSET : int
    STORM_FLASH_TIME : int
    STREET_GRID_SIZE_X : int
    STREET_GRID_SIZE_Y : int
    SUN_COUNTDOWN : int
    SUN_COUNTDOWN_MAX : int
    SUN_COUNTDOWN_RANGE : int
    SURVIVAL_HARD_FLAGS : int
    SURVIVAL_HELL_FLAGS : int
    SURVIVAL_NORMAL_FLAGS : int
    TAP_TAP_TO_PLANT : int
    TESTING_LOAD_BAR : bool
    THOWN_ZOMBIE_GRAVITY : float
    TICKS_BETWEEN_EATS : int
    TICKS_PER_SECOND : int
    TREE_CLOUD_MOVE_TIME : int
    TREE_CLOUD_WAIT_TIME : int
    VASEBREAKER_ACHIEVEMENT : int
    VASEBREAKER_LEVEL_COUNT : int
    WAKE_UP_TIME : int
    YUCKI_HOLD_TIME : int
    YUCKI_PAUSE_TIME : int
    YUCKI_SHORT_PAUSE_TIME : int
    YUCKI_WALK_TIME : int
    ZEN_GARDEN_FADE_DELAY : int
    ZOMBIE_BLINK_RATE : int
    ZOMBIE_COUNTDOWN : int
    ZOMBIE_COUNTDOWN_BEFORE_FLAG : int
    ZOMBIE_COUNTDOWN_BEFORE_REPICK : int
    ZOMBIE_COUNTDOWN_FIRST_WAVE : int
    ZOMBIE_COUNTDOWN_MIN : int
    ZOMBIE_COUNTDOWN_RANGE : int
    ZOMBIE_LIMP_SPEED_FACTOR : int
    ZOMBIE_MINDCONTROLLED_COLOR : SexyColor
    ZOMBIE_WALK_IN_FRONT_DOOR_Y : float
    ZOMBIE_WAVE_CUTSCENE : int
    ZOMBIE_WAVE_DEBUG : int
    ZOMBIE_WAVE_UI : int
    ZOMBIE_WAVE_WINNER : int
    ZOMBIQUARIUM_WINNING_SCORE : int
    @staticmethod
    def GetCircleRectOverlap(theCircleX: int, theCircleY: int, theRadius: int, theRect: TRect) -> bool: ...
    @staticmethod
    def GetRectOverlap(rect1: TRect, rect2: TRect) -> int: ...
    @staticmethod
    def Init() -> None: ...

    class CoverInfo:
        def __init__(self, mX: float, mY: float, mScale: float) -> None: ...
        mScale : float
        mX : float
        mY : float



class GameMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    AdventureStart : GameMode # 0
    Adventure : GameMode # 0
    AdventureCount : GameMode # 1
    SurvivalStart : GameMode # 1
    ChallengeStart : GameMode # 1
    SurvivalNormalStage1 : GameMode # 1
    SurvivalNormalStage2 : GameMode # 2
    SurvivalNormalStage3 : GameMode # 3
    SurvivalNormalStage4 : GameMode # 4
    SurvivalNormalStage5 : GameMode # 5
    SurvivalHardStage1 : GameMode # 6
    SurvivalHardStage2 : GameMode # 7
    SurvivalHardStage3 : GameMode # 8
    SurvivalHardStage4 : GameMode # 9
    SurvivalHardStage5 : GameMode # 10
    PuzzleIZombieCount : GameMode # 10
    ScaryPotterCount : GameMode # 10
    SurvivalEndlessStage1 : GameMode # 11
    ExtraChallengeCount : GameMode # 11
    SurvivalEndlessStage2 : GameMode # 12
    SurvivalEndlessStage3 : GameMode # 13
    SurvivalEndlessStage4 : GameMode # 14
    SurvivalCount : GameMode # 15
    SurvivalEndlessStage5 : GameMode # 15
    MiniGameStart : GameMode # 16
    ChallengeWarAndPeas : GameMode # 16
    ChallengeWallnutBowling : GameMode # 17
    ChallengeSlotMachine : GameMode # 18
    ChallengeRainingSeeds : GameMode # 19
    ChallengeBeghouled : GameMode # 20
    MiniGameCount : GameMode # 20
    ChallengeInvisighoul : GameMode # 21
    ChallengeSeeingStars : GameMode # 22
    ChallengeBeghouledTwist : GameMode # 23
    ChallengeLittleTrouble : GameMode # 24
    ChallengePortalCombat : GameMode # 25
    ChallengeColumn : GameMode # 26
    ChallengeBobsledBonanza : GameMode # 27
    ChallengeSpeed : GameMode # 28
    ChallengeWhackAZombie : GameMode # 29
    ChallengeLastStand : GameMode # 30
    ChallengeWarAndPeas2 : GameMode # 31
    ChallengeWallnutBowling2 : GameMode # 32
    ChallengePogoParty : GameMode # 33
    ChallengeFinalBoss : GameMode # 34
    ChallengeArtChallenge1 : GameMode # 35
    ChallengeSunnyDay : GameMode # 36
    ChallengeResodded : GameMode # 37
    ChallengeBigTime : GameMode # 38
    ChallengeArtChallenge2 : GameMode # 39
    ChallengeAirRaid : GameMode # 40
    ChallengeIce : GameMode # 41
    ChallengeZenGarden : GameMode # 42
    ChallengeHighGravity : GameMode # 43
    ChallengeGraveDanger : GameMode # 44
    ChallengeShovel : GameMode # 45
    ChallengeStormyNight : GameMode # 46
    ChallengeBungeeBlitz : GameMode # 47
    ChallengeSquirrel : GameMode # 48
    TreeOfWisdom : GameMode # 49
    QuickplayCount : GameMode # 50
    ScaryPotterStart : GameMode # 50
    ScaryPotter1 : GameMode # 50
    ScaryPotter2 : GameMode # 51
    ScaryPotter3 : GameMode # 52
    ScaryPotter4 : GameMode # 53
    ScaryPotter5 : GameMode # 54
    ScaryPotter6 : GameMode # 55
    ScaryPotter7 : GameMode # 56
    ScaryPotter8 : GameMode # 57
    ScaryPotter9 : GameMode # 58
    ScaryPotterEndless : GameMode # 59
    PuzzleIZombieStart : GameMode # 60
    PuzzleIZombie1 : GameMode # 60
    PuzzleIZombie2 : GameMode # 61
    PuzzleIZombie3 : GameMode # 62
    PuzzleIZombie4 : GameMode # 63
    PuzzleIZombie5 : GameMode # 64
    PuzzleIZombie6 : GameMode # 65
    PuzzleIZombie7 : GameMode # 66
    PuzzleIZombie8 : GameMode # 67
    PuzzleIZombie9 : GameMode # 68
    PuzzleIZombieEndless : GameMode # 69
    Upsell : GameMode # 70
    Intro : GameMode # 71
    Quickplay1 : GameMode # 72
    QuickplayStart : GameMode # 72
    Quickplay2 : GameMode # 73
    Quickplay3 : GameMode # 74
    Quickplay4 : GameMode # 75
    Quickplay5 : GameMode # 76
    Quickplay6 : GameMode # 77
    Quickplay7 : GameMode # 78
    Quickplay8 : GameMode # 79
    Quickplay9 : GameMode # 80
    Quickplay10 : GameMode # 81
    Quickplay11 : GameMode # 82
    Quickplay12 : GameMode # 83
    Quickplay13 : GameMode # 84
    Quickplay14 : GameMode # 85
    Quickplay15 : GameMode # 86
    Quickplay16 : GameMode # 87
    Quickplay17 : GameMode # 88
    Quickplay18 : GameMode # 89
    Quickplay19 : GameMode # 90
    Quickplay20 : GameMode # 91
    Quickplay21 : GameMode # 92
    Quickplay22 : GameMode # 93
    Quickplay23 : GameMode # 94
    Quickplay24 : GameMode # 95
    Quickplay25 : GameMode # 96
    Quickplay26 : GameMode # 97
    Quickplay27 : GameMode # 98
    Quickplay28 : GameMode # 99
    Quickplay29 : GameMode # 100
    Quickplay30 : GameMode # 101
    Quickplay31 : GameMode # 102
    Quickplay32 : GameMode # 103
    Quickplay33 : GameMode # 104
    Quickplay34 : GameMode # 105
    Quickplay35 : GameMode # 106
    Quickplay36 : GameMode # 107
    Quickplay37 : GameMode # 108
    Quickplay38 : GameMode # 109
    Quickplay39 : GameMode # 110
    Quickplay40 : GameMode # 111
    Quickplay41 : GameMode # 112
    Quickplay42 : GameMode # 113
    Quickplay43 : GameMode # 114
    Quickplay44 : GameMode # 115
    Quickplay45 : GameMode # 116
    Quickplay46 : GameMode # 117
    Quickplay47 : GameMode # 118
    Quickplay48 : GameMode # 119
    Quickplay49 : GameMode # 120
    Quickplay50 : GameMode # 121
    ChallengeZombiquarium : GameMode # 122
    ChallengeAttackOnTitans : GameMode # 123
    ExtraChallengeStart : GameMode # 123
    ChallengeAttackOnTitans2 : GameMode # 124
    ChallengeAttackOnTitans3 : GameMode # 125
    MarvelousPeople : GameMode # 126
    MarvelousPeople2 : GameMode # 127
    MarvelousPeople3 : GameMode # 128
    RogueConveyorbelt : GameMode # 129
    RogueConveyorbeltHard : GameMode # 130
    ChallengeFinalBoss2 : GameMode # 131
    ImitaterRandom : GameMode # 132
    ChallengeColumn2 : GameMode # 133
    ChallengeColumn3 : GameMode # 134
    ChallengeColumn4 : GameMode # 135
    SurvivalHellStage1 : GameMode # 136
    SurvivalHellStage2 : GameMode # 137
    SurvivalHellStage3 : GameMode # 138
    SurvivalHellStage4 : GameMode # 139
    SurvivalHellStage5 : GameMode # 140
    MarvelousPeople4 : GameMode # 141
    PoolParty : GameMode # 142
    ChallengeBobsledBonanza2 : GameMode # 143
    ChallengeMoreAirRaid : GameMode # 144
    BigPoolSurvivalNormalStage : GameMode # 145
    BigPoolSurvivalHardStage : GameMode # 146
    BigPoolSurvivalHellStage : GameMode # 147
    ChallengeFusion : GameMode # 148
    ChallengeStageRandom : GameMode # 149
    OccupyHighGround : GameMode # 150
    GameModeCount : GameMode # 151


class GameObject(abc.ABC):
    mApp : LawnApp
    mBoard : Board
    mHeight : int
    mPosScaled : bool
    mPrevTransX : float
    mPrevTransY : float
    mRenderOrder : int
    mRow : int
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    def BeginDraw(self, g: Graphics) -> bool: ...
    def EndDraw(self, g: Graphics) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def MakeParentGraphicsFrame(self, g: Graphics) -> None: ...
    def PrepareForReuse(self) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...


class GameObjectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : GameObjectType # 0
    Plant : GameObjectType # 1
    Projectile : GameObjectType # 2
    Coin : GameObjectType # 3
    Seedpacket : GameObjectType # 4
    Shovel : GameObjectType # 5
    WateringCan : GameObjectType # 6
    Fertilizer : GameObjectType # 7
    BugSpray : GameObjectType # 8
    Phonograph : GameObjectType # 9
    Chocolate : GameObjectType # 10
    Glove : GameObjectType # 11
    MoneySign : GameObjectType # 12
    Wheelbarrow : GameObjectType # 13
    TreeFood : GameObjectType # 14
    NextGarden : GameObjectType # 15
    PrevGarden : GameObjectType # 16
    MenuButton : GameObjectType # 17
    StoreButton : GameObjectType # 18
    SlotMachineHandle : GameObjectType # 19
    ScaryPot : GameObjectType # 20
    Stinky : GameObjectType # 21
    TreeOfWisdom : GameObjectType # 22


class GameScenes(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Loading : GameScenes # 0
    Menu : GameScenes # 1
    LevelIntro : GameScenes # 2
    Playing : GameScenes # 3
    ZombiesWon : GameScenes # 4
    Award : GameScenes # 5
    Credit : GameScenes # 6
    Challenge : GameScenes # 7
    Leaderboard : GameScenes # 8


class GameSelector(Widget, QuickPlayWidgetListener, MiniGamesWidgetListener, AlmanacListener, StoreListener, ButtonListener):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    mAchievementsScrollWidget : ScrollWidget
    mAchievementsWidget : AchievementsWidget
    mAdventureButton : NewLawnButton
    mAlmanacButton : DialogButton
    mApp : LawnApp
    mChallengePageLimboButton : DialogButton
    mChallengePageSurvivalButton : DialogButton
    mClip : bool
    mCloudCounter : Array_1[int]
    mCloudReanimID : Array_1[Reanimation]
    mColors : List_1[Color]
    mComicButton : DialogButton
    mCommunityButton : DialogButton
    mCreativeLevelButton : DialogButton
    mDestX : int
    mDestY : int
    mDisabled : bool
    mDoFinger : bool
    mDoNewGameAfterStore : bool
    mFadeInCounter : int
    mFlowerReanimID : Array_1[Reanimation]
    mFullScreenButton : DialogButton
    mHalfDeltaHeight : int
    mHalfDeltaWidth : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHasTrophy : bool
    mHeight : int
    mInUserDialog : bool
    mIsDown : bool
    mIsOver : bool
    mIZombieButton : ToggleButton
    mLastWMUpdateCount : int
    mLeafCounter : int
    mLeftLength : int
    mLevel : int
    mLexText : str
    mLoading : bool
    mMiniGamesButton : DialogButton
    mMiniGamesScrollWidget : ScrollWidget
    mMiniGamesWidget : MiniGamesWidget
    mMiscButton : ToggleButton
    mMoreGamesListWidget : MoreGamesListWidget
    mMoreGamesScrollWidget : ScrollWidget
    mMoreWaysBackButton : DialogButton
    mMoreWaysToPlayButton : NewLawnButton
    mMouseInsets : Insets
    mMouseVisible : bool
    mNeedToPlayRollIn : bool
    mOptionsButton : NewLawnButton
    mParent : WidgetContainer
    mPekingCounter : float
    mPriority : int
    mPuzzleButton : DialogButton
    mQuickplayLocked : bool
    mQuickplayScrollWidget : ScrollWidget
    mQuickplaySlideCounter : int
    mQuickplayWidget : QuickPlayWidget
    mRetractingQuickplay : bool
    mSelectedQuickplayButtonId : int
    mShowStartButton : bool
    mSignState : SelectorSignState
    mSlideCounter : int
    mStartX : int
    mStartY : int
    mStoreButton : DialogButton
    mSurvivalButton : DialogButton
    mTabNext : Widget
    mTabPrev : Widget
    mTrophyButton : DialogButton
    mTrophyParticleID : TodParticleSystem
    mUnlockButton : DialogButton
    mUnlockSelectorCheat : bool
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mUserDialogButton : DialogButton
    mVaseBreakerButton : ToggleButton
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mWoodSignReanimID : Reanimation
    mX : int
    mY : int
    mZenGardenButton : NewLawnButton
    mZOrder : int
    @property
    def mLastScene(self) -> GameSelector.GameSelectorScene: ...
    @property
    def mScene(self) -> GameSelector.GameSelectorScene: ...
    @mScene.setter
    def mScene(self, value: GameSelector.GameSelectorScene) -> GameSelector.GameSelectorScene: ...
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def AddTrophySparkle(self) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def BackFromAlmanac(self) -> None: ...
    def BackFromStore(self) -> None: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, id: int) -> None: ...
    def ButtonMouseEnter(self, theId: int) -> None: ...
    def ButtonMouseLeave(self, id: int) -> None: ...
    def ButtonMouseMove(self, id: int, x: int, y: int) -> None: ...
    def ButtonMouseTick(self, id: int) -> None: ...
    def ClickedAdventure(self) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawMainMenuArea(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def DrawScreen2(self, g: Graphics) -> None: ...
    def DrawScreen3(self, g: Graphics) -> None: ...
    def HideAllHidableButton(self) -> None: ...
    def InitMainButton(self) -> None: ...
    def InitMainSmallButton(self) -> None: ...
    def InitMoreGamesButton(self) -> None: ...
    def InitPuzzleButton(self) -> None: ...
    def KeyChar(self, theChar: SexyChar) -> None: ...
    def KeyDown(self, theKey: KeyCode) -> None: ...
    def LoadGames(self) -> None: ...
    def LowerSign(self) -> None: ...
    def MiniGamesStageSelected(self, theLevel: int) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MoveToQuickplay(self, theDoFadeIn: bool, theButton: GameSelectorButtons) -> None: ...
    def PopulateQuickPlayWidget(self) -> None: ...
    def PuzzleSetPosition(self, theId: GameSelectorButtons) -> None: ...
    def QuickPlayStageSelected(self, theLevel: int) -> None: ...
    def RaiseSign(self) -> None: ...
    def RetractQuickPlayWidget(self) -> None: ...
    def SetButtonAvailable(self, button: DialogButton, available: bool, preserveVisibility: bool = ...) -> None: ...
    def ShouldDoZenTuturialBeforeAdventure(self) -> bool: ...
    def SlideOutQuickPlayWidget(self) -> None: ...
    def SlideTo(self, theX: int, theY: int) -> None: ...
    def SwitchToCreativeLevel(self) -> None: ...
    def SwitchToMain(self) -> None: ...
    def SwitchToMiniGames(self) -> None: ...
    def SwitchToMoreGames(self, isInstant: bool = ...) -> None: ...
    def SwitchToPuzzle(self) -> None: ...
    def SwitchToSurvival(self) -> None: ...
    def SyncAllHidableButton(self) -> None: ...
    def SyncButtons(self) -> None: ...
    def SyncButtonVisible(self, button: DialogButton) -> None: ...
    def SyncProfile(self, theShowLoading: bool) -> None: ...
    def UnlockGame(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateScreen(self) -> None: ...
    def UpdateSmallButtonPosition(self) -> None: ...
    def UpdateUIPosition(self) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, id: int) -> None:...
        @typing.overload
        def __call__(self, theId: int, theClickCount: int) -> None:...


    class GameSelectorAdventureType(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        First : GameSelector.GameSelectorAdventureType # 0
        Second : GameSelector.GameSelectorAdventureType # 1
        Quick : GameSelector.GameSelectorAdventureType # 2


    class GameSelectorScene(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Main : GameSelector.GameSelectorScene # 0
        MoreGames : GameSelector.GameSelectorScene # 1
        Puzzle : GameSelector.GameSelectorScene # 2
        MiniGame : GameSelector.GameSelectorScene # 3
        Survival : GameSelector.GameSelectorScene # 4
        CreativeLevel : GameSelector.GameSelectorScene # 5



class GameSelectorButtons(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Adventure : GameSelectorButtons # 100
    MoreWays : GameSelectorButtons # 101
    QuickplayBack : GameSelectorButtons # 102
    Options : GameSelectorButtons # 103
    Help : GameSelectorButtons # 104
    Quit : GameSelectorButtons # 105
    Store : GameSelectorButtons # 106
    UnlockGame : GameSelectorButtons # 107
    Almanac : GameSelectorButtons # 108
    UpdateAvailable : GameSelectorButtons # 109
    Leaderboards : GameSelectorButtons # 110
    MiniGames : GameSelectorButtons # 111
    Vasebreaker : GameSelectorButtons # 112
    IZombie : GameSelectorButtons # 113
    Misc : GameSelectorButtons # 114
    ZenGarden : GameSelectorButtons # 115
    ChangeUser : GameSelectorButtons # 116
    ChallengePageSurvival : GameSelectorButtons # 117
    ChallengePageLimbo : GameSelectorButtons # 118
    Survival : GameSelectorButtons # 119
    Puzzle : GameSelectorButtons # 120
    CreativeLevel : GameSelectorButtons # 121
    MiniGameRaw : GameSelectorButtons # 122
    MiniGameHidden : GameSelectorButtons # 123
    Comic : GameSelectorButtons # 124
    Unlock : GameSelectorButtons # 125
    Community : GameSelectorButtons # 126
    FullScreen : GameSelectorButtons # 127
    Trophy : GameSelectorButtons # 128


class GameType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Action : GameType # 0
    Strategy : GameType # 1
    Puzzle : GameType # 2
    GameTypeCount : GameType # 3


class GardenType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Main : GardenType # 0
    Mushroom : GardenType # 1
    Wheelbarrow : GardenType # 2
    Aquarium : GardenType # 3
    Main2 : GardenType # 4
    Mushroom2 : GardenType # 5
    Night : GardenType # 6
    GardenTypeCount : GardenType # 7


class GlobalContentManager:
    def __init__(self, m: Main) -> None: ...
    content : ContentManager
    cursor_texture : Texture2D
    DEFAULT_FONT : SpriteFont
    graphicsDevice : GraphicsDevice
    LOCALIZED_FONT_ARIAL : SpriteFont
    main : Main
    splashScreen_ring : Texture2D
    splashScreen_texture : Texture2D
    def cleanUp(self) -> None: ...
    def LoadFonts(self) -> None: ...
    def LoadGameContent(self) -> None: ...
    def LoadLevelBackdrops(self) -> None: ...
    def LoadSounds(self) -> None: ...
    def LoadSplashScreen(self) -> None: ...


class GlobalMembersReanimIds(abc.ABC):
    ReanimTrackId_additive : str
    ReanimTrackId_anim_appear : str
    ReanimTrackId_anim_aquarium_bite : str
    ReanimTrackId_anim_aquarium_death : str
    ReanimTrackId_anim_aquarium_swim : str
    ReanimTrackId_anim_armed : str
    ReanimTrackId_anim_armraise : str
    ReanimTrackId_anim_attack : str
    ReanimTrackId_anim_attract : str
    ReanimTrackId_anim_bigidle : str
    ReanimTrackId_anim_bigsleep : str
    ReanimTrackId_anim_bite : str
    ReanimTrackId_anim_blahblah : str
    ReanimTrackId_anim_blink : str
    ReanimTrackId_anim_blink_thrice : str
    ReanimTrackId_anim_blink_twice : str
    ReanimTrackId_anim_blink_twitch : str
    ReanimTrackId_anim_blink1 : str
    ReanimTrackId_anim_blink2 : str
    ReanimTrackId_anim_blink3 : str
    ReanimTrackId_anim_block : str
    ReanimTrackId_anim_blow : str
    ReanimTrackId_anim_bounce : str
    ReanimTrackId_anim_bucket : str
    ReanimTrackId_anim_bungee_1_enter : str
    ReanimTrackId_anim_bungee_1_leave : str
    ReanimTrackId_anim_caidan : str
    ReanimTrackId_anim_charge : str
    ReanimTrackId_anim_chew : str
    ReanimTrackId_anim_cone : str
    ReanimTrackId_anim_crazy : str
    ReanimTrackId_anim_crumble : str
    ReanimTrackId_anim_crumble_noaxe : str
    ReanimTrackId_anim_dance : str
    ReanimTrackId_anim_death : str
    ReanimTrackId_anim_death2 : str
    ReanimTrackId_anim_dig : str
    ReanimTrackId_anim_dissapear : str
    ReanimTrackId_anim_dizzy : str
    ReanimTrackId_anim_dolphinjump : str
    ReanimTrackId_anim_done : str
    ReanimTrackId_anim_drill : str
    ReanimTrackId_anim_drive : str
    ReanimTrackId_anim_drop : str
    ReanimTrackId_anim_eat : str
    ReanimTrackId_anim_eat_nopaper : str
    ReanimTrackId_anim_enter : str
    ReanimTrackId_anim_enterup : str
    ReanimTrackId_anim_explode : str
    ReanimTrackId_anim_face : str
    ReanimTrackId_anim_face1 : str
    ReanimTrackId_anim_face2 : str
    ReanimTrackId_anim_face3 : str
    ReanimTrackId_anim_flag : str
    ReanimTrackId_anim_flag_loop : str
    ReanimTrackId_anim_flame : str
    ReanimTrackId_anim_form : str
    ReanimTrackId_anim_gasp : str
    ReanimTrackId_anim_glow : str
    ReanimTrackId_anim_grab : str
    ReanimTrackId_anim_grow : str
    ReanimTrackId_anim_head_attack_1 : str
    ReanimTrackId_anim_head_attack_2 : str
    ReanimTrackId_anim_head_attack_3 : str
    ReanimTrackId_anim_head_attack_4 : str
    ReanimTrackId_anim_head_attack_5 : str
    ReanimTrackId_anim_head_enter : str
    ReanimTrackId_anim_head_idle : str
    ReanimTrackId_anim_head_idle1 : str
    ReanimTrackId_anim_head_idle2 : str
    ReanimTrackId_anim_head_idle3 : str
    ReanimTrackId_anim_head_jaw : str
    ReanimTrackId_anim_head_leave : str
    ReanimTrackId_anim_head_look : str
    ReanimTrackId_anim_head1 : str
    ReanimTrackId_anim_head2 : str
    ReanimTrackId_anim_head3 : str
    ReanimTrackId_anim_idle : str
    ReanimTrackId_anim_idle_aquarium : str
    ReanimTrackId_anim_idle_handing : str
    ReanimTrackId_anim_idle_noflower : str
    ReanimTrackId_anim_idle2 : str
    ReanimTrackId_anim_idlehigh : str
    ReanimTrackId_anim_in : str
    ReanimTrackId_anim_jump : str
    ReanimTrackId_anim_jumpdown : str
    ReanimTrackId_anim_jumpdown_left : str
    ReanimTrackId_anim_jumpdown_left_water : str
    ReanimTrackId_anim_jumpdown_water : str
    ReanimTrackId_anim_jumpinpool : str
    ReanimTrackId_anim_jumpup : str
    ReanimTrackId_anim_laddereat : str
    ReanimTrackId_anim_ladderwalk : str
    ReanimTrackId_anim_land : str
    ReanimTrackId_anim_land_treasure : str
    ReanimTrackId_anim_landing : str
    ReanimTrackId_anim_landsuck : str
    ReanimTrackId_anim_laugh : str
    ReanimTrackId_anim_leave : str
    ReanimTrackId_anim_lift : str
    ReanimTrackId_anim_light : str
    ReanimTrackId_anim_lookleft : str
    ReanimTrackId_anim_lookright : str
    ReanimTrackId_anim_loop : str
    ReanimTrackId_anim_lower : str
    ReanimTrackId_anim_mediumtalk : str
    ReanimTrackId_anim_moonwalk : str
    ReanimTrackId_anim_nonactive_idle2 : str
    ReanimTrackId_anim_normal : str
    ReanimTrackId_anim_open_pot : str
    ReanimTrackId_anim_out : str
    ReanimTrackId_anim_placeladder : str
    ReanimTrackId_anim_pogo : str
    ReanimTrackId_anim_point : str
    ReanimTrackId_anim_pop : str
    ReanimTrackId_anim_puff : str
    ReanimTrackId_anim_pull : str
    ReanimTrackId_anim_pulse : str
    ReanimTrackId_anim_push : str
    ReanimTrackId_anim_raise : str
    ReanimTrackId_anim_return : str
    ReanimTrackId_anim_ride : str
    ReanimTrackId_anim_rise : str
    ReanimTrackId_anim_role : str
    ReanimTrackId_anim_run : str
    ReanimTrackId_anim_rustle : str
    ReanimTrackId_anim_rv_1 : str
    ReanimTrackId_anim_scared : str
    ReanimTrackId_anim_scaredidle : str
    ReanimTrackId_anim_screen : str
    ReanimTrackId_anim_screendoor : str
    ReanimTrackId_anim_shoot : str
    ReanimTrackId_anim_shooting : str
    ReanimTrackId_anim_shooting1 : str
    ReanimTrackId_anim_shooting2 : str
    ReanimTrackId_anim_shooting3 : str
    ReanimTrackId_anim_shootinghigh : str
    ReanimTrackId_anim_sleep : str
    ReanimTrackId_anim_smalltalk : str
    ReanimTrackId_anim_smash : str
    ReanimTrackId_anim_spawn_1 : str
    ReanimTrackId_anim_spawn_2 : str
    ReanimTrackId_anim_spawn_3 : str
    ReanimTrackId_anim_spawn_4 : str
    ReanimTrackId_anim_spawn_5 : str
    ReanimTrackId_anim_splitpea_blink : str
    ReanimTrackId_anim_splitpea_idle : str
    ReanimTrackId_anim_splitpea_shooting : str
    ReanimTrackId_anim_stem : str
    ReanimTrackId_anim_stomp_1 : str
    ReanimTrackId_anim_stomp_2 : str
    ReanimTrackId_anim_stomp_3 : str
    ReanimTrackId_anim_stomp_4 : str
    ReanimTrackId_anim_suck : str
    ReanimTrackId_anim_superlongdeath : str
    ReanimTrackId_anim_swallow : str
    ReanimTrackId_anim_swim : str
    ReanimTrackId_anim_talk_handing : str
    ReanimTrackId_anim_teeter : str
    ReanimTrackId_anim_throw : str
    ReanimTrackId_anim_thrown : str
    ReanimTrackId_anim_tongue : str
    ReanimTrackId_anim_tricked : str
    ReanimTrackId_anim_unarmed_idle : str
    ReanimTrackId_anim_uptoeat : str
    ReanimTrackId_anim_walk_nopaper : str
    ReanimTrackId_anim_walk2 : str
    ReanimTrackId_anim_walkdolphin : str
    ReanimTrackId_anim_water : str
    ReanimTrackId_anim_waterdeath : str
    ReanimTrackId_anim_waterplants : str
    ReanimTrackId_anim_whack_zombie : str
    ReanimTrackId_anim_wheelie1 : str
    ReanimTrackId_anim_wheelie2 : str
    ReanimTrackId_anim_zengarden : str
    ReanimTrackId_bag : str
    ReanimTrackId_bigspike2 : str
    ReanimTrackId_bigspike3 : str
    ReanimTrackId_boss_eyeglow_red : str
    ReanimTrackId_boss_head : str
    ReanimTrackId_boss_head2 : str
    ReanimTrackId_boss_innerleg_foot : str
    ReanimTrackId_boss_jaw : str
    ReanimTrackId_boss_mouthglow_red : str
    ReanimTrackId_boss_outerarm_hand : str
    ReanimTrackId_boss_outerarm_thumb2 : str
    ReanimTrackId_boss_outerleg_foot : str
    ReanimTrackId_cobcannon_cob : str
    ReanimTrackId_dave_eye : str
    ReanimTrackId_dave_handinghand : str
    ReanimTrackId_dave_head : str
    ReanimTrackId_dave_mouths : str
    ReanimTrackId_doomshroom_head1 : str
    ReanimTrackId_doomshroom_head2 : str
    ReanimTrackId_doomshroom_head3 : str
    ReanimTrackId_fire : str
    ReanimTrackId_fire_broken : str
    ReanimTrackId_fireshroom_body : str
    ReanimTrackId_fireshroom_head1 : str
    ReanimTrackId_fireShroom_sleepinghead : str
    ReanimTrackId_hat : str
    ReanimTrackId_ice_highlight : str
    ReanimTrackId_impblink : str
    ReanimTrackId_imphead : str
    ReanimTrackId_pot_top : str
    ReanimTrackId_propeller : str
    ReanimTrackId_pumpkin_back : str
    ReanimTrackId_pumpkin_front : str
    ReanimTrackId_shell : str
    ReanimTrackId_splitpea_head : str
    ReanimTrackId_superglow : str
    ReanimTrackId_turn : str
    ReanimTrackId_welcome : str
    ReanimTrackId_zombie_body : str
    ReanimTrackId_zombie_bungi_body : str
    ReanimTrackId_zombie_catapult_basketball : str
    ReanimTrackId_zombie_catapult_basketball2 : str
    ReanimTrackId_zombie_catapult_basketball3 : str
    ReanimTrackId_zombie_catapult_basketball4 : str
    ReanimTrackId_zombie_catapult_driver_head : str
    ReanimTrackId_zombie_catapult_pole : str
    ReanimTrackId_zombie_catapult_siding : str
    ReanimTrackId_zombie_digger_dirt : str
    ReanimTrackId_zombie_digger_hardhat : str
    ReanimTrackId_zombie_digger_outerarm_upper : str
    ReanimTrackId_zombie_digger_pickaxe : str
    ReanimTrackId_zombie_disco_outerhand : str
    ReanimTrackId_zombie_dolphinrider_dolphininwater : str
    ReanimTrackId_zombie_dolphinrider_outerarm_upper : str
    ReanimTrackId_zombie_dolphinrider_whitewater : str
    ReanimTrackId_zombie_duckytube : str
    ReanimTrackId_zombie_flag : str
    ReanimTrackId_zombie_flaghand : str
    ReanimTrackId_zombie_football_helmet : str
    ReanimTrackId_zombie_football_leftarm_hand : str
    ReanimTrackId_zombie_football_leftarm_upper : str
    ReanimTrackId_zombie_gargantua_body1 : str
    ReanimTrackId_zombie_gargantuar_outerarm_lower : str
    ReanimTrackId_zombie_gargantuar_outerleg_foot : str
    ReanimTrackId_zombie_gargantuar_telephonepole : str
    ReanimTrackId_zombie_gargantuar_whiterope : str
    ReanimTrackId_zombie_imp_outerarm_upper : str
    ReanimTrackId_zombie_innerarm_screendoor : str
    ReanimTrackId_zombie_innerarm3 : str
    ReanimTrackId_zombie_jackbox_box : str
    ReanimTrackId_zombie_jackbox_handle : str
    ReanimTrackId_zombie_jackbox_outerarm_lower : str
    ReanimTrackId_zombie_jackson_outerarm_upper : str
    ReanimTrackId_zombie_ladder_1 : str
    ReanimTrackId_zombie_ladder_outerarm_upper : str
    ReanimTrackId_zombie_mustache : str
    ReanimTrackId_zombie_outerarm_hand : str
    ReanimTrackId_zombie_outerarm_lower : str
    ReanimTrackId_zombie_outerarm_upper : str
    ReanimTrackId_zombie_paper_hands : str
    ReanimTrackId_zombie_paper_leftarm_lower : str
    ReanimTrackId_zombie_paper_leftarm_upper : str
    ReanimTrackId_zombie_paper_paper : str
    ReanimTrackId_zombie_pogo_stick : str
    ReanimTrackId_zombie_pogo_stick2 : str
    ReanimTrackId_zombie_pogo_stickhands : str
    ReanimTrackId_zombie_polevaulter_outerarm_lower : str
    ReanimTrackId_zombie_polevaulter_outerarm_upper : str
    ReanimTrackId_zombie_snorkle_outerarm_upper : str
    ReanimTrackId_zombie_snorkle_whitewater : str
    ReanimTrackId_zombie_snorkle_whitewater2 : str
    ReanimTrackId_zombie_whitewater : str
    ReanimTrackId_zombie_whitewater2 : str
    ReanimTrackId_zombie_yeti_outerarm_upper : str
    ReanimTrackId_zombie_zamboni_1 : str
    ReanimTrackId_zombie_zamboni_2 : str
    ReanimTrackId_zombieswon : str


class GraveStoneLayers(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Brain : GraveStoneLayers # 0
    Squirrel : GraveStoneLayers # 1
    Door2 : GraveStoneLayers # 2
    Stones : GraveStoneLayers # 3
    Door1 : GraveStoneLayers # 4
    Daisies : GraveStoneLayers # 5
    BossFireball : GraveStoneLayers # 6
    Bungee : GraveStoneLayers # 7
    SquishedPlant : GraveStoneLayers # 8
    Rake : GraveStoneLayers # 9


class GridItem:
    mApp : LawnApp
    mBoard : Board
    mDead : bool
    mGoalX : float
    mGoalY : float
    mGridItemCounter : int
    mGridItemParticleID : TodParticleSystem
    mGridItemParticleID_Save : int
    mGridItemReanimID : Reanimation
    mGridItemReanimID_Save : int
    mGridItemState : GridItemState
    mGridItemType : GridItemType
    mGridX : int
    mGridY : int
    mHighlighted : bool
    mMotionTrailCount : int
    mMotionTrailFrames : Array_1[MotionTrailFrame]
    mPosX : float
    mPosY : float
    mRenderOrder : int
    mScaryPotType : ScaryPotType
    mSeedType : SeedType
    mSunCount : int
    mTransparentCounter : int
    mZombieType : ZombieType
    def AddGraveStoneParticles(self) -> None: ...
    def ClosePortal(self) -> None: ...
    def DoRakeDamage(self) -> None: ...
    def DrawCrater(self, g: Graphics) -> None: ...
    def DrawGraveStone(self, g: Graphics) -> None: ...
    def DrawGridItem(self, g: Graphics) -> None: ...
    def DrawGridItemOverlay(self, g: Graphics) -> None: ...
    def DrawIZombieBrain(self, g: Graphics) -> None: ...
    def DrawLadder(self, g: Graphics) -> None: ...
    def DrawScaryPot(self, g: Graphics) -> None: ...
    def DrawSquirrel(self, g: Graphics) -> None: ...
    def DrawStinky(self, g: Graphics) -> None: ...
    @staticmethod
    def GetNewGridItem() -> GridItem: ...
    def GridItemDie(self) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def OpenPortal(self) -> None: ...
    def PrepareForReuse(self) -> None: ...
    def RakeFindZombie(self) -> Zombie: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def Update(self) -> None: ...
    def UpdateBrain(self) -> None: ...
    def UpdatePortal(self) -> None: ...
    def UpdateRake(self) -> None: ...
    def UpdateScaryPot(self) -> None: ...
    def UpdateTalisman(self) -> None: ...
    def UpdateTalismanMove(self) -> None: ...


class GridItemID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : GridItemID # 0


class GridItemState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : GridItemState # 0
    GravestoneSpecial : GridItemState # 1
    PortalClosed : GridItemState # 2
    ScaryPotQuestion : GridItemState # 3
    ScaryPotLeaf : GridItemState # 4
    ScaryPotZombie : GridItemState # 5
    SquirrelWaiting : GridItemState # 6
    SquirrelPeeking : GridItemState # 7
    SquirrelRunningUp : GridItemState # 8
    SquirrelRunningDown : GridItemState # 9
    SquirrelRunningLeft : GridItemState # 10
    SquirrelRunningRight : GridItemState # 11
    SquirrelCaught : GridItemState # 12
    SquirrelZombie : GridItemState # 13
    ZenToolWateringCan : GridItemState # 14
    ZenToolFertilizer : GridItemState # 15
    ZenToolBugSpray : GridItemState # 16
    ZenToolPhonograph : GridItemState # 17
    ZenToolGoldWateringCan : GridItemState # 18
    StinkyWalkingLeft : GridItemState # 19
    StinkyTurningLeft : GridItemState # 20
    StinkyWalkingRight : GridItemState # 21
    StinkyTurningRight : GridItemState # 22
    StinkySleeping : GridItemState # 23
    StinkyFallingAsleep : GridItemState # 24
    StinkyWakingUp : GridItemState # 25
    RakeAttracting : GridItemState # 26
    RakeWaiting : GridItemState # 27
    RakeTriggered : GridItemState # 28
    BrainSquished : GridItemState # 29
    TalismanDisappearing : GridItemState # 30


class GridItemType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : GridItemType # 0
    Gravestone : GridItemType # 1
    Crater : GridItemType # 2
    Ladder : GridItemType # 3
    PortalCircle : GridItemType # 4
    PortalSquare : GridItemType # 5
    Brain : GridItemType # 6
    ScaryPot : GridItemType # 7
    Squirrel : GridItemType # 8
    ZenTool : GridItemType # 9
    Stinky : GridItemType # 10
    Rake : GridItemType # 11
    IzombieBrain : GridItemType # 12
    Talisman : GridItemType # 13
    TalismanMove : GridItemType # 14


class GridSquareType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : GridSquareType # 0
    Grass : GridSquareType # 1
    Dirt : GridSquareType # 2
    Pool : GridSquareType # 3
    HighGround : GridSquareType # 4
    Shallow : GridSquareType # 5


class GroundLayers(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    PoolSparkle : GroundLayers # 0
    Crater : GroundLayers # 1
    Ice : GroundLayers # 2
    Shadow : GroundLayers # 3


class HelmType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : HelmType # 0
    TrafficCone : HelmType # 1
    Pail : HelmType # 2
    Football : HelmType # 3
    Digger : HelmType # 4
    Redeyes : HelmType # 5
    Headband : HelmType # 6
    Bobsled : HelmType # 7
    Wallnut : HelmType # 8
    Tallnut : HelmType # 9
    Bell : HelmType # 10
    FootballPremium : HelmType # 11
    RobotTitanHead : HelmType # 12
    RedeyeRobotTitanHead : HelmType # 13


class HitResult:
    mObject : typing.Any
    mObjectType : GameObjectType


class InGameButtons(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MenuButton : InGameButtons # 0
    StoreButton : InGameButtons # 1
    AccelerateButton : InGameButtons # 2
    PauseButton : InGameButtons # 3


class Label(Widget):
    def __init__(self, text: str, font: Font, color: Color, scale: float = ..., just: DrawStringJustification = ...) -> None: ...
    FullRect : TRect
    mClip : bool
    mColor : Color
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mDrawStringJustification : DrawStringJustification
    mFont : Font
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mScale : float
    mTabNext : Widget
    mTabPrev : Widget
    mText : str
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...


class LaunchTime(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : LaunchTime # 0
    RepeaterPrelaunch : LaunchTime # 1


class LawnApp(SexyAppBase):
    def __init__(self, m: Main) -> None: ...
    achievementToCheck : AchievementId
    applicationStoragePath : str
    AppVersionNumber : str
    checkGiveAchievements : bool
    gSexyAppBase : SexyAppBase
    mAppCounter : int
    mAppRandSeed : int
    mAutoStartLoadingThread : bool
    mAwardScreen : AwardScreen
    mBoard : Board
    mBoardResult : BoardResult
    mBoolProperties : Dictionary_2[str, bool]
    mChallengeScreen : ChallengeScreen
    mCheatHoverDialog : Dialog
    mCloseRequest : bool
    mCompanyName : str
    mCompletedLoadingThreadTasks : int
    mContentManager : ContentManager
    mControlButtonList : LinkedList_1[ButtonWidget]
    mCrazyDaveBlinkCounter : int
    mCrazyDaveBlinkReanimID : Reanimation
    mCrazyDaveMessageIndex : int
    mCrazyDaveMessageText : str
    mCrazyDaveReanimID : Reanimation
    mCrazyDaveState : CrazyDaveState
    mCreatedImageList : LinkedList_1[Image]
    mCreditScreen : CreditScreen
    mDaisyCheck : TypingCheck
    mDaisyMode : bool
    mDanceCheck : TypingCheck
    mDanceMode : bool
    mDebugTrialLocked : bool
    mDialogList : LinkedList_1[Dialog]
    mDialogMap : Dictionary_2[int, Dialog]
    mDoubleProperties : Dictionary_2[str, float]
    mEasyPlantingCheat : bool
    mEffectSystem : EffectSystem
    mFirstTimeGameSelector : bool
    mFullCompanyName : str
    mFutureCheck : TypingCheck
    mFutureMode : bool
    mGameMode : GameMode
    mGameScene : GameScenes
    mGameSelector : GameSelector
    mGamesPlayed : int
    mHeight : int
    mImagesToBeFiltered : ConcurrentQueue_1[Image]
    mInitialized : bool
    mInterfaceOrientation : UI_ORIENTATION
    mIntProperties : Dictionary_2[str, int]
    mIsOrientationLocked : bool
    mKilledYetiAndRestarted : bool
    mKonamiCheck : TypingCheck
    mLastLevelStats : LevelStats
    mLawnMessageBoxListener : LawnMessageBoxListener
    mLeaderboardScreen : LeaderboardScreen
    mLoaded : bool
    mLoadingFailed : bool
    mLoadingThreadCompleted : bool
    mLoadingThreadStarted : bool
    mLoadingZombiesThreadCompleted : bool
    mMaxExecutions : int
    mMaxPlays : int
    mMaxTime : int
    mMod : str
    mMoustacheCheck : TypingCheck
    mMusic : Music
    mMusicEnabled : bool
    mMusicInterface : MusicInterface
    mMustacheCheck : TypingCheck
    mMustacheMode : bool
    mMuteCount : int
    mMuteSoundsForCutscene : bool
    mNumLoadingThreadTasks : int
    mOldFocus : Widget
    mPaused : bool
    mPinataCheck : TypingCheck
    mPinataMode : bool
    mPlayTimeActiveSession : int
    mPlayTimeInactiveSession : int
    mProdName : str
    mProfileMgr : ProfileMgr
    mReadFromRegistry : bool
    mReanimatorCache : ReanimatorCache
    mReferId : str
    mRegisterLink : str
    mRegisterResourcesLoaded : bool
    mResourceManager : ResourceManager
    mRestoreGameMode : GameMode
    mRestoreLocation : RestoreLocation
    mScreenScales : ScreenScales
    mSeedChooserScreen : SeedChooserScreen
    mSessionID : int
    mSfxVolume : float
    mShutdown : bool
    mSoundManager : SoundManager
    mSoundSystem : TodFoley
    mStringProperties : Dictionary_2[str, str]
    mStringVectorProperties : Dictionary_2[str, List_1[str]]
    mSukhbirCheck : TypingCheck
    mSukhbirMode : bool
    mSuperMowerCheck : TypingCheck
    mSuperMowerCheck2 : TypingCheck
    mSuperMowerMode : bool
    mTexturesToBePremultiplied : ConcurrentQueue_1[Texture2D]
    mTitle : str
    mTitleScreen : TitleScreen
    mTodCheatKeys : bool
    mTrialType : TrialType
    mUpdateAppDepth : int
    mUpdateCount : int
    mWidgetManager : WidgetManager
    mWidth : int
    mZenGarden : ZenGarden
    saveStateLock : typing.Any
    @property
    def mMusicVolume(self) -> float: ...
    @mMusicVolume.setter
    def mMusicVolume(self, value: float) -> float: ...
    @property
    def mPlayerInfo(self) -> PlayerInfo: ...
    @mPlayerInfo.setter
    def mPlayerInfo(self, value: PlayerInfo) -> PlayerInfo: ...
    @property
    def WantsToExit(self) -> bool: ...
    @WantsToExit.setter
    def WantsToExit(self, value: bool) -> bool: ...
    def AboutToEarnGoldSunflower(self) -> bool: ...
    def AddTodParticle(self, theX: float, theY: float, aRenderOrder: int, theEffect: ParticleEffect) -> TodParticleSystem: ...
    def AdvanceCrazyDaveText(self) -> bool: ...
    def AppEnteredBackground(self) -> None: ...
    def Apply500pMode(self, enable: bool) -> None: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonPress(self, theId: int) -> None: ...
    def CanDoDaisyMode(self) -> bool: ...
    def CanDoDanceMode(self) -> bool: ...
    def CanDoPinataMode(self) -> bool: ...
    def CanDoRegisterDialog(self) -> bool: ...
    def CanPauseNow(self) -> bool: ...
    def CanShowAlmanac(self) -> bool: ...
    def CanShowStore(self) -> bool: ...
    def CanShowZenGarden(self) -> bool: ...
    def CanSpawnYetis(self) -> bool: ...
    @staticmethod
    def CenterDialog(theDialog: Dialog, theWidth: int, theHeight: int) -> None: ...
    def ChangeDirHook(self, theIntendedPath: str) -> bool: ...
    def CheckForGameEnd(self) -> None: ...
    def CheckForUpdates(self) -> None: ...
    def CloseRequestAsync(self) -> None: ...
    def ConfirmCheckForUpdates(self) -> None: ...
    def ConfirmQuit(self) -> None: ...
    def CrazyDaveDie(self) -> None: ...
    def CrazyDaveDoneHanding(self) -> None: ...
    def CrazyDaveEnter(self) -> None: ...
    def CrazyDaveLeave(self) -> None: ...
    def CrazyDaveStopSound(self) -> None: ...
    def CrazyDaveStopTalking(self) -> None: ...
    def CrazyDaveTalkIndex(self, theMessageIndex: int) -> None: ...
    def CrazyDaveTalkMessage(self, theMessage: str) -> None: ...
    def DebugKeyDown(self, theKey: int) -> bool: ...
    def DelayLoadBackgroundResource(self, theGroupName: str) -> None: ...
    def DelayLoadComicThumbnailsResource(self, theGroupName: str) -> None: ...
    def DelayLoadGamePlayResources(self, doLoad: bool) -> None: ...
    def DelayLoadLeaderboardResource(self, doLoad: bool) -> None: ...
    def DelayLoadMainMenuResource(self, doLoad: bool) -> None: ...
    def DelayLoadPileResource(self, doLoad: bool) -> None: ...
    def DelayLoadStoreResource(self, theGroupName: str) -> None: ...
    def DelayLoadUpsellResource(self, theGroupName: str) -> None: ...
    def DelayLoadZenGardenBackground(self, theGroupName: str) -> None: ...
    def DelayLoadZenGardenResources(self, doLoad: bool) -> None: ...
    def DelayLoadZombieNotePaperResource(self, theGroupName: str) -> None: ...
    def DelayLoadZombieNoteResource(self, theGroupName: str) -> None: ...
    def Dispose(self) -> None: ...
    def DoAboutDialog(self) -> None: ...
    def DoAlmanacDialog(self, theSeedType: SeedType, theZombieType: ZombieType, theListener: AlmanacListener) -> AlmanacDialog: ...
    def DoCheatDialog(self) -> None: ...
    def DoConfirmBackToMain(self) -> None: ...
    def DoConfirmDeleteUserDialog(self, theName: str) -> None: ...
    def DoContinueDialog(self) -> None: ...
    def DoCreateUserDialog(self, isOnlyUser: bool) -> None: ...
    def DoDialog(self, theDialogId: int, isModal: bool, theDialogHeader: str, theDialogLines: str, theDialogFooter: str, theButtonMode: int) -> LawnDialog: ...
    def DoDialogDelay(self, theDialogId: int, isModal: bool, theDialogHeader: str, theDialogLines: str, theDialogFooter: str, theButtonMode: int) -> LawnDialog: ...
    def DoExportData(self) -> None: ...
    def DoLockedAchievementDialog(self, theId: AchievementId) -> None: ...
    def DoNeedRegisterDialog(self) -> None: ...
    def DoNewOptions(self, theFromGameSelector: bool) -> None: ...
    def DoPauseDialog(self) -> None: ...
    def DoRegister(self) -> None: ...
    def DoRegisterError(self) -> None: ...
    def DoRenameUserDialog(self, theName: str) -> None: ...
    def DoUpdateDialog(self) -> None: ...
    def DoUpdateFrames(self) -> bool: ...
    def DoUpsellScreen(self) -> None: ...
    def DoUserDialog(self) -> None: ...
    def DrawBlackFrame(self, g: Graphics) -> None: ...
    def DrawDebugInfo(self, gameTime: GameTime) -> None: ...
    def DrawGame(self, gameTime: GameTime) -> None: ...
    def EarnedGoldTrophy(self) -> bool: ...
    def EndLevel(self) -> None: ...
    def EnforceCursor(self) -> None: ...
    def FastLoad(self, theGameMode: GameMode) -> None: ...
    def FinishAboutDialog(self, isYes: bool) -> None: ...
    def FinishCheatDialog(self, isYes: bool) -> None: ...
    def FinishConfirmDeleteUserDialog(self, isYes: bool) -> None: ...
    def FinishCreateUserDialog(self, isYes: bool) -> None: ...
    def FinishInGameRestartConfirmDialog(self, isYes: bool) -> None: ...
    def FinishLawnDialogMessageBox(self, isYes: bool) -> None: ...
    def FinishModelessDialogs(self) -> None: ...
    def FinishNameError(self, theId: int) -> None: ...
    def FinishPacketSlotPurchaseDialog(self, isYes: bool) -> None: ...
    def FinishPlantSale(self, isYes: bool) -> None: ...
    def FinishRenameUserDialog(self, isYes: bool) -> None: ...
    def FinishRestartConfirmDialog(self) -> None: ...
    def FinishRestartWarningDialog(self, isYes: bool) -> None: ...
    def FinishTimesUpDialog(self) -> None: ...
    def FinishUserDialog(self, isYes: bool) -> None: ...
    def FinishZenGardenTutorial(self) -> None: ...
    def GetAchievementDescription(self, theAchievement: AchievementId) -> str: ...
    def GetAchievementIcon(self, theAchievement: AchievementId) -> int: ...
    def GetAchievementName(self, theAchievement: AchievementId) -> str: ...
    def GetAwardSeedForLevel(self, theLevel: int) -> SeedType: ...
    def GetCrazyDaveText(self, theMessageIndex: int) -> str: ...
    def GetCurrentChallengeIndex(self) -> int: ...
    @staticmethod
    def GetMoneyString(theAmount: int) -> str: ...
    def GetNumPreloadingTasks(self) -> int: ...
    def GetNumTrophies(self, thePage: ChallengePage) -> int: ...
    def GetPottedPlantByIndex(self, thePottedPlantIndex: int) -> PottedPlant: ...
    def GetSeedsAvailable(self) -> int: ...
    def GetStageString(self, theLevel: int) -> str: ...
    def GotFocus(self) -> None: ...
    def HandleCmdLineParam(self, theParamName: str, theParamValue: str) -> None: ...
    def HasBeatenChallenge(self, theGameMode: GameMode) -> bool: ...
    def HasFinishedAdventure(self) -> bool: ...
    def HasSeedType(self, theSeedType: SeedType) -> bool: ...
    def Init(self) -> None: ...
    def InitHook(self) -> None: ...
    def IsAdventureMode(self) -> bool: ...
    def IsArtChallenge(self) -> bool: ...
    def IsBungeeBlitzLevel(self) -> bool: ...
    def IsCattailSkinEnabled(self) -> bool: ...
    def IsChallengeMode(self) -> bool: ...
    def IsChallengeWithoutSeedBank(self) -> bool: ...
    def IsColumnLevel(self) -> bool: ...
    def IsContinuousChallenge(self) -> bool: ...
    def IsDRMConnected(self) -> bool: ...
    def IsEndlessIZombie(self, theGameMode: GameMode) -> bool: ...
    def IsEndlessScaryPotter(self, theGameMode: GameMode) -> bool: ...
    def IsFinalBossLevel(self) -> bool: ...
    def IsFirstTimeAdventureMode(self) -> bool: ...
    def IsIceDemo(self) -> bool: ...
    def IsIZombieLevel(self) -> bool: ...
    def IsLevelWithExtendedPoolZombies(self) -> bool: ...
    def IsLevelWithHighPresentPlantDropRate(self, theGameMode: GameMode) -> bool: ...
    def IsLittleTroubleLevel(self) -> bool: ...
    def IsMiniBossLevel(self) -> bool: ...
    def IsNight(self) -> bool: ...
    def IsPuzzleMode(self) -> bool: ...
    def IsQuickPlayMode(self) -> bool: ...
    def IsRegistered(self) -> bool: ...
    def IsRogueConveyorbeltLevel(self) -> bool: ...
    def IsScaryPotterLevel(self) -> bool: ...
    def IsShovelLevel(self) -> bool: ...
    def IsSlotMachineLevel(self) -> bool: ...
    def IsSquirrelLevel(self) -> bool: ...
    def IsStormyNightLevel(self) -> bool: ...
    def IsSurvivalEndless(self, theGameMode: GameMode) -> bool: ...
    def IsSurvivalHard(self, theGameMode: GameMode) -> bool: ...
    def IsSurvivalHell(self, theGameMode: GameMode) -> bool: ...
    def IsSurvivalMode(self) -> bool: ...
    def IsSurvivalNormal(self, theGameMode: GameMode) -> bool: ...
    def IsTrialStageLocked(self) -> bool: ...
    def IsWallnutBowlingLevel(self) -> bool: ...
    def IsWhackAZombieLevel(self) -> bool: ...
    def KillAlmanacDialog(self) -> bool: ...
    def KillAwardScreen(self) -> None: ...
    def KillBoard(self) -> None: ...
    def KillChallengeScreen(self) -> None: ...
    def KillCreditScreen(self) -> None: ...
    def KillDialog(self, theDialogId: int) -> bool: ...
    def KillGameSelector(self) -> None: ...
    def KillLeaderboardDialog(self) -> bool: ...
    def KillLeaderboardScreen(self) -> None: ...
    def KillNewOptionsDialog(self) -> bool: ...
    def KillSeedChooserScreen(self) -> None: ...
    def KillStoreScreen(self) -> None: ...
    def LawnMessageBox(self, theDialogId: int, theHeaderName: str, theLinesName: str, theButton1Name: str, theButton2Name: str, theButtonMode: int, theListener: LawnMessageBoxListener) -> None: ...
    def LeftTrialMode(self) -> None: ...
    def LevelCanEarnGoldSunFlower(self) -> bool: ...
    def LoadGroup(self, theGroupName: str, theGroupAveMsToLoad: int) -> None: ...
    def LoadingCompleted(self) -> None: ...
    def LoadingThreadAfterWorks(self) -> IEnumerable_1[bool]: ...
    def LoadingThreadCompleted(self) -> None: ...
    def LoadingThreadProc(self) -> None: ...
    def LostFocus(self) -> None: ...
    def MakeNewBoard(self) -> None: ...
    def ModalClose(self) -> None: ...
    def ModalOpen(self) -> None: ...
    def MoviePlayerContentPreloadDidFinish(self, succeeded: bool) -> None: ...
    def MoviePlayerPlaybackDidFinish(self) -> None: ...
    def NeedPauseGame(self) -> bool: ...
    def NeedRegister(self) -> bool: ...
    def NewDialog(self, theDialogId: int, isModal: bool, theDialogHeader: str, theDialogLines: str, theDialogFooter: str, theButtonMode: int) -> Dialog: ...
    @staticmethod
    def OpenUrl(url: str) -> None: ...
    def ParticleGet(self, theParticleID: TodParticleSystem) -> TodParticleSystem: ...
    def ParticleGetID(self, theParticle: TodParticleSystem) -> TodParticleSystem: ...
    def ParticleTryToGet(self, theParticleID: TodParticleSystem) -> TodParticleSystem: ...
    def PlayFoley(self, theFoleyType: FoleyType) -> None: ...
    def PlayFoleyPitch(self, theFoleyType: FoleyType, aPitch: float) -> None: ...
    def PlaySample(self, theSoundNum: int) -> None: ...
    def Pluralize(self, theCount: int, theSingular: str, thePlural: str) -> str: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PreDisplayHook(self) -> None: ...
    def PreloadForUser(self) -> None: ...
    def PreloadLoadingThreadReanimations(self) -> None: ...
    def PreloadReanimation(self, theReanimType: ReanimationType) -> None: ...
    def ReadRestoreInfo(self) -> None: ...
    def ReanimationGet(self, theReanimID: Reanimation) -> Reanimation: ...
    def ReanimationGetID(self, theReanimation: Reanimation) -> Reanimation: ...
    def ReanimationTryToGet(self, theReanimID: Reanimation) -> Reanimation: ...
    def RegistryReadString(self, key: str, value: str) -> str: ...
    def RemoveParticle(self, theParticleID: TodParticleSystem) -> None: ...
    def RemoveReanimation(self, theReanimationID: clr.Reference[Reanimation]) -> None: ...
    def RestartLoopingSounds(self) -> None: ...
    def RestoreGame(self) -> bool: ...
    def SaveFileExists(self) -> bool: ...
    def SetMusicVolume(self, theVolume: float) -> None: ...
    def SetSfxVolume(self, theVolume: float) -> None: ...
    def ShouldAutorotateToInterfaceOrientation(self, theOrientation: UI_ORIENTATION) -> bool: ...
    def ShouldInit500p(self) -> bool: ...
    def ShowAwardScreen(self, theAwardType: AwardType, theShowAchievements: bool) -> None: ...
    def ShowChallengeScreen(self, thePage: ChallengePage) -> None: ...
    def ShowCreditScreen(self) -> None: ...
    def ShowGameSelector(self) -> None: ...
    def ShowGameSelectorMoreGames(self) -> None: ...
    def ShowGameSelectorWithOptions(self) -> None: ...
    def ShowLeaderboardDialog(self, aType: LeaderBoardType) -> None: ...
    def ShowLeaderboardScreen(self) -> None: ...
    def ShowSeedChooserScreen(self) -> None: ...
    def ShowStoreScreen(self, theListener: StoreListener) -> StoreScreen: ...
    def ShowUpsellScreen(self) -> UpsellScreen: ...
    def Shutdown(self) -> None: ...
    def Start(self) -> None: ...
    def StartPlaying(self) -> None: ...
    def ToggleFastMo(self) -> None: ...
    def ToggleSlowMo(self) -> None: ...
    @staticmethod
    def ToString(i: int) -> str: ...
    def TraceLoadGroup(self, theGroupName: str, theGroupTime: int, theTotalGroupWeigth: int, theTaskWeight: int) -> None: ...
    def TrophiesNeedForGoldSunflower(self) -> int: ...
    def TryLoadGame(self) -> bool: ...
    def UpdateCrazyDave(self) -> None: ...
    def UpdateFrames(self) -> None: ...
    def UpdatePlayerProfileForFinishingLevel(self) -> bool: ...
    def UpdatePlayTimeStats(self) -> None: ...
    def UpdateRegisterInfo(self) -> None: ...
    def Vibrate(self, vibrationTime: typing.Optional[TimeSpan] = ...) -> None: ...
    def WriteCurrentUserConfig(self) -> bool: ...
    def WriteRestoreInfo(self) -> None: ...
    def WriteToRegistry(self) -> None: ...
    # Skipped AddReanimation due to it being static, abstract and generic.

    AddReanimation : AddReanimation_MethodGroup
    class AddReanimation_MethodGroup:
        @typing.overload
        def __call__(self, theX: float, theY: float, aRenderOrder: int, theReanimationType: ReanimationType) -> Reanimation:...
        @typing.overload
        def __call__(self, theX: float, theY: float, aRenderOrder: int, theReanimationType: ReanimationType, theDoScalePos: bool) -> Reanimation:...

    # Skipped DoBackToMain due to it being static, abstract and generic.

    DoBackToMain : DoBackToMain_MethodGroup
    class DoBackToMain_MethodGroup:
        @typing.overload
        def __call__(self) -> None:...
        @typing.overload
        def __call__(self, stopMusic: bool) -> None:...

    # Skipped DrawCrazyDave due to it being static, abstract and generic.

    DrawCrazyDave : DrawCrazyDave_MethodGroup
    class DrawCrazyDave_MethodGroup:
        @typing.overload
        def __call__(self, g: Graphics) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, theUseSmallFont: bool) -> None:...

    # Skipped PreNewGame due to it being static, abstract and generic.

    PreNewGame : PreNewGame_MethodGroup
    class PreNewGame_MethodGroup:
        @typing.overload
        def __call__(self, theGameMode: GameMode, theLookForSavedGame: bool) -> None:...
        @typing.overload
        def __call__(self, theGameMode: GameMode, theLookForSavedGame: bool, checkForTutorialCompletion: bool) -> None:...

    # Skipped ShowGameSelectorQuickPlay due to it being static, abstract and generic.

    ShowGameSelectorQuickPlay : ShowGameSelectorQuickPlay_MethodGroup
    class ShowGameSelectorQuickPlay_MethodGroup:
        @typing.overload
        def __call__(self, theDoFadeIn: bool) -> None:...
        @typing.overload
        def __call__(self, theDoFadeIn: bool, theButton: GameSelectorButtons) -> None:...

    # Skipped ShowResourceError due to it being static, abstract and generic.

    ShowResourceError : ShowResourceError_MethodGroup
    class ShowResourceError_MethodGroup:
        @typing.overload
        def __call__(self) -> None:...
        @typing.overload
        def __call__(self, doExit: bool) -> None:...



class LawnDialog(Dialog):
    def __init__(self, theApp: LawnApp, theButtonComponentImage: Image, theId: int, isModal: bool, theDialogHeader: str, theDialogLines: str, theDialogFooter: str, theButtonMode: int) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mBackgroundInsets : Insets
    mButtonDelay : int
    mButtonHeight : int
    mButtonHorzSpacing : int
    mButtonMode : int
    mButtonSidePadding : int
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mContentInsets : Insets
    mDialogFooter : str
    mDialogHeader : str
    mDialogLines : str
    mDialogListener : DialogListener
    mDisabled : bool
    mDoFinger : bool
    mDragging : bool
    mDragMouseX : int
    mDragMouseY : int
    mDrawStandardBack : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeaderFont : Font
    mHeight : int
    mId : int
    mIsDown : bool
    mIsModal : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLawnNoButton : LawnStoneButton
    mLawnYesButton : LawnStoneButton
    mLinesFont : Font
    mLineSpacingOffset : int
    mMinWidth : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNoButton : DialogButton
    mNumButtons : int
    mParent : WidgetContainer
    mPriority : int
    mReanimation : ReanimationWidget
    mResult : int
    mSpaceAfterHeader : int
    mTabNext : Widget
    mTabPrev : Widget
    mTallBottom : bool
    mTextAlign : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVerticalCenterText : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mYesButton : DialogButton
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonPress(self, theId: int) -> None: ...
    def CheckboxChecked(self, theId: int, cheked: bool) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def GetLeft(self) -> int: ...
    def GetTop(self) -> int: ...
    def GetWidth(self) -> int: ...
    def GetWordWrappedHeight(self, g: Graphics, theWidth: int, theLine: str, aLineSpacing: int) -> int: ...
    def KeyDown(self, theKey: KeyCode) -> None: ...
    def MouseDown(self, x: int, y: int, clickCount: int) -> None: ...
    def MouseDrag(self, x: int, y: int) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def SetButtonDelay(self, theDelay: int) -> None: ...
    def Update(self) -> None: ...
    def WriteWordWrapped(self, g: Graphics, theRect: TRect, theLine: str, theLineSpacing: int, theJustification: int) -> int: ...
    # Skipped CalcSize due to it being static, abstract and generic.

    CalcSize : CalcSize_MethodGroup
    class CalcSize_MethodGroup:
        @typing.overload
        def __call__(self, theExtraX: int, theExtraY: int) -> None:...
        @typing.overload
        def __call__(self, theExtraX: int, theExtraY: int, theMinWidth: int) -> None:...



class LawnDialogResult(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TryAgainMenu : LawnDialogResult # 1
    InAppNotificationNo : LawnDialogResult # 2


class LawnFPoint:
    def __init__(self, theX: float, theY: float) -> None: ...
    x : float
    y : float


class LawnGameConfig:
    def __init__(self) -> None: ...
    mCurrentUser : str
    mCustomConfigPath : str
    mFullscreen : typing.Optional[bool]
    mIronpythonEnabled : typing.Optional[bool]
    mIronpythonPort : typing.Optional[int]
    mLocale : typing.Optional[Constants.LanguageIndex]
    mScreenSize : typing.Optional[TPoint]
    mStoragePath : str
    def __add__(self, configOriginal: LawnGameConfig, configOverwrite: LawnGameConfig) -> LawnGameConfig: ...
    def __sub__(self, configOriginal: LawnGameConfig, configExclude: LawnGameConfig) -> LawnGameConfig: ...


class LawnMessageBoxListener(typing.Protocol):
    @abc.abstractmethod
    def LawnMessageBoxDone(self, theResult: int) -> None: ...


class LawnMower:
    mAltitude : float
    mAnimTicksPerFrame : int
    mApp : LawnApp
    mBoard : Board
    mChompCounter : int
    mDead : bool
    mLastPortalX : int
    mMowerHeight : MowerHeight
    mMowerState : LawnMowerState
    mMowerType : LawnMowerType
    mPosX : float
    mPosY : float
    mReanimID : Reanimation
    mReanimID_Save : int
    mRenderOrder : int
    mRollingInCounter : int
    mRow : int
    mSquishedCounter : int
    mVisible : bool
    def Die(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def EnableSuperMower(self, theEnable: bool) -> None: ...
    def GetLawnMowerAttackRect(self) -> TRect: ...
    @staticmethod
    def GetNewLawnMower() -> LawnMower: ...
    def LawnMowerInitialize(self, theRow: int) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def MowZombie(self, theZombie: Zombie) -> None: ...
    def PrepareForReuse(self) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def SquishMower(self) -> None: ...
    def StartMower(self) -> None: ...
    def Update(self) -> None: ...
    def UpdatePool(self) -> None: ...


class LawnMowerState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RollingIn : LawnMowerState # 0
    Ready : LawnMowerState # 1
    Triggered : LawnMowerState # 2
    Squished : LawnMowerState # 3


class LawnMowerType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Lawn : LawnMowerType # 0
    Pool : LawnMowerType # 1
    Roof : LawnMowerType # 2
    SuperMower : LawnMowerType # 3
    MowerTypesCount : LawnMowerType # 4


class LawnStoneButton(DialogButton):
    def __init__(self, theComponentImage: Image, theId: int, theListener: ButtonListener) -> None: ...
    FullRect : TRect
    mBtnNoDraw : bool
    mButtonImage : Image
    mButtonListener : ButtonListener
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mDisabled : bool
    mDisabledImage : Image
    mDisabledRect : TRect
    mDoFinger : bool
    mDownImage : Image
    mDownRect : TRect
    mFont : Font
    mFrameNoDraw : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mId : int
    mInverted : bool
    mIsDown : bool
    mIsOver : bool
    mLabelJustify : int
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNormalRect : TRect
    mOverAlpha : float
    mOverAlphaFadeInSpeed : float
    mOverAlphaSpeed : float
    mOverImage : Image
    mOverRect : TRect
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mTextOffsetX : int
    mTextOffsetY : int
    mTranslateWhenDown : bool
    mTranslateX : int
    mTranslateY : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    @property
    def mLabel(self) -> str: ...
    @mLabel.setter
    def mLabel(self, value: str) -> str: ...
    def Draw(self, g: Graphics) -> None: ...
    def SetLabel(self, theLabel: str) -> None: ...
    # Skipped Resize due to it being static, abstract and generic.

    Resize : Resize_MethodGroup
    class Resize_MethodGroup:
        @typing.overload
        def __call__(self, theRect: TRect) -> None:...
        @typing.overload
        def __call__(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None:...



class LeaderBoardButtonValues(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Back : LeaderBoardButtonValues # 0
    Pile : LeaderBoardButtonValues # 1
    LeavePile : LeaderBoardButtonValues # 2
    VaseBreaker : LeaderBoardButtonValues # 3
    Izombie : LeaderBoardButtonValues # 4
    Killed : LeaderBoardButtonValues # 5


class LeaderboardScreen(Widget):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDestX : int
    mDestY : int
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPileScrollWidget : ScrollWidget
    mPileStart : int
    mPriority : int
    mSlideCounter : int
    mStartX : int
    mStartY : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZombiePileWidget : ZombiePileWidget
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def SetGrayed(self, aGray: bool) -> None: ...
    def SlideTo(self, theX: int, theY: int) -> None: ...
    def UnloadResources(self) -> None: ...
    def Update(self) -> None: ...


class LeaderBoardType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Izombie : LeaderBoardType # 0
    Vasebreaker : LeaderBoardType # 1
    Killed : LeaderBoardType # 2


class LevelStats:
    def __init__(self) -> None: ...
    mUnusedLawnMowers : int
    def Reset(self) -> None: ...


class MagnetItem:
    def __init__(self) -> None: ...
    mDestOffsetX : float
    mDestOffsetY : float
    mItemType : MagnetItemType
    mPosX : float
    mPosY : float
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def Reset(self) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...


class MagnetItemType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : MagnetItemType # 0
    Pail1 : MagnetItemType # 1
    Pail2 : MagnetItemType # 2
    Pail3 : MagnetItemType # 3
    FootballHelmet1 : MagnetItemType # 4
    FootballHelmet2 : MagnetItemType # 5
    FootballHelmet3 : MagnetItemType # 6
    Door1 : MagnetItemType # 7
    Door2 : MagnetItemType # 8
    Door3 : MagnetItemType # 9
    Pogo1 : MagnetItemType # 10
    Pogo2 : MagnetItemType # 11
    Pogo3 : MagnetItemType # 12
    JackInTheBox : MagnetItemType # 13
    Ladder1 : MagnetItemType # 14
    Ladder2 : MagnetItemType # 15
    Ladder3 : MagnetItemType # 16
    LadderPlaced : MagnetItemType # 17
    SilverCoin : MagnetItemType # 18
    GoldCoin : MagnetItemType # 19
    Diamond : MagnetItemType # 20
    PickAxe : MagnetItemType # 21
    RobotTitanHead1 : MagnetItemType # 22
    RobotTitanHead2 : MagnetItemType # 23
    RedeyeRobotTitanHead1 : MagnetItemType # 24
    RedeyeRobotTitanHead2 : MagnetItemType # 25
    FootballPremiumHelmet1 : MagnetItemType # 26
    FootballPremiumHelmet2 : MagnetItemType # 27
    FootballPremiumHelmet3 : MagnetItemType # 28


class MainMenuButton(NewLawnButton):
    def __init__(self, theComponentImage: Image, theId: int, theListener: ButtonListener) -> None: ...
    FullRect : TRect
    mBtnNoDraw : bool
    mButtonImage : Image
    mButtonListener : ButtonListener
    mButtonOffsetX : int
    mButtonOffsetY : int
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mDisabled : bool
    mDisabledImage : Image
    mDisabledRect : TRect
    mDoFinger : bool
    mDownImage : Image
    mDownRect : TRect
    mFont : Font
    mFrameNoDraw : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mHiliteFont : Font
    mId : int
    mInverted : bool
    mIsDown : bool
    mIsOver : bool
    mLabelJustify : int
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNormalRect : TRect
    mOverAlpha : float
    mOverAlphaFadeInSpeed : float
    mOverAlphaSpeed : float
    mOverImage : Image
    mOverRect : TRect
    mParent : WidgetContainer
    mPolygonShape : Array_1[SexyVector2]
    mPriority : int
    mScaler : int
    mTabNext : Widget
    mTabPrev : Widget
    mTextDownOffsetX : int
    mTextDownOffsetY : int
    mTextOffsetX : int
    mTextOffsetY : int
    mTopImage : Image
    mTopImageOffsetX : int
    mTopImageOffsetY : int
    mTranslateWhenDown : bool
    mTranslateX : int
    mTranslateY : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mUsePolygonShape : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    SCALER_MAX_VALUE : int
    @property
    def mLabel(self) -> str: ...
    @mLabel.setter
    def mLabel(self, value: str) -> str: ...
    def Draw(self, g: Graphics) -> None: ...
    @staticmethod
    def MakeNewButton(theId: int, theListener: ButtonListener, theFont: Font, theImage: Image, theX: int = ..., theY: int = ...) -> MainMenuButton: ...
    def Update(self) -> None: ...


class MessageStyle(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Off : MessageStyle # 0
    TutorialLevel1 : MessageStyle # 1
    TutorialLevel1Stay : MessageStyle # 2
    TutorialLevel2 : MessageStyle # 3
    TutorialLater : MessageStyle # 4
    TutorialLaterStay : MessageStyle # 5
    HintLong : MessageStyle # 6
    HintFast : MessageStyle # 7
    HintStay : MessageStyle # 8
    HintTallFast : MessageStyle # 9
    HintTallUnlockmessage : MessageStyle # 10
    HintTallLong : MessageStyle # 11
    BigMiddle : MessageStyle # 12
    BigMiddleFast : MessageStyle # 13
    HouseName : MessageStyle # 14
    HugeWave : MessageStyle # 15
    SlotMachine : MessageStyle # 16
    ZenGardenLong : MessageStyle # 17
    Achievement : MessageStyle # 18


class MessageWidget:
    def __init__(self, theApp: LawnApp) -> None: ...
    mApp : LawnApp
    mDisplayTime : int
    mDuration : int
    mIcon : Image
    mLabel : str
    mLabelNext : Array_1[str]
    mLabelString : str
    mLabelStringList : List_1[str]
    mMessageStyle : MessageStyle
    mMessageStyleNext : MessageStyle
    mReanimType : ReanimationType
    mSlideOffTime : int
    mTextReanimID : Array_1[Reanimation]
    def ClearLabel(self) -> None: ...
    def ClearReanim(self) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawReanimatedText(self, g: Graphics, theFont: Font, theColor: SexyColor, thePosY: float) -> None: ...
    def GetFont(self) -> Font: ...
    def IsBeingDisplayed(self) -> bool: ...
    def LayoutReanimText(self) -> None: ...
    def Update(self) -> None: ...
    # Skipped SetLabel due to it being static, abstract and generic.

    SetLabel : SetLabel_MethodGroup
    class SetLabel_MethodGroup:
        @typing.overload
        def __call__(self, theNewLabel: str, theMessageStyle: MessageStyle) -> None:...
        @typing.overload
        def __call__(self, theNewLabel: str, theMessageStyle: MessageStyle, theIcon: Image) -> None:...



class MiniGameMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Games : MiniGameMode # 0
    IZombie : MiniGameMode # 1
    Vasebreaker : MiniGameMode # 2
    Survival : MiniGameMode # 10
    Limbo : MiniGameMode # 11
    Extra : MiniGameMode # 12


class MiniGamesWidget(Widget):
    def __init__(self, theApp: LawnApp, theListener: MiniGamesWidgetListener) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mListener : MiniGamesWidgetListener
    mMode : MiniGameMode
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def DisplayLockedMessage(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawBackgroundThumbnailForLevel(self, g: Graphics, theX: int, theY: int, theLevel: int) -> None: ...
    @staticmethod
    def GetChallengeImage(mode: GameMode) -> Image: ...
    def GetDrawPadlock(self) -> bool: ...
    def GetDrawWaves(self, index: int) -> bool: ...
    def GetGameMode(self, index: int) -> int: ...
    def GetGameModeExtraGames(self, index: int) -> int: ...
    def GetGameModeIZombie(self, index: int) -> int: ...
    def GetGameModeMiniGames(self, index: int) -> int: ...
    def GetGameModeVasebreaker(self, index: int) -> int: ...
    def GetImageForExtra(self, index: int) -> Image: ...
    def GetImageForGames(self, index: int) -> Image: ...
    def GetImageForIZombie(self, index: int) -> Image: ...
    def GetImageForLimbo(self, index: int) -> Image: ...
    def GetImageForMode(self, index: int) -> Image: ...
    def GetImageForSurvival(self, index: int) -> Image: ...
    def GetImageForVasebreaker(self, index: int) -> Image: ...
    def GetLevelName(self, index: int) -> str: ...
    def GetModeLevelCount(self) -> int: ...
    def HasBeenBeaten(self, index: int) -> bool: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def RecoverLastPlayedMode(self) -> None: ...
    def SizeToFit(self) -> None: ...
    def SwitchMode(self, mode: MiniGameMode) -> None: ...


class MiniGamesWidgetListener(typing.Protocol):
    @abc.abstractmethod
    def MiniGamesStageSelected(self, theLevel: int) -> None: ...


class MoreGamesListWidget(Widget):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mGames : List_1[MoreGamesListWidget.GameInfo]
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNextY : int
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AddRow(self, image: Image, theSrcRect: TRect, link: str) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def GetPreferredHeight(self) -> int: ...
    def MouseUp(self, theX: int, theY: int, theClickCount: int) -> None: ...

    class GameInfo:
        def __init__(self) -> None: ...
        mImage : Image
        mLink : str
        mSrcRect : TRect
        mY : int



class MotionTrailFrame:
    def __init__(self) -> None: ...
    mAnimTime : float
    mPosX : float
    mPosY : float
    def LoadFromFile(self, b: Buffer) -> None: ...
    def SaveToFile(self, b: Buffer) -> None: ...


class MowerHeight(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Land : MowerHeight # 0
    DownToPool : MowerHeight # 1
    InPool : MowerHeight # 2
    UpToLand : MowerHeight # 3


class Music:
    def __init__(self) -> None: ...
    mApp : LawnApp
    mCurMusicTune : MusicTune
    mMusicInterface : MusicInterface
    def FadeOut(self, aFadeOutDuration: int) -> None: ...
    def GameMusicPause(self, thePause: bool) -> None: ...
    def GetNumLoadingTasks(self) -> int: ...
    def MakeSureMusicIsPlaying(self, theMusicTune: MusicTune) -> None: ...
    def MusicInit(self) -> None: ...
    def MusicTitleScreenInit(self) -> None: ...
    def StartGameMusic(self) -> None: ...
    def StopAllMusic(self) -> None: ...


class MusicFile(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    MainMusic : MusicFile # 1
    Drums : MusicFile # 2
    Hihats : MusicFile # 3
    CreditsZombiesOnYourLawn : MusicFile # 4
    NumMusicFiles : MusicFile # 5
    None_ : MusicFile # -1


class MusicTune(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DayGrasswalk : MusicTune # 1
    NightMoongrains : MusicTune # 2
    PoolWaterygraves : MusicTune # 3
    FogRigormormist : MusicTune # 4
    RoofGrazetheroof : MusicTune # 5
    ChooseYourSeeds : MusicTune # 6
    TitleCrazyDaveMainTheme : MusicTune # 7
    PuzzleCerebrawl : MusicTune # 8
    MinigameLoonboon : MusicTune # 9
    Conveyer : MusicTune # 10
    FinalBossBrainiacManiac : MusicTune # 11
    ZenGarden : MusicTune # 12
    FinalBoss2 : MusicTune # 13
    MusicTuneCount : MusicTune # 14
    None_ : MusicTune # -1


class NewLawnButton(DialogButton):
    def __init__(self, theComponentImage: Image, theId: int, theListener: ButtonListener) -> None: ...
    FullRect : TRect
    mBtnNoDraw : bool
    mButtonImage : Image
    mButtonListener : ButtonListener
    mButtonOffsetX : int
    mButtonOffsetY : int
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mDisabled : bool
    mDisabledImage : Image
    mDisabledRect : TRect
    mDoFinger : bool
    mDownImage : Image
    mDownRect : TRect
    mFont : Font
    mFrameNoDraw : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mHiliteFont : Font
    mId : int
    mInverted : bool
    mIsDown : bool
    mIsOver : bool
    mLabelJustify : int
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNormalRect : TRect
    mOverAlpha : float
    mOverAlphaFadeInSpeed : float
    mOverAlphaSpeed : float
    mOverImage : Image
    mOverRect : TRect
    mParent : WidgetContainer
    mPolygonShape : Array_1[SexyVector2]
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mTextDownOffsetX : int
    mTextDownOffsetY : int
    mTextOffsetX : int
    mTextOffsetY : int
    mTranslateWhenDown : bool
    mTranslateX : int
    mTranslateY : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mUsePolygonShape : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    @property
    def mLabel(self) -> str: ...
    @mLabel.setter
    def mLabel(self, value: str) -> str: ...
    def Draw(self, g: Graphics) -> None: ...
    def IsPointVisible(self, x: int, y: int) -> bool: ...
    def SetLabel(self, theLabel: str) -> None: ...


class NewOptionsDialogs(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NewOptionsDialog_Almanac : NewOptionsDialogs # 0
    NewOptionsDialog_MainMenu : NewOptionsDialogs # 1
    NewOptionsDialog_Restart : NewOptionsDialogs # 2
    NewOptionsDialog_Update : NewOptionsDialogs # 3
    NewOptionsDialog_MusicVolume : NewOptionsDialogs # 4
    NewOptionsDialog_SoundVolume : NewOptionsDialogs # 5
    NewOptionDialog_Help : NewOptionsDialogs # 6
    NewOptionsDialog_About : NewOptionsDialogs # 7
    NewOptionsDialog_Vibrate : NewOptionsDialogs # 8
    NewOptionsDialog_HardwareAcceleration : NewOptionsDialogs # 9
    NewOptionsDialog_Credits : NewOptionsDialogs # 10
    NewOptionsDialog_RunWhileLocked : NewOptionsDialogs # 11


class NumImages(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NUM_IMAGES : NumImages # 249


class ParticleSystemID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : ParticleSystemID # 0


class Plant(GameObject):
    mAnimCounter : int
    mAnimPing : bool
    mApp : LawnApp
    mAttackingReanimID : Reanimation
    mAttackingReanimID_Save : int
    mBeghouledFlashCountdown : int
    mBlinkCountdown : int
    mBlinkReanimID : Reanimation
    mBlinkReanimID_Save : int
    mBoard : Board
    mBodyReanimID : Reanimation
    mBodyReanimID_Save : int
    mDead : bool
    mDisappearCountdown : int
    mDoSpecialCountdown : int
    mEatenFlashCountdown : int
    mFrame : int
    mFrameLength : int
    mGloveGrabbed : bool
    mGravebusterDrop : DropLootType
    mHeadReanimID : Reanimation
    mHeadReanimID_Save : int
    mHeadReanimID2 : Reanimation
    mHeadReanimID2_Save : int
    mHeadReanimID3 : Reanimation
    mHeadReanimID3_Save : int
    mHeight : int
    mHighlighted : bool
    mImitaterType : SeedType
    mInFlowerPot : bool
    mInTalismanCounter : int
    mIsAsleep : bool
    mIsOnBoard : bool
    mLaunchCounter : int
    mLaunchRate : int
    mLightReanimID : Reanimation
    mLightReanimID_Save : int
    mMagnetItems : Array_1[MagnetItem]
    mNumFrames : int
    mOnBungeeState : PlantOnBungeeState
    mParticleID : TodParticleSystem
    mParticleID_Save : int
    mPlantAttackRect : TRect
    mPlantCol : int
    mPlantHealth : int
    mPlantMaxHealth : int
    mPlantRect : TRect
    mPosScaled : bool
    mPottedPlantIndex : int
    mPrevTransX : float
    mPrevTransY : float
    mRecentlyEatenCountdown : int
    mRenderOrder : int
    mRow : int
    mSealedCountdown : int
    mSealedReanimID : Reanimation
    mSealedReanimID_Save : int
    mSeedType : SeedType
    mShakeOffsetX : float
    mShakeOffsetY : float
    mShootingCounter : int
    mSleepingReanimID : Reanimation
    mSleepingReanimID_Save : int
    mSquished : bool
    mStartRow : int
    mState : PlantState
    mStateCountdown : int
    mSubclass : int
    mTargetX : int
    mTargetY : int
    mTargetZombieID : Zombie
    mTargetZombieID_Save : int
    mVisible : bool
    mWakeUpCounter : int
    mWidth : int
    mX : int
    mY : int
    def AddAttachedParticle(self, thePosX: int, thePosY: int, theRenderPostition: int, theEffect: ParticleEffect) -> TodParticleSystem: ...
    def AgaveSkillCanCancel(self) -> bool: ...
    def Animate(self) -> None: ...
    def AnimateFireShroom(self) -> None: ...
    def AnimateGarlic(self) -> None: ...
    def AnimateHypnoShroom(self) -> None: ...
    def AnimateNuts(self) -> None: ...
    def AnimatePumpkin(self) -> None: ...
    def AnimateSleeping(self) -> None: ...
    def AttachBlinkAnim(self, theReanimBody: Reanimation) -> Reanimation: ...
    def BlowAwayFliers(self, theX: int, theRow: int) -> None: ...
    def BurnLine(self) -> None: ...
    def BurnRow(self, theRow: int) -> None: ...
    def CalcRenderOrder(self) -> int: ...
    def CanDoTouch(self, touchType: int) -> bool: ...
    @staticmethod
    def CanSwap(aType: SeedType) -> bool: ...
    def checkForPlantAchievements(self) -> None: ...
    def CobCannonFire(self, theTargetX: int, theTargetY: int) -> None: ...
    def Die(self) -> None: ...
    def DistanceToClosestZombie(self) -> int: ...
    @staticmethod
    def DoAdvancedSleeping(seedType: SeedType) -> bool: ...
    def DoAgaveDamage(self, theWeapon: PlantWeapon, theDamage: int, isAway: bool, isPowerfulSkill: bool = ...) -> None: ...
    def DoBlink(self) -> None: ...
    def DoDyingSpecial(self) -> None: ...
    def DoEndoflameDamage(self, theWeapon: PlantWeapon, theDamage: int, theAroundDamage: int, theDoBossDamage: bool = ...) -> None: ...
    def DoGatlingDamage(self, theWeapon: PlantWeapon, theDamage: int, theAwayAmount: int = ...) -> None: ...
    def DoRowAreaDamage(self, theDamage: int, theDamageFlags: int) -> None: ...
    def DoSpecial(self) -> None: ...
    def DoSquashDamage(self) -> None: ...
    def DoTouch(self, touchType: int) -> bool: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawMagnetItems(self, g: Graphics) -> None: ...
    def DrawMagnetItemsOnTop(self) -> bool: ...
    @staticmethod
    def DrawSeedType(g: Graphics, theSeedType: SeedType, theImitaterType: SeedType, theDrawVariation: DrawVariation, thePosX: float, thePosY: float) -> None: ...
    def DrawShadow(self, g: Graphics, theOffsetX: float, theOffsetY: float) -> None: ...
    def EndBlink(self) -> None: ...
    def FindGoldMagnetTarget(self) -> Coin: ...
    def FindSquashTarget(self) -> Zombie: ...
    def FindStarFruitTarget(self) -> bool: ...
    def FindTargetZombie(self, theRow: int, thePlantWeapon: PlantWeapon) -> Zombie: ...
    def Fire(self, theTargetZombie: Zombie, theRow: int, thePlantWeapon: PlantWeapon) -> None: ...
    @staticmethod
    def GetCost(theSeedType: SeedType, theImitaterType: SeedType) -> int: ...
    def GetDamageRangeFlags(self, thePlantWeapon: PlantWeapon) -> int: ...
    def GetFreeMagnetItem(self) -> MagnetItem: ...
    @staticmethod
    def GetImage(theSeedtype: SeedType) -> Image: ...
    @staticmethod
    def GetNameString(theSeedtype: SeedType, theImitaterType: SeedType) -> str: ...
    @staticmethod
    def GetNewPlant() -> Plant: ...
    def GetPeaHeadOffset(self, theOffsetX: clr.Reference[int], theOffsetY: clr.Reference[int]) -> None: ...
    def GetPlantAttackRect(self, thePlantWeapon: PlantWeapon) -> TRect: ...
    @staticmethod
    def GetPlantDefinition(theSeedtype: SeedType) -> PlantDefinition: ...
    def GetPlantRect(self) -> TRect: ...
    @staticmethod
    def GetRefreshTime(theSeedType: SeedType, theImitaterType: SeedType) -> int: ...
    def GetSleepingReanimOffset(self) -> Array_1[float]: ...
    def GetStateTrackIdSuffix(self) -> str: ...
    @staticmethod
    def GetToolTip(theSeedType: SeedType) -> str: ...
    @staticmethod
    def GetValidFusion(theBaseType: SeedType, theCoverType: SeedType) -> SeedType: ...
    def GoldMagnetFindTargets(self) -> None: ...
    def HasSleepingReanim(self) -> bool: ...
    def IceZombies(self) -> None: ...
    def ImitaterMorph(self) -> None: ...
    def IsAGoldMagnetAboutToSuck(self) -> bool: ...
    @staticmethod
    def IsAquatic(theSeedType: SeedType) -> bool: ...
    def IsDisabled(self) -> bool: ...
    @staticmethod
    def IsFlying(theSeedtype: SeedType) -> bool: ...
    def IsInPlay(self) -> bool: ...
    @staticmethod
    def IsNocturnal(theSeedtype: SeedType) -> bool: ...
    def IsOnBoard(self) -> bool: ...
    def IsOnHighGround(self) -> bool: ...
    def IsPartOfUpgradableTo(self, aUpdatedType: SeedType) -> bool: ...
    def IsSpiky(self) -> bool: ...
    def IsUpgradableTo(self, aUpdatedType: SeedType) -> bool: ...
    @staticmethod
    def IsUpgrade(theSeedtype: SeedType) -> bool: ...
    def KillAllPlantsNearDoom(self) -> None: ...
    def LaunchStarFruit(self) -> None: ...
    def LaunchThreepeater(self) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def MagnetShroomAttactItem(self, theZombie: Zombie) -> None: ...
    def MakesSun(self) -> bool: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def NotOnGround(self) -> bool: ...
    @staticmethod
    def PlantDrawHeightOffset(theBoard: Board, thePlant: Plant, theSeedType: SeedType, theCol: int, theRow: int) -> float: ...
    @staticmethod
    def PlantFlowerPotHeightOffset(theSeedType: SeedType, theFlowerPotScale: float) -> float: ...
    def PlantInitialize(self, theGridX: int, theGridY: int, theSeedType: SeedType, theImitaterType: SeedType) -> None: ...
    def PlayBodyReanim(self, theTrackName: str, theLoopType: ReanimLoopType, theBlendTime: int, theAnimRate: float) -> None: ...
    def PlayIdleAnim(self, theRate: float) -> None: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    @staticmethod
    def PreloadPlantResources(theSeedType: SeedType) -> None: ...
    def PrepareForReuse(self) -> None: ...
    def RemoveEffects(self) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def SetSealing(self, theIsSealed: bool) -> None: ...
    def SetSleeping(self, theIsAsleep: bool) -> None: ...
    def SpikeRockTakeDamage(self) -> None: ...
    def SpikeweedAttack(self) -> None: ...
    def Squish(self) -> None: ...
    def StarFruitFire(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateAbilities(self) -> None: ...
    def UpdateAgave(self) -> None: ...
    def UpdateBlink(self) -> None: ...
    def UpdateBlover(self) -> None: ...
    def UpdateBowling(self) -> None: ...
    def UpdateCactus(self) -> None: ...
    def UpdateChomper(self) -> None: ...
    def UpdateCobCannon(self) -> None: ...
    def UpdateCoffeeBean(self) -> None: ...
    def UpdateDoomShroom(self) -> None: ...
    def UpdateEndoflame(self) -> None: ...
    def UpdateFlowerPot(self) -> None: ...
    def UpdateGatlingpea(self) -> None: ...
    def UpdateGoldMagnetShroom(self) -> None: ...
    def UpdateGraveBuster(self) -> None: ...
    def UpdateIceShroom(self) -> None: ...
    def UpdateImitater(self) -> None: ...
    def UpdateLilypad(self) -> None: ...
    def UpdateMagnetShroom(self) -> None: ...
    def UpdateNeedsFood(self) -> None: ...
    def UpdatePotato(self) -> None: ...
    def UpdateProductionPlant(self) -> None: ...
    def UpdateReanim(self) -> None: ...
    def UpdateReanimColor(self) -> None: ...
    def UpdateScaredyShroom(self) -> None: ...
    def UpdateShooter(self) -> None: ...
    def UpdateShooting(self) -> None: ...
    def UpdateSpikeweed(self) -> None: ...
    def UpdateSquash(self) -> None: ...
    def UpdateSunShroom(self) -> None: ...
    def UpdateSuperChomper(self) -> None: ...
    def UpdateTanglekelp(self) -> None: ...
    def UpdateTorchwood(self) -> None: ...
    def UpdateUmbrella(self) -> None: ...
    # Skipped FindTargetAndFire due to it being static, abstract and generic.

    FindTargetAndFire : FindTargetAndFire_MethodGroup
    class FindTargetAndFire_MethodGroup:
        @typing.overload
        def __call__(self, theRow: int, thePlantWeapon: PlantWeapon) -> bool:...
        @typing.overload
        def __call__(self, theRow: int, thePlantWeapon: PlantWeapon, theLaunchTime: LaunchTime) -> bool:...



class PlantDefinition:
    def __init__(self, aSeedType: SeedType, aPlantImage: Array_1[Image], aReanimationType: ReanimationType, aPacketIndex: int, aSeedCost: int, aRefreshTime: int, aSubClass: PlantSubClass, aLaunchRate: int, aPlantName: str) -> None: ...
    mLaunchRate : int
    mPacketIndex : int
    mPlantImage : Array_1[Image]
    mPlantName : str
    mReanimationType : ReanimationType
    mRefreshTime : int
    mSeedCost : int
    mSeedType : SeedType
    mSubClass : PlantSubClass


class PlantGalleryWidget(Widget):
    def __init__(self, theDialog: AlmanacDialog) -> None: ...
    FullRect : TRect
    mClip : bool
    mColors : List_1[Color]
    mDialog : AlmanacDialog
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def GetSeedPosition(self, theSeedType: SeedType, x: clr.Reference[int], y: clr.Reference[int]) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def SeedHitTest(self, x: int, y: int) -> SeedType: ...


class PlantID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : PlantID # 0


class PlantingReason(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ok : PlantingReason # 0
    NotHere : PlantingReason # 1
    OnlyOnGraves : PlantingReason # 2
    OnlyInPool : PlantingReason # 3
    OnlyOnGround : PlantingReason # 4
    NeedsPot : PlantingReason # 5
    NotOnArt : PlantingReason # 6
    NotPassedLine : PlantingReason # 7
    NeedsUpgrade : PlantingReason # 8
    NotOnGrave : PlantingReason # 9
    NotOnCrater : PlantingReason # 10
    NotOnWater : PlantingReason # 11
    NeedsGround : PlantingReason # 12
    NeedsSleeping : PlantingReason # 13
    CelSealed : PlantingReason # 14
    JalapenoSealed : PlantingReason # 15


class PlantLayer(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Main : PlantLayer # 0
    Reanim : PlantLayer # 1
    ReanimHead : PlantLayer # 2
    ReanimBlink : PlantLayer # 3
    OnTop : PlantLayer # 4
    PlantLayerCount : PlantLayer # 5
    Below : PlantLayer # -1


class PlantOnBungeeState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NotOnBungee : PlantOnBungeeState # 0
    GettingGrabbedByBungee : PlantOnBungeeState # 1
    RisingWithBungee : PlantOnBungeeState # 2


class PlantOrder(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Lilypad : PlantOrder # 0
    Normal : PlantOrder # 1
    Pumpkin : PlantOrder # 2
    Flyer : PlantOrder # 3
    Cherrybomb : PlantOrder # 4


class PlantRowType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Dirt : PlantRowType # 0
    Normal : PlantRowType # 1
    Pool : PlantRowType # 2
    HighGround : PlantRowType # 3
    Shallow : PlantRowType # 4


class PlantsOnLawn:
    mFlyingPlant : Plant
    mNormalPlant : Plant
    mPumpkinPlant : Plant
    mUnderPlant : Plant


class PlantState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Notready : PlantState # 0
    Ready : PlantState # 1
    Doingspecial : PlantState # 2
    SquashLook : PlantState # 3
    SquashPreLaunch : PlantState # 4
    SquashRising : PlantState # 5
    SquashFalling : PlantState # 6
    SquashDoneFalling : PlantState # 7
    GravebusterLanding : PlantState # 8
    GravebusterEating : PlantState # 9
    ChomperBiting : PlantState # 10
    ChomperBitingGotOne : PlantState # 11
    ChomperBitingMissed : PlantState # 12
    ChomperDigesting : PlantState # 13
    ChomperSwallowing : PlantState # 14
    PotatoRising : PlantState # 15
    PotatoArmed : PlantState # 16
    PotatoMashed : PlantState # 17
    SpikeweedAttacking : PlantState # 18
    SpikeweedAttacking2 : PlantState # 19
    ScaredyshroomLowering : PlantState # 20
    ScaredyshroomScared : PlantState # 21
    ScaredyshroomRaising : PlantState # 22
    SunshroomSmall : PlantState # 23
    SunshroomGrowing : PlantState # 24
    SunshroomBig : PlantState # 25
    MagnetshroomSucking : PlantState # 26
    MagnetshroomCharging : PlantState # 27
    BowlingUp : PlantState # 28
    BowlingDown : PlantState # 29
    CactusLow : PlantState # 30
    CactusRising : PlantState # 31
    CactusHigh : PlantState # 32
    CactusLowering : PlantState # 33
    TanglekelpGrabbing : PlantState # 34
    CobcannonArming : PlantState # 35
    CobcannonLoading : PlantState # 36
    CobcannonReady : PlantState # 37
    CobcannonFiring : PlantState # 38
    KernelpultButter : PlantState # 39
    UmbrellaTriggered : PlantState # 40
    UmbrellaReflecting : PlantState # 41
    ImitaterMorphing : PlantState # 42
    ZenGardenWatered : PlantState # 43
    ZenGardenNeedy : PlantState # 44
    ZenGardenHappy : PlantState # 45
    MarigoldEnding : PlantState # 46
    FlowerpotInvulnerable : PlantState # 47
    LilypadInvulnerable : PlantState # 48
    JalapenoFwoosh : PlantState # 49
    AgaveEntering : PlantState # 50
    AgaveAttacking : PlantState # 51
    AgavePowerfulTendToLaunching : PlantState # 52
    AgavePowerfulPreparing : PlantState # 53
    AgavePowerfulWaitingForTarget : PlantState # 54
    AgavePowerfulTendToCanceling : PlantState # 55
    AgavePowerfulCanceling : PlantState # 56
    AgavePowerfulAttacking : PlantState # 57
    UmbrellaDeathTriggered : PlantState # 58
    UmbrellaDeathReflecting : PlantState # 59
    PumpkinDeploying : PlantState # 60
    ZenGardenInteracting : PlantState # 61
    ZenGardenBackFromInteracting : PlantState # 62
    FlowerpotEndoflameOverrideNoDraw : PlantState # 63
    Entering : PlantState # 64
    SpikeweedReadyForAttack2 : PlantState # 65
    SquashCaidanInReady : PlantState # 66
    AfterEntering : PlantState # 67
    Dying : PlantState # 68
    GatlingPreShooting1 : PlantState # 69
    GatlingPreShooting2 : PlantState # 70
    GatlingShooting1 : PlantState # 71
    GatlingShooting2 : PlantState # 72
    GatlingAfterShooting1 : PlantState # 73
    GatlingAfterShooting2 : PlantState # 74
    GatlingIdle1 : PlantState # 75


class PlantSubClass(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : PlantSubClass # 0
    Shooter : PlantSubClass # 1


class PlantVoice(abc.ABC):
    @staticmethod
    def Initialize() -> None: ...
    @staticmethod
    def Play(seedType: SeedType, imitatorType: SeedType, purpose: PlantVoice.VoiceType) -> None: ...
    @staticmethod
    def Prepare(seedType: SeedType, purpose: PlantVoice.VoiceType, isSpecial: bool = ...) -> typing.Optional[int]: ...

    class VoiceType(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Plant1 : PlantVoice.VoiceType # 0
        Plant2 : PlantVoice.VoiceType # 1
        Garden1 : PlantVoice.VoiceType # 2
        Garden2 : PlantVoice.VoiceType # 3
        Garden2_2 : PlantVoice.VoiceType # 4
        Sleep1 : PlantVoice.VoiceType # 5
        Sleep2 : PlantVoice.VoiceType # 6
        Power : PlantVoice.VoiceType # 7
        Attack : PlantVoice.VoiceType # 8
        SkillCancel : PlantVoice.VoiceType # 9
        Mending : PlantVoice.VoiceType # 10
        Die : PlantVoice.VoiceType # 11
        NumVoiceTypes : PlantVoice.VoiceType # 12
        Special_Title_En : PlantVoice.VoiceType # 13
        Special_Title_Cn : PlantVoice.VoiceType # 14
        Special_Title_Jp : PlantVoice.VoiceType # 15
        Special_Garlic_Mending : PlantVoice.VoiceType # 16
        Special_Ninja_Appear : PlantVoice.VoiceType # 17
        Special_Ninja_Die : PlantVoice.VoiceType # 18
        Special_Squash_Attack : PlantVoice.VoiceType # 19
        Special_Squash_Water : PlantVoice.VoiceType # 20
        Special_Squash_Caidan : PlantVoice.VoiceType # 21
        Special_Talisman_Wuguiyuncai : PlantVoice.VoiceType # 22
        Special_Talisman_Tianshuihengliu : PlantVoice.VoiceType # 23
        Special_Talisman_Fengyin : PlantVoice.VoiceType # 24
        Special_Zorrose_Attack1 : PlantVoice.VoiceType # 25
        Special_Zorrose_Attack2 : PlantVoice.VoiceType # 26
        Special_Zorrose_Enable : PlantVoice.VoiceType # 27
        Special_Zorrose_Disable : PlantVoice.VoiceType # 28
        Special_Gatlingpea_Attack1 : PlantVoice.VoiceType # 29
        Special_Gatlingpea_Attack2 : PlantVoice.VoiceType # 30
        NumSpecialTypes : PlantVoice.VoiceType # 31



class PlantWeapon(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Primary : PlantWeapon # 0
    Secondary : PlantWeapon # 1


class PlayerInfo:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, id: int) -> None: ...
    m500pMode : bool
    mCardGroup : Array_1[CardGroup]
    mChallengeRecords : Array_1[int]
    mCoins : int
    mDidntPurchasePacketUpgrade : int
    mDoVibration : bool
    mEarnedAchievements : Array_1[bool]
    mFinishedAdventure : int
    mHasFinishedTutorial : bool
    mHasNewIZombie : bool
    mHasNewMiniGame : bool
    mHasNewSurvival : bool
    mHasNewVasebreaker : bool
    mHasSeenAchievementDialog : bool
    mHasSeenStinky : bool
    mHasSeenUpsell : bool
    mHasUnlockedMinigames : bool
    mHasUnlockedPuzzleMode : bool
    mHasUnlockedSurvivalMode : bool
    mHasUsedCheatKeys : bool
    mHasWokenStinky : bool
    mId : int
    mIsDaveTalkingZenTutorial : bool
    mIsInZenTutorial : bool
    mIZombieScore : int
    mIZombieUnlocked : int
    mLastSeenMoreGames : DateTime
    mLastStinkyChocolateTime : DateTime
    mLevel : int
    mMiniGamesUnlockable : int
    mMiniGamesUnlocked : int
    mMoneySpent : int
    mMusicVolume : float
    mName : str
    mNeedsGrayedPlantWarning : bool
    mNeedsMagicBaconReward : bool
    mNeedsMagicTacoReward : bool
    mNeedsMessageOnGameSelector : bool
    mNeedsTrialLevelReset : bool
    mNumPottedPlants : int
    mPlaceHolderPlayerStats : Array_1[int]
    mPlantTypesUsed : Array_1[bool]
    mPlayTimeActivePlayer : int
    mPlayTimeInactivePlayer : int
    mPottedPlant : Array_1[PottedPlant]
    mPurchases : Array_1[int]
    mRunWhileLocked : bool
    mSaveStateAppVersionNumber : str
    mSeenLeaderboardArrow : bool
    mShownAchievements : Array_1[bool]
    mShowName : bool
    mSoundVolume : float
    mStinkyPosX : int
    mStinkyPosY : int
    mUseSeq : int
    mVasebreakerScore : int
    mVasebreakerUnlocked : int
    mZenGardenTutorialComplete : bool
    mZenTutorialMessage : int
    mZombiesKilled : int
    @property
    def FirstRun(self) -> bool: ...
    @FirstRun.setter
    def FirstRun(self, value: bool) -> bool: ...
    def AddCoins(self, theAmount: int) -> None: ...
    def DeleteUserFiles(self) -> None: ...
    def DeleteUserFilesAfterUnlock(self) -> None: ...
    def Dispose(self) -> None: ...
    def GamerSignedInCallback(self, sender: typing.Any, args: SignedInEventArgs) -> None: ...
    def GetLevel(self) -> int: ...
    def HandleAfterLoading(self, version: int) -> None: ...
    def LoadDetails(self) -> bool: ...
    def LoadDetailsOld(self) -> bool: ...
    def Reset(self) -> None: ...
    def ResetChallengeRecord(self, theGameMode: GameMode) -> None: ...
    def SaveDetails(self) -> None: ...
    def SetLevel(self, theLevel: int) -> None: ...
    def UnlockFirstMiniGames(self) -> None: ...
    def UnlockPuzzleMode(self) -> None: ...
    def UpdateAchievementInfo(self) -> None: ...


class PottedPlant:
    def __init__(self) -> None: ...
    mDrawVariation : DrawVariation
    mFacing : PottedPlant.FacingDirection
    mFeedingsPerGrow : int
    mFutureAttribute : Array_1[int]
    mLastChocolateTime : DateTime
    mLastFertilizedTime : DateTime
    mLastNeedFulfilledTime : DateTime
    mLastWateredTime : DateTime
    mPlantAge : PottedPlantAge
    mPlantNeed : PottedPlantNeed
    mSeedType : SeedType
    mTimesFed : int
    mWhichZenGarden : GardenType
    mX : int
    mY : int
    def InitializePottedPlant(self, theSeedType: SeedType) -> None: ...
    def Load(self, b: Buffer) -> None: ...
    def Save(self, b: Buffer) -> None: ...

    class FacingDirection(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Right : PottedPlant.FacingDirection # 0
        Left : PottedPlant.FacingDirection # 1



class PottedPlantAge(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Sprout : PottedPlantAge # 0
    Small : PottedPlantAge # 1
    Medium : PottedPlantAge # 2
    Full : PottedPlantAge # 3


class PottedPlantNeed(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : PottedPlantNeed # 0
    Water : PottedPlantNeed # 1
    Fertilizer : PottedPlantNeed # 2
    Bugspray : PottedPlantNeed # 3
    Phonograph : PottedPlantNeed # 4


class ProfileMgr:
    def __init__(self) -> None: ...
    mLastMoreGamesUpdate : DateTime
    def AddProfile(self, theName: str) -> PlayerInfo: ...
    def Clear(self) -> None: ...
    def DeleteProfile(self, theName: str) -> bool: ...
    def Dispose(self) -> None: ...
    def GetAnyProfile(self) -> PlayerInfo: ...
    @staticmethod
    def GetNewProfileId() -> int: ...
    def GetNumProfiles(self) -> int: ...
    def GetProfile(self, theName: str) -> PlayerInfo: ...
    def GetProfileMap(self) -> Dictionary_2[str, PlayerInfo]: ...
    def Load(self) -> None: ...
    def RenameProfile(self, theOldName: str, theNewName: str) -> bool: ...
    def Save(self) -> None: ...


class Projectile(GameObject):
    mAccZ : float
    mAnimCounter : int
    mAnimTicksPerFrame : int
    mApp : LawnApp
    mAttachmentID : Attachment
    mAttachmentID_Save : int
    mBoard : Board
    mClickBackoffCounter : int
    mCobTargetRow : int
    mCobTargetX : float
    mDamageRangeFlags : int
    mDead : bool
    mFrame : int
    mFromPlant : SeedType
    mHeight : int
    mHitTorchwoodGridX : int
    mLastPortalX : int
    mMotionType : ProjectileMotion
    mNumFrames : int
    mOnHighGround : bool
    mPosScaled : bool
    mPosX : float
    mPosY : float
    mPosZ : float
    mPrevTransX : float
    mPrevTransY : float
    mProjectileAge : int
    mProjectileReanimID : Reanimation
    mProjectileType : ProjectileType
    mRenderOrder : int
    mRotation : float
    mRotationSpeed : float
    mRow : int
    mShadowY : float
    mTargetZombieID : Zombie
    mTargetZombieID_Save : int
    mVelX : float
    mVelY : float
    mVelZ : float
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    def CantHitHighGround(self) -> bool: ...
    def CheckForCollision(self) -> None: ...
    def CheckForHighGround(self) -> None: ...
    def ConvertToEndoflameFireball(self, aGridX: int) -> None: ...
    def ConvertToPea(self, aGridX: int) -> None: ...
    def Die(self) -> None: ...
    def Dispose(self) -> None: ...
    def DoImpact(self, theZombie: Zombie) -> None: ...
    def DoSplashDamage(self, theZombie: Zombie) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawShadow(self, g: Graphics) -> None: ...
    def EndoflameRetarget(self) -> None: ...
    def FindCollisionTarget(self) -> Zombie: ...
    def FindCollisionTargetPlant(self) -> Plant: ...
    def GetDamageFlags(self, theZombie: Zombie) -> int: ...
    def GetProjectileDef(self) -> ProjectileDefinition: ...
    def GetProjectileRect(self) -> TRect: ...
    def IsSplashDamage(self, theZombie: Zombie) -> bool: ...
    def IsZombieHitBySplash(self, theZombie: Zombie) -> bool: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def PeaAboutToHitTorchwood(self) -> bool: ...
    def PlayImpactSound(self, theZombie: Zombie) -> None: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...
    def ProjectileInitialize(self, theX: int, theY: int, theRenderOrder: int, theRow: int, theProjectileType: ProjectileType) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def Update(self) -> None: ...
    def UpdateLobMotion(self) -> None: ...
    def UpdateMotion(self) -> None: ...
    def UpdateNormalMotion(self) -> None: ...
    # Skipped ConvertToFireball due to it being static, abstract and generic.

    ConvertToFireball : ConvertToFireball_MethodGroup
    class ConvertToFireball_MethodGroup:
        @typing.overload
        def __call__(self) -> None:...
        @typing.overload
        def __call__(self, aGridX: int) -> None:...



class ProjectileDefinition:
    def __init__(self, theType: ProjectileType, theRow: int, theDamage: int) -> None: ...
    mDamage : int
    mImageRow : int
    mProjectileType : ProjectileType


class ProjectileMotion(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Straight : ProjectileMotion # 0
    Lobbed : ProjectileMotion # 1
    Threepeater : ProjectileMotion # 2
    Bee : ProjectileMotion # 3
    BeeBackwards : ProjectileMotion # 4
    Puff : ProjectileMotion # 5
    Backwards : ProjectileMotion # 6
    Star : ProjectileMotion # 7
    FloatOver : ProjectileMotion # 8
    Homing : ProjectileMotion # 9
    EndoflameHoming : ProjectileMotion # 10
    YAwareStraight : ProjectileMotion # 11


class ProjectileType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Pea : ProjectileType # 0
    Snowpea : ProjectileType # 1
    Cabbage : ProjectileType # 2
    Melon : ProjectileType # 3
    Puff : ProjectileType # 4
    Wintermelon : ProjectileType # 5
    Fireball : ProjectileType # 6
    Star : ProjectileType # 7
    Spike : ProjectileType # 8
    Basketball : ProjectileType # 9
    Kernel : ProjectileType # 10
    Cobbig : ProjectileType # 11
    Butter : ProjectileType # 12
    ZombiePea : ProjectileType # 13
    ZombiePeaMindControl : ProjectileType # 14
    CattailSpike : ProjectileType # 15
    EndoflameSpike : ProjectileType # 16
    EndoflameFireball : ProjectileType # 17
    Talisman : ProjectileType # 18
    TalismanMove : ProjectileType # 19
    TalismanSeal : ProjectileType # 20
    HypnoCattailSpike : ProjectileType # 21
    ProjectilesCount : ProjectileType # 22


class QuickPlayWidget(Widget):
    def __init__(self, theApp: LawnApp, theListener: QuickPlayWidgetListener) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mListener : QuickPlayWidgetListener
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AddLevel(self, theLevel: int) -> None: ...
    def Clear(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawBackgroundThumbnailForLevel(self, g: Graphics, theX: int, theY: int, theLevel: int) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def SizeToFit(self) -> None: ...
    # Skipped DrawZombieThumbnail due to it being static, abstract and generic.

    DrawZombieThumbnail : DrawZombieThumbnail_MethodGroup
    class DrawZombieThumbnail_MethodGroup:
        @typing.overload
        def __call__(self, g: Graphics, theZombieType: ZombieType, theX: int, theY: int) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, theZombieType: ZombieType, theX: int, theY: int, mirror: bool) -> None:...



class QuickPlayWidgetListener(typing.Protocol):
    @abc.abstractmethod
    def QuickPlayStageSelected(self, theLevel: int) -> None: ...


class ReanimationID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : ReanimationID # 0


class ReanimationWidget(Widget):
    def __init__(self) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLawnDialog : LawnDialog
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPosX : float
    mPosY : float
    mPriority : int
    mReanim : Reanimation
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AddReanimation(self, x: float, y: float, theReanimationType: ReanimationType) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def Update(self) -> None: ...


class ReanimatorCache:
    def __init__(self) -> None: ...
    mApp : LawnApp
    mImageVariationList : Dictionary_2[ReanimatorCache.CachedPlantVariation, MemoryImage]
    mLawnMowers : List_1[MemoryImage]
    mPlantImages : List_1[MemoryImage]
    mZombieImages : List_1[MemoryImage]
    def DrawCachedMower(self, g: Graphics, thePosX: float, thePosY: float, mowerType: LawnMowerType) -> None: ...
    def DrawCachedPlant(self, g: Graphics, thePosX: float, thePosY: float, theSeedType: SeedType, theDrawVariation: DrawVariation) -> None: ...
    def DrawCachedZombie(self, g: Graphics, thePosX: float, thePosY: float, theZombieType: ZombieType) -> None: ...
    def DrawCachedZombieNew(self, g: Graphics, thePosX: float, thePosY: float, theZombieType: ZombieType) -> None: ...
    def DrawReanimatorFrame(self, g: Graphics, x: float, y: float, reanimType: ReanimationType, trackName: str, variation: DrawVariation) -> None: ...
    def GetPlantImageSize(self, seedtype: SeedType) -> TRect: ...
    def LoadCachedImages(self) -> None: ...
    def MakeBlankCanvasImage(self, width: int, height: int) -> MemoryImage: ...
    def MakeCachedMowerFrame(self, mowerType: LawnMowerType) -> MemoryImage: ...
    def MakeCachedPlantFrame(self, seedType: SeedType, drawVariation: DrawVariation) -> MemoryImage: ...
    def MakeCachedZombieFrame(self, zombieType: ZombieType) -> MemoryImage: ...
    def ReanimatorCacheDispose(self) -> None: ...
    def ReanimatorCacheInitialize(self) -> None: ...
    def SaveCachedImages(self) -> None: ...
    def UpdateReanimationforVariation(self, reanimation: Reanimation, variation: DrawVariation) -> None: ...

    class CachedPlantVariation:
        mDrawVariation : DrawVariation
        mSeedType : SeedType



class RenderItem(IComparable):
    id : int
    mBoardGridY : int
    mBossPart : BossPart
    mCoin : Coin
    mCursorPreview : CursorPreview
    mGameObject : GameObject
    mGridItem : GridItem
    mMower : LawnMower
    mParticleSytem : TodParticleSystem
    mPlant : Plant
    mProjectile : Projectile
    mReanimation : Reanimation
    mRenderObjectType : RenderObjectType
    mZombie : Zombie
    mZPos : int
    @staticmethod
    def CompareByZ(a: RenderItem, b: RenderItem) -> int: ...
    @staticmethod
    def GetNewRenderItem() -> RenderItem: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...


class RenderLayer(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RowOffset : RenderLayer # 10000
    UiBottom : RenderLayer # 100000
    Ground : RenderLayer # 200000
    Lawn : RenderLayer # 300000
    GraveStone : RenderLayer # 301000
    Plant : RenderLayer # 302000
    Zombie : RenderLayer # 303000
    Boss : RenderLayer # 304000
    Projectile : RenderLayer # 305000
    LawnMower : RenderLayer # 306000
    Particle : RenderLayer # 307000
    CoverLayer : RenderLayer # 308000
    Top : RenderLayer # 400000
    Fog : RenderLayer # 500000
    CoinBank : RenderLayer # 600000
    UiTop : RenderLayer # 700000
    AboveUI : RenderLayer # 800000
    ScreenFade : RenderLayer # 900000


class RenderObjectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Coin : RenderObjectType # 1
    Projectile : RenderObjectType # 2
    Zombie : RenderObjectType # 3
    ZombieShadow : RenderObjectType # 4
    ZombieBungeeTarget : RenderObjectType # 5
    Plant : RenderObjectType # 6
    PlantOverlay : RenderObjectType # 7
    PlantMagnetItems : RenderObjectType # 8
    CursorPreview : RenderObjectType # 9
    Particle : RenderObjectType # 10
    Reanimation : RenderObjectType # 11
    Ice : RenderObjectType # 12
    TopUi : RenderObjectType # 13
    Cover0 : RenderObjectType # 14
    Cover1 : RenderObjectType # 15
    Cover2 : RenderObjectType # 16
    Cover3 : RenderObjectType # 17
    Cover4 : RenderObjectType # 18
    Cover5 : RenderObjectType # 19
    Cover6 : RenderObjectType # 20
    Fog : RenderObjectType # 21
    Storm : RenderObjectType # 22
    BottomUi : RenderObjectType # 23
    Backdrop : RenderObjectType # 24
    DoorMask : RenderObjectType # 25
    CoinBank : RenderObjectType # 26
    ProjectileShadow : RenderObjectType # 27
    Mower : RenderObjectType # 28
    ScreenFade : RenderObjectType # 29
    BossPart : RenderObjectType # 30
    GridItem : RenderObjectType # 31
    GridItemOverlay : RenderObjectType # 32


class RestoreLocation(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Mainmenu : RestoreLocation # 0
    Board : RestoreLocation # 1
    Titlescreen : RestoreLocation # 2


class SaveFileVersion(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Initial : SaveFileVersion # 0
    Board_Widescreen : SaveFileVersion # 1
    CardGroup : SaveFileVersion # 1
    Agave : SaveFileVersion # 2
    RecordAppVersionNumber : SaveFileVersion # 2
    SpineAnimFirstStage : SaveFileVersion # 3
    Projectile_FromPlant : SaveFileVersion # 4
    Endoflame : SaveFileVersion # 5
    ImitaterRandom : SaveFileVersion # 6
    Board_GloveCounter : SaveFileVersion # 7
    VersionUnify : SaveFileVersion # 8
    SpineAnimTrackNames : SaveFileVersion # 9
    Talisman : SaveFileVersion # 10
    NewLayout600 : SaveFileVersion # 11
    Layout500pMode : SaveFileVersion # 12
    OptionShowName : SaveFileVersion # 13


class ScaryPotType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ScaryPotType # 0
    Seed : ScaryPotType # 1
    Zombie : ScaryPotType # 2
    Sun : ScaryPotType # 3


class SeedBank(GameObject):
    def __init__(self) -> None: ...
    mApp : LawnApp
    mBoard : Board
    mConveyorBeltCounter : int
    mCutSceneDarken : int
    mHeight : int
    mNumPackets : int
    mPosScaled : bool
    mPrevTransX : float
    mPrevTransY : float
    mRenderOrder : int
    mRow : int
    mSeedPackets : Array_1[SeedPacket]
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    def AddSeed(self, theSeedType: SeedType) -> None: ...
    def ContainsPoint(self, theX: int, theY: int) -> bool: ...
    def CountOfTypeOnConveyorBelt(self, aSeedType: SeedType) -> int: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawSun(self, g: Graphics) -> None: ...
    def GetNumSeedsOnConveyorBelt(self) -> int: ...
    def IsSeedPacketAccessible(self, theSeedPacket: SeedPacket) -> bool: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def MouseHitTest(self, x: int, y: int, theHitResult: clr.Reference[HitResult]) -> bool: ...
    def Move(self, x: int, y: int) -> None: ...
    def RefreshAllPackets(self) -> None: ...
    def RemoveSeed(self, theIndex: int) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def UpdateConveyorBelt(self) -> None: ...
    def UpdateHeight(self) -> None: ...


class SeedChooserScreen(Widget, SeedPacketsWidgetListener, LawnMessageBoxListener, AlmanacListener, StoreListener):
    def __init__(self) -> None: ...
    FullRect : TRect
    mAlmanacButton : GameButton
    mApp : LawnApp
    mBoard : Board
    mCardGroupButton : GameButton
    mCardGroupWidget : CardGroupWidget
    mChooseState : SeedChooserState
    mChosenSeeds : Array_1[ChosenSeed]
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mDoStartButton : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mImitaterButton : GameButton
    mInCardGroupScreen : bool
    mIsDown : bool
    mIsOver : bool
    mLastCardButton : GameButton
    mLastMouseX : int
    mLastMouseY : int
    mLastWMUpdateCount : int
    mLoadButton : GameButton
    mMenuButton : GameButton
    mMouseInsets : Insets
    mMouseVisible : bool
    mNumSeedsToChoose : int
    mParent : WidgetContainer
    mPendingWarningId : int
    mPickWarningsWaved : Array_1[bool]
    mPriority : int
    mRandomButton : GameButton
    mRoseButton : GameButton
    mSaveButton : GameButton
    mScrollWidget : ScrollWidget
    mScrollWidget2 : ScrollWidget
    mSeedChooserAge : int
    mSeedPacketsWidget : SeedPacketsWidget
    mSeedsInBank : int
    mSeedsInFlight : int
    mStartButton : GameButton
    mStoreButton : GameButton
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mViewLawnButton : GameButton
    mViewLawnTime : int
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def BackButtonPress(self) -> bool: ...
    def BackFromAlmanac(self) -> None: ...
    def BackFromStore(self) -> None: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonPress(self, theId: int) -> None: ...
    def CancelLawnView(self) -> None: ...
    def CheckSeedUpgrade(self, theWarningId: int, theSeedTypeTo: SeedType, theSeedTypeFrom: SeedType) -> bool: ...
    def CleanSeed(self, immediate: bool) -> None: ...
    def ClickedSeedInBank(self, theChosenSeed: clr.Reference[ChosenSeed]) -> None: ...
    def ClickedSeedInChooser(self, theChosenSeed: clr.Reference[ChosenSeed]) -> None: ...
    def CloseSeedChooser(self) -> None: ...
    def CrazyDavePickSeeds(self) -> None: ...
    def DisplayRepickWarningDialog(self, theWarningId: int, theMessage: str) -> bool: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def EnableStartButton(self, theEnabled: bool) -> None: ...
    def FindSeedInBank(self, theIndexInBank: int) -> SeedType: ...
    def FlyersAreComing(self) -> bool: ...
    def FlyProtectionCurrentlyPlanted(self) -> bool: ...
    def GetSeedPositionInBank(self, theIndex: int, x: clr.Reference[int], y: clr.Reference[int]) -> None: ...
    def GetSeedPositionInChooser(self, theIndex: int, x: clr.Reference[int], y: clr.Reference[int]) -> None: ...
    def Has12Rows(self) -> bool: ...
    def KeyChar(self, theChar: SexyChar) -> None: ...
    def KeyDown(self, theKey: KeyCode) -> None: ...
    def LandFlyingSeed(self, theChosenSeed: clr.Reference[ChosenSeed]) -> None: ...
    def LawnMessageBoxDone(self, theResult: int) -> None: ...
    def LoadSeedGroup(self, seedGroup: CardGroup, theIndex: int = ...) -> bool: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def OnStartButton(self) -> None: ...
    def PickedPlantType(self, theSeedType: SeedType) -> bool: ...
    def PickFromWeightedArrayUsingSpecialRandSeed(self, theArray: Array_1[TodWeightedArray], theCount: int) -> int: ...
    def PickRandomSeeds(self) -> None: ...
    def PreChooseSeed(self, seedType: SeedType, locked: bool) -> None: ...
    def SaveToSeedGroup(self, seedGroup: CardGroup) -> bool: ...
    def SeedNotAllowedDuringTrial(self, theSeedType: SeedType) -> bool: ...
    def SeedNotAllowedToPick(self, theSeedType: SeedType) -> bool: ...
    def SeedNotRecommendedToPick(self, theSeedType: SeedType) -> int: ...
    def SeedSelected(self, theSeedType: SeedType) -> None: ...
    def SetInCardGroupScreen(self, isIn: bool) -> None: ...
    def Update(self) -> None: ...
    def UpdateAfterPurchase(self) -> None: ...
    def UpdateImitaterButton(self) -> None: ...
    def UpdateViewLawn(self) -> None: ...


class SeedChooserScreens(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SeedChooserScreen_Start : SeedChooserScreens # 100
    SeedChooserScreen_Random : SeedChooserScreens # 101
    SeedChooserScreen_ViewLawn : SeedChooserScreens # 102
    SeedChooserScreen_Almanac : SeedChooserScreens # 103
    SeedChooserScreen_Menu : SeedChooserScreens # 104
    SeedChooserScreen_Store : SeedChooserScreens # 105
    SeedChooserScreen_Imitater : SeedChooserScreens # 106


class SeedChooserState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : SeedChooserState # 0
    ViewLawn : SeedChooserState # 1


class SeedPacket(GameObject):
    def __init__(self) -> None: ...
    gDynamicTachieSeedPacketSpineWidgets : Array_1[SpineWidget]
    mActive : bool
    mApp : LawnApp
    mBoard : Board
    mBuzzedCounter : int
    mHeight : int
    mImitaterType : SeedType
    mIndex : int
    mOffsetY : int
    mPacketType : SeedType
    mPosScaled : bool
    mPrevTransX : float
    mPrevTransY : float
    mRefreshCounter : int
    mRefreshing : bool
    mRefreshTime : int
    mRenderOrder : int
    mRow : int
    mSlotMachineCountDown : int
    mSlotMachiningNextSeed : SeedType
    mSlotMachiningPosition : float
    mTimesUsed : int
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    def Activate(self) -> None: ...
    def CanPickUp(self) -> bool: ...
    def CenterY(self) -> int: ...
    def Deactivate(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawBackground(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    @staticmethod
    def DrawSmallSeedPacket(g: Graphics, x: float, y: float, theSeedType: SeedType, theImitaterType: SeedType, thePercentDark: float, theGrayness: int, theDrawCost: bool, theUseCurrentCost: bool, theDrawBackground: bool, theDrawCostBackground: bool, canShowName: bool = ...) -> None: ...
    def FlashIfReady(self) -> None: ...
    def GetGraynessAndDarkness(self, theGrayness: clr.Reference[int], thePercentDark: clr.Reference[float]) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def MouseHitTest(self, theX: int, theY: int, theHitResult: HitResult) -> bool: ...
    def PickNextSlotMachineSeed(self) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def SetPacketType(self, theSeedType: SeedType, theImitaterType: SeedType) -> None: ...
    def SlotMachineStart(self) -> None: ...
    def ToString(self) -> str: ...
    def Update(self) -> None: ...
    def WasPlanted(self) -> None: ...


class SeedPacketsWidget(Widget):
    def __init__(self, theApp: LawnApp, theNumberOfRows: int, theIsImitaters: bool, theListener: SeedPacketsWidgetListener) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mImitaters : bool
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mListener : SeedPacketsWidgetListener
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mRows : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    SEEDPACKETS_MARGIN_UP : int
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawPackets(self, g: Graphics, theDrawCost: bool, theDrawBackground: bool) -> None: ...
    def GetSeedPosition(self, theSeedType: SeedType, theX: clr.Reference[int], theY: clr.Reference[int]) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...


class SeedPacketsWidgetListener(typing.Protocol):
    @abc.abstractmethod
    def SeedSelected(self, UnnamedParameter1: SeedType) -> None: ...


class SeedType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Peashooter : SeedType # 0
    Sunflower : SeedType # 1
    Cherrybomb : SeedType # 2
    Wallnut : SeedType # 3
    Potatomine : SeedType # 4
    Snowpea : SeedType # 5
    Chomper : SeedType # 6
    Repeater : SeedType # 7
    Puffshroom : SeedType # 8
    Sunshroom : SeedType # 9
    Fumeshroom : SeedType # 10
    Gravebuster : SeedType # 11
    Hypnoshroom : SeedType # 12
    Scaredyshroom : SeedType # 13
    Iceshroom : SeedType # 14
    Doomshroom : SeedType # 15
    Lilypad : SeedType # 16
    Squash : SeedType # 17
    Threepeater : SeedType # 18
    Tanglekelp : SeedType # 19
    Jalapeno : SeedType # 20
    Spikeweed : SeedType # 21
    Torchwood : SeedType # 22
    Tallnut : SeedType # 23
    Seashroom : SeedType # 24
    Plantern : SeedType # 25
    Cactus : SeedType # 26
    Blover : SeedType # 27
    Splitpea : SeedType # 28
    Starfruit : SeedType # 29
    Pumpkinshell : SeedType # 30
    Magnetshroom : SeedType # 31
    Cabbagepult : SeedType # 32
    Flowerpot : SeedType # 33
    Kernelpult : SeedType # 34
    InstantCoffee : SeedType # 35
    Garlic : SeedType # 36
    Umbrella : SeedType # 37
    Marigold : SeedType # 38
    Melonpult : SeedType # 39
    Gatlingpea : SeedType # 40
    Twinsunflower : SeedType # 41
    Gloomshroom : SeedType # 42
    Cattail : SeedType # 43
    Wintermelon : SeedType # 44
    GoldMagnet : SeedType # 45
    Spikerock : SeedType # 46
    Cobcannon : SeedType # 47
    SuperChomper : SeedType # 48
    PickledPepper : SeedType # 49
    FireShroom : SeedType # 50
    Agave : SeedType # 51
    Endoflame : SeedType # 52
    Imitater : SeedType # 53
    ExplodeONut : SeedType # 54
    SeedsInChooserCount : SeedType # 54
    GiantWallnut : SeedType # 55
    Sprout : SeedType # 56
    Leftpeater : SeedType # 57
    ImitaterRandomPlant : SeedType # 58
    ImitaterRandomZombie : SeedType # 59
    HypnoCattail : SeedType # 60
    SunflowerPea : SeedType # 61
    PeaWallnut : SeedType # 62
    SunflowerWallnut : SeedType # 63
    IceWallnut : SeedType # 64
    SeedTypeCount : SeedType # 65
    BeghouledButtonShuffle : SeedType # 66
    BeghouledButtonCrater : SeedType # 67
    SlotMachineSun : SeedType # 68
    SlotMachineDiamond : SeedType # 69
    ZombiquariumSnorkel : SeedType # 70
    ZombiquariumTrophy : SeedType # 71
    ZombieNormal : SeedType # 72
    ZombieTrafficCone : SeedType # 73
    ZombiePolevaulter : SeedType # 74
    ZombiePail : SeedType # 75
    ZombieLadder : SeedType # 76
    ZombieDigger : SeedType # 77
    ZombieBungee : SeedType # 78
    ZombieFootball : SeedType # 79
    ZombieBalloon : SeedType # 80
    ZombieScreenDoor : SeedType # 81
    Zomboni : SeedType # 82
    ZombiePogo : SeedType # 83
    ZombieDancer : SeedType # 84
    ZombieGargantuar : SeedType # 85
    ZombieImp : SeedType # 86
    None_ : SeedType # -1


class SeedTypeLegacy(abc.ABC):
    @staticmethod
    def FromInt(i: int) -> SeedType: ...


class SelectorSignState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Down : SelectorSignState # 0
    Up : SelectorSignState # 1
    MovingUp : SelectorSignState # 2
    MovingDown : SelectorSignState # 3


class ShieldType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : ShieldType # 0
    Door : ShieldType # 1
    Newspaper : ShieldType # 2
    Ladder : ShieldType # 3


class SpecialGridPlacement:
    def __init__(self, aPixelX: int, aPixelY: int, aGridX: int, aGridY: int) -> None: ...
    mGridX : int
    mGridY : int
    mPixelX : int
    mPixelY : int


class SpineWidget(Widget):
    def __init__(self, atlasPath: str, jsonPath: str, scale: float, skeletonFormat: SpineWidget.SkeletonFormat = ...) -> None: ...
    FullRect : TRect
    mAppCounterLast : int
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def SetAnimationTrack(self, track: str, loopType: ReanimLoopType) -> None: ...
    def SetSkeletonPos(self, x: float, y: float) -> None: ...
    def Update(self) -> None: ...
    def Update_FromDraw(self, appCounter: int) -> None: ...

    class SkeletonFormat(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Json : SpineWidget.SkeletonFormat # 0
        Skel : SpineWidget.SkeletonFormat # 1



class StackPanel(Widget):
    def __init__(self, isVertical: bool) -> None: ...
    FullRect : TRect
    mAlignment : LayoutFlags
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mIsVertical : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mSupressRefresh : bool
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def AddWidget(self, theWidget: Widget) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def MouseUp(self, x: int, y: int, theBtnNum: int, theClickCount: int) -> None: ...
    def RefreshSize(self) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def RemoveWidget(self, theWidget: Widget) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...


class StoreItem(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    STORE_ITEM_PLANT_GATLINGPEA : StoreItem # 0
    STORE_ITEM_PLANT_TWINSUNFLOWER : StoreItem # 1
    STORE_ITEM_PLANT_GLOOMSHROOM : StoreItem # 2
    STORE_ITEM_PLANT_CATTAIL : StoreItem # 3
    STORE_ITEM_PLANT_WINTERMELON : StoreItem # 4
    STORE_ITEM_PLANT_GOLD_MAGNET : StoreItem # 5
    STORE_ITEM_PLANT_SPIKEROCK : StoreItem # 6
    STORE_ITEM_PLANT_COBCANNON : StoreItem # 7
    STORE_ITEM_PLANT_IMITATER : StoreItem # 8
    STORE_ITEM_BONUS_LAWN_MOWER : StoreItem # 9
    STORE_ITEM_POTTED_MARIGOLD_1 : StoreItem # 10
    STORE_ITEM_POTTED_MARIGOLD_2 : StoreItem # 11
    STORE_ITEM_POTTED_MARIGOLD_3 : StoreItem # 12
    STORE_ITEM_GOLD_WATERINGCAN : StoreItem # 13
    STORE_ITEM_FERTILIZER : StoreItem # 14
    STORE_ITEM_BUG_SPRAY : StoreItem # 15
    STORE_ITEM_PHONOGRAPH : StoreItem # 16
    STORE_ITEM_GARDENING_GLOVE : StoreItem # 17
    STORE_ITEM_MUSHROOM_GARDEN : StoreItem # 18
    STORE_ITEM_WHEEL_BARROW : StoreItem # 19
    STORE_ITEM_STINKY_THE_SNAIL : StoreItem # 20
    STORE_ITEM_PACKET_UPGRADE : StoreItem # 21
    STORE_ITEM_POOL_CLEANER : StoreItem # 22
    STORE_ITEM_ROOF_CLEANER : StoreItem # 23
    STORE_ITEM_RAKE : StoreItem # 24
    STORE_ITEM_AQUARIUM_GARDEN : StoreItem # 25
    STORE_ITEM_CHOCOLATE : StoreItem # 26
    STORE_ITEM_TREE_OF_WISDOM : StoreItem # 27
    STORE_ITEM_TREE_FOOD : StoreItem # 28
    STORE_ITEM_FIRSTAID : StoreItem # 29
    STORE_ITEM_GARLICFIRSTAID : StoreItem # 30
    STORE_ITEM_PLANT_SUPER_CHOMPER : StoreItem # 31
    STORE_ITEM_PLANT_PICKLED_PEPPER : StoreItem # 32
    STORE_ITEM_PLANT_FIRE_SHROOM : StoreItem # 33
    STORE_ITEM_PLANT_AGAVE : StoreItem # 34
    STORE_ITEM_AGAVE_SKILL : StoreItem # 35
    STORE_ITEM_CARD_GROUP_UPGRADE : StoreItem # 36
    STORE_ITEM_GREENHOUSE_NIGHT : StoreItem # 37
    STORE_ITEM_CATTAIL_DRIVER_HYPNO : StoreItem # 38
    STORE_ITEM_CATTAIL_DRIVER : StoreItem # 39
    STORE_ITEM_INVALID : StoreItem # -1


class StoreListener(typing.Protocol):
    @abc.abstractmethod
    def BackFromStore(self) -> None: ...


class StorePage(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SlotUpgrades : StorePage # 0
    PlantUpgrades : StorePage # 1
    Zen1 : StorePage # 2
    Zen2 : StorePage # 3
    ExtraSlot : StorePage # 4
    NumStorePages : StorePage # 5


class StoreScreen(Dialog):
    def __init__(self, theApp: LawnApp, theListener: StoreListener) -> None: ...
    FullRect : TRect
    mAmbientSpeechCountDown : int
    mApp : LawnApp
    mBackButton : NewLawnButton
    mBackgroundInsets : Insets
    mBubbleAutoAdvance : bool
    mBubbleClickToContinue : bool
    mBubbleCountDown : int
    mBubbleText : str
    mButtonHeight : int
    mButtonHorzSpacing : int
    mButtonMode : int
    mButtonSidePadding : int
    mClip : bool
    mCoins : DataArray_1[Coin]
    mColors : List_1[Color]
    mComponentImage : Image
    mContentInsets : Insets
    mDialogFooter : str
    mDialogHeader : str
    mDialogLines : str
    mDialogListener : DialogListener
    mDisabled : bool
    mDoFinger : bool
    mDragging : bool
    mDragMouseX : int
    mDragMouseY : int
    mDrawnOnce : bool
    mEasyBuyingCheat : bool
    mGoToTreeNow : bool
    mHalfDeltaHeight : int
    mHalfDeltaWidth : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHatchOpen : bool
    mHatchTimer : int
    mHeaderFont : Font
    mHeight : int
    mId : int
    mIsDown : bool
    mIsModal : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLinesFont : Font
    mLineSpacingOffset : int
    mListener : StoreListener
    mMouseInsets : Insets
    mMouseOverItem : StoreItem
    mMouseVisible : bool
    mNextButton : NewLawnButton
    mNoButton : DialogButton
    mNumButtons : int
    mOverlayWidget : Widget
    mPage : StorePage
    mParent : WidgetContainer
    mPendingPurchaseItem : StoreItem
    mPottedPlantSpecs : PottedPlant
    mPrevButton : NewLawnButton
    mPreviousAmbientSpeechIndex : int
    mPriority : int
    mPurchasedFullVersion : bool
    mResult : int
    mShakeX : int
    mShakeY : int
    mSpaceAfterHeader : int
    mStartDialog : int
    mStoreTime : int
    mTabNext : Widget
    mTabPrev : Widget
    mTextAlign : int
    mTrialLockedWhenStoreOpened : bool
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mYesButton : DialogButton
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def AdvanceCrazyDaveDialog(self) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonPress(self, theId: int) -> None: ...
    def CanAffordItem(self, theStoreItem: StoreItem) -> bool: ...
    def CanInteractWithButtons(self) -> bool: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawItem(self, g: Graphics, theItemPosition: int, theItemType: StoreItem) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def EnableButtons(self, theEnable: bool) -> None: ...
    def FinishTreeOfWisdomDialog(self, isYes: bool) -> None: ...
    @staticmethod
    def GetItemCost(theStoreItem: StoreItem) -> int: ...
    def GetStoreItemType(self, theSpotIndex: int) -> StoreItem: ...
    def GetStorePosition(self, theSpotIndex: int, thePosX: clr.Reference[int], thePosY: clr.Reference[int]) -> None: ...
    def IsComingSoon(self, theStoreItem: StoreItem) -> bool: ...
    def IsFullVersionOnly(self, theStoreItem: StoreItem) -> bool: ...
    def IsItemSoldOut(self, theStoreItem: StoreItem) -> bool: ...
    def IsItemUnavailable(self, theStoreItem: StoreItem) -> bool: ...
    def IsPageShown(self, thePage: StorePage) -> bool: ...
    @staticmethod
    def IsPottedPlant(theStoreItem: StoreItem) -> bool: ...
    def IsWaitingForDialog(self) -> bool: ...
    def KeyChar(self, theChar: str) -> None: ...
    def KeyDown(self, theKey: KeyCode) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def PurchaseItem(self, theItemType: StoreItem) -> None: ...
    def PurchasePendingItem(self) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def SetBubbleText(self, theCrazyDaveMessage: int, theTime: int, theClickToContinue: bool) -> None: ...
    def SetupBackButtonForZenGarden(self) -> None: ...
    def SetupForIntro(self, theDialogIndex: int) -> None: ...
    def StorePreLoad(self) -> None: ...
    def Update(self) -> None: ...
    def UpdateMouse(self) -> None: ...
    def UpdateScreen(self) -> None: ...
    def UpdateUIPosition(self) -> None: ...


class StoreScreens(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    StoreScreen_Back : StoreScreens # 100
    StoreScreen_Prev : StoreScreens # 101
    StoreScreen_Next : StoreScreens # 102


class SyncGameException_GenericClasses(abc.ABCMeta):
    Generic_SyncGameException_GenericClasses_SyncGameException_1_T = typing.TypeVar('Generic_SyncGameException_GenericClasses_SyncGameException_1_T')
    def __getitem__(self, types : typing.Type[Generic_SyncGameException_GenericClasses_SyncGameException_1_T]) -> typing.Type[SyncGameException_1[Generic_SyncGameException_GenericClasses_SyncGameException_1_T]]: ...

SyncGameException : SyncGameException_GenericClasses

SyncGameException_1_T = typing.TypeVar('SyncGameException_1_T')
class SyncGameException_1(typing.Generic[SyncGameException_1_T], Exception):
    def __init__(self, data: BufferNew, innerException: Exception = ...) -> None: ...
    buffer : BufferNew
    @property
    def Data(self) -> IDictionary: ...
    @property
    def HelpLink(self) -> str: ...
    @HelpLink.setter
    def HelpLink(self, value: str) -> str: ...
    @property
    def HResult(self) -> int: ...
    @HResult.setter
    def HResult(self, value: int) -> int: ...
    @property
    def InnerException(self) -> Exception: ...
    @property
    def Message(self) -> str: ...
    @property
    def Source(self) -> str: ...
    @Source.setter
    def Source(self, value: str) -> str: ...
    @property
    def StackTrace(self) -> str: ...
    @property
    def TargetSite(self) -> MethodBase: ...


class TachieWidget(Widget):
    @typing.overload
    def __init__(self, images: Array_1[Image]) -> None: ...
    @typing.overload
    def __init__(self, mImage: Image) -> None: ...
    FullRect : TRect
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mImages : Array_1[Image]
    mIsDown : bool
    mIsDragging : bool
    mIsOver : bool
    mIsSlidingOut : bool
    mLastWMUpdateCount : int
    mMouseDownPos : TPoint
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPrevScale : float
    mPrevTransX : float
    mPriority : int
    mScale : float
    mSlideInCounter : int
    mSlideOutCounter : int
    mTabNext : Widget
    mTabPrev : Widget
    mTransX : float
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    @property
    def Image(self) -> Image: ...
    @property
    def Page(self) -> int: ...
    @Page.setter
    def Page(self, value: int) -> int: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def MouseDown(self, x: int, y: int, theBtnNum: int, theClickCount: int) -> None: ...
    def MouseDrag(self, x: int, y: int) -> None: ...
    def MouseUp(self, x: int, y: int, theBtnNum: int, theClickCount: int) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def SwitchPage(self, newIndex: int) -> None: ...
    def Update(self) -> None: ...


class TitleScreen(Widget, ButtonListener):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    LEFT_LENGTH : int
    mApp : LawnApp
    mBarStartProgress : float
    mBarVel : float
    mClip : bool
    mColors : List_1[Color]
    mCurBarWidth : float
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLoaderScreenIsLoaded : bool
    mLoadingThreadComplete : bool
    mMouseInsets : Insets
    mMouseVisible : bool
    mNeedRegister : bool
    mNeedShowRegisterBox : bool
    mNeedToInit : bool
    mNeedToUnpackAtlas : bool
    mNextImageIndex : int
    mParent : WidgetContainer
    mPrevLoadingPercent : float
    mPriority : int
    mQuickLoadKey : KeyCode
    mRegisterClicked : bool
    mStartButton : HyperlinkWidget
    mTabNext : Widget
    mTabPrev : Widget
    mTitleAge : int
    mTitleState : TitleState
    mTitleStateCounter : int
    mTitleStateDuration : int
    mTitleVoicePlayed : bool
    mTotalBarWidth : float
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def BackButtonPress(self) -> bool: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, theId: int) -> None: ...
    def ButtonMouseEnter(self, theId: int) -> None: ...
    def ButtonMouseLeave(self, theId: int) -> None: ...
    def ButtonMouseMove(self, theId: int, theX: int, theY: int) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawToPreload(self, g: Graphics) -> None: ...
    def KeyDown(self, theKey: KeyCode) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def PreflightNextImage(self, g: Graphics) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def Resize(self, theX: int, theY: int, theWidth: int, theHeight: int) -> None: ...
    def SetRegistered(self) -> None: ...
    def Update(self) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, theId: int, theClickCount: int) -> None:...



class TitleScreens(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    TitleScreen_Start : TitleScreens # 0
    TitleScreen_Register : TitleScreens # 1


class TitleState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    WaitingForFirstDraw : TitleState # 0
    PopcapLogo : TitleState # 1
    PartnerLogo : TitleState # 2
    Screen : TitleState # 3


class ToggleButton(NewLawnButton):
    def __init__(self, theComponentImage: Image, theId: int, theListener: ButtonListener) -> None: ...
    FullRect : TRect
    mBtnNoDraw : bool
    mButtonImage : Image
    mButtonListener : ButtonListener
    mButtonOffsetX : int
    mButtonOffsetY : int
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mDisabled : bool
    mDisabledImage : Image
    mDisabledRect : TRect
    mDoFinger : bool
    mDownImage : Image
    mDownRect : TRect
    mFont : Font
    mFrameNoDraw : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mHiliteFont : Font
    mId : int
    mInverted : bool
    mIsDown : bool
    mIsOver : bool
    mIsToggled : bool
    mLabelJustify : int
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNormalRect : TRect
    mNoToggledImage : Image
    mOverAlpha : float
    mOverAlphaFadeInSpeed : float
    mOverAlphaSpeed : float
    mOverImage : Image
    mOverRect : TRect
    mParent : WidgetContainer
    mPolygonShape : Array_1[SexyVector2]
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mTextDownOffsetX : int
    mTextDownOffsetY : int
    mTextOffsetX : int
    mTextOffsetY : int
    mToggledImage : Image
    mTranslateWhenDown : bool
    mTranslateX : int
    mTranslateY : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mUsePolygonShape : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    @property
    def mLabel(self) -> str: ...
    @mLabel.setter
    def mLabel(self, value: str) -> str: ...
    @staticmethod
    def MakeNewButton(theId: int, theListener: ButtonListener, theImage: Image, theToggledImage: Image) -> ToggleButton: ...
    def SetToggled(self, toggled: bool) -> None: ...


class TopPlant(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    EatingOrder : TopPlant # 0
    DiggingOrder : TopPlant # 1
    BungeeOrder : TopPlant # 2
    CatapultOrder : TopPlant # 3
    ZenToolOrder : TopPlant # 4
    Any : TopPlant # 5
    OnlyNormalPosition : TopPlant # 6
    OnlyFlying : TopPlant # 7
    OnlyPumpkin : TopPlant # 8
    OnlyUnderPlant : TopPlant # 9


class TrialType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : TrialType # 0
    Stagelocked : TrialType # 1


class TutorialState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Off : TutorialState # 0
    Level1PickUpPeashooter : TutorialState # 1
    Level1PlantPeashooter : TutorialState # 2
    Level1RefreshPeashooter : TutorialState # 3
    Level1Completed : TutorialState # 4
    Level2PickUpSunflower : TutorialState # 5
    Level2PlantSunflower : TutorialState # 6
    Level2RefreshSunflower : TutorialState # 7
    Level2Completed : TutorialState # 8
    MoresunPickUpSunflower : TutorialState # 9
    MoresunPlantSunflower : TutorialState # 10
    MoresunRefreshSunflower : TutorialState # 11
    MoresunCompleted : TutorialState # 12
    SlotMachinePull : TutorialState # 13
    SlotMachineCompleted : TutorialState # 14
    ShovelPickup : TutorialState # 15
    ShovelDig : TutorialState # 16
    ShovelKeepDigging : TutorialState # 17
    ShovelCompleted : TutorialState # 18
    ZombiquariumBuySnorkel : TutorialState # 19
    ZombiquariumBoughtSnorkel : TutorialState # 20
    ZombiquariumClickTrophy : TutorialState # 21
    ZenGardenPickupWater : TutorialState # 22
    ZenGardenWaterPlant : TutorialState # 23
    ZenGardenKeepWatering : TutorialState # 24
    ZenGardenVisitStore : TutorialState # 25
    ZenGardenFertilizePlants : TutorialState # 26
    ZenGardenCompleted : TutorialState # 27
    WhackAZombieBeforePickSeed : TutorialState # 28
    WhackAZombiePickSeed : TutorialState # 29
    WhackAZombieCompleted : TutorialState # 30


class TypingCheck:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, thePhrase: str) -> None: ...
    def AddChar(self, theChar: str) -> None: ...
    def AddKeyCode(self, theCode: KeyCode) -> None: ...
    def SetPhrase(self, thePhrase: str) -> None: ...
    # Skipped Check due to it being static, abstract and generic.

    Check : Check_MethodGroup
    class Check_MethodGroup:
        @typing.overload
        def __call__(self, theChar: int) -> bool:...
        @typing.overload
        def __call__(self, theCode: KeyCode) -> bool:...



class UnlockingState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Off : UnlockingState # 0
    Shaking : UnlockingState # 1
    Fading : UnlockingState # 2


class UpdateChoices(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : UpdateChoices # 0
    Yes : UpdateChoices # 1
    No : UpdateChoices # 2
    Later : UpdateChoices # 3


class UpdateDialog(LawnDialog):
    def __init__(self, theApp: LawnApp, richTextContent: str, font: Font) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mBackgroundInsets : Insets
    mButtonDelay : int
    mButtonHeight : int
    mButtonHorzSpacing : int
    mButtonMode : int
    mButtonSidePadding : int
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mContentInsets : Insets
    mDialogFooter : str
    mDialogHeader : str
    mDialogLines : str
    mDialogListener : DialogListener
    mDisabled : bool
    mDoFinger : bool
    mDragging : bool
    mDragMouseX : int
    mDragMouseY : int
    mDrawStandardBack : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeaderFont : Font
    mHeight : int
    mId : int
    mIsDown : bool
    mIsModal : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLawnNoButton : LawnStoneButton
    mLawnYesButton : LawnStoneButton
    mLinesFont : Font
    mLineSpacingOffset : int
    mMinWidth : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNoButton : DialogButton
    mNumButtons : int
    mParent : WidgetContainer
    mPriority : int
    mReanimation : ReanimationWidget
    mResult : int
    mSpaceAfterHeader : int
    mTabNext : Widget
    mTabPrev : Widget
    mTallBottom : bool
    mTextAlign : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVerticalCenterText : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mYesButton : DialogButton
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def WriteWordWrapped(self, g: Graphics, theRect: TRect, theLine: str, theLineSpacing: int, theJustification: int) -> int: ...


class UpsellScreen(Dialog):
    def __init__(self, theApp: LawnApp) -> None: ...
    FullRect : TRect
    mApp : LawnApp
    mBackButton : NewLawnButton
    mBackgroundInsets : Insets
    mButtonHeight : int
    mButtonHorzSpacing : int
    mButtonMode : int
    mButtonSidePadding : int
    mBuyButton : NewLawnButton
    mClip : bool
    mColors : List_1[Color]
    mComponentImage : Image
    mContentInsets : Insets
    mDialogFooter : str
    mDialogHeader : str
    mDialogLines : str
    mDialogListener : DialogListener
    mDisabled : bool
    mDoFinger : bool
    mDragging : bool
    mDragMouseX : int
    mDragMouseY : int
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeaderFont : Font
    mHeight : int
    mId : int
    mIsDown : bool
    mIsModal : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mLinesFont : Font
    mLineSpacingOffset : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mNoButton : DialogButton
    mNumButtons : int
    mParent : WidgetContainer
    mPriority : int
    mResult : int
    mSpaceAfterHeader : int
    mTabNext : Widget
    mTabPrev : Widget
    mTextAlign : int
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mYesButton : DialogButton
    mZOrder : int
    def AddedToManager(self, theWidgetManager: WidgetManager) -> None: ...
    def AdvanceCrazyDaveDialog(self) -> None: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonPress(self, theId: int) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def MouseDown(self, x: int, y: int, theClickCount: int) -> None: ...
    def RemovedFromManager(self, theWidgetManager: WidgetManager) -> None: ...
    def SetBubbleText(self, theCrazyDaveMessage: int) -> None: ...
    def Update(self) -> None: ...


class UserDialogs(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    UserDialog_RenameUser : UserDialogs # 0
    UserDialog_DeleteUser : UserDialogs # 1


class Wind:
    def __init__(self, windType: WindType) -> None: ...
    mAge : int
    mCurrentWind : Vector2
    mDead : bool
    mDisappearCountdown : int
    mType : WindType
    def PrepareForReuse(self) -> None: ...
    def Update(self) -> None: ...


class WindType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Blover : WindType # 0
    NumWindTypes : WindType # 1


class ZenGarden(ButtonListener, StoreListener):
    def __init__(self) -> None: ...
    gAquariumGridPlacement : Array_1[SpecialGridPlacement]
    gGreenhouseGridPlacement : Array_1[SpecialGridPlacement]
    mApp : LawnApp
    mBoard : Board
    mFeedButton : NewLawnButton
    mGardenType : GardenType
    mHeartBarButton : NewLawnButton
    mInteracting : Plant
    mIsInteracting : bool
    mIsInteractingInTouch : bool
    mIsTutorial : bool
    mPlantForSale : Plant
    mPlantNameLabel : BoxedLabel
    mPlantVoiceLabel : BoxedLabel
    mTouch1Button : NewLawnButton
    mTouch2Button : NewLawnButton
    STINKY_BASE_TIME : int
    def AddHappyEffect(self, thePlant: Plant) -> None: ...
    def AddPottedPlant(self, thePottedPlant: PottedPlant) -> None: ...
    def AddStinky(self) -> None: ...
    def AdvanceCrazyDaveDialog(self) -> None: ...
    def AllPlantsHaveBeenFertilized(self) -> bool: ...
    def BackFromStore(self) -> None: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, theId: int) -> None: ...
    def ButtonMouseEnter(self, theId: int) -> None: ...
    def ButtonMouseLeave(self, theId: int) -> None: ...
    def ButtonMouseMove(self, theId: int, theX: int, theY: int) -> None: ...
    def CanDropChocolate(self) -> bool: ...
    def CanDropPottedPlantLoot(self) -> bool: ...
    def CountPlantsNeedingFertilizer(self) -> int: ...
    def Dispose(self) -> None: ...
    def DoFeedingTool(self, x: int, y: int, theToolType: GridItemState) -> None: ...
    def DoPlantSale(self, wasSold: bool) -> None: ...
    def DrawBackdrop(self, g: Graphics) -> None: ...
    def DrawPlantOverlay(self, g: Graphics, thePlant: Plant) -> None: ...
    def DrawPottedPlant(self, g: Graphics, x: float, y: float, thePottedPlant: PottedPlant, theScale: float, theDrawPot: bool) -> None: ...
    def DrawPottedPlantIcon(self, g: Graphics, x: float, y: float, thePottedPlant: PottedPlant) -> None: ...
    def EnterPlantInteraction(self, thePlant: Plant) -> None: ...
    def FeedChocolateToPlant(self, thePlant: Plant) -> None: ...
    def FindOpenZenGardenSpot(self, theSpotX: clr.Reference[int], theSpotY: clr.Reference[int], theGardenType: GardenType) -> bool: ...
    @staticmethod
    def GetNextGarden(theApp: LawnApp, theCurrent: clr.Reference[GardenType], theBackground: clr.Reference[BackgroundType], theTree: clr.Reference[bool], theNext: int) -> None: ...
    def GetPlantSellPrice(self, thePlant: Plant) -> int: ...
    def GetPlantsNeed(self, thePottedPlant: PottedPlant) -> PottedPlantNeed: ...
    def GetPottedPlantInWheelbarrow(self) -> PottedPlant: ...
    def GetPottedPlantXOffset(self, theType: SeedType, isFlipped: bool) -> float: ...
    def GetPottedPlantYOffset(self, theType: SeedType, isFlipped: bool) -> float: ...
    def GetSpecialGridPlacements(self, theCount: clr.Reference[int]) -> Array_1[SpecialGridPlacement]: ...
    def GetStinky(self) -> GridItem: ...
    def GotoNextGarden(self) -> None: ...
    def GotoPrevGarden(self, isTreeOfWisdom: bool = ...) -> None: ...
    def GridToPixelX(self, theGridX: int, theGridY: int) -> int: ...
    def GridToPixelY(self, theGridX: int, theGridY: int) -> int: ...
    def HasPurchasedStinky(self) -> bool: ...
    def IsStinkyHighOnChocolate(self) -> bool: ...
    def IsStinkySleeping(self) -> bool: ...
    def IsZenGardenFull(self, theIncludeDroppedPresents: bool) -> bool: ...
    def JumptoNextGarden(self, theTree: bool, theNext: int) -> None: ...
    def LeaveGarden(self) -> None: ...
    def LeavePlantInteraction(self, thePlant: Plant) -> None: ...
    def MakeStinkySleeping(self) -> None: ...
    def MouseDownWithEmptyWheelBarrow(self, thePlant: Plant) -> None: ...
    def MouseDownWithFeedingTool(self, x: int, y: int, theCursorType: CursorType, isTouch: bool = ...) -> None: ...
    def MouseDownWithFullWheelBarrow(self, x: int, y: int) -> None: ...
    def MouseDownWithMoneySign(self, thePlant: Plant) -> None: ...
    def MouseDownWithTool(self, x: int, y: int, theCursorType: CursorType, isTouch: bool) -> None: ...
    def MouseDownZenGarden(self, x: int, y: int, theClickCount: int, theHitResult: HitResult) -> bool: ...
    def MovePlant(self, thePlant: Plant, theGridX: int, theGridY: int) -> None: ...
    def OpenStore(self) -> None: ...
    def PickRandomSeedType(self) -> SeedType: ...
    def PickRandomSeedTypeWithNewPlants(self) -> SeedType: ...
    def PixelToGridX(self, theX: int, theY: int) -> int: ...
    def PixelToGridY(self, theX: int, theY: int) -> int: ...
    def PlacePottedPlant(self, thePottedPlantIndex: int) -> Plant: ...
    def PlantCanBeWatered(self, thePlant: Plant) -> bool: ...
    def PlantCanHaveChocolate(self, thePlant: Plant) -> bool: ...
    def PlantFertilized(self, thePlant: Plant) -> None: ...
    def PlantFulfillNeed(self, thePlant: Plant) -> None: ...
    def PlantGetMinutesSinceHappy(self, thePlant: Plant) -> int: ...
    def PlantHighOnChocolate(self, thePottedPlant: PottedPlant) -> bool: ...
    def PlantSetLaunchCounter(self, thePlant: Plant) -> None: ...
    def PlantShouldRefreshNeed(self, thePottedPlant: PottedPlant) -> bool: ...
    def PlantsNeedWater(self) -> bool: ...
    def PlantUpdateProduction(self, thePlant: Plant) -> None: ...
    def PlantWatered(self, thePlant: Plant) -> None: ...
    def PottedPlantFromIndex(self, thePottedPlantIndex: int) -> PottedPlant: ...
    def PottedPlantUpdate(self, thePlant: Plant) -> None: ...
    @staticmethod
    def RefreshMushroomGridPlacements() -> None: ...
    def RefreshPlantNeeds(self, thePottedPlant: PottedPlant) -> None: ...
    def ReloadPlant(self, thePlant: Plant) -> None: ...
    def RemoveHappyEffect(self, thePlant: Plant) -> None: ...
    def RemovePottedPlant(self, thePlant: Plant) -> None: ...
    def ResetPlantTimers(self, thePottedPlant: PottedPlant) -> None: ...
    def ResetStinkyTimers(self) -> None: ...
    def SetPlantAnimSpeed(self, thePlant: Plant) -> None: ...
    def SetupForZenTutorial(self) -> None: ...
    def ShouldStinkyBeAwake(self) -> bool: ...
    def ShowInteractingButtons(self, doShow: bool) -> None: ...
    def ShowTutorialArrowOnWateringCan(self) -> None: ...
    def StinkyAnimRateUpdate(self, theStinky: GridItem) -> None: ...
    def StinkyFinishFallingAsleep(self, theStinky: GridItem, theBlendTime: int) -> None: ...
    def StinkyPickGoal(self, theStinky: GridItem) -> None: ...
    def StinkyStartFallingAsleep(self, theStinky: GridItem) -> None: ...
    def StinkyUpdate(self, theStinky: GridItem) -> None: ...
    def StinkyWakeUp(self, theStinky: GridItem) -> None: ...
    def UnloadBackdrop(self) -> None: ...
    def UpdatePlantEffectState(self, thePlant: Plant) -> None: ...
    def UpdatePlantNeeds(self) -> None: ...
    def UpdateStinkyMotionTrail(self, theStinky: GridItem, theStinkyHighOnChocolate: bool) -> None: ...
    def WakeStinky(self) -> None: ...
    def WasPlantFertilizedInLastHour(self, thePottedPlant: PottedPlant) -> bool: ...
    def WasPlantNeedFulfilledToday(self, thePottedPlant: PottedPlant) -> bool: ...
    def ZenGardenInitLevel(self, theJustSwitchingGardens: bool) -> None: ...
    def ZenGardenStart(self) -> None: ...
    def ZenGardenUpdate(self) -> None: ...
    def ZenPlantOffsetX(self, thePottedPlant: PottedPlant) -> float: ...
    def ZenToolUpdate(self, theZenTool: GridItem) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, theId: int, theClickCount: int) -> None:...

    # Skipped PlantPottedDrawHeightOffset due to it being static, abstract and generic.

    PlantPottedDrawHeightOffset : PlantPottedDrawHeightOffset_MethodGroup
    class PlantPottedDrawHeightOffset_MethodGroup:
        @typing.overload
        def __call__(self, theSeedType: SeedType, theScale: float, bInWheelBarrow: bool) -> float:...
        @typing.overload
        def __call__(self, theSeedType: SeedType, theScale: float, bInWheelBarrow: bool, theDrawVariation: DrawVariation) -> float:...



class Zombie(GameObject, IComparable):
    cachedZombieRectUpToDate : bool
    draggedByTangleKelp : bool
    mAltitude : float
    mAnimCounter : int
    mAnimFrames : int
    mAnimTicksPerFrame : int
    mApp : LawnApp
    mAttachmentID : Attachment
    mAttachmentID_Save : int
    mAwayCounter : int
    mBlowingAway : bool
    mBoard : Board
    mBodyHealth : int
    mBodyMaxHealth : int
    mBodyReanimID : Reanimation
    mBodyReanimID_Save : int
    mBossBungeeCounter : int
    mBossFireBallReanimID : Reanimation
    mBossFireBallReanimID_Save : int
    mBossHeadCounter : int
    mBossMode : int
    mBossStompCounter : int
    mButteredCounter : int
    mChilledCounter : int
    mDead : bool
    mDroppedLoot : bool
    mFireballRow : int
    mFlatTires : bool
    mFlyingHealth : int
    mFlyingMaxHealth : int
    mFollowerZombieID : Array_1[Zombie]
    mFollowerZombieID_Save : Array_1[int]
    mFrame : int
    mFromWave : int
    mGroanCounter : int
    mHasArm : bool
    mHasGroundTrack : bool
    mHasHead : bool
    mHasHelm : bool
    mHasObject : bool
    mHasShield : bool
    mHeight : int
    mHelmHealth : int
    mHelmMaxHealth : int
    mHelmType : HelmType
    mHitUmbrella : bool
    mIceTrapCounter : int
    mInPool : bool
    mIsButterShowing : bool
    mIsEating : bool
    mIsFireBall : bool
    mJustGotShotCounter : int
    mLastPortalX : int
    mLeaderZombie : Zombie
    mLeaderZombie_Save : int
    mMindControlled : bool
    mMoweredReanimID : Reanimation
    mMoweredReanimID_Save : int
    mOnHighGround : bool
    mOrginalAnimRate : float
    mParticleOffsetX : int
    mParticleOffsetY : int
    mPhaseCounter : int
    mPlayingSong : bool
    mPosScaled : bool
    mPosX : float
    mPosY : float
    mPrevFrame : int
    mPrevTransX : float
    mPrevTransY : float
    mReanimPreview : MemoryImage
    mRelatedZombieID : Zombie
    mRelatedZombieID_Save : int
    mRenderOrder : int
    mRow : int
    mScaleZombie : float
    mShieldHealth : int
    mShieldJustGotShotCounter : int
    mShieldMaxHealth : int
    mShieldRecoilCounter : int
    mShieldType : ShieldType
    mSpecialHeadReanimID : Reanimation
    mSpecialHeadReanimID_Save : int
    mSummonCounter : int
    mSummonedDancers : bool
    mSunMoneyLoot : int
    mSurprised : bool
    mTargetCol : int
    mTargetPlantID : Plant
    mTargetPlantID_Save : int
    mTargetRow : int
    mUseLadderCol : int
    mUsesClipping : bool
    mVariant : bool
    mVelX : float
    mVelZ : float
    mVisible : bool
    mWidth : int
    mX : int
    mY : int
    mYuckyFace : bool
    mYuckyFaceCounter : int
    mYuckySwitchRowsLate : bool
    mYuckyToRow : int
    mZombieAge : int
    mZombieAttackRect : TRect
    mZombieFade : int
    mZombieHeight : ZombieHeight
    mZombiePhase : ZombiePhase
    mZombieRect : TRect
    mZombieType : ZombieType
    WinningZombieReachedDesiredY : bool
    def AddAttachedParticle(self, thePosX: int, thePosY: int, theEffect: ParticleEffect) -> TodParticleSystem: ...
    def AddAttachedReanim(self, thePosX: int, thePosY: int, theReanimType: ReanimationType) -> Reanimation: ...
    def Animate(self) -> None: ...
    def AnimateChewEffect(self) -> None: ...
    def AnimateChewSound(self) -> None: ...
    def ApplyAnimRate(self, theAnimRate: float) -> None: ...
    def ApplyBossSmokeParticles(self, theEnable: bool) -> None: ...
    def ApplyBurn(self) -> None: ...
    def ApplyButter(self) -> None: ...
    def ApplyChill(self, theIsIceTrap: bool) -> None: ...
    def ApplyMindControl(self) -> None: ...
    def AttachShield(self) -> None: ...
    def BalloonPropellerHatSpin(self, theSpinning: bool) -> None: ...
    def BobsledBurn(self) -> None: ...
    def BobsledCrash(self) -> None: ...
    def BobsledDie(self) -> None: ...
    def BossAreBungeesDone(self) -> bool: ...
    def BossBungeeAttack(self) -> None: ...
    def BossBungeeLeave(self) -> None: ...
    def BossBungeeSpawn(self) -> None: ...
    def BossCanStompRow(self, theRow: int) -> bool: ...
    def BossDestroyFireball(self) -> None: ...
    def BossDestroyIceballInRow(self, theRow: int) -> None: ...
    def BossDie(self) -> None: ...
    def BossHeadAttack(self) -> None: ...
    def BossHeadSpit(self) -> None: ...
    def BossHeadSpitContact(self) -> None: ...
    def BossHeadSpitEffect(self) -> None: ...
    def BossPlayIdle(self) -> None: ...
    def BossRVAttack(self) -> None: ...
    def BossRVLanding(self) -> None: ...
    def BossSetupReanim(self) -> None: ...
    def BossSpawnAttack(self) -> None: ...
    def BossSpawnContact(self) -> None: ...
    def BossStartDeath(self) -> None: ...
    def BossStompAttack(self) -> None: ...
    def BossStompContact(self) -> None: ...
    def BungeeDie(self) -> None: ...
    def BungeeDropPlant(self) -> None: ...
    def BungeeDropZombie(self, theDroppedZombie: Zombie, theGridX: int, theGridY: int) -> None: ...
    def BungeeLanding(self) -> None: ...
    def BungeeLiftTarget(self) -> None: ...
    def BungeeStealTarget(self) -> None: ...
    def BurnRow(self, theRow: int) -> None: ...
    def CanBeChilled(self) -> bool: ...
    def CanBeFrozen(self) -> bool: ...
    def CanLoseBodyParts(self) -> bool: ...
    def CanTargetPlant(self, thePlant: Plant, theAttackType: ZombieAttackType) -> bool: ...
    def CatapultDeath(self, theDamageFlags: int) -> None: ...
    def CheckForBoardEdge(self) -> None: ...
    def CheckForHighGround(self) -> None: ...
    def CheckForPool(self) -> None: ...
    def CheckForZombieStep(self) -> None: ...
    def CheckIfPreyCaught(self) -> None: ...
    def CheckSquish(self, theAttackType: ZombieAttackType) -> None: ...
    def ConvertToNormalZombie(self) -> None: ...
    def CountBungeesTargetingSunFlowers(self) -> int: ...
    def CreateTalismanAt(self, theGridX: int, theGridY: int) -> None: ...
    def CreateTalismanMoveAt(self, theGridX: int, theGridY: int) -> None: ...
    def DetachFlag(self) -> None: ...
    def DetachPlantHead(self) -> None: ...
    def DetachRobotTitanHead(self, theDamageFlags: int) -> None: ...
    def DetachShield(self) -> None: ...
    def DieNoLoot(self, giveAchievements: bool) -> None: ...
    def DieWithLoot(self) -> None: ...
    def DiggerLoseAxe(self) -> None: ...
    def Dispose(self) -> None: ...
    def DoDaisies(self) -> None: ...
    def DragUnder(self) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawBobsledReanim(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition], theBeforeZombie: bool) -> None: ...
    def DrawBossBackArm(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawBossFireBall(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawBossPart(self, g: Graphics, theBossPart: BossPart) -> None: ...
    def DrawBungeeCord(self, g: Graphics, theOffsetX: int, theOffsetY: int) -> None: ...
    def DrawBungeeReanim(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawBungeeTarget(self, g: Graphics) -> None: ...
    def DrawButter(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawDancerReanim(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawIceTrap(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition], theFront: bool) -> None: ...
    def DrawReanim(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition], theBaseRenderGroup: int) -> None: ...
    def DrawShadow(self, g: Graphics) -> None: ...
    def DrawZombie(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawZombieHead(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition], theFrame: int) -> None: ...
    def DrawZombiePart(self, g: Graphics, theImage: Image, theFrame: int, theRow: int, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DrawZombieWithParts(self, g: Graphics, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def DropArm(self, theDamageFlags: int) -> None: ...
    def DropFlag(self) -> None: ...
    def DropHead(self, theDamageFlags: int) -> None: ...
    def DropHelm(self, theDamageFlags: int) -> None: ...
    def DropLoot(self) -> None: ...
    def DropPole(self) -> None: ...
    def DropShield(self, theDamageFlags: int) -> None: ...
    def EatPlant(self, thePlant: Plant) -> None: ...
    def EatZombie(self, theZombie: Zombie) -> None: ...
    def EffectedByDamage(self, theDamageRangeFlags: int) -> bool: ...
    def EnableDanceMode(self, theEnableDance: bool) -> None: ...
    def EnableFuture(self, theEnableFuture: bool) -> None: ...
    def EnableMustache(self, theEnableMustache: bool) -> None: ...
    def FindCatapultTarget(self) -> Plant: ...
    def FindPlantTarget(self, theAttackType: ZombieAttackType) -> Plant: ...
    def FindZombieTarget(self) -> Zombie: ...
    def GetBobsledPosition(self) -> int: ...
    def GetBodyDamageIndex(self) -> int: ...
    def GetDancerFrame(self) -> int: ...
    def GetDancerPhase(self) -> ZombiePhase: ...
    def GetDrawPos(self, theDrawPos: clr.Reference[ZombieDrawPosition]) -> None: ...
    def GetHelmDamageIndex(self) -> int: ...
    @staticmethod
    def GetNewZombie() -> Zombie: ...
    def GetPosYBasedOnRow(self, theRow: int) -> float: ...
    def GetShieldDamageIndex(self) -> int: ...
    def GetZombieAttackRect(self) -> TRect: ...
    @staticmethod
    def GetZombieDefinition(theZombieType: ZombieType) -> ZombieDefinition: ...
    def GetZombieRect(self) -> TRect: ...
    def HasShadow(self) -> bool: ...
    def HasYuckyFaceImage(self) -> bool: ...
    def HitIceTrap(self) -> bool: ...
    def IsAboutToLeaveHighGround(self) -> bool: ...
    def IsAliveWithoutHead(self) -> bool: ...
    def IsBobsledTeamWithSled(self) -> bool: ...
    def IsBouncingPogo(self) -> bool: ...
    def IsDeadOrDying(self) -> bool: ...
    def IsFireResistant(self) -> bool: ...
    def IsFlying(self) -> bool: ...
    def IsImmobilizied(self) -> bool: ...
    def IsMovingAtChilledSpeed(self) -> bool: ...
    def IsOnBoard(self) -> bool: ...
    def IsOnHighGround(self) -> bool: ...
    def IsSquashTarget(self, exceptMe: Plant) -> bool: ...
    def IsStandingOnSpikeweed(self) -> Plant: ...
    def IsTanglekelpTarget(self) -> bool: ...
    def IsTangleKelpTarget(self) -> bool: ...
    def IsWalkingBackwards(self) -> bool: ...
    def IsZombotany(self) -> bool: ...
    def LandFlyer(self, theDamageFlags: int) -> None: ...
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def LoadingComplete(self) -> None: ...
    def LoadPlainZombieReanim(self) -> None: ...
    def LoadReanim(self, theReanimationType: ReanimationType) -> Reanimation: ...
    def LoadWaterZombieReanim(self) -> None: ...
    def MowDown(self) -> None: ...
    def NeedsMoreBackupDancers(self) -> bool: ...
    def OverrideParticleColor(self, aParticle: TodParticleSystem) -> None: ...
    def OverrideParticleScale(self, aParticle: TodParticleSystem) -> None: ...
    def PickBungeeZombieTarget(self, theColumn: int) -> None: ...
    def PickRandomSpeed(self) -> None: ...
    def PlayDeathAnim(self, theDamageFlags: int) -> None: ...
    def PlayZombieAppearSound(self) -> None: ...
    def PlayZombieReanim(self, theTrackName: clr.Reference[str], theLoopType: ReanimLoopType, theBlendTime: int, theAnimRate: float) -> None: ...
    def PogoBreak(self, theDamageFlags: int) -> None: ...
    def PoolSplash(self, theInToPoolSound: bool) -> None: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    @staticmethod
    def PreloadZombieResources(theZombieType: ZombieType) -> None: ...
    def PrepareForReuse(self) -> None: ...
    def ReanimIgnoreClipRect(self, theTrackName: str, theIgnoreClipRect: bool) -> None: ...
    def ReanimReenableClipping(self) -> None: ...
    def ReanimShowPrefix(self, theTrackPrefix: str, theRenderGroup: int) -> None: ...
    def RemoveButter(self) -> None: ...
    def RemoveColdEffects(self) -> None: ...
    def RemoveIceTrap(self) -> None: ...
    def RemoveSurprise(self) -> None: ...
    def RiseFromGrave(self, theCol: int, theRow: int) -> None: ...
    def SaveToFile(self, b: Buffer) -> bool: ...
    def SetAnimRate(self, theAnimRate: float) -> None: ...
    def SetRow(self, theRow: int) -> None: ...
    @staticmethod
    def SetupDoorArms(aReanim: Reanimation, theShow: bool) -> None: ...
    def SetupDrawZombieWon(self, g: Graphics) -> bool: ...
    @staticmethod
    def SetupReanimLayers(aReanim: Reanimation, theZombieType: ZombieType) -> None: ...
    def SetupWaterTrack(self, theTrackName: clr.Reference[str]) -> None: ...
    def ShowDoorArms(self, theShow: bool) -> None: ...
    def ShowYuckyFace(self, theShow: bool) -> None: ...
    def SquishAllInSquare(self, theX: int, theY: int, theAttackType: ZombieAttackType) -> None: ...
    def StartEating(self) -> None: ...
    def StartMindControlled(self) -> None: ...
    def StartWalkAnim(self, theBlendTime: int) -> None: ...
    def StartZombieSound(self) -> None: ...
    def StopEating(self) -> None: ...
    def StopZombieSound(self) -> None: ...
    def SummonBackupDancer(self, theRow: int, thePosX: int) -> Zombie: ...
    def SummonBackupDancers(self) -> None: ...
    def TakeBodyDamage(self, theDamage: int, theDamageFlags: int) -> None: ...
    def TakeDamage(self, theDamage: int, theDamageFlags: int) -> None: ...
    def TakeFlyingDamage(self, theDamage: int, theDamageFlags: int) -> int: ...
    def TakeHelmDamage(self, theDamage: int, theDamageFlags: int) -> int: ...
    def TakeShieldDamage(self, theDamage: int, theDamageFlags: int) -> int: ...
    def TrySpawnLevelAward(self) -> bool: ...
    def Update(self) -> None: ...
    def UpdateActions(self) -> None: ...
    def UpdateAnimSpeed(self) -> None: ...
    def UpdateBoss(self) -> None: ...
    def UpdateBossFireball(self) -> None: ...
    def UpdateBurn(self) -> None: ...
    def UpdateClimbingLadder(self) -> None: ...
    def UpdateDamageStates(self, theDamageFlags: int) -> None: ...
    def UpdateDeath(self) -> None: ...
    def UpdateLadder(self) -> None: ...
    def UpdateMowered(self) -> None: ...
    def UpdateNinja(self) -> None: ...
    def UpdatePlaying(self) -> None: ...
    def UpdateReanim(self) -> None: ...
    def UpdateYeti(self) -> None: ...
    def UpdateYuckyFace(self) -> None: ...
    def UpdateZamboni(self) -> None: ...
    def UpdateZombieBackupDancer(self) -> None: ...
    def UpdateZombieBobsled(self) -> None: ...
    def UpdateZombieBungee(self) -> None: ...
    def UpdateZombieCatapult(self) -> None: ...
    def UpdateZombieChimney(self) -> None: ...
    def UpdateZombieDancer(self) -> None: ...
    def UpdateZombieDigger(self) -> None: ...
    def UpdateZombieDolphinRider(self) -> None: ...
    def UpdateZombieFalling(self) -> None: ...
    def UpdateZombieFlyer(self) -> None: ...
    def UpdateZombieGargantuar(self) -> None: ...
    def UpdateZombieGatlingHead(self) -> None: ...
    def UpdateZombieHighGround(self) -> None: ...
    def UpdateZombieImp(self) -> None: ...
    def UpdateZombieJackInTheBox(self) -> None: ...
    def UpdateZombieJalapenoHead(self) -> None: ...
    def UpdateZombieMonk(self) -> None: ...
    def UpdateZombieNewspaper(self) -> None: ...
    def UpdateZombiePeaHead(self) -> None: ...
    def UpdateZombiePogo(self) -> None: ...
    def UpdateZombiePolevaulter(self) -> None: ...
    def UpdateZombiePool(self) -> None: ...
    def UpdateZombiePosition(self) -> None: ...
    def UpdateZombieRiseFromGrave(self) -> None: ...
    def UpdateZombieSnorkel(self) -> None: ...
    def UpdateZombieSquashHead(self) -> None: ...
    def UpdateZombieTalisman(self) -> None: ...
    def UpdateZombieWalking(self) -> None: ...
    def UpdateZombieWalkingIntoHouse(self) -> None: ...
    def UpdateZombiquarium(self) -> None: ...
    def WalkIntoHouse(self) -> None: ...
    def ZamboniDeath(self, theDamageFlags: int) -> None: ...
    def ZombieCatapultFire(self, thePlant: Plant) -> None: ...
    def ZombieInitialize(self, theRow: int, theType: ZombieType, theVariant: bool, theParentZombie: Zombie, theFromWave: int) -> None: ...
    def ZombieNotWalking(self) -> bool: ...
    def ZombieTargetLeadX(self, theTime: float) -> float: ...
    @staticmethod
    def ZombieTypeCanGoInPool(theZombieType: ZombieType) -> bool: ...
    @staticmethod
    def ZombieTypeCanGoInPoolExtended(theZombieType: ZombieType) -> bool: ...
    @staticmethod
    def ZombieTypeCanGoOnHighGround(theZombieType: ZombieType) -> bool: ...
    def ZombiquariumFindClosestBrain(self) -> bool: ...
    # Skipped GetTrackPosition due to it being static, abstract and generic.

    GetTrackPosition : GetTrackPosition_MethodGroup
    class GetTrackPosition_MethodGroup:
        @typing.overload
        def __call__(self, theTrackName: str, thePosX: clr.Reference[float], thePosY: clr.Reference[float]) -> None:...
        @typing.overload
        def __call__(self, theTrackName: clr.Reference[str], thePosX: clr.Reference[float], thePosY: clr.Reference[float]) -> None:...

    # Skipped ReanimShowTrack due to it being static, abstract and generic.

    ReanimShowTrack : ReanimShowTrack_MethodGroup
    class ReanimShowTrack_MethodGroup:
        @typing.overload
        def __call__(self, theTrackName: str, theRenderGroup: int) -> None:...
        @typing.overload
        def __call__(self, theTrackName: clr.Reference[str], theRenderGroup: int) -> None:...


    class ZombieParts(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Body : Zombie.ZombieParts # 0
        Head : Zombie.ZombieParts # 1
        HeadEating : Zombie.ZombieParts # 2
        Tongue : Zombie.ZombieParts # 3
        Arm : Zombie.ZombieParts # 4
        Hair : Zombie.ZombieParts # 5
        HeadYucky : Zombie.ZombieParts # 6
        ArmPickaxe : Zombie.ZombieParts # 7
        ArmPolevault : Zombie.ZombieParts # 8
        ArmLeash : Zombie.ZombieParts # 9
        ArmFlag : Zombie.ZombieParts # 10
        Pogo : Zombie.ZombieParts # 11
        Digger : Zombie.ZombieParts # 12


    class ZombieRenderLayerOffset(typing.SupportsInt):
        @typing.overload
        def __init__(self, value : int) -> None: ...
        @typing.overload
        def __init__(self, value : int, force_if_true: bool) -> None: ...
        def __int__(self) -> int: ...
        
        # Values:
        Bobsled4 : Zombie.ZombieRenderLayerOffset # 0
        Bobsled3 : Zombie.ZombieRenderLayerOffset # 1
        Bobsled2 : Zombie.ZombieRenderLayerOffset # 2
        Bobsled1 : Zombie.ZombieRenderLayerOffset # 3
        Normal : Zombie.ZombieRenderLayerOffset # 4
        DogWalker : Zombie.ZombieRenderLayerOffset # 5
        Dog : Zombie.ZombieRenderLayerOffset # 6
        Digger : Zombie.ZombieRenderLayerOffset # 7
        Zamboni : Zombie.ZombieRenderLayerOffset # 8



class ZombieAllowedLevels:
    def __init__(self, aZombieType: ZombieType, levels: Array_1[int]) -> None: ...
    mAllowedOnLevel : Array_1[int]
    mZombieType : ZombieType


class ZombieAttackType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Chew : ZombieAttackType # 0
    DriveOver : ZombieAttackType # 1
    Vault : ZombieAttackType # 2
    Ladder : ZombieAttackType # 3


class ZombieDefinition:
    def __init__(self, aZombieType: ZombieType, aReanimationType: ReanimationType, aZombieValue: int, aStartingLevel: int, aFirstAllowedWave: int, aPickWeight: int, aZombieName: str) -> None: ...
    mFirstAllowedWave : int
    mPickWeight : int
    mReanimationType : ReanimationType
    mStartingLevel : int
    mZombieName : str
    mZombieType : ZombieType
    mZombieValue : int


class ZombieDescriptor:
    def __init__(self, theType: ZombieType, aX: int, aY: int) -> None: ...
    type : ZombieType
    x : int
    y : int


class ZombieDrawPosition:
    mArmY : int
    mBodyY : float
    mClipHeight : float
    mHeadX : int
    mHeadY : int
    mImageOffsetX : float
    mImageOffsetY : float


class ZombieGalleryWidget(Widget):
    def __init__(self, theDialog: AlmanacDialog) -> None: ...
    FullRect : TRect
    mClip : bool
    mColors : List_1[Color]
    mDialog : AlmanacDialog
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mLastWMUpdateCount : int
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPriority : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZOrder : int
    def Draw(self, g: Graphics) -> None: ...
    def GetZombiePosition(self, theIndex: int, x: clr.Reference[int], y: clr.Reference[int]) -> None: ...
    def GetZombieType(self, theIndex: int) -> ZombieType: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def ZombieHitTest(self, x: int, y: int) -> ZombieType: ...
    def ZombieIsShown(self, theZombieType: ZombieType) -> bool: ...


class ZombieHeight(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ZombieNormal : ZombieHeight # 0
    InToPool : ZombieHeight # 1
    OutOfPool : ZombieHeight # 2
    DraggedUnder : ZombieHeight # 3
    UpToHighGround : ZombieHeight # 4
    DownOffHighGround : ZombieHeight # 5
    UpLadder : ZombieHeight # 6
    Falling : ZombieHeight # 7
    InToChimney : ZombieHeight # 8
    GettingBungeeDropped : ZombieHeight # 9
    Zombiquarium : ZombieHeight # 10


class ZombieID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : ZombieID # 0


class ZombiePhase(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ZombieNormal : ZombiePhase # 0
    ZombieDying : ZombiePhase # 1
    ZombieBurned : ZombiePhase # 2
    ZombieMowered : ZombiePhase # 3
    BungeeDiving : ZombiePhase # 4
    BungeeDivingScreaming : ZombiePhase # 5
    BungeeAtBottom : ZombiePhase # 6
    BungeeGrabbing : ZombiePhase # 7
    BungeeRising : ZombiePhase # 8
    BungeeHitOuchy : ZombiePhase # 9
    BungeeCutscene : ZombiePhase # 10
    PolevaulterPreVault : ZombiePhase # 11
    PolevaulterInVault : ZombiePhase # 12
    PolevaulterPostVault : ZombiePhase # 13
    RisingFromGrave : ZombiePhase # 14
    JackInTheBoxRunning : ZombiePhase # 15
    JackInTheBoxPopping : ZombiePhase # 16
    BobsledSliding : ZombiePhase # 17
    BobsledBoarding : ZombiePhase # 18
    BobsledCrashing : ZombiePhase # 19
    PogoBouncing : ZombiePhase # 20
    PogoHighBounce1 : ZombiePhase # 21
    PogoHighBounce2 : ZombiePhase # 22
    PogoHighBounce3 : ZombiePhase # 23
    PogoHighBounce4 : ZombiePhase # 24
    PogoHighBounce5 : ZombiePhase # 25
    PogoHighBounce6 : ZombiePhase # 26
    PogoForwardBounce2 : ZombiePhase # 27
    PogoForwardBounce7 : ZombiePhase # 28
    NewspaperReading : ZombiePhase # 29
    NewspaperMaddening : ZombiePhase # 30
    NewspaperMad : ZombiePhase # 31
    DiggerTunneling : ZombiePhase # 32
    DiggerRising : ZombiePhase # 33
    DiggerTunnelingPauseWithoutAxe : ZombiePhase # 34
    DiggerRiseWithoutAxe : ZombiePhase # 35
    DiggerStunned : ZombiePhase # 36
    DiggerWalking : ZombiePhase # 37
    DiggerWalkingWithoutAxe : ZombiePhase # 38
    DiggerCutscene : ZombiePhase # 39
    DancerDancingIn : ZombiePhase # 40
    DancerSnappingFingers : ZombiePhase # 41
    DancerSnappingFingersWithLight : ZombiePhase # 42
    DancerSnappingFingersHold : ZombiePhase # 43
    DancerDancingLeft : ZombiePhase # 44
    DancerWalkToRaise : ZombiePhase # 45
    DancerRaiseLeft1 : ZombiePhase # 46
    DancerRaiseRight1 : ZombiePhase # 47
    DancerRaiseLeft2 : ZombiePhase # 48
    DancerRaiseRight2 : ZombiePhase # 49
    DancerRising : ZombiePhase # 50
    DolphinWalking : ZombiePhase # 51
    DolphinIntoPool : ZombiePhase # 52
    DolphinRiding : ZombiePhase # 53
    DolphinInJump : ZombiePhase # 54
    DolphinWalkingInPool : ZombiePhase # 55
    DolphinWalkingWithoutDolphin : ZombiePhase # 56
    SnorkelWalking : ZombiePhase # 57
    SnorkelIntoPool : ZombiePhase # 58
    SnorkelWalkingInPool : ZombiePhase # 59
    SnorkelUpToEat : ZombiePhase # 60
    SnorkelEatingInPool : ZombiePhase # 61
    SnorkelDownFromEat : ZombiePhase # 62
    ZombiquariumAccel : ZombiePhase # 63
    ZombiquariumDrift : ZombiePhase # 64
    ZombiquariumBackAndForth : ZombiePhase # 65
    ZombiquariumBite : ZombiePhase # 66
    CatapultLaunching : ZombiePhase # 67
    CatapultReloading : ZombiePhase # 68
    GargantuarThrowing : ZombiePhase # 69
    GargantuarSmashing : ZombiePhase # 70
    ImpGettingThrown : ZombiePhase # 71
    ImpLanding : ZombiePhase # 72
    BalloonFlying : ZombiePhase # 73
    BalloonPopping : ZombiePhase # 74
    BalloonWalking : ZombiePhase # 75
    LadderCarrying : ZombiePhase # 76
    LadderPlacing : ZombiePhase # 77
    BossEnter : ZombiePhase # 78
    BossIdle : ZombiePhase # 79
    BossSpawning : ZombiePhase # 80
    BossStomping : ZombiePhase # 81
    BossBungeesEnter : ZombiePhase # 82
    BossBungeesDrop : ZombiePhase # 83
    BossBungeesLeave : ZombiePhase # 84
    BossDropRv : ZombiePhase # 85
    BossHeadEnter : ZombiePhase # 86
    BossHeadIdleBeforeSpit : ZombiePhase # 87
    BossHeadIdleAfterSpit : ZombiePhase # 88
    BossHeadSpit : ZombiePhase # 89
    BossHeadLeave : ZombiePhase # 90
    YetiRunning : ZombiePhase # 91
    SquashPreLaunch : ZombiePhase # 92
    SquashRising : ZombiePhase # 93
    SquashFalling : ZombiePhase # 94
    SquashDoneFalling : ZombiePhase # 95
    MonkInBell : ZombiePhase # 96
    NinjaShownByPlantern : ZombiePhase # 97
    TalismanAttacking : ZombiePhase # 98
    TalismanLeaving : ZombiePhase # 99
    PropellerBlownAway : ZombiePhase # 100
    PropellerTeeter : ZombiePhase # 101


class ZombiePicker:
    def __init__(self) -> None: ...
    mAllWavesZombieTypeCount : Array_1[int]
    mZombieCount : int
    mZombiePoints : int
    mZombieTypeCount : Array_1[int]


class ZombiePileMarker:
    def __init__(self) -> None: ...
    mGamer : Gamer
    mHeight : int


class ZombiePileObject:
    def __init__(self, aHeight: int, aType: ZombiePileObjectType) -> None: ...
    gemImage : Image
    gemRotationSpeed : float
    gemSpeedX : float
    gemSpeedY : float
    maxGemSpeedX : float
    mCounter : float
    mHeight : int
    mOffsetX : float
    mOffsetY : float
    mReanim : Reanimation
    mType : ZombiePileObjectType
    mY : int


class ZombiePileObjectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Balloon : ZombiePileObjectType # 0
    YellowCloud : ZombiePileObjectType # 1
    Airplane : ZombiePileObjectType # 2
    Moon : ZombiePileObjectType # 3
    Satellite : ZombiePileObjectType # 4
    PeggleUrsamajor : ZombiePileObjectType # 5
    Astronaut : ZombiePileObjectType # 6
    Blackhole : ZombiePileObjectType # 7
    Arrow : ZombiePileObjectType # 8
    Gem0 : ZombiePileObjectType # 9
    Gem1 : ZombiePileObjectType # 10
    Gem2 : ZombiePileObjectType # 11
    Gem3 : ZombiePileObjectType # 12
    Gem4 : ZombiePileObjectType # 13
    Gem5 : ZombiePileObjectType # 14
    Gem6 : ZombiePileObjectType # 15


class ZombiePileWidget(Widget, ButtonListener):
    def __init__(self, theApp: LawnApp) -> None: ...
    friendMarkers : Array_1[ZombiePileMarker]
    FullRect : TRect
    gPileObjects : Array_1[ZombiePileObject]
    mApp : LawnApp
    maxHeight : int
    mBackButton : NewLawnButton
    mClip : bool
    mColors : List_1[Color]
    mDisabled : bool
    mDoFinger : bool
    mHasAlpha : bool
    mHasFocus : bool
    mHasTransparencies : bool
    mHeight : int
    mIsDown : bool
    mIsOver : bool
    mIZombieButton : DialogButton
    mLastWMUpdateCount : int
    mLoadedFriends : bool
    mMouseInsets : Insets
    mMouseVisible : bool
    mParent : WidgetContainer
    mPileHeight : int
    mPriority : int
    mScreenTop : int
    mTabNext : Widget
    mTabPrev : Widget
    mUpdateCnt : int
    mUpdateIterator : LinkedListNode_1[Widget]
    mUpdateIteratorModified : bool
    mVasebreakerButton : DialogButton
    mVisible : bool
    mWantsFocus : bool
    mWidgetFlagsMod : FlagsMod
    mWidgetManager : WidgetManager
    mWidgets : LinkedList_1[Widget]
    mWidth : int
    mX : int
    mY : int
    mZombieScale : int
    mZombiesKilledButton : DialogButton
    mZombieSpace : int
    mZOrder : int
    pileObjectParallax : float
    screenBottomLeft : TriVertex
    screenBottomRight : TriVertex
    skyBottomLeft : TriVertex
    skyBottomRight : TriVertex
    skyColor : Color
    skyEndHeight : int
    spaceBottomLeft : TriVertex
    spaceBottomRight : TriVertex
    spaceColor : Color
    spaceStartHeight : int
    spaceTopLeft : TriVertex
    spaceTopRight : TriVertex
    starParallax : float
    transferBottomLeft : TriVertex
    transferBottomRight : TriVertex
    def BackButtonPress(self) -> bool: ...
    def ButtonDepress(self, theId: int) -> None: ...
    def ButtonDownTick(self, id: int) -> None: ...
    def ButtonMouseEnter(self, id: int) -> None: ...
    def ButtonMouseLeave(self, id: int) -> None: ...
    def ButtonMouseMove(self, id: int, x: int, y: int) -> None: ...
    def ButtonMouseTick(self, id: int) -> None: ...
    def CalculatePileHeight(self, height: int) -> int: ...
    def Draw(self, g: Graphics) -> None: ...
    def DrawOverlay(self, g: Graphics) -> None: ...
    def DrawPileMarkers(self, g: Graphics) -> None: ...
    def DrawPileObjects(self, g: Graphics) -> None: ...
    def MouseUp(self, x: int, y: int, theClickCount: int) -> None: ...
    def SetGray(self, aGrayed: bool) -> None: ...
    def SetObjectYVals(self) -> None: ...
    def ShowLeaderboard(self, aType: LeaderBoardType) -> None: ...
    def Update(self) -> None: ...
    def UpdatePileObjects(self) -> None: ...
    def UpdateToolTip(self) -> None: ...
    # Skipped ButtonPress due to it being static, abstract and generic.

    ButtonPress : ButtonPress_MethodGroup
    class ButtonPress_MethodGroup:
        @typing.overload
        def __call__(self, theId: int) -> None:...
        @typing.overload
        def __call__(self, id: int, id2: int) -> None:...

    # Skipped DoScroll due to it being static, abstract and generic.

    DoScroll : DoScroll_MethodGroup
    class DoScroll_MethodGroup:
        @typing.overload
        def __call__(self, touch: _Touch) -> bool:...
        @typing.overload
        def __call__(self, x: int, y: int) -> bool:...



class ZombieType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Normal : ZombieType # 0
    Flag : ZombieType # 1
    TrafficCone : ZombieType # 2
    Polevaulter : ZombieType # 3
    Pail : ZombieType # 4
    Newspaper : ZombieType # 5
    Door : ZombieType # 6
    Football : ZombieType # 7
    Dancer : ZombieType # 8
    BackupDancer : ZombieType # 9
    DuckyTube : ZombieType # 10
    Snorkel : ZombieType # 11
    Zamboni : ZombieType # 12
    Bobsled : ZombieType # 13
    DolphinRider : ZombieType # 14
    JackInTheBox : ZombieType # 15
    Balloon : ZombieType # 16
    Digger : ZombieType # 17
    Pogo : ZombieType # 18
    Yeti : ZombieType # 19
    Bungee : ZombieType # 20
    Ladder : ZombieType # 21
    Catapult : ZombieType # 22
    Gargantuar : ZombieType # 23
    Imp : ZombieType # 24
    Boss : ZombieType # 25
    PeaHead : ZombieType # 26
    WallnutHead : ZombieType # 27
    JalapenoHead : ZombieType # 28
    GatlingHead : ZombieType # 29
    SquashHead : ZombieType # 30
    TallnutHead : ZombieType # 31
    RedeyeGargantuar : ZombieType # 32
    RobotTitan : ZombieType # 33
    RedeyeRobotTitan : ZombieType # 34
    Monk : ZombieType # 35
    FootballPremium : ZombieType # 36
    Ninja : ZombieType # 37
    Talisman : ZombieType # 38
    Propeller : ZombieType # 39
    ZombieTypesCount : ZombieType # 40
    CachedPolevaulterWithPole : ZombieType # 41
    CachedZombieTypesCount : ZombieType # 42
    Invalid : ZombieType # -1

