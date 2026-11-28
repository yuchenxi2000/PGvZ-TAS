"""Serve the GUI before importing the game-dependent pgvztool package."""
import http.server
import json
import os
import socketserver
import threading
import urllib.parse


bound_port = None


class GuiRuntime:
    def __init__(self, mods_dir, instance):
        self.mods_dir = mods_dir
        self.instance = instance
        self._lock = threading.Lock()
        self._started = False
        self._done = threading.Event()
        self._dispatcher = None
        self._error = None
        self._version = ''
        self._metadata = {}

        path = os.path.join(mods_dir, 'pgvz', 'version.py')
        try:
            with open(path, 'rb') as source:
                exec(compile(source.read(), path, 'exec'), self._metadata)
        except (OSError, ValueError, SyntaxError):
            pass

    def start(self):
        with self._lock:
            if self._started:
                return
            self._started = True
            threading.Thread(target=self._load_mod, daemon=True).start()

    def _load_mod(self):
        try:
            import time
            import Sexy
            while True:
                app = Sexy.GlobalStaticVars.gSexyAppBase
                # 场地尺寸常量在 StartLoadingThread 置位之前完成初始化。
                if app is not None and app.mLoadingThreadStarted:
                    break
                time.sleep(0.1)

            import Lawn
            parts = Lawn.LawnApp.AppVersionNumber.split()
            self._version = parts[1] if len(parts) > 1 else ''
            from pgvztool import gui_dispatcher
            self._dispatcher = gui_dispatcher
        except Exception:
            import traceback
            self._error = traceback.format_exc()
        finally:
            self._done.set()

    @property
    def dispatcher(self):
        return self._dispatcher if self._done.is_set() else None

    def status(self):
        self.start()
        ready = self._done.is_set()
        return {
            'instance': self.instance,
            'ready': ready,
            'error': self._error if ready else None,
            'version': self._version if ready else '',
            'modVersion': self._metadata.get('MOD_VERSION', ''),
            'supportedVersions': self._metadata.get('SUPPORTED_GAME_VERSIONS', ()),
        }


class _GUIHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        root = os.path.abspath(os.path.join(self.server.runtime.mods_dir, 'gui'))
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
        # 避免重新打开页面时使用上一次安装的静态文件。
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, format, *args):
        pass

    def _json(self, status, value):
        body = (value if isinstance(value, str) else json.dumps(value)).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _api_origin_allowed(self):
        host = self.headers.get('Host', '').lower()
        port = self.server.server_port
        origin = self.headers.get('Origin')
        return (host in ('127.0.0.1:{}'.format(port), 'localhost:{}'.format(port))
                and (origin is None or origin == 'http://' + host))

    def do_GET(self):
        if self.path != '/api/status':
            return super().do_GET()
        if not self._api_origin_allowed():
            return self._json(403, {'error': 'Invalid GUI origin'})
        self._json(200, self.server.runtime.status())

    def do_POST(self):
        if self.path not in ('/api/request', '/api/poll'):
            return self._json(404, {'error': 'Unknown GUI endpoint'})
        if not self._api_origin_allowed():
            return self._json(403, {'error': 'Invalid GUI origin'})
        runtime = self.server.runtime
        if self.headers.get('X-PGvZ-Instance') != runtime.instance:
            return self._json(409, {'error': 'The game instance changed'})
        dispatcher = runtime.dispatcher
        if dispatcher is None:
            return self._json(503, {'error': 'The mod is not ready'})
        if self.headers.get_content_type() != 'application/json':
            return self._json(415, {'error': 'Expected a JSON request'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 1024 * 1024:
                raise ValueError('Invalid GUI request size')
            body = self.rfile.read(length).decode('utf-8')
            if self.path == '/api/request':
                result = dispatcher.submit(body, close_on_release=True)
            else:
                payload = json.loads(body)
                if not isinstance(payload, dict):
                    raise TypeError('GUI poll must be an object')
                client_id = payload.get('_clientId')
                revision = payload.get('revision', 0)
                if type(revision) is not int or revision < 0:
                    raise ValueError('Invalid GUI state revision')
                if 'acknowledged' in payload:
                    dispatcher.acknowledge(client_id, json.dumps(payload['acknowledged']))
                if 'cancelled' in payload:
                    dispatcher.cancel(client_id, json.dumps(payload['cancelled']))
                result = dispatcher.poll(client_id, revision=revision)
        except (TypeError, ValueError) as error:
            return self._json(400, {'error': str(error)})
        self._json(200, result)


class _ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    # 每个端口只服务一个游戏进程。
    allow_reuse_address = os.name != 'nt'
    allow_reuse_port = False

    def __init__(self, port, runtime):
        self.runtime = runtime
        super().__init__(('127.0.0.1', port), _GUIHandler)


def create_server(mods_dir, port, instance, *, load_on_request=False):
    global bound_port
    runtime = GuiRuntime(mods_dir, instance)
    ports = range(port, port + 10)
    try:
        for candidate in ports:
            try:
                server = _ThreadingServer(candidate, runtime)
            except OSError:
                if candidate == ports[-1]:
                    raise
            else:
                bound_port = server.server_port
                return server
    finally:
        # 正式入口即使无法监听，仍加载游戏内功能。绑定成功时先公布端口。
        if not load_on_request:
            runtime.start()
