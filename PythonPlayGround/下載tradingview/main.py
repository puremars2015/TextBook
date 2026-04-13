import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

def scrape_tradingview_strategy():
    """
    爬取 TradingView 策略交易清單數據
    
    使用方式：
    1. 先手動開啟 Chrome（可以正常登入 TradingView）
    2. 在 Chrome 網址列輸入：chrome://version/
    3. 找到「可執行檔路徑」，複製該路徑
    4. 開啟命令提示字元或 PowerShell，執行：
       "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
       （請替換成您的 Chrome 路徑）
    5. 在開啟的 Chrome 登入 TradingView 並開啟策略頁面
    6. 執行此腳本
    """
    
    # 設定 Chrome WebDriver - 連接到正在執行的 Chrome
    options = webdriver.ChromeOptions()
    
    # 連接到已經開啟的 Chrome（需先以 --remote-debugging-port=9222 啟動）
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 如果還沒開啟策略頁面，可以導航過去
        current_url = driver.current_url
        if "tradingview.com/chart/zKyrXngV" not in current_url:
            driver.get("https://tw.tradingview.com/chart/zKyrXngV/")
            time.sleep(3)
        
        # 確認策略報告已開啟
        input("請確保策略報告已開啟，然後按 Enter 繼續...")
        
        # 點擊"交易清單"標籤
        wait = WebDriverWait(driver, 10)
        trade_list_tab = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '交易清單')]"))
        )
        trade_list_tab.click()
        time.sleep(2)
        
        # 找到交易列表容器
        trade_container = driver.find_element(By.CSS_SELECTOR, "[id='bottom-area']")
        
        # 滾動到列表底部以確保載入所有交易
        last_height = driver.execute_script(
            "return arguments[0].scrollHeight", trade_container
        )
        
        while True:
            # 滾動到底部
            driver.execute_script(
                "arguments[0].scrollTo(0, arguments[0].scrollHeight)", 
                trade_container
            )
            time.sleep(1)
            
            # 檢查是否有新內容載入
            new_height = driver.execute_script(
                "return arguments[0].scrollHeight", trade_container
            )
            if new_height == last_height:
                break
            last_height = new_height
        
        # 滾動回頂部
        driver.execute_script("arguments[0].scrollTo(0, 0)", trade_container)
        time.sleep(1)
        
        # 提取所有交易數據
        trades_data = []
        
        # 找到所有交易行
        trade_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        
        for i in range(0, len(trade_rows), 2):  # 每兩行代表一筆完整交易
            try:
                exit_row = trade_rows[i]
                entry_row = trade_rows[i + 1] if i + 1 < len(trade_rows) else None
                
                if not entry_row:
                    continue
                
                # 提取交易編號和類型
                trade_number_cell = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(1)")
                trade_number = trade_number_cell.text.strip().split()[0]  # 取得數字部分
                trade_type = trade_number_cell.text.strip().split()[1]  # 看多/看空
                
                # 提取退出時間和訊號
                exit_time = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
                exit_signal = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
                
                # 提取進場時間和訊號
                entry_time = entry_row.find_element(By.CSS_SELECTOR, "td:nth-child(3)").text.strip()
                entry_signal = entry_row.find_element(By.CSS_SELECTOR, "td:nth-child(4)").text.strip()
                
                # 提取價格
                exit_price = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip().split()[0]
                entry_price = entry_row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip().split()[0]
                
                # 提取倉位大小
                position_size = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(6)").text.strip()
                
                # 提取淨損益
                pnl_cell = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(7)")
                pnl = pnl_cell.text.strip().split('\n')[0]  # 取得金額部分
                pnl_percent = pnl_cell.text.strip().split('\n')[1] if '\n' in pnl_cell.text else ''
                
                # 提取 Favorable excursion
                fav_exc_cell = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(8)")
                fav_exc = fav_exc_cell.text.strip().split('\n')[0]
                fav_exc_percent = fav_exc_cell.text.strip().split('\n')[1] if '\n' in fav_exc_cell.text else ''
                
                # 提取 Adverse excursion
                adv_exc_cell = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(9)")
                adv_exc = adv_exc_cell.text.strip().split('\n')[0]
                adv_exc_percent = adv_exc_cell.text.strip().split('\n')[1] if '\n' in adv_exc_cell.text else ''
                
                # 提取累積損益
                cum_pnl_cell = exit_row.find_element(By.CSS_SELECTOR, "td:nth-child(10)")
                cum_pnl = cum_pnl_cell.text.strip().split('\n')[0]
                cum_pnl_percent = cum_pnl_cell.text.strip().split('\n')[1] if '\n' in cum_pnl_cell.text else ''
                
                # 組織數據
                trade_data = {
                    '交易編號': trade_number,
                    '類型': trade_type,
                    '進場時間': entry_time,
                    '進場訊號': entry_signal,
                    '進場價格': entry_price,
                    '退出時間': exit_time,
                    '退出訊號': exit_signal,
                    '退出價格': exit_price,
                    '倉位大小': position_size,
                    '淨損益': pnl,
                    '淨損益(%)': pnl_percent,
                    'Favorable_Excursion': fav_exc,
                    'Favorable_Excursion(%)': fav_exc_percent,
                    'Adverse_Excursion': adv_exc,
                    'Adverse_Excursion(%)': adv_exc_percent,
                    '累積損益': cum_pnl,
                    '累積損益(%)': cum_pnl_percent
                }
                
                trades_data.append(trade_data)
                print(f"已提取交易 #{trade_number}")
                
            except Exception as e:
                print(f"提取第 {i//2 + 1} 筆交易時發生錯誤: {str(e)}")
                continue
        
        # 建立 DataFrame
        df = pd.DataFrame(trades_data)
        
        # 儲存到 CSV
        df.to_csv('tradingview_trades.csv', index=False, encoding='utf-8-sig')
        print(f"\n成功提取 {len(df)} 筆交易數據！")
        print(f"數據已儲存至 tradingview_trades.csv")
        
        return df
        
    finally:
        driver.quit()

if __name__ == "__main__":
    df = scrape_tradingview_strategy()
    print("\n數據預覽：")
    print(df.head())
