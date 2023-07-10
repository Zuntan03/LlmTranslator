@echo off
pushd %~dp0

if not exist .\venv\ ( python -m venv venv )

echo https://github.com/UKPLab/EasyNMT
echo https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt
echo https://huggingface.co/facebook/mbart-large-50-one-to-many-mmt
echo https://huggingface.co/facebook/mbart-large-50-many-to-one-mmt

call .\venv\Scripts\activate.bat
python.exe -m pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install --no-deps easynmt
pip install nltk transformers sentencepiece protobuf~=3.20.0
pip install darkdetect pywinctl pyperclip pyautogui
popd
