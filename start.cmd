@echo off
cd /d "%~dp0"

rem Intel OpenMP keeps its worker threads spinning for 200ms after every parallel CPU op. On a desktop
rem that is seven cores of pure heat per sampling step, and turning it off costs nothing in throughput.
set KMP_BLOCKTIME=0

call venv\Scripts\activate

rem boot.py stops CUDA busy-waiting, then runs main.py itself. See the comment at the top of it.
python boot.py --disable-dynamic-vram --windows-standalone-build --port 8188 --front-end-version Comfy-Org/ComfyUI_frontend@latest
pause