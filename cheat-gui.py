"""
修改器内置服务端
从 58080 开始尝试绑定，主界面「修改器」打开实际监听地址。
"""
import sys
import System
import System.IO
# 貌似手机版不需要设置路径也能正常运行，但这里还是加上以防万一
# Android: IronPython库在 CurrentDirectory/IronPython/Libs
pyLibPath = System.IO.Path.Combine(System.Environment.CurrentDirectory, 'IronPython', 'Libs')
if not System.IO.Directory.Exists(pyLibPath):
    # Windows: IronPython库在游戏主程序同目录下的lib
    pyLibPath = System.IO.Path.Combine(System.IO.Path.GetDirectoryName(System.Environment.ProcessPath), 'lib')
modsDirPath = System.IO.Path.Combine(System.Environment.CurrentDirectory, 'mods')
sys.path.append(pyLibPath)
sys.path.append(modsDirPath)

import threading
from types import ModuleType


def _serve_gui():
    try:
        # 按文件加载 HTTP 服务，游戏常量就绪前不执行 pgvztool/__init__.py。
        path = System.IO.Path.Combine(modsDirPath, 'pgvztool', 'gui_http.py')
        module = ModuleType('_pgvz_gui_http')
        with open(path, 'rb') as source:
            exec(compile(source.read(), path, 'exec'), module.__dict__)
        sys.modules[module.__name__] = module
        server = module.create_server(modsDirPath, 58080, System.Guid.NewGuid().ToString('N'))
        try:
            server.serve_forever()
        finally:
            server.server_close()
    except Exception:
        import traceback
        import Sexy
        Sexy.Debug.Log(Sexy.DebugType.Error, '[PGvZTool] GUI HTTP server failed:\n' + traceback.format_exc())


threading.Thread(target=_serve_gui, daemon=True).start()
