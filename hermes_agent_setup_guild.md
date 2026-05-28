以下是一份可直接給學員或自己照做的 **Windows 環境安裝 Hermes Agent，並製作影片上傳 YouTube 的操作步驟**。

---

# Hermes Agent 安裝與影片製作上傳 YouTube 操作步驟

環境：Windows 10 / Windows 11

## 一、準備工作

請先準備以下項目：

1. Windows 10 / 11 電腦
2. PowerShell 或 Windows Terminal
3. MiniMax API Key，建議用來產生影片、語音
4. OpenRouter API Key，建議用來讓 Hermes Agent 使用 LLM 模型
5. YouTube 帳號與頻道
6. 一張人物圖片、產品圖片或影片主題素材
7. 建議建立一個工作資料夾，例如：

```powershell
mkdir C:\AI_VIDEO
mkdir C:\AI_VIDEO\project01
```

Hermes Agent 目前 Windows 有兩種安裝方式：**Native Windows 安裝**與 **WSL2 安裝**。官方說明中，Native Windows 支援仍屬 early beta；若追求穩定，官方仍建議在 Windows 內使用 WSL2 安裝。([GitHub][1])

---

# 二、安裝 Hermes Agent

## 方案 A：Windows Native 安裝，較簡單，但仍是 Beta

開啟 PowerShell，執行：

```powershell
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1 | iex
```

安裝程式會自動處理 Hermes 所需環境，例如 Python 3.11、Node.js 22、ripgrep、ffmpeg、Git Bash 等，並把 Hermes 安裝在 `%LOCALAPPDATA%\hermes` 底下。([GitHub][2])

安裝完成後，關閉 PowerShell，重新開啟一個新的 PowerShell，輸入：

```powershell
hermes doctor
```

如果檢查正常，再輸入：

```powershell
hermes
```

看到 Hermes 對話介面，就代表安裝完成。

---

## 方案 B：WSL2 安裝，較穩定，推薦

先在 PowerShell 以系統管理員身分執行：

```powershell
wsl --install -d Ubuntu
```

安裝完後重新開機，打開 Ubuntu 終端機，執行：

```bash
sudo apt update && sudo apt upgrade -y
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
source ~/.bashrc
hermes doctor
hermes
```

WSL2 版本的 Hermes 資料通常會放在：

```bash
~/.hermes
```

從 Windows 檔案總管可用這個路徑查看：

```text
\\wsl.localhost\Ubuntu\home\你的使用者名稱\.hermes
```

---

# 三、設定 Hermes Agent 的模型

安裝完成後，執行：

```bash
hermes setup
```

或單獨設定模型：

```bash
hermes model
```

建議設定方式：

## 使用 OpenRouter

選擇 OpenRouter，然後填入：

```text
API Key: 你的 OpenRouter API Key
Model: 你要使用的模型代號
```

如果 Hermes 沒有列出 OpenRouter，也可以選擇 Custom Endpoint：

```text
Base URL: https://openrouter.ai/api/v1
API Key: 你的 OpenRouter API Key
Model Name: 你在 OpenRouter 上選的模型代號
```

設定完成後，測試：

```bash
hermes
```

然後輸入：

```text
請幫我寫一段 60 秒的 YouTube Shorts 影片腳本，主題是 AI 自動化工作流程。
```

如果可以正常回覆，就代表 LLM 模型已經可用。

---

# 四、安裝 MiniMax CLI，讓 Hermes 可以產生影片與語音

MiniMax 官方 CLI 支援文字、圖片、影片、語音、音樂等生成，也提供給 AI Agent 或終端機使用。([GitHub][3])

在 PowerShell 或 WSL2 裡執行：

```bash
npm install -g mmx-cli
```

登入 MiniMax：

```bash
mmx auth login --api-key 你的MiniMax_API_KEY
```

檢查登入狀態：

```bash
mmx auth status
```

測試產生語音：

```bash
mmx speech synthesize --text "大家好，這是一段 AI 自動生成的影片旁白。" --out voice.mp3
```

測試產生影片：

```bash
mmx video generate --prompt "A modern AI news studio, cinematic lighting, professional host, futuristic screen background" --download video.mp4
```

MiniMax CLI 官方範例也包含影片產生、非同步任務查詢、影片下載與語音合成等指令。([GitHub][3])

---

# 五、建立影片製作專案資料夾

建議每支影片使用一個獨立資料夾：

```powershell
mkdir C:\AI_VIDEO\project01
cd C:\AI_VIDEO\project01
```

資料夾建議結構：

```text
project01
├─ script.txt          影片腳本
├─ voice.mp3           旁白音檔
├─ video.mp4           AI 產生的影片
├─ subtitle.srt        字幕
├─ thumbnail.png       YouTube 縮圖
└─ final.mp4           最終輸出影片
```

---

# 六、請 Hermes Agent 幫你製作影片

進入 Hermes：

```bash
hermes
```

輸入以下任務：

```text
請幫我建立一支 60 秒 YouTube Shorts 影片。

主題：AI Agent 如何幫助上班族自動完成工作
風格：科技感、專業、適合社群短影音
比例：9:16
語言：繁體中文
輸出位置：C:\AI_VIDEO\project01

請完成以下工作：
1. 寫一份 60 秒影片腳本
2. 產生旁白文字
3. 使用 MiniMax CLI 產生語音 voice.mp3
4. 使用 MiniMax CLI 產生影片 video.mp4
5. 產生 subtitle.srt 字幕
6. 使用 ffmpeg 合併影片、語音與字幕
7. 輸出 final.mp4
8. 幫我產生 YouTube 標題、描述、Hashtags
```

如果你用的是 WSL2，請把輸出位置改成：

```text
~/ai-video/project01
```

---

# 七、用 FFmpeg 合併影片、語音與字幕

如果 Hermes 沒有自動完成，你可以手動執行：

```bash
ffmpeg -i video.mp4 -i voice.mp3 -c:v copy -c:a aac -shortest output.mp4
```

如果要加字幕：

```bash
ffmpeg -i output.mp4 -vf subtitles=subtitle.srt -c:a copy final.mp4
```

如果要做 YouTube Shorts，建議輸出成直式 9:16：

```bash
ffmpeg -i output.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:a copy final.mp4
```

---

# 八、上傳到 YouTube

## 方法 A：手動上傳，最穩定，推薦

1. 開啟 YouTube Studio
2. 右上角點選「建立 / Create」
3. 選擇「上傳影片 / Upload videos」
4. 選擇 `final.mp4`
5. 填寫標題、描述、縮圖、標籤
6. 設定觀眾類型：是否為兒童內容
7. 設定公開狀態：私人、不公開、公開
8. 按下發布

YouTube 官方說明指出，電腦版可從 YouTube Studio 右上角的 Create 上傳影片，且一次最多可上傳 15 支影片。([Google支援中心][4])

---

## 方法 B：用 YouTube API 自動上傳，適合後續自動化

如果你要讓 Hermes Agent 自動上傳，需要設定：

1. Google Cloud Project
2. YouTube Data API v3
3. OAuth 2.0 Client ID
4. 授權範圍：

```text
https://www.googleapis.com/auth/youtube.upload
```

YouTube Data API 的 `videos.insert` 可以用來上傳影片並設定 metadata，支援 `video/*` 類型影片，單支最大檔案可到 256GB。([Google for Developers][5])

但要注意一點：Google 官方文件說明，2020 年 7 月 28 日後建立且未通過驗證的 API 專案，透過 `videos.insert` 上傳的影片會被限制為私人觀看模式；若要解除限制，API 專案需要通過審核。([Google for Developers][5])

所以初期建議：

```text
Hermes 負責製作 final.mp4、標題、描述、縮圖
YouTube 上傳先用手動方式完成
等流程穩定後，再改成 API 自動上傳
```

---

# 九、建議的完整流程

```text
1. 安裝 Hermes Agent
2. 設定 OpenRouter 或其他 LLM 模型
3. 安裝 MiniMax CLI
4. 測試 MiniMax 語音與影片生成
5. 建立影片專案資料夾
6. 請 Hermes 寫腳本
7. 請 Hermes 產生旁白
8. 請 Hermes 呼叫 MiniMax 產生語音
9. 請 Hermes 呼叫 MiniMax 產生影片
10. 使用 ffmpeg 合併影片、語音與字幕
11. 輸出 final.mp4
12. 手動上傳 YouTube
13. 後續再改成 YouTube API 自動上傳
```

---

# 十、給 Hermes Agent 的範例任務指令

可以直接貼給 Hermes：

```text
你是一位影片製作助理。

請幫我在 C:\AI_VIDEO\project01 製作一支 60 秒 YouTube Shorts。

影片主題：
AI Agent 如何幫助公司自動完成報表、Email、資料整理與影片製作。

影片風格：
專業、科技感、簡潔、適合上班族觀看。

請完成：
1. 建立影片腳本 script.txt
2. 建立 60 秒中文旁白 voice_text.txt
3. 產生 YouTube 標題 title.txt
4. 產生 YouTube 描述 description.txt
5. 產生 hashtags.txt
6. 使用 MiniMax CLI 產生 voice.mp3
7. 使用 MiniMax CLI 產生 video.mp4
8. 產生 subtitle.srt
9. 使用 ffmpeg 合併成 final.mp4
10. 最後列出我需要手動上傳 YouTube 的步驟
```

---

# 十一、注意事項

1. API Key 不要放在公開文件、GitHub、影片描述或字幕裡。
2. 如果只是一般 AI 影片，MiniMax 影片加語音就夠用。
3. 如果你要做「人物照片開口對嘴」影片，Hermes 只是流程控制器，還需要另外接 lip-sync API，例如 Kling、HeyGen、D-ID 或其他支援對嘴的服務。
4. 如果 YouTube 自動上傳要公開發布，建議後期才做，因為 YouTube API 專案可能需要審核。
5. 初期最穩流程是：Hermes 製作影片 → 手動檢查 final.mp4 → 手動上傳 YouTube。

[1]: https://github.com/nousresearch/hermes-agent "GitHub - NousResearch/hermes-agent: The agent that grows with you · GitHub"
[2]: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md "hermes-agent/website/docs/getting-started/installation.md at main · NousResearch/hermes-agent · GitHub"
[3]: https://github.com/MiniMax-AI/cli "GitHub - MiniMax-AI/cli: Generate text, images, video, speech, and music by MiniMax. · GitHub"
[4]: https://support.google.com/youtube/answer/57407?co=GENIE.Platform%3DDesktop&hl=en "Upload YouTube videos - Computer - YouTube Help"
[5]: https://developers.google.com/youtube/v3/docs/videos/insert "Videos: insert  |  YouTube Data API  |  Google for Developers"
