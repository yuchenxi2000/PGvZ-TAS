import typing
from System import IDisposable, IServiceProvider
from System.Collections.Generic import IList_1

class ContentManager(IDisposable):
    @typing.overload
    def __init__(self, serviceProvider: IServiceProvider) -> None: ...
    @typing.overload
    def __init__(self, serviceProvider: IServiceProvider, rootDirectory: str) -> None: ...
    @property
    def RootDirectory(self) -> str: ...
    @RootDirectory.setter
    def RootDirectory(self, value: str) -> str: ...
    @property
    def ServiceProvider(self) -> IServiceProvider: ...
    def Dispose(self) -> None: ...
    def Unload(self) -> None: ...
    def UnloadAsset(self, assetName: str) -> None: ...
    def UnloadAssets(self, assetNames: IList_1[str]) -> None: ...
    # Skipped Load due to it being static, abstract and generic.

    Load : Load_MethodGroup
    class Load_MethodGroup:
        def __getitem__(self, t:typing.Type[Load_1_T1]) -> Load_1[Load_1_T1]: ...

        Load_1_T1 = typing.TypeVar('Load_1_T1')
        class Load_1(typing.Generic[Load_1_T1]):
            Load_1_T = ContentManager.Load_MethodGroup.Load_1_T1
            def __call__(self, assetName: str) -> Load_1_T:...


    # Skipped LoadLocalized due to it being static, abstract and generic.

    LoadLocalized : LoadLocalized_MethodGroup
    class LoadLocalized_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadLocalized_1_T1]) -> LoadLocalized_1[LoadLocalized_1_T1]: ...

        LoadLocalized_1_T1 = typing.TypeVar('LoadLocalized_1_T1')
        class LoadLocalized_1(typing.Generic[LoadLocalized_1_T1]):
            LoadLocalized_1_T = ContentManager.LoadLocalized_MethodGroup.LoadLocalized_1_T1
            def __call__(self, assetName: str) -> LoadLocalized_1_T:...



