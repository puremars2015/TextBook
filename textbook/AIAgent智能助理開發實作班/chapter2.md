# 2. 🛠️ AI 專案規劃與初步實作

---

## 2-1 專案目標設定與需求分析

### 2-1-1 專案目標理論基礎與學術脈絡
AI 專案目標設定是人工智慧系統工程的核心，涉及軟體工程、系統工程、管理科學等多領域理論。明確的目標有助於資源分配、風險控管與成果評估。常用理論包括 SMART 原則、OKR、KPI、Balanced Scorecard 等。AI 項目目標設定還需考慮倫理、隱私、可解釋性等新興議題。

#### 步驟與實作
1. **問題定義與需求動機**：
   - 以問題導向（Problem-driven）或技術導向（Technology-driven）出發，明確描述要解決的業務或技術問題。
2. **目標拆解與層級化**：
   - 採用目標分解法（Goal Decomposition），將總體目標分解為可執行的子目標與里程碑。
   - 實作：繪製目標分解樹（Goal Tree）。
3. **指標設計與評估**：
   - 設計可量化的評估指標（如準確率、回應時間、用戶滿意度、資安合規性）。
   - 參考 ISO/IEC 25010 軟體品質模型。
4. **風險評估與管理**：
   - 分析技術、資料、資源、倫理、法規等潛在風險，並規劃緩解措施。
   - 實作：建立風險矩陣（Risk Matrix）。

#### 實例
- 目標：「開發一個能自動回應 80% 常見問題的 AI 客服系統，並將人工客服量降低 50%。」
- 指標：「系統回應準確率 > 90%，平均回應時間 < 2 秒。」
- 風險：「資料偏見導致模型不公平」、「用戶資料外洩」等。

#### 圖表建議
- 目標分解樹、風險矩陣、KPI Dashboard。

---

### 2-1-2 需求分析理論、方法與實務
需求分析是軟體工程與人機互動（HCI）領域的基礎，常用方法有用戶故事（User Story）、UML 用例圖、需求訪談、問卷調查、焦點團體、情境分析（Scenario Analysis）、設計思考（Design Thinking）等。

#### 詳細步驟
1. **利害關係人分析**：
   - 識別專案相關人員（用戶、管理者、開發者、法規單位、維運人員）。
   - 實作：繪製利害關係人地圖（Stakeholder Map）。
2. **需求蒐集**：
   - 訪談、問卷、觀察、文件分析、焦點團體。
   - 實作：設計半結構式訪談大綱。
3. **需求建模**：
   - 用 UML 用例圖、流程圖、ERD、用戶旅程圖（User Journey Map）等工具建模。
   - 實作：draw.io、PlantUML、Miro。
4. **需求驗證與溝通**：
   - 與用戶反覆確認需求正確性與完整性，進行需求審查會議。
   - 實作：需求追蹤矩陣（Requirement Traceability Matrix）。

#### 實作建議
- 撰寫用戶故事：「作為一名客服人員，我希望 AI 能自動回覆常見問題，讓我能專注於複雜案件。」
- 畫出用例圖，標示主要功能與互動對象。
- 設計需求文件範本（SRS, Software Requirement Specification）。

#### 延伸閱讀
- Sommerville, I. (2016). Software Engineering.
- Preece, J., Rogers, Y., & Sharp, H. (2015). Interaction Design.

---

## 2-2 功能模組拆解與架構設計

### 2-2-1 軟體架構理論與設計模式
AI 系統常見架構有分層架構（Layered Architecture）、微服務（Microservices）、事件驅動（Event-driven）、黑板架構（Blackboard Architecture）、管道-過濾器（Pipe-Filter）等。良好的架構有助於模組化、可維護性與擴展性。

#### 模組拆解原則
- 高內聚、低耦合（Cohesion & Coupling）
- 單一職責原則（SRP, Single Responsibility Principle）
- 明確定義介面與資料流（Interface & Data Flow）
- 依據 DDD（Domain-Driven Design）劃分子領域

#### 常見 AI 助理模組
1. **對話管理（Dialog Manager）**：負責對話狀態追蹤與流程控制。
2. **自然語言理解（NLU）**：將用戶輸入轉換為結構化意圖與參數。
3. **任務管理（Task Manager）**：處理待辦事項、提醒、任務分派。
4. **知識庫/FAQ 模組**：儲存常見問題與答案。
5. **回饋與學習模組**：收集用戶回饋，驅動模型優化。
6. **外部 API 整合**：串接天氣、行事曆、資料查詢等服務。
7. **安全與隱私模組**：權限控管、資料加密、合規性檢查。

#### UML 與流程圖實作
- 畫出系統架構圖、資料流圖（DFD）、時序圖、組件圖。
- 建議使用 draw.io、PlantUML、UMLet、Miro。

#### 進階設計模式
- 觀察者模式（Observer）、策略模式（Strategy）、工廠模式（Factory）、中介者模式（Mediator）等。

#### 圖表建議
- 系統架構圖、模組互動圖、資料流圖、時序圖。

---

## 2-3 資料蒐集、標註與品質控管

### 2-3-1 資料需求分析與倫理考量
- 明確定義訓練、測試、驗證所需資料型態與規模。
- 分析資料來源（內部歷史紀錄、公開語料、網路爬蟲等）。
- 資料隱私、GDPR、資料偏見與倫理議題。

### 2-3-2 資料標註與品質控管
- 設計標註規則（如意圖分類、槽位填充、情感標註）。
- 建立標註團隊與流程，進行多輪審查與一致性檢查（Inter-annotator Agreement, Kappa Score）。
- 使用標註工具（如 Label Studio、Prodigy、Doccano）。

### 2-3-3 資料前處理與增強
- 分詞、去除雜訊、正規化、資料增強（Data Augmentation）。
- 資料分割（訓練/驗證/測試集），交叉驗證（Cross-validation）。

#### 範例程式：資料前處理（Python）
```python
import re

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

print(preprocess('Hello, AI Agent! 2025.'))
```

---

## 2-4 基本對答系統設計與實作

### 2-4-1 對話系統理論與分類
- 基於規則（Rule-based）、檢索式（Retrieval-based）、生成式（Generative-based）三大類。
- 對話狀態追蹤（Dialog State Tracking）、多輪對話管理、上下文維護。

### 2-4-2 Python 範例：規則式對答系統
```python
def chatbot(text):
    if '你好' in text:
        return '哈囉！很高興認識你。'
    elif '幫忙' in text:
        return '請問需要什麼協助？'
    elif '天氣' in text:
        return '今天天氣晴朗，適合出門！'
    else:
        return '目前只支援簡單問候與協助，歡迎提出建議！'

# 測試
print(chatbot('你好'))
print(chatbot('可以幫忙嗎？'))
print(chatbot('請問天氣如何？'))
```

### 2-4-3 進階：NLU 與意圖分類
- 使用 scikit-learn、spaCy、transformers 等工具訓練意圖分類模型。
- 範例：
```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

X = ['查詢天氣', '訂餐', '查詢訂單', '取消訂單']
y = ['天氣', '訂餐', '查詢', '取消']
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)
clf = MultinomialNB().fit(X_vec, y)

print(clf.predict(vectorizer.transform(['我要查天氣'])))
```

### 2-4-4 生成式對話系統（基於 LLM）
- 使用 HuggingFace Transformers、OpenAI API 等。
- 範例：
```python
from transformers import pipeline
chatbot = pipeline('text-generation', model='gpt2')
print(chatbot('請介紹 AI 助理', max_length=50))
```

---

## 2-5 測試、驗證與優化

### 2-5-1 單元測試與整合測試
- 撰寫測試案例，檢查每個模組功能。
- 使用 pytest、unittest、doctest 等工具。
- 持續整合（CI）、自動化測試。

### 2-5-2 性能評估與指標
- 準確率、召回率、F1 分數、用戶滿意度、平均回應時間。
- 壓力測試（Load Testing）、資源監控（Prometheus、Grafana）。
- A/B 測試、用戶行為分析。

### 2-5-3 持續優化與 DevOps
- 根據測試與用戶回饋調整規則、模型與流程。
- 版本控管（Git）、自動化部署（CI/CD）、回滾機制。
- 模型監控與自動重訓（Model Retraining）。

#### 範例程式：單元測試（Python）
```python
def test_chatbot():
    assert chatbot('你好') == '哈囉！很高興認識你。'
    assert chatbot('可以幫忙嗎？') == '請問需要什麼協助？'
    assert chatbot('請問天氣如何？') == '今天天氣晴朗，適合出門！'
test_chatbot()
print('所有測試通過')
```

---

## 2-6 產業案例與學術資源

### 2-6-1 產業案例
- 金融：智能客服、詐騙偵測、智能投顧、合規審查。
- 零售：自動化訂單處理、商品推薦、客戶分群、庫存預測。
- 教育：AI 助教、學習歷程分析、自適應學習系統。
- 醫療：智能問診、醫療影像分析、健康管理。

### 2-6-2 學術資源
- Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing.
- Russell, S., & Norvig, P. (2021). Artificial Intelligence: A Modern Approach.
- Papers with Code: https://paperswithcode.com/
- arXiv: https://arxiv.org/
- ACL Anthology: https://aclanthology.org/

---

## 2-7 進階實作練習

### 2-7-1 多模組協作範例
```python
class DialogManager:
    def __init__(self):
        self.state = {}
    def update(self, user_input):
        # 根據 NLU 結果更新狀態
        pass

class NLU:
    def parse(self, text):
        # 回傳意圖與參數
        return {'intent': '查詢', 'slots': {}}

class TaskManager:
    def handle(self, intent, slots):
        if intent == '查詢':
            return '這是查詢結果'
        return '尚未支援此功能'

# 主流程
nlu = NLU()
dm = DialogManager()
tm = TaskManager()
user_input = '我要查天氣'
parsed = nlu.parse(user_input)
dm.update(user_input)
response = tm.handle(parsed['intent'], parsed['slots'])
print(response)
```

### 2-7-2 產業級專案架構實作
- 以 Flask/FastAPI + Celery + Redis + PostgreSQL 為例，設計一個可擴展的 AI 助理系統。
- 提供 Docker Compose 部署範例。
- 程式碼略。

---

## 2-8 UML 圖表與設計文件建議
- 系統架構圖、資料流圖、用例圖、時序圖、組件圖、部署圖。
- 設計文件範本：需求規格書（SRS）、架構設計書（SAD）、測試計畫書（STP）、維運手冊。
- 建議附上範例模板與繪圖工具教學。

---

## 2-9 研究挑戰、未來展望與延伸閱讀
- AI 專案的跨領域協作挑戰、資料倫理、可解釋性、模型壽命管理。
- 未來趨勢：AutoML、MLOps、AI for Good、AI 安全。
- 延伸閱讀：
  - Amershi, S., et al. (2019). Software Engineering for Machine Learning: A Case Study.
  - Sculley, D., et al. (2015). Hidden Technical Debt in Machine Learning Systems。
