from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
# 完全簡化的 CORS 設置
CORS(app, supports_credentials=True)  # 使用默認配置並支援憑證

@app.route('/')
def index():
    return "飲料訂單 API 服務運行中..."

@app.route('/api/order', methods=['POST', 'OPTIONS'])
def receive_order():
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

        print(f"收到訂單: {name} 訂購了 {drink}")
        
        # Log the order details for debugging
        app.logger.info(f"Order received - Name: {name}, Drink: {drink}")

        # 返回成功響應
        return jsonify({
            'success': True,
            'message': f'收到 {name} 的訂單: {drink}',
            'order': order_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'處理訂單時發生錯誤: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
