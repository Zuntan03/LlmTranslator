@echo off
pushd %~dp0KoboldCpp\
if not exist .\wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin (
	echo https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-SuperHOT-8K-GGML/
	curl -LO https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-SuperHOT-8K-GGML/resolve/main/wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin
