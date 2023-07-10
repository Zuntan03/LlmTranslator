@echo off
pushd %~dp0KoboldCpp\
if not exist .\wizardlm-33b-v1.0-uncensored.ggmlv3.q4_K_M.bin (
	echo https://huggingface.co/TheBloke/WizardLM-33B-V1.0-Uncensored-GGML/
	curl -LO https://huggingface.co/TheBloke/WizardLM-33B-V1.0-Uncensored-GGML/resolve/main/wizardlm-33b-v1.0-uncensored.ggmlv3.q4_K_M.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat wizardlm-33b-v1.0-uncensored.ggmlv3.q4_K_M.bin
