import Lawn
import Sexy
from .rng import rng_manip
from .util import GetBoard

def SetZombies(zb_list: 'list[Lawn.ZombieType]', internal_spawn: bool = True) -> None:
    board = GetBoard()
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
        board.InitZombieWaves()
        # disable RNG manipulation
        rng_manip.enabled = False
    else:
        for i in range(40):
            board.mZombieAllowed[i] = False
        for zb in zb_list:
            board.mZombieAllowed[int(zb)] = True
        board.mZombieAllowed[0] = True
        board.PickZombieWaves()
    # reset zombie preview
    board.RemoveCutsceneZombies()
    board.mCutScene.mPlacedZombies = False
