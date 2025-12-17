# Python基礎教學 v3

這份教材以「初學者看得懂、做得出來」為目標：每個語法段落都包含**說明**、**一個範例題目（含參考解答）**、以及**兩個練習題**。

建議學習方式：

1. 先看「說明」理解概念
2. 自己先做「範例題目」再對照解答
3. 完成「練習題」並自己驗證輸出

---

## 目錄

1. 甚麼是程式語言? Python介紹
    - 到底該學哪個程式語言?
    - AI已經很強大了,我還需要學程式語言嗎?
2. 簡單的應用場景介紹
3. Python安裝與設定
4. 執行環境介紹, IDE介紹
5. Python基本語法
    - 變數與資料型態
    - 運算子
    - 控制流程
        1. if
        2. for
        3. break
        4. continue
        5. pass
        6. match
    - 函式
    - 資料結構 (串列, 字典, 集合, 元組)
    - 模組
    - 字串處理
6. Exception處理
7. Excel檔案操作
8. 物件導向程式設計基礎
    - 類別與物件
    - 繼承與多型

---

## 1. 甚麼是程式語言? Python介紹

### 1.1 甚麼是程式語言？

你可以把「程式語言」想成：**跟電腦溝通的一套規則**。電腦本質上只會照著指令做事，而程式語言就是用來把「你想做的事情」寫成電腦能執行的步驟。

一個程式通常包含：

- **輸入（Input）**：從鍵盤、檔案、網路、資料庫取得資料
- **處理（Process）**：計算、判斷、整理、分類
- **輸出（Output）**：印在螢幕、寫入檔案、回傳到網頁、產生報表

### 1.2 為什麼選 Python？

Python 常被當作入門首選，原因包括：

- **語法接近人類語言**：可讀性高
- **用途廣**：自動化、資料分析、網頁後端、爬蟲、AI/機器學習
- **社群大、資源多**：遇到問題更容易找到答案

> 本教材假設你使用 Python 3.10 以上（因為會用到 `match`）。

### 1.3 到底該學哪個程式語言？

選語言最實用的方式是：**先想你要做什麼**。

- 想做網頁前端（畫面互動）：JavaScript / TypeScript
- 想做網站後端、API：Python / Node.js / Java / C#
- 想做手機 App：Swift（iOS）/ Kotlin（Android）
- 想做資料分析、AI、自動化：Python（最常見）
- 想做遊戲或高效能：C++ / C#

如果你現在還不確定方向，Python 的「通用性」會讓你學了不吃虧：學到的基本概念（變數、條件、迴圈、函式、資料結構）之後換語言也能用。

### 1.4 AI 已經很強大了，我還需要學程式語言嗎？

需要，而且比以前更重要。AI 工具（如 ChatGPT、GitHub Copilot）確實能幫你生成程式碼，但這就像「有了 GPS 導航」並不代表「不需要會開車」一樣。以下用實際案例說明：

#### 案例一：你要能把需求說清楚

**情境**：你想寫一個程式，自動整理資料夾裡的檔案，把 Excel 檔案移到「報表」資料夾，圖片移到「圖片」資料夾。

如果你不懂程式：
- 可能會問 AI：「幫我寫一個整理檔案的程式」
- AI 給你一段程式，但可能沒考慮到：檔案重名怎麼辦？資料夾不存在要不要自動建？是要移動還是複製？

如果你懂程式：
- 你會明確描述：「用 Python 寫一個腳本，遍歷指定資料夾，根據副檔名（.xlsx, .xls 移到『報表』，.jpg, .png 移到『圖片』），如果目標資料夾不存在就建立，檔名重複時加上時間戳記」
- AI 根據這個清晰的需求，產生的程式一次到位

**結論**：懂程式概念（檔案操作、迴圈、條件判斷）才能寫出精確的 prompt，讓 AI 理解你真正的需求。

#### 案例二：你要能判斷對不對

**情境**：你請 AI 寫一個「計算 1 到 100 總和」的程式。

AI 可能給你：
```python
total = 0
for i in range(100):
    total += i
print(total)
```

如果你不懂程式，你可能覺得「看起來沒問題」就直接用了。但實際上這段程式只算到 99（因為 `range(100)` 是 0 到 99）。

如果你懂程式，你會立刻發現：
- `range(100)` 產生的是 `[0, 1, 2, ..., 99]`，應該改成 `range(1, 101)`
- 或者你會測試輸出，發現結果是 4950 而不是正確答案 5050

**結論**：AI 會犯錯，而且常常是「看起來合理但實際上有 bug」的錯。你需要能讀懂程式碼、知道如何測試，才能驗證 AI 的輸出。

#### 案例三：你要能整合與維護

**情境**：公司要你做一個「每天早上自動產生銷售報表」的系統。

這個任務不是「寫一段程式」就結束了，你需要：

1. **從資料庫取資料**：需要知道如何連接資料庫、寫 SQL 查詢
2. **處理與計算**：用 pandas 整理資料、算總和、排名
3. **產生 Excel**：用 openpyxl 或 pandas 輸出格式化的報表
4. **發送郵件**：把報表寄給主管
5. **設定排程**：讓程式每天早上 8 點自動執行
6. **錯誤處理**：資料庫連不上怎麼辦？檔案產生失敗要通知誰？

AI 可以幫你寫每一個「部分」，但把這些部分「串起來、除錯、維護」需要你懂：
- 模組如何 import 和使用
- 錯誤如何捕捉（try/except）
- 檔案路徑如何處理
- 環境變數與設定檔如何管理

**結論**：真實專案是多個功能的組合，需要長期維護。你要能理解整個架構、知道哪裡可能出錯、如何優化效能。

#### 案例四：AI 生成的程式碼需要你理解才能修改

**情境**：你用 AI 生成了一個爬蟲程式，成功抓到網頁資料。但三個月後，網站改版了，程式失效。

如果你不懂程式：
- 你只能再去問 AI，但 AI 不知道網站具體改了什麼，可能給你錯誤的修正方向

如果你懂程式：
- 你會檢查：是 HTML 結構變了？還是網站加了反爬蟲機制？
- 你會用瀏覽器開發者工具查看新的 HTML 結構
- 你會修改對應的 CSS selector 或 XPath
- 你可以精確地請 AI 幫你重寫特定部分

**結論**：程式不是寫完就不會變的。需求會改、外部系統會改、你自己的理解也會更深入。懂程式才能「持續改進」而不是「每次都重頭來過」。

#### 總結：學程式不是跟 AI 競爭，而是讓你能駕馭 AI

把 AI 想成「超強助手」，而你是「專案負責人」：

- **助手很厲害**：可以快速寫出大量程式碼
- **但負責人需要懂業務**：知道要做什麼、判斷對不對、如何整合
- **最強組合**：懂程式的人 + AI 工具 = 10 倍生產力

實際工作中最有競爭力的人，不是「完全靠自己寫」，也不是「完全靠 AI」，而是：

1. 用程式知識精確表達需求
2. 用 AI 快速產生初版程式碼
3. 用程式能力檢查、測試、修改
4. 用經驗整合成完整可靠的系統

**一句話總結**：AI 時代，懂程式的人不是被取代，而是能做到以前 10 個人才能做到的事。不懂程式的人，連 AI 給的答案對不對都看不出來。

---

## 2. 簡單的應用場景介紹

下面是 Python 常見的「入門就做得出來」的應用：

1. **自動化**
   - 批次改檔名、整理資料夾
   - 讀寫 Excel、產生報表
   - 每天定時下載資料
2. **資料處理與分析**
   - 清理 CSV/Excel
   - 計算平均、排名、趨勢
3. **網路爬蟲**（注意網站規範）
   - 把網頁上的表格抓下來整理
4. **網頁後端 / API**
   - 用 Flask/FastAPI 提供資料查詢
5. **AI 應用**
   - 串接大型語言模型 API
   - 建立簡單的聊天機器人

初學者最推薦從「自動化 + 讀寫檔案」開始，因為能很快看見成果。

---

## 3. Python安裝與設定（Windows）

### 3.1 安裝 Python

建議做法：使用官方安裝程式。

安裝重點：

1. 安裝時勾選 **Add Python to PATH**
2. 建議安裝 Python 3.11 或 3.12（新版本效能與相容性通常更好）

### 3.2 驗證是否安裝成功

打開 PowerShell 後輸入：

```powershell
python --version
pip --version
```

如果你電腦同時裝了多個 Python，有些環境需要改用：

```powershell
py -V
py -m pip --version
```

### 3.3 建立專案與虛擬環境（推薦）

「虛擬環境」可以把每個專案用到的套件隔離開來，避免版本互相打架。

```powershell
cd "c:\Users\purem\OneDrive\文件\TextBook"
mkdir my_python_project
cd my_python_project

py -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
```

看到命令列前面出現 `(.venv)` 通常表示啟動成功。

---

## 4. 執行環境介紹, IDE介紹

### 4.1 你會遇到的「執行方式」

1. **互動式（REPL）**：
   - 直接輸入一行跑一行，適合試語法
2. **執行檔案（.py）**：
   - 寫成程式檔，適合做完整功能
3. **Notebook（.ipynb）**：
   - 常用在資料分析與教學（Jupyter）

### 4.2 IDE 是什麼？

IDE（整合開發環境）可以幫你：

- 自動排版、提示錯誤
- 斷點除錯（Debug）
- 管理專案與套件

常見選擇：

- **VS Code**：輕量、外掛多、很常用
- **PyCharm**：功能完整，較重

### 4.3 VS Code 建議設定

1. 安裝 Python 外掛（Microsoft Python）
2. 選擇解譯器（Interpreter）為你的 `.venv`
3. 用內建終端機執行：

```powershell
python your_script.py
```

---

## 5. Python基本語法

本章每一節都會用「說明 → 範例題目（含解答）→ 練習題」的方式。

### 5.1 變數與資料型態

#### 說明

**變數**就是替資料取名字，讓你之後能拿來用。

Python 常見資料型態：

- `int`：整數，例如 `10`
- `float`：小數，例如 `3.14`
- `str`：字串，例如 `"hello"`
- `bool`：布林值（真假），`True` / `False`
- `None`：代表「沒有值」

你可以用 `type()` 看型態：

```python
x = 10
print(type(x))  # <class 'int'>
```

#### 範例題目：計算總價

題目：

輸入商品單價 `price` 與數量 `qty`，計算總價 `total`，並印出：

`單價=..., 數量=..., 總價=...`

參考解答：

```python
price = 35
qty = 4

total = price * qty
print(f"單價={price}, 數量={qty}, 總價={total}")
```

#### 練習題

1. 設定 `height_cm = 170`、`weight_kg = 65`，計算 BMI（$BMI=weight/(height_m^2)$），印出到小數點後 2 位。
2. 讓使用者輸入名字與年齡（用 `input()`），印出：`你好 {名字}，明年你 {年齡+1} 歲`。

---

### 5.2 運算子

#### 說明

常用運算子：

- 算術：`+ - * / // % **`
  - `/`：除法（會有小數）
  - `//`：整除（只取商）
  - `%`：取餘數
  - `**`：次方
- 比較：`== != > < >= <=`（結果是 `True/False`）
- 邏輯：`and or not`

#### 範例題目：判斷能否被 3 整除

題目：

給定整數 `n`，如果 `n` 可以被 3 整除，印出 `True`，否則印出 `False`。

參考解答：

```python
n = 21
print(n % 3 == 0)
```

#### 練習題

1. 給定 `a=17`、`b=5`，分別印出 `a/b`、`a//b`、`a%b`。
2. 給定分數 `score`，判斷是否在 60 到 100（含）之間，印出布林值。

---

### 5.3 控制流程

控制流程讓程式能「做選擇」或「重複執行」。

#### 5.3.1 if

##### 說明

`if` 用來做判斷：條件成立才做某件事。

```python
if 條件:
    # 條件成立做這裡
else:
    # 否則做這裡
```

##### 範例題目：成績等第

題目：

給定 `score`，

- `>= 90` 印 `A`
- `>= 80` 印 `B`
- `>= 70` 印 `C`
- 否則印 `D`

參考解答：

```python
score = 83

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
else:
    print("D")
```

##### 練習題

1. 輸入年齡 `age`：`< 18` 印 `未成年`，否則印 `成年`。
2. 輸入兩個數字 `x, y`，印出較大的那個（相等就印 `一樣大`）。

---

#### 5.3.2 for

##### 說明

`for` 常用來「跑一段範圍」或「走訪序列（例如串列、字串）」。

```python
for i in range(5):
    print(i)  # 0~4
```

##### 範例題目：計算 1 到 n 的總和

題目：

給定 `n`，用 `for` 計算 `1+2+...+n`。

參考解答：

```python
n = 10
total = 0

for i in range(1, n + 1):
    total += i

print(total)
```

##### 練習題

1. 用 `for` 印出 1 到 100 之間所有偶數。
2. 給定字串 `s = "python"`，用 `for` 逐字印出每個字母。

---

#### 5.3.3 break

##### 說明

`break` 用來「提前結束迴圈」。

##### 範例題目：找到第一個能被 7 整除的數

題目：

從 1 開始往上找，找到第一個能被 7 整除、且同時能被 5 整除的數字，找到後印出並停止。

參考解答：

```python
for n in range(1, 10000):
    if n % 7 == 0 and n % 5 == 0:
        print(n)
        break
```

##### 練習題

1. 從 1 開始找，找到第一個平方大於 500 的整數 `n`，印出 `n` 並停止。
2. 用 `for` 走訪一個串列 `nums=[3, 8, 2, 9, 7]`，找到 `9` 就印 `found` 然後停止。

---

#### 5.3.4 continue

##### 說明

`continue` 用來「跳過本次迴圈剩下的程式」，直接進入下一次。

##### 範例題目：加總奇數

題目：

將 1 到 100 的奇數加總。

參考解答：

```python
total = 0
for n in range(1, 101):
    if n % 2 == 0:
        continue
    total += n

print(total)
```

##### 練習題

1. 印出 1 到 50，但遇到 3 的倍數不要印（跳過）。
2. 走訪字串 `"a1b2c3"`，只印出其中的字母（略過數字）。

---

#### 5.3.5 pass

##### 說明

`pass` 表示「先留空」，讓程式在語法上完整但暫時不做事。常用於：

- 先把架構寫好
- 之後再補內容

##### 範例題目：先建立判斷架構

題目：

寫一個程式：如果 `mode == "dev"` 先留空；如果 `mode == "prod"` 印出 `running`。

參考解答：

```python
mode = "dev"

if mode == "dev":
    pass
elif mode == "prod":
    print("running")
```

##### 練習題

1. 建立一個函式 `todo()`，先用 `pass` 佔位（不要報錯）。
2. 用 `if/elif/else` 建立三種狀態的架構，先全部 `pass`，之後再補功能。

---

#### 5.3.6 match（Python 3.10+）

##### 說明

`match` 是「模式比對」，很像其他語言的 switch，但更強。

```python
match value:
    case 1:
        ...
    case 2:
        ...
    case _:
        ...  # 預設
```

##### 範例題目：星期轉中文

題目：

給定 `day`（1~7），印出對應中文：1=一、2=二...7=日，其它印出 `輸入錯誤`。

參考解答：

```python
day = 6

match day:
    case 1:
        print("星期一")
    case 2:
        print("星期二")
    case 3:
        print("星期三")
    case 4:
        print("星期四")
    case 5:
        print("星期五")
    case 6:
        print("星期六")
    case 7:
        print("星期日")
    case _:
        print("輸入錯誤")
```

##### 練習題

1. 用 `match` 做簡單計算器：`op` 可能是 `+ - * /`，根據 `op` 計算 `a op b`。
2. 用 `match` 根據字串 `"start"/"stop"/"pause"` 印出不同訊息，其它印 `unknown`。

---

### 5.4 函式

#### 說明

函式（function）就是把一段可以重複用的程式「包起來」，取一個名字。

```python
def add(a, b):
    return a + b
```

重點：

- **參數**：函式需要的輸入
- **回傳值**：函式算完的結果

#### 範例題目：寫一個判斷偶數的函式

題目：

寫 `is_even(n)`，如果 `n` 是偶數回傳 `True`，否則回傳 `False`。

參考解答：

```python
def is_even(n: int) -> bool:
    return n % 2 == 0


print(is_even(10))  # True
print(is_even(7))   # False
```

#### 練習題

1. 寫 `circle_area(r)` 回傳圓面積（$\pi r^2$），並呼叫它印出半徑 3、5 的結果。
2. 寫 `count_vowels(s)` 回傳字串中母音（a,e,i,o,u）數量（不分大小寫）。

---

### 5.5 資料結構（串列、字典、集合、元組）

#### 說明

資料結構用來「把多個資料放在一起」。

- 串列 `list`：有順序、可修改
  - 例：`["apple", "banana"]`
- 元組 `tuple`：有順序、通常不修改
  - 例：`("台北", "台中")`
- 字典 `dict`：用 key 找 value
  - 例：`{"name": "Amy", "age": 18}`
- 集合 `set`：不重複、無順序
  - 例：`{1, 2, 3}`

#### 範例題目：統計成績平均

題目：

給定成績串列 `scores`，計算平均並印出。

參考解答：

```python
scores = [80, 90, 75, 88]

avg = sum(scores) / len(scores)
print(avg)
```

#### 練習題

1. 給一個字典 `student = {"name": "Tom", "scores": [70, 85, 90]}`，印出名字與平均分數。
2. 給兩個集合 `a={1,2,3,4}`、`b={3,4,5}`，印出交集、聯集、差集（`a-b`）。

---

### 5.6 模組

#### 說明

模組就是「把程式碼整理在檔案裡，讓別人/自己可以重複使用」。

- 內建模組（不用安裝）：`math`, `random`, `datetime`, `pathlib`...
- 第三方模組（需要安裝）：`requests`, `pandas`, `openpyxl`...

常見用法：

```python
import math
print(math.sqrt(9))

from datetime import datetime
print(datetime.now())
```

#### 範例題目：隨機抽籤

題目：

用 `random` 從名單中隨機抽一個人。

參考解答：

```python
import random

names = ["Amy", "Bob", "Cindy", "David"]
winner = random.choice(names)
print(winner)
```

#### 練習題

1. 用 `math` 計算 `sqrt(2)` 並印出小數點後 4 位。
2. 用 `datetime` 印出今天日期（年-月-日）。

---

### 5.7 字串處理

#### 說明

字串（`str`）非常常用，常見操作：

- 取長度：`len(s)`
- 切片：`s[start:end]`
- 分割：`s.split(",")`
- 取代：`s.replace("a", "b")`
- 去空白：`s.strip()`
- 轉大小寫：`s.lower()` / `s.upper()`
- f-string 格式化：`f"...{var}..."`

#### 範例題目：Email 簡單檢查

題目：

給定字串 `email`，檢查是否同時包含 `@` 與 `.`，如果是印出 `OK`，否則印出 `Invalid`。

參考解答：

```python
email = "test@example.com"

if "@" in email and "." in email:
    print("OK")
else:
    print("Invalid")
```

#### 練習題

1. 給定 `s = "  Hello, Python  "`，去除前後空白後轉成小寫並印出。
2. 給定 `csv_line = "Tom,80,90,70"`，用 `split` 解析後印出名字與三科平均。

---

## 6. Exception處理

### 說明

程式執行時可能出錯，例如：

- 使用者輸入不是數字
- 檔案不存在
- 除以 0

Exception（例外）處理讓程式「出錯時不會直接崩潰」，你可以：

- 顯示友善訊息
- 做補救處理
- 或記錄錯誤

基本語法：

```python
try:
    # 可能出錯的程式
except 某種錯誤:
    # 發生該錯誤時怎麼做
else:
    # 沒出錯才會跑
finally:
    # 不管有沒有出錯都會跑（常用於釋放資源）
```

### 範例題目：安全的數字除法

題目：

讓使用者輸入 `a` 與 `b`，印出 `a/b`。若輸入不是數字或 `b=0`，要印出友善訊息。

參考解答：

```python
try:
    a = float(input("請輸入 a: "))
    b = float(input("請輸入 b: "))
    result = a / b
except ValueError:
    print("輸入錯誤：請輸入數字")
except ZeroDivisionError:
    print("不能除以 0")
else:
    print(f"結果：{result}")
```

### 練習題

1. 讀取檔案 `data.txt` 並印出內容；若檔案不存在，要印出 `找不到檔案`。
2. 寫一段程式把使用者輸入轉成整數；若失敗要一直請他重輸，直到成功為止（提示：`while True` + `try/except`）。

---

## 7. Excel檔案操作

### 說明

Python 操作 Excel 常見方式：

1. **openpyxl**：讀寫 `.xlsx`（最常見、入門友善）
2. **pandas**：資料分析很強，讀寫 Excel 也方便（底層常搭配 openpyxl）

安裝（在啟動虛擬環境後）：

```powershell
python -m pip install openpyxl pandas
```

### 範例題目：建立一個簡單的成績表 Excel

題目：

用 `openpyxl` 建立 `scores.xlsx`，內容如下：

- A1:B1 為標題：`Name`, `Score`
- 從第 2 列開始寫入三筆資料：`Tom 80`, `Amy 92`, `Bob 75`
- 最後再寫一列 `Average` 與平均分數

參考解答：

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Scores"

ws.append(["Name", "Score"])
rows = [
    ["Tom", 80],
    ["Amy", 92],
    ["Bob", 75],
]

for r in rows:
    ws.append(r)

avg = sum(score for _, score in rows) / len(rows)
ws.append(["Average", avg])

wb.save("scores.xlsx")
print("已輸出 scores.xlsx")
```

### 練習題

1. 讀取 `scores.xlsx`，把所有分數加總並印出總分與平均。
2. 用 `pandas` 讀取 Excel，新增一欄 `Pass`（分數 >= 60 為 True），再輸出成 `scores_with_pass.xlsx`。

---

## 8. 物件導向程式設計基礎

### 8.1 類別與物件

#### 說明

物件導向（OOP）把程式世界想成由「物件」組成。

- **類別（class）**：物件的藍圖（定義有哪些資料、有哪些行為）
- **物件（object / instance）**：照著藍圖做出來的實體

類別裡常見：

- 屬性（attributes）：這個物件「有什麼資料」
- 方法（methods）：這個物件「會做什麼事」

#### 範例題目：建立 `Student` 類別

題目：

建立 `Student`：

- 屬性：`name`、`scores`（串列）
- 方法：`average()` 回傳平均分數

建立兩個學生並印出平均。

參考解答：

```python
class Student:
    def __init__(self, name: str, scores: list[int]):
        self.name = name
        self.scores = scores

    def average(self) -> float:
        return sum(self.scores) / len(self.scores)


s1 = Student("Tom", [80, 70, 90])
s2 = Student("Amy", [95, 88, 92])

print(s1.name, s1.average())
print(s2.name, s2.average())
```

#### 練習題

1. 寫一個 `Rectangle` 類別，有 `width`、`height`，提供 `area()` 與 `perimeter()`。
2. 寫一個 `BankAccount` 類別，有 `balance`，提供 `deposit(amount)`、`withdraw(amount)`（餘額不足要提示）。

---

### 8.2 繼承與多型

#### 說明

**繼承（Inheritance）**：用現有類別當基底，延伸出更具體的類別。

- 父類別（base / parent）提供共用功能
- 子類別（subclass / child）可以新增或覆寫（override）方法

**多型（Polymorphism）**：不同類別的物件可以用「相同的方法名稱」被呼叫，表現出各自的行為。

#### 範例題目：不同員工計算薪資

題目：

建立 `Employee` 父類別與兩個子類別：

- `FullTimeEmployee`：月薪固定
- `PartTimeEmployee`：時薪 * 工時

都提供 `pay()` 回傳薪資，並用同一段程式走訪清單印出每個人的薪資（多型）。

參考解答：

```python
class Employee:
    def __init__(self, name: str):
        self.name = name

    def pay(self) -> float:
        raise NotImplementedError()


class FullTimeEmployee(Employee):
    def __init__(self, name: str, monthly_salary: float):
        super().__init__(name)
        self.monthly_salary = monthly_salary

    def pay(self) -> float:
        return self.monthly_salary


class PartTimeEmployee(Employee):
    def __init__(self, name: str, hourly_wage: float, hours: float):
        super().__init__(name)
        self.hourly_wage = hourly_wage
        self.hours = hours

    def pay(self) -> float:
        return self.hourly_wage * self.hours


employees = [
    FullTimeEmployee("Amy", 52000),
    PartTimeEmployee("Bob", 220, 60),
]

for e in employees:
    print(e.name, e.pay())
```

#### 練習題

1. 設計 `Animal` 父類別與 `Dog`、`Cat` 子類別，各自覆寫 `speak()`，走訪清單印出叫聲。
2. 設計 `Shape` 父類別與 `Circle`、`Rectangle` 子類別，提供 `area()`；用多型計算所有形狀面積總和。

---

## 附錄：初學者常見問題

### Q1：為什麼我的縮排會報錯？

Python 用「縮排」表示程式區塊，同一層級必須對齊。建議使用 4 個空格，不要混用 Tab。

### Q2：我輸入中文路徑/檔名會不會有問題？

大多數情況沒問題，但遇到套件或系統設定差異時可能出現編碼問題。初學時可以先用英文檔名，等熟悉後再處理中文情境。

