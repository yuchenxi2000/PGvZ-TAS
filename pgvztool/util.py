"""
主线程运行装饰器，供 cheat.py 和 placer.py 共用
"""
from pgvz import script_manager, ScriptRunMode
from functools import wraps

def main_thread(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def _ScriptFunc():
            func(*args, **kwargs)
            yield
        script_manager.Register(_ScriptFunc, runmode=ScriptRunMode.GLOBAL)
    return wrapper
