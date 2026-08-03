"""
导入目录下所有脚本
该文件必须要有，IronPython不支持无__init__.py的Python模块
"""
from .beghouled import script_beghouled, script_beghouled_twist
from .me10 import script_me10
from .pe12 import script_pe12
from .slotmachine import script_slotmachine
from .whackazombie import script_whackazombie

__all__ = [
    'script_beghouled', 'script_beghouled_twist',
    'script_me10', 'script_pe12',
    'script_slotmachine', 'script_whackazombie'
]
