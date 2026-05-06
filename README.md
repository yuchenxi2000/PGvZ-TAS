# PGvZ-TAS

植物娘大战僵尸键控框架 Tool-Assisted Superplay framework for PlantsGirls vs. Zombies

by yuchenxi2000

## 介绍

这个项目是植物大战僵尸改版，植物娘大战僵尸的键控框架。游戏作者[庄不纯](https://space.bilibili.com/20530305)

“键控框架”这个名称是历史原因，更准确的名称是工具辅助操作框架（TAS框架）。可以实现自动操作，比如自动锤僵尸，自动操作泳池无尽的玉米加农炮等。

## 使用方法

把本仓库下载下来，然后把里面的所有文件放到游戏的mods目录下。注意游戏只会加载mods目录下以.py作为后缀的文件，因此脚本必须直接放mods目录下。pgvz文件夹直接放mods目录下，里面文件不要动。

对于PC版游戏，默认的mods目录是C:\\Users\\你的用户名\\AppData\\Roaming\\ZBC\\PlantGirlsVsZombies\\mods

如果不生效，可能的原因是没有开启模组功能，你需要编辑一下配置文件C:\\Users\\你的用户名\\AppData\\Roaming\\ZBC\\PlantGirlsVsZombies\\user_config.json，把ironpython_enabled这个选项改成true

本仓库包含键控框架模块`pgvz`，以及几个可直接作为模组加载的示例脚本。

## 脚本编写教程

TAS框架的模块是pgvz，编写脚本先要import这个模块。

接口和植物大战僵尸原版的[pyvz](https://pvz.tools/scripts/)、[AvZ](https://github.com/vector-wlc/AsmVsZombies)框架类似，如果熟悉这两个框架会容易一些。因为接口类似，建议先阅读[pyvz](https://pvz.tools/scripts/)的教程。

由于时间精力关系，本模块没有实现所有功能。本模块实现的主要功能有种植物`Card`、铲植物`Shovel`、发射玉米炮`CobManager.Fire`、时间相关操作`Delay``Prejudge``Until`，以及一些常用操作，比如迭代所有存活植物/僵尸/物品`IterAliveZombies``IterAlivePlants``IterAliveCoins`。

下面介绍和pyvz、AvZ的异同：

1. PvZ基类、主类的访问通过全局对象`gvar`，`gvar.glawnapp`就是其他框架的`PvzBase`，`gvar.gboard`就是其他框架的`MainObject`

2. 脚本在引入pgvz模块前，必须设置加载路径为脚本所在目录，如下所示。这个是游戏本身的锅，我也没办法

    ```python
    # 先设置加载路径
    import sys
    import os
    sys.path.append(os.path.dirname(__file__))
    # 然后再引入模块
    from pgvz import *
    ```

3. 不同于pyvz直接写脚本和AvZ需要写在AScript函数里面，本框架的脚本可以写在任意无参数函数里面，且一个脚本可以写任意数量的脚本。但是脚本需要注册到`script_manager`：

    ```python
    # 泳池无尽经典十二炮脚本
    def ScriptPE12():
        ...

    # 需要注册，你可以限制它只在泳池无尽关卡运行
    script_manager.Register(ScriptPE12, gamemode=Lawn.GameMode.SurvivalEndlessStage3)
    ```

4. 本框架允许多个`.py`脚本文件共存，各脚本互不影响。

5. 本框架的脚本函数分为阻塞和非阻塞两种。阻塞（类似协程）用生成器函数实现，函数内有`yield`关键字，按时间顺序执行；非阻塞脚本函数每个游戏帧被调用一次。所有时间相关操作都是阻塞操作，因此都需要在前面加`yield from`：

    ```python
    def ScriptPE12():
        ...
        # 比如十二炮预判炸
        # 每关预判
        yield from Prejudge(-199, wave)

        # 每波预判炸
        yield from Until(341 - 373)
        cob_manager.Fire((2, 8.8), (5, 8.8))
        ...
    ```

6. 不同于pyvz和AvZ，本框架可以调用任意游戏内部函数。内部函数可以通过反编译得到（比如用ILSpy），也可以参考`typings`目录下的`.pyi`存根文件，它们列出了所有游戏内部C#对象/方法的Python对应。所以要使用左键点击直接调用`Lawn.Board.MouseDown`（用全局对象获取游戏`Board`对象，`gvar.gboard`），本框架不再提供此类接口

可以参考本仓库的示例脚本，`pe12.py`是泳池无尽的经典十二炮脚本（阻塞脚本），`beghouled.py`是宝石迷阵系列的自动脚本（非阻塞），`whackazombie.py`是锤僵尸自动脚本（非阻塞）。

如果需要调试，可以运行`Lawn.Console.exe`，这是包含命令行界面的游戏版本。在脚本里使用`Sexy.Debug.Log`在命令行输出调试信息。

可以将`typings`目录加到类型检查器的路径里面，比如VS Code的pylance插件默认python存根文件目录`typings`。需要调用游戏内部函数时，`typings`目录下的pyi可以提供类型提示。

## 进阶教程

一些功能的实现可能需要hook游戏内部函数，游戏自带的`LawnMod`可实现这个功能。

主要有两种方式：

1. 使用`LawnMod.MonoModUtils.HookTo`装饰器，此时游戏会调用被装饰的Python函数而不是内部函数。此类钩子只能挂一次

2. 使用`LawnMod.MonoModUtils.AsAction`装饰器，作用是把函数转为类方法，然后用`LawnMod.MonoModUtils.On`的+运算符。这类钩子能挂多次

注意被包装函数的第一个参数是原方法。如果是成员方法，第二个参数是对象，后续是类方法的参数；如果是静态方法，则没有对象参数。

具体写法详见`cheat.py`以及`pgvz/__init__.py`。

## 参考资料

下面是一些资料可供参考：

1. 游戏实现python模组的代码 https://github.com/rspforhp/PVZdotnet-ready-to-mod/blob/master/LawnModExtension/MonoModUtils.cs

2. 游戏模组脚本语言IronPython的文档 https://ironpython.pythonlang.cn/documentation/dotnet/

3. 游戏实现模组对游戏内容修改的框架MonoMod https://github.com/MonoMod/MonoMod/tree/reorganize

4. C#反编译工具ILSpy https://github.com/icsharpcode/ILSpy

5. 从C#动态库生成Python存根文件的工具PythonNetStubGenerator https://www.nuget.org/packages/PythonNetStubGenerator.Tool/

6. 植物大战僵尸原版键控框架AvZ https://github.com/vector-wlc/AsmVsZombies

7. 植物大战僵尸原版键控框架pyvz https://pvz.tools/scripts/

