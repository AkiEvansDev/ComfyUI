@echo off
cd /d "%~dp0"

git pull
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python main.py --disable-dynamic-vram --windows-standalone-build --port 8188 --front-end-version Comfy-Org/ComfyUI_frontend@latest
pause