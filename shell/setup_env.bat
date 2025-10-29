@echo off
py -3.13 -m venv venv
call venv\Scripts\activate
python -m pip install -U pip
pip install -r requirements.txt
