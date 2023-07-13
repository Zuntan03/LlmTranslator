@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/airoboros-65B-gpt4-1.4-GGML/
if not exist .\airoboros-65b-gpt4-1.4.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/airoboros-65B-gpt4-1.4-GGML/resolve/main/airoboros-65b-gpt4-1.4.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat airoboros-65b-gpt4-1.4.ggmlv3.q4_K_M.bin
