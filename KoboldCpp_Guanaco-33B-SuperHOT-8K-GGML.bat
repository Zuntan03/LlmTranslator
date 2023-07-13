@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/Guanaco-33B-SuperHOT-8K-GGML/
if not exist .\guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/Guanaco-33B-SuperHOT-8K-GGML/resolve/main/guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat --linearrope guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin
