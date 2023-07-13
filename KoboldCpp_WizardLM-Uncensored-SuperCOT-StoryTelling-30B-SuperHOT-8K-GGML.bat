@echo off
pushd %~dp0KoboldCpp\
echo https://huggingface.co/TheBloke/WizardLM-Uncensored-SuperCOT-StoryTelling-30B-SuperHOT-8K-GGML/
if not exist .\WizardLM-Uncensored-SuperCOT-StoryTelling-30b-superhot-8k.ggmlv3.q4_0.bin (
	curl -LO https://huggingface.co/TheBloke/WizardLM-Uncensored-SuperCOT-StoryTelling-30B-SuperHOT-8K-GGML/resolve/main/WizardLM-Uncensored-SuperCOT-StoryTelling-30b-superhot-8k.ggmlv3.q4_0.bin
)
popd

call %~dp0LlmTranslator\KoboldCpp-Run.bat --linearrope WizardLM-Uncensored-SuperCOT-StoryTelling-30b-superhot-8k.ggmlv3.q4_0.bin
