## n8n個人本地安裝方法：使用 Docker 或 Docker Compose（推薦，穩定可持續使用）

此方式適合：需要環境一致性、方便升級與設定資料持久化的情境。

---
### 方式 1：快速體驗（無持久化）
用途：臨時或功能試用；關閉終端或 Ctrl + C 即停止並刪除容器。

```bash
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
```

---
### 方式 2：正式使用（推薦：Docker Compose + 持久化）
建立 `docker-compose.yml`：

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "127.0.0.1:5678:5678"
    volumes:
      - n8n_storage:/home/node/.n8n
volumes:
  n8n_storage:
```

啟動服務：

```powershell
docker compose up -d
```

開啟瀏覽器：
http://127.0.0.1:5678

---
#### 補充建議
- 若需外網存取，可將 `127.0.0.1:5678:5678` 改為 `5678:5678`，並自行加上 Proxy / SSL（例如：Caddy / Nginx / Traefik）。
- 升級版本：
  1. `docker compose pull`
  2. `docker compose up -d`
- 匯出設定：資料位於 volume 對應的目錄（容器內路徑：`/home/node/.n8n`）。

---
完成後即可使用 n8n 介面進行流程開發。