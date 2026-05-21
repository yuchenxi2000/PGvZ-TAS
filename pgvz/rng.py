import Sexy
import LawnMod
import System
import clr  # type: ignore
clr.AddReference("MonoMod.RuntimeDetour")
import System.Reflection
import MonoMod.RuntimeDetour

class RNGManip:
    def __init__(self) -> None:
        self.enabled = False
        self.next_rand = []  # type: list[int | float]

rng_manip = RNGManip()

# 这玩意儿还有重载，真难搞。。。
@LawnMod.MonoModUtils.As(Sexy.RandomNumbers.NextNumber.Overloads[()])  # type: ignore
def RandomNumbers__NextNumber(orig):
    if rng_manip.enabled:
        try:
            rng = rng_manip.next_rand.pop(0)
            Sexy.Debug.Log(f'maniped rng: {rng}')
            return rng
        except IndexError:
            return orig()
    else:
        return orig()

@LawnMod.MonoModUtils.As(Sexy.RandomNumbers.NextNumber.Overloads[System.Int32])  # type: ignore
def RandomNumbers__NextNumber2(orig, n):
    if rng_manip.enabled:
        try:
            rng = rng_manip.next_rand.pop(0)
            Sexy.Debug.Log(f'maniped rng: {rng}')
            return rng
        except IndexError:
            return orig(n)
    else:
        return orig(n)

assembly = System.Reflection.Assembly.GetAssembly(Sexy.RandomNumbers)
rng_type = assembly.GetType("Sexy.RandomNumbers")

method1 = rng_type.GetMethod("NextNumber", ())
method2 = rng_type.GetMethod("NextNumber", (System.Int32, ))

hook1 = MonoMod.RuntimeDetour.Hook(method1, RandomNumbers__NextNumber)  # type: ignore
hook2 = MonoMod.RuntimeDetour.Hook(method2, RandomNumbers__NextNumber2)  # type: ignore
