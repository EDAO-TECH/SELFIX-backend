@echo off
title SELFIX USB Installer
echo.
echo ====================================================
echo       🛡️  SELFIX - Cyber Healing USB Tool
echo ====================================================
echo.

:: Move to the directory where this script is located
cd /d %~dp0

:: Check if bash is available (Git Bash, WSL, or MSYS2)
where bash >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERROR: Bash shell not found on this system.
    echo.
    echo 👉 Please install Git Bash (https://git-scm.com/downloads)
    echo    or enable WSL (Windows Subsystem for Linux).
    echo.
    pause
    exit /b 1
)

:: Optional: Check if install.sh exists
if not exist install.sh (
    echo ❌ ERROR: install.sh not found in current directory.
    echo 👉 Make sure this USB contains SELFIX properly.
    pause
    exit /b 1
)

:: Launch the Linux installer script
echo ✅ Bash detected. Launching SELFIX installer...
bash install.sh

echo.
echo 🎉 SELFIX installation completed (if no errors).
pause
