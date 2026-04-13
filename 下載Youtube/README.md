# YouTube 下載工具

這是一個功能完整的 YouTube 影片與音訊下載工具，使用 Python 和 yt-dlp 函式庫開發。

## 功能特色

✅ 下載 YouTube 影片（多種品質選項）  
✅ 下載純音訊檔案（支援 MP3、WAV、M4A、FLAC）  
✅ 下載整個播放清單  
✅ 查看影片詳細資訊  
✅ 即時顯示下載進度  
✅ 友善的中文介面  

## 安裝步驟

### 1. 啟動虛擬環境

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 2. 安裝相依套件

```bash
pip install -r requirements.txt
```

### 3. 安裝 FFmpeg（音訊轉檔需要）

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
下載並安裝 [FFmpeg](https://ffmpeg.org/download.html)

## 使用方式

### 執行程式

```bash
python app.py
```

### 功能說明

1. **下載影片**
   - 支援多種品質: best, worst, 720p, 1080p, 1440p, 4k
   - 自動合併為 MP4 格式

2. **下載音訊**
   - 支援格式: MP3, WAV, M4A, FLAC
   - 預設品質: 192kbps

3. **下載播放清單**
   - 可選擇下載影片或純音訊
   - 自動建立播放清單資料夾

4. **查看影片資訊**
   - 標題、頻道、長度
   - 觀看次數、上傳日期
   - 影片描述

## 使用範例

### 範例 1: 下載單個影片
```
請選擇功能: 1
請輸入 YouTube 網址: https://www.youtube.com/watch?v=xxxxx
請選擇影片品質: 1080p
```

### 範例 2: 下載音樂
```
請選擇功能: 2
請輸入 YouTube 網址: https://www.youtube.com/watch?v=xxxxx
請選擇音訊格式: mp3
```

### 範例 3: 下載播放清單
```
請選擇功能: 3
請輸入 YouTube 網址: https://www.youtube.com/playlist?list=xxxxx
```

## 檔案儲存位置

所有下載的檔案預設儲存在 `downloads/` 資料夾中。

## 注意事項

⚠️ 請遵守 YouTube 服務條款和版權法規  
⚠️ 僅供個人學習和研究使用  
⚠️ 下載受版權保護的內容可能違法  

## 常見問題

**Q: 下載失敗怎麼辦？**  
A: 確認網址正確、網路連線正常，並檢查是否安裝了 FFmpeg

**Q: 可以下載私人影片嗎？**  
A: 無法下載私人或需要登入才能觀看的影片

**Q: 支援哪些網站？**  
A: 主要支援 YouTube，yt-dlp 也支援其他多個影片網站

## 技術支援

如遇到問題，請檢查：
- yt-dlp 是否為最新版本: `pip install --upgrade yt-dlp`
- FFmpeg 是否正確安裝: `ffmpeg -version`
- Python 版本是否 >= 3.7

## 授權

本專案僅供教育和學習使用。
