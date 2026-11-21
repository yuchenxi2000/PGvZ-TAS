"""
修改器内置服务端
访问地址http://localhost:58080
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

# ========== 内置HTTP服务器 ==========
# 提供一个本地HTTP服务，使PC/手机浏览器可以访问修改器GUI
# 浏览器打开 http://localhost:58080 即可使用
import http.server
import socketserver
import os
import threading
import time
import urllib.parse

_GUI_PORT = 58080
_bootstrap_done = threading.Event()
_bootstrap_error = None


def bootstrap_status():
    if _bootstrap_done.is_set():
        return True, _bootstrap_error
    return False, None


def _load_mod():
    global _bootstrap_error
    try:
        import Sexy
        while True:
            app = Sexy.GlobalStaticVars.gSexyAppBase
            # StartLoadingThread 在场地尺寸常量完成初始化后才置位。
            if app is not None and app.mLoadingThreadStarted:
                break
            time.sleep(0.1)
        import pgvztool  # 导入包会加载 pgvz 并安装 Hook。
    except Exception:
        import traceback
        _bootstrap_error = traceback.format_exc()
    finally:
        _bootstrap_done.set()


class _GUIHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        root = os.path.abspath(os.path.join(modsDirPath, 'gui'))
        decoded = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        relative = decoded.replace('\\', '/').lstrip('/')
        candidate = os.path.abspath(os.path.join(root, relative))
        normalized_root = os.path.normcase(root)
        normalized_path = os.path.normcase(candidate)
        if normalized_path != normalized_root and not normalized_path.startswith(normalized_root + os.sep):
            raise PermissionError('path is outside the GUI directory')
        return candidate

    def send_head(self):
        try:
            return super().send_head()
        except (PermissionError, ValueError):
            self.send_error(403, 'Forbidden')
            return None

    def end_headers(self):
        # 防止之后的页面加载复用缓存；已在运行的旧页面仍需由会话校验拦截。
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        pass

class _ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

threading.Thread(target=_load_mod, daemon=True).start()
_server = _ThreadingServer(('127.0.0.1', _GUI_PORT), _GUIHandler)
threading.Thread(target=_server.serve_forever, daemon=True).start()
