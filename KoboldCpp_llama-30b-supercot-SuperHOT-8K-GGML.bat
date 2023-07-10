@echo off
pushd %~dp0KoboldCpp\
if not exist .\llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin (
	echo https://huggingface.co/TheBloke/llama-30b-supercot-SuperHOT-8K-GGML/
	curl -LO https://huggingface.co/TheBloke/llama-30b-supercot-SuperHOT-8K-GGML/resolve/main/llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin
