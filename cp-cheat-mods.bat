@echo off
set "TARGET=%APPDATA%\ZBC\PlantGirlsVsZombies\mods"

if not exist "%TARGET%" mkdir "%TARGET%"

echo Copying cheat-gui.py ...
copy /Y "%~dp0cheat-gui.py" "%TARGET%\" >nul 2>&1
if %errorlevel% equ 0 (echo   OK) else (echo   FAILED)

echo Copying pgvz ...
if exist "%~dp0pgvz\" (
    xcopy /E /I /Y "%~dp0pgvz" "%TARGET%\pgvz\" >nul 2>&1
    if %errorlevel% equ 0 (echo   OK) else (echo   FAILED)
) else (echo   ERROR: pgvz not found)

echo Copying pgvztool ...
if exist "%~dp0pgvztool\" (
    xcopy /E /I /Y "%~dp0pgvztool" "%TARGET%\pgvztool\" >nul 2>&1
    if %errorlevel% equ 0 (echo   OK) else (echo   FAILED)
) else (echo   ERROR: pgvztool not found)

echo Copying gui ...
if exist "%~dp0gui\" (
    xcopy /E /I /Y "%~dp0gui" "%TARGET%\gui\" >nul 2>&1
    if %errorlevel% equ 0 (echo   OK) else (echo   FAILED)
) else (echo   ERROR: gui not found)

echo.
echo Done. Start the game, then open http://localhost:58080 in browser.
pause >nul
