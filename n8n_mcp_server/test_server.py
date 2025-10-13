"""Test script for MCP Server endpoints"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """測試根端點"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_list_endpoints():
    """測試列出所有 endpoints"""
    print("\n=== Testing List Endpoints ===")
    response = requests.get(f"{BASE_URL}/endpoints")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_database_query():
    """測試資料庫查詢"""
    print("\n=== Testing Database Query ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "query_database",
            "arguments": {
                "sql": "SELECT * FROM users"
            }
        }
    }
    response = requests.post(
        f"{BASE_URL}/database_ops",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_file_list():
    """測試列出檔案"""
    print("\n=== Testing List Files ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "list_files",
            "arguments": {
                "directory": "."
            }
        }
    }
    response = requests.post(
        f"{BASE_URL}/file_handler",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_file_write_read():
    """測試寫入和讀取檔案"""
    print("\n=== Testing File Write ===")
    # 寫入檔案
    payload_write = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "write_file",
            "arguments": {
                "filepath": "test_output.txt",
                "content": "Hello from MCP Server test!"
            }
        }
    }
    response = requests.post(
        f"{BASE_URL}/file_handler",
        json=payload_write,
        headers={"Content-Type": "application/json"}
    )
    print(f"Write Status: {response.status_code}")
    print(f"Write Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n=== Testing File Read ===")
    # 讀取檔案
    payload_read = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "read_file",
            "arguments": {
                "filepath": "test_output.txt"
            }
        }
    }
    response = requests.post(
        f"{BASE_URL}/file_handler",
        json=payload_read,
        headers={"Content-Type": "application/json"}
    )
    print(f"Read Status: {response.status_code}")
    print(f"Read Response: {json.dumps(response.json(), indent=2)}")

def main():
    """執行所有測試"""
    print("=" * 50)
    print("MCP Server API Tests")
    print("=" * 50)
    
    try:
        test_root()
        test_list_endpoints()
        test_database_query()
        test_file_list()
        test_file_write_read()
        
        print("\n" + "=" * 50)
        print("All tests completed!")
        print("=" * 50)
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server")
        print("Please make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
