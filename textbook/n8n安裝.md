
安裝方法二：使用 Docker 或 Docker Compose（推薦穩定可持續使用）

這種方式適合想確保環境一致性、並方便設定資料持久化的使用者：

快速容器跑起來（無持久化）
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n


用途：快速測試用。終端 Ctrl + C 即可停止 
Latenode Official Community
+1
。

建議：使用 Docker Compose 配置持久化

建立 docker-compose.yml，範例如下：

version: '3.8'
volumes:
  n8n_storage:

services:
  n8n:
    image: n8nio/n8n:latest
    restart: always
    ports:
      - "127.0.0.1:5678:5678"
    volumes:
      - n8n_storage:/home/node/.n8n


執行：

docker compose up -d


啟動後即可在 http://127.0.0.1:5678 使用