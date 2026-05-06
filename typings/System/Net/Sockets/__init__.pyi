import typing

class AddressFamily(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unspecified : AddressFamily # 0
    Unix : AddressFamily # 1
    InterNetwork : AddressFamily # 2
    ImpLink : AddressFamily # 3
    Pup : AddressFamily # 4
    Chaos : AddressFamily # 5
    NS : AddressFamily # 6
    Ipx : AddressFamily # 6
    Osi : AddressFamily # 7
    Iso : AddressFamily # 7
    Ecma : AddressFamily # 8
    DataKit : AddressFamily # 9
    Ccitt : AddressFamily # 10
    Sna : AddressFamily # 11
    DecNet : AddressFamily # 12
    DataLink : AddressFamily # 13
    Lat : AddressFamily # 14
    HyperChannel : AddressFamily # 15
    AppleTalk : AddressFamily # 16
    NetBios : AddressFamily # 17
    VoiceView : AddressFamily # 18
    FireFox : AddressFamily # 19
    Banyan : AddressFamily # 21
    Atm : AddressFamily # 22
    InterNetworkV6 : AddressFamily # 23
    Cluster : AddressFamily # 24
    Ieee12844 : AddressFamily # 25
    Irda : AddressFamily # 26
    NetworkDesigners : AddressFamily # 28
    Max : AddressFamily # 29
    Packet : AddressFamily # 65536
    ControllerAreaNetwork : AddressFamily # 65537
    Unknown : AddressFamily # -1

