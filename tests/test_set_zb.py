"""Natural spawning keeps game filters and scopes RNG overrides to candidate draws."""
import ast
import enum
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ZombieType(enum.IntEnum):
    Normal = 0
    Flag = 1
    TrafficCone = 2
    Newspaper = 5
    Football = 7
    Zamboni = 12
    ZombieTypesCount = 40


class Generic:
    def __getitem__(self, key):
        return DelegateType(key)


class DelegateType:
    def __init__(self, parameters):
        self.parameters = parameters

    def __call__(self, callback):
        return callback


class Emitter:
    def __init__(self, il):
        self.il = il

    def __getitem__(self, delegate_type):
        def emit(callback):
            self.il.delegates[delegate_type.parameters[0]] = callback
        return emit


class Parameters(list):
    @property
    def Count(self):
        return len(self)


def instruction(owner, name, param=None):
    return types.SimpleNamespace(OpCode='call', Operand=types.SimpleNamespace(
        DeclaringType=types.SimpleNamespace(FullName=owner), Name=name,
        Parameters=Parameters([] if param is None else [types.SimpleNamespace(
            ParameterType=types.SimpleNamespace(FullName=param))])))


class Cursor:
    def __init__(self, il):
        self.il = il
        self.EmitDelegate = Emitter(il)

    def Goto(self, instruction):
        pass

    def Remove(self):
        pass


class SetZombiesTests(unittest.TestCase):
    def setUp(self):
        self.active = {}
        self.disposed = []
        self.install_fail = False
        self.game_fail = False
        self.mode = 'InitZombieWavesSurvival'
        self.stage = 2049  # 4098 completed flags in pool endless.
        self.filler_index = 0
        self.random_calls = []

        def original_int(ceiling):
            self.random_calls.append(('int', ceiling))
            if ceiling != 40:
                return ceiling - 1
            fillers = [3, 4, 6, 7, 8, 11, 14, 15, 16, 17, 18, 21, 22, 23]
            result = fillers[self.filler_index % len(fillers)]
            self.filler_index += 1
            return result

        overloads = {'int': original_int, 'float': lambda ceiling: 3.0}
        sexy = types.SimpleNamespace(RandomNumbers=types.SimpleNamespace(
            NextNumber=types.SimpleNamespace(Overloads=overloads)))
        challenge_type = types.SimpleNamespace(GetMethod=lambda name: name)
        system = types.SimpleNamespace(Int32='int', Single='float', Func=Generic(),
            Reflection=types.SimpleNamespace(Assembly=types.SimpleNamespace(
                GetAssembly=lambda cls: types.SimpleNamespace(GetType=lambda name: challenge_type))))
        test = self

        class Hook:
            def __init__(self, name, callback):
                if test.install_fail and name == 'InitZombieWavesChallengStageRandom':
                    raise RuntimeError('install failed')
                instructions = [instruction('Sexy.RandomNumbers', 'NextNumber', 'System.Int32')]
                if name == 'InitZombieWavesSurvival':
                    instructions.append(instruction('Sexy.RandomNumbers', 'NextNumber', 'System.Single'))
                # Non-matching calls must be left alone.
                instructions += [instruction('Other', 'NextNumber', 'System.Int32'),
                                 instruction('Sexy.RandomNumbers', 'NextNumber')]
                il = types.SimpleNamespace(Body=types.SimpleNamespace(Instructions=instructions), delegates={})
                callback(il)
                self.name = name
                test.active[name] = il.delegates

            def Dispose(self):
                test.disposed.append(self.name)
                del test.active[self.name]

        monomod = types.SimpleNamespace(
            Cil=types.SimpleNamespace(ILCursor=Cursor, ILContext=types.SimpleNamespace(Manipulator=lambda fn: fn)),
            RuntimeDetour=types.SimpleNamespace(ILHook=Hook))
        self.board = types.SimpleNamespace(
            mZombieAllowed=[False] * 40, mCutScene=types.SimpleNamespace(mPlacedZombies=True),
            InitZombieWaves=self.init_waves, PickZombieWaves=lambda: original_int(40),
            RemoveCutsceneZombies=lambda: self.preview_resets.append(True))
        self.preview_resets = []
        namespace = {'Lawn': types.SimpleNamespace(ZombieType=ZombieType, Board=object, Challenge=object),
                     'Sexy': sexy, 'System': system, 'MonoMod': monomod,
                     'OpCodes': types.SimpleNamespace(Call='call'), 'GetBoard': lambda: self.board}
        tree = ast.parse((ROOT / 'pgvz/set_zb.py').read_text(encoding='utf-8'))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        exec(compile(ast.Module(body=functions, type_ignores=[]), 'set_zb', 'exec'), namespace)
        self.set_zombies = namespace['SetZombies']

    def init_waves(self):
        allowed = self.board.mZombieAllowed
        allowed[:] = [False] * 40
        allowed[0] = True
        callbacks = self.active[self.mode]
        # An unrelated integer draw must not consume the selected zombie.
        self.assertEqual(callbacks['int'](100), 99)
        if self.mode == 'InitZombieWavesSurvival':
            allowed[5 if int(callbacks['float'](5.0)) == 0 else 2] = True
            self.assertEqual(callbacks['float'](8.0), 3.0)
        remaining = min(self.stage + 1, 9) if self.mode == 'InitZombieWavesSurvival' else 9
        while remaining:
            zombie = callbacks['int'](40)
            if allowed[zombie] or (self.mode == 'InitZombieWavesSurvival'
                                   and zombie == 12 and self.stage * 2 < 4):
                continue
            allowed[zombie] = True
            remaining -= 1
        if self.game_fail:
            raise RuntimeError('game failed')
        self.board.PickZombieWaves()

    def test_single_zamboni_at_4098_flags_is_prioritized(self):
        self.set_zombies([ZombieType.Zamboni])
        self.assertTrue(self.board.mZombieAllowed[12])
        self.assertFalse(self.board.mZombieAllowed[1])
        self.assertEqual(self.preview_resets, [True])
        self.assertFalse(self.board.mCutScene.mPlacedZombies)
        self.assertFalse(self.active)

    def test_newspaper_uses_float_choice(self):
        self.set_zombies([ZombieType.Newspaper, ZombieType.Zamboni])
        self.assertTrue(self.board.mZombieAllowed[5])
        self.assertTrue(self.board.mZombieAllowed[12])
        self.assertFalse(self.board.mZombieAllowed[2])

    def test_random_challenge_has_no_survival_choice_prefix(self):
        self.mode = 'InitZombieWavesChallengStageRandom'
        self.stage = 0
        self.set_zombies([ZombieType.Zamboni])
        self.assertTrue(self.board.mZombieAllowed[12])
        self.assertFalse(self.board.mZombieAllowed[1])

    def test_game_still_filters_zamboni_before_four_flags(self):
        self.stage = 0
        self.set_zombies([ZombieType.Zamboni])
        self.assertFalse(self.board.mZombieAllowed[12])

    def test_empty_selection_falls_back_to_game_randomness(self):
        self.set_zombies([])
        self.assertEqual(sum(self.board.mZombieAllowed), 11)

    def test_unused_candidates_do_not_leak_into_wave_randomness(self):
        self.stage = 0
        self.set_zombies([ZombieType.Football, ZombieType.Zamboni])
        self.assertTrue(self.board.mZombieAllowed[7])
        self.assertFalse(self.board.mZombieAllowed[12])
        self.assertIn(('int', 40), self.random_calls)

    def test_game_error_removes_overrides_without_refreshing_preview(self):
        self.game_fail = True
        with self.assertRaisesRegex(RuntimeError, 'game failed'):
            self.set_zombies([ZombieType.Zamboni])
        self.assertFalse(self.active)
        self.assertEqual(len(self.disposed), 2)
        self.assertFalse(self.preview_resets)

    def test_partial_hook_installation_is_cleaned_up(self):
        self.install_fail = True
        with self.assertRaisesRegex(RuntimeError, 'install failed'):
            self.set_zombies([ZombieType.Zamboni])
        self.assertFalse(self.active)
        self.assertEqual(self.disposed, ['InitZombieWavesSurvival'])

    def test_forced_spawn_does_not_install_natural_spawn_hooks(self):
        self.set_zombies([ZombieType.Zamboni], False)
        self.assertEqual([i for i, allowed in enumerate(self.board.mZombieAllowed) if allowed], [0, 12])
        self.assertFalse(self.disposed)


if __name__ == '__main__':
    unittest.main()
