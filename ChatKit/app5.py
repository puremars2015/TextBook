import asyncio
from urllib.parse import urljoin
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

BASE_SEARCH_URL = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"

RESULT_ITEM_SELECTOR = "tr.GridViewRowStyle, tr.GridViewAlternatingRowStyle"
RESULT_LINK_SELECTOR = "a"
DETAIL_CONTENT_SELECTOR = "#divFull, #JudgmentContent, .fulltext, #MainContent"

# 隱藏欄位名稱
FIELD_VIEWSTATE = "__VIEWSTATE"
FIELD_EVENTVALIDATION = "__EVENTVALIDATION"
FIELD_VIEWSTATEGENERATOR = "__VIEWSTATEGENERATOR"  # 修正命名：跟 HTML 中那個一致
FIELD_VIEWSTATEENCRYPTED = "__VIEWSTATEENCRYPTED"

# 查詢條件欄位名稱（根據 HTML 你貼的那段）
FIELD_JUD_COURT = "jud_court"
FIELD_JUD_SYS = "jud_sys"
FIELD_JUD_YEAR = "jud_year"
FIELD_SEL_JUDWORD = "sel_judword"
FIELD_JUD_CASE = "jud_case"
FIELD_JUD_NO = "jud_no"
FIELD_JUD_NO_END = "jud_no_end"
FIELD_DY1 = "dy1"
FIELD_DM1 = "dm1"
FIELD_DD1 = "dd1"
FIELD_DY2 = "dy2"
FIELD_DM2 = "dm2"
FIELD_DD2 = "dd2"
FIELD_JUD_TITLE = "jud_title"
FIELD_JUD_JMAIN = "jud_jmain"
FIELD_JUD_KW = "jud_kw"
FIELD_KBSTART = "KbStart"
FIELD_KBEND = "KbEnd"
FIELD_JUDTYPE = "judtype"
FIELD_WHOSUB = "whosub"

# 查詢按鈕名稱
FIELD_BTN_QRY = "ctl00$cp_content$btnQry"

async def fetch_single_case(keyword: str):
    browser_cfg = BrowserConfig(headless=True, verbose=False)
    run_cfg = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 1. GET 初始查詢頁面
        init = await crawler.arun(url=BASE_SEARCH_URL, config=run_cfg)
        init_html = init.cleaned_html
        init_soup = BeautifulSoup(init_html, "html.parser")

        def get_input_value(soup, name):
            tag = soup.select_one(f"input[name='{name}']")
            return tag["value"] if (tag and tag.has_attr("value")) else ""

        vs = get_input_value(init_soup, FIELD_VIEWSTATE)
        ev = get_input_value(init_soup, FIELD_EVENTVALIDATION)
        vgen = get_input_value(init_soup, FIELD_VIEWSTATEGENERATOR)
        ven = get_input_value(init_soup, FIELD_VIEWSTATEENCRYPTED)

        logging.info("hidden fields: viewstate len %d, eventval len %d, vgen len %d", len(vs), len(ev), len(vgen))

        # 2. 構造 POST 表單
        form_data = {
            FIELD_VIEWSTATE: vs,
            FIELD_EVENTVALIDATION: ev,
            FIELD_VIEWSTATEGENERATOR: vgen,
            FIELD_VIEWSTATEENCRYPTED: ven,

            # 查詢條件欄位
            FIELD_JUD_COURT: "",  # 全法院
            # FIELD_JUD_SYS: "",  # 若要限制案件類別，可指定
            FIELD_JUD_TITLE: "",
            FIELD_JUD_JMAIN: "",
            FIELD_JUD_KW: keyword,  # 把關鍵字放在全文搜尋欄位
            FIELD_KBSTART: "",
            FIELD_KBEND: "",
            FIELD_JUDTYPE: "JUDBOOK",
            FIELD_WHOSUB: "0",
            FIELD_BTN_QRY: "送出查詢",
        }

        resp = await crawler.arun(
            url=BASE_SEARCH_URL,
            config=run_cfg,
            method="POST",
            post_data=form_data
        )
        resp_html = resp.cleaned_html
        resp_url = resp.url
        logging.info("POST query done, response URL: %s", resp_url)

        # 3. 解析查詢結果頁
        soup = BeautifulSoup(resp_html, "html.parser")
        items = soup.select(RESULT_ITEM_SELECTOR)
        if not items:
            with open("debug_search.html", "w", encoding="utf-8") as f:
                f.write(resp_html)
            logging.warning("查無結果 items = 0 → debug_search.html")
            return None

        first = items[0]
        a = first.select_one(RESULT_LINK_SELECTOR)
        if a is None:
            logging.warning("第一筆結果沒有 <a>")
            return None

        href = a.get("href")
        detail_url = urljoin(resp_url, href)
        logging.info("Detail URL: %s", detail_url)

        # 4. 抓詳細頁
        detail_res = await crawler.arun(url=detail_url, config=run_cfg)
        detail_html = detail_res.cleaned_html
        soup2 = BeautifulSoup(detail_html, "html.parser")

        content_elem = None
        for sel in DETAIL_CONTENT_SELECTOR.split(","):
            sel = sel.strip()
            if sel:
                tmp = soup2.select_one(sel)
                if tmp:
                    content_elem = tmp
                    break

        if content_elem is not None:
            content_text = content_elem.get_text("\n", strip=True)
        else:
            with open("debug_detail.html", "w", encoding="utf-8") as f:
                f.write(detail_html)
            logging.warning("詳細頁無法定位正文 → debug_detail.html")
            content_text = detail_html

        return {
            "keyword": keyword,
            "detail_url": detail_url,
            "content": content_text
        }


if __name__ == "__main__":
    test_keyword = "詐騙 虛擬貨幣 台灣 柬埔寨 網路"
    res = asyncio.run(fetch_single_case(test_keyword))
    if res:
        print("=== 成功取得 ===")
        print("URL：", res["detail_url"])
        print("內容前 500 字：")
        print(res["content"][:500])
    else:
        print("未能取得判決")
