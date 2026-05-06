import typing

class ConsoleStreamType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Input : ConsoleStreamType # 0
    Output : ConsoleStreamType # 1
    ErrorOutput : ConsoleStreamType # 2

