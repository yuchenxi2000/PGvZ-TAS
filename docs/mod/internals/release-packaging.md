# 正式版与 nightly 打包

使用 Python 3 运行仓库中的 `tools/build-release.py`。两种模式共用文件收集、前端依赖下载、离线资源替换、说明文件生成和 ZIP 压缩流程，无需额外的 nightly 脚本。

```sh
# 原有正式版打包
python tools/build-release.py

# 打包当前工作区的 nightly
python tools/build-release.py --nightly

# 明确指定下一版的基础版本
python tools/build-release.py --nightly --mod-version 1.17.0

# 自定义输出目录（两种模式均支持）
python tools/build-release.py --nightly --output-root dist/nightly
```

## 版本号

nightly 没有跨项目统一的命名规范。例如 [Rust](https://rust-lang.github.io/rustup/concepts/toolchains.html) 使用 `nightly-YYYY-MM-DD` 标识工具链，[Electron](https://releases.electronjs.org/release?channel=nightly) 使用 `主.次.修订-nightly.YYYYMMDD`。

本项目使用 `基础版本-nightly.YYYYMMDDTHHMMSSZ`，例如 `1.16.1-nightly.20261115T183106Z`。时间为 UTC，`Z` 表示 UTC；精确到秒，以区分同一天多次本地构建。整个时间戳包含字母，符合 [SemVer](https://semver.org/) 对预发布标识符的要求，也避免将带前导零的时分秒作为独立数值标识符。

基础版本默认取源码的 `MOD_VERSION`，也可通过 `--mod-version` 指定，必须为不含后缀的 `主.次.修订`。默认沿用源码版本便于识别构建基线，不自动推断下一次正式发布的版本号。按 SemVer，同一基础版本的 nightly 小于正式版；需要作为下一正式版的预发布版本分发时，应明确指定目标基础版本。

## 产物与覆盖规则

默认输出到 `dist/`，同时保留解包目录和 ZIP。nightly 示例：

```text
PGvZTool_v1.16.1-nightly.20261115T183106Z_for_PGvZ_v1.4.3/
PGvZTool_v1.16.1-nightly.20261115T183106Z_for_PGvZ_v1.4.3.zip
```

nightly 遇到同名目录或 ZIP 会报错退出，不覆盖已有产物；同一秒再次打包或失败后重试，可等到下一秒再运行。正式版保留原有行为，重新打包会替换同名目录和 ZIP。

文件名、包内 `pgvz/version.py` 和使用说明均使用本次构建版本，网页也会读取到该版本。`--mod-version` 在正式版模式下同样修改包内版本。

打包不会修改工作区的 `pgvz/version.py` 或 `CHANGELOG.md`。nightly 保留源码中的正式版本号及 `[unreleased]` 日志；正式发布仍需先按仓库的发布规则更新版本和日志，再执行打包。前端依赖始终按源码中固定的 Vue 和 Element Plus 版本下载，生成的控制台可离线使用。
