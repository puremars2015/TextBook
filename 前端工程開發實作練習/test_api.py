import requests
import json

def test_order_api():
    url = 'http://localhost:5000/api/order'
    
    # 測試用數據
    test_data = {
        'drink': '珍珠奶茶',
        'name': '小馬'
    }
    
    # 發送 POST 請求
    try:
        response = requests.post(url, json=test_data)
        
        # 打印響應狀態碼和內容
        print(f"狀態碼: {response.status_code}")
        print(f"響應內容: {response.json()}")
        
        return response.json()
    except Exception as e:
        print(f"發生錯誤: {str(e)}")
        return None

if __name__ == '__main__':
    print("開始測試 API...")
    test_order_api()
