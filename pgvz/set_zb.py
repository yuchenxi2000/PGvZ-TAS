import Lawn
import Sexy
import System
import clr  # type: ignore
clr.AddReference("MonoMod.RuntimeDetour")
clr.AddReference("MonoMod.Utils")
clr.AddReference("Mono.Cecil")
import MonoMod.RuntimeDetour
import MonoMod.Cil  # type: ignore
from Mono.Cecil.Cil import OpCodes  # type: ignore
from .util import GetBoard


def InitNaturalZombieWaves(board: Lawn.Board, zb_list: 'list[Lawn.ZombieType]') -> None:
    candidates = [int(zb) for zb in zb_list]

    def next_int(ceiling):
        # 只控制候选种类抽取，不能把种类编号送给波次权重或其他随机调用。
        if ceiling == int(Lawn.ZombieType.ZombieTypesCount) and candidates:
            return candidates.pop(0)
        return Sexy.RandomNumbers.NextNumber.Overloads[System.Int32](ceiling)  # type: ignore

    def next_float(ceiling):
        # 生存模式的路障/报纸二选一使用 Single 重载，不占用种类抽取队列。
        if ceiling == 5.0:
            return 0.0 if Lawn.ZombieType.Newspaper in zb_list else 1.0
        return Sexy.RandomNumbers.NextNumber.Overloads[System.Single](ceiling)  # type: ignore

    int_delegate = System.Func[System.Int32, System.Int32](next_int)  # type: ignore
    float_delegate = System.Func[System.Single, System.Single](next_float)  # type: ignore

    def replace_random_calls(il):
        cursor = MonoMod.Cil.ILCursor(il)
        for instruction in list(il.Body.Instructions):
            if instruction.OpCode != OpCodes.Call:
                continue
            method = instruction.Operand
            if (method.DeclaringType.FullName != 'Sexy.RandomNumbers'
                    or method.Name != 'NextNumber' or method.Parameters.Count != 1):
                continue
            param_type = method.Parameters[0].ParameterType.FullName
            if param_type == 'System.Int32':
                delegate = int_delegate
                delegate_type = System.Func[System.Int32, System.Int32]
            elif param_type == 'System.Single':
                delegate = float_delegate
                delegate_type = System.Func[System.Single, System.Single]
            else:
                continue
            cursor.Goto(instruction)
            cursor.Remove()
            cursor.EmitDelegate[delegate_type](delegate)

    # 直接改写较大的调用者，避免 NextNumber 已被 JIT 内联而绕过随机数钩子。
    challenge_type = System.Reflection.Assembly.GetAssembly(Lawn.Challenge).GetType('Lawn.Challenge')  # type: ignore
    hooks = []
    try:
        for name in ('InitZombieWavesSurvival', 'InitZombieWavesChallengStageRandom'):
            hooks.append(MonoMod.RuntimeDetour.ILHook(  # type: ignore
                challenge_type.GetMethod(name), MonoMod.Cil.ILContext.Manipulator(replace_random_calls)))
        board.InitZombieWaves()
    finally:
        for hook in reversed(hooks):
            hook.Dispose()


def SetZombies(zb_list: 'list[Lawn.ZombieType]', internal_spawn: bool = True) -> None:
    board = GetBoard()
    if internal_spawn:
        InitNaturalZombieWaves(board, zb_list)
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
