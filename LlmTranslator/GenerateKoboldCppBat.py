models = [
    (
        "airoboros-65B-gpt4-1.2-GGML",
        "airoboros-65B-gpt4-1.2.ggmlv3.q4_K_M.bin",
    ),
    (
        "airoboros-65B-gpt4-1.4-GGML",
        "airoboros-65b-gpt4-1.4.ggmlv3.q4_K_M.bin",
    ),
    (
        "Guanaco-33B-SuperHOT-8K-GGML",
        "guanaco-33b-superhot-8k.ggmlv3.q4_K_M.bin",
    ),
    (
        "llama-30b-supercot-SuperHOT-8K-GGML",
        "llama-30b-supercot-superhot-8k.ggmlv3.q4_K_M.bin",
    ),
    (
        "Nous-Hermes-13B-GGML",
        "nous-hermes-13b.ggmlv3.q4_K_M.bin",
    ),
    (
        "WizardLM-33B-V1.0-Uncensored-GGML",
        "wizardlm-33b-v1.0-uncensored.ggmlv3.q4_K_M.bin",
    ),
    (
        "WizardLM-Uncensored-SuperCOT-StoryTelling-30B-SuperHOT-8K-GGML",
        "WizardLM-Uncensored-SuperCOT-StoryTelling-30b-superhot-8k.ggmlv3.q4_0.bin",
    ),
    (
        "Wizard-Vicuna-7B-Uncensored-GGML",
        "Wizard-Vicuna-7B-Uncensored.ggmlv3.q4_K_M.bin",
    ),
    (
        "Wizard-Vicuna-7B-Uncensored-SuperHOT-8K-GGML",
        "wizard-vicuna-7b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin",
    ),
    (
        "Wizard-Vicuna-13B-Uncensored-GGML",
        "Wizard-Vicuna-13B-Uncensored.ggmlv3.q4_K_M.bin",
    ),
    (
        "Wizard-Vicuna-13B-Uncensored-SuperHOT-8K-GGML",
        "wizard-vicuna-13b-uncensored-superhot-8k.ggmlv3.q4_K_M.bin",
    ),
    (
        "Wizard-Vicuna-30B-Uncensored-GGML",
        "Wizard-Vicuna-30B-Uncensored.ggmlv3.q4_K_M.bin",
    ),
]

print()
for model in models:
    batScript = f"""@echo off
pushd %~dp0KoboldCpp\\
if not exist .\\{model[1]} (
\techo https://huggingface.co/TheBloke/{model[0]}/
\tcurl -LO https://huggingface.co/TheBloke/{model[0]}/resolve/main/{model[1]}
)
popd

call %~dp0LlmTranslator\\KoboldCpp-Run.bat {model[1]}
"""
    batFileName = f"KoboldCpp_{model[0]}.bat"
    with open(f"..\\{batFileName}", "w") as batFile:
        batFile.write(batScript)
    print(f"copy /Y .\\{batFileName} %DST%\\")
print()
