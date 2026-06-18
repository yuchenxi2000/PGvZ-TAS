# 示例脚本

本目录下是一些示例PGvZ-TAS脚本

## 使用方法

如果想使用有两种方法：

1. 把脚本从这个文件夹移到外面，使其直接位于模组文件夹下面，这样游戏启动时会将其自动加载

2. 不移动文件，游戏运行时打开修改器，最后一栏“自定义”里面输入Python代码然后执行。假设要使用`pe12.py`，那么就输入代码
   ```python
   import scripts.pe12
   ```
   想全都用可以
   ```python
   from scripts import *
   ```

3. 想在游戏开启状态下停用某个已import的脚本，可以按上述方法执行Python代码，假设我们想停用`pe12.py`，就输入代码
   ```python
   script_pe12.Off()
   ```
   这个`script_pe12`是`pe12.py`导出的`ScriptObj`对象。或者也可以直接卸载该脚本：
   ```python
   script_manager.Unregister(script_pe12)
   ```

> `__init__.py`没什么用，单纯为了让第二种方法能够成功import
> 
> 因为IronPython的Python版本太老了，竟然不支持无`__init__.py`的Python模块！
