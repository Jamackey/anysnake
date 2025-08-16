@echo off
REM Build and upload anysnake package to PyPI

REM Step 1: Clean previous builds
echo Cleaning previous builds...
rmdir /s /q dist

REM Step 2: Build the package
echo Building the package...
python -m build --wheel

REM Step 3: Upload to PyPI
echo Uploading to PyPI...
python -m twine upload dist/*

echo Done!
pause
