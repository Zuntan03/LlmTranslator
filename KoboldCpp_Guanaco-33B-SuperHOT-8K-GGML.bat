@echo off
pushd %~dp0KoboldCpp\
if not exist .\guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin (
	echo https://huggingface.co/TheBloke/Guanaco-33B-SuperHOT-8K-GGML/
	curl -LO https://huggingface.co/TheBloke/Guanaco-33B-SuperHOT-8K-GGML/resolve/main/guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin
