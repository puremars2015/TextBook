# 網站架構

目前的網站架構如下：

```
MyLineBots/
├── README.md
├── WEBAPI/
│   ├── app.py  # 主 Flask 應用程式
│   ├── routes/ # 各功能的 API 路由
│   ├── static/ # 靜態資源（CSS、JS、圖片等）
│   └── templates/ # HTML 模板
```

`app.py` 是主應用程式入口，`routes` 資料夾用於存放各功能的 API 路由，`static` 資料夾用於靜態資源，`templates` 資料夾用於 HTML 模板。