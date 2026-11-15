"""Production-state and portrait-option regressions without loading the game."""
import ast
import pathlib
import types
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
NS = types.SimpleNamespace


class Game143HookTests(unittest.TestCase):
    def setUp(self):
        self.options = NS(disableTachieCensor=False, marigoldAlwaysThreeDiamonds=False)
        self.voices = []
        self.animations = []
        self.reanim = NS(mAnimTime=0.3, PlayReanim=lambda *args: self.animations.append(args))
        lawn = NS(LawnApp=object, Plant=object,
                  SeedType=NS(Marigold='marigold'),
                  PlantState=NS(MarigoldProducing='producing'),
                  DropLootType=NS(ThreeDiamonds='three-diamonds'),
                  PlantVoice=NS(VoiceType=NS(Diamond='diamond'),
                                Play=lambda *args: self.voices.append(args)))
        namespace = {'Lawn': lawn, 'cheat_option': self.options,
                     'Sexy': NS(TodLib=NS(ReanimLoopType=NS(PlayOnceAndHold='hold')))}
        names = ('LawnApp__ShouldCensorTachie', 'Plant__UpdateProductionPlant')
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names]
        for function in functions:
            function.decorator_list = []
        exec(compile(ast.Module(body=functions, type_ignores=[]), 'game-143-hooks', 'exec'), namespace)
        self.censor = namespace[names[0]]
        self.production = namespace[names[1]]
        self.plant = NS(mSeedType='marigold', mImitaterType='none', mState='idle',
                        mGravebusterDrop='silver', mBodyReanimID=1,
                        mApp=NS(ReanimationTryToGet=lambda _: self.reanim))

    def test_portrait_option_keeps_native_platform_result_until_enabled(self):
        calls = []
        for native in (False, True):
            def original(app):
                calls.append(app)
                return native
            self.assertEqual(self.censor(original, 'app'), native)
            self.options.disableTachieCensor = True
            self.assertFalse(self.censor(original, 'app'))
            self.options.disableTachieCensor = False
            self.assertEqual(self.censor(original, 'app'), native)
        self.assertEqual(calls, ['app'] * 4)

    def begin_production(self, plant):
        plant.mState = 'producing'
        plant.mGravebusterDrop = 'silver'
        plant.mStateCountdown = 190
        return 'native-result'

    def test_forcing_result_preserves_native_delay_and_animation_progress(self):
        self.options.marigoldAlwaysThreeDiamonds = True
        self.assertEqual(self.production(self.begin_production, self.plant), 'native-result')
        self.assertEqual(self.plant.mGravebusterDrop, 'three-diamonds')
        self.assertEqual(self.plant.mStateCountdown, 190)
        self.assertEqual(self.reanim.mAnimTime, 0.3)
        self.assertEqual(self.animations[0][0], 'anim_producing3')
        self.assertEqual(len(self.voices), 1)

    def test_enabling_during_production_changes_drop_before_native_settlement(self):
        self.options.marigoldAlwaysThreeDiamonds = True
        self.plant.mState = 'producing'
        drops = []
        def settle(plant):
            drops.append(plant.mGravebusterDrop)
            plant.mState = 'idle'
        self.production(settle, self.plant)
        self.assertEqual(drops, ['three-diamonds'])
        self.assertFalse(self.voices)

    def test_disabling_restores_random_result_for_next_production(self):
        self.options.marigoldAlwaysThreeDiamonds = True
        self.production(self.begin_production, self.plant)
        self.options.marigoldAlwaysThreeDiamonds = False
        self.plant.mState = 'idle'
        self.production(self.begin_production, self.plant)
        self.assertEqual(self.plant.mGravebusterDrop, 'silver')
        self.assertEqual(len(self.voices), 1)

    def test_native_diamond_voice_is_not_duplicated(self):
        self.options.marigoldAlwaysThreeDiamonds = True
        def native_diamonds(plant):
            self.begin_production(plant)
            plant.mGravebusterDrop = 'three-diamonds'
            self.voices.append('native')
        self.production(native_diamonds, self.plant)
        self.assertEqual(self.voices, ['native'])

    def test_ineligible_plants_and_blocked_production_keep_native_behavior(self):
        self.options.marigoldAlwaysThreeDiamonds = True
        self.plant.mSeedType = 'sunflower'
        self.production(self.begin_production, self.plant)
        self.assertEqual(self.plant.mGravebusterDrop, 'silver')
        self.assertFalse(self.voices)
        self.plant.mSeedType = 'marigold'
        self.plant.mState = 'idle'
        self.assertEqual(self.production(lambda _: 'blocked', self.plant), 'blocked')
        self.assertEqual(self.plant.mState, 'idle')
        self.assertFalse(self.voices)


if __name__ == '__main__':
    unittest.main()
