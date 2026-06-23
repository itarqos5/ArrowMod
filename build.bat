@echo off
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
set "BUILDS_DIR=%PROJECT_DIR%builds"
set "FAIL=0"

echo ========================================
echo  Arrow ^& Slots - Build Script
echo ========================================
echo.

REM Use wrapper if available, otherwise system gradle
if exist "%PROJECT_DIR%gradlew.bat" (
    set "GRADLE=%PROJECT_DIR%gradlew.bat"
) else (
    set "GRADLE=gradle"
)

echo [1/2] Building subprojects...
echo.

for %%M in (fabric neoforge paper) do (
    if "%%M"=="fabric" (
        set "TASK=remapJar"
    ) else (
        set "TASK=jar"
    )
    call "%GRADLE%" :%%M:!TASK! --no-daemon --warning-mode summary
    if errorlevel 1 (
        echo   [WARN] %%M FAILED
        set "FAIL=1"
    ) else (
        echo   [OK] %%M
    )
    echo.
)

echo [2/2] Copying jars to builds\...
echo.

if not exist "%BUILDS_DIR%" mkdir "%BUILDS_DIR%"

for %%M in (fabric neoforge paper) do (
    if exist "%PROJECT_DIR%%%M\build\libs" (
        for %%F in ("%PROJECT_DIR%%%M\build\libs\*.jar") do (
            echo "%%~nxF" | findstr /i "_dev" >nul
            if errorlevel 1 (
                echo   %%~nxF
                copy /y "%%F" "%BUILDS_DIR%\" >nul
            )
        )
    )
)

echo.
if "%FAIL%"=="1" (
    echo Finished with errors. Check output above.
) else (
    echo All builds succeeded.
)
echo.
echo Artifacts in builds\:
for %%F in ("%BUILDS_DIR%\*.jar") do echo   %%~nxF
echo.

endlocal
