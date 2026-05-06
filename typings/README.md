# 关于存根文件

本目录下存根文件（.pyi）由PythonNetStubGenerator根据动态库元数据提取而成，不包括具体实现。原API及版权归各作者所有，存根文件仅作为接口声明。

生成Python存根文件的方法：

```powershell
# 安装pyi生成工具
dotnet tool install --global PythonNetStubGenerator.Tool
# 生成stub，假设生成在stubs目录下
GeneratePythonNetStubs.exe --target-dlls Lawn.dll --dest-path stubs
```

