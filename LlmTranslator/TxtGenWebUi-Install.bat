@echo off
pushd %~dp0..

if not exist TxtGenWebUi\text-generation-webui\ (
	echo https://github.com/oobabooga/text-generation-webui/
	curl -LO https://github.com/oobabooga/text-generation-webui/releases/latest/download/oobabooga_windows.zip
	PowerShell -Version 5.1 -ExecutionPolicy Bypass Expand-Archive -Path .\oobabooga_windows.zip -DestinationPath .
	del .\oobabooga_windows.zip

	rename oobabooga_windows\ TxtGenWebUi
	pushd TxtGenWebUi\
		set OOBABOOGA_FLAGS=--chat --auto-launch
		rem A: NVIDIA, B: AMD, C: Apple M, D:CPU
		echo A|call .\start_windows.bat
	popd
)

popd
