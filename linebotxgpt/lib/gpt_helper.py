

# pip install openai
from openai import OpenAI
from lib.sqlite_helper import SQLiteHelper
import my_config
from datetime import datetime
import requests
from bs4 import BeautifulSoup




api_key = my_config.section['OPEN_AI']


class MyGPT:


    __model__ = "gpt-4o-mini"
    __advanced_model__ = "gpt-4o"


    def __init__(self):
        self.openai = OpenAI(api_key=api_key)


    def __extract_text_between_markers(self, text, start_marker, end_marker):
        start_index = text.find(start_marker)
        end_index = text.find(end_marker, start_index)


        if start_index != -1 and end_index != -1:
            start_index += len(start_marker)
            return text[start_index:end_index].strip()
        else:
            return "Markers not found in the text."


    def AskGPT(self, msg) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=2,
            messages=[
                {"role": "user", "content": f"{msg}"}
            ]
        )
        return completion.choices[0].message.content
    
    def QueryGPT(self, msg) -> str:
        now = datetime.now()

        # 使用爬蟲來查詢相關資訊
        queryResult = self.bing_search(msg)

        completion = self.openai.chat.completions.create(
            model=self.__model__,
            messages=[
                {"role": "system", "content": f"現在是{now}"},
                {"role": "user", "content": f"{queryResult}"},
                {"role": "user", "content": f"{msg}"}
            ],
            frequency_penalty=0, # 這次我們不調頻率懲罰
            presence_penalty=0,  # 給重複詞彙大大的壓力
            max_tokens=200
        )
        rm = completion.choices[0].message.content
        print(rm)
        return rm
   
    def CalGPT(self, msg) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=0.5,
            messages=[
                {"role": "system", "content": "你是一個計算機,依據提示進行數學運算"},
                {"role": "user", "content": f"請問9.11跟9.9哪一個比較大?"},
                {"role": "assistant", "content": "9.11 比 9.9 大。因為在小數點後的第一位數字上，9.11 的 1 大於 9.9 的 0，所以 9.11 的值更大。"},
                {"role": "user", "content": "你說錯了,9.9比較大,你先忽略小數點,然後把整個數字從左邊的數字開始比較"},
                {"role": "assistant", "content": "9.9比9.11 大。因為左邊第一個數字是9,兩者一樣,所以再比較第二個數字,9比1大,所以9.9比9.11大。"},
                {"role": "user", "content": f"{msg}"}


            ]
        )
        return completion.choices[0].message.content
   
    def FineTurnCalGPT(self, msg) -> str:
        completion = self.openai.chat.completions.create(
            model='ft:gpt-4o-mini-2024-07-18:personal::9xVI9AgM',
            frequency_penalty=0.5,
            messages=[
                {"role": "user", "content": f"{msg}"}
            ]
        )
        return completion.choices[0].message.content


    def TranDemoGPT(self, msg) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=2,
            messages=[
                {"role": "user", "content": f"請幫我下面的句子翻譯成英文:人山人海"},
                {"role": "assistant", "content": '"人山人海" 可以翻譯為 "a sea of people" 或者 "crowds of people."'},
                {"role": "user", "content": "請只要回應翻譯後的英文就好"},
                {"role": "assistant", "content": "a sea of people"},
                {"role": "user", "content": f"{msg}"}
            ]
        )
        return completion.choices[0].message.content


    def PromptCodeNoExecuteHelper(self, issue) -> str:
        return f'{issue},且在非main環境時不需要執行'


    def PromptHelperWithoutExecuteForCode(self, issue, file_name) -> str:
        return f'{issue} 並將其存為一個方法名稱為{file_name},且不需要執行'
   
    def PromptHelperForCode(self, issue, file_name) -> str:
        return f'{issue} 並將其存為一個方法名稱為{file_name},並顯示結果'
   
    def PromptHelperForAnalysisExcelCode(self, issue, file_name, output_file_name) -> str:
        return f'資料來源檔案為{file_name}, {issue}, 並將其儲存為另一個檔案{output_file_name}'


    def CodeGPT(self, issue) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=0.5,
            messages=[
                {"role": "system", "content": "你是一個程式碼產生器,依據提示產生Python程式碼,且不使用try...except語句,並將程式碼以<<<<與>>>>包住"},
                {"role": "user", "content": f"{issue}"}
            ]
        )
        text = completion.choices[0].message.content
        return self.__extract_text_between_markers(text, "<<<<", ">>>>")
   
    def FixCodeGPT(self, code, errMessage) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=0.5,
            messages=[
                {"role": "system", "content": "你是一個程式碼修復機,收到有錯誤的程式碼後會修復程式碼,且不使用try...except語句,並將程式碼以<<<<與>>>>包住"},
                {"role": "user", "content": f"執行有問題的程式碼:{code} "},
                {"role": "user", "content": f"錯誤訊息如下:{errMessage} "}
            ]
        )
        text = completion.choices[0].message.content
        return self.__extract_text_between_markers(text, "<<<<", ">>>>")
   
    def PipGPT(self, msg) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=0.5,
            messages=[
                {"role": "system", "content": "pip指令產生器,依據訊息產生對應所需的pip安裝指令,並將指令以<<<<與>>>>包住"},
                {"role": "user", "content": f"{msg}"}
            ]
        )
        text = completion.choices[0].message.content
        return self.__extract_text_between_markers(text, "<<<<", ">>>>")


    def TranslateGPT(self, msg) -> str:
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=0.5,
            messages=[
                {"role": "system", "content": "你是一個中文與英文的翻譯機,收到中文後會翻譯成英文,收到英文後會翻譯成中文"},
                {"role": "user", "content": f"{msg}"}
            ]
        )
        return completion.choices[0].message.content
   
    def MemoryGPT(self, msg) -> str:
        msgs = []
        db = SQLiteHelper('linebotxgpt.db')
        db.execute_query('INSERT INTO bot_memory (role,content,line_id) VALUES (?,?,?)', ('user', msg, 'no-key'))
        data = db.execute_read_query(f"SELECT role,content FROM bot_memory WHERE line_id = 'no-key' ORDER BY id")    
        msgs.extend([{'role': role, 'content': content} for role, content in data])
        completion = self.openai.chat.completions.create(
            model=self.__model__,
            frequency_penalty=0.5,
            messages=msgs
        )
        response_message = completion.choices[0].message.content
        db.execute_query('INSERT INTO bot_memory (role,content,line_id) VALUES (?,?,?)', ('assistant', response_message, 'no-key'))
        return response_message
   
    def UploadFile(self, training_file) -> str:
        response = self.openai.files.create(
            file=open(training_file, "rb"),
            purpose='fine-tune'
        )
        return response.id
   
    def FineTune(self, training_file_id) -> str:
        response = self.openai.fine_tuning.jobs.create(
            training_file=training_file_id,
            model='gpt-4o-mini-2024-07-18'
        )
        return response.id
   
    def RetrieveFineTune(self, fine_tune_id) -> str:
        return self.openai.fine_tuning.jobs.retrieve(fine_tune_id)

    def fetch_additional_content(self, url):
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

    def bing_search(self, query, num_results=3):
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
                additional_content = self.fetch_additional_content(link)

            results.append({
                'title': title,
                'link': link,
                'description': description,
                'additional_content': additional_content
            })

            # time.sleep(2)

        return results
