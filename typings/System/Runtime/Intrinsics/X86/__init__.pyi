import typing, clr, abc
from System.Runtime.Intrinsics import Vector128_1, Vector256_1
from System import ValueTuple_4

class Aes(Sse2):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def Decrypt(value: Vector128_1[int], roundKey: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def DecryptLast(value: Vector128_1[int], roundKey: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def Encrypt(value: Vector128_1[int], roundKey: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def EncryptLast(value: Vector128_1[int], roundKey: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def InverseMixColumns(value: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def KeygenAssist(value: Vector128_1[int], control: int) -> Vector128_1[int]: ...

    class X64(Sse2.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Avx(Sse42):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def BroadcastScalarToVector128(source: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def ConvertToVector128Int32(value: Vector256_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToVector128Int32WithTruncation(value: Vector256_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToVector128Single(value: Vector256_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def ConvertToVector256Int32(value: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToVector256Int32WithTruncation(value: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToVector256Single(value: Vector256_1[int]) -> Vector256_1[float]: ...
    @staticmethod
    def DotProduct(left: Vector256_1[float], right: Vector256_1[float], control: int) -> Vector256_1[float]: ...
    @staticmethod
    def DuplicateOddIndexed(value: Vector256_1[float]) -> Vector256_1[float]: ...
    @staticmethod
    def Reciprocal(value: Vector256_1[float]) -> Vector256_1[float]: ...
    @staticmethod
    def ReciprocalSqrt(value: Vector256_1[float]) -> Vector256_1[float]: ...
    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped AddSubtract due to it being static, abstract and generic.

    AddSubtract : AddSubtract_MethodGroup
    class AddSubtract_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method AddSubtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped And due to it being static, abstract and generic.

    And : And_MethodGroup
    class And_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Blend due to it being static, abstract and generic.

    Blend : Blend_MethodGroup
    class Blend_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float], control: int) -> Vector256_1[float]:...
        # Method Blend(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped BlendVariable due to it being static, abstract and generic.

    BlendVariable : BlendVariable_MethodGroup
    class BlendVariable_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float], mask: Vector256_1[float]) -> Vector256_1[float]:...
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method

    # Skipped BroadcastScalarToVector256 due to it being static, abstract and generic.

    BroadcastScalarToVector256 : BroadcastScalarToVector256_MethodGroup
    class BroadcastScalarToVector256_MethodGroup:
        def __call__(self, source: clr.Reference[float]) -> Vector256_1[float]:...
        # Method BroadcastScalarToVector256(source : Double*) was skipped since it collides with above method

    # Skipped BroadcastVector128ToVector256 due to it being static, abstract and generic.

    BroadcastVector128ToVector256 : BroadcastVector128ToVector256_MethodGroup
    class BroadcastVector128ToVector256_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector256_1[float]:...
        # Method BroadcastVector128ToVector256(address : Double*) was skipped since it collides with above method

    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Ceiling(value : Vector256`1) was skipped since it collides with above method

    # Skipped Compare due to it being static, abstract and generic.

    Compare : Compare_MethodGroup
    class Compare_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], mode: FloatComparisonMode) -> Vector128_1[float]:...
        # Method Compare(left : Vector128`1, right : Vector128`1, mode : FloatComparisonMode) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float], mode: FloatComparisonMode) -> Vector256_1[float]:...
        # Method Compare(left : Vector256`1, right : Vector256`1, mode : FloatComparisonMode) was skipped since it collides with above method

    # Skipped CompareEqual due to it being static, abstract and generic.

    CompareEqual : CompareEqual_MethodGroup
    class CompareEqual_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareGreaterThan due to it being static, abstract and generic.

    CompareGreaterThan : CompareGreaterThan_MethodGroup
    class CompareGreaterThan_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareGreaterThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareGreaterThanOrEqual due to it being static, abstract and generic.

    CompareGreaterThanOrEqual : CompareGreaterThanOrEqual_MethodGroup
    class CompareGreaterThanOrEqual_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareGreaterThanOrEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareLessThan due to it being static, abstract and generic.

    CompareLessThan : CompareLessThan_MethodGroup
    class CompareLessThan_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareLessThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareLessThanOrEqual due to it being static, abstract and generic.

    CompareLessThanOrEqual : CompareLessThanOrEqual_MethodGroup
    class CompareLessThanOrEqual_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareLessThanOrEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareNotEqual due to it being static, abstract and generic.

    CompareNotEqual : CompareNotEqual_MethodGroup
    class CompareNotEqual_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareNotEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareNotGreaterThan due to it being static, abstract and generic.

    CompareNotGreaterThan : CompareNotGreaterThan_MethodGroup
    class CompareNotGreaterThan_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareNotGreaterThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareNotGreaterThanOrEqual due to it being static, abstract and generic.

    CompareNotGreaterThanOrEqual : CompareNotGreaterThanOrEqual_MethodGroup
    class CompareNotGreaterThanOrEqual_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareNotGreaterThanOrEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareNotLessThan due to it being static, abstract and generic.

    CompareNotLessThan : CompareNotLessThan_MethodGroup
    class CompareNotLessThan_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareNotLessThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareNotLessThanOrEqual due to it being static, abstract and generic.

    CompareNotLessThanOrEqual : CompareNotLessThanOrEqual_MethodGroup
    class CompareNotLessThanOrEqual_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareNotLessThanOrEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareOrdered due to it being static, abstract and generic.

    CompareOrdered : CompareOrdered_MethodGroup
    class CompareOrdered_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareOrdered(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareScalar due to it being static, abstract and generic.

    CompareScalar : CompareScalar_MethodGroup
    class CompareScalar_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], mode: FloatComparisonMode) -> Vector128_1[float]:...
        # Method CompareScalar(left : Vector128`1, right : Vector128`1, mode : FloatComparisonMode) was skipped since it collides with above method

    # Skipped CompareUnordered due to it being static, abstract and generic.

    CompareUnordered : CompareUnordered_MethodGroup
    class CompareUnordered_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method CompareUnordered(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped ConvertToVector256Double due to it being static, abstract and generic.

    ConvertToVector256Double : ConvertToVector256Double_MethodGroup
    class ConvertToVector256Double_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector256_1[float]:...
        # Method ConvertToVector256Double(value : Vector128`1) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Divide(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped DuplicateEvenIndexed due to it being static, abstract and generic.

    DuplicateEvenIndexed : DuplicateEvenIndexed_MethodGroup
    class DuplicateEvenIndexed_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method DuplicateEvenIndexed(value : Vector256`1) was skipped since it collides with above method

    # Skipped ExtractVector128 due to it being static, abstract and generic.

    ExtractVector128 : ExtractVector128_MethodGroup
    class ExtractVector128_MethodGroup:
        def __call__(self, value: Vector256_1[float], index: int) -> Vector128_1[float]:...
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method

    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Floor(value : Vector256`1) was skipped since it collides with above method

    # Skipped HorizontalAdd due to it being static, abstract and generic.

    HorizontalAdd : HorizontalAdd_MethodGroup
    class HorizontalAdd_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method HorizontalAdd(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped HorizontalSubtract due to it being static, abstract and generic.

    HorizontalSubtract : HorizontalSubtract_MethodGroup
    class HorizontalSubtract_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method HorizontalSubtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped InsertVector128 due to it being static, abstract and generic.

    InsertVector128 : InsertVector128_MethodGroup
    class InsertVector128_MethodGroup:
        def __call__(self, value: Vector256_1[float], data: Vector128_1[float], index: int) -> Vector256_1[float]:...
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped LoadAlignedVector256 due to it being static, abstract and generic.

    LoadAlignedVector256 : LoadAlignedVector256_MethodGroup
    class LoadAlignedVector256_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector256_1[float]:...
        # Method LoadAlignedVector256(address : Double*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : SByte*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : Byte*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : Int16*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : UInt16*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : Int32*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : UInt32*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : Int64*) was skipped since it collides with above method
        # Method LoadAlignedVector256(address : UInt64*) was skipped since it collides with above method

    # Skipped LoadDquVector256 due to it being static, abstract and generic.

    LoadDquVector256 : LoadDquVector256_MethodGroup
    class LoadDquVector256_MethodGroup:
        def __call__(self, address: clr.Reference[int]) -> Vector256_1[int]:...
        # Method LoadDquVector256(address : Byte*) was skipped since it collides with above method
        # Method LoadDquVector256(address : Int16*) was skipped since it collides with above method
        # Method LoadDquVector256(address : UInt16*) was skipped since it collides with above method
        # Method LoadDquVector256(address : Int32*) was skipped since it collides with above method
        # Method LoadDquVector256(address : UInt32*) was skipped since it collides with above method
        # Method LoadDquVector256(address : Int64*) was skipped since it collides with above method
        # Method LoadDquVector256(address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVector256 due to it being static, abstract and generic.

    LoadVector256 : LoadVector256_MethodGroup
    class LoadVector256_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector256_1[float]:...
        # Method LoadVector256(address : Double*) was skipped since it collides with above method
        # Method LoadVector256(address : SByte*) was skipped since it collides with above method
        # Method LoadVector256(address : Byte*) was skipped since it collides with above method
        # Method LoadVector256(address : Int16*) was skipped since it collides with above method
        # Method LoadVector256(address : UInt16*) was skipped since it collides with above method
        # Method LoadVector256(address : Int32*) was skipped since it collides with above method
        # Method LoadVector256(address : UInt32*) was skipped since it collides with above method
        # Method LoadVector256(address : Int64*) was skipped since it collides with above method
        # Method LoadVector256(address : UInt64*) was skipped since it collides with above method

    # Skipped MaskLoad due to it being static, abstract and generic.

    MaskLoad : MaskLoad_MethodGroup
    class MaskLoad_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[float], mask: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MaskLoad(address : Double*, mask : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[float], mask: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MaskLoad(address : Double*, mask : Vector256`1) was skipped since it collides with above method

    # Skipped MaskStore due to it being static, abstract and generic.

    MaskStore : MaskStore_MethodGroup
    class MaskStore_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[float], mask: Vector128_1[float], source: Vector128_1[float]) -> None:...
        # Method MaskStore(address : Double*, mask : Vector128`1, source : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[float], mask: Vector256_1[float], source: Vector256_1[float]) -> None:...
        # Method MaskStore(address : Double*, mask : Vector256`1, source : Vector256`1) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Max(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Min(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped MoveMask due to it being static, abstract and generic.

    MoveMask : MoveMask_MethodGroup
    class MoveMask_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> int:...
        # Method MoveMask(value : Vector256`1) was skipped since it collides with above method

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Multiply(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Or due to it being static, abstract and generic.

    Or : Or_MethodGroup
    class Or_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Permute due to it being static, abstract and generic.

    Permute : Permute_MethodGroup
    class Permute_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float], control: int) -> Vector128_1[float]:...
        # Method Permute(value : Vector128`1, control : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector256_1[float], control: int) -> Vector256_1[float]:...
        # Method Permute(value : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped Permute2x128 due to it being static, abstract and generic.

    Permute2x128 : Permute2x128_MethodGroup
    class Permute2x128_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float], control: int) -> Vector256_1[float]:...
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped PermuteVar due to it being static, abstract and generic.

    PermuteVar : PermuteVar_MethodGroup
    class PermuteVar_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[float], control: Vector128_1[int]) -> Vector128_1[float]:...
        # Method PermuteVar(left : Vector128`1, control : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector256_1[float], control: Vector256_1[int]) -> Vector256_1[float]:...
        # Method PermuteVar(left : Vector256`1, control : Vector256`1) was skipped since it collides with above method

    # Skipped RoundCurrentDirection due to it being static, abstract and generic.

    RoundCurrentDirection : RoundCurrentDirection_MethodGroup
    class RoundCurrentDirection_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method RoundCurrentDirection(value : Vector256`1) was skipped since it collides with above method

    # Skipped RoundToNearestInteger due to it being static, abstract and generic.

    RoundToNearestInteger : RoundToNearestInteger_MethodGroup
    class RoundToNearestInteger_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method RoundToNearestInteger(value : Vector256`1) was skipped since it collides with above method

    # Skipped RoundToNegativeInfinity due to it being static, abstract and generic.

    RoundToNegativeInfinity : RoundToNegativeInfinity_MethodGroup
    class RoundToNegativeInfinity_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method RoundToNegativeInfinity(value : Vector256`1) was skipped since it collides with above method

    # Skipped RoundToPositiveInfinity due to it being static, abstract and generic.

    RoundToPositiveInfinity : RoundToPositiveInfinity_MethodGroup
    class RoundToPositiveInfinity_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method RoundToPositiveInfinity(value : Vector256`1) was skipped since it collides with above method

    # Skipped RoundToZero due to it being static, abstract and generic.

    RoundToZero : RoundToZero_MethodGroup
    class RoundToZero_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method RoundToZero(value : Vector256`1) was skipped since it collides with above method

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __call__(self, value: Vector256_1[float], right: Vector256_1[float], control: int) -> Vector256_1[float]:...
        # Method Shuffle(value : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped Sqrt due to it being static, abstract and generic.

    Sqrt : Sqrt_MethodGroup
    class Sqrt_MethodGroup:
        def __call__(self, value: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Sqrt(value : Vector256`1) was skipped since it collides with above method

    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector256_1[float]) -> None:...
        # Method Store(address : Double*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : SByte*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : Byte*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : Int16*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : UInt16*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : Int32*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : UInt32*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : Int64*, source : Vector256`1) was skipped since it collides with above method
        # Method Store(address : UInt64*, source : Vector256`1) was skipped since it collides with above method

    # Skipped StoreAligned due to it being static, abstract and generic.

    StoreAligned : StoreAligned_MethodGroup
    class StoreAligned_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector256_1[float]) -> None:...
        # Method StoreAligned(address : Double*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : SByte*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : Byte*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : Int16*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : UInt16*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : Int32*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : UInt32*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : Int64*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAligned(address : UInt64*, source : Vector256`1) was skipped since it collides with above method

    # Skipped StoreAlignedNonTemporal due to it being static, abstract and generic.

    StoreAlignedNonTemporal : StoreAlignedNonTemporal_MethodGroup
    class StoreAlignedNonTemporal_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector256_1[float]) -> None:...
        # Method StoreAlignedNonTemporal(address : Double*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : SByte*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Byte*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Int16*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : UInt16*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Int32*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : UInt32*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Int64*, source : Vector256`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : UInt64*, source : Vector256`1) was skipped since it collides with above method

    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped TestC due to it being static, abstract and generic.

    TestC : TestC_MethodGroup
    class TestC_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> bool:...
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> bool:...
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped TestNotZAndNotC due to it being static, abstract and generic.

    TestNotZAndNotC : TestNotZAndNotC_MethodGroup
    class TestNotZAndNotC_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> bool:...
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> bool:...
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped TestZ due to it being static, abstract and generic.

    TestZ : TestZ_MethodGroup
    class TestZ_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> bool:...
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> bool:...
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method TestZ(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped UnpackHigh due to it being static, abstract and generic.

    UnpackHigh : UnpackHigh_MethodGroup
    class UnpackHigh_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped UnpackLow due to it being static, abstract and generic.

    UnpackLow : UnpackLow_MethodGroup
    class UnpackLow_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method


    class X64(Sse42.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Avx2(Avx):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def ConvertToInt32(value: Vector256_1[int]) -> int: ...
    @staticmethod
    def ConvertToUInt32(value: Vector256_1[int]) -> int: ...
    @staticmethod
    def HorizontalAddSaturate(left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]: ...
    @staticmethod
    def HorizontalSubtractSaturate(left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]: ...
    @staticmethod
    def MultipleSumAbsoluteDifferences(left: Vector256_1[int], right: Vector256_1[int], mask: int) -> Vector256_1[int]: ...
    @staticmethod
    def MultiplyHighRoundScale(left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]: ...
    @staticmethod
    def SumAbsoluteDifferences(left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __call__(self, value: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Abs(value : Vector256`1) was skipped since it collides with above method
        # Method Abs(value : Vector256`1) was skipped since it collides with above method

    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Add(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method AddSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped AlignRight due to it being static, abstract and generic.

    AlignRight : AlignRight_MethodGroup
    class AlignRight_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int], mask: int) -> Vector256_1[int]:...
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector256`1, right : Vector256`1, mask : Byte) was skipped since it collides with above method

    # Skipped And due to it being static, abstract and generic.

    And : And_MethodGroup
    class And_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method And(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method AndNot(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Average due to it being static, abstract and generic.

    Average : Average_MethodGroup
    class Average_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Average(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Blend due to it being static, abstract and generic.

    Blend : Blend_MethodGroup
    class Blend_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], control: int) -> Vector128_1[int]:...
        # Method Blend(left : Vector128`1, right : Vector128`1, control : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int], control: int) -> Vector256_1[int]:...
        # Method Blend(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Blend(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Blend(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped BlendVariable due to it being static, abstract and generic.

    BlendVariable : BlendVariable_MethodGroup
    class BlendVariable_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int], mask: Vector256_1[int]) -> Vector256_1[int]:...
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector256`1, right : Vector256`1, mask : Vector256`1) was skipped since it collides with above method

    # Skipped BroadcastScalarToVector128 due to it being static, abstract and generic.

    BroadcastScalarToVector128 : BroadcastScalarToVector128_MethodGroup
    class BroadcastScalarToVector128_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, source: clr.Reference[int]) -> Vector128_1[int]:...
        # Method BroadcastScalarToVector128(source : SByte*) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(source : Int16*) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(source : UInt16*) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(source : Int32*) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(source : UInt32*) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(source : Int64*) was skipped since it collides with above method
        # Method BroadcastScalarToVector128(source : UInt64*) was skipped since it collides with above method

    # Skipped BroadcastScalarToVector256 due to it being static, abstract and generic.

    BroadcastScalarToVector256 : BroadcastScalarToVector256_MethodGroup
    class BroadcastScalarToVector256_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector256_1[float]:...
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, source: clr.Reference[int]) -> Vector256_1[int]:...
        # Method BroadcastScalarToVector256(source : Int16*) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(source : UInt16*) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(source : Int32*) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(source : UInt32*) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(source : Int64*) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(source : UInt64*) was skipped since it collides with above method
        # Method BroadcastScalarToVector256(source : Byte*) was skipped since it collides with above method

    # Skipped BroadcastVector128ToVector256 due to it being static, abstract and generic.

    BroadcastVector128ToVector256 : BroadcastVector128ToVector256_MethodGroup
    class BroadcastVector128ToVector256_MethodGroup:
        def __call__(self, address: clr.Reference[int]) -> Vector256_1[int]:...
        # Method BroadcastVector128ToVector256(address : Byte*) was skipped since it collides with above method
        # Method BroadcastVector128ToVector256(address : Int16*) was skipped since it collides with above method
        # Method BroadcastVector128ToVector256(address : UInt16*) was skipped since it collides with above method
        # Method BroadcastVector128ToVector256(address : Int32*) was skipped since it collides with above method
        # Method BroadcastVector128ToVector256(address : UInt32*) was skipped since it collides with above method
        # Method BroadcastVector128ToVector256(address : Int64*) was skipped since it collides with above method
        # Method BroadcastVector128ToVector256(address : UInt64*) was skipped since it collides with above method

    # Skipped CompareEqual due to it being static, abstract and generic.

    CompareEqual : CompareEqual_MethodGroup
    class CompareEqual_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped CompareGreaterThan due to it being static, abstract and generic.

    CompareGreaterThan : CompareGreaterThan_MethodGroup
    class CompareGreaterThan_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method CompareGreaterThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped ConvertToVector256Int16 due to it being static, abstract and generic.

    ConvertToVector256Int16 : ConvertToVector256Int16_MethodGroup
    class ConvertToVector256Int16_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector256_1[int]:...
        # Method ConvertToVector256Int16(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int]) -> Vector256_1[int]:...
        # Method ConvertToVector256Int16(address : Byte*) was skipped since it collides with above method

    # Skipped ConvertToVector256Int32 due to it being static, abstract and generic.

    ConvertToVector256Int32 : ConvertToVector256Int32_MethodGroup
    class ConvertToVector256Int32_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector256_1[int]:...
        # Method ConvertToVector256Int32(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector256Int32(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector256Int32(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int]) -> Vector256_1[int]:...
        # Method ConvertToVector256Int32(address : Byte*) was skipped since it collides with above method
        # Method ConvertToVector256Int32(address : Int16*) was skipped since it collides with above method
        # Method ConvertToVector256Int32(address : UInt16*) was skipped since it collides with above method

    # Skipped ConvertToVector256Int64 due to it being static, abstract and generic.

    ConvertToVector256Int64 : ConvertToVector256Int64_MethodGroup
    class ConvertToVector256Int64_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector256_1[int]:...
        # Method ConvertToVector256Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector256Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector256Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector256Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector256Int64(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int]) -> Vector256_1[int]:...
        # Method ConvertToVector256Int64(address : Byte*) was skipped since it collides with above method
        # Method ConvertToVector256Int64(address : Int16*) was skipped since it collides with above method
        # Method ConvertToVector256Int64(address : UInt16*) was skipped since it collides with above method
        # Method ConvertToVector256Int64(address : Int32*) was skipped since it collides with above method
        # Method ConvertToVector256Int64(address : UInt32*) was skipped since it collides with above method

    # Skipped ExtractVector128 due to it being static, abstract and generic.

    ExtractVector128 : ExtractVector128_MethodGroup
    class ExtractVector128_MethodGroup:
        def __call__(self, value: Vector256_1[int], index: int) -> Vector128_1[int]:...
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(value : Vector256`1, index : Byte) was skipped since it collides with above method

    # Skipped GatherMaskVector128 due to it being static, abstract and generic.

    GatherMaskVector128 : GatherMaskVector128_MethodGroup
    class GatherMaskVector128_MethodGroup:
        @typing.overload
        def __call__(self, source: Vector128_1[float], baseAddress: clr.Reference[float], index: Vector128_1[int], mask: Vector128_1[float], scale: int) -> Vector128_1[float]:...
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Double*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Single*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Double*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, source: Vector128_1[float], baseAddress: clr.Reference[float], index: Vector256_1[int], mask: Vector128_1[float], scale: int) -> Vector128_1[float]:...
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Int32*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : UInt32*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Int64*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : UInt64*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Int32*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : UInt32*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Int64*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : UInt64*, index : Vector128`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : Int32*, index : Vector256`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector128(source : Vector128`1, baseAddress : UInt32*, index : Vector256`1, mask : Vector128`1, scale : Byte) was skipped since it collides with above method

    # Skipped GatherMaskVector256 due to it being static, abstract and generic.

    GatherMaskVector256 : GatherMaskVector256_MethodGroup
    class GatherMaskVector256_MethodGroup:
        @typing.overload
        def __call__(self, source: Vector256_1[float], baseAddress: clr.Reference[float], index: Vector256_1[int], mask: Vector256_1[float], scale: int) -> Vector256_1[float]:...
        @typing.overload
        def __call__(self, source: Vector256_1[float], baseAddress: clr.Reference[float], index: Vector128_1[int], mask: Vector256_1[float], scale: int) -> Vector256_1[float]:...
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : Double*, index : Vector256`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : Int32*, index : Vector256`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : UInt32*, index : Vector256`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : Int64*, index : Vector128`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : UInt64*, index : Vector128`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : Int64*, index : Vector256`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherMaskVector256(source : Vector256`1, baseAddress : UInt64*, index : Vector256`1, mask : Vector256`1, scale : Byte) was skipped since it collides with above method

    # Skipped GatherVector128 due to it being static, abstract and generic.

    GatherVector128 : GatherVector128_MethodGroup
    class GatherVector128_MethodGroup:
        @typing.overload
        def __call__(self, baseAddress: clr.Reference[float], index: Vector128_1[int], scale: int) -> Vector128_1[float]:...
        # Method GatherVector128(baseAddress : Double*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : Single*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : Double*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, baseAddress: clr.Reference[float], index: Vector256_1[int], scale: int) -> Vector128_1[float]:...
        # Method GatherVector128(baseAddress : Int32*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : UInt32*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : Int64*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : UInt64*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : Int32*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : UInt32*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : Int64*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : UInt64*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : Int32*, index : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector128(baseAddress : UInt32*, index : Vector256`1, scale : Byte) was skipped since it collides with above method

    # Skipped GatherVector256 due to it being static, abstract and generic.

    GatherVector256 : GatherVector256_MethodGroup
    class GatherVector256_MethodGroup:
        @typing.overload
        def __call__(self, baseAddress: clr.Reference[float], index: Vector256_1[int], scale: int) -> Vector256_1[float]:...
        @typing.overload
        def __call__(self, baseAddress: clr.Reference[float], index: Vector128_1[int], scale: int) -> Vector256_1[float]:...
        # Method GatherVector256(baseAddress : Double*, index : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector256(baseAddress : Int32*, index : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector256(baseAddress : UInt32*, index : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector256(baseAddress : Int64*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector256(baseAddress : UInt64*, index : Vector128`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector256(baseAddress : Int64*, index : Vector256`1, scale : Byte) was skipped since it collides with above method
        # Method GatherVector256(baseAddress : UInt64*, index : Vector256`1, scale : Byte) was skipped since it collides with above method

    # Skipped HorizontalAdd due to it being static, abstract and generic.

    HorizontalAdd : HorizontalAdd_MethodGroup
    class HorizontalAdd_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method HorizontalAdd(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped HorizontalSubtract due to it being static, abstract and generic.

    HorizontalSubtract : HorizontalSubtract_MethodGroup
    class HorizontalSubtract_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method HorizontalSubtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped InsertVector128 due to it being static, abstract and generic.

    InsertVector128 : InsertVector128_MethodGroup
    class InsertVector128_MethodGroup:
        def __call__(self, value: Vector256_1[int], data: Vector128_1[int], index: int) -> Vector256_1[int]:...
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method InsertVector128(value : Vector256`1, data : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped LoadAlignedVector256NonTemporal due to it being static, abstract and generic.

    LoadAlignedVector256NonTemporal : LoadAlignedVector256NonTemporal_MethodGroup
    class LoadAlignedVector256NonTemporal_MethodGroup:
        def __call__(self, address: clr.Reference[int]) -> Vector256_1[int]:...
        # Method LoadAlignedVector256NonTemporal(address : Byte*) was skipped since it collides with above method
        # Method LoadAlignedVector256NonTemporal(address : Int16*) was skipped since it collides with above method
        # Method LoadAlignedVector256NonTemporal(address : UInt16*) was skipped since it collides with above method
        # Method LoadAlignedVector256NonTemporal(address : Int32*) was skipped since it collides with above method
        # Method LoadAlignedVector256NonTemporal(address : UInt32*) was skipped since it collides with above method
        # Method LoadAlignedVector256NonTemporal(address : Int64*) was skipped since it collides with above method
        # Method LoadAlignedVector256NonTemporal(address : UInt64*) was skipped since it collides with above method

    # Skipped MaskLoad due to it being static, abstract and generic.

    MaskLoad : MaskLoad_MethodGroup
    class MaskLoad_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[int], mask: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MaskLoad(address : UInt32*, mask : Vector128`1) was skipped since it collides with above method
        # Method MaskLoad(address : Int64*, mask : Vector128`1) was skipped since it collides with above method
        # Method MaskLoad(address : UInt64*, mask : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int], mask: Vector256_1[int]) -> Vector256_1[int]:...
        # Method MaskLoad(address : UInt32*, mask : Vector256`1) was skipped since it collides with above method
        # Method MaskLoad(address : Int64*, mask : Vector256`1) was skipped since it collides with above method
        # Method MaskLoad(address : UInt64*, mask : Vector256`1) was skipped since it collides with above method

    # Skipped MaskStore due to it being static, abstract and generic.

    MaskStore : MaskStore_MethodGroup
    class MaskStore_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[int], mask: Vector128_1[int], source: Vector128_1[int]) -> None:...
        # Method MaskStore(address : UInt32*, mask : Vector128`1, source : Vector128`1) was skipped since it collides with above method
        # Method MaskStore(address : Int64*, mask : Vector128`1, source : Vector128`1) was skipped since it collides with above method
        # Method MaskStore(address : UInt64*, mask : Vector128`1, source : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int], mask: Vector256_1[int], source: Vector256_1[int]) -> None:...
        # Method MaskStore(address : UInt32*, mask : Vector256`1, source : Vector256`1) was skipped since it collides with above method
        # Method MaskStore(address : Int64*, mask : Vector256`1, source : Vector256`1) was skipped since it collides with above method
        # Method MaskStore(address : UInt64*, mask : Vector256`1, source : Vector256`1) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Max(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Max(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Max(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Max(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Max(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Min(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Min(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Min(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Min(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Min(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped MoveMask due to it being static, abstract and generic.

    MoveMask : MoveMask_MethodGroup
    class MoveMask_MethodGroup:
        def __call__(self, value: Vector256_1[int]) -> int:...
        # Method MoveMask(value : Vector256`1) was skipped since it collides with above method

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Multiply(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplyAddAdjacent due to it being static, abstract and generic.

    MultiplyAddAdjacent : MultiplyAddAdjacent_MethodGroup
    class MultiplyAddAdjacent_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method MultiplyAddAdjacent(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplyHigh due to it being static, abstract and generic.

    MultiplyHigh : MultiplyHigh_MethodGroup
    class MultiplyHigh_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method MultiplyHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplyLow due to it being static, abstract and generic.

    MultiplyLow : MultiplyLow_MethodGroup
    class MultiplyLow_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method MultiplyLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method MultiplyLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method MultiplyLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Or due to it being static, abstract and generic.

    Or : Or_MethodGroup
    class Or_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Or(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped PackSignedSaturate due to it being static, abstract and generic.

    PackSignedSaturate : PackSignedSaturate_MethodGroup
    class PackSignedSaturate_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method PackSignedSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped PackUnsignedSaturate due to it being static, abstract and generic.

    PackUnsignedSaturate : PackUnsignedSaturate_MethodGroup
    class PackUnsignedSaturate_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method PackUnsignedSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Permute2x128 due to it being static, abstract and generic.

    Permute2x128 : Permute2x128_MethodGroup
    class Permute2x128_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int], control: int) -> Vector256_1[int]:...
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute2x128(left : Vector256`1, right : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped Permute4x64 due to it being static, abstract and generic.

    Permute4x64 : Permute4x64_MethodGroup
    class Permute4x64_MethodGroup:
        def __call__(self, value: Vector256_1[float], control: int) -> Vector256_1[float]:...
        # Method Permute4x64(value : Vector256`1, control : Byte) was skipped since it collides with above method
        # Method Permute4x64(value : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped PermuteVar8x32 due to it being static, abstract and generic.

    PermuteVar8x32 : PermuteVar8x32_MethodGroup
    class PermuteVar8x32_MethodGroup:
        def __call__(self, left: Vector256_1[float], control: Vector256_1[int]) -> Vector256_1[float]:...
        # Method PermuteVar8x32(left : Vector256`1, control : Vector256`1) was skipped since it collides with above method
        # Method PermuteVar8x32(left : Vector256`1, control : Vector256`1) was skipped since it collides with above method

    # Skipped ShiftLeftLogical due to it being static, abstract and generic.

    ShiftLeftLogical : ShiftLeftLogical_MethodGroup
    class ShiftLeftLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: int) -> Vector256_1[int]:...
        # Method ShiftLeftLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: Vector128_1[int]) -> Vector256_1[int]:...
        # Method ShiftLeftLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLeftLogical128BitLane due to it being static, abstract and generic.

    ShiftLeftLogical128BitLane : ShiftLeftLogical128BitLane_MethodGroup
    class ShiftLeftLogical128BitLane_MethodGroup:
        def __call__(self, value: Vector256_1[int], numBytes: int) -> Vector256_1[int]:...
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalVariable due to it being static, abstract and generic.

    ShiftLeftLogicalVariable : ShiftLeftLogicalVariable_MethodGroup
    class ShiftLeftLogicalVariable_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: Vector256_1[int]) -> Vector256_1[int]:...
        # Method ShiftLeftLogicalVariable(value : Vector256`1, count : Vector256`1) was skipped since it collides with above method
        # Method ShiftLeftLogicalVariable(value : Vector256`1, count : Vector256`1) was skipped since it collides with above method
        # Method ShiftLeftLogicalVariable(value : Vector256`1, count : Vector256`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftLeftLogicalVariable(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogicalVariable(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogicalVariable(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: int) -> Vector256_1[int]:...
        # Method ShiftRightArithmetic(value : Vector256`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: Vector128_1[int]) -> Vector256_1[int]:...
        # Method ShiftRightArithmetic(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticVariable due to it being static, abstract and generic.

    ShiftRightArithmeticVariable : ShiftRightArithmeticVariable_MethodGroup
    class ShiftRightArithmeticVariable_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: Vector256_1[int]) -> Vector256_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: int) -> Vector256_1[int]:...
        # Method ShiftRightLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: Vector128_1[int]) -> Vector256_1[int]:...
        # Method ShiftRightLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector256`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftRightLogical128BitLane due to it being static, abstract and generic.

    ShiftRightLogical128BitLane : ShiftRightLogical128BitLane_MethodGroup
    class ShiftRightLogical128BitLane_MethodGroup:
        def __call__(self, value: Vector256_1[int], numBytes: int) -> Vector256_1[int]:...
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector256`1, numBytes : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalVariable due to it being static, abstract and generic.

    ShiftRightLogicalVariable : ShiftRightLogicalVariable_MethodGroup
    class ShiftRightLogicalVariable_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], count: Vector256_1[int]) -> Vector256_1[int]:...
        # Method ShiftRightLogicalVariable(value : Vector256`1, count : Vector256`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftRightLogicalVariable(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogicalVariable(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogicalVariable(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogicalVariable(value : Vector256`1, count : Vector256`1) was skipped since it collides with above method
        # Method ShiftRightLogicalVariable(value : Vector256`1, count : Vector256`1) was skipped since it collides with above method

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector256_1[int], control: int) -> Vector256_1[int]:...
        # Method Shuffle(value : Vector256`1, control : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector256_1[int], mask: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Shuffle(value : Vector256`1, mask : Vector256`1) was skipped since it collides with above method

    # Skipped ShuffleHigh due to it being static, abstract and generic.

    ShuffleHigh : ShuffleHigh_MethodGroup
    class ShuffleHigh_MethodGroup:
        def __call__(self, value: Vector256_1[int], control: int) -> Vector256_1[int]:...
        # Method ShuffleHigh(value : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped ShuffleLow due to it being static, abstract and generic.

    ShuffleLow : ShuffleLow_MethodGroup
    class ShuffleLow_MethodGroup:
        def __call__(self, value: Vector256_1[int], control: int) -> Vector256_1[int]:...
        # Method ShuffleLow(value : Vector256`1, control : Byte) was skipped since it collides with above method

    # Skipped Sign due to it being static, abstract and generic.

    Sign : Sign_MethodGroup
    class Sign_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Sign(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Sign(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Subtract(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method SubtractSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped UnpackHigh due to it being static, abstract and generic.

    UnpackHigh : UnpackHigh_MethodGroup
    class UnpackHigh_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped UnpackLow due to it being static, abstract and generic.

    UnpackLow : UnpackLow_MethodGroup
    class UnpackLow_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __call__(self, left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method
        # Method Xor(left : Vector256`1, right : Vector256`1) was skipped since it collides with above method


    class X64(Avx.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class AvxVnni(Avx2):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    # Skipped MultiplyWideningAndAdd due to it being static, abstract and generic.

    MultiplyWideningAndAdd : MultiplyWideningAndAdd_MethodGroup
    class MultiplyWideningAndAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector256_1[int], left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method MultiplyWideningAndAdd(addend : Vector256`1, left : Vector256`1, right : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplyWideningAndAddSaturate due to it being static, abstract and generic.

    MultiplyWideningAndAddSaturate : MultiplyWideningAndAddSaturate_MethodGroup
    class MultiplyWideningAndAddSaturate_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningAndAddSaturate(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector256_1[int], left: Vector256_1[int], right: Vector256_1[int]) -> Vector256_1[int]:...
        # Method MultiplyWideningAndAddSaturate(addend : Vector256`1, left : Vector256`1, right : Vector256`1) was skipped since it collides with above method


    class X64(Avx2.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Bmi1(X86Base):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def AndNot(left: int, right: int) -> int: ...
    @staticmethod
    def ExtractLowestSetBit(value: int) -> int: ...
    @staticmethod
    def GetMaskUpToLowestSetBit(value: int) -> int: ...
    @staticmethod
    def ResetLowestSetBit(value: int) -> int: ...
    @staticmethod
    def TrailingZeroCount(value: int) -> int: ...
    # Skipped BitFieldExtract due to it being static, abstract and generic.

    BitFieldExtract : BitFieldExtract_MethodGroup
    class BitFieldExtract_MethodGroup:
        @typing.overload
        def __call__(self, value: int, control: int) -> int:...
        @typing.overload
        def __call__(self, value: int, start: int, length: int) -> int:...


    class X64(X86Base.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def AndNot(left: int, right: int) -> int: ...
        @staticmethod
        def ExtractLowestSetBit(value: int) -> int: ...
        @staticmethod
        def GetMaskUpToLowestSetBit(value: int) -> int: ...
        @staticmethod
        def ResetLowestSetBit(value: int) -> int: ...
        @staticmethod
        def TrailingZeroCount(value: int) -> int: ...
        # Skipped BitFieldExtract due to it being static, abstract and generic.

        BitFieldExtract : BitFieldExtract_MethodGroup
        class BitFieldExtract_MethodGroup:
            @typing.overload
            def __call__(self, value: int, control: int) -> int:...
            @typing.overload
            def __call__(self, value: int, start: int, length: int) -> int:...




class Bmi2(X86Base):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def ParallelBitDeposit(value: int, mask: int) -> int: ...
    @staticmethod
    def ParallelBitExtract(value: int, mask: int) -> int: ...
    @staticmethod
    def ZeroHighBits(value: int, index: int) -> int: ...
    # Skipped MultiplyNoFlags due to it being static, abstract and generic.

    MultiplyNoFlags : MultiplyNoFlags_MethodGroup
    class MultiplyNoFlags_MethodGroup:
        @typing.overload
        def __call__(self, left: int, right: int) -> int:...
        @typing.overload
        def __call__(self, left: int, right: int, low: clr.Reference[int]) -> int:...


    class X64(X86Base.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def ParallelBitDeposit(value: int, mask: int) -> int: ...
        @staticmethod
        def ParallelBitExtract(value: int, mask: int) -> int: ...
        @staticmethod
        def ZeroHighBits(value: int, index: int) -> int: ...
        # Skipped MultiplyNoFlags due to it being static, abstract and generic.

        MultiplyNoFlags : MultiplyNoFlags_MethodGroup
        class MultiplyNoFlags_MethodGroup:
            @typing.overload
            def __call__(self, left: int, right: int) -> int:...
            @typing.overload
            def __call__(self, left: int, right: int, low: clr.Reference[int]) -> int:...




class FloatComparisonMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    OrderedEqualNonSignaling : FloatComparisonMode # 0
    OrderedLessThanSignaling : FloatComparisonMode # 1
    OrderedLessThanOrEqualSignaling : FloatComparisonMode # 2
    UnorderedNonSignaling : FloatComparisonMode # 3
    UnorderedNotEqualNonSignaling : FloatComparisonMode # 4
    UnorderedNotLessThanSignaling : FloatComparisonMode # 5
    UnorderedNotLessThanOrEqualSignaling : FloatComparisonMode # 6
    OrderedNonSignaling : FloatComparisonMode # 7
    UnorderedEqualNonSignaling : FloatComparisonMode # 8
    UnorderedNotGreaterThanOrEqualSignaling : FloatComparisonMode # 9
    UnorderedNotGreaterThanSignaling : FloatComparisonMode # 10
    OrderedFalseNonSignaling : FloatComparisonMode # 11
    OrderedNotEqualNonSignaling : FloatComparisonMode # 12
    OrderedGreaterThanOrEqualSignaling : FloatComparisonMode # 13
    OrderedGreaterThanSignaling : FloatComparisonMode # 14
    UnorderedTrueNonSignaling : FloatComparisonMode # 15
    OrderedEqualSignaling : FloatComparisonMode # 16
    OrderedLessThanNonSignaling : FloatComparisonMode # 17
    OrderedLessThanOrEqualNonSignaling : FloatComparisonMode # 18
    UnorderedSignaling : FloatComparisonMode # 19
    UnorderedNotEqualSignaling : FloatComparisonMode # 20
    UnorderedNotLessThanNonSignaling : FloatComparisonMode # 21
    UnorderedNotLessThanOrEqualNonSignaling : FloatComparisonMode # 22
    OrderedSignaling : FloatComparisonMode # 23
    UnorderedEqualSignaling : FloatComparisonMode # 24
    UnorderedNotGreaterThanOrEqualNonSignaling : FloatComparisonMode # 25
    UnorderedNotGreaterThanNonSignaling : FloatComparisonMode # 26
    OrderedFalseSignaling : FloatComparisonMode # 27
    OrderedNotEqualSignaling : FloatComparisonMode # 28
    OrderedGreaterThanOrEqualNonSignaling : FloatComparisonMode # 29
    OrderedGreaterThanNonSignaling : FloatComparisonMode # 30
    UnorderedTrueSignaling : FloatComparisonMode # 31


class Fma(Avx):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    # Skipped MultiplyAdd due to it being static, abstract and generic.

    MultiplyAdd : MultiplyAdd_MethodGroup
    class MultiplyAdd_MethodGroup:
        @typing.overload
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplyAdd(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, a: Vector256_1[float], b: Vector256_1[float], c: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplyAdd(a : Vector256`1, b : Vector256`1, c : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplyAddNegated due to it being static, abstract and generic.

    MultiplyAddNegated : MultiplyAddNegated_MethodGroup
    class MultiplyAddNegated_MethodGroup:
        @typing.overload
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplyAddNegated(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, a: Vector256_1[float], b: Vector256_1[float], c: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplyAddNegated(a : Vector256`1, b : Vector256`1, c : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplyAddNegatedScalar due to it being static, abstract and generic.

    MultiplyAddNegatedScalar : MultiplyAddNegatedScalar_MethodGroup
    class MultiplyAddNegatedScalar_MethodGroup:
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplyAddNegatedScalar(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyAddScalar due to it being static, abstract and generic.

    MultiplyAddScalar : MultiplyAddScalar_MethodGroup
    class MultiplyAddScalar_MethodGroup:
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplyAddScalar(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyAddSubtract due to it being static, abstract and generic.

    MultiplyAddSubtract : MultiplyAddSubtract_MethodGroup
    class MultiplyAddSubtract_MethodGroup:
        @typing.overload
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplyAddSubtract(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, a: Vector256_1[float], b: Vector256_1[float], c: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplyAddSubtract(a : Vector256`1, b : Vector256`1, c : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplySubtract due to it being static, abstract and generic.

    MultiplySubtract : MultiplySubtract_MethodGroup
    class MultiplySubtract_MethodGroup:
        @typing.overload
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplySubtract(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, a: Vector256_1[float], b: Vector256_1[float], c: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplySubtract(a : Vector256`1, b : Vector256`1, c : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplySubtractAdd due to it being static, abstract and generic.

    MultiplySubtractAdd : MultiplySubtractAdd_MethodGroup
    class MultiplySubtractAdd_MethodGroup:
        @typing.overload
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplySubtractAdd(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, a: Vector256_1[float], b: Vector256_1[float], c: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplySubtractAdd(a : Vector256`1, b : Vector256`1, c : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplySubtractNegated due to it being static, abstract and generic.

    MultiplySubtractNegated : MultiplySubtractNegated_MethodGroup
    class MultiplySubtractNegated_MethodGroup:
        @typing.overload
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplySubtractNegated(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, a: Vector256_1[float], b: Vector256_1[float], c: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplySubtractNegated(a : Vector256`1, b : Vector256`1, c : Vector256`1) was skipped since it collides with above method

    # Skipped MultiplySubtractNegatedScalar due to it being static, abstract and generic.

    MultiplySubtractNegatedScalar : MultiplySubtractNegatedScalar_MethodGroup
    class MultiplySubtractNegatedScalar_MethodGroup:
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplySubtractNegatedScalar(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplySubtractScalar due to it being static, abstract and generic.

    MultiplySubtractScalar : MultiplySubtractScalar_MethodGroup
    class MultiplySubtractScalar_MethodGroup:
        def __call__(self, a: Vector128_1[float], b: Vector128_1[float], c: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplySubtractScalar(a : Vector128`1, b : Vector128`1, c : Vector128`1) was skipped since it collides with above method


    class X64(Avx.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Lzcnt(X86Base):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def LeadingZeroCount(value: int) -> int: ...

    class X64(X86Base.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def LeadingZeroCount(value: int) -> int: ...



class Pclmulqdq(Sse2):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    # Skipped CarrylessMultiply due to it being static, abstract and generic.

    CarrylessMultiply : CarrylessMultiply_MethodGroup
    class CarrylessMultiply_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], control: int) -> Vector128_1[int]:...
        # Method CarrylessMultiply(left : Vector128`1, right : Vector128`1, control : Byte) was skipped since it collides with above method


    class X64(Sse2.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Popcnt(Sse42):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def PopCount(value: int) -> int: ...

    class X64(Sse42.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def PopCount(value: int) -> int: ...



class Sse(X86Base):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def Add(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def AddScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def And(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def AndNot(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareOrdered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarOrdered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarOrderedEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnordered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarUnorderedEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareUnordered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def ConvertScalarToVector128Single(upper: Vector128_1[float], value: int) -> Vector128_1[float]: ...
    @staticmethod
    def ConvertToInt32(value: Vector128_1[float]) -> int: ...
    @staticmethod
    def ConvertToInt32WithTruncation(value: Vector128_1[float]) -> int: ...
    @staticmethod
    def Divide(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def DivideScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def LoadAlignedVector128(address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def LoadHigh(lower: Vector128_1[float], address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def LoadLow(upper: Vector128_1[float], address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def LoadScalarVector128(address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def LoadVector128(address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Max(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MaxScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Min(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MinScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MoveHighToLow(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MoveLowToHigh(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MoveMask(value: Vector128_1[float]) -> int: ...
    @staticmethod
    def MoveScalar(upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Multiply(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MultiplyScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Or(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Prefetch0(address: clr.Reference[None]) -> None: ...
    @staticmethod
    def Prefetch1(address: clr.Reference[None]) -> None: ...
    @staticmethod
    def Prefetch2(address: clr.Reference[None]) -> None: ...
    @staticmethod
    def PrefetchNonTemporal(address: clr.Reference[None]) -> None: ...
    @staticmethod
    def Reciprocal(value: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def ReciprocalSqrt(value: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Shuffle(left: Vector128_1[float], right: Vector128_1[float], control: int) -> Vector128_1[float]: ...
    @staticmethod
    def Sqrt(value: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Store(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def StoreAligned(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def StoreAlignedNonTemporal(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def StoreFence() -> None: ...
    @staticmethod
    def StoreHigh(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def StoreLow(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def StoreScalar(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def Subtract(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def SubtractScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def UnpackHigh(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def UnpackLow(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Xor(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    # Skipped ReciprocalScalar due to it being static, abstract and generic.

    ReciprocalScalar : ReciprocalScalar_MethodGroup
    class ReciprocalScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped ReciprocalSqrtScalar due to it being static, abstract and generic.

    ReciprocalSqrtScalar : ReciprocalSqrtScalar_MethodGroup
    class ReciprocalSqrtScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped SqrtScalar due to it being static, abstract and generic.

    SqrtScalar : SqrtScalar_MethodGroup
    class SqrtScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...


    class X64(X86Base.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def ConvertScalarToVector128Single(upper: Vector128_1[float], value: int) -> Vector128_1[float]: ...
        @staticmethod
        def ConvertToInt64(value: Vector128_1[float]) -> int: ...
        @staticmethod
        def ConvertToInt64WithTruncation(value: Vector128_1[float]) -> int: ...



class Sse2(Sse):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def AddScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareNotLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareOrdered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarNotLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarOrdered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarOrderedEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarOrderedNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnordered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def CompareScalarUnorderedEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareScalarUnorderedNotEqual(left: Vector128_1[float], right: Vector128_1[float]) -> bool: ...
    @staticmethod
    def CompareUnordered(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def ConvertScalarToVector128Int32(value: int) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertScalarToVector128Single(upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def ConvertScalarToVector128UInt32(value: int) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToInt32WithTruncation(value: Vector128_1[float]) -> int: ...
    @staticmethod
    def ConvertToUInt32(value: Vector128_1[int]) -> int: ...
    @staticmethod
    def Divide(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def DivideScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def Extract(value: Vector128_1[int], index: int) -> int: ...
    @staticmethod
    def LoadFence() -> None: ...
    @staticmethod
    def LoadHigh(lower: Vector128_1[float], address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def LoadLow(upper: Vector128_1[float], address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MaxScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MemoryFence() -> None: ...
    @staticmethod
    def MinScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MultiplyAddAdjacent(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def MultiplyScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def PackUnsignedSaturate(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def Sqrt(value: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def StoreHigh(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def StoreLow(address: clr.Reference[float], source: Vector128_1[float]) -> None: ...
    @staticmethod
    def SubtractScalar(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def SumAbsoluteDifferences(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped And due to it being static, abstract and generic.

    And : And_MethodGroup
    class And_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AndNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Average due to it being static, abstract and generic.

    Average : Average_MethodGroup
    class Average_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method Average(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareEqual due to it being static, abstract and generic.

    CompareEqual : CompareEqual_MethodGroup
    class CompareEqual_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareGreaterThan due to it being static, abstract and generic.

    CompareGreaterThan : CompareGreaterThan_MethodGroup
    class CompareGreaterThan_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareLessThan due to it being static, abstract and generic.

    CompareLessThan : CompareLessThan_MethodGroup
    class CompareLessThan_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertScalarToVector128Double due to it being static, abstract and generic.

    ConvertScalarToVector128Double : ConvertScalarToVector128Double_MethodGroup
    class ConvertScalarToVector128Double_MethodGroup:
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: int) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped ConvertToInt32 due to it being static, abstract and generic.

    ConvertToInt32 : ConvertToInt32_MethodGroup
    class ConvertToInt32_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> int:...
        # Method ConvertToInt32(value : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToVector128Double due to it being static, abstract and generic.

    ConvertToVector128Double : ConvertToVector128Double_MethodGroup
    class ConvertToVector128Double_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method ConvertToVector128Double(value : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToVector128Int32 due to it being static, abstract and generic.

    ConvertToVector128Int32 : ConvertToVector128Int32_MethodGroup
    class ConvertToVector128Int32_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int32(value : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToVector128Int32WithTruncation due to it being static, abstract and generic.

    ConvertToVector128Int32WithTruncation : ConvertToVector128Int32WithTruncation_MethodGroup
    class ConvertToVector128Int32WithTruncation_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int32WithTruncation(value : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToVector128Single due to it being static, abstract and generic.

    ConvertToVector128Single : ConvertToVector128Single_MethodGroup
    class ConvertToVector128Single_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method ConvertToVector128Single(value : Vector128`1) was skipped since it collides with above method

    # Skipped Insert due to it being static, abstract and generic.

    Insert : Insert_MethodGroup
    class Insert_MethodGroup:
        def __call__(self, value: Vector128_1[int], data: int, index: int) -> Vector128_1[int]:...
        # Method Insert(value : Vector128`1, data : UInt16, index : Byte) was skipped since it collides with above method

    # Skipped LoadAlignedVector128 due to it being static, abstract and generic.

    LoadAlignedVector128 : LoadAlignedVector128_MethodGroup
    class LoadAlignedVector128_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector128_1[float]:...
        # Method LoadAlignedVector128(address : SByte*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : Byte*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : Int16*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : UInt16*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : Int32*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : UInt32*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : Int64*) was skipped since it collides with above method
        # Method LoadAlignedVector128(address : UInt64*) was skipped since it collides with above method

    # Skipped LoadScalarVector128 due to it being static, abstract and generic.

    LoadScalarVector128 : LoadScalarVector128_MethodGroup
    class LoadScalarVector128_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector128_1[float]:...
        # Method LoadScalarVector128(address : Int32*) was skipped since it collides with above method
        # Method LoadScalarVector128(address : UInt32*) was skipped since it collides with above method
        # Method LoadScalarVector128(address : Int64*) was skipped since it collides with above method
        # Method LoadScalarVector128(address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVector128 due to it being static, abstract and generic.

    LoadVector128 : LoadVector128_MethodGroup
    class LoadVector128_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector128_1[float]:...
        # Method LoadVector128(address : SByte*) was skipped since it collides with above method
        # Method LoadVector128(address : Byte*) was skipped since it collides with above method
        # Method LoadVector128(address : Int16*) was skipped since it collides with above method
        # Method LoadVector128(address : UInt16*) was skipped since it collides with above method
        # Method LoadVector128(address : Int32*) was skipped since it collides with above method
        # Method LoadVector128(address : UInt32*) was skipped since it collides with above method
        # Method LoadVector128(address : Int64*) was skipped since it collides with above method
        # Method LoadVector128(address : UInt64*) was skipped since it collides with above method

    # Skipped MaskMove due to it being static, abstract and generic.

    MaskMove : MaskMove_MethodGroup
    class MaskMove_MethodGroup:
        def __call__(self, source: Vector128_1[int], mask: Vector128_1[int], address: clr.Reference[int]) -> None:...
        # Method MaskMove(source : Vector128`1, mask : Vector128`1, address : Byte*) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MoveMask due to it being static, abstract and generic.

    MoveMask : MoveMask_MethodGroup
    class MoveMask_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> int:...
        # Method MoveMask(value : Vector128`1) was skipped since it collides with above method
        # Method MoveMask(value : Vector128`1) was skipped since it collides with above method

    # Skipped MoveScalar due to it being static, abstract and generic.

    MoveScalar : MoveScalar_MethodGroup
    class MoveScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MoveScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyHigh due to it being static, abstract and generic.

    MultiplyHigh : MultiplyHigh_MethodGroup
    class MultiplyHigh_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyLow due to it being static, abstract and generic.

    MultiplyLow : MultiplyLow_MethodGroup
    class MultiplyLow_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Or due to it being static, abstract and generic.

    Or : Or_MethodGroup
    class Or_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped PackSignedSaturate due to it being static, abstract and generic.

    PackSignedSaturate : PackSignedSaturate_MethodGroup
    class PackSignedSaturate_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method PackSignedSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLeftLogical due to it being static, abstract and generic.

    ShiftLeftLogical : ShiftLeftLogical_MethodGroup
    class ShiftLeftLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftLeftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLeftLogical128BitLane due to it being static, abstract and generic.

    ShiftLeftLogical128BitLane : ShiftLeftLogical128BitLane_MethodGroup
    class ShiftLeftLogical128BitLane_MethodGroup:
        def __call__(self, value: Vector128_1[int], numBytes: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmetic(value : Vector128`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftRightArithmetic(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftRightLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftRightLogical128BitLane due to it being static, abstract and generic.

    ShiftRightLogical128BitLane : ShiftRightLogical128BitLane_MethodGroup
    class ShiftRightLogical128BitLane_MethodGroup:
        def __call__(self, value: Vector128_1[int], numBytes: int) -> Vector128_1[int]:...
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical128BitLane(value : Vector128`1, numBytes : Byte) was skipped since it collides with above method

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int], control: int) -> Vector128_1[int]:...
        # Method Shuffle(value : Vector128`1, control : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], control: int) -> Vector128_1[float]:...

    # Skipped ShuffleHigh due to it being static, abstract and generic.

    ShuffleHigh : ShuffleHigh_MethodGroup
    class ShuffleHigh_MethodGroup:
        def __call__(self, value: Vector128_1[int], control: int) -> Vector128_1[int]:...
        # Method ShuffleHigh(value : Vector128`1, control : Byte) was skipped since it collides with above method

    # Skipped ShuffleLow due to it being static, abstract and generic.

    ShuffleLow : ShuffleLow_MethodGroup
    class ShuffleLow_MethodGroup:
        def __call__(self, value: Vector128_1[int], control: int) -> Vector128_1[int]:...
        # Method ShuffleLow(value : Vector128`1, control : Byte) was skipped since it collides with above method

    # Skipped SqrtScalar due to it being static, abstract and generic.

    SqrtScalar : SqrtScalar_MethodGroup
    class SqrtScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector128_1[float]) -> None:...
        # Method Store(address : SByte*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Byte*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Int16*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : UInt16*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Int32*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : UInt32*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Int64*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : UInt64*, source : Vector128`1) was skipped since it collides with above method

    # Skipped StoreAligned due to it being static, abstract and generic.

    StoreAligned : StoreAligned_MethodGroup
    class StoreAligned_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector128_1[float]) -> None:...
        # Method StoreAligned(address : SByte*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : Byte*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : Int16*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : UInt16*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : Int32*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : UInt32*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : Int64*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAligned(address : UInt64*, source : Vector128`1) was skipped since it collides with above method

    # Skipped StoreAlignedNonTemporal due to it being static, abstract and generic.

    StoreAlignedNonTemporal : StoreAlignedNonTemporal_MethodGroup
    class StoreAlignedNonTemporal_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector128_1[float]) -> None:...
        # Method StoreAlignedNonTemporal(address : SByte*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Byte*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Int16*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : UInt16*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Int32*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : UInt32*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : Int64*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreAlignedNonTemporal(address : UInt64*, source : Vector128`1) was skipped since it collides with above method

    # Skipped StoreNonTemporal due to it being static, abstract and generic.

    StoreNonTemporal : StoreNonTemporal_MethodGroup
    class StoreNonTemporal_MethodGroup:
        def __call__(self, address: clr.Reference[int], value: int) -> None:...
        # Method StoreNonTemporal(address : UInt32*, value : UInt32) was skipped since it collides with above method

    # Skipped StoreScalar due to it being static, abstract and generic.

    StoreScalar : StoreScalar_MethodGroup
    class StoreScalar_MethodGroup:
        def __call__(self, address: clr.Reference[float], source: Vector128_1[float]) -> None:...
        # Method StoreScalar(address : Int32*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreScalar(address : Int64*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreScalar(address : UInt32*, source : Vector128`1) was skipped since it collides with above method
        # Method StoreScalar(address : UInt64*, source : Vector128`1) was skipped since it collides with above method

    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped UnpackHigh due to it being static, abstract and generic.

    UnpackHigh : UnpackHigh_MethodGroup
    class UnpackHigh_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped UnpackLow due to it being static, abstract and generic.

    UnpackLow : UnpackLow_MethodGroup
    class UnpackLow_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method UnpackLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method


    class X64(Sse.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def ConvertScalarToVector128Double(upper: Vector128_1[float], value: int) -> Vector128_1[float]: ...
        @staticmethod
        def ConvertScalarToVector128Int64(value: int) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertScalarToVector128UInt64(value: int) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToInt64WithTruncation(value: Vector128_1[float]) -> int: ...
        @staticmethod
        def ConvertToUInt64(value: Vector128_1[int]) -> int: ...
        # Skipped ConvertToInt64 due to it being static, abstract and generic.

        ConvertToInt64 : ConvertToInt64_MethodGroup
        class ConvertToInt64_MethodGroup:
            def __call__(self, value: Vector128_1[float]) -> int:...
            # Method ConvertToInt64(value : Vector128`1) was skipped since it collides with above method

        # Skipped StoreNonTemporal due to it being static, abstract and generic.

        StoreNonTemporal : StoreNonTemporal_MethodGroup
        class StoreNonTemporal_MethodGroup:
            def __call__(self, address: clr.Reference[int], value: int) -> None:...
            # Method StoreNonTemporal(address : UInt64*, value : UInt64) was skipped since it collides with above method




class Sse3(Sse2):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def LoadAndDuplicateToVector128(address: clr.Reference[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MoveAndDuplicate(source: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MoveHighAndDuplicate(source: Vector128_1[float]) -> Vector128_1[float]: ...
    @staticmethod
    def MoveLowAndDuplicate(source: Vector128_1[float]) -> Vector128_1[float]: ...
    # Skipped AddSubtract due to it being static, abstract and generic.

    AddSubtract : AddSubtract_MethodGroup
    class AddSubtract_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method AddSubtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped HorizontalAdd due to it being static, abstract and generic.

    HorizontalAdd : HorizontalAdd_MethodGroup
    class HorizontalAdd_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method HorizontalAdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped HorizontalSubtract due to it being static, abstract and generic.

    HorizontalSubtract : HorizontalSubtract_MethodGroup
    class HorizontalSubtract_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method HorizontalSubtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped LoadDquVector128 due to it being static, abstract and generic.

    LoadDquVector128 : LoadDquVector128_MethodGroup
    class LoadDquVector128_MethodGroup:
        def __call__(self, address: clr.Reference[int]) -> Vector128_1[int]:...
        # Method LoadDquVector128(address : Byte*) was skipped since it collides with above method
        # Method LoadDquVector128(address : Int16*) was skipped since it collides with above method
        # Method LoadDquVector128(address : UInt16*) was skipped since it collides with above method
        # Method LoadDquVector128(address : Int32*) was skipped since it collides with above method
        # Method LoadDquVector128(address : UInt32*) was skipped since it collides with above method
        # Method LoadDquVector128(address : Int64*) was skipped since it collides with above method
        # Method LoadDquVector128(address : UInt64*) was skipped since it collides with above method


    class X64(Sse2.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Sse41(Ssse3):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def MinHorizontal(value: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def MultipleSumAbsoluteDifferences(left: Vector128_1[int], right: Vector128_1[int], mask: int) -> Vector128_1[int]: ...
    @staticmethod
    def Multiply(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def PackUnsignedSaturate(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    # Skipped Blend due to it being static, abstract and generic.

    Blend : Blend_MethodGroup
    class Blend_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], control: int) -> Vector128_1[float]:...
        # Method Blend(left : Vector128`1, right : Vector128`1, control : Byte) was skipped since it collides with above method
        # Method Blend(left : Vector128`1, right : Vector128`1, control : Byte) was skipped since it collides with above method
        # Method Blend(left : Vector128`1, right : Vector128`1, control : Byte) was skipped since it collides with above method

    # Skipped BlendVariable due to it being static, abstract and generic.

    BlendVariable : BlendVariable_MethodGroup
    class BlendVariable_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], mask: Vector128_1[float]) -> Vector128_1[float]:...
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BlendVariable(left : Vector128`1, right : Vector128`1, mask : Vector128`1) was skipped since it collides with above method

    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Ceiling(value : Vector128`1) was skipped since it collides with above method

    # Skipped CeilingScalar due to it being static, abstract and generic.

    CeilingScalar : CeilingScalar_MethodGroup
    class CeilingScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CeilingScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CeilingScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped CompareEqual due to it being static, abstract and generic.

    CompareEqual : CompareEqual_MethodGroup
    class CompareEqual_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToVector128Int16 due to it being static, abstract and generic.

    ConvertToVector128Int16 : ConvertToVector128Int16_MethodGroup
    class ConvertToVector128Int16_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int16(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int16(address : Byte*) was skipped since it collides with above method

    # Skipped ConvertToVector128Int32 due to it being static, abstract and generic.

    ConvertToVector128Int32 : ConvertToVector128Int32_MethodGroup
    class ConvertToVector128Int32_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int32(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector128Int32(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector128Int32(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int32(address : Byte*) was skipped since it collides with above method
        # Method ConvertToVector128Int32(address : Int16*) was skipped since it collides with above method
        # Method ConvertToVector128Int32(address : UInt16*) was skipped since it collides with above method

    # Skipped ConvertToVector128Int64 due to it being static, abstract and generic.

    ConvertToVector128Int64 : ConvertToVector128Int64_MethodGroup
    class ConvertToVector128Int64_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector128Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector128Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector128Int64(value : Vector128`1) was skipped since it collides with above method
        # Method ConvertToVector128Int64(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[int]) -> Vector128_1[int]:...
        # Method ConvertToVector128Int64(address : Byte*) was skipped since it collides with above method
        # Method ConvertToVector128Int64(address : Int16*) was skipped since it collides with above method
        # Method ConvertToVector128Int64(address : UInt16*) was skipped since it collides with above method
        # Method ConvertToVector128Int64(address : Int32*) was skipped since it collides with above method
        # Method ConvertToVector128Int64(address : UInt32*) was skipped since it collides with above method

    # Skipped DotProduct due to it being static, abstract and generic.

    DotProduct : DotProduct_MethodGroup
    class DotProduct_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], control: int) -> Vector128_1[float]:...
        # Method DotProduct(left : Vector128`1, right : Vector128`1, control : Byte) was skipped since it collides with above method

    # Skipped Extract due to it being static, abstract and generic.

    Extract : Extract_MethodGroup
    class Extract_MethodGroup:
        def __call__(self, value: Vector128_1[float], index: int) -> float:...
        # Method Extract(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(value : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Floor(value : Vector128`1) was skipped since it collides with above method

    # Skipped FloorScalar due to it being static, abstract and generic.

    FloorScalar : FloorScalar_MethodGroup
    class FloorScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method FloorScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method FloorScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped Insert due to it being static, abstract and generic.

    Insert : Insert_MethodGroup
    class Insert_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float], data: Vector128_1[float], index: int) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[int], data: int, index: int) -> Vector128_1[int]:...
        # Method Insert(value : Vector128`1, data : Byte, index : Byte) was skipped since it collides with above method
        # Method Insert(value : Vector128`1, data : Int32, index : Byte) was skipped since it collides with above method
        # Method Insert(value : Vector128`1, data : UInt32, index : Byte) was skipped since it collides with above method

    # Skipped LoadAlignedVector128NonTemporal due to it being static, abstract and generic.

    LoadAlignedVector128NonTemporal : LoadAlignedVector128NonTemporal_MethodGroup
    class LoadAlignedVector128NonTemporal_MethodGroup:
        def __call__(self, address: clr.Reference[int]) -> Vector128_1[int]:...
        # Method LoadAlignedVector128NonTemporal(address : Byte*) was skipped since it collides with above method
        # Method LoadAlignedVector128NonTemporal(address : Int16*) was skipped since it collides with above method
        # Method LoadAlignedVector128NonTemporal(address : UInt16*) was skipped since it collides with above method
        # Method LoadAlignedVector128NonTemporal(address : Int32*) was skipped since it collides with above method
        # Method LoadAlignedVector128NonTemporal(address : UInt32*) was skipped since it collides with above method
        # Method LoadAlignedVector128NonTemporal(address : Int64*) was skipped since it collides with above method
        # Method LoadAlignedVector128NonTemporal(address : UInt64*) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyLow due to it being static, abstract and generic.

    MultiplyLow : MultiplyLow_MethodGroup
    class MultiplyLow_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped RoundCurrentDirection due to it being static, abstract and generic.

    RoundCurrentDirection : RoundCurrentDirection_MethodGroup
    class RoundCurrentDirection_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundCurrentDirection(value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundCurrentDirectionScalar due to it being static, abstract and generic.

    RoundCurrentDirectionScalar : RoundCurrentDirectionScalar_MethodGroup
    class RoundCurrentDirectionScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundCurrentDirectionScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundCurrentDirectionScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToNearestInteger due to it being static, abstract and generic.

    RoundToNearestInteger : RoundToNearestInteger_MethodGroup
    class RoundToNearestInteger_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToNearestInteger(value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToNearestIntegerScalar due to it being static, abstract and generic.

    RoundToNearestIntegerScalar : RoundToNearestIntegerScalar_MethodGroup
    class RoundToNearestIntegerScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToNearestIntegerScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToNearestIntegerScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToNegativeInfinity due to it being static, abstract and generic.

    RoundToNegativeInfinity : RoundToNegativeInfinity_MethodGroup
    class RoundToNegativeInfinity_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToNegativeInfinity(value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToNegativeInfinityScalar due to it being static, abstract and generic.

    RoundToNegativeInfinityScalar : RoundToNegativeInfinityScalar_MethodGroup
    class RoundToNegativeInfinityScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToNegativeInfinityScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToNegativeInfinityScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToPositiveInfinity due to it being static, abstract and generic.

    RoundToPositiveInfinity : RoundToPositiveInfinity_MethodGroup
    class RoundToPositiveInfinity_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToPositiveInfinity(value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToPositiveInfinityScalar due to it being static, abstract and generic.

    RoundToPositiveInfinityScalar : RoundToPositiveInfinityScalar_MethodGroup
    class RoundToPositiveInfinityScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToPositiveInfinityScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToPositiveInfinityScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToZero due to it being static, abstract and generic.

    RoundToZero : RoundToZero_MethodGroup
    class RoundToZero_MethodGroup:
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToZero(value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundToZeroScalar due to it being static, abstract and generic.

    RoundToZeroScalar : RoundToZeroScalar_MethodGroup
    class RoundToZeroScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToZeroScalar(value : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, upper: Vector128_1[float], value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RoundToZeroScalar(upper : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped TestC due to it being static, abstract and generic.

    TestC : TestC_MethodGroup
    class TestC_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> bool:...
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped TestNotZAndNotC due to it being static, abstract and generic.

    TestNotZAndNotC : TestNotZAndNotC_MethodGroup
    class TestNotZAndNotC_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> bool:...
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestNotZAndNotC(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped TestZ due to it being static, abstract and generic.

    TestZ : TestZ_MethodGroup
    class TestZ_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> bool:...
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method TestZ(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method


    class X64(Ssse3.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        # Skipped Extract due to it being static, abstract and generic.

        Extract : Extract_MethodGroup
        class Extract_MethodGroup:
            def __call__(self, value: Vector128_1[int], index: int) -> int:...
            # Method Extract(value : Vector128`1, index : Byte) was skipped since it collides with above method

        # Skipped Insert due to it being static, abstract and generic.

        Insert : Insert_MethodGroup
        class Insert_MethodGroup:
            def __call__(self, value: Vector128_1[int], data: int, index: int) -> Vector128_1[int]:...
            # Method Insert(value : Vector128`1, data : UInt64, index : Byte) was skipped since it collides with above method




class Sse42(Sse41):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def CompareGreaterThan(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    # Skipped Crc32 due to it being static, abstract and generic.

    Crc32 : Crc32_MethodGroup
    class Crc32_MethodGroup:
        def __call__(self, crc: int, data: int) -> int:...
        # Method Crc32(crc : UInt32, data : UInt16) was skipped since it collides with above method
        # Method Crc32(crc : UInt32, data : UInt32) was skipped since it collides with above method


    class X64(Sse41.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def Crc32(crc: int, data: int) -> int: ...



class Ssse3(Sse3):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def HorizontalAddSaturate(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def HorizontalSubtractSaturate(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def MultiplyAddAdjacent(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def MultiplyHighRoundScale(left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method Abs(value : Vector128`1) was skipped since it collides with above method
        # Method Abs(value : Vector128`1) was skipped since it collides with above method

    # Skipped AlignRight due to it being static, abstract and generic.

    AlignRight : AlignRight_MethodGroup
    class AlignRight_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], mask: int) -> Vector128_1[int]:...
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method
        # Method AlignRight(left : Vector128`1, right : Vector128`1, mask : Byte) was skipped since it collides with above method

    # Skipped HorizontalAdd due to it being static, abstract and generic.

    HorizontalAdd : HorizontalAdd_MethodGroup
    class HorizontalAdd_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method HorizontalAdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped HorizontalSubtract due to it being static, abstract and generic.

    HorizontalSubtract : HorizontalSubtract_MethodGroup
    class HorizontalSubtract_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method HorizontalSubtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __call__(self, value: Vector128_1[int], mask: Vector128_1[int]) -> Vector128_1[int]:...
        # Method Shuffle(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method

    # Skipped Sign due to it being static, abstract and generic.

    Sign : Sign_MethodGroup
    class Sign_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method Sign(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Sign(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method


    class X64(Sse3.X64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class X86Base(abc.ABC):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def CpuId(functionId: int, subFunctionId: int) -> ValueTuple_4[int, int, int, int]: ...

    class X64(abc.ABC):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...


