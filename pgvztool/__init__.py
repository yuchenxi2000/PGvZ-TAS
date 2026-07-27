"""
植物娘大战僵尸简易修改器 PGvZTool
by yuchenxi2000
依赖pgvz包
"""
from pgvz.version import MOD_VERSION, SUPPORTED_GAME_VERSIONS
from .cheat import cheat_option
from .placer import placer
from .sync import sync_reg
from . import hook

sync_reg.register('cheat', cheat_option)
sync_reg.register('placer', placer)

__version__ = MOD_VERSION
__supported_game_versions__ = SUPPORTED_GAME_VERSIONS

__all__ = [
    "cheat_option", "placer", "sync_reg",
    "MOD_VERSION", "SUPPORTED_GAME_VERSIONS",
    "__version__", "__supported_game_versions__",
]
