import ollama

content = """
bundle no | serial no| jumbo no|lot no| net weight|width|join|OD|meters
1471294688010 0380 3F092601 01 222.4 29.7 0 110 6296.4
1471294688010 0381 3F092601 05 222.4 29.7 0 110 6296.4
1471294688010 0382 3F092601 09 222.4 29.7 0 110 6296.4
1471294688010 0383 3F092602 01 222.4 29.7 0 110 6296.4
1471294688010 0384 3F092602 05 222.4 29.7 0 110 6296.4

轉換上面的資料為下方的json格式
[{
"bundle_no":"1471294688010",
"serial_no":"0380",
"jumbo_no":"3F092601",
"lot_no":"01",
"net_weight":"222.4",
"width":"29.7",
"join":"0",
"OD":"110",
"meters":"6296.4"
}]

注意:只要回傳轉換結果就好
"""

response = ollama.chat(
    model='gemma3:4b',  # 這裡改成你在 ollama 裡的實際模型名稱
    messages=[
        {'role': 'user', 'content': content}
    ],
)

print(response['message']['content'])
