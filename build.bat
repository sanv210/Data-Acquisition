@echo off
REM Quick build script for DAQ System .exe on Windows
REM Run this batch file from the project root directory

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo DAQ System - Quick Build Script
echo ============================================================
echo.

REM Check if venv is activated
if not defined VIRTUAL_ENV (
    echo WARNING: Virtual environment not activated!
    echo Please activate venv first:
    echo   .\venv\Scripts\Activate.ps1
    echo.
    pause
    exit /b 1
)

echo Virtual Environment: !VIRTUAL_ENV!
echo.

REM Check if PyInstaller is installed
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Building DAQ_System.exe...
echo.

REM Run the build script
python build_exe.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Build completed successfully!
echo ============================================================
echo.
echo Executable location:
echo   dist\DAQ_System\DAQ_System.exe
echo.
echo To run:
echo   dist\DAQ_System\DAQ_System.exe
echo.
pause
