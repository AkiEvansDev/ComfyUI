@echo off
cd /d "%~dp0"

git pull
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt