# 3. 🧾 提示詞設計與流程思維

---

## 3-1 提示詞（Prompt）設計理論與實務

### 3-1-1 Prompt Engineering 理論基礎
Prompt Engineering 是現代 LLM 應用的核心技術，涉及語言學、語意學、認知科學與人機互動（HCI）等多領域理論。良好的提示詞設計能顯著提升 AI 回應的準確性、可控性與創造力。

#### 主要理論
- 語境依賴性（Contextuality）：LLM 依賴上下文理解任務。
  - 範例：
    - Prompt：「請根據下列文章摘要內容：...」
    - LLM 會根據前文提供的文章內容進行摘要。
- 指令明確性（Instruction Clarity）：明確指令可減少模型誤解。
  - 範例：
    - Prompt：「請用 100 字說明 AI Agent 的應用。」
    - 指令明確，模型回應長度與主題皆可控。
- Few-shot/Zero-shot Learning：透過範例引導模型學習新任務。
  - 範例：
    - Zero-shot：「請翻譯下列句子為英文：我喜歡人工智慧。」
    - Few-shot：「Q: 什麼是 AI？A: 人工智慧是... Q: 什麼是 LLM？A: ...」
- Chain-of-Thought Prompting：引導模型逐步推理。
  - 範例：
    - Prompt：「請逐步推理：一個蘋果加兩個蘋果等於幾個蘋果？」
    - LLM 會先列出推理步驟再給答案。

### 3-1-2 提示詞設計步驟與範例
1. 明確描述任務與輸出格式。
   - 範例：Prompt：「請以表格列出三種 AI Agent 類型及其特點。」
2. 提供範例（Few-shot）或明確指令（Zero-shot）。
   - 範例：Prompt：「Q: 什麼是強化學習？A: ... Q: 什麼是監督式學習？A: ...」
3. 測試不同提示詞，觀察模型回應差異。
   - 範例：
     - Prompt1：「請簡述 AI Agent。」
     - Prompt2：「請用 50 字簡述 AI Agent 並舉一例。」
4. 優化提示詞，減少歧義與偏見。
   - 範例：
     - 原始：「請推薦一本書。」
     - 優化：「請推薦一本適合初學者學習 AI 的中文書籍，並說明理由。」

#### 範例
- Zero-shot：「請用 100 字說明 AI Agent 的應用。」
- Few-shot：「Q: 什麼是 AI Agent？A: ... Q: LLM 有哪些應用？A: ...」
- Chain-of-Thought：「請逐步推理：...」

#### 進階技巧
- 使用系統提示（System Prompt）設定角色與風格。
  - 範例：
    - Prompt：「你是一位資深 AI 教授，請用簡明方式解釋強化學習。」
- 控制溫度（temperature）、最大長度（max_tokens）等參數。
  - 範例：
    - API 呼叫時設定 temperature=0.2（提升回應穩定性）、max_tokens=100（限制回應長度）。

---

## 3-2 UML 流程圖與對話流程設計

### 3-2-1 UML 與流程圖理論
- UML（Unified Modeling Language）是軟體工程標準建模語言，常用於描述系統結構與行為。
- 常見圖表：用例圖、活動圖、時序圖、狀態圖。

### 3-2-2 對話流程設計步驟
1. 定義對話目標與場景（如訂餐、查詢天氣）。
2. 畫出用例圖，標示用戶與系統互動。
3. 設計活動圖或流程圖，描述對話分支與條件。
4. 製作時序圖，標示訊息交換順序。

#### 工具建議
- draw.io、PlantUML、Miro、Lucidchart。

#### 範例：訂餐對話流程
- 用戶發起訂單 → AI 詢問品項 → 用戶回覆 → AI 詢問數量 → ... → 訂單確認

#### 模擬案例：AI 智能客服訂餐流程

假設設計一個 AI 智能客服協助用戶訂餐，完整流程如下：

1. **定義對話目標與場景**
   - 目標：協助用戶完成線上訂餐。
   - 場景：用戶透過聊天介面與 AI 互動。
2. **用例圖（Use Case Diagram）**
   - 參與者：用戶、AI 系統。
   - 用例：發起訂單、選擇餐點、確認數量、填寫聯絡資訊、訂單確認。
   - （建議繪製用例圖，標示用戶與 AI 的互動關係）
3. **活動圖/流程圖（Activity/Flowchart）**
   - 用戶發起訂單 → AI 詢問餐點 → 用戶選擇 → AI 詢問數量 → 用戶輸入 → AI 詢問聯絡資訊 → 用戶填寫 → AI 確認訂單 → 完成
   - （建議繪製流程圖，標示每個分支與條件）
4. **時序圖（Sequence Diagram）**
   - 用戶：我要訂餐 → AI：請問要點什麼？ → 用戶：牛肉麵 → AI：幾份？ → 用戶：2 份 → AI：請提供聯絡電話 → 用戶：0912xxx → AI：訂單確認，感謝您的訂購！
   - （建議繪製時序圖，標示訊息交換順序）

**流程 Python 範例（簡化版）**
```python
# AI 智能客服訂餐對話流程模擬
order = {}
print("AI: 歡迎訂餐，請問要點什麼？")
order['item'] = input("用戶: ")
print(f"AI: 請問要幾份 {order['item']}？")
order['qty'] = input("用戶: ")
print("AI: 請提供聯絡電話：")
order['phone'] = input("用戶: ")
print(f"AI: 您訂購了 {order['qty']} 份 {order['item']}，聯絡電話：{order['phone']}。訂單已成立，感謝您的訂購！")
```

---

## 3-3 多階段問題處理與 LLM 串接策略

### 3-3-1 多階段對話理論
- 多輪對話（Multi-turn Dialogue）需追蹤上下文與狀態。
- 任務導向對話（Task-oriented Dialogue）強調資訊收集與任務完成。

### 3-3-2 LLM 串接策略
1. 將複雜任務拆解為多個階段，每階段設計專屬 prompt。
2. 保存對話狀態，動態調整 prompt 與 API 請求。
3. 結合外部工具（如資料庫、API）提升任務能力。

#### 進階範例：多階段訂餐對話
```python
def multi_stage_chat(user_input, stage=1):
    if stage == 1:
        return '請問您要查詢什麼資訊？', 2
    elif stage == 2:
        if '天氣' in user_input:
            return '請問哪個城市的天氣？', 3
        else:
            return '目前只支援天氣查詢。', 3
    elif stage == 3:
        return f'查詢 {user_input} 的天氣中...', None

# 測試
msg, next_stage = multi_stage_chat('', 1)
print(msg)
msg, next_stage = multi_stage_chat('我要查天氣', next_stage)
print(msg)
msg, next_stage = multi_stage_chat('台北', next_stage)
print(msg)
```

---

## 3-4 產業案例、學術資源與研究挑戰
- 產業：智慧客服、醫療問診、教育助理、法律諮詢。
- 學術：PromptBench、PromptSource、ACL Anthology。
- 挑戰：提示詞泛化、對抗攻擊、倫理偏見。

---

## 3-5 進階實作練習與圖表建議
- 練習設計多種 prompt，觀察 LLM 回應差異。
- 畫出對話流程圖、狀態轉移圖。
- 比較不同 prompt 對模型行為的影響。
