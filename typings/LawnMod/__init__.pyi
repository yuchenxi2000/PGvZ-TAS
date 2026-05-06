import typing, clr, abc
from System import Array_1, Func_2, Delegate, MulticastDelegate, IAsyncResult, AsyncCallback
from MonoMod.RuntimeDetour import DynamicHookGen
from System.Reflection import MethodBase, MethodInfo
from IronPython.Runtime.Types import BuiltinFunction, BuiltinMethodDescriptor
from System.Dynamic import DynamicObject, InvokeBinder
from Lawn import SeedPacketsWidget, SeedType

class DynamicHelper(abc.ABC):
    @staticmethod
    def GetDynamicMember(obj: typing.Any, memberName: str) -> typing.Any: ...
    @staticmethod
    def SetDynamicMember(obj: typing.Any, memberName: str, value: typing.Any) -> None: ...
    @staticmethod
    def SetPrivateField(instance: typing.Any, fieldname: str, value: typing.Any) -> None: ...
    @staticmethod
    def SetPrivateFieldStatic(type: typing.Type[typing.Any], fieldname: str, value: typing.Any) -> None: ...
    @staticmethod
    def SetPrivateProperty(instance: typing.Any, propertyname: str, value: typing.Any) -> None: ...
    @staticmethod
    def SetPrivatePropertyStatic(type: typing.Type[typing.Any], propertyname: str, value: typing.Any) -> None: ...
    # Skipped CallPrivateMethod due to it being static, abstract and generic.

    CallPrivateMethod : CallPrivateMethod_MethodGroup
    class CallPrivateMethod_MethodGroup:
        def __getitem__(self, t:typing.Type[CallPrivateMethod_1_T1]) -> CallPrivateMethod_1[CallPrivateMethod_1_T1]: ...

        CallPrivateMethod_1_T1 = typing.TypeVar('CallPrivateMethod_1_T1')
        class CallPrivateMethod_1(typing.Generic[CallPrivateMethod_1_T1]):
            CallPrivateMethod_1_T = DynamicHelper.CallPrivateMethod_MethodGroup.CallPrivateMethod_1_T1
            def __call__(self, instance: typing.Any, name: str, param: Array_1[typing.Any]) -> CallPrivateMethod_1_T:...


    # Skipped CallPrivateMethodStatic due to it being static, abstract and generic.

    CallPrivateMethodStatic : CallPrivateMethodStatic_MethodGroup
    class CallPrivateMethodStatic_MethodGroup:
        def __getitem__(self, t:typing.Type[CallPrivateMethodStatic_1_T1]) -> CallPrivateMethodStatic_1[CallPrivateMethodStatic_1_T1]: ...

        CallPrivateMethodStatic_1_T1 = typing.TypeVar('CallPrivateMethodStatic_1_T1')
        class CallPrivateMethodStatic_1(typing.Generic[CallPrivateMethodStatic_1_T1]):
            CallPrivateMethodStatic_1_T = DynamicHelper.CallPrivateMethodStatic_MethodGroup.CallPrivateMethodStatic_1_T1
            def __call__(self, type: typing.Type[typing.Any], name: str, param: Array_1[typing.Any]) -> CallPrivateMethodStatic_1_T:...


    # Skipped GetPrivateField due to it being static, abstract and generic.

    GetPrivateField : GetPrivateField_MethodGroup
    class GetPrivateField_MethodGroup:
        def __getitem__(self, t:typing.Type[GetPrivateField_1_T1]) -> GetPrivateField_1[GetPrivateField_1_T1]: ...

        GetPrivateField_1_T1 = typing.TypeVar('GetPrivateField_1_T1')
        class GetPrivateField_1(typing.Generic[GetPrivateField_1_T1]):
            GetPrivateField_1_T = DynamicHelper.GetPrivateField_MethodGroup.GetPrivateField_1_T1
            def __call__(self, instance: typing.Any, fieldname: str) -> GetPrivateField_1_T:...


    # Skipped GetPrivateFieldStatic due to it being static, abstract and generic.

    GetPrivateFieldStatic : GetPrivateFieldStatic_MethodGroup
    class GetPrivateFieldStatic_MethodGroup:
        def __getitem__(self, t:typing.Type[GetPrivateFieldStatic_1_T1]) -> GetPrivateFieldStatic_1[GetPrivateFieldStatic_1_T1]: ...

        GetPrivateFieldStatic_1_T1 = typing.TypeVar('GetPrivateFieldStatic_1_T1')
        class GetPrivateFieldStatic_1(typing.Generic[GetPrivateFieldStatic_1_T1]):
            GetPrivateFieldStatic_1_T = DynamicHelper.GetPrivateFieldStatic_MethodGroup.GetPrivateFieldStatic_1_T1
            def __call__(self, type: typing.Type[typing.Any], fieldname: str) -> GetPrivateFieldStatic_1_T:...


    # Skipped GetPrivateProperty due to it being static, abstract and generic.

    GetPrivateProperty : GetPrivateProperty_MethodGroup
    class GetPrivateProperty_MethodGroup:
        def __getitem__(self, t:typing.Type[GetPrivateProperty_1_T1]) -> GetPrivateProperty_1[GetPrivateProperty_1_T1]: ...

        GetPrivateProperty_1_T1 = typing.TypeVar('GetPrivateProperty_1_T1')
        class GetPrivateProperty_1(typing.Generic[GetPrivateProperty_1_T1]):
            GetPrivateProperty_1_T = DynamicHelper.GetPrivateProperty_MethodGroup.GetPrivateProperty_1_T1
            def __call__(self, instance: typing.Any, propertyname: str) -> GetPrivateProperty_1_T:...


    # Skipped GetPrivatePropertyStatic due to it being static, abstract and generic.

    GetPrivatePropertyStatic : GetPrivatePropertyStatic_MethodGroup
    class GetPrivatePropertyStatic_MethodGroup:
        def __getitem__(self, t:typing.Type[GetPrivatePropertyStatic_1_T1]) -> GetPrivatePropertyStatic_1[GetPrivatePropertyStatic_1_T1]: ...

        GetPrivatePropertyStatic_1_T1 = typing.TypeVar('GetPrivatePropertyStatic_1_T1')
        class GetPrivatePropertyStatic_1(typing.Generic[GetPrivatePropertyStatic_1_T1]):
            GetPrivatePropertyStatic_1_T = DynamicHelper.GetPrivatePropertyStatic_MethodGroup.GetPrivatePropertyStatic_1_T1
            def __call__(self, type: typing.Type[typing.Any], propertyname: str) -> GetPrivatePropertyStatic_1_T:...




class MonoModUtils(abc.ABC):
    IL : DynamicHookGen
    On : DynamicHookGen
    OnOrIL : DynamicHookGen
    @staticmethod
    def As(funcOrMethoddesc: typing.Any) -> Func_2[typing.Any, Delegate]: ...
    @staticmethod
    def AsAction(generics: Array_1[typing.Type[typing.Any]]) -> Func_2[typing.Any, Delegate]: ...
    @staticmethod
    def AsFunc(generics: Array_1[typing.Type[typing.Any]]) -> Func_2[typing.Any, Delegate]: ...
    @staticmethod
    def GetFirstTargetFromPythonBuiltinFunc(func: clr.Reference[BuiltinFunction]) -> MethodBase: ...
    @staticmethod
    def GetFirstTargetFromPythonMethodDesc(desc: clr.Reference[BuiltinMethodDescriptor]) -> MethodBase: ...
    @staticmethod
    def GetGenericsForAction(method: clr.Reference[MethodInfo]) -> Array_1[typing.Type[typing.Any]]: ...
    @staticmethod
    def GetGenericsForFunc(method: clr.Reference[MethodInfo]) -> Array_1[typing.Type[typing.Any]]: ...
    @staticmethod
    def GetMethodArgs(method: clr.Reference[MethodInfo]) -> Array_1[typing.Type[typing.Any]]: ...
    @staticmethod
    def HookTo(funcOrMethoddesc: typing.Any, hookType: DynamicHookGen.HookType = ...) -> Func_2[typing.Any, MonoModUtils.HookResult]: ...
    @staticmethod
    def MakeRuntimeDetourGenerics(theTypes: clr.Reference[Array_1[typing.Type[typing.Any]]]) -> Array_1[typing.Type[typing.Any]]: ...
    @staticmethod
    def StripPythonMethodDesc(o: clr.Reference[typing.Any]) -> MethodBase: ...

    class HookResult(DynamicObject):
        def TryInvoke(self, binder: InvokeBinder, args: Array_1[typing.Any], result: clr.Reference[typing.Any]) -> bool: ...
        def UnHook(self) -> None: ...


    class MethodToDelegateHelper(abc.ABC):
        # Skipped A due to it being static, abstract and generic.

        A : A_MethodGroup
        class A_MethodGroup:
            @typing.overload
            def __getitem__(self, t:typing.Type[A_1_T1]) -> A_1[A_1_T1]: ...

            A_1_T1 = typing.TypeVar('A_1_T1')
            class A_1(typing.Generic[A_1_T1]):
                A_1_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_1_T1
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_2_T1], typing.Type[A_2_T2]]) -> A_2[A_2_T1, A_2_T2]: ...

            A_2_T1 = typing.TypeVar('A_2_T1')
            A_2_T2 = typing.TypeVar('A_2_T2')
            class A_2(typing.Generic[A_2_T1, A_2_T2]):
                A_2_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_2_T1
                A_2_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_2_T2
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_3_T1], typing.Type[A_3_T2], typing.Type[A_3_T3]]) -> A_3[A_3_T1, A_3_T2, A_3_T3]: ...

            A_3_T1 = typing.TypeVar('A_3_T1')
            A_3_T2 = typing.TypeVar('A_3_T2')
            A_3_T3 = typing.TypeVar('A_3_T3')
            class A_3(typing.Generic[A_3_T1, A_3_T2, A_3_T3]):
                A_3_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_3_T1
                A_3_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_3_T2
                A_3_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_3_T3
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_4_T1], typing.Type[A_4_T2], typing.Type[A_4_T3], typing.Type[A_4_T4]]) -> A_4[A_4_T1, A_4_T2, A_4_T3, A_4_T4]: ...

            A_4_T1 = typing.TypeVar('A_4_T1')
            A_4_T2 = typing.TypeVar('A_4_T2')
            A_4_T3 = typing.TypeVar('A_4_T3')
            A_4_T4 = typing.TypeVar('A_4_T4')
            class A_4(typing.Generic[A_4_T1, A_4_T2, A_4_T3, A_4_T4]):
                A_4_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_4_T1
                A_4_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_4_T2
                A_4_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_4_T3
                A_4_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_4_T4
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_5_T1], typing.Type[A_5_T2], typing.Type[A_5_T3], typing.Type[A_5_T4], typing.Type[A_5_T5]]) -> A_5[A_5_T1, A_5_T2, A_5_T3, A_5_T4, A_5_T5]: ...

            A_5_T1 = typing.TypeVar('A_5_T1')
            A_5_T2 = typing.TypeVar('A_5_T2')
            A_5_T3 = typing.TypeVar('A_5_T3')
            A_5_T4 = typing.TypeVar('A_5_T4')
            A_5_T5 = typing.TypeVar('A_5_T5')
            class A_5(typing.Generic[A_5_T1, A_5_T2, A_5_T3, A_5_T4, A_5_T5]):
                A_5_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_5_T1
                A_5_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_5_T2
                A_5_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_5_T3
                A_5_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_5_T4
                A_5_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_5_T5
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_6_T1], typing.Type[A_6_T2], typing.Type[A_6_T3], typing.Type[A_6_T4], typing.Type[A_6_T5], typing.Type[A_6_T6]]) -> A_6[A_6_T1, A_6_T2, A_6_T3, A_6_T4, A_6_T5, A_6_T6]: ...

            A_6_T1 = typing.TypeVar('A_6_T1')
            A_6_T2 = typing.TypeVar('A_6_T2')
            A_6_T3 = typing.TypeVar('A_6_T3')
            A_6_T4 = typing.TypeVar('A_6_T4')
            A_6_T5 = typing.TypeVar('A_6_T5')
            A_6_T6 = typing.TypeVar('A_6_T6')
            class A_6(typing.Generic[A_6_T1, A_6_T2, A_6_T3, A_6_T4, A_6_T5, A_6_T6]):
                A_6_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_6_T1
                A_6_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_6_T2
                A_6_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_6_T3
                A_6_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_6_T4
                A_6_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_6_T5
                A_6_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_6_T6
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_7_T1], typing.Type[A_7_T2], typing.Type[A_7_T3], typing.Type[A_7_T4], typing.Type[A_7_T5], typing.Type[A_7_T6], typing.Type[A_7_T7]]) -> A_7[A_7_T1, A_7_T2, A_7_T3, A_7_T4, A_7_T5, A_7_T6, A_7_T7]: ...

            A_7_T1 = typing.TypeVar('A_7_T1')
            A_7_T2 = typing.TypeVar('A_7_T2')
            A_7_T3 = typing.TypeVar('A_7_T3')
            A_7_T4 = typing.TypeVar('A_7_T4')
            A_7_T5 = typing.TypeVar('A_7_T5')
            A_7_T6 = typing.TypeVar('A_7_T6')
            A_7_T7 = typing.TypeVar('A_7_T7')
            class A_7(typing.Generic[A_7_T1, A_7_T2, A_7_T3, A_7_T4, A_7_T5, A_7_T6, A_7_T7]):
                A_7_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T1
                A_7_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T2
                A_7_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T3
                A_7_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T4
                A_7_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T5
                A_7_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T6
                A_7_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_7_T7
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_8_T1], typing.Type[A_8_T2], typing.Type[A_8_T3], typing.Type[A_8_T4], typing.Type[A_8_T5], typing.Type[A_8_T6], typing.Type[A_8_T7], typing.Type[A_8_T8]]) -> A_8[A_8_T1, A_8_T2, A_8_T3, A_8_T4, A_8_T5, A_8_T6, A_8_T7, A_8_T8]: ...

            A_8_T1 = typing.TypeVar('A_8_T1')
            A_8_T2 = typing.TypeVar('A_8_T2')
            A_8_T3 = typing.TypeVar('A_8_T3')
            A_8_T4 = typing.TypeVar('A_8_T4')
            A_8_T5 = typing.TypeVar('A_8_T5')
            A_8_T6 = typing.TypeVar('A_8_T6')
            A_8_T7 = typing.TypeVar('A_8_T7')
            A_8_T8 = typing.TypeVar('A_8_T8')
            class A_8(typing.Generic[A_8_T1, A_8_T2, A_8_T3, A_8_T4, A_8_T5, A_8_T6, A_8_T7, A_8_T8]):
                A_8_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T1
                A_8_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T2
                A_8_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T3
                A_8_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T4
                A_8_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T5
                A_8_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T6
                A_8_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T7
                A_8_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_8_T8
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_9_T1], typing.Type[A_9_T2], typing.Type[A_9_T3], typing.Type[A_9_T4], typing.Type[A_9_T5], typing.Type[A_9_T6], typing.Type[A_9_T7], typing.Type[A_9_T8], typing.Type[A_9_T9]]) -> A_9[A_9_T1, A_9_T2, A_9_T3, A_9_T4, A_9_T5, A_9_T6, A_9_T7, A_9_T8, A_9_T9]: ...

            A_9_T1 = typing.TypeVar('A_9_T1')
            A_9_T2 = typing.TypeVar('A_9_T2')
            A_9_T3 = typing.TypeVar('A_9_T3')
            A_9_T4 = typing.TypeVar('A_9_T4')
            A_9_T5 = typing.TypeVar('A_9_T5')
            A_9_T6 = typing.TypeVar('A_9_T6')
            A_9_T7 = typing.TypeVar('A_9_T7')
            A_9_T8 = typing.TypeVar('A_9_T8')
            A_9_T9 = typing.TypeVar('A_9_T9')
            class A_9(typing.Generic[A_9_T1, A_9_T2, A_9_T3, A_9_T4, A_9_T5, A_9_T6, A_9_T7, A_9_T8, A_9_T9]):
                A_9_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T1
                A_9_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T2
                A_9_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T3
                A_9_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T4
                A_9_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T5
                A_9_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T6
                A_9_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T7
                A_9_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T8
                A_9_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_9_T9
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_10_T1], typing.Type[A_10_T2], typing.Type[A_10_T3], typing.Type[A_10_T4], typing.Type[A_10_T5], typing.Type[A_10_T6], typing.Type[A_10_T7], typing.Type[A_10_T8], typing.Type[A_10_T9], typing.Type[A_10_T10]]) -> A_10[A_10_T1, A_10_T2, A_10_T3, A_10_T4, A_10_T5, A_10_T6, A_10_T7, A_10_T8, A_10_T9, A_10_T10]: ...

            A_10_T1 = typing.TypeVar('A_10_T1')
            A_10_T2 = typing.TypeVar('A_10_T2')
            A_10_T3 = typing.TypeVar('A_10_T3')
            A_10_T4 = typing.TypeVar('A_10_T4')
            A_10_T5 = typing.TypeVar('A_10_T5')
            A_10_T6 = typing.TypeVar('A_10_T6')
            A_10_T7 = typing.TypeVar('A_10_T7')
            A_10_T8 = typing.TypeVar('A_10_T8')
            A_10_T9 = typing.TypeVar('A_10_T9')
            A_10_T10 = typing.TypeVar('A_10_T10')
            class A_10(typing.Generic[A_10_T1, A_10_T2, A_10_T3, A_10_T4, A_10_T5, A_10_T6, A_10_T7, A_10_T8, A_10_T9, A_10_T10]):
                A_10_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T1
                A_10_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T2
                A_10_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T3
                A_10_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T4
                A_10_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T5
                A_10_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T6
                A_10_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T7
                A_10_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T8
                A_10_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T9
                A_10_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_10_T10
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_11_T1], typing.Type[A_11_T2], typing.Type[A_11_T3], typing.Type[A_11_T4], typing.Type[A_11_T5], typing.Type[A_11_T6], typing.Type[A_11_T7], typing.Type[A_11_T8], typing.Type[A_11_T9], typing.Type[A_11_T10], typing.Type[A_11_T11]]) -> A_11[A_11_T1, A_11_T2, A_11_T3, A_11_T4, A_11_T5, A_11_T6, A_11_T7, A_11_T8, A_11_T9, A_11_T10, A_11_T11]: ...

            A_11_T1 = typing.TypeVar('A_11_T1')
            A_11_T2 = typing.TypeVar('A_11_T2')
            A_11_T3 = typing.TypeVar('A_11_T3')
            A_11_T4 = typing.TypeVar('A_11_T4')
            A_11_T5 = typing.TypeVar('A_11_T5')
            A_11_T6 = typing.TypeVar('A_11_T6')
            A_11_T7 = typing.TypeVar('A_11_T7')
            A_11_T8 = typing.TypeVar('A_11_T8')
            A_11_T9 = typing.TypeVar('A_11_T9')
            A_11_T10 = typing.TypeVar('A_11_T10')
            A_11_T11 = typing.TypeVar('A_11_T11')
            class A_11(typing.Generic[A_11_T1, A_11_T2, A_11_T3, A_11_T4, A_11_T5, A_11_T6, A_11_T7, A_11_T8, A_11_T9, A_11_T10, A_11_T11]):
                A_11_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T1
                A_11_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T2
                A_11_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T3
                A_11_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T4
                A_11_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T5
                A_11_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T6
                A_11_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T7
                A_11_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T8
                A_11_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T9
                A_11_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T10
                A_11_T11 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_11_T11
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_12_T1], typing.Type[A_12_T2], typing.Type[A_12_T3], typing.Type[A_12_T4], typing.Type[A_12_T5], typing.Type[A_12_T6], typing.Type[A_12_T7], typing.Type[A_12_T8], typing.Type[A_12_T9], typing.Type[A_12_T10], typing.Type[A_12_T11], typing.Type[A_12_T12]]) -> A_12[A_12_T1, A_12_T2, A_12_T3, A_12_T4, A_12_T5, A_12_T6, A_12_T7, A_12_T8, A_12_T9, A_12_T10, A_12_T11, A_12_T12]: ...

            A_12_T1 = typing.TypeVar('A_12_T1')
            A_12_T2 = typing.TypeVar('A_12_T2')
            A_12_T3 = typing.TypeVar('A_12_T3')
            A_12_T4 = typing.TypeVar('A_12_T4')
            A_12_T5 = typing.TypeVar('A_12_T5')
            A_12_T6 = typing.TypeVar('A_12_T6')
            A_12_T7 = typing.TypeVar('A_12_T7')
            A_12_T8 = typing.TypeVar('A_12_T8')
            A_12_T9 = typing.TypeVar('A_12_T9')
            A_12_T10 = typing.TypeVar('A_12_T10')
            A_12_T11 = typing.TypeVar('A_12_T11')
            A_12_T12 = typing.TypeVar('A_12_T12')
            class A_12(typing.Generic[A_12_T1, A_12_T2, A_12_T3, A_12_T4, A_12_T5, A_12_T6, A_12_T7, A_12_T8, A_12_T9, A_12_T10, A_12_T11, A_12_T12]):
                A_12_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T1
                A_12_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T2
                A_12_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T3
                A_12_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T4
                A_12_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T5
                A_12_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T6
                A_12_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T7
                A_12_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T8
                A_12_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T9
                A_12_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T10
                A_12_T11 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T11
                A_12_T12 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_12_T12
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_13_T1], typing.Type[A_13_T2], typing.Type[A_13_T3], typing.Type[A_13_T4], typing.Type[A_13_T5], typing.Type[A_13_T6], typing.Type[A_13_T7], typing.Type[A_13_T8], typing.Type[A_13_T9], typing.Type[A_13_T10], typing.Type[A_13_T11], typing.Type[A_13_T12], typing.Type[A_13_T13]]) -> A_13[A_13_T1, A_13_T2, A_13_T3, A_13_T4, A_13_T5, A_13_T6, A_13_T7, A_13_T8, A_13_T9, A_13_T10, A_13_T11, A_13_T12, A_13_T13]: ...

            A_13_T1 = typing.TypeVar('A_13_T1')
            A_13_T2 = typing.TypeVar('A_13_T2')
            A_13_T3 = typing.TypeVar('A_13_T3')
            A_13_T4 = typing.TypeVar('A_13_T4')
            A_13_T5 = typing.TypeVar('A_13_T5')
            A_13_T6 = typing.TypeVar('A_13_T6')
            A_13_T7 = typing.TypeVar('A_13_T7')
            A_13_T8 = typing.TypeVar('A_13_T8')
            A_13_T9 = typing.TypeVar('A_13_T9')
            A_13_T10 = typing.TypeVar('A_13_T10')
            A_13_T11 = typing.TypeVar('A_13_T11')
            A_13_T12 = typing.TypeVar('A_13_T12')
            A_13_T13 = typing.TypeVar('A_13_T13')
            class A_13(typing.Generic[A_13_T1, A_13_T2, A_13_T3, A_13_T4, A_13_T5, A_13_T6, A_13_T7, A_13_T8, A_13_T9, A_13_T10, A_13_T11, A_13_T12, A_13_T13]):
                A_13_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T1
                A_13_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T2
                A_13_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T3
                A_13_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T4
                A_13_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T5
                A_13_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T6
                A_13_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T7
                A_13_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T8
                A_13_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T9
                A_13_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T10
                A_13_T11 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T11
                A_13_T12 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T12
                A_13_T13 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_13_T13
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_14_T1], typing.Type[A_14_T2], typing.Type[A_14_T3], typing.Type[A_14_T4], typing.Type[A_14_T5], typing.Type[A_14_T6], typing.Type[A_14_T7], typing.Type[A_14_T8], typing.Type[A_14_T9], typing.Type[A_14_T10], typing.Type[A_14_T11], typing.Type[A_14_T12], typing.Type[A_14_T13], typing.Type[A_14_T14]]) -> A_14[A_14_T1, A_14_T2, A_14_T3, A_14_T4, A_14_T5, A_14_T6, A_14_T7, A_14_T8, A_14_T9, A_14_T10, A_14_T11, A_14_T12, A_14_T13, A_14_T14]: ...

            A_14_T1 = typing.TypeVar('A_14_T1')
            A_14_T2 = typing.TypeVar('A_14_T2')
            A_14_T3 = typing.TypeVar('A_14_T3')
            A_14_T4 = typing.TypeVar('A_14_T4')
            A_14_T5 = typing.TypeVar('A_14_T5')
            A_14_T6 = typing.TypeVar('A_14_T6')
            A_14_T7 = typing.TypeVar('A_14_T7')
            A_14_T8 = typing.TypeVar('A_14_T8')
            A_14_T9 = typing.TypeVar('A_14_T9')
            A_14_T10 = typing.TypeVar('A_14_T10')
            A_14_T11 = typing.TypeVar('A_14_T11')
            A_14_T12 = typing.TypeVar('A_14_T12')
            A_14_T13 = typing.TypeVar('A_14_T13')
            A_14_T14 = typing.TypeVar('A_14_T14')
            class A_14(typing.Generic[A_14_T1, A_14_T2, A_14_T3, A_14_T4, A_14_T5, A_14_T6, A_14_T7, A_14_T8, A_14_T9, A_14_T10, A_14_T11, A_14_T12, A_14_T13, A_14_T14]):
                A_14_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T1
                A_14_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T2
                A_14_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T3
                A_14_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T4
                A_14_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T5
                A_14_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T6
                A_14_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T7
                A_14_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T8
                A_14_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T9
                A_14_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T10
                A_14_T11 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T11
                A_14_T12 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T12
                A_14_T13 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T13
                A_14_T14 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_14_T14
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_15_T1], typing.Type[A_15_T2], typing.Type[A_15_T3], typing.Type[A_15_T4], typing.Type[A_15_T5], typing.Type[A_15_T6], typing.Type[A_15_T7], typing.Type[A_15_T8], typing.Type[A_15_T9], typing.Type[A_15_T10], typing.Type[A_15_T11], typing.Type[A_15_T12], typing.Type[A_15_T13], typing.Type[A_15_T14], typing.Type[A_15_T15]]) -> A_15[A_15_T1, A_15_T2, A_15_T3, A_15_T4, A_15_T5, A_15_T6, A_15_T7, A_15_T8, A_15_T9, A_15_T10, A_15_T11, A_15_T12, A_15_T13, A_15_T14, A_15_T15]: ...

            A_15_T1 = typing.TypeVar('A_15_T1')
            A_15_T2 = typing.TypeVar('A_15_T2')
            A_15_T3 = typing.TypeVar('A_15_T3')
            A_15_T4 = typing.TypeVar('A_15_T4')
            A_15_T5 = typing.TypeVar('A_15_T5')
            A_15_T6 = typing.TypeVar('A_15_T6')
            A_15_T7 = typing.TypeVar('A_15_T7')
            A_15_T8 = typing.TypeVar('A_15_T8')
            A_15_T9 = typing.TypeVar('A_15_T9')
            A_15_T10 = typing.TypeVar('A_15_T10')
            A_15_T11 = typing.TypeVar('A_15_T11')
            A_15_T12 = typing.TypeVar('A_15_T12')
            A_15_T13 = typing.TypeVar('A_15_T13')
            A_15_T14 = typing.TypeVar('A_15_T14')
            A_15_T15 = typing.TypeVar('A_15_T15')
            class A_15(typing.Generic[A_15_T1, A_15_T2, A_15_T3, A_15_T4, A_15_T5, A_15_T6, A_15_T7, A_15_T8, A_15_T9, A_15_T10, A_15_T11, A_15_T12, A_15_T13, A_15_T14, A_15_T15]):
                A_15_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T1
                A_15_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T2
                A_15_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T3
                A_15_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T4
                A_15_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T5
                A_15_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T6
                A_15_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T7
                A_15_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T8
                A_15_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T9
                A_15_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T10
                A_15_T11 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T11
                A_15_T12 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T12
                A_15_T13 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T13
                A_15_T14 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T14
                A_15_T15 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_15_T15
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[A_16_T1], typing.Type[A_16_T2], typing.Type[A_16_T3], typing.Type[A_16_T4], typing.Type[A_16_T5], typing.Type[A_16_T6], typing.Type[A_16_T7], typing.Type[A_16_T8], typing.Type[A_16_T9], typing.Type[A_16_T10], typing.Type[A_16_T11], typing.Type[A_16_T12], typing.Type[A_16_T13], typing.Type[A_16_T14], typing.Type[A_16_T15], typing.Type[A_16_T16]]) -> A_16[A_16_T1, A_16_T2, A_16_T3, A_16_T4, A_16_T5, A_16_T6, A_16_T7, A_16_T8, A_16_T9, A_16_T10, A_16_T11, A_16_T12, A_16_T13, A_16_T14, A_16_T15, A_16_T16]: ...

            A_16_T1 = typing.TypeVar('A_16_T1')
            A_16_T2 = typing.TypeVar('A_16_T2')
            A_16_T3 = typing.TypeVar('A_16_T3')
            A_16_T4 = typing.TypeVar('A_16_T4')
            A_16_T5 = typing.TypeVar('A_16_T5')
            A_16_T6 = typing.TypeVar('A_16_T6')
            A_16_T7 = typing.TypeVar('A_16_T7')
            A_16_T8 = typing.TypeVar('A_16_T8')
            A_16_T9 = typing.TypeVar('A_16_T9')
            A_16_T10 = typing.TypeVar('A_16_T10')
            A_16_T11 = typing.TypeVar('A_16_T11')
            A_16_T12 = typing.TypeVar('A_16_T12')
            A_16_T13 = typing.TypeVar('A_16_T13')
            A_16_T14 = typing.TypeVar('A_16_T14')
            A_16_T15 = typing.TypeVar('A_16_T15')
            A_16_T16 = typing.TypeVar('A_16_T16')
            class A_16(typing.Generic[A_16_T1, A_16_T2, A_16_T3, A_16_T4, A_16_T5, A_16_T6, A_16_T7, A_16_T8, A_16_T9, A_16_T10, A_16_T11, A_16_T12, A_16_T13, A_16_T14, A_16_T15, A_16_T16]):
                A_16_T1 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T1
                A_16_T2 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T2
                A_16_T3 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T3
                A_16_T4 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T4
                A_16_T5 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T5
                A_16_T6 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T6
                A_16_T7 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T7
                A_16_T8 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T8
                A_16_T9 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T9
                A_16_T10 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T10
                A_16_T11 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T11
                A_16_T12 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T12
                A_16_T13 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T13
                A_16_T14 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T14
                A_16_T15 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T15
                A_16_T16 = MonoModUtils.MethodToDelegateHelper.A_MethodGroup.A_16_T16
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...


        # Skipped F due to it being static, abstract and generic.

        F : F_MethodGroup
        class F_MethodGroup:
            @typing.overload
            def __getitem__(self, t:typing.Type[F_1_T1]) -> F_1[F_1_T1]: ...

            F_1_T1 = typing.TypeVar('F_1_T1')
            class F_1(typing.Generic[F_1_T1]):
                F_1_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_1_T1
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_2_T1], typing.Type[F_2_T2]]) -> F_2[F_2_T1, F_2_T2]: ...

            F_2_T1 = typing.TypeVar('F_2_T1')
            F_2_T2 = typing.TypeVar('F_2_T2')
            class F_2(typing.Generic[F_2_T1, F_2_T2]):
                F_2_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_2_T1
                F_2_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_2_T2
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_3_T1], typing.Type[F_3_T2], typing.Type[F_3_T3]]) -> F_3[F_3_T1, F_3_T2, F_3_T3]: ...

            F_3_T1 = typing.TypeVar('F_3_T1')
            F_3_T2 = typing.TypeVar('F_3_T2')
            F_3_T3 = typing.TypeVar('F_3_T3')
            class F_3(typing.Generic[F_3_T1, F_3_T2, F_3_T3]):
                F_3_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_3_T1
                F_3_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_3_T2
                F_3_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_3_T3
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_4_T1], typing.Type[F_4_T2], typing.Type[F_4_T3], typing.Type[F_4_T4]]) -> F_4[F_4_T1, F_4_T2, F_4_T3, F_4_T4]: ...

            F_4_T1 = typing.TypeVar('F_4_T1')
            F_4_T2 = typing.TypeVar('F_4_T2')
            F_4_T3 = typing.TypeVar('F_4_T3')
            F_4_T4 = typing.TypeVar('F_4_T4')
            class F_4(typing.Generic[F_4_T1, F_4_T2, F_4_T3, F_4_T4]):
                F_4_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_4_T1
                F_4_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_4_T2
                F_4_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_4_T3
                F_4_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_4_T4
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_5_T1], typing.Type[F_5_T2], typing.Type[F_5_T3], typing.Type[F_5_T4], typing.Type[F_5_T5]]) -> F_5[F_5_T1, F_5_T2, F_5_T3, F_5_T4, F_5_T5]: ...

            F_5_T1 = typing.TypeVar('F_5_T1')
            F_5_T2 = typing.TypeVar('F_5_T2')
            F_5_T3 = typing.TypeVar('F_5_T3')
            F_5_T4 = typing.TypeVar('F_5_T4')
            F_5_T5 = typing.TypeVar('F_5_T5')
            class F_5(typing.Generic[F_5_T1, F_5_T2, F_5_T3, F_5_T4, F_5_T5]):
                F_5_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_5_T1
                F_5_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_5_T2
                F_5_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_5_T3
                F_5_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_5_T4
                F_5_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_5_T5
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_6_T1], typing.Type[F_6_T2], typing.Type[F_6_T3], typing.Type[F_6_T4], typing.Type[F_6_T5], typing.Type[F_6_T6]]) -> F_6[F_6_T1, F_6_T2, F_6_T3, F_6_T4, F_6_T5, F_6_T6]: ...

            F_6_T1 = typing.TypeVar('F_6_T1')
            F_6_T2 = typing.TypeVar('F_6_T2')
            F_6_T3 = typing.TypeVar('F_6_T3')
            F_6_T4 = typing.TypeVar('F_6_T4')
            F_6_T5 = typing.TypeVar('F_6_T5')
            F_6_T6 = typing.TypeVar('F_6_T6')
            class F_6(typing.Generic[F_6_T1, F_6_T2, F_6_T3, F_6_T4, F_6_T5, F_6_T6]):
                F_6_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_6_T1
                F_6_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_6_T2
                F_6_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_6_T3
                F_6_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_6_T4
                F_6_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_6_T5
                F_6_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_6_T6
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_7_T1], typing.Type[F_7_T2], typing.Type[F_7_T3], typing.Type[F_7_T4], typing.Type[F_7_T5], typing.Type[F_7_T6], typing.Type[F_7_T7]]) -> F_7[F_7_T1, F_7_T2, F_7_T3, F_7_T4, F_7_T5, F_7_T6, F_7_T7]: ...

            F_7_T1 = typing.TypeVar('F_7_T1')
            F_7_T2 = typing.TypeVar('F_7_T2')
            F_7_T3 = typing.TypeVar('F_7_T3')
            F_7_T4 = typing.TypeVar('F_7_T4')
            F_7_T5 = typing.TypeVar('F_7_T5')
            F_7_T6 = typing.TypeVar('F_7_T6')
            F_7_T7 = typing.TypeVar('F_7_T7')
            class F_7(typing.Generic[F_7_T1, F_7_T2, F_7_T3, F_7_T4, F_7_T5, F_7_T6, F_7_T7]):
                F_7_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T1
                F_7_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T2
                F_7_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T3
                F_7_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T4
                F_7_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T5
                F_7_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T6
                F_7_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_7_T7
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_8_T1], typing.Type[F_8_T2], typing.Type[F_8_T3], typing.Type[F_8_T4], typing.Type[F_8_T5], typing.Type[F_8_T6], typing.Type[F_8_T7], typing.Type[F_8_T8]]) -> F_8[F_8_T1, F_8_T2, F_8_T3, F_8_T4, F_8_T5, F_8_T6, F_8_T7, F_8_T8]: ...

            F_8_T1 = typing.TypeVar('F_8_T1')
            F_8_T2 = typing.TypeVar('F_8_T2')
            F_8_T3 = typing.TypeVar('F_8_T3')
            F_8_T4 = typing.TypeVar('F_8_T4')
            F_8_T5 = typing.TypeVar('F_8_T5')
            F_8_T6 = typing.TypeVar('F_8_T6')
            F_8_T7 = typing.TypeVar('F_8_T7')
            F_8_T8 = typing.TypeVar('F_8_T8')
            class F_8(typing.Generic[F_8_T1, F_8_T2, F_8_T3, F_8_T4, F_8_T5, F_8_T6, F_8_T7, F_8_T8]):
                F_8_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T1
                F_8_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T2
                F_8_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T3
                F_8_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T4
                F_8_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T5
                F_8_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T6
                F_8_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T7
                F_8_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_8_T8
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_9_T1], typing.Type[F_9_T2], typing.Type[F_9_T3], typing.Type[F_9_T4], typing.Type[F_9_T5], typing.Type[F_9_T6], typing.Type[F_9_T7], typing.Type[F_9_T8], typing.Type[F_9_T9]]) -> F_9[F_9_T1, F_9_T2, F_9_T3, F_9_T4, F_9_T5, F_9_T6, F_9_T7, F_9_T8, F_9_T9]: ...

            F_9_T1 = typing.TypeVar('F_9_T1')
            F_9_T2 = typing.TypeVar('F_9_T2')
            F_9_T3 = typing.TypeVar('F_9_T3')
            F_9_T4 = typing.TypeVar('F_9_T4')
            F_9_T5 = typing.TypeVar('F_9_T5')
            F_9_T6 = typing.TypeVar('F_9_T6')
            F_9_T7 = typing.TypeVar('F_9_T7')
            F_9_T8 = typing.TypeVar('F_9_T8')
            F_9_T9 = typing.TypeVar('F_9_T9')
            class F_9(typing.Generic[F_9_T1, F_9_T2, F_9_T3, F_9_T4, F_9_T5, F_9_T6, F_9_T7, F_9_T8, F_9_T9]):
                F_9_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T1
                F_9_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T2
                F_9_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T3
                F_9_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T4
                F_9_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T5
                F_9_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T6
                F_9_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T7
                F_9_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T8
                F_9_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_9_T9
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_10_T1], typing.Type[F_10_T2], typing.Type[F_10_T3], typing.Type[F_10_T4], typing.Type[F_10_T5], typing.Type[F_10_T6], typing.Type[F_10_T7], typing.Type[F_10_T8], typing.Type[F_10_T9], typing.Type[F_10_T10]]) -> F_10[F_10_T1, F_10_T2, F_10_T3, F_10_T4, F_10_T5, F_10_T6, F_10_T7, F_10_T8, F_10_T9, F_10_T10]: ...

            F_10_T1 = typing.TypeVar('F_10_T1')
            F_10_T2 = typing.TypeVar('F_10_T2')
            F_10_T3 = typing.TypeVar('F_10_T3')
            F_10_T4 = typing.TypeVar('F_10_T4')
            F_10_T5 = typing.TypeVar('F_10_T5')
            F_10_T6 = typing.TypeVar('F_10_T6')
            F_10_T7 = typing.TypeVar('F_10_T7')
            F_10_T8 = typing.TypeVar('F_10_T8')
            F_10_T9 = typing.TypeVar('F_10_T9')
            F_10_T10 = typing.TypeVar('F_10_T10')
            class F_10(typing.Generic[F_10_T1, F_10_T2, F_10_T3, F_10_T4, F_10_T5, F_10_T6, F_10_T7, F_10_T8, F_10_T9, F_10_T10]):
                F_10_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T1
                F_10_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T2
                F_10_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T3
                F_10_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T4
                F_10_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T5
                F_10_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T6
                F_10_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T7
                F_10_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T8
                F_10_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T9
                F_10_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_10_T10
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_11_T1], typing.Type[F_11_T2], typing.Type[F_11_T3], typing.Type[F_11_T4], typing.Type[F_11_T5], typing.Type[F_11_T6], typing.Type[F_11_T7], typing.Type[F_11_T8], typing.Type[F_11_T9], typing.Type[F_11_T10], typing.Type[F_11_T11]]) -> F_11[F_11_T1, F_11_T2, F_11_T3, F_11_T4, F_11_T5, F_11_T6, F_11_T7, F_11_T8, F_11_T9, F_11_T10, F_11_T11]: ...

            F_11_T1 = typing.TypeVar('F_11_T1')
            F_11_T2 = typing.TypeVar('F_11_T2')
            F_11_T3 = typing.TypeVar('F_11_T3')
            F_11_T4 = typing.TypeVar('F_11_T4')
            F_11_T5 = typing.TypeVar('F_11_T5')
            F_11_T6 = typing.TypeVar('F_11_T6')
            F_11_T7 = typing.TypeVar('F_11_T7')
            F_11_T8 = typing.TypeVar('F_11_T8')
            F_11_T9 = typing.TypeVar('F_11_T9')
            F_11_T10 = typing.TypeVar('F_11_T10')
            F_11_T11 = typing.TypeVar('F_11_T11')
            class F_11(typing.Generic[F_11_T1, F_11_T2, F_11_T3, F_11_T4, F_11_T5, F_11_T6, F_11_T7, F_11_T8, F_11_T9, F_11_T10, F_11_T11]):
                F_11_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T1
                F_11_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T2
                F_11_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T3
                F_11_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T4
                F_11_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T5
                F_11_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T6
                F_11_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T7
                F_11_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T8
                F_11_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T9
                F_11_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T10
                F_11_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_11_T11
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_12_T1], typing.Type[F_12_T2], typing.Type[F_12_T3], typing.Type[F_12_T4], typing.Type[F_12_T5], typing.Type[F_12_T6], typing.Type[F_12_T7], typing.Type[F_12_T8], typing.Type[F_12_T9], typing.Type[F_12_T10], typing.Type[F_12_T11], typing.Type[F_12_T12]]) -> F_12[F_12_T1, F_12_T2, F_12_T3, F_12_T4, F_12_T5, F_12_T6, F_12_T7, F_12_T8, F_12_T9, F_12_T10, F_12_T11, F_12_T12]: ...

            F_12_T1 = typing.TypeVar('F_12_T1')
            F_12_T2 = typing.TypeVar('F_12_T2')
            F_12_T3 = typing.TypeVar('F_12_T3')
            F_12_T4 = typing.TypeVar('F_12_T4')
            F_12_T5 = typing.TypeVar('F_12_T5')
            F_12_T6 = typing.TypeVar('F_12_T6')
            F_12_T7 = typing.TypeVar('F_12_T7')
            F_12_T8 = typing.TypeVar('F_12_T8')
            F_12_T9 = typing.TypeVar('F_12_T9')
            F_12_T10 = typing.TypeVar('F_12_T10')
            F_12_T11 = typing.TypeVar('F_12_T11')
            F_12_T12 = typing.TypeVar('F_12_T12')
            class F_12(typing.Generic[F_12_T1, F_12_T2, F_12_T3, F_12_T4, F_12_T5, F_12_T6, F_12_T7, F_12_T8, F_12_T9, F_12_T10, F_12_T11, F_12_T12]):
                F_12_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T1
                F_12_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T2
                F_12_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T3
                F_12_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T4
                F_12_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T5
                F_12_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T6
                F_12_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T7
                F_12_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T8
                F_12_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T9
                F_12_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T10
                F_12_T11 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T11
                F_12_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_12_T12
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_13_T1], typing.Type[F_13_T2], typing.Type[F_13_T3], typing.Type[F_13_T4], typing.Type[F_13_T5], typing.Type[F_13_T6], typing.Type[F_13_T7], typing.Type[F_13_T8], typing.Type[F_13_T9], typing.Type[F_13_T10], typing.Type[F_13_T11], typing.Type[F_13_T12], typing.Type[F_13_T13]]) -> F_13[F_13_T1, F_13_T2, F_13_T3, F_13_T4, F_13_T5, F_13_T6, F_13_T7, F_13_T8, F_13_T9, F_13_T10, F_13_T11, F_13_T12, F_13_T13]: ...

            F_13_T1 = typing.TypeVar('F_13_T1')
            F_13_T2 = typing.TypeVar('F_13_T2')
            F_13_T3 = typing.TypeVar('F_13_T3')
            F_13_T4 = typing.TypeVar('F_13_T4')
            F_13_T5 = typing.TypeVar('F_13_T5')
            F_13_T6 = typing.TypeVar('F_13_T6')
            F_13_T7 = typing.TypeVar('F_13_T7')
            F_13_T8 = typing.TypeVar('F_13_T8')
            F_13_T9 = typing.TypeVar('F_13_T9')
            F_13_T10 = typing.TypeVar('F_13_T10')
            F_13_T11 = typing.TypeVar('F_13_T11')
            F_13_T12 = typing.TypeVar('F_13_T12')
            F_13_T13 = typing.TypeVar('F_13_T13')
            class F_13(typing.Generic[F_13_T1, F_13_T2, F_13_T3, F_13_T4, F_13_T5, F_13_T6, F_13_T7, F_13_T8, F_13_T9, F_13_T10, F_13_T11, F_13_T12, F_13_T13]):
                F_13_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T1
                F_13_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T2
                F_13_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T3
                F_13_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T4
                F_13_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T5
                F_13_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T6
                F_13_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T7
                F_13_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T8
                F_13_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T9
                F_13_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T10
                F_13_T11 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T11
                F_13_T12 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T12
                F_13_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_13_T13
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_14_T1], typing.Type[F_14_T2], typing.Type[F_14_T3], typing.Type[F_14_T4], typing.Type[F_14_T5], typing.Type[F_14_T6], typing.Type[F_14_T7], typing.Type[F_14_T8], typing.Type[F_14_T9], typing.Type[F_14_T10], typing.Type[F_14_T11], typing.Type[F_14_T12], typing.Type[F_14_T13], typing.Type[F_14_T14]]) -> F_14[F_14_T1, F_14_T2, F_14_T3, F_14_T4, F_14_T5, F_14_T6, F_14_T7, F_14_T8, F_14_T9, F_14_T10, F_14_T11, F_14_T12, F_14_T13, F_14_T14]: ...

            F_14_T1 = typing.TypeVar('F_14_T1')
            F_14_T2 = typing.TypeVar('F_14_T2')
            F_14_T3 = typing.TypeVar('F_14_T3')
            F_14_T4 = typing.TypeVar('F_14_T4')
            F_14_T5 = typing.TypeVar('F_14_T5')
            F_14_T6 = typing.TypeVar('F_14_T6')
            F_14_T7 = typing.TypeVar('F_14_T7')
            F_14_T8 = typing.TypeVar('F_14_T8')
            F_14_T9 = typing.TypeVar('F_14_T9')
            F_14_T10 = typing.TypeVar('F_14_T10')
            F_14_T11 = typing.TypeVar('F_14_T11')
            F_14_T12 = typing.TypeVar('F_14_T12')
            F_14_T13 = typing.TypeVar('F_14_T13')
            F_14_T14 = typing.TypeVar('F_14_T14')
            class F_14(typing.Generic[F_14_T1, F_14_T2, F_14_T3, F_14_T4, F_14_T5, F_14_T6, F_14_T7, F_14_T8, F_14_T9, F_14_T10, F_14_T11, F_14_T12, F_14_T13, F_14_T14]):
                F_14_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T1
                F_14_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T2
                F_14_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T3
                F_14_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T4
                F_14_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T5
                F_14_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T6
                F_14_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T7
                F_14_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T8
                F_14_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T9
                F_14_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T10
                F_14_T11 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T11
                F_14_T12 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T12
                F_14_T13 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T13
                F_14_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_14_T14
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_15_T1], typing.Type[F_15_T2], typing.Type[F_15_T3], typing.Type[F_15_T4], typing.Type[F_15_T5], typing.Type[F_15_T6], typing.Type[F_15_T7], typing.Type[F_15_T8], typing.Type[F_15_T9], typing.Type[F_15_T10], typing.Type[F_15_T11], typing.Type[F_15_T12], typing.Type[F_15_T13], typing.Type[F_15_T14], typing.Type[F_15_T15]]) -> F_15[F_15_T1, F_15_T2, F_15_T3, F_15_T4, F_15_T5, F_15_T6, F_15_T7, F_15_T8, F_15_T9, F_15_T10, F_15_T11, F_15_T12, F_15_T13, F_15_T14, F_15_T15]: ...

            F_15_T1 = typing.TypeVar('F_15_T1')
            F_15_T2 = typing.TypeVar('F_15_T2')
            F_15_T3 = typing.TypeVar('F_15_T3')
            F_15_T4 = typing.TypeVar('F_15_T4')
            F_15_T5 = typing.TypeVar('F_15_T5')
            F_15_T6 = typing.TypeVar('F_15_T6')
            F_15_T7 = typing.TypeVar('F_15_T7')
            F_15_T8 = typing.TypeVar('F_15_T8')
            F_15_T9 = typing.TypeVar('F_15_T9')
            F_15_T10 = typing.TypeVar('F_15_T10')
            F_15_T11 = typing.TypeVar('F_15_T11')
            F_15_T12 = typing.TypeVar('F_15_T12')
            F_15_T13 = typing.TypeVar('F_15_T13')
            F_15_T14 = typing.TypeVar('F_15_T14')
            F_15_T15 = typing.TypeVar('F_15_T15')
            class F_15(typing.Generic[F_15_T1, F_15_T2, F_15_T3, F_15_T4, F_15_T5, F_15_T6, F_15_T7, F_15_T8, F_15_T9, F_15_T10, F_15_T11, F_15_T12, F_15_T13, F_15_T14, F_15_T15]):
                F_15_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T1
                F_15_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T2
                F_15_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T3
                F_15_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T4
                F_15_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T5
                F_15_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T6
                F_15_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T7
                F_15_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T8
                F_15_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T9
                F_15_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T10
                F_15_T11 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T11
                F_15_T12 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T12
                F_15_T13 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T13
                F_15_T14 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T14
                F_15_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_15_T15
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_16_T1], typing.Type[F_16_T2], typing.Type[F_16_T3], typing.Type[F_16_T4], typing.Type[F_16_T5], typing.Type[F_16_T6], typing.Type[F_16_T7], typing.Type[F_16_T8], typing.Type[F_16_T9], typing.Type[F_16_T10], typing.Type[F_16_T11], typing.Type[F_16_T12], typing.Type[F_16_T13], typing.Type[F_16_T14], typing.Type[F_16_T15], typing.Type[F_16_T16]]) -> F_16[F_16_T1, F_16_T2, F_16_T3, F_16_T4, F_16_T5, F_16_T6, F_16_T7, F_16_T8, F_16_T9, F_16_T10, F_16_T11, F_16_T12, F_16_T13, F_16_T14, F_16_T15, F_16_T16]: ...

            F_16_T1 = typing.TypeVar('F_16_T1')
            F_16_T2 = typing.TypeVar('F_16_T2')
            F_16_T3 = typing.TypeVar('F_16_T3')
            F_16_T4 = typing.TypeVar('F_16_T4')
            F_16_T5 = typing.TypeVar('F_16_T5')
            F_16_T6 = typing.TypeVar('F_16_T6')
            F_16_T7 = typing.TypeVar('F_16_T7')
            F_16_T8 = typing.TypeVar('F_16_T8')
            F_16_T9 = typing.TypeVar('F_16_T9')
            F_16_T10 = typing.TypeVar('F_16_T10')
            F_16_T11 = typing.TypeVar('F_16_T11')
            F_16_T12 = typing.TypeVar('F_16_T12')
            F_16_T13 = typing.TypeVar('F_16_T13')
            F_16_T14 = typing.TypeVar('F_16_T14')
            F_16_T15 = typing.TypeVar('F_16_T15')
            F_16_T16 = typing.TypeVar('F_16_T16')
            class F_16(typing.Generic[F_16_T1, F_16_T2, F_16_T3, F_16_T4, F_16_T5, F_16_T6, F_16_T7, F_16_T8, F_16_T9, F_16_T10, F_16_T11, F_16_T12, F_16_T13, F_16_T14, F_16_T15, F_16_T16]):
                F_16_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T1
                F_16_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T2
                F_16_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T3
                F_16_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T4
                F_16_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T5
                F_16_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T6
                F_16_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T7
                F_16_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T8
                F_16_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T9
                F_16_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T10
                F_16_T11 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T11
                F_16_T12 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T12
                F_16_T13 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T13
                F_16_T14 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T14
                F_16_T15 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T15
                F_16_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_16_T16
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...

            @typing.overload
            def __getitem__(self, t:typing.Tuple[typing.Type[F_17_T1], typing.Type[F_17_T2], typing.Type[F_17_T3], typing.Type[F_17_T4], typing.Type[F_17_T5], typing.Type[F_17_T6], typing.Type[F_17_T7], typing.Type[F_17_T8], typing.Type[F_17_T9], typing.Type[F_17_T10], typing.Type[F_17_T11], typing.Type[F_17_T12], typing.Type[F_17_T13], typing.Type[F_17_T14], typing.Type[F_17_T15], typing.Type[F_17_T16], typing.Type[F_17_T17]]) -> F_17[F_17_T1, F_17_T2, F_17_T3, F_17_T4, F_17_T5, F_17_T6, F_17_T7, F_17_T8, F_17_T9, F_17_T10, F_17_T11, F_17_T12, F_17_T13, F_17_T14, F_17_T15, F_17_T16, F_17_T17]: ...

            F_17_T1 = typing.TypeVar('F_17_T1')
            F_17_T2 = typing.TypeVar('F_17_T2')
            F_17_T3 = typing.TypeVar('F_17_T3')
            F_17_T4 = typing.TypeVar('F_17_T4')
            F_17_T5 = typing.TypeVar('F_17_T5')
            F_17_T6 = typing.TypeVar('F_17_T6')
            F_17_T7 = typing.TypeVar('F_17_T7')
            F_17_T8 = typing.TypeVar('F_17_T8')
            F_17_T9 = typing.TypeVar('F_17_T9')
            F_17_T10 = typing.TypeVar('F_17_T10')
            F_17_T11 = typing.TypeVar('F_17_T11')
            F_17_T12 = typing.TypeVar('F_17_T12')
            F_17_T13 = typing.TypeVar('F_17_T13')
            F_17_T14 = typing.TypeVar('F_17_T14')
            F_17_T15 = typing.TypeVar('F_17_T15')
            F_17_T16 = typing.TypeVar('F_17_T16')
            F_17_T17 = typing.TypeVar('F_17_T17')
            class F_17(typing.Generic[F_17_T1, F_17_T2, F_17_T3, F_17_T4, F_17_T5, F_17_T6, F_17_T7, F_17_T8, F_17_T9, F_17_T10, F_17_T11, F_17_T12, F_17_T13, F_17_T14, F_17_T15, F_17_T16, F_17_T17]):
                F_17_T1 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T1
                F_17_T2 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T2
                F_17_T3 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T3
                F_17_T4 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T4
                F_17_T5 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T5
                F_17_T6 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T6
                F_17_T7 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T7
                F_17_T8 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T8
                F_17_T9 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T9
                F_17_T10 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T10
                F_17_T11 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T11
                F_17_T12 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T12
                F_17_T13 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T13
                F_17_T14 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T14
                F_17_T15 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T15
                F_17_T16 = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T16
                F_17_TResult = MonoModUtils.MethodToDelegateHelper.F_MethodGroup.F_17_T17
                def __call__(self, theInputMethod: typing.Any) -> Delegate:...



        class MyDel(MulticastDelegate):
            def __init__(self, object: typing.Any, method: int) -> None: ...
            @property
            def Method(self) -> MethodInfo: ...
            @property
            def Target(self) -> typing.Any: ...
            def BeginInvoke(self, arg1: SeedPacketsWidget, arg2: SeedType, arg3: clr.Reference[int], arg4: clr.Reference[int], callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
            def EndInvoke(self, arg3: clr.Reference[int], arg4: clr.Reference[int], result: IAsyncResult) -> None: ...
            def Invoke(self, arg1: SeedPacketsWidget, arg2: SeedType, arg3: clr.Reference[int], arg4: clr.Reference[int]) -> None: ...


        class MyDel_Outer(MulticastDelegate):
            def __init__(self, object: typing.Any, method: int) -> None: ...
            @property
            def Method(self) -> MethodInfo: ...
            @property
            def Target(self) -> typing.Any: ...
            def BeginInvoke(self, arg0: MonoModUtils.MethodToDelegateHelper.MyDel, arg1: SeedPacketsWidget, arg2: SeedType, arg3: clr.Reference[int], arg4: clr.Reference[int], callback: AsyncCallback, object: typing.Any) -> IAsyncResult: ...
            def EndInvoke(self, arg3: clr.Reference[int], arg4: clr.Reference[int], result: IAsyncResult) -> None: ...
            def Invoke(self, arg0: MonoModUtils.MethodToDelegateHelper.MyDel, arg1: SeedPacketsWidget, arg2: SeedType, arg3: clr.Reference[int], arg4: clr.Reference[int]) -> None: ...



