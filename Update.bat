@echo off
pushd %~dp0

git pull

pushd .\LlmTranslator\
	call LlmTranslator-Install.bat
popd

if exist .\KoboldCpp\koboldcpp.exe (
	pushd .\KoboldCpp\
	del /Q .\koboldcpp.exe
	curl -LO https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp.exe
	popd
)

if exist .\TxtGenWebUi\update_windows.bat (
	pushd .\TxtGenWebUi\
	echo Y|call update_windows.bat
	popd
)

popd
