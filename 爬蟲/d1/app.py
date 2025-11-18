"""
AI爬蟲研究 - 司法院判決書爬蟲
使用 LangChain + Playwright 爬取判決書資料
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pymongo import MongoClient


class JudgmentCrawler:
    def __init__(self, keyword="詐騙", mongodb_uri="mongodb://localhost:27017/"):
        """
        初始化爬蟲
        :param keyword: 查詢關鍵字
        :param mongodb_uri: MongoDB連接字串
        """
        self.keyword = keyword
        self.base_url = "https://judgment.judicial.gov.tw/FJUD/default.aspx"
        self.mongodb_uri = mongodb_uri
        self.judgments = []
        
    async def setup_browser(self, playwright):
        """設定瀏覽器"""
        browser = await playwright.chromium.launch(headless=False)  # headless=True 可以背景執行
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = await context.new_page()
        return browser, page
    
    async def search_judgments(self, page):
        """
        執行判決書搜尋
        """
        print(f"正在搜尋關鍵字: {self.keyword}")
        
        # 前往首頁
        await page.goto(self.base_url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        try:
            # 點擊「進階查詢」或找到搜尋框
            # 這裡需要根據實際網站結構調整選擇器
            
            # 等待頁面載入
            await page.wait_for_load_state('networkidle')
            
            # 輸入關鍵字 (需要根據實際網站調整選擇器)
            # 範例: 找到搜尋框並輸入關鍵字
            search_input = await page.query_selector('input[name="txtKW"]')
            if search_input:
                await search_input.fill(self.keyword)
                print(f"已輸入關鍵字: {self.keyword}")
            
            # 點擊搜尋按鈕
            search_button = await page.query_selector('input[type="submit"]')
            if search_button:
                await search_button.click()
                print("已點擊搜尋按鈕")
                await page.wait_for_load_state('networkidle')
                await asyncio.sleep(3)
            
            # 取得頁面內容
            content = await page.content()
            return content
            
        except Exception as e:
            print(f"搜尋時發生錯誤: {str(e)}")
            # 保存錯誤時的截圖
            await page.screenshot(path='error_screenshot.png')
            return None
    
    def parse_judgment_list(self, html_content):
        """
        解析判決書列表
        """
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        judgments = []
        
        # 根據實際網站結構調整選擇器
        # 這是一個範例結構，需要根據實際網站調整
        judgment_items = soup.select('tr.GridRow, tr.GridAltRow')
        
        print(f"找到 {len(judgment_items)} 筆判決書")
        
        for item in judgment_items[:10]:  # 限制只取前10筆作為範例
            try:
                # 提取判決書資訊
                judgment_data = {
                    '案號': item.select_one('td:nth-child(1)').text.strip() if item.select_one('td:nth-child(1)') else '',
                    '日期': item.select_one('td:nth-child(2)').text.strip() if item.select_one('td:nth-child(2)') else '',
                    '案由': item.select_one('td:nth-child(3)').text.strip() if item.select_one('td:nth-child(3)') else '',
                    '法院': item.select_one('td:nth-child(4)').text.strip() if item.select_one('td:nth-child(4)') else '',
                    '爬取時間': datetime.now().isoformat(),
                    '關鍵字': self.keyword
                }
                judgments.append(judgment_data)
            except Exception as e:
                print(f"解析單筆資料時發生錯誤: {str(e)}")
                continue
        
        return judgments
    
    async def get_judgment_detail(self, page, judgment_url):
        """
        取得判決書詳細內容
        """
        try:
            await page.goto(judgment_url, wait_until='networkidle')
            await asyncio.sleep(2)
            
            content = await page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # 提取判決書全文
            judgment_text = soup.select_one('.judgment-content')
            if judgment_text:
                return judgment_text.text.strip()
            return None
            
        except Exception as e:
            print(f"取得判決書詳情時發生錯誤: {str(e)}")
            return None
    
    def save_to_mongodb(self, judgments):
        """
        儲存資料到MongoDB
        """
        try:
            client = MongoClient(self.mongodb_uri)
            db = client['judgment_db']
            collection = db['judgments']
            
            if judgments:
                result = collection.insert_many(judgments)
                print(f"成功儲存 {len(result.inserted_ids)} 筆資料到MongoDB")
            else:
                print("沒有資料需要儲存")
                
            client.close()
            
        except Exception as e:
            print(f"儲存到MongoDB時發生錯誤: {str(e)}")
            print("請確認MongoDB服務是否已啟動")
    
    def save_to_json(self, judgments, filename='judgments.json'):
        """
        儲存資料到JSON檔案 (作為備份或MongoDB未啟動時使用)
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(judgments, f, ensure_ascii=False, indent=2)
            print(f"已儲存到 {filename}")
        except Exception as e:
            print(f"儲存JSON時發生錯誤: {str(e)}")
    
    async def run(self):
        """
        執行爬蟲主流程
        """
        print("=" * 50)
        print("AI爬蟲啟動 - 司法院判決書爬蟲")
        print("=" * 50)
        
        async with async_playwright() as playwright:
            browser, page = await self.setup_browser(playwright)
            
            try:
                # 1. 搜尋判決書
                html_content = await self.search_judgments(page)
                
                # 2. 解析判決書列表
                if html_content:
                    self.judgments = self.parse_judgment_list(html_content)
                    
                    # 3. 顯示爬取結果
                    print("\n爬取結果:")
                    print("-" * 50)
                    for idx, judgment in enumerate(self.judgments, 1):
                        print(f"\n{idx}. {judgment}")
                    
                    # 4. 儲存資料
                    if self.judgments:
                        # 儲存到JSON
                        self.save_to_json(self.judgments)
                        
                        # 嘗試儲存到MongoDB
                        try:
                            self.save_to_mongodb(self.judgments)
                        except Exception as e:
                            print(f"MongoDB儲存失敗，資料已保存在JSON檔案中")
                    
                    print("\n" + "=" * 50)
                    print(f"爬蟲執行完成！共爬取 {len(self.judgments)} 筆資料")
                    print("=" * 50)
                else:
                    print("未能取得網頁內容")
                
            except Exception as e:
                print(f"執行過程中發生錯誤: {str(e)}")
                
            finally:
                # 關閉瀏覽器
                await browser.close()


async def main():
    """
    主程式
    """
    # 建立爬蟲實例
    crawler = JudgmentCrawler(
        keyword="詐騙",
        mongodb_uri="mongodb://localhost:27017/"
    )
    
    # 執行爬蟲
    await crawler.run()


if __name__ == "__main__":
    # 執行非同步主程式
    asyncio.run(main())
