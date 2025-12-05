"""
臺灣期貨交易所 (TAIFEX) 交易資料下載程式
從 https://www.taifex.com.tw/cht/3/dlFutPrevious30DaysSalesData 下載特定日期的交易資料
"""

import requests
from datetime import datetime
import os
import sys


def download_taifex_data(date=None, save_dir='data'):
    """
    下載臺灣期貨交易所特定日期的交易資料。
    
    參數:
        date: 日期字串，格式為 YYYY/MM/DD 或 YYYY-MM-DD，預設為今天
        save_dir: 儲存資料的目錄，預設為 'data'
    
    返回:
        bool: 下載成功返回 True，失敗返回 False
    """
    # 處理日期參數
    if date is None:
        date_obj = datetime.today()
    else:
        # 支援多種日期格式
        try:
            if '/' in date:
                date_obj = datetime.strptime(date, '%Y/%m/%d')
            elif '-' in date:
                date_obj = datetime.strptime(date, '%Y-%m-%d')
            else:
                print(f"錯誤：不支援的日期格式 '{date}'。請使用 YYYY/MM/DD 或 YYYY-MM-DD 格式。")
                return False
        except ValueError as e:
            print(f"錯誤：日期格式錯誤 - {e}")
            return False
    
    # 格式化日期用於 URL（YYYY/MM/DD）和檔案名稱
    date_str_url = date_obj.strftime('%Y/%m/%d')
    date_str_file = date_obj.strftime('%Y%m%d')
    
    # 建立請求 URL
    base_url = 'https://www.taifex.com.tw/cht/3/dlFutPrevious30DaysSalesData'
    
    # 根據 Taifex 網站的實際需求設定參數
    params = {
        'queryStartDate': date_str_url,
        'queryEndDate': date_str_url
    }
    
    # 建立儲存目錄
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"建立目錄：{save_dir}")
    
    # 設定檔案名稱
    filename = f'taifex_trading_data_{date_str_file}.csv'
    filepath = os.path.join(save_dir, filename)
    
    try:
        print(f"正在下載 {date_str_url} 的交易資料...")
        print(f"URL: {base_url}")
        
        # 發送 GET 請求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        # 儲存檔案
        with open(filepath, 'wb') as file:
            file.write(response.content)
        
        # 檢查檔案大小
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            print(f"警告：下載的檔案大小為 0，可能該日期無資料。")
            os.remove(filepath)
            return False
        
        print(f"✓ 成功下載資料至：{filepath}")
        print(f"  檔案大小：{file_size:,} bytes")
        return True
        
    except requests.exceptions.Timeout:
        print("錯誤：請求超時，請檢查網路連線。")
        return False
    except requests.exceptions.ConnectionError:
        print("錯誤：無法連線到 Taifex 網站，請檢查網路連線。")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"錯誤：HTTP 錯誤 - {e}")
        return False
    except Exception as e:
        print(f"錯誤：{e}")
        return False


def main():
    """
    主程式：處理命令列參數並執行下載
    """
    print("=" * 60)
    print("臺灣期貨交易所 (TAIFEX) 交易資料下載程式")
    print("=" * 60)
    
    # 檢查命令列參數
    if len(sys.argv) > 1:
        date = sys.argv[1]
        print(f"指定日期：{date}")
    else:
        date = None
        print(f"使用今天日期：{datetime.today().strftime('%Y-%m-%d')}")
    
    # 執行下載
    success = download_taifex_data(date)
    
    if success:
        print("\n✓ 下載完成！")
        return 0
    else:
        print("\n✗ 下載失敗。")
        return 1


if __name__ == '__main__':
    exit(main())
