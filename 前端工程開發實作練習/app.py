import json
from flask import Flask, Response, jsonify, make_response
from flask_cors import CORS
from flask import request

app = Flask(__name__)

# 允許跨域請求
CORS(app)

@app.route('/api/order', methods=['POST', 'OPTIONS'])
def receive_order():

    # 處理 OPTIONS 請求（預檢請求）
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response

    try:
        # 從請求中獲取 JSON 數據
        order_data = request.get_json()
        
        # 檢查是否包含必要的字段
        if not order_data or 'drink' not in order_data or 'name' not in order_data:
            return jsonify({
                'success': False,
                'message': '請提供飲料和姓名'
            }), 400
        
        drink = order_data.get('drink')
        name = order_data.get('name')
        
        # 這裡可以添加訂單處理邏輯，例如保存到數據庫

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
    app.run(debug=True, port=5900, host='0.0.0.0')
