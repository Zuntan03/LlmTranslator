@echo off
pushd %~dp0KoboldCpp\
if not exist .\Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_K_M.bin (
	echo https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GGML/
	curl -LO https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-GGML/resolve/main/Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_K_M.bin
