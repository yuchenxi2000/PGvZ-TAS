import typing, clr, abc
from Sexy import SexyTransform2D, Graphics, SexyColor, SexyVector2, Image, XNASoundInstance, TRect, MemoryImage, Font, ResourceManager, Buffer
from System import Array_1, MulticastDelegate, IAsyncResult, AsyncCallback
from System.Collections.Generic import List_1, HashSet_1, Dictionary_2
from Microsoft.Xna.Framework.Graphics import Texture2D, Effect
from System.Runtime.CompilerServices import ConditionalWeakTable_2
from Microsoft.Xna.Framework import Matrix
from Spine import AnimationState, Skeleton, SkeletonRenderer, Atlas, SkeletonData
from System.Reflection import MethodInfo

class AttachEffect:
    mDontDrawIfParentHidden : bool
    mDontPropogateColor : bool
    mEffectID : typing.Any
    mEffectID_Save : int
    mEffectType : EffectType
    mOffset : SexyTransform2D
    @staticmethod
    def GetNewAttachEffect() -> AttachEffect: ...
    def PrepareForReuse(self) -> None: ...
    def Reset(self) -> None: ...


class AttacherInfo:
    def __init__(self) -> None: ...
    mAnimRate : float
    mLoopType : ReanimLoopType
    mReanimName : str
    mTrackName : str


class Attachment:
    mActive : bool
    mDead : bool
    mEffectArray : Array_1[AttachEffect]
    mNumEffects : int
    mUsesClipping : bool
    reused : bool
    def AttachmentDie(self) -> None: ...
    def CrossFade(self, theCrossFadeName: str) -> None: ...
    def Detach(self) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics, theParentHidden: bool, doScale: bool) -> None: ...
    @staticmethod
    def GetNewAttachment() -> Attachment: ...
    def OverrideColor(self, theColor: SexyColor) -> None: ...
    def OverrideScale(self, theScale: float) -> None: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...
    def PropogateColor(self, theColor: SexyColor, theEnableAdditiveColor: bool, theAdditiveColor: SexyColor, theEnableOverlayColor: bool, theOverlayColor: SexyColor) -> None: ...
    def SetMatrix(self, theMatrix: clr.Reference[SexyTransform2D]) -> None: ...
    def SetPosition(self, thePosition: SexyVector2) -> None: ...
    def Update(self) -> None: ...
    def Upgrade600(self) -> None: ...


class AttachmentHolder:
    def __init__(self) -> None: ...
    mAttachments : List_1[Attachment]
    def AllocAttachment(self) -> Attachment: ...
    def Dispose(self) -> None: ...
    def DisposeHolder(self) -> None: ...
    def InitializeHolder(self) -> None: ...


class AttachmentID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : AttachmentID # 0


class DataArray_GenericClasses(abc.ABCMeta):
    Generic_DataArray_GenericClasses_DataArray_1_T = typing.TypeVar('Generic_DataArray_GenericClasses_DataArray_1_T')
    def __getitem__(self, types : typing.Type[Generic_DataArray_GenericClasses_DataArray_1_T]) -> typing.Type[DataArray_1[Generic_DataArray_GenericClasses_DataArray_1_T]]: ...

DataArray : DataArray_GenericClasses

DataArray_1_T = typing.TypeVar('DataArray_1_T')
class DataArray_1(typing.Generic[DataArray_1_T]):
    def __init__(self) -> None: ...
    mBlock : Array_1[DataArray_1_T]
    mFreeListHead : int
    mMaxSize : int
    mMaxUsedCount : int
    mName : str
    mNextKey : int
    mSize : int
    def DataArrayAlloc(self) -> DataArray_1_T: ...
    def DataArrayDispose(self) -> None: ...
    def DataArrayFree(self, theItem: DataArray_1_T) -> None: ...
    def DataArrayFreeAll(self) -> None: ...
    def DataArrayGet(self, theId: int) -> DataArray_1_T: ...
    def DataArrayGetID(self, theItem: DataArray_1_T) -> int: ...
    def DataArrayInitialize(self, theMaxSize: int, theName: str) -> None: ...
    def DataArrayTryToGet(self, theId: int) -> DataArray_1_T: ...
    def Dispose(self) -> None: ...
    def IterateNext(self, theItem: clr.Reference[DataArray_1_T]) -> bool: ...


class DataArrayFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    DATAID_NULL : DataArrayFlags # 0
    DATA_ARRAY_KEY_FIRST : DataArrayFlags # 1
    DATA_ARRAY_KEY_SHIFT : DataArrayFlags # 16
    DATA_ARRAY_INDEX_MASK : DataArrayFlags # 65535
    DATA_ARRAY_MAX_SIZE : DataArrayFlags # 65536
    DATA_ARRAY_KEY_MASK : DataArrayFlags # 4294901760


class DefFieldType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Invalid : DefFieldType # 0
    Int : DefFieldType # 1
    Float : DefFieldType # 2
    String : DefFieldType # 3
    Enum : DefFieldType # 4
    Vector2 : DefFieldType # 5
    Array : DefFieldType # 6
    TrackFloat : DefFieldType # 7
    Flags : DefFieldType # 8
    Image : DefFieldType # 9
    Font : DefFieldType # 10


class DrawStringJustification(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Left : DrawStringJustification # 0
    Right : DrawStringJustification # 1
    Center : DrawStringJustification # 2
    LeftVerticalMiddle : DrawStringJustification # 3
    RightVerticalMiddle : DrawStringJustification # 4
    CenterVerticalMiddle : DrawStringJustification # 5


class EffectSystem:
    def __init__(self) -> None: ...
    gEffectSystem : EffectSystem
    mAttachmentHolder : AttachmentHolder
    mParticleHolder : TodParticleHolder
    mReanimationHolder : ReanimationHolder
    mTrailHolder : TrailHolder
    def Dispose(self) -> None: ...
    def EffectSystemDispose(self) -> None: ...
    def EffectSystemFreeAll(self) -> None: ...
    def EffectSystemInitialize(self) -> None: ...
    def ProcessDeleteQueue(self) -> None: ...
    def Update(self) -> None: ...


class EffectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Particle : EffectType # 0
    Trail : EffectType # 1
    Reanim : EffectType # 2
    Attachment : EffectType # 3
    Other : EffectType # 4


class EmitterType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Circle : EmitterType # 0
    Box : EmitterType # 1
    BoxPath : EmitterType # 2
    CirclePath : EmitterType # 3
    CircleEvenSpacing : EmitterType # 4


class FilterEffect:
    def __init__(self) -> None: ...
    gFilterCacheLastFrame : HashSet_1[Texture2D]
    gFilterCacheThisFrame : HashSet_1[Texture2D]
    gFilterMap : List_1[ConditionalWeakTable_2[Texture2D, Texture2D]]
    mEffectMap : Dictionary_2[FilterEffectType, Effect]
    @staticmethod
    def FilterEffectDisposeForApp() -> None: ...
    @staticmethod
    def FilterEffectGetImage(theImage: Image, theFilterEffect: FilterEffectType) -> Image: ...
    @staticmethod
    def FilterEffectInitForApp() -> None: ...
    @staticmethod
    def FilterEffectInitTexture(texture: Texture2D, theFilterEffect: FilterEffectType) -> Texture2D: ...
    @staticmethod
    def FilterEffectProcessDeleteQueue() -> None: ...


class FilterEffectType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    WashedOut : FilterEffectType # 0
    LessWashedOut : FilterEffectType # 1
    White : FilterEffectType # 2
    FilterEffectCount : FilterEffectType # 3
    None_ : FilterEffectType # -1


class FloatParameterTrack:
    def __init__(self) -> None: ...
    mCountNodes : int
    mNodes : Array_1[FloatParameterTrackNode]


class FloatParameterTrackNode:
    def __init__(self) -> None: ...
    mCurveType : TodCurves
    mDistribution : TodCurves
    mHighValue : float
    mLowValue : float
    mTime : float
    SIZE : int


class FoleyFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Loop : FoleyFlags # 0
    OneAtATime : FoleyFlags # 1
    MuteOnPause : FoleyFlags # 2
    UsesMusicVolume : FoleyFlags # 3
    DontRepeat : FoleyFlags # 4


class FoleyInstance:
    def __init__(self) -> None: ...
    mInstance : XNASoundInstance
    mPauseOffset : int
    mRefCount : int
    mStartTime : int
    @property
    def mPaused(self) -> bool: ...
    @mPaused.setter
    def mPaused(self, value: bool) -> bool: ...


class FoleyParams:
    def __init__(self, aFoleyType: FoleyType, aPitchRange: float, aIDs: Array_1[int], aFoleyFlags: int) -> None: ...
    mFoleyFlags : int
    mFoleyType : FoleyType
    mPitchRange : float
    mSfxID : Array_1[int]


class FoleyType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Sun : FoleyType # 0
    Splat : FoleyType # 1
    Lawnmower : FoleyType # 2
    Throw : FoleyType # 3
    SpawnSun : FoleyType # 4
    Chomp : FoleyType # 5
    ChompSoft : FoleyType # 6
    Plant : FoleyType # 7
    UseShovel : FoleyType # 8
    Drop : FoleyType # 9
    Bleep : FoleyType # 10
    Groan : FoleyType # 11
    Brains : FoleyType # 12
    Jackinthebox : FoleyType # 13
    ArtChallenge : FoleyType # 14
    Zamboni : FoleyType # 15
    Thunder : FoleyType # 16
    Frozen : FoleyType # 17
    Zombiesplash : FoleyType # 18
    Bowlingimpact : FoleyType # 19
    Squish : FoleyType # 20
    TirePop : FoleyType # 21
    Explosion : FoleyType # 22
    Slurp : FoleyType # 23
    LimbsPop : FoleyType # 24
    PogoZombie : FoleyType # 25
    SnowPeaSparkles : FoleyType # 26
    ZombieFalling : FoleyType # 27
    Puff : FoleyType # 28
    Fume : FoleyType # 29
    Coin : FoleyType # 30
    KernelSplat : FoleyType # 31
    Digger : FoleyType # 32
    JackSurprise : FoleyType # 33
    VaseBreaking : FoleyType # 34
    PoolCleaner : FoleyType # 35
    Basketball : FoleyType # 36
    Ignite : FoleyType # 37
    Firepea : FoleyType # 38
    Thump : FoleyType # 39
    SquashHmm : FoleyType # 40
    Magnetshroom : FoleyType # 41
    Butter : FoleyType # 42
    BungeeScream : FoleyType # 43
    BossExplosionSmall : FoleyType # 44
    ShieldHit : FoleyType # 45
    Swing : FoleyType # 46
    Bonk : FoleyType # 47
    Rain : FoleyType # 48
    DolphinBeforeJumping : FoleyType # 49
    DolphinAppears : FoleyType # 50
    PlantWater : FoleyType # 51
    ZombieEnteringWater : FoleyType # 52
    Gravebusterchomp : FoleyType # 53
    Cherrybomb : FoleyType # 54
    JalapenoIgnite : FoleyType # 55
    ReverseExplosion : FoleyType # 56
    PlasticHit : FoleyType # 57
    Winmusic : FoleyType # 58
    Ballooninflate : FoleyType # 59
    Bigchomp : FoleyType # 60
    Melonimpact : FoleyType # 61
    Plantgrow : FoleyType # 62
    Shoop : FoleyType # 63
    Juicy : FoleyType # 64
    NewspaperRarrgh : FoleyType # 65
    NewspaperRip : FoleyType # 66
    Floop : FoleyType # 67
    Coffee : FoleyType # 68
    Lowgroan : FoleyType # 69
    Prize : FoleyType # 70
    Yuck : FoleyType # 71
    Umbrella : FoleyType # 72
    Grassstep : FoleyType # 73
    Shovel : FoleyType # 74
    Coblaunch : FoleyType # 75
    Watering : FoleyType # 76
    Polevault : FoleyType # 77
    GravestoneRumble : FoleyType # 78
    DirtRise : FoleyType # 79
    Fertilizer : FoleyType # 80
    Portal : FoleyType # 81
    Wakeup : FoleyType # 82
    Bugspray : FoleyType # 83
    Scream : FoleyType # 84
    Paper : FoleyType # 85
    Moneyfalls : FoleyType # 86
    Imp : FoleyType # 87
    HydraulicShort : FoleyType # 88
    Hydraulic : FoleyType # 89
    Gargantudeath : FoleyType # 90
    Ceramic : FoleyType # 91
    Bossboulderattack : FoleyType # 92
    Chime : FoleyType # 93
    Crazydaveshort : FoleyType # 94
    Crazydavelong : FoleyType # 95
    Crazydaveextralong : FoleyType # 96
    Crazydavecrazy : FoleyType # 97
    Phonograph : FoleyType # 98
    Dancer : FoleyType # 99
    Finalfanfare : FoleyType # 100
    Crazydavescream : FoleyType # 101
    Crazydavescream2 : FoleyType # 102
    CattailSplat : FoleyType # 103
    ZombieMonkSp : FoleyType # 104
    FoleyCount : FoleyType # 105


class FoleyTypeData:
    def __init__(self) -> None: ...
    mFoleyInstances : Array_1[FoleyInstance]
    mLastVariationPlayed : int


class ParticleEffect(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Melonsplash : ParticleEffect # 0
    Wintermelon : ParticleEffect # 1
    Fumecloud : ParticleEffect # 2
    Popcornsplash : ParticleEffect # 3
    Powie : ParticleEffect # 4
    Jackexplode : ParticleEffect # 5
    ZombieHead : ParticleEffect # 6
    ZombieArm : ParticleEffect # 7
    ZombieTrafficCone : ParticleEffect # 8
    ZombiePail : ParticleEffect # 9
    ZombieHelmet : ParticleEffect # 10
    ZombieFlag : ParticleEffect # 11
    ZombieDoor : ParticleEffect # 12
    ZombieNewspaper : ParticleEffect # 13
    ZombieHeadlight : ParticleEffect # 14
    Pow : ParticleEffect # 15
    ZombiePogo : ParticleEffect # 16
    ZombieNewspaperHead : ParticleEffect # 17
    ZombieBalloonHead : ParticleEffect # 18
    SodRoll : ParticleEffect # 19
    GraveStoneRise : ParticleEffect # 20
    Planting : ParticleEffect # 21
    PlantingPool : ParticleEffect # 22
    ZombieRise : ParticleEffect # 23
    GraveBuster : ParticleEffect # 24
    GraveBusterDie : ParticleEffect # 25
    PoolSplash : ParticleEffect # 26
    IceSparkle : ParticleEffect # 27
    SeedPacket : ParticleEffect # 28
    TallNutBlock : ParticleEffect # 29
    Doom : ParticleEffect # 30
    DiggerRise : ParticleEffect # 31
    DiggerTunnel : ParticleEffect # 32
    DancerRise : ParticleEffect # 33
    PoolSparkly : ParticleEffect # 34
    WallnutEatSmall : ParticleEffect # 35
    WallnutEatLarge : ParticleEffect # 36
    PeaSplat : ParticleEffect # 37
    ButterSplat : ParticleEffect # 38
    CabbageSplat : ParticleEffect # 39
    PuffSplat : ParticleEffect # 40
    StarSplat : ParticleEffect # 41
    IceTrap : ParticleEffect # 42
    SnowpeaSplat : ParticleEffect # 43
    SnowpeaPuff : ParticleEffect # 44
    SnowpeaTrail : ParticleEffect # 45
    LanternShine : ParticleEffect # 46
    SeedPacketPickup : ParticleEffect # 47
    PotatoMine : ParticleEffect # 48
    PotatoMineRise : ParticleEffect # 49
    PuffshroomTrail : ParticleEffect # 50
    PuffshroomMuzzle : ParticleEffect # 51
    SeedPacketFlash : ParticleEffect # 52
    WhackAZombieRise : ParticleEffect # 53
    ZombieLadder : ParticleEffect # 54
    UmbrellaReflect : ParticleEffect # 55
    SeedPacketPick : ParticleEffect # 56
    IceTrapZombie : ParticleEffect # 57
    IceTrapRelease : ParticleEffect # 58
    ZamboniSmoke : ParticleEffect # 59
    Gloomcloud : ParticleEffect # 60
    ZombiePogoHead : ParticleEffect # 61
    ZamboniTire : ParticleEffect # 62
    ZamboniExplosion : ParticleEffect # 63
    ZamboniExplosion2 : ParticleEffect # 64
    CatapultExplosion : ParticleEffect # 65
    MowerCloud : ParticleEffect # 66
    BossIceBall : ParticleEffect # 67
    Blastmark : ParticleEffect # 68
    CoinPickupArrow : ParticleEffect # 69
    PresentPickup : ParticleEffect # 70
    ImitaterMorph : ParticleEffect # 71
    MoweredZombieHead : ParticleEffect # 72
    MoweredZombieArm : ParticleEffect # 73
    ZombieHeadPool : ParticleEffect # 74
    ZombieBossFireball : ParticleEffect # 75
    FireballDeath : ParticleEffect # 76
    IceballDeath : ParticleEffect # 77
    IceballTrail : ParticleEffect # 78
    FireballTrail : ParticleEffect # 79
    BossExplosion : ParticleEffect # 80
    ScreenFlash : ParticleEffect # 81
    TrophySparkle : ParticleEffect # 82
    PortalCircle : ParticleEffect # 83
    PortalSquare : ParticleEffect # 84
    PottedPlantGlow : ParticleEffect # 85
    PottedWaterPlantGlow : ParticleEffect # 86
    PottedZenGlow : ParticleEffect # 87
    MindControl : ParticleEffect # 88
    VaseShatter : ParticleEffect # 89
    VaseShatterLeaf : ParticleEffect # 90
    VaseShatterZombie : ParticleEffect # 91
    AwardPickupArrow : ParticleEffect # 92
    ZombieSeaweed : ParticleEffect # 93
    ZombieMustache : ParticleEffect # 94
    ZombieFutureGlasses : ParticleEffect # 95
    Pinata : ParticleEffect # 96
    DustSquash : ParticleEffect # 97
    DustFoot : ParticleEffect # 98
    Daisy : ParticleEffect # 99
    Starburst : ParticleEffect # 100
    UpsellArrow : ParticleEffect # 101
    ZombieMonkBell : ParticleEffect # 102
    RobotTitanExplosion : ParticleEffect # 103
    PoolSparklyFull : ParticleEffect # 104
    WallnutNewEatLarge : ParticleEffect # 105
    WallnutNewEatSmall : ParticleEffect # 106
    ParticleCount : ParticleEffect # 107
    None_ : ParticleEffect # -1


class ParticleEmitterID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : ParticleEmitterID # 0


class ParticleField:
    def __init__(self) -> None: ...
    mFieldType : ParticleFieldType
    mX : FloatParameterTrack
    mY : FloatParameterTrack


class ParticleFieldType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Invalid : ParticleFieldType # 0
    Friction : ParticleFieldType # 1
    Acceleration : ParticleFieldType # 2
    Attractor : ParticleFieldType # 3
    MaxVelocity : ParticleFieldType # 4
    Velocity : ParticleFieldType # 5
    Position : ParticleFieldType # 6
    SystemPosition : ParticleFieldType # 7
    GroundConstraint : ParticleFieldType # 8
    Shake : ParticleFieldType # 9
    Circle : ParticleFieldType # 10
    Away : ParticleFieldType # 11
    FieldCount : ParticleFieldType # 12


class ParticleFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    RandomLaunchSpin : ParticleFlags # 0
    AlignLaunchSpin : ParticleFlags # 1
    AlignToPixels : ParticleFlags # 2
    SystemLoops : ParticleFlags # 3
    ParticleLoops : ParticleFlags # 4
    ParticlesDontFollow : ParticleFlags # 5
    RandomStartTime : ParticleFlags # 6
    DieIfOverloaded : ParticleFlags # 7
    Additive : ParticleFlags # 8
    Fullscreen : ParticleFlags # 9
    SoftwareOnly : ParticleFlags # 10
    HardwareOnly : ParticleFlags # 11


class ParticleID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : ParticleID # 0


class ParticleParams:
    def __init__(self, aParticleEffect: ParticleEffect, aParticleName: str) -> None: ...
    mParticleEffect : ParticleEffect
    mParticleFileName : str


class ParticleRenderParams:
    mAlpha : float
    mAlphaIsSet : bool
    mBlue : float
    mBlueIsSet : bool
    mGreen : float
    mGreenIsSet : bool
    mParticleScale : float
    mParticleScaleIsSet : bool
    mParticleStretch : float
    mParticleStretchIsSet : bool
    mPositionIsSet : bool
    mPosX : float
    mPosY : float
    mRed : float
    mRedIsSet : bool
    mSpinPosition : float
    mSpinPositionIsSet : bool


class ParticleSystemID(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Null : ParticleSystemID # 0


class ParticleSystemTracks(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    SpawnRate : ParticleSystemTracks # 0
    SpawnMinActive : ParticleSystemTracks # 1
    SpawnMaxActive : ParticleSystemTracks # 2
    SpawnMaxLaunched : ParticleSystemTracks # 3
    EmitterPath : ParticleSystemTracks # 4
    SystemRed : ParticleSystemTracks # 5
    SystemGreen : ParticleSystemTracks # 6
    SystemBlue : ParticleSystemTracks # 7
    SystemAlpha : ParticleSystemTracks # 8
    SystemBrightness : ParticleSystemTracks # 9
    NumSystemTracks : ParticleSystemTracks # 10


class ParticleTracks(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    ParticleRed : ParticleTracks # 0
    ParticleGreen : ParticleTracks # 1
    ParticleBlue : ParticleTracks # 2
    ParticleAlpha : ParticleTracks # 3
    ParticleBrightness : ParticleTracks # 4
    ParticleSpinSpeed : ParticleTracks # 5
    ParticleSpinAngle : ParticleTracks # 6
    ParticleScale : ParticleTracks # 7
    ParticleStretch : ParticleTracks # 8
    ParticleCollisionReflect : ParticleTracks # 9
    ParticleCollisionSpin : ParticleTracks # 10
    ParticleClipTop : ParticleTracks # 11
    ParticleClipBottom : ParticleTracks # 12
    ParticleClipLeft : ParticleTracks # 13
    ParticleClipRight : ParticleTracks # 14
    ParticleAnimationRate : ParticleTracks # 15
    NumParticleTracks : ParticleTracks # 16


class Reanimation:
    _animTime : float
    aBasePoseMatrix : Matrix
    aOverlayMatrix : SexyTransform2D
    Attacher : str
    basePose : SexyTransform2D
    mAction : Reanimation.ReanimLoopAction
    mActive : bool
    mAnimRate : float
    mClip : bool
    mColorOverride : SexyColor
    mDead : bool
    mDefinition : ReanimatorDefinition
    mEnableExtraAdditiveDraw : bool
    mEnableExtraOverlayDraw : bool
    mExtraAdditiveColor : SexyColor
    mExtraOverlayColor : SexyColor
    mFilterEffect : FilterEffectType
    mFrameBasePose : int
    mFrameCount : int
    mFrameStart : int
    mFrameTime : ReanimatorFrameTime
    mGetFrameTime : bool
    mInterpolate : bool
    mIsAttachment : bool
    mIsSpine : bool
    mIsSpine_Save : bool
    mLastFrameTime : float
    mOverlayMatrix : SexyTransform2D
    mReanimationHolder : ReanimationHolder
    mReanimationType : ReanimationType
    mRenderOrder : int
    mSpineAnimationState : AnimationState
    mSpineAnimTrackCount : int
    mSpineBlendTime : int
    mSpineCurrentTrackName : str
    mSpineSkeleton : Skeleton
    mSpineSkeletonRenderer : Dictionary_2[FilterEffectType, SkeletonRenderer]
    mTrackInstances : Array_1[ReanimatorTrackInstance]
    ReanimTrackId__ground : str
    ReanimTrackId_anim_crawl : str
    ReanimTrackId_anim_walk : str
    ReanimTrackId_fullscreen : str
    ReanimTrackIdEmpty : str
    tempOverlayMatrix : Matrix
    @property
    def mAnimTime(self) -> float: ...
    @mAnimTime.setter
    def mAnimTime(self, value: float) -> float: ...
    @property
    def mAnimTime_Save(self) -> clr.Reference[float]: ...
    @property
    def mLoopCount(self) -> int: ...
    @mLoopCount.setter
    def mLoopCount(self, value: int) -> int: ...
    @property
    def mLoopCount_Save(self) -> clr.Reference[int]: ...
    @property
    def mLoopType(self) -> ReanimLoopType: ...
    @mLoopType.setter
    def mLoopType(self, value: ReanimLoopType) -> ReanimLoopType: ...
    @property
    def mLoopType_Save(self) -> clr.Reference[ReanimLoopType]: ...
    def AssignRenderGroupToPrefix(self, theTrackName: str, theRenderGroup: int) -> None: ...
    def AssignRenderGroupToTrack(self, theTrackName: str, theRenderGroup: int) -> None: ...
    def AttacherSynchWalkSpeed(self, theTrackIndex: int, theAttachReanim: clr.Reference[Reanimation], theAttacherInfo: AttacherInfo) -> None: ...
    def AttachParticleToTrack(self, theTrackName: str, theParticleSystem: clr.Reference[TodParticleSystem], thePosX: float, thePosY: float) -> AttachEffect: ...
    def AttachToAnotherReanimation(self, theAttachReanim: clr.Reference[Reanimation], theTrackName: str) -> None: ...
    def Draw(self, g: Graphics, isHardwareClipRequired: bool = ...) -> None: ...
    def DrawRenderGroup(self, g: Graphics, theRenderGroup: int, isHardwareClipRequired: bool = ...) -> None: ...
    def FindSubReanim(self, theReanimType: ReanimationType) -> Reanimation: ...
    def FindTrackIndex(self, theTrackName: str) -> int: ...
    def GetAttachmentOverlayMatrix(self, theTrackIndex: int, theOverlayMatrix: clr.Reference[SexyTransform2D]) -> None: ...
    def GetCurrentTrackImage(self, theTrackName: str) -> Image: ...
    def GetCurrentTransform(self, theTrackIndex: int, aTransformCurrent: clr.Reference[ReanimatorTransform], nullIfInvalidFrame: bool) -> None: ...
    def GetFramesForLayer(self, theTrackName: str, theFrameStart: clr.Reference[int], theFrameCount: clr.Reference[int]) -> None: ...
    def GetFrameTime(self, theFrameTime: clr.Reference[ReanimatorFrameTime]) -> None: ...
    def GetImageOverride(self, theTrackName: str) -> Image: ...
    @staticmethod
    def GetNewReanimation() -> Reanimation: ...
    def GetTrackBasePoseMatrix(self, theTrackIndex: int, theBasePoseMatrix: clr.Reference[SexyTransform2D]) -> None: ...
    def GetTrackIndex(self, theTrackName: str) -> int: ...
    def GetTrackInstanceByName(self, theTrackName: str) -> ReanimatorTrackInstance: ...
    def GetTrackMatrix(self, theTrackIndex: int, theMatrix: clr.Reference[SexyTransform2D]) -> None: ...
    def GetTransformAtTime(self, theTrackIndex: int, aTransform: clr.Reference[ReanimatorTransform], theFrameTime: ReanimatorFrameTime, nullIfInvalidFrame: bool) -> None: ...
    def IsAnimPlaying(self, theTrackName: str) -> bool: ...
    def IsTrackShowing(self, theTrackName: str) -> bool: ...
    @staticmethod
    def MatrixFromTransform(theTransform: ReanimatorTransform, theMatrix: clr.Reference[Matrix]) -> None: ...
    def OverrideScale(self, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def ParseAttacherTrack(theTransform: ReanimatorTransform, theAttacherInfo: clr.Reference[AttacherInfo]) -> None: ...
    def PlayReanim(self, theTrackName: str, theLoopType: ReanimLoopType, theBlendTime: int, theAnimRate: float) -> None: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...
    def PropogateColorToAttachments(self) -> None: ...
    def ReanimationDelete(self) -> None: ...
    def ReanimationDie(self) -> None: ...
    def ReanimationInitialize(self, theX: float, theY: float, theDefinition: int) -> None: ...
    def ReanimationInitializeType(self, theX: float, theY: float, theReanimType: ReanimationType) -> None: ...
    def ReanimationSpineInitialize(self, theX: float, theY: float) -> None: ...
    def ReanimBltMatrix(self, g: Graphics, theImage: Image, theTransform: clr.Reference[Matrix], theClipRect: clr.Reference[TRect], theColor: SexyColor, theDrawMode: Graphics.DrawMode, theSrcRect: TRect, isHardwareClipRequired: bool) -> None: ...
    @staticmethod
    def ReanimSpineInit(g: Graphics, theFilterEffect: FilterEffectType) -> None: ...
    def SetBasePoseFromAnim(self, theTrackName: str) -> None: ...
    def SetFramesForLayer(self, theTrackName: str) -> None: ...
    def SetImageOverride(self, theTrackName: str, theImage: Image) -> None: ...
    def SetPosition(self, theX: float, theY: float) -> None: ...
    def SetShakeOverride(self, theTrackName: str, theShakeAmount: float) -> None: ...
    def SetTruncateDisappearingFrames(self, theTrackName: str, theTruncateDisappearingFrames: bool) -> None: ...
    def ShouldTriggerTimedEvent(self, theEventTime: float) -> bool: ...
    def ShowOnlyTrack(self, theTrackName: str) -> None: ...
    def SpineStartBlend(self, theBlendTime: int) -> None: ...
    def StartBlend(self, theBlendTime: int) -> None: ...
    def TodTriangleGroupDraw(self, g: Graphics, theTriangleGroup: clr.Reference[TodTriangleGroup]) -> None: ...
    @staticmethod
    def ToLower(s: str) -> str: ...
    def ToString(self) -> str: ...
    def TrackExists(self, theTrackName: str) -> bool: ...
    def Update(self) -> None: ...
    def UpdateAttacherTrack(self, theTrackIndex: int) -> None: ...
    # Skipped GetTrackVelocity due to it being static, abstract and generic.

    GetTrackVelocity : GetTrackVelocity_MethodGroup
    class GetTrackVelocity_MethodGroup:
        @typing.overload
        def __call__(self, aTrackIndex: int) -> float:...
        @typing.overload
        def __call__(self, theTrackName: str) -> float:...


    class ReanimLoopAction(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, self: Reanimation, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> bool: ...
        def Invoke(self, self: Reanimation) -> bool: ...



class ReanimationHolder:
    def __init__(self) -> None: ...
    DUMMY : Reanimation
    mReanimations : List_1[Reanimation]
    def AllocReanimation(self, theX: float, theY: float, theRenderOrder: int, theReanimationType: ReanimationType) -> Reanimation: ...
    def DisposeHolder(self) -> None: ...
    def InitializeHolder(self) -> None: ...


class ReanimationParams:
    @typing.overload
    def __init__(self, aReanimationType: ReanimationType, aReanimFilename: str) -> None: ...
    @typing.overload
    def __init__(self, aReanimationType: ReanimationType, aReanimFilename: str, aReanimparamFlags: int) -> None: ...
    @typing.overload
    def __init__(self, aReanimationType: ReanimationType, aReanimFilename: str, aReanimparamFlags: int, isSpine: bool, aOldFilename: str = ..., aSpineScale: float = ...) -> None: ...
    mIsSpine : bool
    mOldFilename : str
    mReanimationType : ReanimationType
    mReanimFileName : str
    mReanimParamFlags : int
    mSpineScale : float


class ReanimationType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LoadbarSprout : ReanimationType # 0
    LoadbarZombiehead : ReanimationType # 1
    Sodroll : ReanimationType # 2
    FinalWave : ReanimationType # 3
    Peashooter : ReanimationType # 4
    Wallnut : ReanimationType # 5
    Lilypad : ReanimationType # 6
    Sunflower : ReanimationType # 7
    Lawnmower : ReanimationType # 8
    Readysetplant : ReanimationType # 9
    Cherrybomb : ReanimationType # 10
    Squash : ReanimationType # 11
    Doomshroom : ReanimationType # 12
    Snowpea : ReanimationType # 13
    Repeater : ReanimationType # 14
    Sunshroom : ReanimationType # 15
    Tallnut : ReanimationType # 16
    Fumeshroom : ReanimationType # 17
    Puffshroom : ReanimationType # 18
    Hypnoshroom : ReanimationType # 19
    Chomper : ReanimationType # 20
    Zombie : ReanimationType # 21
    Sun : ReanimationType # 22
    Potatomine : ReanimationType # 23
    Spikeweed : ReanimationType # 24
    Spikerock : ReanimationType # 25
    Threepeater : ReanimationType # 26
    Marigold : ReanimationType # 27
    Iceshroom : ReanimationType # 28
    ZombieFootball : ReanimationType # 29
    ZombieNewspaper : ReanimationType # 30
    ZombieZamboni : ReanimationType # 31
    Splash : ReanimationType # 32
    Jalapeno : ReanimationType # 33
    JalapenoFire : ReanimationType # 34
    CoinSilver : ReanimationType # 35
    ZombieCharred : ReanimationType # 36
    ZombieCharredImp : ReanimationType # 37
    ZombieCharredDigger : ReanimationType # 38
    ZombieCharredZamboni : ReanimationType # 39
    ZombieCharredCatapult : ReanimationType # 40
    ZombieCharredGargantuar : ReanimationType # 41
    Scrareyshroom : ReanimationType # 42
    Pumpkin : ReanimationType # 43
    Plantern : ReanimationType # 44
    Torchwood : ReanimationType # 45
    Splitpea : ReanimationType # 46
    Seashroom : ReanimationType # 47
    Blover : ReanimationType # 48
    FlowerPot : ReanimationType # 49
    Cactus : ReanimationType # 50
    Disco : ReanimationType # 51
    Tanglekelp : ReanimationType # 52
    Starfruit : ReanimationType # 53
    Polevaulter : ReanimationType # 54
    Balloon : ReanimationType # 55
    Gargantuar : ReanimationType # 56
    Imp : ReanimationType # 57
    Digger : ReanimationType # 58
    DiggerDirt : ReanimationType # 59
    ZombieDolphinrider : ReanimationType # 60
    Pogo : ReanimationType # 61
    BackupDancer : ReanimationType # 62
    Bobsled : ReanimationType # 63
    Jackinthebox : ReanimationType # 64
    Snorkel : ReanimationType # 65
    Bungee : ReanimationType # 66
    Catapult : ReanimationType # 67
    Ladder : ReanimationType # 68
    Puff : ReanimationType # 69
    Sleeping : ReanimationType # 70
    GraveBuster : ReanimationType # 71
    ZombiesWon : ReanimationType # 72
    Magnetshroom : ReanimationType # 73
    Boss : ReanimationType # 74
    Cabbagepult : ReanimationType # 75
    Kernelpult : ReanimationType # 76
    Melonpult : ReanimationType # 77
    Coffeebean : ReanimationType # 78
    Umbrellaleaf : ReanimationType # 79
    Gatlingpea : ReanimationType # 80
    Cattail : ReanimationType # 81
    Gloomshroom : ReanimationType # 82
    BossIceball : ReanimationType # 83
    BossFireball : ReanimationType # 84
    Cobcannon : ReanimationType # 85
    Garlic : ReanimationType # 86
    GoldMagnet : ReanimationType # 87
    WinterMelon : ReanimationType # 88
    TwinSunflower : ReanimationType # 89
    PoolCleaner : ReanimationType # 90
    RoofCleaner : ReanimationType # 91
    FirePea : ReanimationType # 92
    Imitater : ReanimationType # 93
    Yeti : ReanimationType # 94
    BossDriver : ReanimationType # 95
    LawnMoweredZombie : ReanimationType # 96
    CrazyDave : ReanimationType # 97
    TextFadeOn : ReanimationType # 98
    Hammer : ReanimationType # 99
    SlotMachineHandle : ReanimationType # 100
    SelectorScreen : ReanimationType # 101
    PortalCircle : ReanimationType # 102
    PortalSquare : ReanimationType # 103
    ZengardenSprout : ReanimationType # 104
    ZengardenWateringcan : ReanimationType # 105
    ZengardenFertilizer : ReanimationType # 106
    ZengardenBugspray : ReanimationType # 107
    ZengardenPhonograph : ReanimationType # 108
    Diamond : ReanimationType # 109
    Stinky : ReanimationType # 110
    Rake : ReanimationType # 111
    RainCircle : ReanimationType # 112
    RainSplash : ReanimationType # 113
    ZombieSurprise : ReanimationType # 114
    CoinGold : ReanimationType # 115
    ZombieFlagpole : ReanimationType # 116
    Woodsign : ReanimationType # 117
    Astronaut : ReanimationType # 118
    ZombieRobotTitan : ReanimationType # 119
    ZombieMonk : ReanimationType # 120
    ZombieFootballPremium : ReanimationType # 121
    Bushes3 : ReanimationType # 122
    Bushes4 : ReanimationType # 123
    Bushes5 : ReanimationType # 124
    NightBushes3 : ReanimationType # 125
    NightBushes4 : ReanimationType # 126
    NightBushes5 : ReanimationType # 127
    ZombieNinja : ReanimationType # 128
    TreeFood : ReanimationType # 129
    TreeOfWisdom : ReanimationType # 130
    TreeOfWisdomCloud : ReanimationType # 131
    SuperChomper : ReanimationType # 132
    PickledPepper : ReanimationType # 133
    FireShroom : ReanimationType # 134
    Agave : ReanimationType # 135
    AgaveParticle : ReanimationType # 136
    AgaveFullattack : ReanimationType # 137
    ZengardenWateringcanDiamond : ReanimationType # 138
    PumpkinUpper : ReanimationType # 139
    PumpkinLower : ReanimationType # 140
    Endoflame : ReanimationType # 141
    EndoflameSpike : ReanimationType # 142
    EndoflameFullattack : ReanimationType # 143
    SquashWater : ReanimationType # 144
    ZombieTalisman : ReanimationType # 145
    Talisman : ReanimationType # 146
    Zorrose : ReanimationType # 147
    ZombiePropeller : ReanimationType # 148
    NumReanims : ReanimationType # 149
    None_ : ReanimationType # -1


class ReanimAtlas:
    def __init__(self) -> None: ...
    mImageArray : Array_1[ReanimAtlasImage]
    mImageCount : int
    mMemoryImage : MemoryImage
    def AddImage(self, theImage: Image) -> None: ...
    def ArrangeImages(self, theAtlasWidth: clr.Reference[int], theAtlasHeight: clr.Reference[int]) -> None: ...
    def FindImage(self, theImage: Image) -> int: ...
    def GetEncodedReanimAtlas(self, theImage: Image) -> ReanimAtlasImage: ...
    def ImageFindPlace(self, theAtlasImage: ReanimAtlasImage, theImageIndex: int, theMaxWidth: int) -> bool: ...
    def ImageFindPlaceOnSide(self, theAtlasImageToPlace: ReanimAtlasImage, theImageCount: int, theMaxWidth: int, theToRight: bool) -> bool: ...
    def ImageFits(self, theImageCount: int, rectTest: TRect, theMaxWidth: int) -> bool: ...
    def PickAtlasWidth(self) -> int: ...
    def PlaceAtlasImage(self, theAtlasImage: ReanimAtlasImage, theImageIndex: int, theMaxWidth: int) -> bool: ...
    def ReanimAtlasCreate(self, theReanimDef: ReanimatorDefinition) -> None: ...
    def ReanimAtlasDispose(self) -> None: ...


class ReanimAtlasImage:
    def __init__(self) -> None: ...
    mHeight : int
    mOriginalImage : Image
    mWidth : int
    mX : int
    mY : int


class ReanimatorDefinition:
    def __init__(self) -> None: ...
    mFPS : float
    mIsSpine : bool
    mReanimAtlas : ReanimAtlas
    mSpineAtlas : Atlas
    mSpineAtlasPath : str
    mSpineScale : float
    mSpineSkeletonData : SkeletonData
    mTrackCount : int
    mTracks : Array_1[ReanimatorTrack]
    def ExtractImages(self) -> None: ...


class ReanimatorFrameTime:
    mAnimFrameAfterInt : int
    mAnimFrameBeforeInt : int
    mFraction : float


class ReanimatorTrack:
    def __init__(self, name: str, transformCount: int) -> None: ...
    IsAttacher : bool
    mTransformCount : int
    mTransforms : Array_1[ReanimatorTransform]
    @property
    def mName(self) -> str: ...
    @mName.setter
    def mName(self, value: str) -> str: ...
    def ExtractImages(self) -> None: ...
    def ToString(self) -> str: ...


class ReanimatorTrackInstance:
    mAttachmentID : Attachment
    mAttachmentID_Save : int
    mBlendCounter : int
    mBlendTime : int
    mBlendTransform : ReanimatorTransform
    mIgnoreClipRect : bool
    mIgnoreColorOverride : bool
    mIgnoreExtraAdditiveColor : bool
    mImageOverride : Image
    mRenderGroup : int
    mShakeOverride : float
    mShakeX : float
    mShakeY : float
    mTrackColor : SexyColor
    mTruncateDisappearingFrames : bool
    @staticmethod
    def GetNewReanimatorTrackInstance() -> ReanimatorTrackInstance: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...
    def ToString(self) -> str: ...


class ReanimatorTransform:
    def __init__(self) -> None: ...
    mAlpha : float
    mFont : Font
    mFontName : str
    mFrame : float
    mImage : Image
    mImageName : str
    mScaleX : float
    mScaleY : float
    mSkewX : float
    mSkewXCos : float
    mSkewXSin : float
    mSkewY : float
    mSkewYCos : float
    mSkewYSin : float
    mText : str
    mTransX : float
    mTransY : float
    def ExtractImages(self) -> None: ...
    @staticmethod
    def GetNewReanimatorTransform() -> ReanimatorTransform: ...
    @staticmethod
    def GetReanimatorTransformForLoadingThread() -> ReanimatorTransform: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...
    def ToString(self) -> str: ...


class ReanimFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    NoAtlas : ReanimFlags # 0
    FastDrawInSwMode : ReanimFlags # 1


class ReanimLoopType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Loop : ReanimLoopType # 0
    LoopFullLastFrame : ReanimLoopType # 1
    PlayOnce : ReanimLoopType # 2
    PlayOnceAndHold : ReanimLoopType # 3
    PlayOnceFullLastFrame : ReanimLoopType # 4
    PlayOnceFullLastFrameAndHold : ReanimLoopType # 5
    PlayThenAction : ReanimLoopType # 6


class TodCommon(abc.ABC):
    D3DImageFlag_NeedsSanding : int
    DEG_TO_RAD : float
    gAppCloseRequest : TodCommon.gAppCloseRequestDelegate
    gAppHasUsedCheatKeys : TodCommon.gAppHasUsedCheatKeysDelegate
    gExtractResourcesByName : TodCommon.gExtractResourcesByNameDelegate
    gGetCurrentLevelName : TodCommon.gGetCurrentLevelNameDelegate
    gNumGobalAllocators : int
    MAX_GLOBAL_ALLOCATORS : int
    OffsetForGraphicsTranslation : bool
    RAD_TO_DEG : float
    SEXY_RAND_MAX : int
    @staticmethod
    def ClampByte(num: int, minNum: int, maxNum: int) -> int: ...
    @staticmethod
    def ClampFloat(num: float, minNum: float, maxNum: float) -> float: ...
    @staticmethod
    def ClampInt(num: int, minNum: int, maxNum: int) -> int: ...
    @staticmethod
    def ColorAdd(theColor1: SexyColor, theColor2: SexyColor) -> SexyColor: ...
    @staticmethod
    def ColorComponentMultiply(theColor1: int, theColor2: int) -> int: ...
    @staticmethod
    def ColorsMultiply(theColor1: SexyColor, theColor2: SexyColor) -> SexyColor: ...
    @staticmethod
    def DegToRad(theAngle: float) -> float: ...
    @staticmethod
    def Distance2D(x1: float, y1: float, x2: float, y2: float) -> float: ...
    @staticmethod
    def FloatApproxEqual(theFloatValue1: float, theFloatValue2: float) -> bool: ...
    @staticmethod
    def FloatLerp(start: float, end: float, t: float) -> float: ...
    @staticmethod
    def FloatRoundToInt(theFloatValue: float) -> int: ...
    @staticmethod
    def GetFlashingColor(theCounter: int, theFlashTime: int) -> SexyColor: ...
    @staticmethod
    def PixelAligned(num: float) -> float: ...
    @staticmethod
    def RadToDeg(theAngle: float) -> float: ...
    @staticmethod
    def RandRangeFloat(theMin: float, theMax: float) -> float: ...
    @staticmethod
    def RandRangeInt(theMin: int, theMax: int) -> int: ...
    @staticmethod
    def SetBit(theNumber: clr.Reference[int], theBitIndex: int, theValue: int) -> None: ...
    @staticmethod
    def SexyMatrix3ExtractScale(m: Matrix, theScaleX: clr.Reference[float], theScaleY: clr.Reference[float]) -> None: ...
    @staticmethod
    def SexyMatrix3Inverse(mat: clr.Reference[Matrix], r: clr.Reference[Matrix]) -> None: ...
    @staticmethod
    def SexyMatrix3Multiply(m: clr.Reference[Matrix], l: Matrix, r: Matrix) -> None: ...
    @staticmethod
    def SexyMatrix3Translation(m: clr.Reference[Matrix], x: float, y: float) -> None: ...
    @staticmethod
    def SexyMatrix3Transpose(m: Matrix, r: clr.Reference[Matrix]) -> None: ...
    @staticmethod
    def TestBit(theNumber: int, theBitIndex: int) -> bool: ...
    @staticmethod
    def TodAnimateCurve(theTimeStart: int, theTimeEnd: int, theTimeAge: int, thePositionStart: int, thePositionEnd: int, theCurve: TodCurves) -> int: ...
    @staticmethod
    def TodAnimateCurveFloat(theTimeStart: int, theTimeEnd: int, theTimeAge: int, thePositionStart: float, thePositionEnd: float, theCurve: TodCurves) -> float: ...
    @staticmethod
    def TodAnimateCurveFloatTime(theTimeStart: float, theTimeEnd: float, theTimeAge: float, thePositionStart: float, thePositionEnd: float, theCurve: TodCurves) -> float: ...
    @staticmethod
    def TodAppCloseRequest() -> bool: ...
    @staticmethod
    def TodAppHasUsedCheatKeys() -> bool: ...
    @staticmethod
    def TodCalcSmoothWeight(aWeight: float, aLastPicked: float, aSecondLastPicked: float) -> float: ...
    @staticmethod
    def TodCurveBounce(theTime: float) -> float: ...
    @staticmethod
    def TodCurveCircle(theTime: float) -> float: ...
    @staticmethod
    def TodCurveCubic(theTime: float) -> float: ...
    @staticmethod
    def TodCurveCubicS(theTime: float) -> float: ...
    @staticmethod
    def TodCurveEvaluate(theTime: float, thePositionStart: float, thePositionEnd: float, theCurve: TodCurves) -> float: ...
    @staticmethod
    def TodCurveEvaluateClamped(theTime: float, thePositionStart: float, thePositionEnd: float, theCurve: TodCurves) -> float: ...
    @staticmethod
    def TodCurveInvCircle(theTime: float) -> float: ...
    @staticmethod
    def TodCurveInvCubic(theTime: float) -> float: ...
    @staticmethod
    def TodCurveInvPoly(theTime: float, thePoly: float) -> float: ...
    @staticmethod
    def TodCurveInvQuad(theTime: float) -> float: ...
    @staticmethod
    def TodCurveInvQuadS(theTime: float) -> float: ...
    @staticmethod
    def TodCurvePoly(theTime: float, thePoly: float) -> float: ...
    @staticmethod
    def TodCurvePolyS(theTime: float, thePoly: float) -> float: ...
    @staticmethod
    def TodCurveQuad(theTime: float) -> float: ...
    @staticmethod
    def TodCurveQuadS(theTime: float) -> float: ...
    @staticmethod
    def TodCurveS(theTime: float) -> float: ...
    @staticmethod
    def TodDrawImageCelCenterScaledF(g: Graphics, theImageStrip: Image, thePosX: float, thePosY: float, theCelCol: int, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def TodDrawImageCelF(g: Graphics, theImageStrip: Image, thePosX: float, thePosY: float, theCelCol: int, theCelRow: int) -> None: ...
    @staticmethod
    def TodDrawImageCelScaled(g: Graphics, theImageStrip: Image, thePosX: int, thePosY: int, theCelCol: int, theCelRow: int, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def TodDrawImageCelScaledF(g: Graphics, theImageStrip: Image, thePosX: float, thePosY: float, theCelCol: int, theCelRow: int, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def TodDrawImageScaledF(g: Graphics, theImage: Image, thePosX: float, thePosY: float, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def TodDrawStringCenterBy(g: Graphics, theText: str, thePosX: int, thePosY: int, theFont: Font, theColor: SexyColor, theJustification: DrawStringJustification, scale: float, centerString: str) -> None: ...
    @staticmethod
    def TodDrawStringLayer(g: Graphics, theText: str, thePosX: int, thePosY: int, theFont: Font, theColor: SexyColor, theJustification: DrawStringJustification, scale: float, layer: int) -> None: ...
    @staticmethod
    def TodDrawStringMatrix(g: Graphics, theFont: Font, theMatrix: Matrix, theString: str, theColor: SexyColor) -> None: ...
    @staticmethod
    def TodFindImagePath(theImage: Image, thePath: clr.Reference[str]) -> bool: ...
    @staticmethod
    def TodGetCurrentLevelName() -> str: ...
    @staticmethod
    def TodIsPointInPolygon(thePolygonPoint: Array_1[SexyVector2], theNumberPolygonPoints: int, theCheckPoint: SexyVector2) -> bool: ...
    @staticmethod
    def TodLoadNextResource() -> bool: ...
    @staticmethod
    def TodPickArrayItemFromWeightedArray(theArray: Array_1[TodWeightedArray], theCount: int) -> TodWeightedArray: ...
    @staticmethod
    def TodPickFromArray(theArray: Array_1[int], theCount: int) -> int: ...
    @staticmethod
    def TodPickFromSmoothArray(theArray: Array_1[TodSmoothArray], theCount: int) -> int: ...
    @staticmethod
    def TodPickFromWeightedArray(theArray: Array_1[TodWeightedArray], theCount: int) -> typing.Any: ...
    @staticmethod
    def TodPickFromWeightedGridArray(theArray: Array_1[TodWeightedGridArray], theCount: int) -> TodWeightedGridArray: ...
    @staticmethod
    def TodReplaceNumberString(theText: str, theStringToFind: str, theNumber: int) -> str: ...
    @staticmethod
    def TodReplaceString(theText: str, theStringToFind: str, theStringToSubstitute: str) -> str: ...
    @staticmethod
    def TodScaleRotateTransformMatrix(m: clr.Reference[Matrix], x: float, y: float, rad: float, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def TodScaleTransformMatrix(m: clr.Reference[Matrix], x: float, y: float, theScaleX: float, theScaleY: float) -> None: ...
    @staticmethod
    def TodUpdateSmoothArrayPick(theArray: Array_1[TodSmoothArray], theCount: int, thePickIndex: int) -> None: ...
    # Skipped TodBltMatrix due to it being static, abstract and generic.

    TodBltMatrix : TodBltMatrix_MethodGroup
    class TodBltMatrix_MethodGroup:
        @typing.overload
        def __call__(self, g: Graphics, theImage: Image, theTransform: Matrix, theClipRect: clr.Reference[TRect], theColor: SexyColor, theDrawMode: Graphics.DrawMode, theSrcRect: TRect) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, theImage: Image, theTransform: clr.Reference[Matrix], theClipRect: TRect, theColor: SexyColor, theDrawMode: Graphics.DrawMode, theSrcRect: TRect, clip: bool) -> None:...

    # Skipped TodDrawImageCenterScaledF due to it being static, abstract and generic.

    TodDrawImageCenterScaledF : TodDrawImageCenterScaledF_MethodGroup
    class TodDrawImageCenterScaledF_MethodGroup:
        @typing.overload
        def __call__(self, g: Graphics, theImage: Image, thePosX: float, thePosY: float, theScaleX: float, theScaleY: float) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, theImage: Image, thePosX: float, thePosY: float, theScaleX: float, theScaleY: float, cel: int, doTexelOffset: bool) -> None:...

    # Skipped TodDrawString due to it being static, abstract and generic.

    TodDrawString : TodDrawString_MethodGroup
    class TodDrawString_MethodGroup:
        @typing.overload
        def __call__(self, g: Graphics, theText: str, thePosX: int, thePosY: int, theFont: Font, theColor: SexyColor, theJustification: DrawStringJustification) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, theText: str, thePosX: int, thePosY: int, theFont: Font, theColor: SexyColor, maxWidth: int, theJustification: DrawStringJustification) -> None:...
        @typing.overload
        def __call__(self, g: Graphics, theText: str, thePosX: int, thePosY: int, theFont: Font, theColor: SexyColor, theJustification: DrawStringJustification, scale: float) -> None:...

    # Skipped TodLoadResources due to it being static, abstract and generic.

    TodLoadResources : TodLoadResources_MethodGroup
    class TodLoadResources_MethodGroup:
        @typing.overload
        def __call__(self, theGroup: str) -> bool:...
        @typing.overload
        def __call__(self, theGroup: str, doUnpackAtlasImages: bool) -> bool:...


    class gAppCloseRequestDelegate(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> bool: ...
        def Invoke(self) -> bool: ...


    class gAppHasUsedCheatKeysDelegate(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> bool: ...
        def Invoke(self) -> bool: ...


    class gExtractResourcesByNameDelegate(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, theManager: ResourceManager, theName: str, doUnpackAtlasImages: bool, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> bool: ...
        def Invoke(self, theManager: ResourceManager, theName: str, doUnpackAtlasImages: bool) -> bool: ...


    class gGetCurrentLevelNameDelegate(MulticastDelegate):
        def __init__(self, object: typing.Any, method: int) -> None: ...
        @property
        def Method(self) -> MethodInfo: ...
        @property
        def Target(self) -> typing.Any: ...
        def BeginInvoke(self, callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
        def EndInvoke(self, result: IAsyncResult) -> str: ...
        def Invoke(self) -> str: ...



class TodCurves(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Constant : TodCurves # 0
    Linear : TodCurves # 1
    EaseIn : TodCurves # 2
    EaseOut : TodCurves # 3
    EaseInOut : TodCurves # 4
    EaseInOutWeak : TodCurves # 5
    FastInOut : TodCurves # 6
    FastInOutWeak : TodCurves # 7
    WeakFastInOut : TodCurves # 8
    Bounce : TodCurves # 9
    BounceFastMiddle : TodCurves # 10
    BounceSlowMiddle : TodCurves # 11
    SinWave : TodCurves # 12
    EaseSinWave : TodCurves # 13


class TodEmitterDefinition:
    def __init__(self) -> None: ...
    mAnimated : int
    mAnimationRate : FloatParameterTrack
    mClipBottom : FloatParameterTrack
    mClipLeft : FloatParameterTrack
    mClipRight : FloatParameterTrack
    mClipTop : FloatParameterTrack
    mCollisionReflect : FloatParameterTrack
    mCollisionSpin : FloatParameterTrack
    mCrossFadeDuration : FloatParameterTrack
    mEmitterBoxX : FloatParameterTrack
    mEmitterBoxY : FloatParameterTrack
    mEmitterOffsetX : FloatParameterTrack
    mEmitterOffsetY : FloatParameterTrack
    mEmitterPath : FloatParameterTrack
    mEmitterRadius : FloatParameterTrack
    mEmitterSkewX : FloatParameterTrack
    mEmitterSkewY : FloatParameterTrack
    mEmitterType : EmitterType
    mImage : Image
    mImageCol : int
    mImageFrames : int
    mImageRow : int
    mLaunchAngle : FloatParameterTrack
    mLaunchSpeed : FloatParameterTrack
    mName : str
    mOnDuration : str
    mParticleAlpha : FloatParameterTrack
    mParticleBlue : FloatParameterTrack
    mParticleBrightness : FloatParameterTrack
    mParticleDuration : FloatParameterTrack
    mParticleFieldCount : int
    mParticleFields : Array_1[ParticleField]
    mParticleFlags : int
    mParticleGreen : FloatParameterTrack
    mParticleRed : FloatParameterTrack
    mParticleScale : FloatParameterTrack
    mParticleSpinAngle : FloatParameterTrack
    mParticleSpinSpeed : FloatParameterTrack
    mParticleStretch : FloatParameterTrack
    mSpawnMaxActive : FloatParameterTrack
    mSpawnMaxLaunched : FloatParameterTrack
    mSpawnMinActive : FloatParameterTrack
    mSpawnRate : FloatParameterTrack
    mSystemAlpha : FloatParameterTrack
    mSystemBlue : FloatParameterTrack
    mSystemBrightness : FloatParameterTrack
    mSystemDuration : FloatParameterTrack
    mSystemFieldCount : int
    mSystemFields : Array_1[ParticleField]
    mSystemGreen : FloatParameterTrack
    mSystemRed : FloatParameterTrack
    def Dispose(self) -> None: ...


class TodFoley:
    def __init__(self) -> None: ...
    gFoleyParamArray : Array_1[FoleyParams]
    gFoleyParamArraySize : int
    mFoleyTypeData : Array_1[FoleyTypeData]
    def ApplyMusicVolume(self, theFoleyInstance: FoleyInstance) -> None: ...
    def CancelPausedFoley(self) -> None: ...
    def GamePause(self, theEnteringPause: bool) -> None: ...
    def IsFoleyPlaying(self, theFoleyType: FoleyType) -> bool: ...
    @staticmethod
    def LookupFoley(theFoleyType: FoleyType) -> FoleyParams: ...
    def PlayFoley(self, theFoleyType: FoleyType) -> None: ...
    def PlayFoleyPitch(self, theFoleyType: FoleyType, aPitch: float) -> None: ...
    def RehookupSoundWithMusicVolume(self) -> None: ...
    @staticmethod
    def SoundSystemFindInstance(theSoundSystem: TodFoley, theFoleyType: FoleyType) -> FoleyInstance: ...
    @staticmethod
    def SoundSystemGetFreeInstanceIndex(theSoundSystem: TodFoley, theFoleyType: FoleyType) -> FoleyInstance: ...
    @staticmethod
    def SoundSystemHasFoleyPlayedTooRecently(theSoundSystem: TodFoley, theFoleyType: FoleyType) -> bool: ...
    @staticmethod
    def SoundSystemReleaseFinishedInstances(theSoundSystem: TodFoley) -> None: ...
    def StopFoley(self, theFoleyType: FoleyType) -> None: ...
    @staticmethod
    def TodFoleyDispose() -> None: ...
    @staticmethod
    def TodFoleyInitialize(theFoleyParamArray: Array_1[FoleyParams], theFoleyParamArraySize: int) -> None: ...


class TodParticle:
    mAnimationTimeValue : float
    mCrossFadeDuration : int
    mCrossFadeParticleID : TodParticle
    mCrossFadeParticleID_Save : int
    mImageFrame : int
    mParticleAge : int
    mParticleDuration : int
    mParticleEmitter : TodParticleEmitter
    mParticleEmitter_Save : int
    mParticleFieldInterp : Array_1[float]
    mParticleInterp : Array_1[float]
    mParticleLastTimeValue : float
    mParticleTimeValue : float
    mPosition : SexyVector2
    mSpinPosition : float
    mSpinVelocity : float
    mVelocity : SexyVector2
    @staticmethod
    def GetNewTodParticle() -> TodParticle: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...


class TodParticleDefinition:
    def __init__(self) -> None: ...
    mEmitterDefCount : int
    mEmitterDefs : Array_1[TodEmitterDefinition]


class TodParticleEmitter:
    mActive : bool
    mColorOverride : SexyColor
    mCrossFadeEmitterID : TodParticleEmitter
    mCrossFadeEmitterID_Save : int
    mDead : bool
    mEmitterCrossFadeCountDown : int
    mEmitterDef : TodEmitterDefinition
    mEmitterDef_Save : int
    mExtraAdditiveDrawOverride : bool
    mFrameOverride : int
    mImageOverride : Image
    mParticleList : List_1[TodParticle]
    mParticlesSpawned : int
    mParticleSystem : TodParticleSystem
    mParticleSystem_Save : int
    mScaleOverride : float
    mSpawnAccum : float
    mSystemAge : int
    mSystemCenter : SexyVector2
    mSystemDuration : int
    mSystemFieldInterp : Array_1[float]
    mSystemLastTimeValue : float
    mSystemTimeValue : float
    mTrackInterp : Array_1[float]
    def CrossFadeEmitter(self, theToEmitter: TodParticleEmitter) -> None: ...
    def CrossFadeParticle(self, theParticle: TodParticle, theToEmitter: TodParticleEmitter) -> bool: ...
    def CrossFadeParticleToName(self, theParticle: TodParticle, theEmitterName: str) -> bool: ...
    def DeleteAll(self) -> None: ...
    def DeleteNonCrossFading(self) -> None: ...
    def DeleteParticle(self, theParticle: TodParticle) -> None: ...
    def Draw(self, g: Graphics, doScale: bool) -> None: ...
    def DrawParticle(self, g: Graphics, theParticle: TodParticle, doScale: bool) -> None: ...
    @staticmethod
    def GetNewTodParticleEmitter() -> TodParticleEmitter: ...
    @staticmethod
    def GetRenderParams(theParticle: TodParticle, theParams: clr.Reference[ParticleRenderParams]) -> bool: ...
    def ParticleTrackEvaluate(self, theTrack: clr.Reference[FloatParameterTrack], theParticle: TodParticle, theInterp: ParticleTracks) -> float: ...
    @staticmethod
    def PreallocateMemory() -> None: ...
    def PrepareForReuse(self) -> None: ...
    def SpawnParticle(self, theIndex: int, theSpawnCount: int) -> TodParticle: ...
    def SystemMove(self, theX: float, theY: float) -> None: ...
    def SystemMoveBy(self, theX: float, theY: float) -> None: ...
    def SystemTrackEvaluate(self, theTrack: clr.Reference[FloatParameterTrack], theInterp: ParticleSystemTracks) -> float: ...
    def TodEmitterInitialize(self, theX: float, theY: float, theSystem: TodParticleSystem, theEmitterDef: TodEmitterDefinition) -> None: ...
    def Update(self) -> None: ...
    def UpdateParticle(self, theParticle: TodParticle) -> bool: ...
    def UpdateParticleField(self, theParticle: TodParticle, theParticleField: ParticleField, theParticleTimeValue: float, theFieldIndex: int) -> None: ...
    def UpdateSpawning(self) -> None: ...
    def UpdateSystemField(self, theParticleField: ParticleField, theParticleTimeValue: float, theFieldIndex: int) -> None: ...


class TodParticleHolder:
    def __init__(self) -> None: ...
    mEmitters : List_1[TodParticleEmitter]
    mParticles : List_1[TodParticle]
    mParticleSystems : List_1[TodParticleSystem]
    def AllocParticleSystem(self, theX: float, theY: float, theRenderOrder: int, theParticleEffect: ParticleEffect) -> TodParticleSystem: ...
    def AllocParticleSystemFromDef(self, theX: float, theY: float, theRenderOrder: int, theDefinition: TodParticleDefinition, theParticleEffect: ParticleEffect) -> TodParticleSystem: ...
    def Dispose(self) -> None: ...
    def DisposeHolder(self) -> None: ...
    def InitializeHolder(self) -> None: ...
    def IsOverLoaded(self) -> bool: ...


class TodParticleSystem:
    mActive : bool
    mDead : bool
    mDontUpdate : bool
    mEffectType : ParticleEffect
    mEmitterList : List_1[TodParticleEmitter]
    mIsAttachment : bool
    mParticleDef : TodParticleDefinition
    mParticleHolder : TodParticleHolder
    mRenderOrder : int
    def CrossFade(self, theCrossFadeEmitter: str) -> None: ...
    def Dispose(self) -> None: ...
    def Draw(self, g: Graphics, doScale: bool) -> None: ...
    def FindEmitterByName(self, theEmitterName: str) -> TodParticleEmitter: ...
    def FindEmitterDefByName(self, theEmitterName: str) -> TodEmitterDefinition: ...
    @staticmethod
    def GetNewTodParticleSystem() -> TodParticleSystem: ...
    def OverrideColor(self, theEmitterName: str, theColor: SexyColor) -> None: ...
    def OverrideExtraAdditiveDraw(self, theEmitterName: str, theEnableExtraAdditiveDraw: bool) -> None: ...
    def OverrideFrame(self, theEmitterName: str, theFrame: int) -> None: ...
    def OverrideImage(self, theEmitterName: str, theImage: Image) -> None: ...
    def OverrideScale(self, theEmitterName: str, theScale: float) -> None: ...
    def ParticleSystemDie(self) -> None: ...
    def PrepareForReuse(self) -> None: ...
    def SystemMove(self, theX: float, theY: float) -> None: ...
    def SystemMoveBy(self, theX: float, theY: float) -> None: ...
    def TodParticleInitializeFromDef(self, theX: float, theY: float, theRenderOrder: int, theDefinition: TodParticleDefinition, theEffectType: ParticleEffect) -> None: ...
    def Update(self) -> None: ...


class TodSmoothArray:
    def __init__(self) -> None: ...
    mItem : int
    mLastPicked : float
    mSecondLastPicked : float
    mWeight : float
    def LoadFromFile(self, b: Buffer) -> bool: ...
    def SaveToFile(self, b: Buffer) -> bool: ...


class TodStringFormatFlag(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    IgnoreNewlines : TodStringFormatFlag # 0
    HideUntilMagnetshroom : TodStringFormatFlag # 1


class TodStringListFormat:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, aFormatName: str, aNewFont: Font, aNewColor: SexyColor, aLineSpacingOffset: int, aFormatFlags: int) -> None: ...
    mBaseColor : SexyColor
    mFormatFlags : int
    mFormatName : str
    mLineSpacingOffset : int
    mNewColor : SexyColor
    mNewFont : Font
    def Reset(self) -> None: ...


class TodTriangleGroup:
    gTodTriangleDrawAdditive : bool
    def AddTriangle(self, g: Graphics, theImage: Image, theTransform: ReanimatorTransform, theClipRect: TRect, theColor: SexyColor, theDrawMode: Graphics.DrawMode, theSrcRect: TRect) -> None: ...
    def DrawGroup(self, g: Graphics) -> None: ...
    @staticmethod
    def GetNewTodTriangleGroup() -> TodTriangleGroup: ...
    def PrepareForReuse(self) -> None: ...


class TodWeightedArray:
    mItem : typing.Any
    mWeight : int
    @staticmethod
    def GetNewTodWeightedArray() -> TodWeightedArray: ...
    def PrepareForReuse(self) -> None: ...
    def Reset(self) -> None: ...


class TodWeightedGridArray:
    mWeight : int
    mX : int
    mY : int
    @staticmethod
    def GetNewTodWeightedGridArray() -> TodWeightedGridArray: ...
    def PrepareForReuse(self) -> None: ...
    def Reset(self) -> None: ...


class Trail:
    def __init__(self) -> None: ...
    mColorOverride : SexyColor
    mDead : bool
    mDefinition : TrailDefinition
    mIsAttachment : bool
    mNumTrailPoints : int
    mRenderOrder : int
    mTrailAge : int
    mTrailCenter : SexyVector2
    mTrailDuration : int
    mTrailHolder : TrailHolder
    mTrailInterp : Array_1[float]
    mTrailPoints : Array_1[TrailPoint]
    def AddPoint(self, x: float, y: float) -> None: ...
    def Draw(self, g: Graphics) -> None: ...
    def GetNormalAtPoint(self, nIndex: int, theNormal: clr.Reference[SexyVector2]) -> bool: ...
    def Update(self) -> None: ...


class TrailDefinition:
    def __init__(self) -> None: ...
    mAlphaOverLength : FloatParameterTrack
    mAlphaOverTime : FloatParameterTrack
    mImage : Image
    mImageName : str
    mImages : Array_1[Image]
    mMaxPoints : int
    mMinPointDistance : float
    mNumImages : int
    mTrailDuration : FloatParameterTrack
    mTrailFlags : int
    mWidthOverLength : FloatParameterTrack
    mWidthOverTime : FloatParameterTrack
    def Dispose(self) -> None: ...
    def ExtractImages(self) -> None: ...


class TrailFlags(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Loops : TrailFlags # 1


class TrailHolder:
    def __init__(self) -> None: ...
    mTrails : List_1[Trail]
    def AllocTrail(self, theRenderOrder: int, theTrailType: TrailType) -> Trail: ...
    def AllocTrailFromDef(self, theRenderOrder: int, theDefinition: TrailDefinition) -> Trail: ...
    def Dispose(self) -> None: ...
    def DisposeHolder(self) -> None: ...
    def InitializeHolder(self) -> None: ...


class TrailParams:
    def __init__(self, aTrailType: TrailType, aTrailFileName: str) -> None: ...
    mTrailFileName : str
    mTrailType : TrailType


class TrailPoint:
    def __init__(self) -> None: ...
    aPos : SexyVector2


class TrailTracks(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    WidthOverLength : TrailTracks # 0
    WidthOverTime : TrailTracks # 1
    AlphaOverLength : TrailTracks # 2
    AlphaOverTime : TrailTracks # 3
    NumTrailTracks : TrailTracks # 4


class TrailType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Ice : TrailType # 0
    Cattail : TrailType # 1
    Endoflame : TrailType # 2
    NumTrails : TrailType # 3
    None_ : TrailType # -1

