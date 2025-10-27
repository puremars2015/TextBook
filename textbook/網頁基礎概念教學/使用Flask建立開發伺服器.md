# 使用 Flask 建立開發伺服器

## 什麼是 Flask？

Flask 是一個輕量級的 Python Web 框架，非常適合用來快速建立 Web 應用程式和 API。它簡單易學，但功能強大，是初學者和專業開發者都喜愛的框架。

## 環境準備

### 1. 安裝 Python

確保你的電腦已安裝 Python 3.7 或更新版本。可以在終端機執行以下命令檢查：

```bash
python --version
```

### 2. 安裝 Flask

使用 pip 安裝 Flask：

```bash
pip install flask
```

## 建立第一個 Flask 應用程式

### 基礎範例

建立一個名為 `app.py` 的檔案，內容如下：

```python
from flask import Flask

# 建立 Flask 應用程式實例
app = Flask(__name__)

# 定義路由和對應的處理函數
@app.route('/')
def home():
    return 'Hello, Flask!'

@app.route('/about')
def about():
    return 'This is the about page.'

# 啟動開發伺服器
if __name__ == '__main__':
    app.run(debug=True)
```

### 執行應用程式

在終端機中執行：

```bash
python app.py
```

你會看到類似以下的輸出：

```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

現在打開瀏覽器，訪問 `http://127.0.0.1:5000`，就能看到你的應用程式了！

## 進階功能

### 1. 返回 HTML 頁面

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

記得在專案目錄中建立 `templates` 資料夾，並在其中放置 `index.html` 檔案。

### 2. 處理動態路由

```python
@app.route('/user/<username>')
def user_profile(username):
    return f'Hello, {username}!'
```

### 3. 處理 POST 請求

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form.get('data')
    return f'Received: {data}'
```

### 4. 返回 JSON 資料

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    data = {
        'name': 'John',
        'age': 30,
        'city': 'Taipei'
    }
    return jsonify(data)
```

## 開發伺服器設定

### 自訂主機和埠號

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

- `host='0.0.0.0'`: 允許外部裝置訪問（預設只能本機訪問）
- `port=8080`: 指定埠號（預設是 5000）
- `debug=True`: 啟用偵錯模式，修改程式碼後會自動重新載入

### 偵錯模式的優點

1. **自動重新載入**: 修改程式碼後，伺服器會自動重啟
2. **詳細錯誤資訊**: 瀏覽器會顯示詳細的錯誤堆疊追蹤
3. **互動式偵錯器**: 可以在瀏覽器中檢查變數值

⚠️ **注意**: 正式環境（Production）絕對不要使用 `debug=True`！

## 專案結構建議

```
my_flask_app/
│
├── app.py                 # 主要應用程式檔案
├── requirements.txt       # 依賴套件列表
│
├── templates/            # HTML 模板資料夾
│   ├── index.html
│   └── about.html
│
├── static/               # 靜態檔案資料夾
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
└── venv/                 # 虛擬環境（建議使用）
```

## 使用虛擬環境（建議）

### 建立虛擬環境

```bash
python -m venv venv
```

### 啟動虛擬環境

**Windows (PowerShell)**:
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD)**:
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

### 安裝依賴

```bash
pip install flask
```

### 匯出依賴列表

```bash
pip freeze > requirements.txt
```

## 常用 Flask 延伸套件

1. **Flask-SQLAlchemy**: 資料庫 ORM
2. **Flask-WTF**: 表單處理
3. **Flask-Login**: 使用者認證
4. **Flask-CORS**: 跨域資源共享
5. **Flask-RESTful**: RESTful API 開發

## 實用技巧

### 1. 設定環境變數

建立 `.env` 檔案：

```
FLASK_APP=app.py
FLASK_ENV=development
```

### 2. 使用藍圖 (Blueprints) 組織程式碼

適合大型專案，可以將不同功能模組化：

```python
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/users')
def get_users():
    return jsonify([{'id': 1, 'name': 'John'}])
```

### 3. 錯誤處理

```python
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return 'Internal Server Error', 500
```

## 下一步學習

1. 學習 Flask 的模板引擎 Jinja2
2. 了解如何連接資料庫
3. 學習 RESTful API 設計
4. 研究如何部署 Flask 應用程式到正式環境
5. 探索 Flask 的安全性最佳實踐

## 參考資源

- [Flask 官方文件](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Real Python Flask Tutorials](https://realpython.com/tutorials/flask/)

---

## 快速開始範本

最後，這裡是一個完整的快速開始範本：

```python
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# 首頁
@app.route('/')
def index():
    return render_template('index.html')

# API 端點
@app.route('/api/hello', methods=['GET'])
def api_hello():
    return jsonify({'message': 'Hello from Flask API!'})

# 處理表單提交
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    return jsonify({
        'status': 'success',
        'data': {
            'name': name,
            'email': email
        }
    })

# 動態路由
@app.route('/user/<int:user_id>')
def user_profile(user_id):
    return f'User Profile: {user_id}'

# 錯誤處理
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    # 開發模式設定
    app.run(
        host='127.0.0.1',  # 本機訪問
        port=5000,          # 埠號
        debug=True          # 啟用偵錯模式
    )
```

祝你學習愉快！🚀
