import ast
import http.client
import http.server
import json
import os
import pathlib
import runpy
import sys
import tempfile
import threading
import types
import unittest
import urllib.parse
from unittest.mock import Mock, mock_open, patch

ROOT = pathlib.Path(__file__).resolve().parents[1]


def handler_from_entry(filename, mods):
    if filename == 'cheat-gui.py':
        return runpy.run_path(str(ROOT / 'pgvztool/gui_http.py'))['_GUIHandler']
    tree = ast.parse((ROOT / filename).read_text(encoding='utf-8-sig'))
    cls = next(node for node in ast.walk(tree) if isinstance(node, ast.ClassDef) and node.name == '_GUIHandler')
    namespace = {'http': http, 'urllib': urllib, 'os': os, 'modsDirPath': str(mods)}
    exec(compile(ast.Module(body=[cls], type_ignores=[]), filename, 'exec'), namespace)
    return namespace['_GUIHandler']


class GuiHttpPathTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.mods = pathlib.Path(self.directory.name)
        (self.mods / 'gui').mkdir()
        (self.mods / 'gui' / 'index.html').write_text('GUI index', encoding='utf-8')
        (self.mods / 'gui' / 'styles.css').write_text('GUI style', encoding='utf-8')
        (self.mods / 'secret.txt').write_text('PRIVATE OUTSIDE FILE', encoding='utf-8')
        (self.mods / 'gui-other').mkdir()
        (self.mods / 'gui-other' / 'secret.txt').write_text('PRIVATE OUTSIDE FILE', encoding='utf-8')

    def test_formal_entry_defers_loading_and_serving_http_to_its_worker(self):
        filename = ROOT / 'cheat-gui.py'
        code = compile(filename.read_bytes(), str(filename), 'exec')
        io = types.ModuleType('System.IO')
        io.Path = types.SimpleNamespace(Combine=os.path.join)
        io.Directory = types.SimpleNamespace(Exists=lambda _: True)
        system = types.ModuleType('System')
        system.IO = io
        system.Environment = types.SimpleNamespace(CurrentDirectory=str(self.mods))
        system.Guid = types.SimpleNamespace(NewGuid=lambda: types.SimpleNamespace(ToString=lambda _: 'instance'))
        server = Mock()
        probe = types.SimpleNamespace(create_server=Mock(return_value=server))
        source = mock_open(read_data=b'from gui_startup_probe import create_server\n')
        modules = {'System': system, 'System.IO': io, 'gui_startup_probe': probe}

        with patch.dict(sys.modules, modules), patch.object(sys, 'path', list(sys.path)):
            with patch.object(threading, 'Thread') as thread, patch('builtins.open', source):
                exec(code, {})
                source.assert_not_called()
                probe.create_server.assert_not_called()
                thread.return_value.start.assert_called_once()
                self.assertTrue(thread.call_args.kwargs['daemon'])

                thread.call_args.kwargs['target']()
                mods_dir = str(self.mods / 'mods')
                source.assert_called_once_with(os.path.join(mods_dir, 'pgvztool', 'gui_http.py'), 'rb')
                probe.create_server.assert_called_once_with(mods_dir, 58080, 'instance')
                server.serve_forever.assert_called_once_with()
                server.server_close.assert_called_once_with()

    def test_both_entries_reject_escaped_paths_and_serve_gui_files(self):
        for filename in ('cheat-gui.py', 'debug/cheat-gui.py'):
            with self.subTest(filename=filename):
                handler = handler_from_entry(filename, self.mods)
                server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
                server.runtime = types.SimpleNamespace(mods_dir=str(self.mods))
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    for url in ('/../secret.txt', '/%2e%2e/secret.txt', '/..%5csecret.txt',
                                '/../gui-other/secret.txt'):
                        connection = http.client.HTTPConnection('127.0.0.1', server.server_port)
                        connection.request('GET', url)
                        response = connection.getresponse()
                        self.assertEqual(response.status, 403, url)
                        self.assertNotIn(b'PRIVATE OUTSIDE FILE', response.read())
                        connection.close()
                    for url, expected in (('/', b'GUI index'), ('/styles.css?v=1#fragment', b'GUI style'),
                                          ('/js/../styles.css', b'GUI style')):
                        connection = http.client.HTTPConnection('127.0.0.1', server.server_port)
                        connection.request('GET', url)
                        response = connection.getresponse()
                        self.assertEqual(response.status, 200)
                        self.assertEqual(response.read(), expected)
                        connection.close()
                finally:
                    server.shutdown()
                    server.server_close()
                    thread.join()

    def test_link_targets_are_not_resolved_for_directory_check(self):
        for filename in ('cheat-gui.py', 'debug/cheat-gui.py'):
            cls = handler_from_entry(filename, self.mods)
            handler = cls.__new__(cls)
            handler.server = types.SimpleNamespace(runtime=types.SimpleNamespace(mods_dir=str(self.mods)))
            outside = str(self.mods / 'secret.txt')
            # Model a user-created link; translation keeps the path under gui without resolving its target.
            with patch.object(os.path, 'realpath', return_value=outside):
                self.assertEqual(handler.translate_path('/linked/secret.txt'),
                                 str(self.mods / 'gui' / 'linked' / 'secret.txt'))

    def test_status_submit_and_poll_share_the_static_file_listener(self):
        namespace = runpy.run_path(str(ROOT / 'pgvztool/gui_http.py'))
        calls = []

        def submit(body, *, close_on_release):
            calls.append(('submit', json.loads(body), close_on_release))
            return '{"action":"queued","id":"one"}'

        def poll(client_id, *, revision):
            calls.append(('poll', client_id, revision))
            return '{"results":[],"updates":[]}'

        runtime = types.SimpleNamespace(
            mods_dir=str(self.mods), instance='current-game',
            status=lambda: {'ready': True, 'instance': 'current-game'},
            dispatcher=types.SimpleNamespace(submit=submit, poll=poll),
        )
        server = namespace['_ThreadingServer'](0, runtime)
        self.addCleanup(server.server_close)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(server.shutdown)
        origin = 'http://127.0.0.1:{}'.format(server.server_port)
        headers = {'Origin': origin, 'X-PGvZ-Instance': 'current-game', 'Content-Type': 'application/json'}

        def request(method, path, body=None, request_headers=None):
            conn = http.client.HTTPConnection('127.0.0.1', server.server_port, timeout=5)
            try:
                conn.request(method, path, body, request_headers or {})
                response = conn.getresponse()
                return response.status, response.read()
            finally:
                conn.close()

        self.assertEqual(request('GET', '/'), (200, b'GUI index'))
        status, body = request('GET', '/api/status')
        self.assertEqual((status, json.loads(body)['instance']), (200, 'current-game'))
        payload = '{"_clientId":"page","kind":"action","id":"one","name":"winLevel"}'
        self.assertEqual(request('POST', '/api/request', payload, dict(headers, Origin='https://example.org'))[0], 403)
        self.assertEqual(request('GET', '/api/status', request_headers={'Host': 'example.org'})[0], 403)
        self.assertEqual(request('POST', '/api/request', payload, {**headers, 'X-PGvZ-Instance': 'old'})[0], 409)
        self.assertEqual(calls, [])
        status, body = request('POST', '/api/request', payload, headers)
        self.assertEqual((status, json.loads(body)), (200, {'action': 'queued', 'id': 'one'}))
        status, body = request('POST', '/api/poll', '{"_clientId":"page","revision":3}', headers)
        self.assertEqual((status, json.loads(body)), (200, {'results': [], 'updates': []}))
        self.assertEqual(calls, [('submit', json.loads(payload), True), ('poll', 'page', 3)])

    def test_startup_status_preserves_version_metadata_when_dispatcher_import_fails(self):
        metadata = self.mods / 'pgvz' / 'version.py'
        metadata.parent.mkdir()
        metadata.write_text("MOD_VERSION = '1.18.1'\nSUPPORTED_GAME_VERSIONS = ('1.4.3',)\n", encoding='utf-8')
        namespace = runpy.run_path(str(ROOT / 'pgvztool/gui_http.py'))
        runtime = namespace['GuiRuntime'](str(self.mods), 'current-game')
        sexy = types.ModuleType('Sexy')
        sexy.GlobalStaticVars = types.SimpleNamespace(
            gSexyAppBase=types.SimpleNamespace(mLoadingThreadStarted=True),
        )
        lawn = types.ModuleType('Lawn')
        lawn.LawnApp = types.SimpleNamespace(AppVersionNumber='PGvZ 1.4.3')
        broken_mod = types.ModuleType('pgvztool')
        with patch.dict(sys.modules, {'Sexy': sexy, 'Lawn': lawn, 'pgvztool': broken_mod}):
            runtime.status()
            self.assertTrue(runtime._done.wait(2))
            status = runtime.status()
        self.assertTrue(status['ready'])
        self.assertIsNone(runtime.dispatcher)
        self.assertIn('Traceback', status['error'])
        self.assertIn('gui_dispatcher', status['error'])
        self.assertEqual((status['version'], status['modVersion'], status['supportedVersions']),
                         ('1.4.3', '1.18.1', ('1.4.3',)))


if __name__ == '__main__':
    unittest.main()
