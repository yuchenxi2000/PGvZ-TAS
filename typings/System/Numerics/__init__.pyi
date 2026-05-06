import typing, clr, abc
from System import ISpanFormattable, IEquatable_1, IComparable_1, IComparable, Decimal, Array_1, ReadOnlySpan_1, Span_1, IFormatProvider, UIntPtr, IFormattable
from System.Globalization import NumberStyles

class BigInteger(ISpanFormattable, IEquatable_1[BigInteger], IComparable_1[BigInteger], IComparable_0):
    # Constructor .ctor(value : UInt32) was skipped since it collides with above method
    # Constructor .ctor(value : Int64) was skipped since it collides with above method
    # Constructor .ctor(value : UInt64) was skipped since it collides with above method
    # Constructor .ctor(value : Single) was skipped since it collides with above method
    # Constructor .ctor(value : Double) was skipped since it collides with above method
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, value: Decimal) -> None: ...
    @typing.overload
    def __init__(self, value: Array_1[int]) -> None: ...
    @typing.overload
    def __init__(self, value: ReadOnlySpan_1[int], isUnsigned: bool = ..., isBigEndian: bool = ...) -> None: ...
    @property
    def IsEven(self) -> bool: ...
    @property
    def IsOne(self) -> bool: ...
    @property
    def IsPowerOfTwo(self) -> bool: ...
    @property
    def IsZero(self) -> bool: ...
    @classmethod
    @property
    def MinusOne(cls) -> BigInteger: ...
    @classmethod
    @property
    def One(cls) -> BigInteger: ...
    @property
    def Sign(self) -> int: ...
    @classmethod
    @property
    def Zero(cls) -> BigInteger: ...
    @staticmethod
    def Abs(value: BigInteger) -> BigInteger: ...
    @staticmethod
    def Add(left: BigInteger, right: BigInteger) -> BigInteger: ...
    @staticmethod
    def Compare(left: BigInteger, right: BigInteger) -> int: ...
    @staticmethod
    def Divide(dividend: BigInteger, divisor: BigInteger) -> BigInteger: ...
    @staticmethod
    def DivRem(dividend: BigInteger, divisor: BigInteger, remainder: clr.Reference[BigInteger]) -> BigInteger: ...
    def GetBitLength(self) -> int: ...
    def GetByteCount(self, isUnsigned: bool = ...) -> int: ...
    def GetHashCode(self) -> int: ...
    @staticmethod
    def GreatestCommonDivisor(left: BigInteger, right: BigInteger) -> BigInteger: ...
    @staticmethod
    def Log10(value: BigInteger) -> float: ...
    @staticmethod
    def Max(left: BigInteger, right: BigInteger) -> BigInteger: ...
    @staticmethod
    def Min(left: BigInteger, right: BigInteger) -> BigInteger: ...
    @staticmethod
    def ModPow(value: BigInteger, exponent: BigInteger, modulus: BigInteger) -> BigInteger: ...
    @staticmethod
    def Multiply(left: BigInteger, right: BigInteger) -> BigInteger: ...
    @staticmethod
    def Negate(value: BigInteger) -> BigInteger: ...
    def __add__(self, left: BigInteger, right: BigInteger) -> BigInteger: ...
    def __and__(self, left: BigInteger, right: BigInteger) -> BigInteger: ...
    def __or__(self, left: BigInteger, right: BigInteger) -> BigInteger: ...
    # Operator not supported op_Decrement(value: BigInteger)
    def __truediv__(self, dividend: BigInteger, divisor: BigInteger) -> BigInteger: ...
    @typing.overload
    def __eq__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __eq__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __eq__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __eq__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __eq__(self, left: BigInteger, right: BigInteger) -> bool: ...
    def __xor__(self, left: BigInteger, right: BigInteger) -> BigInteger: ...
    # Operator not supported op_Explicit(value: Double)
    # Operator not supported op_Explicit(value: Single)
    # Operator not supported op_Explicit(value: Decimal)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    # Operator not supported op_Explicit(value: BigInteger)
    @typing.overload
    def __gt__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __gt__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __gt__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __gt__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __gt__(self, left: BigInteger, right: BigInteger) -> bool: ...
    @typing.overload
    def __ge__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __ge__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __ge__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __ge__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __ge__(self, left: BigInteger, right: BigInteger) -> bool: ...
    # Operator not supported op_Implicit(value: Byte)
    # Operator not supported op_Implicit(value: SByte)
    # Operator not supported op_Implicit(value: Int16)
    # Operator not supported op_Implicit(value: UInt16)
    # Operator not supported op_Implicit(value: Int32)
    # Operator not supported op_Implicit(value: UInt32)
    # Operator not supported op_Implicit(value: Int64)
    # Operator not supported op_Implicit(value: UInt64)
    # Operator not supported op_Increment(value: BigInteger)
    @typing.overload
    def __ne__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __ne__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __ne__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __ne__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __ne__(self, left: BigInteger, right: BigInteger) -> bool: ...
    def __lshift__(self, value: BigInteger, shift: int) -> BigInteger: ...
    @typing.overload
    def __lt__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __lt__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __lt__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __lt__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __lt__(self, left: BigInteger, right: BigInteger) -> bool: ...
    @typing.overload
    def __le__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __le__(self, left: int, right: BigInteger) -> bool: ...
    @typing.overload
    def __le__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __le__(self, left: BigInteger, right: int) -> bool: ...
    @typing.overload
    def __le__(self, left: BigInteger, right: BigInteger) -> bool: ...
    def __mod__(self, dividend: BigInteger, divisor: BigInteger) -> BigInteger: ...
    def __mul__(self, left: BigInteger, right: BigInteger) -> BigInteger: ...
    def __invert__(self, value: BigInteger) -> BigInteger: ...
    def __rshift__(self, value: BigInteger, shift: int) -> BigInteger: ...
    def __sub__(self, left: BigInteger, right: BigInteger) -> BigInteger: ...
    def __neg__(self, value: BigInteger) -> BigInteger: ...
    def __pos__(self, value: BigInteger) -> BigInteger: ...
    @staticmethod
    def Pow(value: BigInteger, exponent: int) -> BigInteger: ...
    @staticmethod
    def Remainder(dividend: BigInteger, divisor: BigInteger) -> BigInteger: ...
    @staticmethod
    def Subtract(left: BigInteger, right: BigInteger) -> BigInteger: ...
    def TryFormat(self, destination: Span_1[str], charsWritten: clr.Reference[int], format: ReadOnlySpan_1[str] = ..., provider: IFormatProvider = ...) -> bool: ...
    def TryWriteBytes(self, destination: Span_1[int], bytesWritten: clr.Reference[int], isUnsigned: bool = ..., isBigEndian: bool = ...) -> bool: ...
    # Skipped CompareTo due to it being static, abstract and generic.

    CompareTo : CompareTo_MethodGroup
    class CompareTo_MethodGroup:
        @typing.overload
        def __call__(self, other: int) -> int:...
        # Method CompareTo(other : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, other: BigInteger) -> int:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> int:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: int) -> bool:...
        # Method Equals(other : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, other: BigInteger) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Log due to it being static, abstract and generic.

    Log : Log_MethodGroup
    class Log_MethodGroup:
        @typing.overload
        def __call__(self, value: BigInteger) -> float:...
        @typing.overload
        def __call__(self, value: BigInteger, baseValue: float) -> float:...

    # Skipped Parse due to it being static, abstract and generic.

    Parse : Parse_MethodGroup
    class Parse_MethodGroup:
        @typing.overload
        def __call__(self, value: str) -> BigInteger:...
        @typing.overload
        def __call__(self, value: str, style: NumberStyles) -> BigInteger:...
        @typing.overload
        def __call__(self, value: str, provider: IFormatProvider) -> BigInteger:...
        @typing.overload
        def __call__(self, value: ReadOnlySpan_1[str], style: NumberStyles = ..., provider: IFormatProvider = ...) -> BigInteger:...
        @typing.overload
        def __call__(self, value: str, style: NumberStyles, provider: IFormatProvider) -> BigInteger:...

    # Skipped ToByteArray due to it being static, abstract and generic.

    ToByteArray : ToByteArray_MethodGroup
    class ToByteArray_MethodGroup:
        @typing.overload
        def __call__(self) -> Array_1[int]:...
        @typing.overload
        def __call__(self, isUnsigned: bool = ..., isBigEndian: bool = ...) -> Array_1[int]:...

    # Skipped ToString due to it being static, abstract and generic.

    ToString : ToString_MethodGroup
    class ToString_MethodGroup:
        @typing.overload
        def __call__(self) -> str:...
        @typing.overload
        def __call__(self, format: str) -> str:...
        @typing.overload
        def __call__(self, provider: IFormatProvider) -> str:...
        @typing.overload
        def __call__(self, format: str, provider: IFormatProvider) -> str:...

    # Skipped TryParse due to it being static, abstract and generic.

    TryParse : TryParse_MethodGroup
    class TryParse_MethodGroup:
        @typing.overload
        def __call__(self, value: ReadOnlySpan_1[str], result: clr.Reference[BigInteger]) -> bool:...
        @typing.overload
        def __call__(self, value: str, result: clr.Reference[BigInteger]) -> bool:...
        @typing.overload
        def __call__(self, value: ReadOnlySpan_1[str], style: NumberStyles, provider: IFormatProvider, result: clr.Reference[BigInteger]) -> bool:...
        @typing.overload
        def __call__(self, value: str, style: NumberStyles, provider: IFormatProvider, result: clr.Reference[BigInteger]) -> bool:...



class BitOperations(abc.ABC):
    # Skipped IsPow2 due to it being static, abstract and generic.

    IsPow2 : IsPow2_MethodGroup
    class IsPow2_MethodGroup:
        def __call__(self, value: int) -> bool:...
        # Method IsPow2(value : UInt32) was skipped since it collides with above method
        # Method IsPow2(value : Int64) was skipped since it collides with above method
        # Method IsPow2(value : UInt64) was skipped since it collides with above method

    # Skipped LeadingZeroCount due to it being static, abstract and generic.

    LeadingZeroCount : LeadingZeroCount_MethodGroup
    class LeadingZeroCount_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method LeadingZeroCount(value : UInt64) was skipped since it collides with above method

    # Skipped Log2 due to it being static, abstract and generic.

    Log2 : Log2_MethodGroup
    class Log2_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method Log2(value : UInt64) was skipped since it collides with above method

    # Skipped PopCount due to it being static, abstract and generic.

    PopCount : PopCount_MethodGroup
    class PopCount_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method PopCount(value : UInt64) was skipped since it collides with above method

    # Skipped RotateLeft due to it being static, abstract and generic.

    RotateLeft : RotateLeft_MethodGroup
    class RotateLeft_MethodGroup:
        def __call__(self, value: int, offset: int) -> int:...
        # Method RotateLeft(value : UInt64, offset : Int32) was skipped since it collides with above method

    # Skipped RotateRight due to it being static, abstract and generic.

    RotateRight : RotateRight_MethodGroup
    class RotateRight_MethodGroup:
        def __call__(self, value: int, offset: int) -> int:...
        # Method RotateRight(value : UInt64, offset : Int32) was skipped since it collides with above method

    # Skipped RoundUpToPowerOf2 due to it being static, abstract and generic.

    RoundUpToPowerOf2 : RoundUpToPowerOf2_MethodGroup
    class RoundUpToPowerOf2_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method RoundUpToPowerOf2(value : UInt64) was skipped since it collides with above method

    # Skipped TrailingZeroCount due to it being static, abstract and generic.

    TrailingZeroCount : TrailingZeroCount_MethodGroup
    class TrailingZeroCount_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method TrailingZeroCount(value : UInt32) was skipped since it collides with above method
        # Method TrailingZeroCount(value : Int64) was skipped since it collides with above method
        # Method TrailingZeroCount(value : UInt64) was skipped since it collides with above method



class Matrix3x2(IEquatable_1[Matrix3x2]):
    def __init__(self, m11: float, m12: float, m21: float, m22: float, m31: float, m32: float) -> None: ...
    M11 : float
    M12 : float
    M21 : float
    M22 : float
    M31 : float
    M32 : float
    @classmethod
    @property
    def Identity(cls) -> Matrix3x2: ...
    @property
    def IsIdentity(self) -> bool: ...
    @property
    def Translation(self) -> Vector2: ...
    @Translation.setter
    def Translation(self, value: Vector2) -> Vector2: ...
    @staticmethod
    def Add(value1: Matrix3x2, value2: Matrix3x2) -> Matrix3x2: ...
    def GetDeterminant(self) -> float: ...
    def GetHashCode(self) -> int: ...
    @staticmethod
    def Invert(matrix: Matrix3x2, result: clr.Reference[Matrix3x2]) -> bool: ...
    @staticmethod
    def Lerp(matrix1: Matrix3x2, matrix2: Matrix3x2, amount: float) -> Matrix3x2: ...
    @staticmethod
    def Negate(value: Matrix3x2) -> Matrix3x2: ...
    def __add__(self, value1: Matrix3x2, value2: Matrix3x2) -> Matrix3x2: ...
    def __eq__(self, value1: Matrix3x2, value2: Matrix3x2) -> bool: ...
    def __ne__(self, value1: Matrix3x2, value2: Matrix3x2) -> bool: ...
    @typing.overload
    def __mul__(self, value1: Matrix3x2, value2: float) -> Matrix3x2: ...
    @typing.overload
    def __mul__(self, value1: Matrix3x2, value2: Matrix3x2) -> Matrix3x2: ...
    def __sub__(self, value1: Matrix3x2, value2: Matrix3x2) -> Matrix3x2: ...
    def __neg__(self, value: Matrix3x2) -> Matrix3x2: ...
    @staticmethod
    def Subtract(value1: Matrix3x2, value2: Matrix3x2) -> Matrix3x2: ...
    def ToString(self) -> str: ...
    # Skipped CreateRotation due to it being static, abstract and generic.

    CreateRotation : CreateRotation_MethodGroup
    class CreateRotation_MethodGroup:
        @typing.overload
        def __call__(self, radians: float) -> Matrix3x2:...
        @typing.overload
        def __call__(self, radians: float, centerPoint: Vector2) -> Matrix3x2:...

    # Skipped CreateScale due to it being static, abstract and generic.

    CreateScale : CreateScale_MethodGroup
    class CreateScale_MethodGroup:
        @typing.overload
        def __call__(self, scale: float) -> Matrix3x2:...
        @typing.overload
        def __call__(self, scales: Vector2) -> Matrix3x2:...
        @typing.overload
        def __call__(self, xScale: float, yScale: float) -> Matrix3x2:...
        @typing.overload
        def __call__(self, scale: float, centerPoint: Vector2) -> Matrix3x2:...
        @typing.overload
        def __call__(self, scales: Vector2, centerPoint: Vector2) -> Matrix3x2:...
        @typing.overload
        def __call__(self, xScale: float, yScale: float, centerPoint: Vector2) -> Matrix3x2:...

    # Skipped CreateSkew due to it being static, abstract and generic.

    CreateSkew : CreateSkew_MethodGroup
    class CreateSkew_MethodGroup:
        @typing.overload
        def __call__(self, radiansX: float, radiansY: float) -> Matrix3x2:...
        @typing.overload
        def __call__(self, radiansX: float, radiansY: float, centerPoint: Vector2) -> Matrix3x2:...

    # Skipped CreateTranslation due to it being static, abstract and generic.

    CreateTranslation : CreateTranslation_MethodGroup
    class CreateTranslation_MethodGroup:
        @typing.overload
        def __call__(self, position: Vector2) -> Matrix3x2:...
        @typing.overload
        def __call__(self, xPosition: float, yPosition: float) -> Matrix3x2:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Matrix3x2) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, value1: Matrix3x2, value2: float) -> Matrix3x2:...
        @typing.overload
        def __call__(self, value1: Matrix3x2, value2: Matrix3x2) -> Matrix3x2:...



class Matrix4x4(IEquatable_1[Matrix4x4]):
    @typing.overload
    def __init__(self, m11: float, m12: float, m13: float, m14: float, m21: float, m22: float, m23: float, m24: float, m31: float, m32: float, m33: float, m34: float, m41: float, m42: float, m43: float, m44: float) -> None: ...
    @typing.overload
    def __init__(self, value: Matrix3x2) -> None: ...
    M11 : float
    M12 : float
    M13 : float
    M14 : float
    M21 : float
    M22 : float
    M23 : float
    M24 : float
    M31 : float
    M32 : float
    M33 : float
    M34 : float
    M41 : float
    M42 : float
    M43 : float
    M44 : float
    @classmethod
    @property
    def Identity(cls) -> Matrix4x4: ...
    @property
    def IsIdentity(self) -> bool: ...
    @property
    def Translation(self) -> Vector3: ...
    @Translation.setter
    def Translation(self, value: Vector3) -> Vector3: ...
    @staticmethod
    def Add(value1: Matrix4x4, value2: Matrix4x4) -> Matrix4x4: ...
    @staticmethod
    def CreateBillboard(objectPosition: Vector3, cameraPosition: Vector3, cameraUpVector: Vector3, cameraForwardVector: Vector3) -> Matrix4x4: ...
    @staticmethod
    def CreateConstrainedBillboard(objectPosition: Vector3, cameraPosition: Vector3, rotateAxis: Vector3, cameraForwardVector: Vector3, objectForwardVector: Vector3) -> Matrix4x4: ...
    @staticmethod
    def CreateFromAxisAngle(axis: Vector3, angle: float) -> Matrix4x4: ...
    @staticmethod
    def CreateFromQuaternion(quaternion: Quaternion) -> Matrix4x4: ...
    @staticmethod
    def CreateFromYawPitchRoll(yaw: float, pitch: float, roll: float) -> Matrix4x4: ...
    @staticmethod
    def CreateLookAt(cameraPosition: Vector3, cameraTarget: Vector3, cameraUpVector: Vector3) -> Matrix4x4: ...
    @staticmethod
    def CreateOrthographic(width: float, height: float, zNearPlane: float, zFarPlane: float) -> Matrix4x4: ...
    @staticmethod
    def CreateOrthographicOffCenter(left: float, right: float, bottom: float, top: float, zNearPlane: float, zFarPlane: float) -> Matrix4x4: ...
    @staticmethod
    def CreatePerspective(width: float, height: float, nearPlaneDistance: float, farPlaneDistance: float) -> Matrix4x4: ...
    @staticmethod
    def CreatePerspectiveFieldOfView(fieldOfView: float, aspectRatio: float, nearPlaneDistance: float, farPlaneDistance: float) -> Matrix4x4: ...
    @staticmethod
    def CreatePerspectiveOffCenter(left: float, right: float, bottom: float, top: float, nearPlaneDistance: float, farPlaneDistance: float) -> Matrix4x4: ...
    @staticmethod
    def CreateReflection(value: Plane) -> Matrix4x4: ...
    @staticmethod
    def CreateShadow(lightDirection: Vector3, plane: Plane) -> Matrix4x4: ...
    @staticmethod
    def CreateWorld(position: Vector3, forward: Vector3, up: Vector3) -> Matrix4x4: ...
    @staticmethod
    def Decompose(matrix: Matrix4x4, scale: clr.Reference[Vector3], rotation: clr.Reference[Quaternion], translation: clr.Reference[Vector3]) -> bool: ...
    def GetDeterminant(self) -> float: ...
    def GetHashCode(self) -> int: ...
    @staticmethod
    def Invert(matrix: Matrix4x4, result: clr.Reference[Matrix4x4]) -> bool: ...
    @staticmethod
    def Lerp(matrix1: Matrix4x4, matrix2: Matrix4x4, amount: float) -> Matrix4x4: ...
    @staticmethod
    def Negate(value: Matrix4x4) -> Matrix4x4: ...
    def __add__(self, value1: Matrix4x4, value2: Matrix4x4) -> Matrix4x4: ...
    def __eq__(self, value1: Matrix4x4, value2: Matrix4x4) -> bool: ...
    def __ne__(self, value1: Matrix4x4, value2: Matrix4x4) -> bool: ...
    @typing.overload
    def __mul__(self, value1: Matrix4x4, value2: float) -> Matrix4x4: ...
    @typing.overload
    def __mul__(self, value1: Matrix4x4, value2: Matrix4x4) -> Matrix4x4: ...
    def __sub__(self, value1: Matrix4x4, value2: Matrix4x4) -> Matrix4x4: ...
    def __neg__(self, value: Matrix4x4) -> Matrix4x4: ...
    @staticmethod
    def Subtract(value1: Matrix4x4, value2: Matrix4x4) -> Matrix4x4: ...
    def ToString(self) -> str: ...
    @staticmethod
    def Transform(value: Matrix4x4, rotation: Quaternion) -> Matrix4x4: ...
    @staticmethod
    def Transpose(matrix: Matrix4x4) -> Matrix4x4: ...
    # Skipped CreateRotationX due to it being static, abstract and generic.

    CreateRotationX : CreateRotationX_MethodGroup
    class CreateRotationX_MethodGroup:
        @typing.overload
        def __call__(self, radians: float) -> Matrix4x4:...
        @typing.overload
        def __call__(self, radians: float, centerPoint: Vector3) -> Matrix4x4:...

    # Skipped CreateRotationY due to it being static, abstract and generic.

    CreateRotationY : CreateRotationY_MethodGroup
    class CreateRotationY_MethodGroup:
        @typing.overload
        def __call__(self, radians: float) -> Matrix4x4:...
        @typing.overload
        def __call__(self, radians: float, centerPoint: Vector3) -> Matrix4x4:...

    # Skipped CreateRotationZ due to it being static, abstract and generic.

    CreateRotationZ : CreateRotationZ_MethodGroup
    class CreateRotationZ_MethodGroup:
        @typing.overload
        def __call__(self, radians: float) -> Matrix4x4:...
        @typing.overload
        def __call__(self, radians: float, centerPoint: Vector3) -> Matrix4x4:...

    # Skipped CreateScale due to it being static, abstract and generic.

    CreateScale : CreateScale_MethodGroup
    class CreateScale_MethodGroup:
        @typing.overload
        def __call__(self, scale: float) -> Matrix4x4:...
        @typing.overload
        def __call__(self, scales: Vector3) -> Matrix4x4:...
        @typing.overload
        def __call__(self, scale: float, centerPoint: Vector3) -> Matrix4x4:...
        @typing.overload
        def __call__(self, scales: Vector3, centerPoint: Vector3) -> Matrix4x4:...
        @typing.overload
        def __call__(self, xScale: float, yScale: float, zScale: float) -> Matrix4x4:...
        @typing.overload
        def __call__(self, xScale: float, yScale: float, zScale: float, centerPoint: Vector3) -> Matrix4x4:...

    # Skipped CreateTranslation due to it being static, abstract and generic.

    CreateTranslation : CreateTranslation_MethodGroup
    class CreateTranslation_MethodGroup:
        @typing.overload
        def __call__(self, position: Vector3) -> Matrix4x4:...
        @typing.overload
        def __call__(self, xPosition: float, yPosition: float, zPosition: float) -> Matrix4x4:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Matrix4x4) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, value1: Matrix4x4, value2: float) -> Matrix4x4:...
        @typing.overload
        def __call__(self, value1: Matrix4x4, value2: Matrix4x4) -> Matrix4x4:...



class Plane(IEquatable_1[Plane]):
    @typing.overload
    def __init__(self, normal: Vector3, d: float) -> None: ...
    @typing.overload
    def __init__(self, value: Vector4) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float, z: float, d: float) -> None: ...
    D : float
    Normal : Vector3
    @staticmethod
    def CreateFromVertices(point1: Vector3, point2: Vector3, point3: Vector3) -> Plane: ...
    @staticmethod
    def Dot(plane: Plane, value: Vector4) -> float: ...
    @staticmethod
    def DotCoordinate(plane: Plane, value: Vector3) -> float: ...
    @staticmethod
    def DotNormal(plane: Plane, value: Vector3) -> float: ...
    def GetHashCode(self) -> int: ...
    @staticmethod
    def Normalize(value: Plane) -> Plane: ...
    def __eq__(self, value1: Plane, value2: Plane) -> bool: ...
    def __ne__(self, value1: Plane, value2: Plane) -> bool: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Plane) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Transform due to it being static, abstract and generic.

    Transform : Transform_MethodGroup
    class Transform_MethodGroup:
        @typing.overload
        def __call__(self, plane: Plane, matrix: Matrix4x4) -> Plane:...
        @typing.overload
        def __call__(self, plane: Plane, rotation: Quaternion) -> Plane:...



class Quaternion(IEquatable_1[Quaternion]):
    @typing.overload
    def __init__(self, vectorPart: Vector3, scalarPart: float) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None: ...
    W : float
    X : float
    Y : float
    Z : float
    @classmethod
    @property
    def Identity(cls) -> Quaternion: ...
    @property
    def IsIdentity(self) -> bool: ...
    @staticmethod
    def Add(value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    @staticmethod
    def Concatenate(value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    @staticmethod
    def Conjugate(value: Quaternion) -> Quaternion: ...
    @staticmethod
    def CreateFromAxisAngle(axis: Vector3, angle: float) -> Quaternion: ...
    @staticmethod
    def CreateFromRotationMatrix(matrix: Matrix4x4) -> Quaternion: ...
    @staticmethod
    def CreateFromYawPitchRoll(yaw: float, pitch: float, roll: float) -> Quaternion: ...
    @staticmethod
    def Divide(value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    @staticmethod
    def Dot(quaternion1: Quaternion, quaternion2: Quaternion) -> float: ...
    def GetHashCode(self) -> int: ...
    @staticmethod
    def Inverse(value: Quaternion) -> Quaternion: ...
    def Length(self) -> float: ...
    def LengthSquared(self) -> float: ...
    @staticmethod
    def Lerp(quaternion1: Quaternion, quaternion2: Quaternion, amount: float) -> Quaternion: ...
    @staticmethod
    def Negate(value: Quaternion) -> Quaternion: ...
    @staticmethod
    def Normalize(value: Quaternion) -> Quaternion: ...
    def __add__(self, value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    def __truediv__(self, value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    def __eq__(self, value1: Quaternion, value2: Quaternion) -> bool: ...
    def __ne__(self, value1: Quaternion, value2: Quaternion) -> bool: ...
    @typing.overload
    def __mul__(self, value1: Quaternion, value2: float) -> Quaternion: ...
    @typing.overload
    def __mul__(self, value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    def __sub__(self, value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    def __neg__(self, value: Quaternion) -> Quaternion: ...
    @staticmethod
    def Slerp(quaternion1: Quaternion, quaternion2: Quaternion, amount: float) -> Quaternion: ...
    @staticmethod
    def Subtract(value1: Quaternion, value2: Quaternion) -> Quaternion: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Quaternion) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, value1: Quaternion, value2: float) -> Quaternion:...
        @typing.overload
        def __call__(self, value1: Quaternion, value2: Quaternion) -> Quaternion:...



class Vector_GenericClasses(abc.ABCMeta):
    Generic_Vector_GenericClasses_Vector_1_T = typing.TypeVar('Generic_Vector_GenericClasses_Vector_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector_GenericClasses_Vector_1_T]) -> typing.Type[Vector_1[Generic_Vector_GenericClasses_Vector_1_T]]: ...

class Vector(Vector_0, metaclass =Vector_GenericClasses): ...

class Vector_0(abc.ABC):
    @classmethod
    @property
    def IsHardwareAccelerated(cls) -> bool: ...
    @staticmethod
    def ConvertToInt32(value: Vector_1[float]) -> Vector_1[int]: ...
    @staticmethod
    def ConvertToInt64(value: Vector_1[float]) -> Vector_1[int]: ...
    @staticmethod
    def ConvertToUInt32(value: Vector_1[float]) -> Vector_1[int]: ...
    @staticmethod
    def ConvertToUInt64(value: Vector_1[float]) -> Vector_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __getitem__(self, t:typing.Type[Abs_1_T1]) -> Abs_1[Abs_1_T1]: ...

        Abs_1_T1 = typing.TypeVar('Abs_1_T1')
        class Abs_1(typing.Generic[Abs_1_T1]):
            Abs_1_T = Vector_0.Abs_MethodGroup.Abs_1_T1
            def __call__(self, value: Vector_1[Abs_1_T]) -> Vector_1[Abs_1_T]:...


    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __getitem__(self, t:typing.Type[Add_1_T1]) -> Add_1[Add_1_T1]: ...

        Add_1_T1 = typing.TypeVar('Add_1_T1')
        class Add_1(typing.Generic[Add_1_T1]):
            Add_1_T = Vector_0.Add_MethodGroup.Add_1_T1
            def __call__(self, left: Vector_1[Add_1_T], right: Vector_1[Add_1_T]) -> Vector_1[Add_1_T]:...


    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __getitem__(self, t:typing.Type[AndNot_1_T1]) -> AndNot_1[AndNot_1_T1]: ...

        AndNot_1_T1 = typing.TypeVar('AndNot_1_T1')
        class AndNot_1(typing.Generic[AndNot_1_T1]):
            AndNot_1_T = Vector_0.AndNot_MethodGroup.AndNot_1_T1
            def __call__(self, left: Vector_1[AndNot_1_T], right: Vector_1[AndNot_1_T]) -> Vector_1[AndNot_1_T]:...


    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_TFrom = Vector_0.As_MethodGroup.As_2_T1
            As_2_TTo = Vector_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector_1[As_2_TFrom]) -> Vector_1[As_2_TTo]:...


    # Skipped AsVectorByte due to it being static, abstract and generic.

    AsVectorByte : AsVectorByte_MethodGroup
    class AsVectorByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorByte_1_T1]) -> AsVectorByte_1[AsVectorByte_1_T1]: ...

        AsVectorByte_1_T1 = typing.TypeVar('AsVectorByte_1_T1')
        class AsVectorByte_1(typing.Generic[AsVectorByte_1_T1]):
            AsVectorByte_1_T = Vector_0.AsVectorByte_MethodGroup.AsVectorByte_1_T1
            def __call__(self, value: Vector_1[AsVectorByte_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorDouble due to it being static, abstract and generic.

    AsVectorDouble : AsVectorDouble_MethodGroup
    class AsVectorDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorDouble_1_T1]) -> AsVectorDouble_1[AsVectorDouble_1_T1]: ...

        AsVectorDouble_1_T1 = typing.TypeVar('AsVectorDouble_1_T1')
        class AsVectorDouble_1(typing.Generic[AsVectorDouble_1_T1]):
            AsVectorDouble_1_T = Vector_0.AsVectorDouble_MethodGroup.AsVectorDouble_1_T1
            def __call__(self, value: Vector_1[AsVectorDouble_1_T]) -> Vector_1[float]:...


    # Skipped AsVectorInt16 due to it being static, abstract and generic.

    AsVectorInt16 : AsVectorInt16_MethodGroup
    class AsVectorInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorInt16_1_T1]) -> AsVectorInt16_1[AsVectorInt16_1_T1]: ...

        AsVectorInt16_1_T1 = typing.TypeVar('AsVectorInt16_1_T1')
        class AsVectorInt16_1(typing.Generic[AsVectorInt16_1_T1]):
            AsVectorInt16_1_T = Vector_0.AsVectorInt16_MethodGroup.AsVectorInt16_1_T1
            def __call__(self, value: Vector_1[AsVectorInt16_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorInt32 due to it being static, abstract and generic.

    AsVectorInt32 : AsVectorInt32_MethodGroup
    class AsVectorInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorInt32_1_T1]) -> AsVectorInt32_1[AsVectorInt32_1_T1]: ...

        AsVectorInt32_1_T1 = typing.TypeVar('AsVectorInt32_1_T1')
        class AsVectorInt32_1(typing.Generic[AsVectorInt32_1_T1]):
            AsVectorInt32_1_T = Vector_0.AsVectorInt32_MethodGroup.AsVectorInt32_1_T1
            def __call__(self, value: Vector_1[AsVectorInt32_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorInt64 due to it being static, abstract and generic.

    AsVectorInt64 : AsVectorInt64_MethodGroup
    class AsVectorInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorInt64_1_T1]) -> AsVectorInt64_1[AsVectorInt64_1_T1]: ...

        AsVectorInt64_1_T1 = typing.TypeVar('AsVectorInt64_1_T1')
        class AsVectorInt64_1(typing.Generic[AsVectorInt64_1_T1]):
            AsVectorInt64_1_T = Vector_0.AsVectorInt64_MethodGroup.AsVectorInt64_1_T1
            def __call__(self, value: Vector_1[AsVectorInt64_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorNInt due to it being static, abstract and generic.

    AsVectorNInt : AsVectorNInt_MethodGroup
    class AsVectorNInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorNInt_1_T1]) -> AsVectorNInt_1[AsVectorNInt_1_T1]: ...

        AsVectorNInt_1_T1 = typing.TypeVar('AsVectorNInt_1_T1')
        class AsVectorNInt_1(typing.Generic[AsVectorNInt_1_T1]):
            AsVectorNInt_1_T = Vector_0.AsVectorNInt_MethodGroup.AsVectorNInt_1_T1
            def __call__(self, value: Vector_1[AsVectorNInt_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorNUInt due to it being static, abstract and generic.

    AsVectorNUInt : AsVectorNUInt_MethodGroup
    class AsVectorNUInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorNUInt_1_T1]) -> AsVectorNUInt_1[AsVectorNUInt_1_T1]: ...

        AsVectorNUInt_1_T1 = typing.TypeVar('AsVectorNUInt_1_T1')
        class AsVectorNUInt_1(typing.Generic[AsVectorNUInt_1_T1]):
            AsVectorNUInt_1_T = Vector_0.AsVectorNUInt_MethodGroup.AsVectorNUInt_1_T1
            def __call__(self, value: Vector_1[AsVectorNUInt_1_T]) -> Vector_1[UIntPtr]:...


    # Skipped AsVectorSByte due to it being static, abstract and generic.

    AsVectorSByte : AsVectorSByte_MethodGroup
    class AsVectorSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorSByte_1_T1]) -> AsVectorSByte_1[AsVectorSByte_1_T1]: ...

        AsVectorSByte_1_T1 = typing.TypeVar('AsVectorSByte_1_T1')
        class AsVectorSByte_1(typing.Generic[AsVectorSByte_1_T1]):
            AsVectorSByte_1_T = Vector_0.AsVectorSByte_MethodGroup.AsVectorSByte_1_T1
            def __call__(self, value: Vector_1[AsVectorSByte_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorSingle due to it being static, abstract and generic.

    AsVectorSingle : AsVectorSingle_MethodGroup
    class AsVectorSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorSingle_1_T1]) -> AsVectorSingle_1[AsVectorSingle_1_T1]: ...

        AsVectorSingle_1_T1 = typing.TypeVar('AsVectorSingle_1_T1')
        class AsVectorSingle_1(typing.Generic[AsVectorSingle_1_T1]):
            AsVectorSingle_1_T = Vector_0.AsVectorSingle_MethodGroup.AsVectorSingle_1_T1
            def __call__(self, value: Vector_1[AsVectorSingle_1_T]) -> Vector_1[float]:...


    # Skipped AsVectorUInt16 due to it being static, abstract and generic.

    AsVectorUInt16 : AsVectorUInt16_MethodGroup
    class AsVectorUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorUInt16_1_T1]) -> AsVectorUInt16_1[AsVectorUInt16_1_T1]: ...

        AsVectorUInt16_1_T1 = typing.TypeVar('AsVectorUInt16_1_T1')
        class AsVectorUInt16_1(typing.Generic[AsVectorUInt16_1_T1]):
            AsVectorUInt16_1_T = Vector_0.AsVectorUInt16_MethodGroup.AsVectorUInt16_1_T1
            def __call__(self, value: Vector_1[AsVectorUInt16_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorUInt32 due to it being static, abstract and generic.

    AsVectorUInt32 : AsVectorUInt32_MethodGroup
    class AsVectorUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorUInt32_1_T1]) -> AsVectorUInt32_1[AsVectorUInt32_1_T1]: ...

        AsVectorUInt32_1_T1 = typing.TypeVar('AsVectorUInt32_1_T1')
        class AsVectorUInt32_1(typing.Generic[AsVectorUInt32_1_T1]):
            AsVectorUInt32_1_T = Vector_0.AsVectorUInt32_MethodGroup.AsVectorUInt32_1_T1
            def __call__(self, value: Vector_1[AsVectorUInt32_1_T]) -> Vector_1[int]:...


    # Skipped AsVectorUInt64 due to it being static, abstract and generic.

    AsVectorUInt64 : AsVectorUInt64_MethodGroup
    class AsVectorUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVectorUInt64_1_T1]) -> AsVectorUInt64_1[AsVectorUInt64_1_T1]: ...

        AsVectorUInt64_1_T1 = typing.TypeVar('AsVectorUInt64_1_T1')
        class AsVectorUInt64_1(typing.Generic[AsVectorUInt64_1_T1]):
            AsVectorUInt64_1_T = Vector_0.AsVectorUInt64_MethodGroup.AsVectorUInt64_1_T1
            def __call__(self, value: Vector_1[AsVectorUInt64_1_T]) -> Vector_1[int]:...


    # Skipped BitwiseAnd due to it being static, abstract and generic.

    BitwiseAnd : BitwiseAnd_MethodGroup
    class BitwiseAnd_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseAnd_1_T1]) -> BitwiseAnd_1[BitwiseAnd_1_T1]: ...

        BitwiseAnd_1_T1 = typing.TypeVar('BitwiseAnd_1_T1')
        class BitwiseAnd_1(typing.Generic[BitwiseAnd_1_T1]):
            BitwiseAnd_1_T = Vector_0.BitwiseAnd_MethodGroup.BitwiseAnd_1_T1
            def __call__(self, left: Vector_1[BitwiseAnd_1_T], right: Vector_1[BitwiseAnd_1_T]) -> Vector_1[BitwiseAnd_1_T]:...


    # Skipped BitwiseOr due to it being static, abstract and generic.

    BitwiseOr : BitwiseOr_MethodGroup
    class BitwiseOr_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseOr_1_T1]) -> BitwiseOr_1[BitwiseOr_1_T1]: ...

        BitwiseOr_1_T1 = typing.TypeVar('BitwiseOr_1_T1')
        class BitwiseOr_1(typing.Generic[BitwiseOr_1_T1]):
            BitwiseOr_1_T = Vector_0.BitwiseOr_MethodGroup.BitwiseOr_1_T1
            def __call__(self, left: Vector_1[BitwiseOr_1_T], right: Vector_1[BitwiseOr_1_T]) -> Vector_1[BitwiseOr_1_T]:...


    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method Ceiling(value : Vector`1) was skipped since it collides with above method

    # Skipped ConditionalSelect due to it being static, abstract and generic.

    ConditionalSelect : ConditionalSelect_MethodGroup
    class ConditionalSelect_MethodGroup:
        def __getitem__(self, t:typing.Type[ConditionalSelect_1_T1]) -> ConditionalSelect_1[ConditionalSelect_1_T1]: ...

        ConditionalSelect_1_T1 = typing.TypeVar('ConditionalSelect_1_T1')
        class ConditionalSelect_1(typing.Generic[ConditionalSelect_1_T1]):
            ConditionalSelect_1_T = Vector_0.ConditionalSelect_MethodGroup.ConditionalSelect_1_T1
            def __call__(self, condition: Vector_1[ConditionalSelect_1_T], left: Vector_1[ConditionalSelect_1_T], right: Vector_1[ConditionalSelect_1_T]) -> Vector_1[ConditionalSelect_1_T]:...

        def __call__(self, condition: Vector_1[int], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method ConditionalSelect(condition : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToDouble due to it being static, abstract and generic.

    ConvertToDouble : ConvertToDouble_MethodGroup
    class ConvertToDouble_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[float]:...
        # Method ConvertToDouble(value : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[float]:...
        # Method ConvertToSingle(value : Vector`1) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __getitem__(self, t:typing.Type[Divide_1_T1]) -> Divide_1[Divide_1_T1]: ...

        Divide_1_T1 = typing.TypeVar('Divide_1_T1')
        class Divide_1(typing.Generic[Divide_1_T1]):
            Divide_1_T = Vector_0.Divide_MethodGroup.Divide_1_T1
            def __call__(self, left: Vector_1[Divide_1_T], right: Vector_1[Divide_1_T]) -> Vector_1[Divide_1_T]:...


    # Skipped Dot due to it being static, abstract and generic.

    Dot : Dot_MethodGroup
    class Dot_MethodGroup:
        def __getitem__(self, t:typing.Type[Dot_1_T1]) -> Dot_1[Dot_1_T1]: ...

        Dot_1_T1 = typing.TypeVar('Dot_1_T1')
        class Dot_1(typing.Generic[Dot_1_T1]):
            Dot_1_T = Vector_0.Dot_MethodGroup.Dot_1_T1
            def __call__(self, left: Vector_1[Dot_1_T], right: Vector_1[Dot_1_T]) -> Dot_1_T:...


    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        def __getitem__(self, t:typing.Type[Equals_1_T1]) -> Equals_1[Equals_1_T1]: ...

        Equals_1_T1 = typing.TypeVar('Equals_1_T1')
        class Equals_1(typing.Generic[Equals_1_T1]):
            Equals_1_T = Vector_0.Equals_MethodGroup.Equals_1_T1
            def __call__(self, left: Vector_1[Equals_1_T], right: Vector_1[Equals_1_T]) -> Vector_1[Equals_1_T]:...

        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[int]:...
        # Method Equals(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Equals(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Equals(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped EqualsAll due to it being static, abstract and generic.

    EqualsAll : EqualsAll_MethodGroup
    class EqualsAll_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAll_1_T1]) -> EqualsAll_1[EqualsAll_1_T1]: ...

        EqualsAll_1_T1 = typing.TypeVar('EqualsAll_1_T1')
        class EqualsAll_1(typing.Generic[EqualsAll_1_T1]):
            EqualsAll_1_T = Vector_0.EqualsAll_MethodGroup.EqualsAll_1_T1
            def __call__(self, left: Vector_1[EqualsAll_1_T], right: Vector_1[EqualsAll_1_T]) -> bool:...


    # Skipped EqualsAny due to it being static, abstract and generic.

    EqualsAny : EqualsAny_MethodGroup
    class EqualsAny_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAny_1_T1]) -> EqualsAny_1[EqualsAny_1_T1]: ...

        EqualsAny_1_T1 = typing.TypeVar('EqualsAny_1_T1')
        class EqualsAny_1(typing.Generic[EqualsAny_1_T1]):
            EqualsAny_1_T = Vector_0.EqualsAny_MethodGroup.EqualsAny_1_T1
            def __call__(self, left: Vector_1[EqualsAny_1_T], right: Vector_1[EqualsAny_1_T]) -> bool:...


    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method Floor(value : Vector`1) was skipped since it collides with above method

    # Skipped GreaterThan due to it being static, abstract and generic.

    GreaterThan : GreaterThan_MethodGroup
    class GreaterThan_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThan_1_T1]) -> GreaterThan_1[GreaterThan_1_T1]: ...

        GreaterThan_1_T1 = typing.TypeVar('GreaterThan_1_T1')
        class GreaterThan_1(typing.Generic[GreaterThan_1_T1]):
            GreaterThan_1_T = Vector_0.GreaterThan_MethodGroup.GreaterThan_1_T1
            def __call__(self, left: Vector_1[GreaterThan_1_T], right: Vector_1[GreaterThan_1_T]) -> Vector_1[GreaterThan_1_T]:...

        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[int]:...
        # Method GreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method GreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method GreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped GreaterThanAll due to it being static, abstract and generic.

    GreaterThanAll : GreaterThanAll_MethodGroup
    class GreaterThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAll_1_T1]) -> GreaterThanAll_1[GreaterThanAll_1_T1]: ...

        GreaterThanAll_1_T1 = typing.TypeVar('GreaterThanAll_1_T1')
        class GreaterThanAll_1(typing.Generic[GreaterThanAll_1_T1]):
            GreaterThanAll_1_T = Vector_0.GreaterThanAll_MethodGroup.GreaterThanAll_1_T1
            def __call__(self, left: Vector_1[GreaterThanAll_1_T], right: Vector_1[GreaterThanAll_1_T]) -> bool:...


    # Skipped GreaterThanAny due to it being static, abstract and generic.

    GreaterThanAny : GreaterThanAny_MethodGroup
    class GreaterThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAny_1_T1]) -> GreaterThanAny_1[GreaterThanAny_1_T1]: ...

        GreaterThanAny_1_T1 = typing.TypeVar('GreaterThanAny_1_T1')
        class GreaterThanAny_1(typing.Generic[GreaterThanAny_1_T1]):
            GreaterThanAny_1_T = Vector_0.GreaterThanAny_MethodGroup.GreaterThanAny_1_T1
            def __call__(self, left: Vector_1[GreaterThanAny_1_T], right: Vector_1[GreaterThanAny_1_T]) -> bool:...


    # Skipped GreaterThanOrEqual due to it being static, abstract and generic.

    GreaterThanOrEqual : GreaterThanOrEqual_MethodGroup
    class GreaterThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqual_1_T1]) -> GreaterThanOrEqual_1[GreaterThanOrEqual_1_T1]: ...

        GreaterThanOrEqual_1_T1 = typing.TypeVar('GreaterThanOrEqual_1_T1')
        class GreaterThanOrEqual_1(typing.Generic[GreaterThanOrEqual_1_T1]):
            GreaterThanOrEqual_1_T = Vector_0.GreaterThanOrEqual_MethodGroup.GreaterThanOrEqual_1_T1
            def __call__(self, left: Vector_1[GreaterThanOrEqual_1_T], right: Vector_1[GreaterThanOrEqual_1_T]) -> Vector_1[GreaterThanOrEqual_1_T]:...

        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[int]:...
        # Method GreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method GreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method GreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped GreaterThanOrEqualAll due to it being static, abstract and generic.

    GreaterThanOrEqualAll : GreaterThanOrEqualAll_MethodGroup
    class GreaterThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAll_1_T1]) -> GreaterThanOrEqualAll_1[GreaterThanOrEqualAll_1_T1]: ...

        GreaterThanOrEqualAll_1_T1 = typing.TypeVar('GreaterThanOrEqualAll_1_T1')
        class GreaterThanOrEqualAll_1(typing.Generic[GreaterThanOrEqualAll_1_T1]):
            GreaterThanOrEqualAll_1_T = Vector_0.GreaterThanOrEqualAll_MethodGroup.GreaterThanOrEqualAll_1_T1
            def __call__(self, left: Vector_1[GreaterThanOrEqualAll_1_T], right: Vector_1[GreaterThanOrEqualAll_1_T]) -> bool:...


    # Skipped GreaterThanOrEqualAny due to it being static, abstract and generic.

    GreaterThanOrEqualAny : GreaterThanOrEqualAny_MethodGroup
    class GreaterThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAny_1_T1]) -> GreaterThanOrEqualAny_1[GreaterThanOrEqualAny_1_T1]: ...

        GreaterThanOrEqualAny_1_T1 = typing.TypeVar('GreaterThanOrEqualAny_1_T1')
        class GreaterThanOrEqualAny_1(typing.Generic[GreaterThanOrEqualAny_1_T1]):
            GreaterThanOrEqualAny_1_T = Vector_0.GreaterThanOrEqualAny_MethodGroup.GreaterThanOrEqualAny_1_T1
            def __call__(self, left: Vector_1[GreaterThanOrEqualAny_1_T], right: Vector_1[GreaterThanOrEqualAny_1_T]) -> bool:...


    # Skipped LessThan due to it being static, abstract and generic.

    LessThan : LessThan_MethodGroup
    class LessThan_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThan_1_T1]) -> LessThan_1[LessThan_1_T1]: ...

        LessThan_1_T1 = typing.TypeVar('LessThan_1_T1')
        class LessThan_1(typing.Generic[LessThan_1_T1]):
            LessThan_1_T = Vector_0.LessThan_MethodGroup.LessThan_1_T1
            def __call__(self, left: Vector_1[LessThan_1_T], right: Vector_1[LessThan_1_T]) -> Vector_1[LessThan_1_T]:...

        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[int]:...
        # Method LessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method LessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method LessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped LessThanAll due to it being static, abstract and generic.

    LessThanAll : LessThanAll_MethodGroup
    class LessThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAll_1_T1]) -> LessThanAll_1[LessThanAll_1_T1]: ...

        LessThanAll_1_T1 = typing.TypeVar('LessThanAll_1_T1')
        class LessThanAll_1(typing.Generic[LessThanAll_1_T1]):
            LessThanAll_1_T = Vector_0.LessThanAll_MethodGroup.LessThanAll_1_T1
            def __call__(self, left: Vector_1[LessThanAll_1_T], right: Vector_1[LessThanAll_1_T]) -> bool:...


    # Skipped LessThanAny due to it being static, abstract and generic.

    LessThanAny : LessThanAny_MethodGroup
    class LessThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAny_1_T1]) -> LessThanAny_1[LessThanAny_1_T1]: ...

        LessThanAny_1_T1 = typing.TypeVar('LessThanAny_1_T1')
        class LessThanAny_1(typing.Generic[LessThanAny_1_T1]):
            LessThanAny_1_T = Vector_0.LessThanAny_MethodGroup.LessThanAny_1_T1
            def __call__(self, left: Vector_1[LessThanAny_1_T], right: Vector_1[LessThanAny_1_T]) -> bool:...


    # Skipped LessThanOrEqual due to it being static, abstract and generic.

    LessThanOrEqual : LessThanOrEqual_MethodGroup
    class LessThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqual_1_T1]) -> LessThanOrEqual_1[LessThanOrEqual_1_T1]: ...

        LessThanOrEqual_1_T1 = typing.TypeVar('LessThanOrEqual_1_T1')
        class LessThanOrEqual_1(typing.Generic[LessThanOrEqual_1_T1]):
            LessThanOrEqual_1_T = Vector_0.LessThanOrEqual_MethodGroup.LessThanOrEqual_1_T1
            def __call__(self, left: Vector_1[LessThanOrEqual_1_T], right: Vector_1[LessThanOrEqual_1_T]) -> Vector_1[LessThanOrEqual_1_T]:...

        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[int]:...
        # Method LessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method LessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method LessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped LessThanOrEqualAll due to it being static, abstract and generic.

    LessThanOrEqualAll : LessThanOrEqualAll_MethodGroup
    class LessThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAll_1_T1]) -> LessThanOrEqualAll_1[LessThanOrEqualAll_1_T1]: ...

        LessThanOrEqualAll_1_T1 = typing.TypeVar('LessThanOrEqualAll_1_T1')
        class LessThanOrEqualAll_1(typing.Generic[LessThanOrEqualAll_1_T1]):
            LessThanOrEqualAll_1_T = Vector_0.LessThanOrEqualAll_MethodGroup.LessThanOrEqualAll_1_T1
            def __call__(self, left: Vector_1[LessThanOrEqualAll_1_T], right: Vector_1[LessThanOrEqualAll_1_T]) -> bool:...


    # Skipped LessThanOrEqualAny due to it being static, abstract and generic.

    LessThanOrEqualAny : LessThanOrEqualAny_MethodGroup
    class LessThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAny_1_T1]) -> LessThanOrEqualAny_1[LessThanOrEqualAny_1_T1]: ...

        LessThanOrEqualAny_1_T1 = typing.TypeVar('LessThanOrEqualAny_1_T1')
        class LessThanOrEqualAny_1(typing.Generic[LessThanOrEqualAny_1_T1]):
            LessThanOrEqualAny_1_T = Vector_0.LessThanOrEqualAny_MethodGroup.LessThanOrEqualAny_1_T1
            def __call__(self, left: Vector_1[LessThanOrEqualAny_1_T], right: Vector_1[LessThanOrEqualAny_1_T]) -> bool:...


    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __getitem__(self, t:typing.Type[Max_1_T1]) -> Max_1[Max_1_T1]: ...

        Max_1_T1 = typing.TypeVar('Max_1_T1')
        class Max_1(typing.Generic[Max_1_T1]):
            Max_1_T = Vector_0.Max_MethodGroup.Max_1_T1
            def __call__(self, left: Vector_1[Max_1_T], right: Vector_1[Max_1_T]) -> Vector_1[Max_1_T]:...


    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __getitem__(self, t:typing.Type[Min_1_T1]) -> Min_1[Min_1_T1]: ...

        Min_1_T1 = typing.TypeVar('Min_1_T1')
        class Min_1(typing.Generic[Min_1_T1]):
            Min_1_T = Vector_0.Min_MethodGroup.Min_1_T1
            def __call__(self, left: Vector_1[Min_1_T], right: Vector_1[Min_1_T]) -> Vector_1[Min_1_T]:...


    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __getitem__(self, t:typing.Type[Multiply_1_T1]) -> Multiply_1[Multiply_1_T1]: ...

        Multiply_1_T1 = typing.TypeVar('Multiply_1_T1')
        class Multiply_1(typing.Generic[Multiply_1_T1]):
            Multiply_1_T = Vector_0.Multiply_MethodGroup.Multiply_1_T1
            @typing.overload
            def __call__(self, left: Vector_1[Multiply_1_T], right: Vector_1[Multiply_1_T]) -> Vector_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Vector_1[Multiply_1_T], right: Multiply_1_T) -> Vector_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Multiply_1_T, right: Vector_1[Multiply_1_T]) -> Vector_1[Multiply_1_T]:...


    # Skipped Narrow due to it being static, abstract and generic.

    Narrow : Narrow_MethodGroup
    class Narrow_MethodGroup:
        def __call__(self, low: Vector_1[float], high: Vector_1[float]) -> Vector_1[float]:...
        # Method Narrow(low : Vector`1, high : Vector`1) was skipped since it collides with above method
        # Method Narrow(low : Vector`1, high : Vector`1) was skipped since it collides with above method
        # Method Narrow(low : Vector`1, high : Vector`1) was skipped since it collides with above method
        # Method Narrow(low : Vector`1, high : Vector`1) was skipped since it collides with above method
        # Method Narrow(low : Vector`1, high : Vector`1) was skipped since it collides with above method
        # Method Narrow(low : Vector`1, high : Vector`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        def __getitem__(self, t:typing.Type[Negate_1_T1]) -> Negate_1[Negate_1_T1]: ...

        Negate_1_T1 = typing.TypeVar('Negate_1_T1')
        class Negate_1(typing.Generic[Negate_1_T1]):
            Negate_1_T = Vector_0.Negate_MethodGroup.Negate_1_T1
            def __call__(self, value: Vector_1[Negate_1_T]) -> Vector_1[Negate_1_T]:...


    # Skipped OnesComplement due to it being static, abstract and generic.

    OnesComplement : OnesComplement_MethodGroup
    class OnesComplement_MethodGroup:
        def __getitem__(self, t:typing.Type[OnesComplement_1_T1]) -> OnesComplement_1[OnesComplement_1_T1]: ...

        OnesComplement_1_T1 = typing.TypeVar('OnesComplement_1_T1')
        class OnesComplement_1(typing.Generic[OnesComplement_1_T1]):
            OnesComplement_1_T = Vector_0.OnesComplement_MethodGroup.OnesComplement_1_T1
            def __call__(self, value: Vector_1[OnesComplement_1_T]) -> Vector_1[OnesComplement_1_T]:...


    # Skipped SquareRoot due to it being static, abstract and generic.

    SquareRoot : SquareRoot_MethodGroup
    class SquareRoot_MethodGroup:
        def __getitem__(self, t:typing.Type[SquareRoot_1_T1]) -> SquareRoot_1[SquareRoot_1_T1]: ...

        SquareRoot_1_T1 = typing.TypeVar('SquareRoot_1_T1')
        class SquareRoot_1(typing.Generic[SquareRoot_1_T1]):
            SquareRoot_1_T = Vector_0.SquareRoot_MethodGroup.SquareRoot_1_T1
            def __call__(self, value: Vector_1[SquareRoot_1_T]) -> Vector_1[SquareRoot_1_T]:...


    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __getitem__(self, t:typing.Type[Subtract_1_T1]) -> Subtract_1[Subtract_1_T1]: ...

        Subtract_1_T1 = typing.TypeVar('Subtract_1_T1')
        class Subtract_1(typing.Generic[Subtract_1_T1]):
            Subtract_1_T = Vector_0.Subtract_MethodGroup.Subtract_1_T1
            def __call__(self, left: Vector_1[Subtract_1_T], right: Vector_1[Subtract_1_T]) -> Vector_1[Subtract_1_T]:...


    # Skipped Sum due to it being static, abstract and generic.

    Sum : Sum_MethodGroup
    class Sum_MethodGroup:
        def __getitem__(self, t:typing.Type[Sum_1_T1]) -> Sum_1[Sum_1_T1]: ...

        Sum_1_T1 = typing.TypeVar('Sum_1_T1')
        class Sum_1(typing.Generic[Sum_1_T1]):
            Sum_1_T = Vector_0.Sum_MethodGroup.Sum_1_T1
            def __call__(self, value: Vector_1[Sum_1_T]) -> Sum_1_T:...


    # Skipped Widen due to it being static, abstract and generic.

    Widen : Widen_MethodGroup
    class Widen_MethodGroup:
        def __call__(self, source: Vector_1[float], low: clr.Reference[Vector_1[float]], high: clr.Reference[Vector_1[float]]) -> None:...
        # Method Widen(source : Vector`1, low : Vector`1&, high : Vector`1&) was skipped since it collides with above method
        # Method Widen(source : Vector`1, low : Vector`1&, high : Vector`1&) was skipped since it collides with above method
        # Method Widen(source : Vector`1, low : Vector`1&, high : Vector`1&) was skipped since it collides with above method
        # Method Widen(source : Vector`1, low : Vector`1&, high : Vector`1&) was skipped since it collides with above method
        # Method Widen(source : Vector`1, low : Vector`1&, high : Vector`1&) was skipped since it collides with above method
        # Method Widen(source : Vector`1, low : Vector`1&, high : Vector`1&) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __getitem__(self, t:typing.Type[Xor_1_T1]) -> Xor_1[Xor_1_T1]: ...

        Xor_1_T1 = typing.TypeVar('Xor_1_T1')
        class Xor_1(typing.Generic[Xor_1_T1]):
            Xor_1_T = Vector_0.Xor_MethodGroup.Xor_1_T1
            def __call__(self, left: Vector_1[Xor_1_T], right: Vector_1[Xor_1_T]) -> Vector_1[Xor_1_T]:...




Vector_1_T = typing.TypeVar('Vector_1_T')
class Vector_1(typing.Generic[Vector_1_T], IFormattable, IEquatable_1[Vector_1[Vector_1_T]]):
    @typing.overload
    def __init__(self, value: Vector_1_T) -> None: ...
    @typing.overload
    def __init__(self, values: Array_1[Vector_1_T]) -> None: ...
    @typing.overload
    def __init__(self, values: ReadOnlySpan_1[int]) -> None: ...
    @typing.overload
    def __init__(self, values: ReadOnlySpan_1[Vector_1_T]) -> None: ...
    @typing.overload
    def __init__(self, values: Span_1[Vector_1_T]) -> None: ...
    @typing.overload
    def __init__(self, values: Array_1[Vector_1_T], index: int) -> None: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @property
    def Item(self) -> Vector_1_T: ...
    @classmethod
    @property
    def One(cls) -> Vector_1[Vector_1_T]: ...
    @classmethod
    @property
    def Zero(cls) -> Vector_1[Vector_1_T]: ...
    def GetHashCode(self) -> int: ...
    def __add__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __and__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __or__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __truediv__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __eq__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> bool: ...
    def __xor__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    # Operator not supported op_Explicit(value: Vector`1)
    def __ne__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> bool: ...
    @typing.overload
    def __mul__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    @typing.overload
    def __mul__(self, value: Vector_1[Vector_1_T], factor: Vector_1_T) -> Vector_1[Vector_1_T]: ...
    @typing.overload
    def __mul__(self, factor: Vector_1_T, value: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __invert__(self, value: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __sub__(self, left: Vector_1[Vector_1_T], right: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    def __neg__(self, value: Vector_1[Vector_1_T]) -> Vector_1[Vector_1_T]: ...
    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup[Vector_1_T]
    CopyTo_MethodGroup_Vector_1_T = typing.TypeVar('CopyTo_MethodGroup_Vector_1_T')
    class CopyTo_MethodGroup(typing.Generic[CopyTo_MethodGroup_Vector_1_T]):
        CopyTo_MethodGroup_Vector_1_T = Vector_1.CopyTo_MethodGroup_Vector_1_T
        @typing.overload
        def __call__(self, destination: Array_1[CopyTo_MethodGroup_Vector_1_T]) -> None:...
        @typing.overload
        def __call__(self, destination: Span_1[int]) -> None:...
        @typing.overload
        def __call__(self, destination: Span_1[CopyTo_MethodGroup_Vector_1_T]) -> None:...
        @typing.overload
        def __call__(self, destination: Array_1[CopyTo_MethodGroup_Vector_1_T], startIndex: int) -> None:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector_1_T]
    Equals_MethodGroup_Vector_1_T = typing.TypeVar('Equals_MethodGroup_Vector_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector_1_T]):
        Equals_MethodGroup_Vector_1_T = Vector_1.Equals_MethodGroup_Vector_1_T
        @typing.overload
        def __call__(self, other: Vector_1[Equals_MethodGroup_Vector_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped ToString due to it being static, abstract and generic.

    ToString : ToString_MethodGroup[Vector_1_T]
    ToString_MethodGroup_Vector_1_T = typing.TypeVar('ToString_MethodGroup_Vector_1_T')
    class ToString_MethodGroup(typing.Generic[ToString_MethodGroup_Vector_1_T]):
        ToString_MethodGroup_Vector_1_T = Vector_1.ToString_MethodGroup_Vector_1_T
        @typing.overload
        def __call__(self) -> str:...
        @typing.overload
        def __call__(self, format: str) -> str:...
        @typing.overload
        def __call__(self, format: str, formatProvider: IFormatProvider) -> str:...

    # Skipped TryCopyTo due to it being static, abstract and generic.

    TryCopyTo : TryCopyTo_MethodGroup[Vector_1_T]
    TryCopyTo_MethodGroup_Vector_1_T = typing.TypeVar('TryCopyTo_MethodGroup_Vector_1_T')
    class TryCopyTo_MethodGroup(typing.Generic[TryCopyTo_MethodGroup_Vector_1_T]):
        TryCopyTo_MethodGroup_Vector_1_T = Vector_1.TryCopyTo_MethodGroup_Vector_1_T
        @typing.overload
        def __call__(self, destination: Span_1[int]) -> bool:...
        @typing.overload
        def __call__(self, destination: Span_1[TryCopyTo_MethodGroup_Vector_1_T]) -> bool:...



class Vector2(IFormattable, IEquatable_1[Vector2]):
    @typing.overload
    def __init__(self, value: float) -> None: ...
    @typing.overload
    def __init__(self, values: ReadOnlySpan_1[float]) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float) -> None: ...
    X : float
    Y : float
    @classmethod
    @property
    def One(cls) -> Vector2: ...
    @classmethod
    @property
    def UnitX(cls) -> Vector2: ...
    @classmethod
    @property
    def UnitY(cls) -> Vector2: ...
    @classmethod
    @property
    def Zero(cls) -> Vector2: ...
    @staticmethod
    def Abs(value: Vector2) -> Vector2: ...
    @staticmethod
    def Add(left: Vector2, right: Vector2) -> Vector2: ...
    @staticmethod
    def Clamp(value1: Vector2, min: Vector2, max: Vector2) -> Vector2: ...
    @staticmethod
    def Distance(value1: Vector2, value2: Vector2) -> float: ...
    @staticmethod
    def DistanceSquared(value1: Vector2, value2: Vector2) -> float: ...
    @staticmethod
    def Dot(value1: Vector2, value2: Vector2) -> float: ...
    def GetHashCode(self) -> int: ...
    def Length(self) -> float: ...
    def LengthSquared(self) -> float: ...
    @staticmethod
    def Lerp(value1: Vector2, value2: Vector2, amount: float) -> Vector2: ...
    @staticmethod
    def Max(value1: Vector2, value2: Vector2) -> Vector2: ...
    @staticmethod
    def Min(value1: Vector2, value2: Vector2) -> Vector2: ...
    @staticmethod
    def Negate(value: Vector2) -> Vector2: ...
    @staticmethod
    def Normalize(value: Vector2) -> Vector2: ...
    def __add__(self, left: Vector2, right: Vector2) -> Vector2: ...
    @typing.overload
    def __truediv__(self, value1: Vector2, value2: float) -> Vector2: ...
    @typing.overload
    def __truediv__(self, left: Vector2, right: Vector2) -> Vector2: ...
    def __eq__(self, left: Vector2, right: Vector2) -> bool: ...
    def __ne__(self, left: Vector2, right: Vector2) -> bool: ...
    @typing.overload
    def __mul__(self, left: float, right: Vector2) -> Vector2: ...
    @typing.overload
    def __mul__(self, left: Vector2, right: float) -> Vector2: ...
    @typing.overload
    def __mul__(self, left: Vector2, right: Vector2) -> Vector2: ...
    def __sub__(self, left: Vector2, right: Vector2) -> Vector2: ...
    def __neg__(self, value: Vector2) -> Vector2: ...
    @staticmethod
    def Reflect(vector: Vector2, normal: Vector2) -> Vector2: ...
    @staticmethod
    def SquareRoot(value: Vector2) -> Vector2: ...
    @staticmethod
    def Subtract(left: Vector2, right: Vector2) -> Vector2: ...
    def TryCopyTo(self, destination: Span_1[float]) -> bool: ...
    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        @typing.overload
        def __call__(self, array: Array_1[float]) -> None:...
        @typing.overload
        def __call__(self, destination: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, array: Array_1[float], index: int) -> None:...

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector2, divisor: float) -> Vector2:...
        @typing.overload
        def __call__(self, left: Vector2, right: Vector2) -> Vector2:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Vector2) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, left: float, right: Vector2) -> Vector2:...
        @typing.overload
        def __call__(self, left: Vector2, right: float) -> Vector2:...
        @typing.overload
        def __call__(self, left: Vector2, right: Vector2) -> Vector2:...

    # Skipped ToString due to it being static, abstract and generic.

    ToString : ToString_MethodGroup
    class ToString_MethodGroup:
        @typing.overload
        def __call__(self) -> str:...
        @typing.overload
        def __call__(self, format: str) -> str:...
        @typing.overload
        def __call__(self, format: str, formatProvider: IFormatProvider) -> str:...

    # Skipped Transform due to it being static, abstract and generic.

    Transform : Transform_MethodGroup
    class Transform_MethodGroup:
        @typing.overload
        def __call__(self, position: Vector2, matrix: Matrix3x2) -> Vector2:...
        @typing.overload
        def __call__(self, position: Vector2, matrix: Matrix4x4) -> Vector2:...
        @typing.overload
        def __call__(self, value: Vector2, rotation: Quaternion) -> Vector2:...

    # Skipped TransformNormal due to it being static, abstract and generic.

    TransformNormal : TransformNormal_MethodGroup
    class TransformNormal_MethodGroup:
        @typing.overload
        def __call__(self, normal: Vector2, matrix: Matrix3x2) -> Vector2:...
        @typing.overload
        def __call__(self, normal: Vector2, matrix: Matrix4x4) -> Vector2:...



class Vector3(IFormattable, IEquatable_1[Vector3]):
    @typing.overload
    def __init__(self, value: float) -> None: ...
    @typing.overload
    def __init__(self, value: Vector2, z: float) -> None: ...
    @typing.overload
    def __init__(self, values: ReadOnlySpan_1[float]) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float, z: float) -> None: ...
    X : float
    Y : float
    Z : float
    @classmethod
    @property
    def One(cls) -> Vector3: ...
    @classmethod
    @property
    def UnitX(cls) -> Vector3: ...
    @classmethod
    @property
    def UnitY(cls) -> Vector3: ...
    @classmethod
    @property
    def UnitZ(cls) -> Vector3: ...
    @classmethod
    @property
    def Zero(cls) -> Vector3: ...
    @staticmethod
    def Abs(value: Vector3) -> Vector3: ...
    @staticmethod
    def Add(left: Vector3, right: Vector3) -> Vector3: ...
    @staticmethod
    def Clamp(value1: Vector3, min: Vector3, max: Vector3) -> Vector3: ...
    @staticmethod
    def Cross(vector1: Vector3, vector2: Vector3) -> Vector3: ...
    @staticmethod
    def Distance(value1: Vector3, value2: Vector3) -> float: ...
    @staticmethod
    def DistanceSquared(value1: Vector3, value2: Vector3) -> float: ...
    @staticmethod
    def Dot(vector1: Vector3, vector2: Vector3) -> float: ...
    def GetHashCode(self) -> int: ...
    def Length(self) -> float: ...
    def LengthSquared(self) -> float: ...
    @staticmethod
    def Lerp(value1: Vector3, value2: Vector3, amount: float) -> Vector3: ...
    @staticmethod
    def Max(value1: Vector3, value2: Vector3) -> Vector3: ...
    @staticmethod
    def Min(value1: Vector3, value2: Vector3) -> Vector3: ...
    @staticmethod
    def Negate(value: Vector3) -> Vector3: ...
    @staticmethod
    def Normalize(value: Vector3) -> Vector3: ...
    def __add__(self, left: Vector3, right: Vector3) -> Vector3: ...
    @typing.overload
    def __truediv__(self, value1: Vector3, value2: float) -> Vector3: ...
    @typing.overload
    def __truediv__(self, left: Vector3, right: Vector3) -> Vector3: ...
    def __eq__(self, left: Vector3, right: Vector3) -> bool: ...
    def __ne__(self, left: Vector3, right: Vector3) -> bool: ...
    @typing.overload
    def __mul__(self, left: float, right: Vector3) -> Vector3: ...
    @typing.overload
    def __mul__(self, left: Vector3, right: float) -> Vector3: ...
    @typing.overload
    def __mul__(self, left: Vector3, right: Vector3) -> Vector3: ...
    def __sub__(self, left: Vector3, right: Vector3) -> Vector3: ...
    def __neg__(self, value: Vector3) -> Vector3: ...
    @staticmethod
    def Reflect(vector: Vector3, normal: Vector3) -> Vector3: ...
    @staticmethod
    def SquareRoot(value: Vector3) -> Vector3: ...
    @staticmethod
    def Subtract(left: Vector3, right: Vector3) -> Vector3: ...
    @staticmethod
    def TransformNormal(normal: Vector3, matrix: Matrix4x4) -> Vector3: ...
    def TryCopyTo(self, destination: Span_1[float]) -> bool: ...
    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        @typing.overload
        def __call__(self, array: Array_1[float]) -> None:...
        @typing.overload
        def __call__(self, destination: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, array: Array_1[float], index: int) -> None:...

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector3, divisor: float) -> Vector3:...
        @typing.overload
        def __call__(self, left: Vector3, right: Vector3) -> Vector3:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Vector3) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, left: float, right: Vector3) -> Vector3:...
        @typing.overload
        def __call__(self, left: Vector3, right: float) -> Vector3:...
        @typing.overload
        def __call__(self, left: Vector3, right: Vector3) -> Vector3:...

    # Skipped ToString due to it being static, abstract and generic.

    ToString : ToString_MethodGroup
    class ToString_MethodGroup:
        @typing.overload
        def __call__(self) -> str:...
        @typing.overload
        def __call__(self, format: str) -> str:...
        @typing.overload
        def __call__(self, format: str, formatProvider: IFormatProvider) -> str:...

    # Skipped Transform due to it being static, abstract and generic.

    Transform : Transform_MethodGroup
    class Transform_MethodGroup:
        @typing.overload
        def __call__(self, position: Vector3, matrix: Matrix4x4) -> Vector3:...
        @typing.overload
        def __call__(self, value: Vector3, rotation: Quaternion) -> Vector3:...



class Vector4(IFormattable, IEquatable_1[Vector4]):
    @typing.overload
    def __init__(self, value: float) -> None: ...
    @typing.overload
    def __init__(self, value: Vector3, w: float) -> None: ...
    @typing.overload
    def __init__(self, value: Vector2, z: float, w: float) -> None: ...
    @typing.overload
    def __init__(self, values: ReadOnlySpan_1[float]) -> None: ...
    @typing.overload
    def __init__(self, x: float, y: float, z: float, w: float) -> None: ...
    W : float
    X : float
    Y : float
    Z : float
    @classmethod
    @property
    def One(cls) -> Vector4: ...
    @classmethod
    @property
    def UnitW(cls) -> Vector4: ...
    @classmethod
    @property
    def UnitX(cls) -> Vector4: ...
    @classmethod
    @property
    def UnitY(cls) -> Vector4: ...
    @classmethod
    @property
    def UnitZ(cls) -> Vector4: ...
    @classmethod
    @property
    def Zero(cls) -> Vector4: ...
    @staticmethod
    def Abs(value: Vector4) -> Vector4: ...
    @staticmethod
    def Add(left: Vector4, right: Vector4) -> Vector4: ...
    @staticmethod
    def Clamp(value1: Vector4, min: Vector4, max: Vector4) -> Vector4: ...
    @staticmethod
    def Distance(value1: Vector4, value2: Vector4) -> float: ...
    @staticmethod
    def DistanceSquared(value1: Vector4, value2: Vector4) -> float: ...
    @staticmethod
    def Dot(vector1: Vector4, vector2: Vector4) -> float: ...
    def GetHashCode(self) -> int: ...
    def Length(self) -> float: ...
    def LengthSquared(self) -> float: ...
    @staticmethod
    def Lerp(value1: Vector4, value2: Vector4, amount: float) -> Vector4: ...
    @staticmethod
    def Max(value1: Vector4, value2: Vector4) -> Vector4: ...
    @staticmethod
    def Min(value1: Vector4, value2: Vector4) -> Vector4: ...
    @staticmethod
    def Negate(value: Vector4) -> Vector4: ...
    @staticmethod
    def Normalize(vector: Vector4) -> Vector4: ...
    def __add__(self, left: Vector4, right: Vector4) -> Vector4: ...
    @typing.overload
    def __truediv__(self, value1: Vector4, value2: float) -> Vector4: ...
    @typing.overload
    def __truediv__(self, left: Vector4, right: Vector4) -> Vector4: ...
    def __eq__(self, left: Vector4, right: Vector4) -> bool: ...
    def __ne__(self, left: Vector4, right: Vector4) -> bool: ...
    @typing.overload
    def __mul__(self, left: float, right: Vector4) -> Vector4: ...
    @typing.overload
    def __mul__(self, left: Vector4, right: float) -> Vector4: ...
    @typing.overload
    def __mul__(self, left: Vector4, right: Vector4) -> Vector4: ...
    def __sub__(self, left: Vector4, right: Vector4) -> Vector4: ...
    def __neg__(self, value: Vector4) -> Vector4: ...
    @staticmethod
    def SquareRoot(value: Vector4) -> Vector4: ...
    @staticmethod
    def Subtract(left: Vector4, right: Vector4) -> Vector4: ...
    def TryCopyTo(self, destination: Span_1[float]) -> bool: ...
    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        @typing.overload
        def __call__(self, array: Array_1[float]) -> None:...
        @typing.overload
        def __call__(self, destination: Span_1[float]) -> None:...
        @typing.overload
        def __call__(self, array: Array_1[float], index: int) -> None:...

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector4, divisor: float) -> Vector4:...
        @typing.overload
        def __call__(self, left: Vector4, right: Vector4) -> Vector4:...

    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: Vector4) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, left: float, right: Vector4) -> Vector4:...
        @typing.overload
        def __call__(self, left: Vector4, right: float) -> Vector4:...
        @typing.overload
        def __call__(self, left: Vector4, right: Vector4) -> Vector4:...

    # Skipped ToString due to it being static, abstract and generic.

    ToString : ToString_MethodGroup
    class ToString_MethodGroup:
        @typing.overload
        def __call__(self) -> str:...
        @typing.overload
        def __call__(self, format: str) -> str:...
        @typing.overload
        def __call__(self, format: str, formatProvider: IFormatProvider) -> str:...

    # Skipped Transform due to it being static, abstract and generic.

    Transform : Transform_MethodGroup
    class Transform_MethodGroup:
        @typing.overload
        def __call__(self, position: Vector2, matrix: Matrix4x4) -> Vector4:...
        @typing.overload
        def __call__(self, position: Vector3, matrix: Matrix4x4) -> Vector4:...
        @typing.overload
        def __call__(self, value: Vector2, rotation: Quaternion) -> Vector4:...
        @typing.overload
        def __call__(self, value: Vector3, rotation: Quaternion) -> Vector4:...
        @typing.overload
        def __call__(self, value: Vector4, rotation: Quaternion) -> Vector4:...
        @typing.overload
        def __call__(self, vector: Vector4, matrix: Matrix4x4) -> Vector4:...


