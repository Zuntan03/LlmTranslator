@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/Nous-Hermes-13B-GGML/
if not exist .\nous-hermes-13b.ggmlv3.q4_K_M.bin (
	curl -LO https://huggingface.co/TheBloke/Nous-Hermes-13B-GGML/resolve/main/nous-hermes-13b.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat nous-hermes-13b.ggmlv3.q4_K_M.bin
