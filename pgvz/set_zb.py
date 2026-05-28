import Lawn
import Sexy
from .rng import rng_manip

def SetZombies(zb_list, internal_spawn: bool = True):  # type: (list[Lawn.ZombieType], bool) -> None
    if internal_spawn:
        # enable RNG manipulation
        rng_manip.enabled = True
        # set RNG list
        rng_list = []
        if Lawn.ZombieType.Newspaper in zb_list:
            rng_list.append(0)
        else:
            rng_list.append(1)
        for zb in zb_list:
            rng_list.append(int(zb))
        rng_manip.next_rand = rng_list
        Sexy.Debug.Log(f'rng list: {rng_list}')
        # init zombies
        Sexy.GlobalStaticVars.gLawnApp.mBoard.InitZombieWaves()
        # disable RNG manipulation
        rng_manip.enabled = False
    else:
        for i in range(40):
            Sexy.GlobalStaticVars.gLawnApp.mBoard.mZombieAllowed[i] = False
        for zb in zb_list:
            Sexy.GlobalStaticVars.gLawnApp.mBoard.mZombieAllowed[int(zb)] = True
        Sexy.GlobalStaticVars.gLawnApp.mBoard.mZombieAllowed[0] = True
        Sexy.GlobalStaticVars.gLawnApp.mBoard.PickZombieWaves()
    # reset zombie preview
    Sexy.GlobalStaticVars.gLawnApp.mBoard.RemoveCutsceneZombies()
    Sexy.GlobalStaticVars.gLawnApp.mBoard.mCutScene.mPlacedZombies = False
