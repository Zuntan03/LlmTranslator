@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/airoboros-7B-gpt4-1.4-GGML/
if not exist .\airoboros-7b-gpt4-1.4.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/airoboros-7B-gpt4-1.4-GGML/resolve/main/airoboros-7b-gpt4-1.4.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat airoboros-7b-gpt4-1.4.ggmlv3.q4_K_M.bin
