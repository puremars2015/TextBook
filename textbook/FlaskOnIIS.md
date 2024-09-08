## Python Flask 安裝在IIS的方法 - 使用 httpPlatformHandler

(https://docs.lextudio.com/blog/running-flask-web-apps-on-iis-with-httpplatformhandler/)

0. 假設要執行的python flask檔案,名稱為app.py,檔案夾為flaskDemo
1. 下載並安裝httpPlatformHandler(https://www.iis.net/downloads/microsoft/httpplatformhandler)
2. 視狀況重啟iis, 打開cmd, 指令: iisreset
3. 新增一個"網站", 網站的path就設定在要執行的python檔案的檔案夾
4. 設定web.config,該檔案建議放在flaskDemo
5. flaskDemo的權限要設定開放給IUSR跟IIS_IUSRS
6. python執行檔案的檔案夾,<label style="color:red">也要加入IIS_IUSRS</label>
7. web.config上面的python執行檔案

----flaskDemo/
   |
   ----app.py
   |
   ----web.config



### web.config
```web.config
<?xml version="1.0" encoding="utf-8"?>
<configuration>
	<system.webServer>
		<handlers>
			<add name="httpPlatformHandler" 
            path="*" 
            verb="*" 
            modules="httpPlatformHandler" 
            resourceType="Unspecified"  />
		</handlers>
		<httpPlatform 
        stdoutLogEnabled="true" 
        stdoutLogFile=".\logs\stdout.log" 
        startupTimeLimit="20" 
        processPath="C:\Users\Musoon_MA\AppData\Local\Programs\Python\Python312\python.exe" 
        arguments="-m flask run --port %HTTP_PLATFORM_PORT%"></httpPlatform>
	</system.webServer>
</configuration>
```


### app.py
```測試用app.py
from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['port'] = '5050'

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!"), 200
```


### 如果出現500.19的錯誤...

錯誤訊息:
這個設定區段不能在這個路徑中使用。當區段在父層級被鎖定時就會發生這種情況。鎖定可能是預設 (overrideModeDefault="Deny")，
或是由位置標記使用 overrideMode="Deny" 或繼承的 allowOverride="false" 明確設定。

解決方法:

編輯 applicationHost.config

找到 applicationHost.config 文件：

该文件通常位于 C:\Windows\System32\inetsrv\config\ 路径下。
查找 handlers 节：

打开 applicationHost.config 文件，查找 <section name="handlers" overrideModeDefault="Deny"/> 或类似的行。
修改为允许覆盖：

将 overrideModeDefault="Deny" 修改为 overrideModeDefault="Allow"，或完全删除这一行。
