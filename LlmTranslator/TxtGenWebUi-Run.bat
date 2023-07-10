@echo off

pushd %~dp0
call .\TxtGenWebUi-Install.bat
popd

pushd %~dp0..
set /p "TXT_GEN_WEB_UI_OPTION=" < .\TxtGenWebUiOption.txt
set OOBABOOGA_FLAGS=%TXT_GEN_WEB_UI_OPTION% %*

pushd TxtGenWebUi\
	call .\start_windows.bat
popd

popd
