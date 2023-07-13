@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/llama-30b-supercot-SuperHOT-8K-GGML/
if not exist .\llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/llama-30b-supercot-SuperHOT-8K-GGML/resolve/main/llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat --linearrope llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin
