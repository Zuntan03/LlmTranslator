@echo off
pushd %~dp0..

if not exist .\KoboldCpp\ ( mkdir .\KoboldCpp )

pushd KoboldCpp
if not exist .\koboldcpp.exe (
	echo https://github.com/LostRuins/koboldcpp/
	curl -LO https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp.exe
)
popd

popd
