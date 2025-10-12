import requests
from autoscraper import AutoScraper
from bs4 import BeautifulSoup

def fetch_search_page(keyword: str) -> str:
    """
    做 POST 查詢，把查詢結果頁 HTML 拿回來。
    """
    url = "https://judgment.judicial.gov.tw/FJUD/Default_AD.aspx"
    # 第一步先 GET 原始頁面以擷取隱藏欄位值
    resp0 = requests.get(url)
    resp0.raise_for_status()
    soup0 = BeautifulSoup(resp0.text, "html.parser")

    def get_input_val(name):
        tag = soup0.select_one(f"input[name='{name}']")
        return tag["value"] if (tag and tag.has_attr("value")) else ""

    vs = get_input_val("__VIEWSTATE")
    ev = get_input_val("__EVENTVALIDATION")
    vgen = get_input_val("__VIEWSTATEGENERATOR")
    ven = get_input_val("__VIEWSTATEENCRYPTED")

    # 構造 POST 表單參數
    form = {
        "__VIEWSTATE": vs,
        "__EVENTVALIDATION": ev,
        "__VIEWSTATEGENERATOR": vgen,
        "__VIEWSTATEENCRYPTED": ven,

        # 查詢條件欄位（這些可能要根據 devtools 查看實際名稱）
        "jud_kw": keyword,
        # 也可以在這裡指定法院、案件類別、年度、案由、主文等欄位
        # e.g. "jud_court": "TCH", 或 "jud_sys": "M"（刑事）等

        # 查詢按鈕欄位
        "ctl00$cp_content$btnQry": "送出查詢"
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": url
    }

    resp = requests.post(url, data=form, headers=headers)
    resp.raise_for_status()
    return resp.text

def build_scraper(html: str):
    """
    用 AutoScraper 針對查詢結果頁 HTML 建構 scraper, 抽取你目標的標題／案號字串。
    """
    # 這裡填你已知的範例標題／案號，AutoScraper 用它來學習 pattern
    desired = [
        "臺灣高等法院 臺中分院 113 年度 金上訴 字第 607 號 刑事判決（143K）",
        "臺灣高等法院 臺中分院 113 年度 金上訴 字第 606 號 刑事判決（143K）"
    ]
    scraper = AutoScraper()
    result = scraper.build(html, desired)
    print("AutoScraper build 的 result:", result)
    return scraper

def extract_titles(scraper: AutoScraper, html: str):
    """
    用已建立的 scraper 去該頁 HTML 抽出所有匹配的標題／案號字串
    """
    return scraper.get_result_similar(html)

def main():
    # 你要查的關鍵字（可以是案號、部分關鍵字等）
    kw = "113 年度 金上訴 字第 607 號"
    html = fetch_search_page(kw)
    # （可選）把 HTML 寫檔看回傳內容
    with open("search_result.html", "w", encoding="utf-8") as f:
        f.write(html)

    scraper = build_scraper(html)
    extracted = extract_titles(scraper, html)
    print("抽出的標題／案號：")
    for x in extracted:
        print(" -", x)

if __name__ == "__main__":
    main()
