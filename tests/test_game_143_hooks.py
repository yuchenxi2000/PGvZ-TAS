"""Production-state and portrait-option regressions without loading the game."""
import ast
import pathlib
import types
import unittest
from unittest.mock import MagicMock, Mock


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

    def test_builtin_menu_speed_and_checkbox_sync_with_stash_font_methods(self):
        tree = ast.parse((ROOT / 'pgvztool/hook.py').read_text(encoding='utf-8'))
        install = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                       and node.name == '_install_builtin_cheat_menu_hooks')
        menu_type = Mock()
        menu_type.GetField.side_effect = lambda name: NS(GetValue=lambda menu: getattr(menu, name))
        speed_format = Mock(side_effect=['1', '5', '0.25', '0.3333333333333333', '0.2'])
        menu_type.GetMethod.side_effect = lambda name: (
            NS(Invoke=speed_format) if name == 'GetGameSpeedString' else Mock()
        )
        checkbox_type = Mock()
        set_checked = Mock(side_effect=lambda widget, args: setattr(widget, 'mChecked', args[0]))
        checkbox_type.GetField.side_effect = lambda name: NS(GetValue=lambda widget: getattr(widget, name))
        checkbox_type.GetMethod.return_value = NS(Invoke=set_checked)
        assembly = NS(GetType=lambda name, *_: menu_type if name == 'Lawn.ZBCheatDialog' else checkbox_type)
        label_type = object()
        clr = NS(GetClrType=lambda _: NS(Assembly=assembly), Reference={label_type: NS})
        system = MagicMock()
        system.Object.ReferenceEquals.side_effect = lambda left, right: left is right
        system.WeakReference.side_effect = lambda menu: NS(Target=menu)
        system.Array[system.Object].side_effect = lambda values: values
        globals_ = NS(gFastMo=False, gSlowMo=False, gFastSlowMoNum=0)
        options = NS(autoCollect=True)
        sync_reg = Mock()
        log = Mock()
        namespace = {
            'Lawn': NS(LawnApp=object, Label=label_type),
            'Sexy': NS(GlobalStaticVars=globals_, Debug=NS(Log=log), DebugType=NS(Error='error')),
            'clr': clr, 'System': system, 'MonoMod': MagicMock(), 'ILHook': Mock(),
            '_BUILTIN_CHEAT_FIELDS': {5: 'autoCollect'}, 'cheat_option': options, 'sync_reg': sync_reg,
        }
        exec(compile(ast.Module(body=[install], type_ignores=[]), 'built-in-cheat-menu', 'exec'), namespace)
        namespace[install.name]()
        refresh_menu = system.Action[system.Object].call_args.args[0]
        click_checkbox = system.Func[system.Int32, system.Boolean, system.Boolean].call_args.args[0]

        label = NS(mText='', mWidth=24, mFont=NS(StringWidth=len))
        checkbox = NS(mId=5, mChecked=False)
        checkbox_type.IsInstanceOfType.side_effect = lambda widget: widget is checkbox

        def try_get_label(reference):
            reference.Value = label
            return True

        menu = NS(mGameSpeedLabel=NS(TryGetTarget=try_get_label),
                  mPanel=NS(mWidgets=[NS(mWidgets=[checkbox])]))
        refresh_menu(menu)
        self.assertEqual(label.mText, '速度控制 当前:1x')
        set_checked.assert_called_once_with(checkbox, [True, False])
        globals_.gFastMo = True
        globals_.gFastSlowMoNum = 5
        refresh_menu(menu)
        self.assertEqual(label.mText, '速度控制 当前:5x')
        refresh_menu(menu)
        self.assertEqual(speed_format.call_count, 2)
        globals_.gFastMo, globals_.gSlowMo, globals_.gFastSlowMoNum = False, True, 4
        refresh_menu(menu)
        self.assertEqual(label.mText, '速度控制 当前:0.25x')
        globals_.gFastSlowMoNum = 3
        refresh_menu(menu)
        self.assertEqual(label.mText, '速度控制 当前:1/3x')
        log.assert_not_called()

        label.mFont.StringWidth = Mock(side_effect=RuntimeError('font unavailable'))
        globals_.gFastSlowMoNum = 5
        options.autoCollect = False
        refresh_menu(menu)
        set_checked.assert_called_with(checkbox, [False, False])
        self.assertFalse(checkbox.mChecked)
        self.assertTrue(click_checkbox(5, True))
        sync_reg.set_local_state.assert_called_once_with('cheat', 'autoCollect', True)
        log.assert_called_once()


if __name__ == '__main__':
    unittest.main()
