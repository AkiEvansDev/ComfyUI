@echo off
cd /d "%~dp0"

call venv\Scripts\activate

python main.py --disable-dynamic-vram --windows-standalone-build --port 8188 --front-end-version Comfy-Org/ComfyUI_frontend@latest
pause