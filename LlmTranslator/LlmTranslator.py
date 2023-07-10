from configparser import ConfigParser
from easynmt import EasyNMT
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
import time, locale, webbrowser
import darkdetect, pywinctl, pyperclip, pyautogui

# Code config
nmtEnabled = True  # for UI development
reprClipboard = False
windowAfterTime = 20

# .ini config
configFilePath = "LlmTranslator.ini"
config = ConfigParser()
config.add_section("general")
config.add_section("ui")
config.read(configFilePath)

# mbart50_m2m, mbart50_m2en
m2enModelName = config.get("general", "m2en_model_name", fallback="mbart50_m2m")
# mbart50_m2m, mbart50_en2m
en2mModelName = config.get("general", "en2m_model_name", fallback="mbart50_m2m")
nmtDevice = config.get("general", "nmt_device", fallback="cuda")  # cuda, cpu
nmtMaxLength = config.getint("general", "nmt_max_length", fallback=8192)
m2mTest = config.getboolean("general", "m2m_test", fallback=False)

recvKey = config.get("ui", "recv_key", fallback="F2")
generateKey = config.get("ui", "generate_key", fallback="F3")
deleteKey = config.get("ui", "delete_key", fallback="F4")
regenerateKey = config.get("ui", "regenerate_key", fallback="F5")

forceDark = config.getboolean("ui", "force_dark", fallback=False)
darkColFg = config.get("ui", "dark_col_fg", fallback="#CCCCCC")
darkColFgSelect = config.get("ui", "dark_col_fg_select", fallback="#FFFFFF")
darkColBg = config.get("ui", "dark_col_bg", fallback="#222222")
darkColBgSelect = config.get("ui", "dark_col_bg_select", fallback="#555555")


def saveConfig():
    config["general"]["lang"] = lang
    if not m2mTest:
        config["general"]["m2en_model_name"] = m2enModelName
        config["general"]["en2m_model_name"] = en2mModelName
    config["general"]["nmt_device"] = nmtDevice
    config["general"]["nmt_max_length"] = str(nmtMaxLength)
    config["general"]["m2m_test"] = str(m2mTest)
    config["ui"]["recv_key"] = recvKey
    config["ui"]["generate_key"] = generateKey
    config["ui"]["delete_key"] = deleteKey
    config["ui"]["regenerate_key"] = regenerateKey
    config["ui"]["win_width"] = str(window.winfo_width())
    config["ui"]["win_height"] = str(window.winfo_height())
    config["ui"]["win_x"] = str(window.winfo_x())
    config["ui"]["win_y"] = str(window.winfo_y())
    config["ui"]["text_spacing"] = str(textSpacing)
    config["ui"]["en_out_height"] = str(enOutHeightUiInt.get())
    config["ui"]["input_height"] = str(inputHeightUiInt.get())
    config["ui"]["force_dark"] = str(forceDark)
    config["ui"]["dark_col_fg"] = darkColFg
    config["ui"]["dark_col_fg_select"] = darkColFgSelect
    config["ui"]["dark_col_bg"] = darkColBg
    config["ui"]["dark_col_bg_select"] = darkColBgSelect
    with open(configFilePath, "w") as configfile:
        config.write(configfile)


# Mode
def removeLlmHeader(txt, headers):
    result = txt
    for header in headers:
        headerIndex = result.find(header)
        if headerIndex != -1:
            result = result[headerIndex + len(header) :]
            break
    return result


def removeLlmFooter(txt, footers):
    result = txt
    for footer in footers:
        footerIndex = result.rfind(footer)
        if footerIndex != -1:
            result = result[:footerIndex]
            break
    return result


def removeOldLlmMessages(txt):
    result = txt
    while len(llmMessages) > 0:
        message = llmMessages[-1]
        messageIndex = result.rfind(message)
        if messageIndex != -1:
            result = result[messageIndex + len(message) :]
            break
        else:
            llmMessages.pop()
    return result


def extractKoboldCppMessage(txt):
    headers = [
        "Enter a prompt below to begin!\r\nOr, select a Quick Start Scenario by clicking here.\r\n",
        "New Game\r\nScenarios\r\nSave\r\nLoad\r\nSettings\r\nShare\r\nConnected to Custom Endpoint\r\n",
    ]
    result = removeLlmHeader(txt, headers)
    footers = [
        "Enter Sends\r\n\r\nAllow Editing\r\n",
        "Enter text here\r\n",
        "Type a message\r\n\r\n",
        "You're using Kobold Lite Embedded.",
        "Last request served by Custom Endpoint",
    ]
    result = removeLlmFooter(result, footers)

    while len(llmMessages) > 0:
        message = llmMessages[-1]
        messageIndex = result.rfind(message)
        if messageIndex != -1:
            result = result[messageIndex + len(message) :]
            break
        else:
            llmMessages.pop()
    return result.strip()


def generateKoboldCpp():
    pyautogui.press("tab")
    pyautogui.press("space")
    pyautogui.hotkey("shift", "tab")


def deleteKoboldCpp():
    for _ in range(5):
        pyautogui.hotkey("shift", "tab")
    if adventureUiBool.get():
        pyautogui.hotkey("shift", "tab")
        pyautogui.press("space")
        pyautogui.press("tab")
    else:
        pyautogui.press("space")
    for _ in range(5):
        pyautogui.press("tab")


def regenerateKoboldCpp():
    for _ in range(3):
        pyautogui.hotkey("shift", "tab")
    if adventureUiBool.get():
        pyautogui.hotkey("shift", "tab")
        pyautogui.press("space")
        pyautogui.press("tab")
    else:
        pyautogui.press("space")
    for _ in range(3):
        pyautogui.press("tab")


def extractTxtGenWebUiMessage(txt):
    headers = [
        "Text generation\r\nChat settings\r\nParameters\r\nModel\r\nTraining\r\nInterface mode\r\n",
        "Raw\r\nMarkdown\r\nHTML\r\n",
    ]
    result = removeLlmHeader(txt, headers)
    footers = [
        "Input\r\n",
        "gallery\r\nCharacter gallery\r\n",
    ]
    result = removeLlmFooter(result, footers)
    while len(llmMessages) > 0:
        message = llmMessages[-1]
        messageIndex = result.rfind(message)
        if messageIndex != -1:
            result = result[:messageIndex]
            break
        else:
            llmMessages.pop()
    return result.strip()


def generateTxtGenWebUi():
    pyautogui.press("tab")
    pyautogui.press("tab")
    pyautogui.press("space")
    pyautogui.hotkey("shift", "tab")
    pyautogui.hotkey("shift", "tab")


def deleteTxtGenWebUi():
    for _ in range(6):
        pyautogui.press("tab")
    pyautogui.press("space")
    for _ in range(6):
        pyautogui.hotkey("shift", "tab")
    # Ctrl+A > Del?


def regenerateTxtGenWebUi():
    for _ in range(5):
        pyautogui.press("tab")
    pyautogui.press("space")
    for _ in range(5):
        pyautogui.hotkey("shift", "tab")


detectLlmName = "Detect LLM"
koboldCppName = "KoboldCpp"
txtGenWebUiName = "TxtGenWebUi"
modes = {
    detectLlmName: {"name": detectLlmName},
    koboldCppName: {
        "name": koboldCppName,
        "detectWindowTitle": "KoboldAI Lite",
        "extractMessage": extractKoboldCppMessage,
        "generate": generateKoboldCpp,
        "delete": deleteKoboldCpp,
        "regenerate": regenerateKoboldCpp,
    },
    txtGenWebUiName: {
        "name": txtGenWebUiName,
        "detectWindowTitle": "Text generation web UI",
        "extractMessage": extractTxtGenWebUiMessage,
        "generate": generateTxtGenWebUi,
        "delete": deleteTxtGenWebUi,
        "regenerate": regenerateTxtGenWebUi,
    },
}
detectLlmMode = modes[detectLlmName]
koboldCppMode = modes[koboldCppName]

modeNames = list(modes.keys())
mode = detectLlmMode

llmMessages = []
window = tk.Tk()
modeUiStr = tk.StringVar(value=mode["name"])
adventureUiBool = tk.BooleanVar(value=True)


def setMode(newMode):
    global mode
    if mode == newMode:
        return
    print(f"{mode['name']} > {newMode['name']}")
    mode = newMode
    modeUiStr.set(mode["name"])
    llmMessages.clear()
    if mode == koboldCppMode:
        mOutTxt.insert(tk.END, endWithNewline(l10n["infoKoboldCpp"]))
        mOutTxt.see(tk.END)
        adventureCheck.pack(side=tk.LEFT, padx=padX, pady=padY)
    else:
        adventureCheck.pack_forget()


def detectMode():
    if mode != detectLlmMode:
        return True
    for m in modes.values():
        if "detectWindowTitle" in m:
            windows = pywinctl.getWindowsWithTitle(
                m["detectWindowTitle"], condition=pywinctl.Re.CONTAINS
            )
            if len(windows) > 0:
                setMode(m)
                return True
    return False


def checkModeWindow():
    if "detectWindowTitle" in mode:
        windows = pywinctl.getWindowsWithTitle(
            mode["detectWindowTitle"], condition=pywinctl.Re.CONTAINS
        )
        return len(windows) > 0
    return False


def activeteModeWindow():
    if "detectWindowTitle" in mode:
        windows = pywinctl.getWindowsWithTitle(
            mode["detectWindowTitle"], condition=pywinctl.Re.CONTAINS
        )
        if len(windows) > 0:
            return windows[0].activate(wait=True)
    return False


# EasyNMT
if m2mTest:
    m2enModelName = "mbart50_m2en"
    en2mModelName = "mbart50_en2m"
    m2mModelName = "mbart50_m2m"
    print(f"{m2mModelName}: Loading...")
    start_time = time.perf_counter()
    m2mNmt = EasyNMT(m2mModelName, device=nmtDevice) if nmtEnabled else None
    print(f"{m2mModelName}: Loaded {(time.perf_counter() - start_time):.1f}sec")

print(f"{m2enModelName}: Loading...")
start_time = time.perf_counter()
m2enNmt = EasyNMT(m2enModelName, device=nmtDevice) if nmtEnabled else None
print(f"{m2enModelName}: Loaded {(time.perf_counter() - start_time):.1f}sec")

if m2enModelName == en2mModelName:
    en2mNmt = m2enNmt
else:
    print(f"{en2mModelName}: Loading...")
    start_time = time.perf_counter()
    en2mNmt = EasyNMT(en2mModelName, device=nmtDevice) if nmtEnabled else None
    print(f"{en2mModelName}: Loaded {(time.perf_counter() - start_time):.1f}sec")


def translateEn(mTxt):
    if not nmtEnabled:
        return mTxt
    # st = time.perf_counter()
    enTxt = m2enNmt.translate(
        mTxt, source_lang=lang, target_lang="en", max_length=nmtMaxLength
    )
    # print(f"en[{len(enTxt)}] > {lang}[{len(mTxt)}] {(time.perf_counter() - st):.1f}sec")
    # print(f"{repr(enTxt)}\n{repr(mTxt)}")

    if m2mTest:
        enTxt = f"\n[m2en]\n{enTxt}\n[m2m]\n" + m2mNmt.translate(
            mTxt, source_lang=lang, target_lang="en", max_length=nmtMaxLength
        )
    return enTxt


def translateM(enTxt):
    if not nmtEnabled:
        return enTxt
    # st = time.perf_counter()
    mTxt = en2mNmt.translate(
        enTxt, source_lang="en", target_lang=lang, max_length=nmtMaxLength
    )
    # print(f"{lang}[{len(mTxt)}] > en[{len(enTxt)}] {(time.perf_counter() - st):.1f}sec")
    # print(f"{repr(mTxt)}\n{repr(enTxt)}")

    if m2mTest:
        mTxt = f"\n[en2m]\n{mTxt}\n[m2m]\n" + m2mNmt.translate(
            enTxt, source_lang="en", target_lang=lang, max_length=nmtMaxLength
        )
    return mTxt


# Localization
lang = locale.getdefaultlocale()[0][:2]
lang = config.get("general", "lang", fallback=lang)
# lang = "zh"  # Debug

l10n = {
    "title": f"LLM Translator [Input&Enter]Translate>LLM, [Empty&Enter|{recvKey}]LLM>Translate, [Shift+Enter]NewLine",
    "llm": "LLM",
    "sendLlm": "Send",
    "recvLlm": "Receive",
    "generateLlm": "Generate",
    "deleteLlm": "Delete",
    "regenerateLlm": "Regenerate",
    "translation": "Translation",
    "m2en": ">[en]",
    "en2m": f">[{lang}]",
    "watchClipboard": "Watch clipboard",
    "relatedSites": "Related sites",
    "officialSite": "Official site",
    "inputLabel": "Input",
    "lines": "lines",
    "txtClear": "Clear",
    "llmNotFound": "Click on the blank input field for LLM and then use the input field below this field.",
    "infoKoboldCpp": 'For "Delete" and "Regenerate" to work properly, check "Adventure" at the bottom if you are in Adventure mode, or select "Edit" from the KoboldCpp gear icon after a conversation if you are in Chat mode.',
}

if lang == "ja":
    l10n = {
        "title": "AIチャット翻訳 [入力&Enter]英訳してLLM, [空欄&Enter|F2]LLMから和訳, [Shift+Enter]改行",
        "llm": "AIチャット",
        "sendLlm": "送信",
        "recvLlm": "受信",
        "generateLlm": "生成",
        "deleteLlm": "削除",
        "regenerateLlm": "再生成",
        "translation": "翻訳",
        "m2en": "英訳",
        "en2m": "和訳",
        "watchClipboard": "クリップボード和訳",
        "relatedSites": "関連サイト",
        "officialSite": "公式サイト",
        "inputLabel": "入力",
        "lines": "行",
        "txtClear": "クリア",
        "llmNotFound": "空欄にしたAIチャットの入力欄をクリックしてから、下の入力欄を利用します。",
        "infoKoboldCpp": "「削除」と「再生成」を正常に動作させるために、アドベンチャーモードなら一番下の「Adventure」をチェックし、チャットモードなら会話後にKoboldCppの歯車アイコンから「Edit」を選択してください。",
    }
else:
    for key in l10n.keys():
        l10n[key] = translateM(l10n[key])

# Watch clipboard
clipboardValue = ""
watchClipboard = False
watchClipboardUiBool = tk.BooleanVar(value=watchClipboard)
pollClipboardIntervalMs = 100


def setWatchClipboard(val):
    global watchClipboard
    print(f"Watch clipboard: {watchClipboard} > {val}")
    if (not watchClipboard) and val:
        print("Watch Start")
        window.after(pollClipboardIntervalMs, pollClipboard)
    watchClipboard = val


def endWithNewline(text):
    return text if text.endswith("\n") else text + "\n"


def pollClipboard():
    global clipboardValue
    newClipboardValue = pyperclip.paste()
    if newClipboardValue != clipboardValue:
        enOutTxt.insert(tk.END, endWithNewline(newClipboardValue))
        enOutTxt.see(tk.END)
        clipboardValue = newClipboardValue
        window.after(windowAfterTime, translateClipboard)
    elif watchClipboard:
        window.after(pollClipboardIntervalMs, pollClipboard)


def translateClipboard():
    if reprClipboard:
        print(repr(clipboardValue))
    mTxt = translateM(clipboardValue)
    mOutTxt.insert(tk.END, endWithNewline(mTxt))
    mOutTxt.see(tk.END)
    if watchClipboard:
        window.after(pollClipboardIntervalMs, pollClipboard)


# Translate event
def onEn2MTranslate(enTxt):
    mTxt = translateM(enTxt)
    mOutTxt.insert(tk.END, endWithNewline(mTxt))
    mOutTxt.see(tk.END)
    return mTxt


def onEn2M():
    enTxt = inputTxt.get("1.0", "end-1c")
    if enTxt:
        inputTxt.delete("1.0", tk.END)
        enOutTxt.insert(tk.END, endWithNewline(enTxt))
        enOutTxt.see(tk.END)
        window.after(windowAfterTime, onEn2MTranslate, enTxt)


def onM2EnTranslate(mTxt):
    enTxt = translateEn(mTxt)
    enOutTxt.insert(tk.END, endWithNewline(enTxt))
    enOutTxt.see(tk.END)
    return enTxt


def onM2En():
    mTxt = inputTxt.get("1.0", "end-1c")
    if mTxt:
        inputTxt.delete("1.0", tk.END)
        mOutTxt.insert(tk.END, endWithNewline(mTxt))
        mOutTxt.see(tk.END)
        window.after(windowAfterTime, onM2EnTranslate, mTxt)


def onSendLlmTranslate(mTxt):
    global clipboardValue
    enTxt = onM2EnTranslate(mTxt)
    if activeteModeWindow():
        clipboardValue = enTxt
        pyperclip.copy(clipboardValue)
        pyautogui.hotkey("ctrl", "v")
        mode["generate"]()  # pyautogui.press("enter")
        pyautogui.hotkey("alt", "tab")
        inputTxt.delete("1.0", tk.END)

        enTxt = enTxt.strip()
        if len(enTxt) > 0:
            llmMessages.append(enTxt)

        # TODO: SdWebUI連携

    else:
        mOutTxt.insert(tk.END, endWithNewline(l10n["llmNotFound"]))
        mOutTxt.see(tk.END)


def onSendLlm():
    if (not detectMode()) or (not checkModeWindow()):
        mOutTxt.insert(tk.END, endWithNewline(l10n["llmNotFound"]))
        mOutTxt.see(tk.END)
        return
    mTxt = inputTxt.get("1.0", "end-1c")
    mOutTxt.insert(tk.END, endWithNewline(mTxt))
    mOutTxt.see(tk.END)
    window.after(windowAfterTime, onSendLlmTranslate, mTxt)


def onRecvLlm():
    global clipboardValue
    if (not detectMode()) or (not activeteModeWindow()):
        mOutTxt.insert(tk.END, endWithNewline(l10n["llmNotFound"]))
        mOutTxt.see(tk.END)
        return

    pyautogui.hotkey("shift", "tab")
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    pyautogui.press("tab")
    pyautogui.hotkey("alt", "tab")
    clipboardValue = pyperclip.paste()
    message = mode["extractMessage"](clipboardValue)
    if len(message) == 0:
        return
    llmMessages.append(message)
    enOutTxt.insert(tk.END, endWithNewline(message))
    enOutTxt.see(tk.END)

    # TODO: SdWebUI連携

    window.after(windowAfterTime, onEn2MTranslate, message)


def onLlm(funcName):
    if (not detectMode()) or (not activeteModeWindow()):
        mOutTxt.insert(tk.END, endWithNewline(l10n["llmNotFound"]))
        mOutTxt.see(tk.END)
        return
    mode[funcName]()
    pyautogui.hotkey("alt", "tab")


def onInputTxtReturn(event):
    if event.state == 0:
        mTxt = inputTxt.get("1.0", "end-1c")
        if mTxt:
            onSendLlm()
        else:
            onRecvLlm()
        return "break"


# UI
padX = 4
padY = 2
textSpacing = config.getint("ui", "text_spacing", fallback=4)

# Window
winMinW = 400
winMinH = 400
window.title(l10n["title"])
window.minsize(winMinW, winMinH)
winWidth = config.get("ui", "win_width", fallback=str(winMinW * 2))
winHeight = config.get("ui", "win_height", fallback=str(winMinH * 2))
winX = config.get("ui", "win_x", fallback="None")
if winX == "None":
    window.geometry(f"{winWidth}x{winHeight}")
else:
    winY = config.get("ui", "win_y", fallback="100")
    window.geometry(f"{winWidth}x{winHeight}+{winX}+{winY}")

# Menu
menuBar = tk.Menu(window)
window.config(menu=menuBar)

llmMenu = tk.Menu(window, tearoff=False)
menuBar.add_cascade(label=l10n["llm"], menu=llmMenu)
llmMenu.add_cascade(label=f"{l10n['sendLlm']} [Input&Enter]", command=onSendLlm)
llmMenu.add_cascade(
    label=f"{l10n['recvLlm']} [Empty&Enter|{recvKey}]", command=onRecvLlm
)
llmMenu.add_cascade(
    label=f"{l10n['generateLlm']} [{generateKey}]", command=lambda: onLlm("generate")
)
llmMenu.add_cascade(
    label=f"{l10n['deleteLlm']} [{deleteKey}]", command=lambda: onLlm("delete")
)
llmMenu.add_cascade(
    label=f"{l10n['regenerateLlm']} [{regenerateKey}]",
    command=lambda: onLlm("regenerate"),
)

translationMenu = tk.Menu(window, tearoff=False)
menuBar.add_cascade(label=l10n["translation"], menu=translationMenu)
translationMenu.add_cascade(label=f"{l10n['m2en']} [Ctrl+E]", command=onM2En)
translationMenu.add_cascade(label=f"{l10n['en2m']} [Ctrl+W]", command=onEn2M)
translationMenu.add_checkbutton(
    label=l10n["watchClipboard"],
    variable=watchClipboardUiBool,
    command=lambda: setWatchClipboard(watchClipboardUiBool.get()),
)

relatedSitesMenu = tk.Menu(window, tearoff=False)
menuBar.add_cascade(label=l10n["relatedSites"], menu=relatedSitesMenu)
relatedSitesMenu.add_cascade(
    label="KoboldCpp: Aether Room",
    command=lambda: webbrowser.open("https://aetherroom.club", 2),
)
relatedSitesMenu.add_cascade(
    label="TheBloke: Models",
    command=lambda: webbrowser.open(
        "https://huggingface.co/TheBloke?sort_models=downloads#models", 2
    ),
)
relatedSitesMenu.add_separator()
relatedSitesMenu.add_cascade(
    label="KoboldCpp",
    command=lambda: webbrowser.open("https://github.com/LostRuins/koboldcpp", 2),
)
relatedSitesMenu.add_cascade(
    label="Text generation web UI",
    command=lambda: webbrowser.open(
        "https://github.com/oobabooga/text-generation-webui", 2
    ),
)
relatedSitesMenu.add_separator()
relatedSitesMenu.add_cascade(
    label=l10n["officialSite"],
    command=lambda: webbrowser.open("https://github.com/Zuntan03/LlmTranslator", 2),
)

# enOut
enOutFrame = tk.Frame(window)

enOutHeightUiInt = tk.IntVar(
    value=int(config.get("ui", "en_out_height", fallback="10"))
)
enOutSpin = tk.Spinbox(
    enOutFrame,
    textvariable=enOutHeightUiInt,
    from_=1,
    to=99,
    increment=1,
    width=3,
    state="readonly",
    command=lambda: enOutTxt.configure(height=enOutHeightUiInt.get()),
)
enOutSpin.pack(side=tk.LEFT, padx=(padX, 0), pady=padY)

enOutLinesLabel = tk.Label(enOutFrame, text=l10n["lines"])
enOutLinesLabel.pack(side=tk.LEFT, padx=(0, padX), pady=padY)

clearButton = tk.Button(
    enOutFrame,
    text=l10n["txtClear"],
    command=lambda: (
        enOutTxt.delete("1.0", tk.END),
        mOutTxt.delete("1.0", tk.END),
        inputTxt.delete("1.0", tk.END),
        llmMessages.clear(),
    ),
)
clearButton.pack(side=tk.RIGHT, padx=padX, pady=padY)
enOutFrame.pack(fill=tk.X, padx=padX, pady=(padY * 2, padY))


enOutTxt = scrolledtext.ScrolledText(
    window,
    height=enOutHeightUiInt.get(),
    spacing1=textSpacing,
    spacing2=textSpacing,
    spacing3=textSpacing,
)
enOutTxt.pack(fill=tk.X, padx=padX * 2, pady=padY)

# mOut
mOutTxt = scrolledtext.ScrolledText(
    window, height=1, spacing1=textSpacing, spacing2=textSpacing, spacing3=textSpacing
)
mOutTxt.insert(tk.END, endWithNewline(l10n["llmNotFound"]))
mOutTxt.pack(fill=tk.BOTH, expand=True, padx=padX * 2, pady=padY)

# input
inputHeightUiInt = tk.IntVar(value=int(config.get("ui", "input_height", fallback="8")))
inputTxt = scrolledtext.ScrolledText(
    window,
    height=inputHeightUiInt.get(),
    spacing1=textSpacing,
    spacing2=textSpacing,
    spacing3=textSpacing,
)
inputTxt.pack(fill=tk.X, padx=padX * 2, pady=padY)
inputTxt.bind("<Return>", onInputTxtReturn)
inputTxt.bind("<Control-e>", lambda e: onM2En())
inputTxt.bind("<Control-w>", lambda e: onEn2M())
inputTxt.bind(f"<{recvKey}>", lambda e: onRecvLlm())
inputTxt.bind(f"<{generateKey}>", lambda e: onLlm("generate"))
inputTxt.bind(f"<{deleteKey}>", lambda e: onLlm("delete"))
inputTxt.bind(f"<{regenerateKey}>", lambda e: onLlm("regenerate"))
inputTxt.focus_set()

inputFrame = tk.Frame(window)
modeCombo = ttk.Combobox(
    inputFrame, values=modeNames, state="readonly", textvariable=modeUiStr, width=12
)
modeCombo.bind(
    "<<ComboboxSelected>>",
    lambda e: (modeCombo.select_clear(), setMode(modes[modeUiStr.get()])),
)
modeCombo.pack(side=tk.LEFT, padx=padX, pady=padY)

inputSpin = tk.Spinbox(
    inputFrame,
    textvariable=inputHeightUiInt,
    from_=1,
    to=99,
    increment=1,
    width=3,
    state="readonly",
    command=lambda: inputTxt.configure(height=inputHeightUiInt.get()),
)
inputSpin.pack(side=tk.LEFT, padx=(padX, 0), pady=padY)

inputLinesLabel = tk.Label(inputFrame, text=l10n["lines"])
inputLinesLabel.pack(side=tk.LEFT, padx=(0, padX), pady=padY)

adventureCheck = tk.Checkbutton(inputFrame, text="Adventure", variable=adventureUiBool)

watchClipboardCheck = tk.Checkbutton(
    inputFrame,
    text=l10n["watchClipboard"],
    variable=watchClipboardUiBool,
    command=lambda: setWatchClipboard(watchClipboardUiBool.get()),
)
watchClipboardCheck.pack(side=tk.RIGHT, padx=padX, pady=padY)

en2mButton = tk.Button(inputFrame, text=l10n["en2m"], command=onEn2M)
en2mButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

m2enButton = tk.Button(inputFrame, text=l10n["m2en"], command=onM2En)
m2enButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

regenerateButton = tk.Button(
    inputFrame, text=l10n["regenerateLlm"], command=lambda: onLlm("regenerate")
)
regenerateButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

deleteButton = tk.Button(
    inputFrame, text=l10n["deleteLlm"], command=lambda: onLlm("delete")
)
deleteButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

generateButton = tk.Button(
    inputFrame, text=l10n["generateLlm"], command=lambda: onLlm("generate")
)
generateButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

recvLlmButton = tk.Button(inputFrame, text=l10n["recvLlm"], command=onRecvLlm)
recvLlmButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

sendLlmButton = tk.Button(inputFrame, text=l10n["sendLlm"], command=onSendLlm)
sendLlmButton.pack(side=tk.RIGHT, padx=padX, pady=padY)

inputFrame.pack(fill=tk.X, padx=padX, pady=padY * 2)

# Dark
if forceDark or darkdetect.isDark():
    style = ttk.Style()
    style.theme_use("default")
    style.map("TCombobox", foreground=[("readonly", darkColFg)])
    style.map("TCombobox", fieldbackground=[("readonly", darkColBg)])
    style.map("TCombobox", selectbackground=[("readonly", "!focus", darkColBg)])

    darkColFgBg = {"fg": darkColFg, "bg": darkColBg}
    colSelect = darkColFgBg.copy()
    colSelect["selectforeground"] = darkColFgSelect
    colSelect["selectbackground"] = darkColBgSelect
    colActive = darkColFgBg.copy()
    colActive["activeforeground"] = darkColFgSelect
    colActive["activebackground"] = darkColBgSelect
    colCheck = colActive.copy()
    colCheck["selectcolor"] = darkColBg
    colTxt = colSelect.copy()
    colTxt["insertbackground"] = darkColFgSelect

    window.configure(bg=darkColBg)
    menuBar.configure(bg=darkColBg)

    enOutFrame.configure(bg=darkColBg)
    enOutSpin.configure(colSelect)
    enOutSpin.configure({"readonlybackground": darkColBg})
    enOutLinesLabel.configure(darkColFgBg)
    clearButton.configure(colActive)
    enOutTxt.configure(colTxt)

    mOutTxt.configure(colTxt)

    inputTxt.configure(colTxt)
    inputFrame.configure(bg=darkColBg)
    inputSpin.configure(colSelect)
    inputSpin.configure({"readonlybackground": darkColBg})
    inputLinesLabel.configure(darkColFgBg)
    adventureCheck.configure(colCheck)
    watchClipboardCheck.configure(colCheck)
    en2mButton.configure(colActive)
    m2enButton.configure(colActive)
    regenerateButton.configure(colActive)
    deleteButton.configure(colActive)
    generateButton.configure(colActive)
    recvLlmButton.configure(colActive)
    sendLlmButton.configure(colActive)


# Window finalize
def onClose():
    saveConfig()
    window.destroy()


window.after(windowAfterTime, saveConfig)
window.protocol("WM_DELETE_WINDOW", onClose)
window.lift()
window.mainloop()
