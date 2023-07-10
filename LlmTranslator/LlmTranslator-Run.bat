@echo off
pushd %~dp0

call .\venv\Scripts\activate.bat
python %* .\LlmTranslator.py

popd
