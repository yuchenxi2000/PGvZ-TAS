# PGvZ-TAS

植物娘大战僵尸键控框架 Tool-Assisted Superplay framework for PlantGirls vs. Zombies，以及简易修改器

by yuchenxi2000

## 介绍

这个项目是植物大战僵尸改版，植物娘大战僵尸的键控框架。游戏作者[庄不纯](https://space.bilibili.com/20530305)

“键控框架”这个名称是历史原因，更准确的名称是工具辅助操作框架（TAS框架）。可以实现自动操作，比如自动锤僵尸，自动操作泳池无尽的玉米加农炮等。

## 使用方法

把本仓库下载下来，然后把里面的所有文件放到游戏的`mods`目录下。注意游戏只会加载`mods`目录下以`.py`作为后缀的文件，因此脚本必须直接放`mods`目录下。`pgvz`文件夹直接放`mods`目录下，里面文件不要动。

对于PC版游戏，默认的`mods`目录是`C:\Users\你的用户名\AppData\Roaming\ZBC\PlantGirlsVsZombies\mods`

如果不生效，可能的原因是没有开启模组功能，你需要编辑一下配置文件`C:\Users\你的用户名\AppData\Roaming\ZBC\PlantGirlsVsZombies\user_config.json`，把`ironpython_enabled`这个选项改成`true`

本仓库包含键控框架模块`pgvz`，以及几个可直接作为模组加载的示例脚本。

## 修改器使用方法

1. 按上节方法，将`pgvz`文件夹和`cheat.py`放到`mods`目录下；或者直接运行`cp-cheat-mods.bat`

2. 双击`cheat-gui.html`开始使用

## 脚本编写教程

TAS框架的模块是pgvz，编写脚本先要import这个模块。

接口和植物大战僵尸原版的[pyvz](https://pvz.tools/scripts/)、[AvZ](https://github.com/vector-wlc/AsmVsZombies)框架类似，如果熟悉这两个框架会容易一些。因为接口类似，建议先阅读[pyvz](https://pvz.tools/scripts/)的教程。

本模块基本实现所有常用功能。包括种植物`Card`、铲植物`Shovel`、选卡`SelectCards`、设置僵尸列表`SetZombies`、发射玉米炮`CobManager.Fire`、时间相关操作`Delay`,`Prejudge`,`Until`，`DelayA`，以及一些常用操作，比如迭代所有存活植物/僵尸/物品`IterAliveZombies`,`IterAlivePlants`,`IterAliveCoins`等。

下面介绍和pyvz、AvZ的异同：

1. PvZ基类、主类的访问通过游戏C#静态对象`Sexy.GlobalStaticVars`，`Sexy.GlobalStaticVars.gLawnApp`就是其他框架的`PvzBase`，`Sexy.GlobalStaticVars.gLawnApp.mBoard`就是其他框架的`MainObject`

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

    选卡函数`SelectCards`，开始游戏`LetsRock`也是阻塞操作，也需要在前面加`yield from`。或者，凡是函数内含`yield`关键字的都是生成器函数，要以类似方式调用。

    选卡函数的参数是一个`Lawn.SeedType`的列表，以及一个可选参数。如果要选模仿者，那么在列表里填模仿者，然后第二个可选参数填要模仿的植物。选完卡默认等2秒开始游戏，可以改`waitTime`参数来改等待时长。

    如果你的阻塞脚本没有使用任何阻塞函数，那么要在末尾加个`yield`使其成为生成器函数，不然会被认为是非阻塞。

6. 不同于pyvz和AvZ，本框架可以调用任意游戏内部函数。内部函数可以通过反编译得到（比如用ILSpy），也可以参考`typings`目录下的`.pyi`存根文件，它们列出了所有游戏内部C#对象/方法的Python对应。所以要使用左键点击直接调用`Lawn.Board.MouseDown`（用全局对象获取游戏`Board`对象，`Sexy.GlobalStaticVars.gLawnApp.mBoard`），本框架不再提供此类接口

7. 不同于pyvz和AvZ，本框架（有限）支持中途退出游戏。重进以后会从原来退出的时间点继续脚本操作，过去时间点的操作会无视，不会像pyvz和AvZ一样过去时间点的堆积到现在时间点操作。

    但是写脚本时必须需要用`DelayA`替换`Delay`，后者只是为了和pyvz的旧API保持一致。`DelayA`在退出重进时，能保证其行为和非中途退出重进情形一致，但Delay不行，因为Delay等待固定时长，而DelayA的参考点是刷新点。因此，`DelayA`前面一定要有`Prejudge`。
    
    此外，脚本编写时要注意都以刷新点为参考点，避免出现等待固定时长；且涉及分支判断时要小心，比如不能直接判断场上是否存在僵尸，要额外判断僵尸是否属于本波次。

    如果不在写脚本时注意这些，本框架也能在有限程度上支持退出重进，只不过仍存在一些误操作可能。因此最好关卡结束（普通关卡）或重新回到选卡界面（生存模式）后再退出。
    
    或者使用`SurvivalBackupGame`进行备份，破阵就回档（默认存档目录`C:\Users\你的用户名\AppData\Roaming\ZBC\PlantGirlsVsZombies\docs\userdata`）

可以参考本仓库的示例脚本，`pe12.py`是泳池无尽的经典十二炮脚本（阻塞脚本），`beghouled.py`是宝石迷阵系列的自动脚本（非阻塞），`whackazombie.py`是锤僵尸自动脚本（非阻塞）。

如果需要调试，可以运行`Lawn.Console.exe`，这是包含命令行界面的游戏版本。在脚本里使用`Sexy.Debug.Log`在命令行输出调试信息。

可以将`typings`目录加到类型检查器的路径里面，比如VS Code的pylance插件默认python存根文件目录`typings`。需要调用游戏内部函数时，`typings`目录下的pyi可以提供类型提示。

## 进阶教程

一些功能的实现可能需要hook游戏内部函数，游戏自带的`LawnMod`可实现这个功能。

主要有两种方式：

1. 使用`LawnMod.MonoModUtils.HookTo`装饰器

2. 使用`LawnMod.MonoModUtils.As`装饰器，然后用`LawnMod.MonoModUtils.On`的+运算符，这样的好处是可以用-运算符卸载钩子。但注意如果用了多次+运算符挂同一个函数，该函数会被执行多次！

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

