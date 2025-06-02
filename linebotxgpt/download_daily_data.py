import os
import requests
from zipfile import ZipFile
from datetime import datetime

def download_and_extract_taifex_data(date=None, save_dir='extracted_files'):
    """
    下載並解壓臺灣期貨交易所每日交易數據。

    :param date: 指定下載的日期 (格式：YYYY_MM_DD)，預設為今天的日期。
    :param save_dir: 解壓縮檔案的目標資料夾，預設為 'extracted_files'。
    """
    if date is None:
        date = datetime.today().strftime('%Y_%m_%d')  # 預設為今天的日期

    url = f'https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/Daily_{date}.zip'
    zip_path = f'Daily_{date}.zip'

    try:
        # 下載 ZIP 檔案
        response = requests.get(url)
        response.raise_for_status()  # 如果下載失敗，將拋出異常
        with open(zip_path, 'wb') as file:
            file.write(response.content)
        print(f"成功下載 {zip_path}")

        # 解壓縮 ZIP 檔案
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)  # 如果目標資料夾不存在，則建立
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(save_dir)
        print(f"成功解壓縮至 {save_dir} 資料夾")

        # 可選：刪除 ZIP 檔案以節省空間
        os.remove(zip_path)
        print(f"已刪除壓縮檔案 {zip_path}")
    except requests.exceptions.RequestException as e:
        print(f"下載失敗: {e}")
    except Exception as e:
        print(f"解壓縮或其他操作失敗: {e}")

# 呼叫方法
download_and_extract_taifex_data()
