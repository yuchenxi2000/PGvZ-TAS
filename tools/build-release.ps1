param(
    [string]$ModVersion = "",
    [string]$GameVersion = "",
    [string]$OutputRoot = ""
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path $RepoRoot "dist"
}

$ReadmeName = (-join ([char[]](0x4f7f, 0x7528, 0x65b9, 0x6cd5))) + "README.txt"

$RequiredFiles = @(
    "cheat-gui.py",
    "cp-cheat-mods.bat",
    "LICENSE"
)

$RequiredDirs = @(
    "pgvz",
    "pgvztool"
)

function Ensure-CleanDirectory($Path) {
    if (Test-Path $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
    New-Item -ItemType Directory -Path $Path | Out-Null
}

function Copy-DirectoryClean($Source, $Destination) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    $sourceRoot = (Resolve-Path $Source).Path.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    Get-ChildItem -LiteralPath $Source -Recurse -File | ForEach-Object {
        $relative = $_.FullName.Substring($sourceRoot.Length)
        if ($relative -match '(^|[\\/])__pycache__([\\/]|$)') { return }
        if ($_.Extension -in @(".pyc", ".pyo")) { return }
        $target = Join-Path $Destination $relative
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $target -Force
    }
}

function Copy-Gui($Source, $Destination) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $Source "index.html") -Destination (Join-Path $Destination "index.html") -Force
    Copy-Item -LiteralPath (Join-Path $Source "styles.css") -Destination (Join-Path $Destination "styles.css") -Force
    Copy-DirectoryClean (Join-Path $Source "js") (Join-Path $Destination "js")
}

function Get-NpmPackageMeta($PackageName) {
    $uri = "https://registry.npmjs.org/$PackageName"
    Write-Host "Fetching npm metadata: $PackageName"
    return Invoke-RestMethod -Uri $uri -Headers @{ "Accept" = "application/json" }
}

function Get-LatestVue3Version {
    $meta = Get-NpmPackageMeta "vue"
    $versions = $meta.versions.PSObject.Properties.Name |
        Where-Object { $_ -match '^3\.\d+\.\d+$' } |
        Sort-Object { [System.Version]$_ }
    if (-not $versions) {
        throw "Could not find a stable Vue 3 version in npm metadata."
    }
    return $versions[-1]
}

function Get-LatestPackageVersion($PackageName) {
    $meta = Get-NpmPackageMeta $PackageName
    $version = $meta.'dist-tags'.latest
    if ([string]::IsNullOrWhiteSpace($version)) {
        throw "Could not find npm dist-tag latest for $PackageName."
    }
    return $version
}

function Download-File($Uri, $Destination) {
    Write-Host "Downloading $Uri"
    New-Item -ItemType Directory -Path (Split-Path -Parent $Destination) -Force | Out-Null
    Invoke-WebRequest -Uri $Uri -OutFile $Destination
}

function Get-PythonStringConstant($Text, $Name) {
    $pattern = '(?m)^\s*' + [regex]::Escape($Name) + '\s*=\s*[''"]([^''"]+)[''"]'
    $match = [regex]::Match($Text, $pattern)
    if (-not $match.Success) {
        throw "Could not find string constant $Name."
    }
    return $match.Groups[1].Value
}

function Get-PythonTupleStrings($Text, $Name) {
    $pattern = '(?s)' + [regex]::Escape($Name) + '\s*=\s*\((.*?)\)'
    $match = [regex]::Match($Text, $pattern)
    if (-not $match.Success) {
        throw "Could not find tuple constant $Name."
    }
    $items = @()
    [regex]::Matches($match.Groups[1].Value, '[''"]([^''"]+)[''"]') | ForEach-Object {
        $items += $_.Groups[1].Value
    }
    if (-not $items) {
        throw "Tuple constant $Name is empty."
    }
    return $items
}

function Format-SupportedGameVersions($Versions) {
    $parsed = @()
    foreach ($version in $Versions) {
        if ($version -notmatch '^(\d+)\.(\d+)\.(\d+)$') {
            return ($Versions -join "_")
        }
        $parsed += [pscustomobject]@{
            Text = $version
            Major = [int]$Matches[1]
            Minor = [int]$Matches[2]
            Patch = [int]$Matches[3]
        }
    }
    $sorted = $parsed | Sort-Object Major, Minor, Patch
    $parts = @()
    $groupStart = $sorted[0]
    $prev = $sorted[0]
    for ($i = 1; $i -lt $sorted.Count; $i++) {
        $curr = $sorted[$i]
        $sameLine = $curr.Major -eq $prev.Major -and $curr.Minor -eq $prev.Minor
        $nextPatch = $curr.Patch -eq ($prev.Patch + 1)
        if (-not ($sameLine -and $nextPatch)) {
            if ($groupStart.Text -eq $prev.Text) {
                $parts += $groupStart.Text
            } else {
                $parts += "$($groupStart.Text)-v$($prev.Text)"
            }
            $groupStart = $curr
        }
        $prev = $curr
    }
    if ($groupStart.Text -eq $prev.Text) {
        $parts += $groupStart.Text
    } else {
        $parts += "$($groupStart.Text)-v$($prev.Text)"
    }
    return ($parts -join "_v")
}

function Set-ReleaseGuiAssets($GuiDir, $VueVersion, $ElementPlusVersion) {
    $vendorDir = Join-Path $GuiDir "vendor"
    $vueDir = Join-Path $vendorDir "vue"
    $elementDir = Join-Path $vendorDir "element-plus"

    Download-File "https://cdn.jsdelivr.net/npm/vue@$VueVersion/dist/vue.global.prod.js" `
        (Join-Path $vueDir "vue.global.prod.js")
    Download-File "https://cdn.jsdelivr.net/npm/element-plus@$ElementPlusVersion/dist/index.full.min.js" `
        (Join-Path $elementDir "index.full.min.js")
    Download-File "https://cdn.jsdelivr.net/npm/element-plus@$ElementPlusVersion/dist/index.min.css" `
        (Join-Path $elementDir "index.min.css")

    $indexPath = Join-Path $GuiDir "index.html"
    $html = Get-Content -LiteralPath $indexPath -Raw -Encoding UTF8
    $html = $html -replace 'https://cdn\.jsdelivr\.net/npm/element-plus@[^"]+/dist/index\.min\.css', './vendor/element-plus/index.min.css'
    $html = $html -replace 'https://cdn\.jsdelivr\.net/npm/vue@[^"]+/dist/vue\.global\.min\.js', './vendor/vue/vue.global.prod.js'
    $html = $html -replace 'https://cdn\.jsdelivr\.net/npm/element-plus@[^"]+/dist/index\.full\.min\.js', './vendor/element-plus/index.full.min.js'
    Set-Content -LiteralPath $indexPath -Value $html -Encoding UTF8
}

function Write-ReleaseReadme($Path, $ModVersion, $GameVersion, $VueVersion, $ElementPlusVersion) {
    $templatePath = Join-Path $ScriptDir "release-readme.template.txt"
    $content = Get-Content -LiteralPath $templatePath -Raw -Encoding UTF8
    $content = $content.Replace("{{MOD_VERSION}}", $ModVersion)
    $content = $content.Replace("{{GAME_VERSION}}", $GameVersion)
    $content = $content.Replace("{{VUE_VERSION}}", $VueVersion)
    $content = $content.Replace("{{ELEMENT_PLUS_VERSION}}", $ElementPlusVersion)
    Set-Content -LiteralPath $Path -Value $content -Encoding UTF8
}

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$VersionFile = Join-Path $RepoRoot "pgvz\version.py"
$VersionText = Get-Content -LiteralPath $VersionFile -Raw -Encoding UTF8
if ([string]::IsNullOrWhiteSpace($ModVersion)) {
    $ModVersion = Get-PythonStringConstant $VersionText "MOD_VERSION"
}
if ([string]::IsNullOrWhiteSpace($GameVersion)) {
    $GameVersion = Format-SupportedGameVersions (Get-PythonTupleStrings $VersionText "SUPPORTED_GAME_VERSIONS")
}

$PackageName = "PGvZTool_v${ModVersion}_for_PGvZ_v${GameVersion}"
$StageRoot = Join-Path $OutputRoot $PackageName
$ZipPath = Join-Path $OutputRoot "$PackageName.zip"

New-Item -ItemType Directory -Path $OutputRoot -Force | Out-Null
Ensure-CleanDirectory $StageRoot
if (Test-Path $ZipPath) {
    Remove-Item -LiteralPath $ZipPath -Force
}

foreach ($file in $RequiredFiles) {
    Copy-Item -LiteralPath (Join-Path $RepoRoot $file) -Destination (Join-Path $StageRoot $file) -Force
}

foreach ($dir in $RequiredDirs) {
    Copy-DirectoryClean (Join-Path $RepoRoot $dir) (Join-Path $StageRoot $dir)
}

Copy-Gui (Join-Path $RepoRoot "gui") (Join-Path $StageRoot "gui")

$VueVersion = Get-LatestVue3Version
$ElementPlusVersion = Get-LatestPackageVersion "element-plus"

Set-ReleaseGuiAssets (Join-Path $StageRoot "gui") $VueVersion $ElementPlusVersion
Write-ReleaseReadme (Join-Path $StageRoot $ReadmeName) $ModVersion $GameVersion $VueVersion $ElementPlusVersion

Compress-Archive -Path (Join-Path $StageRoot "*") -DestinationPath $ZipPath -Force

Write-Host ""
Write-Host "Release package created:"
Write-Host "  Directory: $StageRoot"
Write-Host "  Zip:       $ZipPath"
Write-Host "  Vue:       $VueVersion"
Write-Host "  Element+:  $ElementPlusVersion"
