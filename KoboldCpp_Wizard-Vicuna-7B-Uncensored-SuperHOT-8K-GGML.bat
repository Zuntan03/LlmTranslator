@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-SuperHOT-8K-GGML/
if not exist .\wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/Wizard-Vicuna-7B-Uncensored-SuperHOT-8K-GGML/resolve/main/wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat --linearrope wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin
