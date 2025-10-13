import asyncio
from urllib.parse import urljoin

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

from bs4 import BeautifulSoup

BASE_SEARCH_URL = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"
# 有可能查詢路徑不同，需依實際觀察調整
# DETAIL_CONTENT_SELECTOR 要你事先用瀏覽器檢查詳細頁面的結構來定

RESULT_ITEM_SELECTOR = ".GridViewRowStyle, .GridViewAlternateRowStyle"  # 假設結果用 GridView 呈現的 row
RESULT_LINK_SELECTOR = "a"  # 在該 row 中 a 標籤
DETAIL_CONTENT_SELECTOR = "#tbAll > div"  # 假設詳細頁正文在一個 container div 內

async def search_and_get_first(keyword: str):
    browser_cfg = BrowserConfig(headless=True, verbose=False)
    run_cfg = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 先 GET 查詢頁，可能拿到一些隱藏欄位 / token / cookie
        init = await crawler.arun(url=BASE_SEARCH_URL, config=run_cfg)
        init_html = init.cleaned_html
        init_soup = BeautifulSoup(init_html, "html.parser")

        # 假設有隱藏欄位 __VIEWSTATE, __EVENTVALIDATION, 或其他 token，你要從頁面抓出來
        viewstate = init_soup.select_one("input[name=__VIEWSTATE]")["value"] if init_soup.select_one("input[name=__VIEWSTATE]") else ""
        eventval = init_soup.select_one("input[name=__EVENTVALIDATION]")["value"] if init_soup.select_one("input[name=__EVENTVALIDATION]") else ""

        # 構造 POST 表單參數（你要填對表單欄位名）
        form_data = {
            "__VIEWSTATE": viewstate,
            "__EVENTVALIDATION": eventval,
            "ctl00$MainContent$txt_KeyWord": keyword,  # 假設表單字段名稱
            # 以下幾個欄位你可能要補：法院、案件類別、日期區間、案由 / 主文 / 全文搜尋開關
            # "ctl00$MainContent$ddlCourt": "全部法院",
            # "ctl00$MainContent$ddlCaseType": "刑事",  # 或空白代表全部
            # "ctl00$MainContent$txtStartYear": "...",
            # "ctl00$MainContent$txtEndYear": "...",
            # "ctl00$MainContent$btnSearch": "查詢",
        }

        # 發 POST 查詢請求
        resp = await crawler.arun(
            url=BASE_SEARCH_URL,
            config=run_cfg,
            method="POST",
            post_data=form_data
        )
        resp_html = resp.cleaned_html
        resp_url = resp.url  # 有可能被重定向

        soup = BeautifulSoup(resp_html, "html.parser")
        items = soup.select(RESULT_ITEM_SELECTOR)
        if not items:
            print("查無結果，可能 selector 錯或表單未帶完全")
            # 你可以印 resp_html 來 debug
            # with open("debug_resp.html", "w", encoding="utf-8") as f: f.write(resp_html)
            return None

        first = items[0]
        a = first.select_one(RESULT_LINK_SELECTOR)
        if a is None:
            print("第一筆無連結標籤")
            return None

        href = a.get("href")
        detail_url = urljoin(resp_url, href)
        print("Detail URL:", detail_url)

        detail_res = await crawler.arun(url=detail_url, config=run_cfg)
        detail_html = detail_res.cleaned_html
        soup2 = BeautifulSoup(detail_html, "html.parser")
        content_elem = soup2.select_one(DETAIL_CONTENT_SELECTOR)
        if content_elem:
            content = content_elem.get_text("\n", strip=True)
        else:
            content = detail_html  # fallback

        return {
            "keyword": keyword,
            "detail_url": detail_url,
            "content": content
        }


if __name__ == "__main__":
    keyword = "詐騙 虛擬貨幣 台灣 柬埔寨 網路"
    res = asyncio.run(search_and_get_first(keyword))
    if res:
        print("取得內容：")
        print(res["content"][:1000])
    else:
        print("無法取得結果")
