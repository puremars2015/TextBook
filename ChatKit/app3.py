import requests

# API endpoints
AUTH_URL = "https://data.judicial.gov.tw/jdg/api/Auth"
JLIST_URL = "https://data.judicial.gov.tw/jdg/api/JList"
JDOC_URL = "https://data.judicial.gov.tw/jdg/api/JDoc"

def get_token(user: str, password: str) -> str:
    payload = {"user": user, "password": password}
    resp = requests.post(AUTH_URL, json=payload)
    resp.raise_for_status()
    j = resp.json()
    if "token" in j:
        return j["token"]
    else:
        raise RuntimeError("Auth failed: " + str(j))

def get_jid_list(token: str) -> list:
    payload = {"token": token}
    resp = requests.post(JLIST_URL, json=payload)
    resp.raise_for_status()
    j = resp.json()
    # 格式可能是 { "DATE": "...", "LIST": [...] } 的列表形式
    # 你要看 j 的結構，這裡假設 LIST 欄位是你要的 jid 清單
    jid_all = []
    for rec in j:
        if "LIST" in rec:
            jid_all.extend(rec["LIST"])
    return jid_all

def get_judgment(token: str, jid: str) -> dict:
    payload = {"token": token, "j": jid}
    resp = requests.post(JDOC_URL, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    user = "你的帳號"
    password = "你的密碼"
    token = get_token(user, password)
    print("取得 token:", token)

    jid_list = get_jid_list(token)
    print("最近有變動的裁判書 jid 數量:", len(jid_list))
    if not jid_list:
        print("沒有變動紀錄，無法取得 journ")
        return

    # 比方說取第一個
    jid0 = jid_list[0]
    print("使用的 jid0：", jid0)

    doc = get_judgment(token, jid0)
    # doc 裡面會有全文 text, 或 PDF 的下載網址
    print("裁判書內容：", doc.get("JFULLCONTENT") or doc.get("JFULLPDF"))
    # 你可以把 doc 回傳給 GPT API 分析

if __name__ == "__main__":
    main()
