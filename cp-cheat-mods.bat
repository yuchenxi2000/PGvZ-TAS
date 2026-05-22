@echo off
:: set target dir path
set "TARGET=%APPDATA%\ZBC\PlantGirlsVsZombies\mods"

:: create mods folder
if not exist "%TARGET%" mkdir "%TARGET%"

:: copy cheat.py
echo Copying cheat.py ...
copy /Y "%~dp0cheat.py" "%TARGET%\" >nul 2>&1
if %errorlevel% equ 0 (echo   cheat.py copyed) else (echo   Failed! please check whether cheat.py exists)

:: copy pgvz
echo Copying pgvz folder ...
if exist "%~dp0pgvz\" (
    xcopy /E /I /Y "%~dp0pgvz" "%TARGET%\pgvz\" >nul 2>&1
    if %errorlevel% equ 0 (echo   pgvz copyed) else (echo   Failed! please check whether pgvz exists)
) else (
    echo   Error: pgvz not exists
)

echo.
echo Success. Press any key to exit...
pause >nul
