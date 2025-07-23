import json
from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask import request

app = Flask(__name__)

# 允許跨域請求
CORS(app)

@app.route('/', methods=['GET'])
def hello():
    data = {
        "message": "Hello, World!",
        "status": "success"
    }
    return jsonify(data)

@app.route('/api/data', methods=['POST'])
def get_data():
    data = request.get_json()
    return jsonify(data)

@app.route('/api/order', methods=['POST'])
def process_order():
    data = request.get_json()
    drink = data.get('drink', '')
    name = data.get('name', '')
    
    # 這裡可以添加訂單處理邏輯，例如儲存到資料庫
    response_message = json.dumps({"message":f"{name} 的訂單已收到，您選擇的飲料是: {drink}"})

    return Response(response_message, content_type='application/json; charset=utf-8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
