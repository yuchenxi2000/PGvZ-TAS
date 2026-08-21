@echo off
set "TARGET=%APPDATA%\ZBC\PlantGirlsVsZombies\mods"

if /I "%~dp0"=="%TARGET%\" goto :installer_inside_target
if not exist "%TARGET%\" mkdir "%TARGET%"
if not exist "%TARGET%\" goto :target_directory_failed

call :require_source_file "cheat-gui.py"
if errorlevel 1 goto :install_failed
call :require_source_directory "pgvz"
if errorlevel 1 goto :install_failed
call :require_source_directory "pgvztool"
if errorlevel 1 goto :install_failed
call :require_source_directory "gui"
if errorlevel 1 goto :install_failed

call :disable_legacy_entry "cheat.py"
if errorlevel 1 goto :install_failed
call :remove_old_file "cheat-gui.py"
if errorlevel 1 goto :install_failed
call :remove_old_directory "pgvz"
if errorlevel 1 goto :install_failed
call :remove_old_directory "pgvztool"
if errorlevel 1 goto :install_failed
call :remove_old_directory "gui"
if errorlevel 1 goto :install_failed

call :copy_source_file "cheat-gui.py"
if errorlevel 1 goto :install_failed
call :copy_source_directory "pgvz"
if errorlevel 1 goto :install_failed
call :copy_source_directory "pgvztool"
if errorlevel 1 goto :install_failed
call :copy_source_directory "gui"
if errorlevel 1 goto :install_failed

echo.
echo Done. Start the game, then open http://localhost:58080 in browser.
pause >nul
exit /b 0

:install_failed
echo.
echo Installation failed. Other mods outside PGvZ-TAS were not removed.
pause >nul
exit /b 1

:target_directory_failed
echo ERROR: could not create mods directory:
echo   %TARGET%
goto :install_failed

:installer_inside_target
echo ERROR: run this installer from the extracted release directory,
echo not from inside the target mods directory.
goto :install_failed

:require_source_file
if exist "%~dp0%~1" exit /b 0
echo ERROR: %~1 not found in the installer directory
exit /b 1

:require_source_directory
if exist "%~dp0%~1\" exit /b 0
echo ERROR: %~1 directory not found in the installer directory
exit /b 1

:copy_source_file
echo Copying %~1 ...
copy /Y "%~dp0%~1" "%TARGET%\" >nul 2>&1
if errorlevel 1 goto :copy_source_file_failed
echo   OK
exit /b 0

:copy_source_file_failed
echo   FAILED: could not copy %~1
exit /b 1

:copy_source_directory
echo Copying %~1 ...
xcopy /E /I /Y "%~dp0%~1" "%TARGET%\%~1\" >nul 2>&1
if errorlevel 1 goto :copy_source_directory_failed
echo   OK
exit /b 0

:copy_source_directory_failed
echo   FAILED: could not copy %~1 directory
exit /b 1

:disable_legacy_entry
if not exist "%TARGET%\%~1" exit /b 0

set "DISABLED_NAME=%~1.disabled"
if not exist "%TARGET%\%DISABLED_NAME%" goto :move_legacy_entry

:find_disabled_name
set "DISABLED_NAME=%~1.%RANDOM%.disabled"
if exist "%TARGET%\%DISABLED_NAME%" goto :find_disabled_name

:move_legacy_entry
echo Disabling old top-level %~1 ...
move "%TARGET%\%~1" "%TARGET%\%DISABLED_NAME%" >nul 2>&1
if errorlevel 1 goto :disable_legacy_entry_failed
echo   OK: renamed to %DISABLED_NAME%
exit /b 0

:disable_legacy_entry_failed
echo   FAILED: could not rename %~1
exit /b 1

:remove_old_file
if not exist "%TARGET%\%~1" exit /b 0
echo Removing old %~1 ...
del /F /Q "%TARGET%\%~1" >nul 2>&1
if exist "%TARGET%\%~1" goto :remove_old_file_failed
echo   OK
exit /b 0

:remove_old_file_failed
echo   FAILED: could not remove %~1
exit /b 1

:remove_old_directory
if not exist "%TARGET%\%~1\" exit /b 0
echo Removing old %~1 directory ...
rmdir /S /Q "%TARGET%\%~1" >nul 2>&1
if exist "%TARGET%\%~1\" goto :remove_old_directory_failed
echo   OK
exit /b 0

:remove_old_directory_failed
echo   FAILED: could not remove %~1 directory
exit /b 1
