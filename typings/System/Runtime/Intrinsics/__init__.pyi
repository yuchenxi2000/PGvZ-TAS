import typing, abc
from System.Numerics import Vector2, Vector3, Vector4, Vector_1
from System import IEquatable_1

class Vector128_GenericClasses(abc.ABCMeta):
    Generic_Vector128_GenericClasses_Vector128_1_T = typing.TypeVar('Generic_Vector128_GenericClasses_Vector128_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector128_GenericClasses_Vector128_1_T]) -> typing.Type[Vector128_1[Generic_Vector128_GenericClasses_Vector128_1_T]]: ...

class Vector128(Vector128_0, metaclass =Vector128_GenericClasses): ...

class Vector128_0(abc.ABC):
    @staticmethod
    def AsVector2(value: Vector128_1[float]) -> Vector2: ...
    @staticmethod
    def AsVector3(value: Vector128_1[float]) -> Vector3: ...
    @staticmethod
    def AsVector4(value: Vector128_1[float]) -> Vector4: ...
    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_T = Vector128_0.As_MethodGroup.As_2_T1
            As_2_U = Vector128_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector128_1[As_2_T]) -> Vector128_1[As_2_U]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector128_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector128_1[AsByte_1_T]) -> Vector128_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector128_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector128_1[AsDouble_1_T]) -> Vector128_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector128_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector128_1[AsInt16_1_T]) -> Vector128_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector128_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector128_1[AsInt32_1_T]) -> Vector128_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector128_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector128_1[AsInt64_1_T]) -> Vector128_1[int]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector128_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector128_1[AsSByte_1_T]) -> Vector128_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector128_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector128_1[AsSingle_1_T]) -> Vector128_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector128_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector128_1[AsUInt16_1_T]) -> Vector128_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector128_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector128_1[AsUInt32_1_T]) -> Vector128_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector128_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector128_1[AsUInt64_1_T]) -> Vector128_1[int]:...


    # Skipped AsVector due to it being static, abstract and generic.

    AsVector : AsVector_MethodGroup
    class AsVector_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector_1_T1]) -> AsVector_1[AsVector_1_T1]: ...

        AsVector_1_T1 = typing.TypeVar('AsVector_1_T1')
        class AsVector_1(typing.Generic[AsVector_1_T1]):
            AsVector_1_T = Vector128_0.AsVector_MethodGroup.AsVector_1_T1
            def __call__(self, value: Vector128_1[AsVector_1_T]) -> Vector_1[AsVector_1_T]:...


    # Skipped AsVector128 due to it being static, abstract and generic.

    AsVector128 : AsVector128_MethodGroup
    class AsVector128_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector128_1_T1]) -> AsVector128_1[AsVector128_1_T1]: ...

        AsVector128_1_T1 = typing.TypeVar('AsVector128_1_T1')
        class AsVector128_1(typing.Generic[AsVector128_1_T1]):
            AsVector128_1_T = Vector128_0.AsVector128_MethodGroup.AsVector128_1_T1
            def __call__(self, value: Vector_1[AsVector128_1_T]) -> Vector128_1[AsVector128_1_T]:...

        @typing.overload
        def __call__(self, value: Vector2) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector3) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector4) -> Vector128_1[float]:...

    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        @typing.overload
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float) -> Vector128_1[float]:...
        # Method Create(e0 : Int64, e1 : Int64) was skipped since it collides with above method
        # Method Create(e0 : UInt64, e1 : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, lower: Vector64_1[float], upper: Vector64_1[float]) -> Vector128_1[float]:...
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float) -> Vector128_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32, e2 : Int32, e3 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32, e2 : UInt32, e3 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> Vector128_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16, e4 : UInt16, e5 : UInt16, e6 : UInt16, e7 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> Vector128_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte, e8 : SByte, e9 : SByte, e10 : SByte, e11 : SByte, e12 : SByte, e13 : SByte, e14 : SByte, e15 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method CreateScalarUnsafe(value : Single) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt64) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector128_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector128_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped GetLower due to it being static, abstract and generic.

    GetLower : GetLower_MethodGroup
    class GetLower_MethodGroup:
        def __getitem__(self, t:typing.Type[GetLower_1_T1]) -> GetLower_1[GetLower_1_T1]: ...

        GetLower_1_T1 = typing.TypeVar('GetLower_1_T1')
        class GetLower_1(typing.Generic[GetLower_1_T1]):
            GetLower_1_T = Vector128_0.GetLower_MethodGroup.GetLower_1_T1
            def __call__(self, vector: Vector128_1[GetLower_1_T]) -> Vector64_1[GetLower_1_T]:...


    # Skipped GetUpper due to it being static, abstract and generic.

    GetUpper : GetUpper_MethodGroup
    class GetUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[GetUpper_1_T1]) -> GetUpper_1[GetUpper_1_T1]: ...

        GetUpper_1_T1 = typing.TypeVar('GetUpper_1_T1')
        class GetUpper_1(typing.Generic[GetUpper_1_T1]):
            GetUpper_1_T = Vector128_0.GetUpper_MethodGroup.GetUpper_1_T1
            def __call__(self, vector: Vector128_1[GetUpper_1_T]) -> Vector64_1[GetUpper_1_T]:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector128_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector128_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped ToVector256 due to it being static, abstract and generic.

    ToVector256 : ToVector256_MethodGroup
    class ToVector256_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector256_1_T1]) -> ToVector256_1[ToVector256_1_T1]: ...

        ToVector256_1_T1 = typing.TypeVar('ToVector256_1_T1')
        class ToVector256_1(typing.Generic[ToVector256_1_T1]):
            ToVector256_1_T = Vector128_0.ToVector256_MethodGroup.ToVector256_1_T1
            def __call__(self, vector: Vector128_1[ToVector256_1_T]) -> Vector256_1[ToVector256_1_T]:...


    # Skipped ToVector256Unsafe due to it being static, abstract and generic.

    ToVector256Unsafe : ToVector256Unsafe_MethodGroup
    class ToVector256Unsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector256Unsafe_1_T1]) -> ToVector256Unsafe_1[ToVector256Unsafe_1_T1]: ...

        ToVector256Unsafe_1_T1 = typing.TypeVar('ToVector256Unsafe_1_T1')
        class ToVector256Unsafe_1(typing.Generic[ToVector256Unsafe_1_T1]):
            ToVector256Unsafe_1_T = Vector128_0.ToVector256Unsafe_MethodGroup.ToVector256Unsafe_1_T1
            def __call__(self, vector: Vector128_1[ToVector256Unsafe_1_T]) -> Vector256_1[ToVector256Unsafe_1_T]:...


    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector128_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector128_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector128_1[WithElement_1_T]:...


    # Skipped WithLower due to it being static, abstract and generic.

    WithLower : WithLower_MethodGroup
    class WithLower_MethodGroup:
        def __getitem__(self, t:typing.Type[WithLower_1_T1]) -> WithLower_1[WithLower_1_T1]: ...

        WithLower_1_T1 = typing.TypeVar('WithLower_1_T1')
        class WithLower_1(typing.Generic[WithLower_1_T1]):
            WithLower_1_T = Vector128_0.WithLower_MethodGroup.WithLower_1_T1
            def __call__(self, vector: Vector128_1[WithLower_1_T], value: Vector64_1[WithLower_1_T]) -> Vector128_1[WithLower_1_T]:...


    # Skipped WithUpper due to it being static, abstract and generic.

    WithUpper : WithUpper_MethodGroup
    class WithUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[WithUpper_1_T1]) -> WithUpper_1[WithUpper_1_T1]: ...

        WithUpper_1_T1 = typing.TypeVar('WithUpper_1_T1')
        class WithUpper_1(typing.Generic[WithUpper_1_T1]):
            WithUpper_1_T = Vector128_0.WithUpper_MethodGroup.WithUpper_1_T1
            def __call__(self, vector: Vector128_1[WithUpper_1_T], value: Vector64_1[WithUpper_1_T]) -> Vector128_1[WithUpper_1_T]:...




Vector128_1_T = typing.TypeVar('Vector128_1_T')
class Vector128_1(typing.Generic[Vector128_1_T], IEquatable_1[Vector128_1[Vector128_1_T]]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector128_1[Vector128_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Zero(cls) -> Vector128_1[Vector128_1_T]: ...
    def GetHashCode(self) -> int: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector128_1_T]
    Equals_MethodGroup_Vector128_1_T = typing.TypeVar('Equals_MethodGroup_Vector128_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector128_1_T]):
        Equals_MethodGroup_Vector128_1_T = Vector128_1.Equals_MethodGroup_Vector128_1_T
        @typing.overload
        def __call__(self, other: Vector128_1[Equals_MethodGroup_Vector128_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class Vector256_GenericClasses(abc.ABCMeta):
    Generic_Vector256_GenericClasses_Vector256_1_T = typing.TypeVar('Generic_Vector256_GenericClasses_Vector256_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector256_GenericClasses_Vector256_1_T]) -> typing.Type[Vector256_1[Generic_Vector256_GenericClasses_Vector256_1_T]]: ...

class Vector256(Vector256_0, metaclass =Vector256_GenericClasses): ...

class Vector256_0(abc.ABC):
    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_T = Vector256_0.As_MethodGroup.As_2_T1
            As_2_U = Vector256_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector256_1[As_2_T]) -> Vector256_1[As_2_U]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector256_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector256_1[AsByte_1_T]) -> Vector256_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector256_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector256_1[AsDouble_1_T]) -> Vector256_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector256_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector256_1[AsInt16_1_T]) -> Vector256_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector256_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector256_1[AsInt32_1_T]) -> Vector256_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector256_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector256_1[AsInt64_1_T]) -> Vector256_1[int]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector256_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector256_1[AsSByte_1_T]) -> Vector256_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector256_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector256_1[AsSingle_1_T]) -> Vector256_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector256_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector256_1[AsUInt16_1_T]) -> Vector256_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector256_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector256_1[AsUInt32_1_T]) -> Vector256_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector256_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector256_1[AsUInt64_1_T]) -> Vector256_1[int]:...


    # Skipped AsVector due to it being static, abstract and generic.

    AsVector : AsVector_MethodGroup
    class AsVector_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector_1_T1]) -> AsVector_1[AsVector_1_T1]: ...

        AsVector_1_T1 = typing.TypeVar('AsVector_1_T1')
        class AsVector_1(typing.Generic[AsVector_1_T1]):
            AsVector_1_T = Vector256_0.AsVector_MethodGroup.AsVector_1_T1
            def __call__(self, value: Vector256_1[AsVector_1_T]) -> Vector_1[AsVector_1_T]:...


    # Skipped AsVector256 due to it being static, abstract and generic.

    AsVector256 : AsVector256_MethodGroup
    class AsVector256_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector256_1_T1]) -> AsVector256_1[AsVector256_1_T1]: ...

        AsVector256_1_T1 = typing.TypeVar('AsVector256_1_T1')
        class AsVector256_1(typing.Generic[AsVector256_1_T1]):
            AsVector256_1_T = Vector256_0.AsVector256_MethodGroup.AsVector256_1_T1
            def __call__(self, value: Vector_1[AsVector256_1_T]) -> Vector256_1[AsVector256_1_T]:...


    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        @typing.overload
        def __call__(self, value: float) -> Vector256_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, lower: Vector128_1[float], upper: Vector128_1[float]) -> Vector256_1[float]:...
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float) -> Vector256_1[float]:...
        # Method Create(e0 : Int64, e1 : Int64, e2 : Int64, e3 : Int64) was skipped since it collides with above method
        # Method Create(e0 : UInt64, e1 : UInt64, e2 : UInt64, e3 : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float, e4: float, e5: float, e6: float, e7: float) -> Vector256_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32, e2 : Int32, e3 : Int32, e4 : Int32, e5 : Int32, e6 : Int32, e7 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32, e2 : UInt32, e3 : UInt32, e4 : UInt32, e5 : UInt32, e6 : UInt32, e7 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> Vector256_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16, e4 : UInt16, e5 : UInt16, e6 : UInt16, e7 : UInt16, e8 : UInt16, e9 : UInt16, e10 : UInt16, e11 : UInt16, e12 : UInt16, e13 : UInt16, e14 : UInt16, e15 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int, e16: int, e17: int, e18: int, e19: int, e20: int, e21: int, e22: int, e23: int, e24: int, e25: int, e26: int, e27: int, e28: int, e29: int, e30: int, e31: int) -> Vector256_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte, e8 : SByte, e9 : SByte, e10 : SByte, e11 : SByte, e12 : SByte, e13 : SByte, e14 : SByte, e15 : SByte, e16 : SByte, e17 : SByte, e18 : SByte, e19 : SByte, e20 : SByte, e21 : SByte, e22 : SByte, e23 : SByte, e24 : SByte, e25 : SByte, e26 : SByte, e27 : SByte, e28 : SByte, e29 : SByte, e30 : SByte, e31 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __call__(self, value: float) -> Vector256_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __call__(self, value: float) -> Vector256_1[float]:...
        # Method CreateScalarUnsafe(value : Single) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt64) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector256_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector256_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped GetLower due to it being static, abstract and generic.

    GetLower : GetLower_MethodGroup
    class GetLower_MethodGroup:
        def __getitem__(self, t:typing.Type[GetLower_1_T1]) -> GetLower_1[GetLower_1_T1]: ...

        GetLower_1_T1 = typing.TypeVar('GetLower_1_T1')
        class GetLower_1(typing.Generic[GetLower_1_T1]):
            GetLower_1_T = Vector256_0.GetLower_MethodGroup.GetLower_1_T1
            def __call__(self, vector: Vector256_1[GetLower_1_T]) -> Vector128_1[GetLower_1_T]:...


    # Skipped GetUpper due to it being static, abstract and generic.

    GetUpper : GetUpper_MethodGroup
    class GetUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[GetUpper_1_T1]) -> GetUpper_1[GetUpper_1_T1]: ...

        GetUpper_1_T1 = typing.TypeVar('GetUpper_1_T1')
        class GetUpper_1(typing.Generic[GetUpper_1_T1]):
            GetUpper_1_T = Vector256_0.GetUpper_MethodGroup.GetUpper_1_T1
            def __call__(self, vector: Vector256_1[GetUpper_1_T]) -> Vector128_1[GetUpper_1_T]:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector256_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector256_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector256_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector256_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector256_1[WithElement_1_T]:...


    # Skipped WithLower due to it being static, abstract and generic.

    WithLower : WithLower_MethodGroup
    class WithLower_MethodGroup:
        def __getitem__(self, t:typing.Type[WithLower_1_T1]) -> WithLower_1[WithLower_1_T1]: ...

        WithLower_1_T1 = typing.TypeVar('WithLower_1_T1')
        class WithLower_1(typing.Generic[WithLower_1_T1]):
            WithLower_1_T = Vector256_0.WithLower_MethodGroup.WithLower_1_T1
            def __call__(self, vector: Vector256_1[WithLower_1_T], value: Vector128_1[WithLower_1_T]) -> Vector256_1[WithLower_1_T]:...


    # Skipped WithUpper due to it being static, abstract and generic.

    WithUpper : WithUpper_MethodGroup
    class WithUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[WithUpper_1_T1]) -> WithUpper_1[WithUpper_1_T1]: ...

        WithUpper_1_T1 = typing.TypeVar('WithUpper_1_T1')
        class WithUpper_1(typing.Generic[WithUpper_1_T1]):
            WithUpper_1_T = Vector256_0.WithUpper_MethodGroup.WithUpper_1_T1
            def __call__(self, vector: Vector256_1[WithUpper_1_T], value: Vector128_1[WithUpper_1_T]) -> Vector256_1[WithUpper_1_T]:...




Vector256_1_T = typing.TypeVar('Vector256_1_T')
class Vector256_1(typing.Generic[Vector256_1_T], IEquatable_1[Vector256_1[Vector256_1_T]]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector256_1[Vector256_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Zero(cls) -> Vector256_1[Vector256_1_T]: ...
    def GetHashCode(self) -> int: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector256_1_T]
    Equals_MethodGroup_Vector256_1_T = typing.TypeVar('Equals_MethodGroup_Vector256_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector256_1_T]):
        Equals_MethodGroup_Vector256_1_T = Vector256_1.Equals_MethodGroup_Vector256_1_T
        @typing.overload
        def __call__(self, other: Vector256_1[Equals_MethodGroup_Vector256_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class Vector64_GenericClasses(abc.ABCMeta):
    Generic_Vector64_GenericClasses_Vector64_1_T = typing.TypeVar('Generic_Vector64_GenericClasses_Vector64_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector64_GenericClasses_Vector64_1_T]) -> typing.Type[Vector64_1[Generic_Vector64_GenericClasses_Vector64_1_T]]: ...

class Vector64(Vector64_0, metaclass =Vector64_GenericClasses): ...

class Vector64_0(abc.ABC):
    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_T = Vector64_0.As_MethodGroup.As_2_T1
            As_2_U = Vector64_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector64_1[As_2_T]) -> Vector64_1[As_2_U]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector64_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector64_1[AsByte_1_T]) -> Vector64_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector64_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector64_1[AsDouble_1_T]) -> Vector64_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector64_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector64_1[AsInt16_1_T]) -> Vector64_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector64_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector64_1[AsInt32_1_T]) -> Vector64_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector64_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector64_1[AsInt64_1_T]) -> Vector64_1[int]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector64_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector64_1[AsSByte_1_T]) -> Vector64_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector64_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector64_1[AsSingle_1_T]) -> Vector64_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector64_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector64_1[AsUInt16_1_T]) -> Vector64_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector64_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector64_1[AsUInt32_1_T]) -> Vector64_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector64_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector64_1[AsUInt64_1_T]) -> Vector64_1[int]:...


    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        @typing.overload
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float) -> Vector64_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int) -> Vector64_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> Vector64_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector64_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector64_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector64_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector64_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped ToVector128 due to it being static, abstract and generic.

    ToVector128 : ToVector128_MethodGroup
    class ToVector128_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector128_1_T1]) -> ToVector128_1[ToVector128_1_T1]: ...

        ToVector128_1_T1 = typing.TypeVar('ToVector128_1_T1')
        class ToVector128_1(typing.Generic[ToVector128_1_T1]):
            ToVector128_1_T = Vector64_0.ToVector128_MethodGroup.ToVector128_1_T1
            def __call__(self, vector: Vector64_1[ToVector128_1_T]) -> Vector128_1[ToVector128_1_T]:...


    # Skipped ToVector128Unsafe due to it being static, abstract and generic.

    ToVector128Unsafe : ToVector128Unsafe_MethodGroup
    class ToVector128Unsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector128Unsafe_1_T1]) -> ToVector128Unsafe_1[ToVector128Unsafe_1_T1]: ...

        ToVector128Unsafe_1_T1 = typing.TypeVar('ToVector128Unsafe_1_T1')
        class ToVector128Unsafe_1(typing.Generic[ToVector128Unsafe_1_T1]):
            ToVector128Unsafe_1_T = Vector64_0.ToVector128Unsafe_MethodGroup.ToVector128Unsafe_1_T1
            def __call__(self, vector: Vector64_1[ToVector128Unsafe_1_T]) -> Vector128_1[ToVector128Unsafe_1_T]:...


    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector64_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector64_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector64_1[WithElement_1_T]:...




Vector64_1_T = typing.TypeVar('Vector64_1_T')
class Vector64_1(typing.Generic[Vector64_1_T], IEquatable_1[Vector64_1[Vector64_1_T]]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector64_1[Vector64_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Zero(cls) -> Vector64_1[Vector64_1_T]: ...
    def GetHashCode(self) -> int: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector64_1_T]
    Equals_MethodGroup_Vector64_1_T = typing.TypeVar('Equals_MethodGroup_Vector64_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector64_1_T]):
        Equals_MethodGroup_Vector64_1_T = Vector64_1.Equals_MethodGroup_Vector64_1_T
        @typing.overload
        def __call__(self, other: Vector64_1[Equals_MethodGroup_Vector64_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...


