# 1. 🧠 AI 基礎與應用探索

---

## 1-1 AI Agent 介紹

### 1-1-1 定義與理論基礎

AI Agent（人工智慧代理人）在人工智慧領域中，指的是一種能夠自主感知環境、理解任務、根據目標進行決策與行動的智能系統。其理論基礎可追溯至人工智慧的經典定義：「能夠感知其環境並採取行動以最大化其目標函數的系統」。

#### 代理人模型（Agent Model）
- **感知（Perception）**：透過感測器（Sensors）獲取環境資訊。
  - Sample：
    ```python
    # 感知：讀取溫度感測器數值
    temperature = 27.5  # 假設由感測器獲得
    print(f"目前溫度：{temperature}°C")
    ```
- **推理（Reasoning）**：利用知識庫、規則、機器學習模型等進行資訊處理與決策。
  - Sample：
    ```python
    # 推理：根據溫度決定是否開啟冷氣
    if temperature > 28:
        action = "開啟冷氣"
    else:
        action = "維持現狀"
    print(action)
    ```
- **行動（Action）**：透過致動器（Actuators）對環境產生影響。
  - Sample：
    ```python
    # 行動：模擬致動器控制冷氣
    if action == "開啟冷氣":
        print("冷氣已啟動")
    else:
        print("冷氣維持關閉")
    ```
- **學習（Learning）**：根據經驗調整決策策略，提升效能。
  - Sample：
    ```python
    # 學習：根據回饋調整決策閾值
    threshold = 28
    feedback = -1  # 假設冷氣開啟後用戶覺得太冷
    if feedback < 0:
        threshold += 1  # 提高啟動冷氣的溫度門檻
    print(f"新閾值：{threshold}°C")
    ```

#### 數學描述
一個 AI Agent 可形式化為一個四元組：

$$
Agent = (S, A, P, \\pi)
$$

- $S$：狀態空間（States）
- $A$：行動空間（Actions）
- $P$：感知函數（Perception Function）
- $\\pi$：策略（Policy），即從狀態到行動的映射

### 1-1-2 AI Agent 分類

AI Agent 可依據其決策方式、知識來源、學習能力與應用場景進行多層次分類。以下針對主要類型進行詳細說明，並輔以範例概念：

1. **基於規則的代理人（Rule-based Agent）**
   - **詳細敘述**：此類代理人以明確的 if-then 規則為核心，根據感知到的環境狀態直接對應行動。規則通常由專家手動設計，適合結構明確、變化有限的任務。
   - **範例概念**：
     - 智能家居溫控系統：若溫度高於 28°C，則開啟冷氣；若低於 18°C，則開啟暖氣。
     - 聊天機器人 FAQ：若用戶輸入包含「營業時間」，則回覆「本店營業時間為...」。

2. **基於知識的代理人（Knowledge-based Agent）**
   - **詳細敘述**：具備知識庫（如專家系統、邏輯規則、語意網）與推理引擎，能根據知識進行複雜推理與決策。適合需要邏輯推理、知識查詢的場景。
   - **範例概念**：
     - 醫療診斷專家系統：根據病徵推理可能疾病，並給出建議。
     - 法律諮詢系統：根據法條與案例推理法律建議。

3. **學習型代理人（Learning Agent）**
   - **詳細敘述**：能根據經驗數據自我優化決策策略，常用方法包括監督式學習、非監督式學習、強化學習等。適合環境複雜、規則難以明確列舉的任務。
   - **範例概念**：
     - 強化學習自走車：透過試誤學習最佳路徑與避障策略。
     - 智能推薦系統：根據用戶歷史行為自動調整推薦內容。

4. **多代理人系統（Multi-agent System, MAS）**
   - **詳細敘述**：由多個代理人組成，彼此可協作或競爭，形成複雜的群體行為。MAS 可用於模擬社會、經濟、生態等多體系統。
   - **範例概念**：
     - 智慧交通系統：多輛自駕車協同避讓、路徑規劃。
     - 金融市場模擬：多個交易代理人根據不同策略進行買賣。

5. **自主型代理人（Autonomous Agent）**
   - **詳細敘述**：具備高度自主決策能力，能在無人監督下根據目標與環境變化自我調整行動。
   - **範例概念**：
     - 行星探測機器人：在未知環境中自主導航、資料蒐集。

6. **反應型代理人（Reactive Agent）**
   - **詳細敘述**：僅根據當前感知做出即時反應，無長期規劃或內部狀態記憶，適合即時性要求高的場景。
   - **範例概念**：
     - 遊戲 NPC：根據玩家動作即時閃避或攻擊。

7. **目標導向型代理人（Goal-based Agent）**
   - **詳細敘述**：具備明確目標，能根據目標規劃多步行動，並根據環境變化調整策略。
   - **範例概念**：
     - 自動導航系統：根據目的地規劃最佳路徑，遇到障礙時重新規劃。

> 各類型代理人可依實際應用需求進行組合與擴展，形成混合型架構以兼顧靈活性與效能。

### 1-1-3 AI Agent 架構

#### 1. 感知-行動循環（Perception-Action Loop）
- 代理人不斷感知環境、決策、執行行動，並根據回饋調整策略。

#### 2. BDI 架構（Belief-Desire-Intention）
- **Belief**：對世界的認知
- **Desire**：目標與動機
- **Intention**：當前計畫與承諾

#### 3. 強化學習代理人（Reinforcement Learning Agent）
- 以最大化累積報酬為目標，透過 trial-and-error 學習最優策略。

#### 4. 混合型架構（Hybrid Architecture）
- 結合規則、知識、學習等多種方法，提升靈活性與適應性。

### 1-1-4 代理人設計挑戰
- 感知不完全與不確定性
- 多目標衝突與決策困難
- 知識表達與推理效率
- 學習收斂速度與泛化能力
- 多代理人協作與溝通

---

## 1-2 LLM 介紹

### 1-2-1 LLM 理論基礎與架構

LLM（Large Language Model，大型語言模型）是基於深度學習的自然語言處理（NLP）模型，通常採用 Transformer 架構，具備數十億至數千億參數，能理解與生成自然語言。

#### Transformer 架構核心
- **Self-Attention**：捕捉序列中各詞之間的關聯性。
- **多層堆疊**：提升模型表達能力。
- **預訓練-微調（Pretrain-Finetune）**：先在大規模語料上預訓練，再針對特定任務微調。

#### LLM 代表模型
- GPT-3/4（OpenAI）
- PaLM（Google）
- LLaMA（Meta）
- GLM（清華大學）

### 1-2-2 LLM 的數學模型

LLM 以條件機率建模：

$$
P(w_1, w_2, ..., w_n) = \\prod_{i=1}^n P(w_i | w_1, ..., w_{i-1})
$$

其中 $w_i$ 為第 $i$ 個詞。

### 1-2-3 LLM 訓練與推論流程
1. **資料蒐集**：大規模語料（如 Wikipedia、書籍、網頁）。
2. **資料前處理**：分詞、去除雜訊、標註。
3. **模型訓練**：使用 GPU/TPU 進行大規模分布式訓練。
4. **推論與應用**：生成文本、摘要、翻譯、問答等。

### 1-2-4 LLM 挑戰與前沿議題
- 計算資源消耗巨大
- 訓練資料偏見與倫理問題
- 長文本記憶與推理能力有限
- 多語言與跨領域泛化

---

## 1-3 AI Agent 與產業應用案例

### 1-3-1 金融業
- 智能客服：自動回應用戶查詢、辦理業務、詐騙偵測。
- 風險評估：自動化信貸審核、異常交易監控。

**Sample：智能客服對話流程**
```python
# 金融業智能客服簡易範例
user_input = "請問我的信用卡額度是多少？"
if "信用卡額度" in user_input:
    reply = "您的信用卡額度為新台幣 10 萬元。"
else:
    reply = "請提供更詳細的問題描述。"
print(reply)
```

### 1-3-2 零售業
- 虛擬助理：商品推薦、庫存查詢、下單流程自動化。
- 客戶行為分析：預測購買意圖、個人化行銷。

**Sample：商品推薦邏輯**
```python
# 零售業商品推薦簡易範例
user_profile = {"age": 25, "gender": "female", "history": ["運動鞋", "瑜伽墊"]}
if "運動鞋" in user_profile["history"]:
    recommend = "推薦新品：輕量慢跑鞋"
else:
    recommend = "推薦熱銷商品：經典帆布鞋"
print(recommend)
```

### 1-3-3 教育領域
- AI 助教：自動批改作業、個人化學習建議。
- 智慧教室：即時互動問答、學習歷程分析。

**Sample：自動批改作業**
```python
# 教育領域自動批改簡易範例
answer = "台灣的首都是台北"
if "台北" in answer:
    score = 1
else:
    score = 0
print(f"得分：{score}")
```

### 1-3-4 醫療產業
- 智能問診：初步健康諮詢、症狀分類。
- 醫療影像分析：輔助診斷、異常偵測。

**Sample：症狀分類**
```python
# 醫療產業症狀分類簡易範例
symptom = "喉嚨痛，咳嗽"
if "喉嚨痛" in symptom and "咳嗽" in symptom:
    result = "可能為上呼吸道感染，建議就醫。"
else:
    result = "請提供更多症狀描述。"
print(result)
```

### 1-3-5 其他前沿應用
- 智慧城市：交通流量預測、能源管理。
- 智慧製造：設備預測維護、流程自動化。

**Sample：設備預測維護**
```python
# 智慧製造設備預測維護簡易範例
sensor_value = 85  # 假設溫度感測值
if sensor_value > 80:
    action = "警告：設備溫度過高，請檢查維護。"
else:
    action = "設備運作正常。"
print(action)
```

#### 案例分析建議
- 可繪製產業應用架構圖，標示 AI Agent 與 LLM 在系統中的角色。
- 分析實際案例的技術挑戰與解決方案。

---

## 1-5 綜合討論與未來展望

### 1-5-1 AI Agent 與 LLM 的融合趨勢
- LLM 作為 AI Agent 的語意理解與推理核心，推動多模態、多任務智能體發展。
- 代理人自主性、可解釋性、倫理安全等議題日益重要。

### 1-5-2 研究挑戰與開放問題
- 如何提升 AI Agent 的長期規劃與推理能力？
- LLM 如何結合外部知識庫與工具，實現更強的推理與行動？
- 多代理人協作下的溝通協議與博弈策略。

### 1-5-3 未來發展方向
- 自主學習與自我優化的智能體
- 跨領域、跨語言的泛化能力
- AI Agent 與人類協作的社會型應用

---

## 1-6 進階程式範例與實作練習

### 1-6-1 強化學習代理人（簡化版）
```python
import random

class SimpleRLAgent:
    def __init__(self):
        self.q_table = {}

    def choose_action(self, state):
        if state not in self.q_table:
            self.q_table[state] = {'A': 0, 'B': 0}
        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, state, action, reward):
        self.q_table[state][action] += 0.1 * (reward - self.q_table[state][action])

# 測試
agent = SimpleRLAgent()
state = 'start'
for _ in range(10):
    action = agent.choose_action(state)
    reward = random.choice([1, -1])
    agent.update(state, action, reward)
print(agent.q_table)
```

### 1-6-2 LLM API 串接（以 OpenAI GPT-3 為例）
```python
import openai
openai.api_key = 'YOUR_API_KEY'

response = openai.Completion.create(
    model='text-davinci-003',
    prompt='請用中文介紹 AI Agent 的應用',
    max_tokens=200
)
print(response.choices[0].text)
```

---

## 1-7 圖表建議與學習路徑

- 建議繪製 AI Agent 架構圖、LLM 訓練流程圖、產業應用案例圖。
- 學習路徑：
  1. 理論基礎 → 2. 經典文獻 → 3. 程式實作 → 4. 產業案例 → 5. 研究前沿