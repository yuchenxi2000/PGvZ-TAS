#!/usr/bin/env python3
"""Build an offline PGvZTool release package using only the standard library."""

import argparse
import ast
import re
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "dist"
README_NAME = "使用方法README.txt"

REQUIRED_FILES = (
    "cheat-gui.py",
    "cp-cheat-mods.bat",
    "LICENSE",
)
REQUIRED_DIRS = (
    "pgvz",
    "pgvztool",
)

VUE_URL_PATTERN = re.compile(
    r"https://cdn\.jsdelivr\.net/npm/vue@(?P<version>\d+\.\d+\.\d+)"
    r"/dist/vue\.global\.min\.js"
)
ELEMENT_PLUS_JS_URL_PATTERN = re.compile(
    r"https://cdn\.jsdelivr\.net/npm/element-plus@(?P<version>\d+\.\d+\.\d+)"
    r"/dist/index\.full\.min\.js"
)
ELEMENT_PLUS_CSS_URL_PATTERN = re.compile(
    r"https://cdn\.jsdelivr\.net/npm/element-plus@(?P<version>\d+\.\d+\.\d+)"
    r"/dist/index\.min\.css"
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build PGvZTool with pinned, locally bundled web dependencies."
    )
    parser.add_argument(
        "--mod-version",
        default="",
        help="override MOD_VERSION from pgvz/version.py",
    )
    parser.add_argument(
        "--game-version",
        default="",
        help="override the formatted SUPPORTED_GAME_VERSIONS value",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help="release output directory (default: %(default)s)",
    )
    return parser.parse_args()


def read_python_constants(path, names):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    values = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else (node.target,)
        for target in targets:
            if isinstance(target, ast.Name) and target.id in names:
                values[target.id] = ast.literal_eval(node.value)  # type: ignore

    missing = names.difference(values)
    if missing:
        raise ValueError(
            "Could not find constant(s) in {}: {}".format(
                path, ", ".join(sorted(missing))
            )
        )
    return values


def format_supported_game_versions(versions):
    parsed = []
    for version in versions:
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
        if match is None:
            return "_".join(versions)
        parsed.append((tuple(int(part) for part in match.groups()), version))

    if not parsed:
        raise ValueError("SUPPORTED_GAME_VERSIONS must not be empty.")

    parsed.sort(key=lambda item: item[0])
    parts = []
    group_start = parsed[0]
    previous = parsed[0]
    for current in parsed[1:]:
        previous_numbers = previous[0]
        current_numbers = current[0]
        is_consecutive = (
            current_numbers[:2] == previous_numbers[:2]
            and current_numbers[2] == previous_numbers[2] + 1
        )
        if not is_consecutive:
            parts.append(format_version_group(group_start[1], previous[1]))
            group_start = current
        previous = current
    parts.append(format_version_group(group_start[1], previous[1]))
    return "_v".join(parts)


def format_version_group(first, last):
    if first == last:
        return first
    return "{}-v{}".format(first, last)


def extract_single_version(html, pattern, dependency_name):
    versions = pattern.findall(html)
    if len(versions) != 1:
        raise ValueError(
            "Expected exactly one pinned {} URL in gui/index.html; found {}."
            .format(dependency_name, len(versions))
        )
    return versions[0]


def read_frontend_versions(index_path):
    html = index_path.read_text(encoding="utf-8")
    vue_version = extract_single_version(html, VUE_URL_PATTERN, "Vue")
    element_js_version = extract_single_version(
        html, ELEMENT_PLUS_JS_URL_PATTERN, "Element Plus JavaScript"
    )
    element_css_version = extract_single_version(
        html, ELEMENT_PLUS_CSS_URL_PATTERN, "Element Plus CSS"
    )

    if not vue_version.startswith("3."):
        raise ValueError("Only Vue 3 is supported; found {}.".format(vue_version))
    if element_js_version != element_css_version:
        raise ValueError(
            "Element Plus JavaScript ({}) and CSS ({}) versions differ."
            .format(element_js_version, element_css_version)
        )
    if not element_js_version.startswith("2."):
        raise ValueError(
            "Only Element Plus 2.x is currently supported; found {}."
            .format(element_js_version)
        )
    return vue_version, element_js_version


def validate_package_component(value, name):
    if re.fullmatch(r"[A-Za-z0-9._-]+", value) is None:
        raise ValueError(
            "{} contains characters that are unsafe in a package name: {!r}"
            .format(name, value)
        )


def ensure_clean_directory(path):
    if path.is_symlink():
        raise ValueError("Refusing to replace symlinked directory: {}".format(path))
    if path.exists():
        if not path.is_dir():
            raise ValueError("Release staging path is not a directory: {}".format(path))
        shutil.rmtree(str(path))
    path.mkdir(parents=True)


def copy_directory_clean(source, destination):
    if not source.is_dir():
        raise FileNotFoundError("Required directory does not exist: {}".format(source))
    destination.mkdir(parents=True, exist_ok=True)
    for source_path in source.rglob("*"):
        relative = source_path.relative_to(source)
        if "__pycache__" in relative.parts:
            continue
        if not source_path.is_file() or source_path.suffix in (".pyc", ".pyo"):
            continue
        target_path = destination / relative
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source_path), str(target_path))


def copy_gui(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    for file_name in ("index.html", "styles.css"):
        shutil.copy2(str(source / file_name), str(destination / file_name))
    copy_directory_clean(source / "js", destination / "js")


def download_file(url, destination):
    print("Downloading {}".format(url))
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part")
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "PGvZTool release builder"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            if getattr(response, "status", 200) != 200:
                raise RuntimeError(
                    "Download failed with HTTP {}: {}".format(response.status, url)
                )
            with temporary.open("wb") as output:
                shutil.copyfileobj(response, output)
        if temporary.stat().st_size == 0:
            raise RuntimeError("Downloaded file is empty: {}".format(url))
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def replace_once(text, pattern, replacement, description):
    result, count = pattern.subn(replacement, text)
    if count != 1:
        raise ValueError("Expected to replace one {}; replaced {}.".format(description, count))
    return result


def set_release_gui_assets(gui_dir, vue_version, element_plus_version):
    vendor_dir = gui_dir / "vendor"
    vue_path = vendor_dir / "vue" / "vue.global.prod.js"
    element_dir = vendor_dir / "element-plus"
    element_js_path = element_dir / "index.full.min.js"
    element_css_path = element_dir / "index.min.css"

    download_file(
        "https://cdn.jsdelivr.net/npm/vue@{}/dist/vue.global.prod.js".format(
            vue_version
        ),
        vue_path,
    )
    download_file(
        "https://cdn.jsdelivr.net/npm/element-plus@{}/dist/index.full.min.js".format(
            element_plus_version
        ),
        element_js_path,
    )
    download_file(
        "https://cdn.jsdelivr.net/npm/element-plus@{}/dist/index.min.css".format(
            element_plus_version
        ),
        element_css_path,
    )

    index_path = gui_dir / "index.html"
    html = index_path.read_text(encoding="utf-8")
    html = replace_once(
        html,
        ELEMENT_PLUS_CSS_URL_PATTERN,
        "./vendor/element-plus/index.min.css",
        "Element Plus CSS URL",
    )
    html = replace_once(
        html,
        VUE_URL_PATTERN,
        "./vendor/vue/vue.global.prod.js",
        "Vue URL",
    )
    html = replace_once(
        html,
        ELEMENT_PLUS_JS_URL_PATTERN,
        "./vendor/element-plus/index.full.min.js",
        "Element Plus JavaScript URL",
    )
    index_path.write_text(html, encoding="utf-8")


def write_release_readme(
    path, mod_version, game_version, vue_version, element_plus_version
):
    content = (SCRIPT_DIR / "release-readme.template.txt").read_text(encoding="utf-8")
    replacements = {
        "{{MOD_VERSION}}": mod_version,
        "{{GAME_VERSION}}": game_version,
        "{{VUE_VERSION}}": vue_version,
        "{{ELEMENT_PLUS_VERSION}}": element_plus_version,
    }
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    path.write_text(content, encoding="utf-8")


def create_zip(stage_root, zip_path):
    if zip_path.is_symlink():
        raise ValueError("Refusing to replace symlinked ZIP path: {}".format(zip_path))
    if zip_path.exists():
        if not zip_path.is_file():
            raise ValueError("Release ZIP path is not a file: {}".format(zip_path))
        zip_path.unlink()

    with zipfile.ZipFile(
        str(zip_path), mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
    ) as archive:
        for source_path in sorted(path for path in stage_root.rglob("*") if path.is_file()):
            archive.write(str(source_path), str(source_path.relative_to(stage_root)))


def build_release(args):
    version_values = read_python_constants(
        REPO_ROOT / "pgvz" / "version.py",
        {"MOD_VERSION", "SUPPORTED_GAME_VERSIONS"},
    )
    mod_version = args.mod_version or version_values["MOD_VERSION"]
    game_version = args.game_version or format_supported_game_versions(
        version_values["SUPPORTED_GAME_VERSIONS"]
    )
    validate_package_component(mod_version, "mod version")
    validate_package_component(game_version, "game version")

    vue_version, element_plus_version = read_frontend_versions(
        REPO_ROOT / "gui" / "index.html"
    )
    package_name = "PGvZTool_v{}_for_PGvZ_v{}".format(mod_version, game_version)
    output_root = args.output_root.expanduser().resolve()
    stage_root = output_root / package_name
    zip_path = output_root / (package_name + ".zip")

    output_root.mkdir(parents=True, exist_ok=True)
    ensure_clean_directory(stage_root)

    for file_name in REQUIRED_FILES:
        source = REPO_ROOT / file_name
        if not source.is_file():
            raise FileNotFoundError("Required file does not exist: {}".format(source))
        shutil.copy2(str(source), str(stage_root / file_name))

    for directory_name in REQUIRED_DIRS:
        copy_directory_clean(
            REPO_ROOT / directory_name,
            stage_root / directory_name,
        )

    copy_gui(REPO_ROOT / "gui", stage_root / "gui")
    set_release_gui_assets(stage_root / "gui", vue_version, element_plus_version)
    write_release_readme(
        stage_root / README_NAME,
        mod_version,
        game_version,
        vue_version,
        element_plus_version,
    )
    create_zip(stage_root, zip_path)

    print("\nRelease package created:")
    print("  Directory: {}".format(stage_root))
    print("  Zip:       {}".format(zip_path))
    print("  Vue:       {}".format(vue_version))
    print("  Element+:  {}".format(element_plus_version))


def main():
    try:
        build_release(parse_args())
    except (OSError, RuntimeError, ValueError) as error:
        print("error: {}".format(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
