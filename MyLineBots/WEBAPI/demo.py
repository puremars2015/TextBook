
# pip install flask
# pip install requests
# pip install openai

from flask import Flask, request, jsonify, render_template, abort
import requests
import json

import config

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = config.section["小馬的小秘書"]["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = config.section["小馬的小秘書"]["CHANNEL_SECRET"]

@app.route('/')
def index():
    return 'Hi, I am a chatbot!', 200

# @app.route('/callback', methods=['GET','POST'])
# def callback():
#     # 確認請求來自 LINE 平台
#     signature = request.headers['X-Line-Signature']

#     body = request.get_data(as_text=True)
#     try:
#         events = json.loads(body).get('events', [])
#     except:
#         abort(400)

#     for event in events:
#         if event['type'] == 'message' and event['message']['type'] == 'text':
#             reply_token = event['replyToken']
#             message_text = event['message']['text']
#             helper = MyGPT()
#             r = helper.TranslateGPT(message_text)
#             reply_message(reply_token, r)

#     return 'OK'

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
            reply_message(reply_token, message_text)

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
    app.run(host='0.0.0.0',port=5000, debug=True)