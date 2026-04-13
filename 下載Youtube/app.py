#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 影片與音樂下載工具
支援下載影片、純音訊檔案，並提供多種品質選項
"""

import os
import sys
from pathlib import Path
try:
    import yt_dlp
except ImportError:
    print("請先安裝 yt-dlp: pip install yt-dlp")
    sys.exit(1)


class YouTubeDownloader:
    """YouTube 下載器類別"""
    
    def __init__(self, download_path='downloads'):
        """
        初始化下載器
        
        Args:
            download_path: 下載檔案儲存路徑
        """
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
    
    def download_video(self, url, quality='best'):
        """
        下載 YouTube 影片
        
        Args:
            url: YouTube 影片網址
            quality: 影片品質 ('best', 'worst', '720p', '1080p', '1440p', '4k')
        """
        print(f"\n📹 開始下載影片: {url}")
        
        # 設定下載選項
        ydl_opts = {
            'format': self._get_video_format(quality),
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'merge_output_format': 'mp4',  # 合併為 mp4 格式
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                print(f"\n✅ 影片下載完成: {info['title']}")
                return True
        except Exception as e:
            print(f"\n❌ 下載失敗: {str(e)}")
            return False
    
    def download_audio(self, url, format='mp3'):
        """
        下載 YouTube 音訊
        
        Args:
            url: YouTube 影片網址
            format: 音訊格式 ('mp3', 'wav', 'm4a', 'flac')
        """
        print(f"\n🎵 開始下載音訊: {url}")
        
        # 設定下載選項
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'progress_hooks': [self._progress_hook],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': format,
                'preferredquality': '192',
            }],
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                print(f"\n✅ 音訊下載完成: {info['title']}")
                return True
        except Exception as e:
            print(f"\n❌ 下載失敗: {str(e)}")
            return False
    
    def download_playlist(self, url, download_type='video'):
        """
        下載 YouTube 播放清單
        
        Args:
            url: YouTube 播放清單網址
            download_type: 下載類型 ('video' 或 'audio')
        """
        print(f"\n📋 開始下載播放清單: {url}")
        
        if download_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.download_path / '%(playlist)s/%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'best',
                'outtmpl': str(self.download_path / '%(playlist)s/%(title)s.%(ext)s'),
                'progress_hooks': [self._progress_hook],
            }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                print(f"\n✅ 播放清單下載完成!")
                return True
        except Exception as e:
            print(f"\n❌ 下載失敗: {str(e)}")
            return False
    
    def get_video_info(self, url):
        """
        取得影片資訊
        
        Args:
            url: YouTube 影片網址
        """
        ydl_opts = {'quiet': True}
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                print("\n" + "="*60)
                print(f"標題: {info.get('title', 'N/A')}")
                print(f"頻道: {info.get('uploader', 'N/A')}")
                print(f"長度: {self._format_duration(info.get('duration', 0))}")
                print(f"觀看次數: {info.get('view_count', 'N/A'):,}")
                print(f"上傳日期: {info.get('upload_date', 'N/A')}")
                print(f"描述: {info.get('description', 'N/A')[:100]}...")
                print("="*60 + "\n")
                
                return info
        except Exception as e:
            print(f"\n❌ 無法取得影片資訊: {str(e)}")
            return None
    
    def _get_video_format(self, quality):
        """根據品質設定回傳格式字串"""
        quality_map = {
            'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'worst': 'worst',
            '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]',
            '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]',
            '1440p': 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440]',
            '4k': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160]',
        }
        return quality_map.get(quality, quality_map['best'])
    
    def _progress_hook(self, d):
        """下載進度顯示"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\r進度: {percent} | 速度: {speed} | 剩餘時間: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\n正在處理檔案...")
    
    def _format_duration(self, seconds):
        """格式化時間長度"""
        if not seconds:
            return "N/A"
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"


def show_menu():
    """顯示主選單"""
    print("\n" + "="*60)
    print("🎬 YouTube 下載工具")
    print("="*60)
    print("1. 下載影片")
    print("2. 下載音訊 (MP3)")
    print("3. 下載播放清單 (影片)")
    print("4. 下載播放清單 (音訊)")
    print("5. 查看影片資訊")
    print("6. 退出")
    print("="*60)


def main():
    """主程式"""
    downloader = YouTubeDownloader()
    
    while True:
        show_menu()
        choice = input("\n請選擇功能 (1-6): ").strip()
        
        if choice == '6':
            print("\n👋 感謝使用，再見！")
            break
        
        if choice not in ['1', '2', '3', '4', '5']:
            print("❌ 無效的選擇，請重新輸入")
            continue
        
        url = input("\n請輸入 YouTube 網址: ").strip()
        
        if not url:
            print("❌ 網址不能為空")
            continue
        
        if choice == '1':
            print("\n可用品質: best, worst, 720p, 1080p, 1440p, 4k")
            quality = input("請選擇影片品質 (預設: best): ").strip() or 'best'
            downloader.download_video(url, quality)
        
        elif choice == '2':
            print("\n可用格式: mp3, wav, m4a, flac")
            format = input("請選擇音訊格式 (預設: mp3): ").strip() or 'mp3'
            downloader.download_audio(url, format)
        
        elif choice == '3':
            downloader.download_playlist(url, 'video')
        
        elif choice == '4':
            downloader.download_playlist(url, 'audio')
        
        elif choice == '5':
            downloader.get_video_info(url)
        
        input("\n按 Enter 繼續...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程式已中斷，再見！")
        sys.exit(0)
