import datetime
from mcp.server.fastmcp import FastMCP
from flask import Flask, jsonify, render_template_string

mcp = FastMCP("TestMCP")
app = Flask(__name__)

# MCP Tools
@mcp.tool() 
def get_tpe_datetime():  
    """取得台北當前日期時間"""
    now = datetime.datetime.now()
    return "台北日期時間:" + now.strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def my_favorite_singer():
    """返回我最喜歡的歌手"""
    return "我最喜歡的歌手:周杰倫"
 
@mcp.tool()
def read_txt(filepath: str):
    """讀取文字檔案內容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"讀取失敗: {str(e)}"

@mcp.tool()
def write_txt(filepath: str, content: str, mode: str = 'w'):
    """寫入內容到文字檔案"""
    try:
        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)
        return f"寫入成功: {filepath}"
    except Exception as e:
        return f"寫入失敗: {str(e)}"

# Flask 路由 - 用於瀏覽器測試
@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>MCP Server 測試介面</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .tool-card {
                background: white;
                padding: 20px;
                margin: 15px 0;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
            .result {
                margin-top: 10px;
                padding: 10px;
                background-color: #e8f5e9;
                border-left: 4px solid #4CAF50;
                border-radius: 4px;
                display: none;
            }
            input, textarea {
                width: 100%;
                padding: 8px;
                margin: 5px 0;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>🔧 MCP Server 測試介面</h1>
        
        <div class="tool-card">
            <h2>取得台北時間</h2>
            <button onclick="callTool('get_tpe_datetime')">執行</button>
            <div id="result-datetime" class="result"></div>
        </div>

        <div class="tool-card">
            <h2>我最喜歡的歌手</h2>
            <button onclick="callTool('my_favorite_singer')">執行</button>
            <div id="result-singer" class="result"></div>
        </div>

        <div class="tool-card">
            <h2>讀取文字檔</h2>
            <input type="text" id="read-filepath" placeholder="輸入檔案路徑 (例如: test.txt)">
            <button onclick="readFile()">讀取</button>
            <div id="result-read" class="result"></div>
        </div>

        <div class="tool-card">
            <h2>寫入文字檔</h2>
            <input type="text" id="write-filepath" placeholder="輸入檔案路徑 (例如: test.txt)">
            <textarea id="write-content" rows="4" placeholder="輸入要寫入的內容"></textarea>
            <button onclick="writeFile()">寫入</button>
            <div id="result-write" class="result"></div>
        </div>

        <script>
            function callTool(toolName) {
                const resultDiv = document.getElementById('result-' + toolName.split('_').pop());
                fetch('/api/' + toolName)
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = '結果: ' + data.result;
                    })
                    .catch(error => {
                        resultDiv.style.display = 'block';
                        resultDiv.style.backgroundColor = '#ffebee';
                        resultDiv.style.borderColor = '#f44336';
                        resultDiv.textContent = '錯誤: ' + error;
                    });
            }

            function readFile() {
                const filepath = document.getElementById('read-filepath').value;
                const resultDiv = document.getElementById('result-read');
                
                fetch('/api/read_txt?filepath=' + encodeURIComponent(filepath))
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = '結果: ' + data.result;
                    })
                    .catch(error => {
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = '錯誤: ' + error;
                    });
            }

            function writeFile() {
                const filepath = document.getElementById('write-filepath').value;
                const content = document.getElementById('write-content').value;
                const resultDiv = document.getElementById('result-write');
                
                fetch('/api/write_txt', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({filepath: filepath, content: content})
                })
                    .then(response => response.json())
                    .then(data => {
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = '結果: ' + data.result;
                    })
                    .catch(error => {
                        resultDiv.style.display = 'block';
                        resultDiv.textContent = '錯誤: ' + error;
                    });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/api/get_tpe_datetime')
def api_datetime():
    result = get_tpe_datetime()
    return jsonify({'result': result})

@app.route('/api/my_favorite_singer')
def api_singer():
    result = my_favorite_singer()
    return jsonify({'result': result})

@app.route('/api/read_txt')
def api_read():
    from flask import request
    filepath = request.args.get('filepath', '')
    result = read_txt(filepath)
    return jsonify({'result': result})

@app.route('/api/write_txt', methods=['POST'])
def api_write():
    from flask import request
    data = request.json
    result = write_txt(data.get('filepath', ''), data.get('content', ''))
    return jsonify({'result': result})

if __name__ == '__main__':
    import threading
    
    # 在背景執行 MCP server
    def run_mcp():
        mcp.run(transport='sse')
    
    mcp_thread = threading.Thread(target=run_mcp, daemon=True)
    mcp_thread.start()
    
    # 啟動 Flask web 介面
    print("=" * 50)
    print("🚀 伺服器啟動中...")
    print("📱 網頁測試介面: http://localhost:5000")
    print("🔌 MCP SSE 端點: http://localhost:8000/sse")
    print("=" * 50)
    app.run(debug=True, port=5000, use_reloader=False)