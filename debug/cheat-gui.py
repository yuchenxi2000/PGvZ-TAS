"""
PGvZTool 调试入口。

仅用于排查正式 cheat-gui.py 未能打开网页的问题。使用时将本文件复制到游戏
mods 目录并覆盖正式 cheat-gui.py；排查完成后必须恢复正式入口。
"""
import sys
import System
import System.IO
import System.Reflection
import Sexy


_GUI_PORT = 58080
_game = Sexy.Main.GamerServicesComp.Game


def _get_websocket_port():
    """读取 IronPyInteractive 已选定、将在模组加载完成后监听的端口。"""
    binding_flags = System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static  # type: ignore
    ironpy_type = _game.GetType().Assembly.GetType('LawnMod.IronPyInteractive')  # type: ignore
    if ironpy_type is None:
        raise RuntimeError('LawnMod.IronPyInteractive type was not found')
    server_field = ironpy_type.GetField('mWS', binding_flags)
    if server_field is None:
        raise RuntimeError('IronPyInteractive.mWS field was not found')
    websocket_server = server_field.GetValue(None)
    if websocket_server is None:
        raise RuntimeError('IronPyInteractive.mWS has not been created')
    return int(websocket_server.Port)


try:
    _websocket_port = _get_websocket_port()
    _websocket_status = 'WebSocket 端口: {}'.format(_websocket_port)
except Exception as error:
    _websocket_status = 'WebSocket: 读取失败（{}）'.format(error)


# Android: IronPython 库位于 CurrentDirectory/IronPython/Libs。
pyLibPath = System.IO.Path.Combine(
    System.Environment.CurrentDirectory,
    'IronPython',
    'Libs',
)
if not System.IO.Directory.Exists(pyLibPath):
    # Windows: IronPython 库位于游戏主程序同目录下的 lib。
    pyLibPath = System.IO.Path.Combine(
        System.IO.Path.GetDirectoryName(System.Environment.ProcessPath),
        'lib',
    )
modsDirPath = System.IO.Path.Combine(
    System.Environment.CurrentDirectory,
    'mods',
)
sys.path.append(pyLibPath)
sys.path.append(modsDirPath)


def _join_mod_path(relative_path):
    result = modsDirPath
    for part in relative_path.split('/'):
        result = System.IO.Path.Combine(result, part)
    return result


def _component_status(name, directory, required_files):
    if not System.IO.Directory.Exists(_join_mod_path(directory)):
        return '{}: 目录缺失'.format(name)
    missing = [
        path for path in required_files
        if not System.IO.File.Exists(_join_mod_path(path))
    ]
    if missing:
        prefix_length = len(directory) + 1
        missing_names = [path[prefix_length:] for path in missing]
        return '{}: 缺 {}'.format(name, ', '.join(missing_names))
    return None


_pgvz_files = (
    'pgvz/__init__.py',
    'pgvz/card.py',
    'pgvz/cob_manager.py',
    'pgvz/global_var.py',
    'pgvz/lineup.py',
    'pgvz/rng.py',
    'pgvz/script.py',
    'pgvz/set_zb.py',
    'pgvz/smart.py',
    'pgvz/speed.py',
    'pgvz/time_operation.py',
    'pgvz/util.py',
    'pgvz/version.py',
)
_pgvztool_files = (
    'pgvztool/__init__.py',
    'pgvztool/cheat.py',
    'pgvztool/hook.py',
    'pgvztool/keybinds.py',
    'pgvztool/placer.py',
    'pgvztool/sync.py',
    'pgvztool/tas.py',
    'pgvztool/util.py',
)
_gui_files = [
    'gui/index.html',
    'gui/styles.css',
    'gui/js/app.js',
    'gui/js/data.js',
    'gui/js/i18n.js',
    'gui/js/protocol.js',
]
_gui_index_path = _join_mod_path('gui/index.html')
if System.IO.File.Exists(_gui_index_path):
    try:
        _gui_index = System.IO.File.ReadAllText(_gui_index_path)
        for _vendor_file in (
            'gui/vendor/vue/vue.global.prod.js',
            'gui/vendor/element-plus/index.full.min.js',
            'gui/vendor/element-plus/index.min.css',
        ):
            _reference = './' + _vendor_file[len('gui/'):]
            if _reference in _gui_index:
                _gui_files.append(_vendor_file)
    except Exception as error:
        _gui_file_status = 'gui: index.html 读取失败（{}）'.format(error)
    else:
        _gui_file_status = _component_status('gui', 'gui', _gui_files)
else:
    _gui_file_status = _component_status('gui', 'gui', _gui_files)

_file_errors = [status for status in (
    _component_status('pgvz', 'pgvz', _pgvz_files),
    _component_status('pgvztool', 'pgvztool', _pgvztool_files),
    _gui_file_status,
) if status is not None]
_file_status = (
    '文件检查：\n' + '\n'.join(_file_errors)
    if _file_errors else
    '文件检查：OK'
)


try:
    import http.server
    import os
    import socketserver
    import threading
    import urllib.parse

    class _GUIHandler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self, path):
            path = urllib.parse.unquote(path.split('?', 1)[0]).lstrip('/')
            gui_dir = os.path.join(modsDirPath, 'gui')
            return os.path.join(gui_dir, path) if path else gui_dir

        def end_headers(self):
            self.send_header(
                'Cache-Control',
                'no-store, no-cache, must-revalidate, max-age=0',
            )
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()

        def log_message(self, format, *args):
            pass

    class _ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        daemon_threads = True

    _server = _ThreadingServer(('127.0.0.1', _GUI_PORT), _GUIHandler)
    threading.Thread(target=_server.serve_forever, daemon=True).start()
    _http_status = 'HTTP {}: OK'.format(_server.server_port)
except Exception as error:
    _http_status = 'HTTP {}: 失败（{}）'.format(_GUI_PORT, error)


_message = (
    '{}\n'
    '{}\n'
    '{}\n\n'
    '仅供故障排查；游玩前请恢复正式 cheat-gui.py。'
).format(_http_status, _websocket_status, _file_status)

Sexy.Debug.Log('[PGvZTool debug loader]\n' + _message)
_game.ShowMessageBox(0, 'PGvZTool 调试入口 / Debug', _message)  # type: ignore
