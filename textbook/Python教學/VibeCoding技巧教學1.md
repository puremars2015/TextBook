# Vibe Coding 技巧教學1 (以 Python 讀取兩個Excel的資料並合併為例)

本篇教你用「Vibe Coding」的方式（用 AI 輔助寫程式，但用規格與驗收把品質拉回來），在 **Windows + VS Code + Python** 環境做出一個能讀取、合併、輸出 Excel 的自動化腳本。

> 這篇不是「叫 AI 生一坨程式碼」；而是教你把 AI 變成可控的工程產線：每次只改一小步、每次都有驗收條件、每次都能回滾。

---

## 你會完成什麼（可驗收成果）

完成後，你應該能做到：

1. 在本機建立一個乾淨的 Python 虛擬環境（venv）
2. 用 pandas/openpyxl 讀取兩個不同的 Excel 檔案
3. 根據指定欄位（如「ID」或「員工編號」）合併資料
4. 將合併結果輸出為新的 Excel 檔案
5. 用「規格 + 驗收」驅動 AI 修改程式，而不是盲改
6. 碰到錯誤時，能用 traceback 把 AI 拉回正軌：定位根因 → 最小修補 → 重新驗收

---

## 適用對象與前置假設

- 你會基本命令列操作（PowerShell 或 CMD）
- 你會安裝 Python、能在 VS Code 開資料夾
- 你想做的是「能跑的 Excel 處理腳本」：先求跑得起來，再談優化與錯誤處理

本篇預設：

- OS：Windows
- Editor：VS Code
- Python：3.10+（建議 3.11/3.12 也可）

---

## Vibe Coding 的核心觀念（一句話）

**先寫規格（spec）與驗收（acceptance criteria），再叫 AI 產出最小可跑版本，最後用小步迭代把品質補回來。**

你要把 AI 當成「很快的實習生」，而不是「自動交付系統」：

- 你提供：需求、限制、檔案結構、驗收條件
- AI 產出：候選實作
- 你負責：驗收、把錯誤訊息給 AI、控制改動範圍

---

## Vibe Coding 標準流程（建議照順序跑）

### Step 0：先讓 AI 問你問題（避免亂猜）

如果你直接說「幫我合併兩個 Excel」，AI 會自己腦補一堆東西。
你要先讓它問你 2–5 個澄清問題，再開始寫。

### Step 1：寫清楚「規格」

規格至少包含：

- 功能（要做什麼）
- 範圍（不做什麼）
- 介面（輸入檔名、合併鍵、輸出檔名）
- 限制（Windows、不要 GUI、只能用常見套件…）

### Step 2：寫清楚「驗收條件」

驗收條件是「能用命令/檢查檔案測出來」的句子，例如：

- 執行後產生 `merged_output.xlsx` 檔案
- 輸出檔案包含兩個來源的所有欄位
- 根據「ID」欄位正確合併（用 left/inner/outer join）

### Step 3：請 AI 只產出「最小可跑版本」

最小版本的原則：

- 只做必要功能
- 先不做複雜的錯誤處理、資料清理、多檔案批次
- 先不引入一堆套件

### Step 4：跑起來 → 驗收 → 紀錄問題

不要靠「看程式碼覺得可以」；要跑、要測。

### Step 5：小步迭代（每次只改一件事）

每次迭代都要：

1. 說明你要改什麼
2. 說明不改什麼
3. 說明驗收方式
4. 要求 AI **只改動少數檔案**

---

## Prompt 模板庫（可直接複製）

你可以把下面這些模板存成 VS Code 的 snippet 或常用筆記。

### 模板 A：先問我澄清問題

```text
你要幫我做一個 Python 腳本，讀取兩個 Excel 檔並合併。
在開始寫任何程式碼前，請先問我 3 個你必須知道的澄清問題（只問問題，不要先寫解法）。
```

### 模板 B：規格 → 驗收 → 檔案樹 → 產出

```text
請依照以下規格完成專案。

【規格】
- 技術：Python + pandas
- OS：Windows
- 需求：
	1) 讀取 file1.xlsx（包含欄位：ID, Name, Department）
	2) 讀取 file2.xlsx（包含欄位：ID, Salary, Position）
	3) 根據 ID 欄位做 inner join 合併
	4) 輸出 merged_output.xlsx
- 不做：GUI、資料庫、複雜錯誤處理

【驗收條件】
- 執行後產生 merged_output.xlsx
- 輸出檔案包含所有欄位：ID, Name, Department, Salary, Position
- 只包含兩個檔案都有的 ID（inner join）

【輸出格式】
1) 先給我檔案結構（tree）
2) 再給每個檔案的完整內容
3) 最後給我 Windows PowerShell 的建立 venv、安裝、執行指令
```

### 模板 C：限制改動範圍（避免 AI 大改）

```text
請在不改動既有行為的前提下，完成以下修改。
限制：
- 只允許修改這 1 個檔案：merge_excel.py
- 不要新增新的外部套件
- 如果你覺得一定要新增檔案/套件，先停下來提出理由與替代方案
```

### 模板 D：我貼錯誤，請你用「根因→最小修補→驗收」

```text
我遇到錯誤，請你依序輸出：
1) 根因判斷（引用 traceback 的關鍵行）
2) 最小修補方案（改哪些檔案、改哪些行）
3) 我該怎麼驗收（給我 2~3 個命令或操作）

【環境】Windows + VS Code
【我做了什麼】<步驟>
【錯誤全文】
<貼上完整 traceback>
```

### 模板 E：請你幫我寫「測試/驗收」而不是只寫功能

```text
請不要直接加功能；請先幫我補上最小的驗收方式（例如檢查輸出檔案的內容），
再依照驗收去完成實作。
```

---

## 實作：Excel 合併腳本（從 0 到能跑）

下面用最小步驟做一個「能跑、能驗收」的 Excel 合併程式。

### 1) 建資料夾

在你要放專案的地方建立資料夾，例如：

```powershell
mkdir excel-merge-demo
cd excel-merge-demo
```

### 2) 建立並啟動 venv

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

如果你遇到 PowerShell 執行政策（ExecutionPolicy）阻擋，先用替代做法：

- 方案 1：改用 CMD 啟動

```bat
.venv\Scripts\activate.bat
```

- 方案 2：只對目前 PowerShell 視窗放行（較安全）

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 3) 安裝套件

```powershell
py -m pip install -U pip
py -m pip install pandas openpyxl
```

> 為什麼要 openpyxl？
> pandas 讀寫 .xlsx 格式需要額外的引擎，openpyxl 是最常用的選項。

### 4) 準備測試資料

建立兩個簡單的 Excel 檔案用於測試。

**方案 A：手動建立（用 Excel）**

建立 `file1.xlsx`：

| ID | Name  | Department |
|----|-------|------------|
| 1  | Alice | HR         |
| 2  | Bob   | IT         |
| 3  | Carol | Finance    |

建立 `file2.xlsx`：

| ID | Salary | Position      |
|----|--------|---------------|
| 1  | 50000  | Manager       |
| 2  | 60000  | Developer     |
| 4  | 55000  | Analyst       |

**方案 B：用 Python 產生測試資料（推薦）**

建立 `create_test_data.py`：

```python
from __future__ import annotations

import pandas as pd


def create_test_files():
	# 建立第一個測試檔案
	df1 = pd.DataFrame({
		"ID": [1, 2, 3],
		"Name": ["Alice", "Bob", "Carol"],
		"Department": ["HR", "IT", "Finance"]
	})
	df1.to_excel("file1.xlsx", index=False, engine="openpyxl")
	print("✓ 已建立 file1.xlsx")

	# 建立第二個測試檔案
	df2 = pd.DataFrame({
		"ID": [1, 2, 4],
		"Salary": [50000, 60000, 55000],
		"Position": ["Manager", "Developer", "Analyst"]
	})
	df2.to_excel("file2.xlsx", index=False, engine="openpyxl")
	print("✓ 已建立 file2.xlsx")


if __name__ == "__main__":
	create_test_files()
```

執行：

```powershell
py create_test_data.py
```

### 5) 建立 `merge_excel.py`

建立檔案 `merge_excel.py`，內容如下：

```python
from __future__ import annotations

import pandas as pd


def merge_excel_files(
	file1_path: str,
	file2_path: str,
	output_path: str,
	merge_on: str = "ID",
	how: str = "inner",
) -> None:
	"""
	讀取兩個 Excel 檔案並根據指定欄位合併。

	Args:
		file1_path: 第一個 Excel 檔案路徑
		file2_path: 第二個 Excel 檔案路徑
		output_path: 輸出檔案路徑
		merge_on: 合併依據的欄位名稱（預設 "ID"）
		how: 合併方式，可選 "inner", "left", "right", "outer"（預設 "inner"）
	"""
	try:
		# 讀取 Excel 檔案
		print(f"正在讀取 {file1_path}...")
		df1 = pd.read_excel(file1_path, engine="openpyxl")
		print(f"  ✓ 讀取成功，共 {len(df1)} 筆資料")

		print(f"正在讀取 {file2_path}...")
		df2 = pd.read_excel(file2_path, engine="openpyxl")
		print(f"  ✓ 讀取成功，共 {len(df2)} 筆資料")

		# 檢查合併欄位是否存在
		if merge_on not in df1.columns:
			raise ValueError(f"欄位 '{merge_on}' 不存在於 {file1_path}")
		if merge_on not in df2.columns:
			raise ValueError(f"欄位 '{merge_on}' 不存在於 {file2_path}")

		# 合併資料
		print(f"正在根據 '{merge_on}' 欄位進行 {how} join...")
		merged_df = pd.merge(df1, df2, on=merge_on, how=how)
		print(f"  ✓ 合併成功，共 {len(merged_df)} 筆資料")

		# 輸出結果
		print(f"正在輸出到 {output_path}...")
		merged_df.to_excel(output_path, index=False, engine="openpyxl")
		print(f"  ✓ 輸出成功！")

		# 顯示結果預覽
		print("\n合併結果預覽（前 5 筆）：")
		print(merged_df.head())

	except FileNotFoundError as e:
		print(f"❌ 錯誤：找不到檔案 - {e}")
		raise
	except ValueError as e:
		print(f"❌ 錯誤：{e}")
		raise
	except Exception as e:
		print(f"❌ 發生未預期的錯誤：{e}")
		raise


if __name__ == "__main__":
	# 預設參數
	FILE1 = "file1.xlsx"
	FILE2 = "file2.xlsx"
	OUTPUT = "merged_output.xlsx"
	MERGE_COLUMN = "ID"
	JOIN_TYPE = "inner"  # 可改為 "left", "right", "outer"

	print("=== Excel 檔案合併工具 ===\n")
	merge_excel_files(
		file1_path=FILE1,
		file2_path=FILE2,
		output_path=OUTPUT,
		merge_on=MERGE_COLUMN,
		how=JOIN_TYPE,
	)
	print("\n=== 完成 ===")
```

### 6) 執行

```powershell
py merge_excel.py
```

看到類似以下輸出就代表成功：

```text
=== Excel 檔案合併工具 ===

正在讀取 file1.xlsx...
  ✓ 讀取成功，共 3 筆資料
正在讀取 file2.xlsx...
  ✓ 讀取成功，共 3 筆資料
正在根據 'ID' 欄位進行 inner join...
  ✓ 合併成功，共 2 筆資料
正在輸出到 merged_output.xlsx...
  ✓ 輸出成功！

合併結果預覽（前 5 筆）：
   ID   Name Department  Salary    Position
0   1  Alice         HR   50000     Manager
1   2    Bob         IT   60000   Developer

=== 完成 ===
```

### 7) 驗收

**驗收項目 1：檢查輸出檔案是否存在**

```powershell
Test-Path merged_output.xlsx
```

應該回傳 `True`。

**驗收項目 2：用 Excel 打開檢查內容**

打開 `merged_output.xlsx`，確認：

- 包含欄位：ID, Name, Department, Salary, Position
- 只有 ID 為 1 和 2 的資料（因為用 inner join，ID=3 和 ID=4 沒有對應）

**驗收項目 3：用程式驗證**

建立 `verify_output.py`：

```python
import pandas as pd

df = pd.read_excel("merged_output.xlsx", engine="openpyxl")
print("欄位：", list(df.columns))
print("資料筆數：", len(df))
print("\n內容：")
print(df)
```

執行：

```powershell
py verify_output.py
```

### 8) Vibe Coding 迭代示範：改用 left join

**需求：** 改用 left join，保留 file1.xlsx 的所有資料，即使 file2.xlsx 沒有對應。

**你要給 AI 的提示：**

```text
請修改 merge_excel.py，把預設的 join 方式從 "inner" 改為 "left"。
限制：只改 merge_excel.py，不要新增套件，不要改函數介面。
驗收：執行後 merged_output.xlsx 應該有 3 筆資料（包含 Carol，但她的 Salary 和 Position 會是 NaN）
```

---

## 除錯：用 traceback 驅動 AI 修正（最有效的 Vibe 技巧）

### 原則：你要貼「完整錯誤」而不是一句話

你給 AI 的資料越完整，它越不需要腦補。

最少要貼：

1. 你做了什麼（幾步就好）
2. 你預期看到什麼
3. **完整 traceback**（從第一行到最後一行）

### 常見錯誤範例 1：ModuleNotFoundError

如果你看到：

```text
ModuleNotFoundError: No module named 'pandas'
```

通常代表：

- 你沒有啟動 venv
- 或你在別的 Python 環境安裝到 pandas

**最小修正流程：**

```powershell
.venv\Scripts\Activate.ps1
py -m pip install pandas openpyxl
py merge_excel.py
```

### 常見錯誤範例 2：FileNotFoundError

看到類似：

```text
FileNotFoundError: [Errno 2] No such file or directory: 'file1.xlsx'
```

**可能原因：**

- 檔案不存在
- 檔案在別的資料夾
- 檔名打錯（大小寫、空格）

**最小修正：**

```powershell
# 確認檔案是否存在
dir *.xlsx

# 如果沒有，先建立測試資料
py create_test_data.py
```

### 常見錯誤範例 3：KeyError (合併欄位不存在)

看到類似：

```text
KeyError: 'ID'
```

或程式自己拋出：

```text
ValueError: 欄位 'ID' 不存在於 file1.xlsx
```

**可能原因：**

- Excel 欄位名稱拼錯（例如 "id" vs "ID"）
- Excel 有額外空格（例如 "ID " vs "ID"）
- Excel 第一列不是欄位名稱

**最小修正：**

用 Python 檢查欄位名稱：

```python
import pandas as pd
df = pd.read_excel("file1.xlsx", engine="openpyxl")
print("欄位名稱：", list(df.columns))
```

再根據實際欄位名稱調整程式中的 `MERGE_COLUMN`。

### 常見錯誤範例 4：openpyxl 沒安裝

看到類似：

```text
ImportError: Missing optional dependency 'openpyxl'.
```

**最小修正：**

```powershell
py -m pip install openpyxl
```

---

## 小步重構：讓專案更可維護（但不要一開始就做）

當你已經「跑得起來」後，再把程式整理成更可維護的形式。

建議的最小重構目標：

- 改用命令列參數（不用每次都改程式碼）
- 加上基本錯誤處理（檔案不存在、欄位不存在）
- 加上 logging（至少能看處理進度/錯誤）

你可以用這個 prompt 叫 AI 幫你做最小重構：

```text
請幫我把目前的 merge_excel.py 做最小重構：
1) 保持現有功能完全不變
2) 改用命令列參數接收檔案路徑與合併設定（用 argparse）
3) 加上基本 logging（處理進度與錯誤訊息）
限制：不要新增新套件（除了標準庫的 argparse 與 logging）
請先列出你要改哪些行，再給我完整 merge_excel.py
```

### 重構範例：加入命令列參數

更新後的 `merge_excel.py`（加入 argparse）：

```python
from __future__ import annotations

import argparse
import logging
import pandas as pd


# 設定 logging
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def merge_excel_files(
	file1_path: str,
	file2_path: str,
	output_path: str,
	merge_on: str = "ID",
	how: str = "inner",
) -> None:
	"""
	讀取兩個 Excel 檔案並根據指定欄位合併。

	Args:
		file1_path: 第一個 Excel 檔案路徑
		file2_path: 第二個 Excel 檔案路徑
		output_path: 輸出檔案路徑
		merge_on: 合併依據的欄位名稱（預設 "ID"）
		how: 合併方式，可選 "inner", "left", "right", "outer"（預設 "inner"）
	"""
	try:
		# 讀取 Excel 檔案
		logger.info(f"正在讀取 {file1_path}...")
		df1 = pd.read_excel(file1_path, engine="openpyxl")
		logger.info(f"讀取成功，共 {len(df1)} 筆資料")

		logger.info(f"正在讀取 {file2_path}...")
		df2 = pd.read_excel(file2_path, engine="openpyxl")
		logger.info(f"讀取成功，共 {len(df2)} 筆資料")

		# 檢查合併欄位是否存在
		if merge_on not in df1.columns:
			raise ValueError(f"欄位 '{merge_on}' 不存在於 {file1_path}")
		if merge_on not in df2.columns:
			raise ValueError(f"欄位 '{merge_on}' 不存在於 {file2_path}")

		# 合併資料
		logger.info(f"正在根據 '{merge_on}' 欄位進行 {how} join...")
		merged_df = pd.merge(df1, df2, on=merge_on, how=how)
		logger.info(f"合併成功，共 {len(merged_df)} 筆資料")

		# 輸出結果
		logger.info(f"正在輸出到 {output_path}...")
		merged_df.to_excel(output_path, index=False, engine="openpyxl")
		logger.info("輸出成功！")

		# 顯示結果預覽
		print("\n合併結果預覽（前 5 筆）：")
		print(merged_df.head())

	except FileNotFoundError as e:
		logger.error(f"找不到檔案：{e}")
		raise
	except ValueError as e:
		logger.error(f"資料錯誤：{e}")
		raise
	except Exception as e:
		logger.error(f"發生未預期的錯誤：{e}")
		raise


def main():
	parser = argparse.ArgumentParser(
		description="合併兩個 Excel 檔案"
	)
	parser.add_argument(
		"file1",
		help="第一個 Excel 檔案路徑"
	)
	parser.add_argument(
		"file2",
		help="第二個 Excel 檔案路徑"
	)
	parser.add_argument(
		"-o", "--output",
		default="merged_output.xlsx",
		help="輸出檔案路徑（預設：merged_output.xlsx）"
	)
	parser.add_argument(
		"-m", "--merge-on",
		default="ID",
		help="合併依據的欄位名稱（預設：ID）"
	)
	parser.add_argument(
		"-j", "--join-type",
		default="inner",
		choices=["inner", "left", "right", "outer"],
		help="合併方式（預設：inner）"
	)

	args = parser.parse_args()

	logger.info("=== Excel 檔案合併工具 ===")
	merge_excel_files(
		file1_path=args.file1,
		file2_path=args.file2,
		output_path=args.output,
		merge_on=args.merge_on,
		how=args.join_type,
	)
	logger.info("=== 完成 ===")


if __name__ == "__main__":
	main()
```

使用範例：

```powershell
# 基本用法（使用預設設定）
py merge_excel.py file1.xlsx file2.xlsx

# 指定輸出檔名
py merge_excel.py file1.xlsx file2.xlsx -o result.xlsx

# 使用 left join
py merge_excel.py file1.xlsx file2.xlsx -j left

# 使用不同的合併欄位
py merge_excel.py employees.xlsx salaries.xlsx -m EmployeeID

# 查看說明
py merge_excel.py -h
```

---

## 進階功能（擇一）：常見的 Excel 處理需求

> 這章不追求「一次全做」，目標是讓你知道可以怎麼擴充。

### 功能 1：處理多個工作表（Sheet）

如果 Excel 檔案有多個工作表，可以這樣讀取：

```python
# 讀取特定工作表
df = pd.read_excel("data.xlsx", sheet_name="Sheet1", engine="openpyxl")

# 讀取所有工作表（回傳 dict）
all_sheets = pd.read_excel("data.xlsx", sheet_name=None, engine="openpyxl")
for sheet_name, df in all_sheets.items():
	print(f"工作表：{sheet_name}，資料筆數：{len(df)}")
```

### 功能 2：批次處理多個檔案

如果有一堆 Excel 要合併：

```python
import glob
import pandas as pd

# 找出所有 Excel 檔案
files = glob.glob("data/*.xlsx")

# 讀取並合併
dfs = []
for file in files:
	df = pd.read_excel(file, engine="openpyxl")
	dfs.append(df)

# 垂直合併（concat）
merged = pd.concat(dfs, ignore_index=True)
merged.to_excel("all_merged.xlsx", index=False, engine="openpyxl")
```

### 功能 3：資料清理

常見的清理需求：

```python
# 移除重複列
df = df.drop_duplicates()

# 移除空白列
df = df.dropna()

# 填補空值
df["Salary"] = df["Salary"].fillna(0)

# 去除欄位名稱的空格
df.columns = df.columns.str.strip()

# 轉換資料型別
df["ID"] = df["ID"].astype(int)
```

### 功能 4：加入計算欄位

```python
# 新增一個計算欄位
df["Annual_Salary"] = df["Salary"] * 12

# 根據條件新增欄位
df["Level"] = df["Salary"].apply(
	lambda x: "Senior" if x > 55000 else "Junior"
)
```

---

## 常見坑速查（Windows 最常踩）

1. **PowerShell 啟動 venv 被擋**：用 `Set-ExecutionPolicy -Scope Process Bypass` 或改用 `activate.bat`
2. **找不到 openpyxl**：記得 `py -m pip install openpyxl`
3. **安裝到錯的 Python**：統一用 `py -m pip ...`，避免 pip 指到別的環境
4. **Excel 檔案被開啟中**：Windows 會鎖定檔案，執行前先關閉 Excel
5. **欄位名稱對不上**：用 `df.columns` 檢查實際欄位名稱，注意大小寫與空格
6. **編碼問題**：如果 Excel 有中文，確保用 UTF-8 儲存或用 `encoding` 參數
7. **亂改一大堆**：每次只改一件事；要求 AI 限制修改檔案數量

---

## 練習題（照 Vibe 流程做：規格→驗收→改→驗收）

### 練習 1：改用 outer join

需求：改用 outer join，保留所有資料（包括只在 file1 或只在 file2 的）。

驗收：

- 輸出檔案有 4 筆資料（ID: 1, 2, 3, 4）
- ID=3 的 Salary 和 Position 是 NaN
- ID=4 的 Name 和 Department 是 NaN

### 練習 2：新增資料筆數統計

需求：在程式結束前，印出三個統計數字：

- file1 原始資料筆數
- file2 原始資料筆數
- 合併後資料筆數

驗收：執行後能看到類似輸出：

```text
統計：
- file1: 3 筆
- file2: 3 筆
- 合併結果: 2 筆
```

### 練習 3：加入資料驗證

需求：在合併前檢查：

- ID 欄位是否有重複（同一個檔案內）
- ID 欄位是否有空值

如果有問題，印出警告訊息（不中斷執行）。

驗收：

- 建立一個有重複 ID 的測試檔案
- 執行後應該看到警告訊息

### 練習 4：支援 CSV 格式

需求：除了 Excel，也支援讀取 CSV 檔案（自動偵測副檔名）。

限制：不改變 Excel 的讀取方式。

驗收：

- 準備 `file1.csv` 和 `file2.xlsx`
- 執行後能正確合併

提示：用 `os.path.splitext()` 取得副檔名，再決定用 `read_excel` 或 `read_csv`。

---

## 一頁命令速查

```powershell
# 建 venv
py -m venv .venv

# 啟動 venv（PowerShell）
.venv\Scripts\Activate.ps1

# 更新 pip
py -m pip install -U pip

# 安裝套件
py -m pip install pandas openpyxl

# 建立測試資料
py create_test_data.py

# 執行合併
py merge_excel.py

# 重構版（命令列參數）
py merge_excel.py file1.xlsx file2.xlsx -o output.xlsx -j left

# 檢查輸出
py verify_output.py
```

---

## 延伸學習資源

- [pandas 官方文件 - Excel I/O](https://pandas.pydata.org/docs/reference/io.html#excel)
- [openpyxl 官方文件](https://openpyxl.readthedocs.io/)
- [pandas merge 教學](https://pandas.pydata.org/docs/user_guide/merging.html)

---

## 總結：Vibe Coding 的價值

用 Vibe Coding 的方式做 Excel 處理，你得到的不只是「一個能跑的腳本」，而是：

1. **可驗收**：每次改動都有明確的驗收條件
2. **可迭代**：從最小版本開始，一步步加功能
3. **可除錯**：用 traceback 和規格驅動 AI 修正
4. **可維護**：小步修改，每次都能回滾

這套方法不只適用於 Excel，也適用於任何 Python 自動化任務：爬蟲、資料清理、報表產生、API 串接…等。

**記住核心原則：規格 → 驗收 → 最小實作 → 小步迭代。**