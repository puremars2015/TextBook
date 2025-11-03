# Dockerfile - 用於將同目錄下的 app.py 打包成一個可執行網站容器
FROM python:3.11-slim

# 避免 Python 緩衝，利於日誌即時顯示
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 複製整個目錄（包含 app.py 與可選的 requirements.txt）
COPY . /app

# 更新 pip，若有 requirements.txt 則安裝，否則預設安裝 Flask
RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then \
      pip install --no-cache-dir -r requirements.txt; \
    else \
      pip install --no-cache-dir flask; \
    fi

# 若 app.py 在內部以 0.0.0.0:80 啟動則公開 80；若使用其他 port 請修改
EXPOSE 5678

# 啟動 app.py（請確保 app.py 使用 host='0.0.0.0' 並監聽相對應的 port）
CMD ["python", "app.py"]