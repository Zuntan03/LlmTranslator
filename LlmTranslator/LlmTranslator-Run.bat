@echo off
pushd %~dp0

set EASYNMT_CACHE=%~dp0cache
set HUGGINGFACE_HUB_CACHE=%~dp0cache

call .\venv\Scripts\activate.bat
python %* .\LlmTranslator.py

popd
