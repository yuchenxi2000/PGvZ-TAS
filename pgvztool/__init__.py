"""
植物娘大战僵尸简易修改器 PGvZTool v1.8.0
for PGvZ v1.1.4-v1.1.5 by yuchenxi2000
依赖pgvz包
"""
from .cheat import cheat_option
from .placer import placer
from .sync import sync_reg
from . import hook

sync_reg.register('cheat', cheat_option)
sync_reg.register('placer', placer)

__all__ = [
    "cheat_option", "placer", "sync_reg",
]
