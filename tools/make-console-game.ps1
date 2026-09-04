[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$GameDirectory = 'C:\Program Files\ZBC\PlantGirlsVsZombies',

    [string]$OutputName = 'Lawn.Console.Fixed.exe',

    [switch]$Force
)

$ErrorActionPreference = 'Stop'

if ([System.IO.Path]::GetFileName($OutputName) -ne $OutputName) {
    throw 'OutputName 只能是文件名；请用 GameDirectory 指定输出目录。'
}

$source = Join-Path $GameDirectory 'Lawn.exe'
$target = Join-Path $GameDirectory $OutputName

if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "找不到游戏主程序：$source"
}

if (
    [System.StringComparer]::OrdinalIgnoreCase.Equals(
        [System.IO.Path]::GetFullPath($source),
        [System.IO.Path]::GetFullPath($target)
    )
) {
    throw '输出文件不能覆盖 Lawn.exe。'
}

if ((Test-Path -LiteralPath $target) -and -not $Force) {
    throw "输出文件已存在：$target。确认游戏已关闭后使用 -Force 覆盖。"
}

# 直接复制单文件版 Lawn.exe 的字节，只修改 PE Optional Header 中的
# Subsystem 字段。不要用 objcopy 等会丢弃文件末尾 .NET bundle 数据的工具。
$bytes = [System.IO.File]::ReadAllBytes($source)

if ($bytes.Length -lt 0x40 -or $bytes[0] -ne 0x4D -or $bytes[1] -ne 0x5A) {
    throw 'Lawn.exe 不是有效的 PE/MZ 文件。'
}

$peOffset = [BitConverter]::ToInt32($bytes, 0x3C)
if ($peOffset -lt 0 -or $peOffset + 96 -gt $bytes.Length) {
    throw 'Lawn.exe 中的 PE 文件头偏移无效。'
}

if (
    $bytes[$peOffset] -ne 0x50 -or
    $bytes[$peOffset + 1] -ne 0x45 -or
    $bytes[$peOffset + 2] -ne 0x00 -or
    $bytes[$peOffset + 3] -ne 0x00
) {
    throw 'Lawn.exe 中没有有效的 PE 文件头。'
}

$optionalHeaderOffset = $peOffset + 24
$optionalHeaderMagic = [BitConverter]::ToUInt16($bytes, $optionalHeaderOffset)
if ($optionalHeaderMagic -ne 0x10B -and $optionalHeaderMagic -ne 0x20B) {
    throw ('不支持的 PE Optional Header 类型：0x{0:X}。' -f $optionalHeaderMagic)
}

$subsystemOffset = $optionalHeaderOffset + 68
$oldSubsystem = [BitConverter]::ToUInt16($bytes, $subsystemOffset)
if ($oldSubsystem -ne 2) {
    throw "预期 Lawn.exe 的 Subsystem 为 WINDOWS_GUI (2)，实际为 $oldSubsystem；未生成文件。"
}

# IMAGE_SUBSYSTEM_WINDOWS_GUI (2) -> IMAGE_SUBSYSTEM_WINDOWS_CUI (3)
$bytes[$subsystemOffset] = 3
$bytes[$subsystemOffset + 1] = 0

try {
    [System.IO.File]::WriteAllBytes($target, $bytes)
}
catch [System.UnauthorizedAccessException] {
    throw "无法写入 $GameDirectory。若游戏安装在 Program Files，请以管理员身份运行 PowerShell。"
}

$check = [System.IO.File]::ReadAllBytes($target)
$newSubsystem = [BitConverter]::ToUInt16($check, $subsystemOffset)
if ($newSubsystem -ne 3) {
    throw "写入后验证失败：Subsystem=$newSubsystem。"
}

Write-Host "已生成控制台版游戏：$target"
Write-Host '原始 Lawn.exe 未被修改。游戏更新后请重新运行本工具。'
