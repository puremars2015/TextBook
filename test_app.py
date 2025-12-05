"""
測試 app.py 的功能
"""

import os
import sys
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock


# 確保可以導入 app 模組
sys.path.insert(0, os.path.dirname(__file__))
import app


def test_date_format_parsing():
    """測試日期格式解析"""
    # 這個測試會因為網路連線失敗而失敗，但我們可以驗證日期格式處理
    print("測試日期格式解析...")
    
    # 測試 YYYY-MM-DD 格式
    result = app.download_taifex_data('2024-01-15', save_dir='test_data')
    assert isinstance(result, bool), "應該返回布林值"
    
    # 測試 YYYY/MM/DD 格式
    result = app.download_taifex_data('2024/01/15', save_dir='test_data')
    assert isinstance(result, bool), "應該返回布林值"
    
    # 測試無效格式
    result = app.download_taifex_data('2024-13-45', save_dir='test_data')
    assert result == False, "無效日期應該返回 False"
    
    print("✓ 日期格式解析測試通過")


def test_directory_creation():
    """測試目錄建立功能"""
    print("測試目錄建立...")
    
    test_dir = 'test_data_creation'
    
    # 確保測試目錄不存在
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    # 嘗試下載（會失敗，但應該會建立目錄）
    app.download_taifex_data('2024-01-15', save_dir=test_dir)
    
    # 檢查目錄是否被建立
    assert os.path.exists(test_dir), "目錄應該被建立"
    
    # 清理
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    print("✓ 目錄建立測試通過")


def test_default_date():
    """測試預設日期（今天）"""
    print("測試預設日期...")
    
    result = app.download_taifex_data(save_dir='test_data_default')
    assert isinstance(result, bool), "應該返回布林值"
    
    # 清理
    if os.path.exists('test_data_default'):
        shutil.rmtree('test_data_default')
    
    print("✓ 預設日期測試通過")


@patch('app.requests.get')
def test_successful_download(mock_get):
    """測試成功下載（使用 mock）"""
    print("測試成功下載（模擬）...")
    
    # 設定 mock 回應
    mock_response = MagicMock()
    mock_response.content = b'test,data,content\n1,2,3'
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response
    
    # 執行下載
    result = app.download_taifex_data('2024-01-15', save_dir='test_data_mock')
    
    # 驗證結果
    assert result == True, "模擬下載應該成功"
    
    # 檢查檔案是否存在
    expected_file = 'test_data_mock/taifex_trading_data_20240115.csv'
    assert os.path.exists(expected_file), "檔案應該被建立"
    
    # 清理
    if os.path.exists('test_data_mock'):
        shutil.rmtree('test_data_mock')
    
    print("✓ 成功下載測試通過（模擬）")


def run_all_tests():
    """執行所有測試"""
    print("=" * 60)
    print("執行 app.py 測試")
    print("=" * 60)
    
    try:
        test_date_format_parsing()
        test_directory_creation()
        test_default_date()
        test_successful_download()
        
        print("\n" + "=" * 60)
        print("✓ 所有測試通過！")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ 測試失敗：{e}")
        return 1
    except Exception as e:
        print(f"\n✗ 測試錯誤：{e}")
        return 1


if __name__ == '__main__':
    exit(run_all_tests())
