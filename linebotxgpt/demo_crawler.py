import time
import requests
from bs4 import BeautifulSoup

def fetch_additional_content(url):
    """從第一筆資料的連結抓取更多詳細內容。"""
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/85.0.4183.83 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 假設主要內容位於 <article> 或 <div> 中，若無則抓取 <p> 段落
        content = ""
        if article := soup.find('article'):
            content = " ".join(p.get_text() for p in article.find_all('p'))
        elif main_div := soup.find('div', class_='main-content'):
            content = " ".join(p.get_text() for p in main_div.find_all('p'))
        else:
            content = " ".join(p.get_text() for p in soup.find_all('p'))

        return content if content else "No additional content available."
    except Exception as e:
        print(f"Error fetching additional content from {url}: {e}")
        return "Error fetching content."

def bing_search(query, num_results=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    url = f"https://www.bing.com/search?q={query}&count={num_results}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for idx, item in enumerate(soup.find_all('li', class_='b_algo')):
        print(f"Processing result {idx + 1}...")
        title = item.find('h2').text
        link = item.find('a')['href']

        # 嘗試取得完整的描述
        description = ""
        if description_tag := item.find('p'):
            description = description_tag.get_text()
        elif caption_div := item.find('div', class_='b_caption'):
            description = " ".join(span.get_text() for span in caption_div.find_all('span'))

        if not description:
            description = "No description available."

        # 若是第一筆資料且有連結，進一步抓取內文
        additional_content = ""
        if link:
            additional_content = fetch_additional_content(link)

        results.append({
            'title': title,
            'link': link,
            'description': description,
            'additional_content': additional_content
        })

        # time.sleep(2)

    return results

# 測試搜尋
search_results = bing_search("今天颱風", num_results=3)
for result in search_results:
    print(f"Title: {result['title']}\nLink: {result['link']}\n"
          f"Description: {result['description']}\n"
          f"Additional Content: {result['additional_content'][:500]}...\n")  # 顯示前 500 字
