# 必须使用全局对象包装。如果直接用全局变量存对象，不同模块的更改互不影响，会导致出错或者访问到None
class GlobalVar:
    def __init__(self) -> None:
        self.timePassed: bool = False
        # 如果想保留其他框架的行为，在时间点已过去时仍执行操作，需要将下面这个变量设置为True
        self.doPassedOp: bool = False
    
    @property
    def opCanceled(self):
        return self.timePassed and not self.doPassedOp

gvar = GlobalVar()
