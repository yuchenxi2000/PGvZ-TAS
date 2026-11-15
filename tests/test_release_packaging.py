"""Exercise stable/nightly archives without network access or game imports."""

import contextlib
import importlib.util
import io
import runpy
import tempfile
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("release_builder", ROOT / "tools/build-release.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class ReleasePackagingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        for name in builder.REQUIRED_FILES:
            (self.repo / name).write_text(name, encoding="utf-8")
        for name in builder.REQUIRED_DIRS:
            (self.repo / name).mkdir()
        self.version_path = self.repo / "pgvz/version.py"
        self.version_path.write_text(
            'MOD_VERSION = "1.16.1"\nSUPPORTED_GAME_VERSIONS = ("1.4.3",)\n'
            'PROJECT_VERSION = MOD_VERSION\nTOOL_VERSION = MOD_VERSION\n',
            encoding="utf-8",
        )
        self.original_version = self.version_path.read_bytes()
        self.changelog = self.repo / "CHANGELOG.md"
        self.changelog.write_text("## [unreleased]\n", encoding="utf-8")
        gui = self.repo / "gui"
        (gui / "js").mkdir(parents=True)
        (gui / "index.html").write_bytes((ROOT / "gui/index.html").read_bytes())
        (gui / "styles.css").write_text("body {}", encoding="utf-8")
        (gui / "js/app.js").write_text("// fixture", encoding="utf-8")
        (self.repo / "pgvz/__pycache__").mkdir()
        (self.repo / "pgvz/__pycache__/version.pyc").write_bytes(b"ignore")
        self.output = self.root / "dist"
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(builder, "REPO_ROOT", self.repo).start()
        clock = mock.patch.object(builder, "datetime").start()
        clock.now.return_value = datetime(2026, 11, 15, 18, 31, 6, tzinfo=timezone.utc)
        self.download = mock.patch.object(builder, "download_file", self.fake_download).start()

    @staticmethod
    def fake_download(url, destination):
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("// bundled " + url, encoding="utf-8")

    def build(self, *arguments):
        args = builder.parse_args(["--output-root", str(self.output), *arguments])
        with contextlib.redirect_stdout(io.StringIO()):
            return builder.build_release(args)

    def assert_source_unchanged(self):
        self.assertEqual(self.version_path.read_bytes(), self.original_version)
        self.assertEqual(self.changelog.read_text(encoding="utf-8"), "## [unreleased]\n")

    def test_nightly_version_matches_filename_readme_and_runtime(self):
        archive = self.build("--nightly")
        version = "1.16.1-nightly.20261115T183106Z"
        self.assertEqual(archive.name, "PGvZTool_v{}_for_PGvZ_v1.4.3.zip".format(version))
        stage = archive.with_suffix("")
        runtime = runpy.run_path(str(stage / "pgvz/version.py"))
        for name in ("MOD_VERSION", "PROJECT_VERSION", "TOOL_VERSION"):
            self.assertEqual(runtime[name], version)
        with zipfile.ZipFile(archive) as package:
            self.assertIsNone(package.testzip())
            self.assertIn(version, package.read(builder.README_NAME).decode("utf-8"))
            self.assertIn(version, package.read("pgvz/version.py").decode("utf-8"))
            html = package.read("gui/index.html").decode("utf-8")
            self.assertNotIn("https://cdn.jsdelivr.net/", html)
            self.assertIn("gui/vendor/vue/vue.global.prod.js", package.namelist())
            self.assertFalse(any("__pycache__" in name for name in package.namelist()))
        self.assert_source_unchanged()

    def test_default_build_keeps_stable_name_and_rebuild_behavior(self):
        archive = self.build()
        self.assertEqual(archive.name, "PGvZTool_v1.16.1_for_PGvZ_v1.4.3.zip")
        stage = archive.with_suffix("")
        (stage / "stale.txt").write_text("stale", encoding="utf-8")
        self.assertEqual(self.build(), archive)
        self.assertFalse((stage / "stale.txt").exists())
        with zipfile.ZipFile(archive) as package:
            self.assertEqual(package.read("pgvz/version.py"), self.original_version)
        self.assert_source_unchanged()

    def test_version_override_is_applied_inside_both_package_modes(self):
        for mode in ([], ["--nightly"]):
            with self.subTest(mode=mode):
                archive = self.build("--mod-version", "1.17.0", *mode)
                expected = "1.17.0" + ("-nightly.20261115T183106Z" if mode else "")
                runtime = runpy.run_path(str(archive.with_suffix("") / "pgvz/version.py"))
                self.assertEqual(runtime["MOD_VERSION"], expected)
                self.assert_source_unchanged()

    def test_nightly_collision_preserves_existing_directory_or_zip(self):
        name = "PGvZTool_v1.16.1-nightly.20261115T183106Z_for_PGvZ_v1.4.3"
        for kind in ("directory", "zip"):
            with self.subTest(kind=kind):
                self.output = self.root / kind
                self.output.mkdir()
                target = self.output / (name + (".zip" if kind == "zip" else ""))
                sentinel = target
                if kind == "directory":
                    target.mkdir()
                    sentinel = target / "sentinel.txt"
                sentinel.write_bytes(b"keep existing package")
                with mock.patch.object(builder, "download_file") as download:
                    with self.assertRaises(FileExistsError):
                        self.build("--nightly")
                    download.assert_not_called()
                self.assertEqual(sentinel.read_bytes(), b"keep existing package")
                self.assert_source_unchanged()

    def test_nightly_zip_creation_also_refuses_late_collision(self):
        stage = self.root / "stage"
        stage.mkdir()
        archive = self.root / "existing.zip"
        archive.write_bytes(b"keep existing zip")
        with self.assertRaises(FileExistsError):
            builder.create_zip(stage, archive, overwrite=False)
        self.assertEqual(archive.read_bytes(), b"keep existing zip")

    def test_nightly_rejects_invalid_or_already_suffixed_base(self):
        for version in ("1.2", "01.2.3", "1.2.3-nightly.20261115", "1.2.3+sha", "1.2.3٤"):
            with self.subTest(version=version):
                with self.assertRaisesRegex(ValueError, "MAJOR.MINOR.PATCH"):
                    self.build("--nightly", "--mod-version", version)
        self.assertFalse(self.output.exists())
        self.assert_source_unchanged()


if __name__ == "__main__":
    unittest.main()
