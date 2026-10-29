import ast
import http.client
import http.server
import os
import pathlib
import tempfile
import threading
import unittest
import urllib.parse
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]


def handler_from_entry(filename, mods):
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

    def test_both_entries_reject_escaped_paths_and_serve_gui_files(self):
        for filename in ('cheat-gui.py', 'debug/cheat-gui.py'):
            with self.subTest(filename=filename):
                handler = handler_from_entry(filename, self.mods)
                server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), handler)
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
            outside = str(self.mods / 'secret.txt')
            # Model a user-created link; translation keeps the path under gui without resolving its target.
            with patch.object(os.path, 'realpath', return_value=outside):
                self.assertEqual(handler.translate_path('/linked/secret.txt'),
                                 str(self.mods / 'gui' / 'linked' / 'secret.txt'))


if __name__ == '__main__':
    unittest.main()
