@echo off
pushd %~dp0

python --version | findstr "3.10.6" || (
	echo [ERROR] Invalid python version. require 3.10.6.
	python --version
	echo Ctrl + Click: https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe
	pause
	exit
)

where git
if %ERRORLEVEL% neq 0 (
	echo [ERROR] git not found. require Git for Windows.
	echo Ctrl + Click: https://gitforwindows.org/
	pause
	exit
)

git clone https://github.com/Zuntan03/LlmTranslator
robocopy .\LlmTranslator\ . /s /move

call LlmTranslator\LlmTranslator-Install.bat
call LlmTranslator\KoboldCpp-Install.bat
start LlmTranslator\LlmTranslator-Run.bat

popd
del %~dp0%~n0%~x0
