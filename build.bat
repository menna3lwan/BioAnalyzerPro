@echo off
title BioAnalyzer Pro - Build Executable
color 0A

echo ============================================
echo    BioAnalyzer Pro - Build Executable
echo ============================================
echo.

echo This will create a standalone .exe file
echo No Python needed to run the final executable!
echo.
pause

echo.
echo [Step 1/4] Installing PyInstaller...
python -m pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    pause
    exit /b 1
)
echo Done!

echo.
echo [Step 2/4] Preparing files...
if not exist main.py (
    echo ERROR: main.py not found!
    echo Please make sure you're in the correct directory.
    pause
    exit /b 1
)
echo Files OK!

echo.
echo [Step 3/4] Building executable...
echo This may take 3-5 minutes...
echo.
python build_exe.py
if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo [Step 4/4] Creating distribution package...
if exist BioAnalyzerPro_Portable.zip del BioAnalyzerPro_Portable.zip
powershell Compress-Archive -Path dist/* -DestinationPath BioAnalyzerPro_Portable.zip
echo.

echo ============================================
echo    BUILD COMPLETE!
echo ============================================
echo.
echo Your files are ready:
echo   - dist/BioAnalyzerPro.exe  (Executable)
echo   - BioAnalyzerPro_Portable.zip (For distribution)
echo.
echo You can now:
echo   1. Run dist/BioAnalyzerPro.exe to test
echo   2. Share BioAnalyzerPro_Portable.zip with others
echo.
pause

echo.
echo Opening dist folder...
explorer dist
