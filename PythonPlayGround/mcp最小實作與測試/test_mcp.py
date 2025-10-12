import requests
import json

def test_rpc_list_tools():
    url = "http://127.0.0.1:8000/mcp"   # 只打到根路徑
    # Use 'initialize' method so the server can create a new session when
    # no mcp-session-id header is provided. After initialization you can use
    # the returned session id for subsequent calls.
    def make_payload(method: str, id: int = 1, params: dict | None = None):
        payload = {
            "jsonrpc": "2.0",
            "id": id,
            "method": method
        }
        # 只有當 params 不為 None 且不為空字典時才加入
        if params:
            payload["params"] = params
        return payload

    # initialize 需要包含 protocolVersion 和 clientInfo
    init_params = {
        "protocolVersion": "2024-11-05",
        "clientInfo": {
            "name": "test-client",
            "version": "1.0.0"
        },
        "capabilities": {}
    }
    init_payload = make_payload("initialize", id=1, params=init_params)
    headers = {"Content-Type": "application/json"}
    # The MCP server requires the client to accept both JSON and server-sent events
    # so include both in the Accept header.
    headers["Accept"] = "application/json, text/event-stream"
    # If your server requires a specific session ID, set it here. By default
    # we omit it so the server may create a new session. Example:
    # headers["mcp-session-id"] = "<your-session-id>"
    try:
        # 1) Send initialize (synchronous read, avoid streaming hang)
        r = requests.post(url, data=json.dumps(init_payload), headers=headers, timeout=5)
        print("Initialize status code:", r.status_code)

        # Try to get session id from response headers first
        session_id = r.headers.get("mcp-session-id")

        # Read raw body (may be SSE). We'll inspect r.text for the first data: line
        raw_text = r.text
        # Try to parse first 'data:' line if present
        if session_id is None and raw_text:
            for ln in raw_text.splitlines():
                if ln.startswith("data:"):
                    data_json = ln[len("data:"):].strip()
                    try:
                        parsed = json.loads(data_json)
                        if isinstance(parsed, dict):
                            if parsed.get("result") and isinstance(parsed.get("result"), dict):
                                session_id = parsed["result"].get("mcp-session-id") or parsed["result"].get("session_id")
                    except Exception:
                        pass
                    break

        print("Initialize response body:\n", raw_text)

        if session_id:
            print("Found session id from headers/body:", session_id)
        else:
            print("No session id found in headers or first SSE data. You may need to inspect the server logs or response to find the session id.")

        # 1.5) Send initialized notification (required by MCP protocol after initialize)
        if session_id:
            headers_with_session = dict(headers)
            headers_with_session["mcp-session-id"] = session_id
            # Notifications don't have an id field
            initialized_payload = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            r_init = requests.post(url, data=json.dumps(initialized_payload), headers=headers_with_session, timeout=5)
            print("Initialized notification status code:", r_init.status_code)

        # 2) If we have a session id, call tools/list; otherwise try calling tools/list without session id (may fail)
        # tools/list 不需要 params，所以不傳入
        tools_payload = make_payload("tools/list", id=2, params=None)
        if session_id:
            headers_with_session = dict(headers)
            headers_with_session["mcp-session-id"] = session_id
            r2 = requests.post(url, data=json.dumps(tools_payload), headers=headers_with_session, timeout=5)
        else:
            r2 = requests.post(url, data=json.dumps(tools_payload), headers=headers, timeout=5)

        print("tools/list status code:", r2.status_code)
        print("tools/list raw response:\n", r2.text)
        ct2 = r2.headers.get("Content-Type", "")
        
        # Parse SSE format response
        if ct2.startswith("text/event-stream"):
            # Extract JSON from SSE data: line
            for ln in r2.text.splitlines():
                if ln.startswith("data:"):
                    data_json = ln[len("data:"):].strip()
                    try:
                        parsed = json.loads(data_json)
                        if "result" in parsed:
                            print("\n=== tools/list 解析成功 ===")
                            print(json.dumps(parsed["result"], indent=2, ensure_ascii=False))
                        elif "error" in parsed:
                            print("\n=== tools/list 錯誤 ===")
                            print(json.dumps(parsed["error"], indent=2, ensure_ascii=False))
                    except Exception as e:
                        print("Failed to parse SSE data:", e)
                    break
        elif ct2.startswith("application/json"):
            try:
                print("tools/list JSON:")
                print(json.dumps(r2.json(), indent=2, ensure_ascii=False))
            except Exception as e:
                print("Failed to parse tools/list JSON:", e)
        else:
            print("tools/list response is not JSON (Content-Type: {}), raw body printed above.".format(ct2))

    except Exception as e:
        print("Error during requests:", e)

if __name__ == "__main__":
    test_rpc_list_tools()
