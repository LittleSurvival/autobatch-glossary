@echo off
REM Check if pip is installed
python -m pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Installing pip...
    python -m ensurepip
)

REM Install required libraries
echo Installing required libraries...
pip install -r requirements.txt