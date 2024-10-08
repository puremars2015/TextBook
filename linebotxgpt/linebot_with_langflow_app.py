
# pip install flask
# pip install requests
# pip install openai

from lib.sqlite_helper import SQLiteHelper

from flask import Flask, request, jsonify, render_template, abort
import requests
import json

from lib.gpt_helper import MyGPT
from lib.file_helper import save_to_file, generate_random_filename_with_timestamp

from code_gpt_engine_helper import auto_generate_code

import my_config

from datetime import datetime

app = Flask(__name__)

# 替換為你的 Channel Access Token
CHANNEL_ACCESS_TOKEN = my_config.section['CHANNEL_ACCESS_TOKEN']
# 替換為你的 Channel Secret
CHANNEL_SECRET = my_config.section['CHANNEL_SECRET']

def get_key(source):
    if source['type'] == "group":
        return source['groupId'] if source['groupId'] is not None else ""
    elif source['type'] == "room":
        return source['roomId'] if source['roomId'] is not None else ""
    elif source['type'] == "user":
        return source['userId']
    else:
        return ""

        
@app.route('/')
def index():
    return 'Hi, I am a chatbot!', 200

@app.route('/callback', methods=['GET','POST'])
def callback():
    # 確認請求來自 LINE 平台
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    try:
        events = json.loads(body).get('events', [])
    except:
        abort(400)

    for event in events:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            reply_token = event['replyToken']
            message_text = event['message']['text']
            event_source = event['source']

            d = datetime.now().date()

            messages = []
            # messages.append({'role': 'system', 'content': '你是一個鶴茶樓的店員,只會使用繁體中文,專門負責幫客人點餐,並檢查是否有提到訂購人的電話跟姓名稱謂'})
            # messages.append({'role': 'user', 'content': f'今天是{d}'})

            db = SQLiteHelper('linebotxgpt.db')
            db.execute_query('INSERT INTO bot_memory (role,content,line_id) VALUES (?,?,?)', ('user', message_text, get_key(event_source)))
            data = db.execute_read_query(f'SELECT role,content FROM bot_memory WHERE line_id = "{get_key(event_source)}" ORDER BY id')    
            messages.extend([{'role': role, 'content': content} for role, content in data])

            # helper = MyGPT()
            # r = helper.MemoryGPT(messages)

            import subprocess

            # 使用 subprocess.run 來執行命令
            command = ['python', 'my_langflow_helper.py', message_text]
            result = subprocess.run(command, capture_output=True, text=True)
            return_message = result.stdout

            data = json.loads(return_message)
            # 取出 "text" 的值
            r = data['outputs'][0]['outputs'][0]['results']['message']['data']['text']


            db.execute_query('INSERT INTO bot_memory (role,content,line_id) VALUES (?,?,?)', ('assistant', r, get_key(event_source)))
            reply_message(reply_token, r)

    return 'OK'

def reply_message(reply_token, message_text):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {CHANNEL_ACCESS_TOKEN}'
    }

    data = {
        'replyToken': reply_token,
        'messages': [
            {
                'type': 'text',
                'text': message_text
            }
        ]
    }

    response = requests.post(
        'https://api.line.me/v2/bot/message/reply',
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code != 200:
        print('Failed to send message:', response.status_code, response.text)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5050,debug=True)