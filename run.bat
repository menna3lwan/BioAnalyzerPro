@echo off
echo ============================================
echo    BioAnalyzer Pro - Quick Setup
echo ============================================
echo.

echo [1/3] Installing Dependencies...
python -m pip install pillow pandas numpy
echo.

echo [2/3] Checking files...
if exist main_fixed.py (
    echo     Found main_fixed.py
    if exist main.py (
        echo     Backing up old main.py...
        ren main.py main.py.backup
    )
    echo     Renaming main_fixed.py to main.py...
    ren main_fixed.py main.py
)
echo.

echo [3/3] Running application...
echo.
python main.py

echo.
echo ============================================
echo    Setup Complete!
echo ============================================
pause
