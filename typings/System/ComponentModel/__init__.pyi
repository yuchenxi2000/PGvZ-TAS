import typing
from System import Attribute

class DefaultValueAttribute(Attribute):
    # Constructor .ctor(value : Int16) was skipped since it collides with above method
    # Constructor .ctor(value : Int32) was skipped since it collides with above method
    # Constructor .ctor(value : Int64) was skipped since it collides with above method
    # Constructor .ctor(value : Single) was skipped since it collides with above method
    # Constructor .ctor(value : Double) was skipped since it collides with above method
    # Constructor .ctor(value : Boolean) was skipped since it collides with above method
    # Constructor .ctor(value : String) was skipped since it collides with above method
    # Constructor .ctor(value : SByte) was skipped since it collides with above method
    # Constructor .ctor(value : UInt16) was skipped since it collides with above method
    # Constructor .ctor(value : UInt32) was skipped since it collides with above method
    # Constructor .ctor(value : UInt64) was skipped since it collides with above method
    @typing.overload
    def __init__(self, type: typing.Type[typing.Any], value: str) -> None: ...
    @typing.overload
    def __init__(self, value: str) -> None: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, value: typing.Any) -> None: ...
    @property
    def TypeId(self) -> typing.Any: ...
    @property
    def Value(self) -> typing.Any: ...
    def Equals(self, obj: typing.Any) -> bool: ...
    def GetHashCode(self) -> int: ...


class EditorBrowsableAttribute(Attribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, state: EditorBrowsableState) -> None: ...
    @property
    def State(self) -> EditorBrowsableState: ...
    @property
    def TypeId(self) -> typing.Any: ...
    def Equals(self, obj: typing.Any) -> bool: ...
    def GetHashCode(self) -> int: ...


class EditorBrowsableState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Always : EditorBrowsableState # 0
    Never : EditorBrowsableState # 1
    Advanced : EditorBrowsableState # 2


class INotifyPropertyChanged(typing.Protocol):
    pass

