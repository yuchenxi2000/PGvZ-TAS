# 必须使用全局对象包装。如果直接用全局变量存对象，不同模块的更改互不影响，会导致出错或者访问到None
class GlobalVar:
    def __init__(self) -> None:
        self.opCanceled: bool = False

gvar = GlobalVar()
