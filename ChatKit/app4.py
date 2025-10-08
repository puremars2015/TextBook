import asyncio
from urllib.parse import urljoin
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

# 篩選頁 URL（查詢頁面）
BASE_SEARCH_URL = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"

# 以下這些 selector、欄位名稱，要你用瀏覽器 DevTools 去確定
# ──────────────────────────────────────────────
# 每筆結果在查詢結果頁中的 CSS selector
RESULT_ITEM_SELECTOR = ".GridViewRowStyle, .GridViewAlternatingRowStyle"  # 假設的例子：grid view 的 row 樣式
# 在該結果 row 中，代表連結到詳細頁的 a 標籤
RESULT_LINK_SELECTOR = "a"
# 在詳細頁中，代表「判決全文／主要內容」的容器 selector
DETAIL_CONTENT_SELECTOR = "#divFull > table"  # 這是猜的，你要實際查詳細頁面的 HTML 結構
# 查詢表單欄位名稱 — 這些是你要從網頁 view-source / DevTools 得到的
FORM_FIELD_KEYWORD = "ctl00$MainContent$txt_KeyWord"
FORM_FIELD_VIEWSTATE = "__VIEWSTATE"
FORM_FIELD_EVENTVALIDATION = "__EVENTVALIDATION"
FORM_FIELD_BTN_SEARCH = "ctl00$MainContent$btnSearch"
# 你可能還有其他的欄位，例如「法院選擇」、「案件類別」、「日期區間」、「全文搜尋開關」等
# 比如：
# FORM_FIELD_COURT = "ctl00$MainContent$ddlCourt"
# FORM_FIELD_CASETYPE = "ctl00$MainContent$ddlCaseType"
# FORM_FIELD_FROM_YEAR = "ctl00$MainContent$txtStartYear"
# FORM_FIELD_TO_YEAR = "ctl00$MainContent$txtEndYear"
# ──────────────────────────────────────────────

async def fetch_single_case(keyword: str):
    browser_cfg = BrowserConfig(headless=True, verbose=False)
    run_cfg = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 1. 先 GET 查詢頁，拿到隱藏欄位（__VIEWSTATE, __EVENTVALIDATION）等
        init = await crawler.arun(url=BASE_SEARCH_URL, config=run_cfg)
        init_html = init.cleaned_html
        init_soup = BeautifulSoup(init_html, "html.parser")

        vs = init_soup.select_one(f"input[name={FORM_FIELD_VIEWSTATE}]")
        ev = init_soup.select_one(f"input[name={FORM_FIELD_EVENTVALIDATION}]")
        viewstate = vs["value"] if vs and vs.has_attr("value") else ""
        eventval = ev["value"] if ev and ev.has_attr("value") else ""

        logging.info("Got viewstate length=%d, eventval length=%d", len(viewstate), len(eventval))

        # 2. 構造 POST 表單資料進行關鍵字查詢
        form_data = {
            FORM_FIELD_VIEWSTATE: viewstate,
            FORM_FIELD_EVENTVALIDATION: eventval,
            FORM_FIELD_KEYWORD: keyword,
            # 下面這個按鈕欄位可能是必要的提交指令
            FORM_FIELD_BTN_SEARCH: "查詢",
            # 若有其他條件欄位，你要把它們也加進來，例如法院、案件類別等
            # FORM_FIELD_COURT: "",
            # FORM_FIELD_CASETYPE: "",
            # FORM_FIELD_FROM_YEAR: "",
            # FORM_FIELD_TO_YEAR: "",
        }

        resp = await crawler.arun(
            url=BASE_SEARCH_URL,
            config=run_cfg,
            method="POST",
            post_data=form_data
        )
        resp_html = resp.cleaned_html
        resp_url = resp.url
        logging.info("Search POST done, response URL: %s", resp_url)

        # 3. 解析查詢結果頁，拿第一筆結果的詳細頁連結
        soup = BeautifulSoup(resp_html, "html.parser")
        items = soup.select(RESULT_ITEM_SELECTOR)
        if not items:
            # debug 輸出 HTML 存檔，方便你檢查
            with open("debug_search.html", "w", encoding="utf-8") as f:
                f.write(resp_html)
            logging.warning("查無結果 (items list is empty). Stored debug_search.html")
            return None

        first = items[0]
        a = first.select_one(RESULT_LINK_SELECTOR)
        if a is None:
            logging.warning("第一筆結果沒有 a 標籤")
            return None

        href = a.get("href")
        detail_url = urljoin(resp_url, href)
        logging.info("Detail URL found: %s", detail_url)

        # 4. 抓詳細判決頁面
        detail_res = await crawler.arun(url=detail_url, config=run_cfg)
        detail_html = detail_res.cleaned_html
        soup2 = BeautifulSoup(detail_html, "html.parser")
        cont = soup2.select_one(DETAIL_CONTENT_SELECTOR)
        if cont:
            content_text = cont.get_text("\n", strip=True)
        else:
            # fallback：如果找不到 selector，就把整頁 HTML 原樣回來供你 debug
            with open("debug_detail.html", "w", encoding="utf-8") as f:
                f.write(detail_html)
            logging.warning("找不到 DETAIL_CONTENT_SELECTOR，已存 debug_detail.html")
            content_text = detail_html

        return {
            "keyword": keyword,
            "detail_url": detail_url,
            "content": content_text
        }


if __name__ == "__main__":
    # 測試關鍵字（你給的關鍵字，我稍微改成空格分隔版）
    test_keyword = "詐騙 虛擬貨幣 台灣 柬埔寨 網路"
    result = asyncio.run(fetch_single_case(test_keyword))
    if result:
        print("=== 取得判決內容 ===")
        print("詳細頁 URL：", result["detail_url"])
        print("內容前 1000 字：")
        print(result["content"][:1000])
    else:
        print("無法取得指定判決")
