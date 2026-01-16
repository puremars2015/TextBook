# 使用VibeCoding操作Excel教學（Office Scripts）

## 目錄

- [使用VibeCoding操作Excel教學（Office Scripts）](#使用vibecoding操作excel教學office-scripts)
    - [一、導論（Why Vibe Coding + Excel + Office Scripts）](#一導論why-vibe-coding--excel--office-scripts)
    - [二、Vibe Coding 操作 Excel 的整體流程（Office Scripts 版）](#二vibe-coding-操作-excel-的整體流程office-scripts-版)
    - [三、環境準備與基本設定（Office Scripts）](#三環境準備與基本設定office-scripts)
    - [四、Vibe Coding 的「需求描述技巧」（核心章節）](#四vibe-coding-的需求描述技巧核心章節)
    - [五、基礎範例：從一句話到可用結果（Office Script）](#五基礎範例從一句話到可用結果office-script)
    - [六、常見錯誤與除錯方式（Office Scripts 非常重要）](#六常見錯誤與除錯方式office-scripts-非常重要)
    - [七、進階應用情境（Office Scripts + Power Automate）](#七進階應用情境office-scripts--power-automate)
    - [八、實務案例（可依你背景客製）](#八實務案例可依你背景客製)
    - [九、建立自己的 Vibe Coding 工作流程（Office Scripts 版）](#九建立自己的-vibe-coding-工作流程office-scripts-版)
    - [十、總結與下一步](#十總結與下一步)

---

## 一、導論（Why Vibe Coding + Excel + Office Scripts）

這份教學的目標是：用「Vibe Coding」（用自然語言把需求寫成可驗證規格，讓 AI 協助你快速產出與修正）來撰寫 **Office Scripts**，把 Excel 的日常工作自動化。

為什麼選 Office Scripts

- 不用安裝 Python、不用處理套件相依。
- 腳本直接跑在 Excel（通常是 Excel 網頁版），修改當前活頁簿。
- 可搭配 Power Automate：排程、自動處理 OneDrive/SharePoint 上的檔案。

你需要先知道的限制（很重要）

- Office Scripts 主要在 **Excel 網頁版（Microsoft 365）** 使用與編寫。
- 腳本通常只能操作「當前活頁簿」的內容；要批次處理多個檔案，通常要靠 **Power Automate** 迴圈呼叫。
- Office Scripts 無法像本機程式一樣自由讀寫電腦檔案路徑；檔案要在 OneDrive/SharePoint 才好自動化。

Vibe Coding 的核心觀念（用一句話記）

> 不是「叫 AI 幫你寫腳本」，而是「把需求寫成可驗證的規格，讓 AI 迭代產出直到符合規格」。

---

## 二、Vibe Coding 操作 Excel 的整體流程（Office Scripts 版）

建議固定使用以下流程，避免「一次生成一大段，結果完全跑不動」。

1. 定義 Input/Output（在 Office Scripts 中通常都在同一個活頁簿內完成）
        - Input：哪個工作表（Sheet）、資料從哪個 Range 或 Table、欄位名稱。
        - Output：寫到哪個工作表、是否覆蓋、是否建立新表、是否需要格式。
2. 先做最小可行版本（MVP）
        - 先做：讀到資料 → 檢查欄位 → 寫出結果（哪怕只是把前 5 列複製到新 sheet）。
3. 每次只加一個規則
        - 例如：先過濾 0 金額 → 再加日期標準化 → 再加彙總。
4. 要 AI 回傳「可直接貼進 Script Editor 的完整腳本」
        - 指定：`function main(workbook: ExcelScript.Workbook)`、sheet 名稱、欄位。
5. 驗證與回饋
        - 用事實回饋：錯誤訊息、實際欄位列表、前 10 列資料樣本（可遮敏）。

Office Scripts 常見結構（你可以把它當成固定骨架）

```typescript
function main(workbook: ExcelScript.Workbook) {
    const source = workbook.getWorksheet("Data");
    if (!source) throw new Error("找不到工作表 Data");

    const used = source.getUsedRange();
    if (!used) throw new Error("Data 沒有資料");

    const values = used.getValues();
    // 1) 讀取與驗證
    // 2) 處理
    // 3) 輸出
}
```

---

## 三、環境準備與基本設定（Office Scripts）

### 3.1 你需要具備的東西

- Microsoft 365 帳號（能使用 Excel 網頁版）
- 檔案放在 OneDrive 或 SharePoint（若要自動化/排程會更順）

### 3.2 如何開啟 Office Scripts 編輯器

1. 用瀏覽器開啟 Excel（Excel for the web）並打開你的活頁簿
2. 找到功能區的 **Automate（自動化）**
3. 選 **New Script（新指令碼）**，貼上腳本
4. 按 **Run（執行）**

小提醒

- 如果你看不到 Automate：通常是授權/系統管理員設定問題，或該帳號未啟用 Office Scripts。

### 3.3 Office Scripts 的資料模型（一定要懂的三件事）

- `Worksheet`：工作表
- `Range`：一塊儲存格區域（例如用 `getUsedRange()` 取得已使用範圍）
- `values`：`Range.getValues()` 會回傳二維陣列 `(string | number | boolean)[][]`

建議習慣

- 優先用「欄位名稱找索引」而不是寫死欄位 A/B/C。
- 優先以「一次讀取整個 usedRange → 在記憶體處理 → 一次寫回」避免逐格操作。

---

## 四、Vibe Coding 的「需求描述技巧」（核心章節）

Office Scripts 的成功關鍵是：**把 Excel 結構講清楚**（sheet 名稱、標題列、欄位名、輸出位置），AI 才能寫出可跑的腳本。

### 4.1 Office Scripts 需求描述模板（可直接複製）

```text
【目標】我想要用 Office Scripts 自動處理 Excel（不要用 Python）。

【活頁簿狀態】
- 我會在 Excel 網頁版打開檔案後執行腳本
- 資料所在工作表：（例如：Data）
- 標題列位置：（例如：第 1 列是欄位名稱）

【欄位定義】（請寫「欄位名稱」而非 A/B/C）
- 日期
- 產品
- 業務
- 金額

【處理規則】
1) （例如：移除金額為空或 0 的列）
2) （例如：日期標準化成 yyyy-mm-dd，無法解析就保留原值）
3) （例如：依業務彙總總金額與筆數，依總金額由大到小排序）

【輸出結果】（在同一個活頁簿內）
- CleanData 工作表：寫入清洗後明細（覆蓋舊內容）
- Summary 工作表：寫入彙總表（覆蓋舊內容）

【限制與偏好】
- 腳本必須是完整可貼上的 Office Script
- 請包含：工作表不存在時的錯誤提示
- 請避免逐格讀寫（效能考量）

【驗證方式】
- 請在 Summary 顯示前 10 名
- CleanData 的列數要等於「符合規則的列數」
```

### 4.2 讓 AI 更穩的三個要求（Office Scripts 特化）

- 要求 AI 「先確認資料長相」：
    - 例如：標題列是不是第一列？欄位名是否有空白？日期欄是文字還是數值（Excel 序號）？
- 要求 AI 「先做 MVP 再加規則」：
    - 先做：把 Data 的 usedRange 複製到 CleanData
- 要求 AI 「固定使用欄位名找索引」：
    - 避免換欄位順序就壞掉

### 4.3 你可以直接貼給 AI 的提示詞（Prompt）

```text
請你用 Office Scripts（TypeScript）寫腳本，不要用 Python。
先做 MVP：
1) 讀取 Data 工作表的 usedRange
2) 印出欄位名稱（用 throw Error 顯示也可以）或至少驗證欄位存在
3) 把整份資料複製到 CleanData 工作表

完成後再問我：要加哪些清洗/彙總規則。
```

---

## 五、基礎範例：從一句話到可用結果（Office Script）

本章示範「一句話 → 規格化 → 產出可直接執行的 Office Script」。

### 5.1 一句話需求（不夠清楚的版本）

> 幫我把銷售資料整理成報表。

問題：缺少 sheet 名稱、欄位、輸出位置，AI 只能猜。

### 5.2 改寫成可執行規格（建議版本）

```text
【目標】整理銷售資料成彙總報表。

【活頁簿狀態】
- 我會在 Excel 網頁版打開該檔案後執行 Office Script
- 資料在 Data 工作表，第 1 列是欄位名稱

【處理規則】
1) 移除「金額」為空或 0 的列
2) 產生新欄位「日期_標準化」
        - 如果日期是 Excel 序號（數字），轉成 yyyy-mm-dd
        - 如果日期是文字，能解析就轉 yyyy-mm-dd，不能解析就保留原文字
3) 依「業務」彙總：總金額與筆數，依總金額由大到小排序

【輸出結果】
- CleanData 工作表：寫入清洗後明細（覆蓋舊內容）
- Summary 工作表：寫入彙總表（覆蓋舊內容）
```

### 5.3 可直接執行的 Office Script（貼到 Automate → New Script）

```typescript
function main(workbook: ExcelScript.Workbook) {
    const sourceSheetName = "Data";
    const cleanSheetName = "CleanData";
    const summarySheetName = "Summary";

    const sourceSheet = workbook.getWorksheet(sourceSheetName);
    if (!sourceSheet) {
        throw new Error(`找不到工作表：${sourceSheetName}`);
    }

    const used = sourceSheet.getUsedRange();
    if (!used) {
        throw new Error(`工作表 ${sourceSheetName} 沒有任何資料（usedRange 為空）`);
    }

    const values = used.getValues();
    if (values.length < 2) {
        throw new Error(`工作表 ${sourceSheetName} 資料列不足（至少要有標題列 + 1 筆資料）`);
    }

    const headers = values[0].map(v => String(v ?? "").trim());
    const indexOf = (headerName: string) => headers.findIndex(h => h === headerName);

    const amountIdx = indexOf("金額");
    const salesIdx = indexOf("業務");
    const dateIdx = indexOf("日期");

    if (amountIdx < 0) throw new Error("找不到欄位：金額（請確認標題列是否正確、欄位名稱是否一致）");
    if (salesIdx < 0) throw new Error("找不到欄位：業務（請確認標題列是否正確、欄位名稱是否一致）");

    const cleaned: (string | number | boolean)[][] = [];
    const outputHeaders = [...values[0]];
    const addNormalizedDate = dateIdx >= 0;
    if (addNormalizedDate) outputHeaders.push("日期_標準化");
    cleaned.push(outputHeaders);

    const totals = new Map<string, { total: number; count: number }>();

    for (let r = 1; r < values.length; r++) {
        const row = values[r];

        const amount = parseNumber(row[amountIdx]);
        if (!Number.isFinite(amount) || amount === 0) continue;

        const salespersonRaw = row[salesIdx];
        const salesperson = String(salespersonRaw ?? "").trim() || "(空白)";

        let normalizedDate = "";
        if (addNormalizedDate) {
            normalizedDate = normalizeDateCell(row[dateIdx]);
        }

        const outRow = [...row];
        if (addNormalizedDate) outRow.push(normalizedDate);
        cleaned.push(outRow);

        const current = totals.get(salesperson) ?? { total: 0, count: 0 };
        current.total += amount;
        current.count += 1;
        totals.set(salesperson, current);
    }

    const summaryRows: (string | number)[][] = [];
    summaryRows.push(["業務", "總金額", "筆數"]);

    const summaryData = Array.from(totals.entries())
        .map(([name, agg]) => ({ name, total: agg.total, count: agg.count }))
        .sort((a, b) => b.total - a.total);

    for (const item of summaryData) {
        summaryRows.push([item.name, item.total, item.count]);
    }

    const cleanSheet = getOrCreateWorksheet(workbook, cleanSheetName);
    clearWorksheet(cleanSheet);
    writeMatrix(cleanSheet, cleaned);

    const summarySheet = getOrCreateWorksheet(workbook, summarySheetName);
    clearWorksheet(summarySheet);
    writeMatrix(summarySheet, summaryRows);

    // 一點點格式（可刪）：總金額套用數字格式
    if (summaryRows.length > 1) {
        const totalColRange = summarySheet.getRangeByIndexes(1, 1, summaryRows.length - 1, 1);
        totalColRange.setNumberFormatLocal("#,##0.00");
    }
}

function getOrCreateWorksheet(workbook: ExcelScript.Workbook, name: string): ExcelScript.Worksheet {
    const existing = workbook.getWorksheet(name);
    return existing ?? workbook.addWorksheet(name);
}

function clearWorksheet(sheet: ExcelScript.Worksheet) {
    const used = sheet.getUsedRange();
    if (used) used.clear(ExcelScript.ClearApplyTo.all);
}

function writeMatrix(sheet: ExcelScript.Worksheet, matrix: (string | number | boolean)[][]) {
    const rowCount = matrix.length;
    const colCount = Math.max(...matrix.map(r => r.length));

    // 讓每列長度一致，避免 setValues 失敗
    const normalized = matrix.map(r => {
        const row = [...r];
        while (row.length < colCount) row.push("");
        return row;
    });

    const range = sheet.getRangeByIndexes(0, 0, rowCount, colCount);
    range.setValues(normalized);
    range.getFormat().autofitColumns();
}

function parseNumber(value: unknown): number {
    if (typeof value === "number") return value;
    if (typeof value === "boolean") return value ? 1 : 0;
    if (typeof value === "string") {
        const trimmed = value.trim();
        if (!trimmed) return Number.NaN;
        return Number(trimmed.replace(/,/g, ""));
    }
    return Number.NaN;
}

function normalizeDateCell(value: unknown): string {
    if (typeof value === "number") {
        // 常見情況：Excel 日期欄回傳序號
        return excelSerialToIsoDate(value);
    }
    if (typeof value === "string") {
        const text = value.trim();
        if (!text) return "";

        const t = Date.parse(text);
        if (!Number.isNaN(t)) {
            return new Date(t).toISOString().slice(0, 10);
        }
        return text; // 無法解析就保留原文
    }
    if (typeof value === "boolean") return value ? "TRUE" : "FALSE";
    return String(value ?? "");
}

function excelSerialToIsoDate(serial: number): string {
    // Excel 的日期序號通常以 1899-12-30 為基準（含歷史相容性問題）
    // 使用 UTC 避免時區造成日期偏移
    const epoch = Date.UTC(1899, 11, 30);
    const millis = epoch + Math.round(serial * 86400 * 1000);
    return new Date(millis).toISOString().slice(0, 10);
}
```

### 5.4 對 AI 的回饋方式（讓下一輪更準）

當結果不符合預期，不要只說「不對」。請用可驗證的方式回饋：

```text
Summary 需要只顯示前 10 名。
另外我的「日期」欄有兩種狀態：有些是 Excel 序號（數字），有些是文字（2026/01/15）。
請你只修改日期標準化與 Top 10 顯示部分，其餘不要動。
```

---

## 六、常見錯誤與除錯方式（Office Scripts 非常重要）

### 6.1 看不到 Automate（自動化）/ New Script

可能原因

- 帳號授權未包含 Office Scripts
- 組織（Tenant）管理員停用 Office Scripts
- 你開的是 Excel 桌面版而不是 Excel 網頁版

處理方式

- 先用瀏覽器開 Excel（for the web）測試
- 若仍沒有，通常需要請 IT/系統管理員確認 Office Scripts 設定

### 6.2 `getWorksheet(...)` 回傳 `undefined`

原因

- 工作表名稱拼錯（含空白/全形空格）
- 檔案裡根本沒有該工作表

解法

- 先確認工作表名稱（建議複製貼上）
- 腳本中使用明確錯誤訊息（範例已示範）

### 6.3 `getUsedRange()` 是空的

原因

- 工作表真的沒有值（或資料在別的 sheet）

解法

- 先人工確認資料在哪個工作表
- 若資料是表格（Table），也可改用 `worksheet.getTables()` 取得

### 6.4 `Range.setValues: The argument is invalid`（常見）

原因

- 你要寫入的二維陣列「每列欄數不一致」

解法

- 寫入前先把每列補齊同樣欄數（範例 `writeMatrix` 已處理）

### 6.5 效能/逾時

症狀

- 資料量大時執行很慢或失敗

解法

- 避免逐格讀寫、逐列 `getRange()`
- 盡量「一次讀取 → 記憶體處理 → 一次寫回」
- 如果要批次處理多檔案，建議改由 Power Automate 逐檔呼叫腳本

---

## 七、進階應用情境（Office Scripts + Power Automate）

### 7.1 什麼時候需要 Power Automate

- 你要每天固定時間跑
- 你要針對 OneDrive/SharePoint 某個資料夾的多個檔案批次處理
- 你要在腳本跑完後做下一步（寄信、Teams 通知、搬檔、轉 PDF）

### 7.2 常見任務與建議做法

1) 批次處理多檔案（每個檔都做同一套清洗/彙總）
- Power Automate：列出資料夾檔案 → 對每個檔案執行「Run script」

2) 套用既有範本
- Office Scripts：在同一個活頁簿內把資料寫入範本指定區域

3) 匯出 PDF
- Office Scripts 本身通常不直接做「另存 PDF」
- 實務上：Power Automate 後續動作做轉檔（依你組織的可用連接器而定）

---

## 八、實務案例（可依你背景客製）

### 案例 A：同一活頁簿內合併多個工作表

情境

- `Jan`, `Feb`, `Mar` 三個 sheet 欄位一致
- 合併成 `AllMonths`，並新增一欄 `月份`

你可以貼給 AI 的提示詞

```text
請用 Office Scripts（TypeScript）寫一支腳本：
1) 讀取工作表 Jan/Feb/Mar 的 usedRange（第 1 列是標題）
2) 合併成 AllMonths 工作表
3) 新增欄位 月份，分別填 Jan/Feb/Mar
4) AllMonths 若已存在就覆蓋內容
```

### 案例 B：建立 KPI 彙總表（Top 10）

- 依部門/業務彙總：總金額、平均單價、成交數
- Summary 只保留前 10 名

### 案例 C：資料清洗與欄位標準化

- 去除前後空白
- 統一欄位名稱（例如：`業務員`/`業務` 合併成 `業務`）
- 金額欄清掉逗號並轉數值

---

## 九、建立自己的 Vibe Coding 工作流程（Office Scripts 版）

你可以把以下流程當成固定 SOP。

1) 先把 Excel 結構講清楚
- sheet 名稱、標題列在哪一列、欄位名稱、輸出要寫到哪

2) 先做 MVP
- 讀 usedRange → 檢查欄位 → 寫到新 sheet

3) 小步迭代（一次一個規則）
- 過濾 → 標準化 → 彙總 → 格式

4) 保存成功的 Prompt 與腳本
- 建議保留：需求描述、版本變更、錯誤與解法

---

## 十、總結與下一步

你已經具備用 Vibe Coding 操作 Excel（Office Scripts）的基本能力：

- 會把需求寫成可執行規格（Sheet/Columns/Rules/Output/Validation）
- 會用 Office Scripts 一次讀寫範圍、避免逐格操作
- 知道常見錯誤與限制，並能用具體回饋引導 AI 修正

下一步建議（選一個做就好）

1) 把你手上最常做的 Excel 任務，改寫成第 4 章模板
2) 先做 MVP（讀 → 寫）
3) 再加規則（清洗/彙總/Top10/格式）

如果你願意，我也可以把第 5 章範例改成「你的真實欄位與規則版本」：你只要提供欄位名稱、sheet 名稱、以及你想輸出的樣子（可截圖/描述）。
