@echo off
REM Prevent commands from being echoed to the terminal for a cleaner output

REM Check if the virtual environment folder 'venv' already exists
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    py -3.13 -m venv venv
) ELSE (
    echo Virtual environment already exists, skipping creation.
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Upgrade pip to the latest version inside the virtual environment
python -m pip install -U pip

REM Install all Python packages listed in the requirements.txt file
pip install -r requirements.txt

echo Virtual environment setup complete!
