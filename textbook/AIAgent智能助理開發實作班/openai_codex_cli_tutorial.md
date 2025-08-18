以下是一篇關於 OpenAI Codex CLI 的研究與教學文章，適合用於教育、開發者培訓或部落格分享，涵蓋安裝、功能、實作範例與教學應用等主題。

---

# 💻 OpenAI Codex CLI 教學與研究：打造你的終端機 AI 程式助手

## 一、什麼是 OpenAI Codex CLI？

OpenAI Codex CLI 是一款開源的命令列工具，將 OpenAI 的先進推理模型（如 o4-mini）引入本地終端機，讓開發者能以自然語言與 AI 互動，進行程式碼生成、錯誤修復、重構與執行等任務。它支援多模態輸入（文字、截圖、圖表），並提供三種互動模式，讓使用者依需求調整 AI 的自主程度。([DataCamp][1])

## 二、安裝與設定

### 系統需求

* 作業系統：macOS 12+、Ubuntu 20.04+/Debian 10+，或 Windows 11（需使用 WSL2）
* Node.js：版本 22 或更新版（建議使用 LTS 版本）
* Git：版本 2.23+（非必要，但建議安裝）
* RAM：至少 4GB（建議 8GB 以上）([Hugging Face][2], [DataCamp][1])

### 安裝步驟

1. 安裝 Node.js 和 Git。
2. 透過 npm 全域安裝 Codex CLI：([Hugging Face][2])

   ```bash
   npm install -g @openai/codex
   ```


3\. 設定 OpenAI API 金鑰：([GitHub][3])

```bash
export OPENAI_API_KEY="你的 API 金鑰"
```


可將上述指令加入 `~/.bashrc` 或 `~/.zshrc` 以永久設定。

## 三、核心功能與使用模式

### 三種互動模式

| 模式名稱      | 說明                            | 適用情境                |                                   |
| --------- | ----------------------------- | ------------------- | --------------------------------- |
| Suggest   | 預設模式，AI 提出建議，需使用者確認後才執行。      | 安全探索、程式碼審查、學習新程式碼庫。 |                                   |
| Auto Edit | AI 可自動讀寫檔案，但執行 shell 指令前仍需確認。 | 重構或重複性編輯，需監控副作用時。   |                                   |
| Full Auto | AI 全自動讀寫檔案並執行指令，於沙盒環境中運行。     | 修復建置錯誤、原型開發等長時間任務。  | ([OpenAI 幫助中心][4], [DataCamp][1]) |

### 多模態輸入

Codex CLI 支援文字、截圖、圖表等輸入形式，能根據這些資料生成或編輯程式碼。([OpenAI 幫助中心][4])

## 四、實作範例

### 1. 建立靜態網站

使用截圖作為設計參考，讓 Codex CLI 生成對應的 HTML/CSS：

```bash
codex --image "路徑/至/截圖.png"
```



AI 會分析截圖，並生成相應的網站結構與樣式。

### 2. 建立機器學習推論應用

讓 Codex CLI 建立一個完整的 FastAPI 應用，包括模型訓練與推論介面：

```bash
codex --approval-mode full-auto "建立一個具有使用者介面的 FastAPI 機器學習應用"
```



AI 會自動生成所需的檔案與程式碼，並提供執行指令。

## 五、教學應用與研究潛力

研究顯示，AI 程式碼生成工具如 Codex CLI 能提升初學者的程式撰寫效率，並在不影響理解能力的情況下，增進學習成果。此外，這些工具也能協助教師自動生成練習題與程式碼解釋，提升教學效率。

## 六、進階設定與安全性

* 支援 `.env` 檔案與 `~/.codex/config.yaml` 進行進階設定。
* 在 macOS 上使用 Apple Seatbelt，在 Linux 上使用 Docker 進行沙盒化，確保執行安全。
* 可透過 `--provider` 參數切換不同的模型提供者，如 OpenAI、Azure 等。([blott.studio][5], [Medium][6], [MachineLearningMastery.com][7])

## 七、結語

OpenAI Codex CLI 為開發者提供了一個強大的工具，能在終端機中以自然語言與 AI 互動，進行程式碼的生成與修改。無論是用於教學、開發還是研究，Codex CLI 都展現了其高度的靈活性與實用性。

---

如果您需要進一步的協助，例如撰寫特定主題的教學文章、製作課程教材或設計練習題，歡迎隨時提出，我將樂意為您提供支援。

[1]: https://www.datacamp.com/tutorial/open-ai-codex-cli-tutorial?utm_source=chatgpt.com "OpenAI Codex CLI Tutorial - DataCamp"
[2]: https://huggingface.co/blog/lynn-mikami/openai-codex-cli?utm_source=chatgpt.com "Getting Started with OpenAI Codex CLI: Open Source AI Coding ..."
[3]: https://github.com/openai/codex?utm_source=chatgpt.com "openai/codex: Lightweight coding agent that runs in your terminal"
[4]: https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started?utm_source=chatgpt.com "OpenAI Codex CLI – Getting Started"
[5]: https://www.blott.studio/blog/post/openai-codex-cli-build-faster-code-right-from-your-terminal?utm_source=chatgpt.com "OpenAI Codex CLI: Build Faster Code Right From Your Terminal"
[6]: https://girff.medium.com/openai-codex-cli-your-terminals-new-ai-assistant-windows-macos-server-guide-22371b63839b?utm_source=chatgpt.com "OpenAI Codex CLI: Your Terminal's New AI Assistant (Windows ..."
[7]: https://machinelearningmastery.com/understanding-openai-codex-cli-commands/?utm_source=chatgpt.com "Understanding OpenAI Codex CLI Commands"
