import Lawn

# 必须使用全局对象包装。如果直接用全局变量存LawnApp或其他对象，不同模块的更改互不影响，会导致访问到None
class GlobalVar:
    def __init__(self) -> None:
        # 下面两条注释是临时把pylance的类型检查关掉，这样不会有红色警告，同时保留其他代码的类型检查
        self.glawnapp: Lawn.LawnApp = None  # type: ignore
        self.gboard: Lawn.Board = None  # type: ignore

    def Set(self, lawnapp: Lawn.LawnApp):
        self.glawnapp = lawnapp
        self.gboard = lawnapp.mBoard

gvar = GlobalVar()
