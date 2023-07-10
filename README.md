# AIチャット翻訳

ローカルPC で動作する英語版の AIチャット [KoboldCpp](https://github.com/LostRuins/koboldcpp) を、ローカル翻訳で [51言語](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt#languages-covered)から利用するツールです。  
チャットの内容はインターネットへ送信されませんので、自由なチャットを楽しめます。

This is a tool to use the English version of AI chat [KoboldCpp](https://github.com/LostRuins/koboldcpp) running on a local PC from [51 languages](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt#languages-covered) with local translation.  
Chat contents are not sent to the Internet, so you can enjoy chatting freely.

# 動作環境

- Windows 10 以降の PC
- 最近の NVIDIA GeForce RTX ビデオカード
- 利用する言語モデルのサイズに合わせたメインメモリ

# インストール

- [Stable Diffusion web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui) と同じく、パスを通した [Python 3.10.6](https://www.python.org/ftp/python/3.10.6/python-3.10.6-amd64.exe) と [Git for Windows](https://gitforwindows.org/) が必要です。
	- [Git for Windows のインストール](https://github.com/Zuntan03/SdWebUiTutorial/blob/main/_/doc/SdWebUiInstall/SdWebUiInstall.md#git-for-windows-%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB) と [Python のインストール](https://github.com/Zuntan03/SdWebUiTutorial/blob/main/_/doc/SdWebUiInstall/SdWebUiInstall.md#python-%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB) を参照してください。
- [`SetupLlmTranslator.bat`](https://github.com/Zuntan03/LlmTranslator/raw/main/LlmTranslator/SetupLlmTranslator.bat) を **右クリックから「名前をつけてリンク先を保存…」** でインストール先のフォルダ（英数字のみの浅いパス）にダウンロードします。
- インストール先フォルダで `SetupLlmTranslator.bat` をダブルクリックで実行すると、AIチャット翻訳のダウンロードとインストールが始まります。
	- **「WindowsによってPCが保護されました」と表示されたら、「詳細表示」から「実行」します。**  
![BatWarning](https://github.com/Zuntan03/SdWebUiTutorial/raw/main/_/doc/SdWebUiInstall/BatWarning.webp)
	- インストールが完了すると AIチャット翻訳が起動します。  
	**以降は `LlmTranslator.bat` をダブルクリックすると AIチャット翻訳を起動できます。**
- `KoboldCpp_*.bat` で KoboldCpp を立ち上げ、AIチャット翻訳といっしょに使用します。
	- アンダーバー以降は言語モデルの名前です。  
	名前に含まれる 7B、13B、30B などは言語モデルのサイズですので、メインメモリに合わせて選択してください。
	- `KoboldCpp_Wizard-Vicuna-*.bat` シリーズが最初の取っ掛かりとして良いかもしれません。おすすめモデルがあったら教えてください。

|メインメモリ|言語モデルサイズ|
|--:|:--|
|16GB|7B?|
|32GB|7B, 13B, 30B?|
|64GB|7b, 13b, 60B|

# 投稿された設定で物語を生成する

1. [aetherroom.club](https://aetherroom.club/) をブラウザ翻訳しつつ、興味の有りそうな物語を探します。
1. 物語を見つけたらタイトルをクリックし、URL 末尾の数値を覚えるか URL をコピーします。
1. `KoboldCpp_*.bat` で KoboldCpp を起動し、`Scenarios` - `Import from aetherroom.club` で数値か URL を入力し、`Confirm` します。
1. **KoboldCpp の入力欄をクリックしてフォーカスしておきます。**
1. `LlmTranslator.bat` で AIチャット翻訳を起動し、下の入力欄で `Enter` すると物語のイントロダクションが翻訳されます。
1. 入力欄で `Space` `Enter` すると、物語の続きが生成されます。生成が終わったら入力欄がからの状態で `Enter` すると、生成された物語が翻訳されます。
1. 入力欄に物語の続きを入力して `Enter` すると、続きに沿った物語が生成され、生成後に空欄 `Enter` で翻訳されます。
1. 物語の進行が気に入らない場合は `Ctrl+R` で再生成します。
1. 上記を繰り返して物語を生成します。

# 自分の設定で物語を生成する

<!--
KoboldCpp に詳しいわけではありませんので、間違っていたらお知らせください。
-->
TODO:

参考: [Kobold.cppで小説っぽいのを作る](https://w.atwiki.jp/localmlhub/pages/19.html)
参考: [Memory, Author's Note and World Info](https://github.com/KoboldAI/KoboldAI-Client/wiki/Memory,-Author's-Note-and-World-Info)

# TIPS

- AIチャット翻訳や KoboldCpp を終了して、`Update.bat` を実行すると、環境を更新します。
- `LlmTranslator/LlmTranslator.ini` に設定を保存しています。
	- `LlmTranslator/LlmTranslator.ini` を削除すれば、設定をリセットできます。
- `KoboldCppOption.txt` の最初の行と `KoboldCpp_*.bat` の引数で、KoboldCppの起動オプションを指定できます。
	- `--gpulayers` や `--usecublas` の利用で、GPU をより活用して高速化できる可能性があります。
- `TxtGenWebUi.bat` で [Text generation web UI`](https://github.com/oobabooga/text-generation-webui) が起動し、`Model` の `Download custom model or LoRA` でモデルをダウンロードして設定した後に chat Mode で AIチャット翻訳を利用できます。
	- が、`TxtGenWebUiGoogleTranslate.bat` で Google Translate を使ったほうが楽です。  
	ただし、チャットの内容は Google に送信されます。

英語以外の言語でも遜色なくローカルLLM を利用できるように、早くなって欲しいなぁ…

# ライセンス

このリポジトリのスクリプトやドキュメントは、[MIT License](./LICENSE.txt)です。

This software is released under the MIT License, see [LICENSE.txt](./LICENSE.txt).
