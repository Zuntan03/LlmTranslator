@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/Airoboros-7B-GPT4-1-4-SuperHOT-8K-GGML/
if not exist .\airoboros-7b-gpt4-1.4-superhot-8k.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/Airoboros-7B-GPT4-1-4-SuperHOT-8K-GGML/resolve/main/airoboros-7b-gpt4-1.4-superhot-8k.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat --linearrope airoboros-7b-gpt4-1.4-superhot-8k.ggmlv3.q4_K_M.bin
