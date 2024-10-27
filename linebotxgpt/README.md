# linebot 加入爬蟲的做法

## Step1
demo_crawler.py 是我們的爬蟲原始檔案
要先測試可不可以執行

最下面倒數第五行,是呼叫包裝好的爬蟲的地方

```
search_results = bing_search("勞動部建議月薪", num_results=5)
```

這邊可以修改關鍵字,和要爬的筆數

上面的方法是呼叫bing_search這個方法,and fetch_additional_content這個方法是我們包裝好的爬蟲方法

我們會需要把上述這兩個方法複製到gpt_helper

## Step2 複製過去之後,我們要修改一下

### 第一步 需要安裝套件
### 第二步 需要縮排
### 第三步 bing_search這個方法的參數要改成
```
def bing_search(self, query, num_results=5):
```
### 第四步 fetch_additional_content這個方法的參數要改成
```
def fetch_additional_content(self, url):
```

### 第五步 bing_search這個方法裡面呼叫的時候,要改成用self呼叫

### 第六步 修改原先的QueryGPT的方法,加入爬蟲的部分
```
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
```


## 附註 安裝套件
pip install bs4
pip install requests