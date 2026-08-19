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
import urllib.parse

_GUI_PORT = 58080

class _GUIHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = urllib.parse.unquote(path.split('?', 1)[0]).lstrip('/')
        gui_dir = os.path.join(modsDirPath, 'gui')
        result = os.path.join(gui_dir, path) if path else gui_dir
        return result

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

_server = _ThreadingServer(('127.0.0.1', _GUI_PORT), _GUIHandler)
threading.Thread(target=_server.serve_forever, daemon=True).start()
