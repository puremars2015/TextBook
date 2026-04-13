import yt_dlp
import sys
import os

def get_ffmpeg_path():
    """獲取 ffmpeg 路徑（支援打包後的環境）"""
    if getattr(sys, 'frozen', False):
        # 打包後的環境
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'bin')
    else:
        # 開發環境
        # 使用相對於此檔案的路徑
        base_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_path, 'bin')

def download_youtube_audio(url, output_dir="downloads", download_playlist=False):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": get_ffmpeg_path(),
        "quiet": False,
        "noplaylist": not download_playlist,  # 如果不下載播放清單，則只下載單個影片
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    print("=== YouTube 音樂下載工具 ===\n")
    
    # 輸入 YouTube 網址
    youtube_url = input("請輸入 YouTube 網址: ").strip()
    
    if not youtube_url:
        print("錯誤：網址不能為空！")
        exit(1)
    
    # 選擇是否下載整個播放清單
    print("\n是否下載整個播放清單？")
    print("1. 是 (下載整個播放清單)")
    print("2. 否 (只下載單個影片)")
    choice = input("請選擇 (1/2): ").strip()
    
    download_playlist = choice == "1"
    
    if download_playlist:
        print("\n開始下載播放清單...")
    else:
        print("\n開始下載單個影片...")
    
    download_youtube_audio(youtube_url, download_playlist=download_playlist)
    print("\n音樂下載完成！")