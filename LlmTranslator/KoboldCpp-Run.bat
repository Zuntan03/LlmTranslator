@echo off

pushd %~dp0
call .\KoboldCpp-Install.bat
popd

pushd %~dp0..\KoboldCpp\
set /p "KOBOLD_CPP_OPTION=" < ..\KoboldCppOption.txt
echo koboldcpp.exe %KOBOLD_CPP_OPTION% %*
.\koboldcpp.exe %KOBOLD_CPP_OPTION% %*
popd
