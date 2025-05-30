from flask import Blueprint, json, request, jsonify
import requests

from WEBAPI import config
from WEBAPI.library.gpt_helper import MyGPT

translator_bp = Blueprint('translator', __name__)

CHANNEL_ACCESS_TOKEN = config.section["小馬的小秘書"]["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = config.section["小馬的小秘書"]["CHANNEL_SECRET"]

@translator_bp.route("/translator", methods=['GET', 'POST'])
def translator():
    if request.method == 'POST':
        # 處理 POST 請求
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
                helper = MyGPT()
                r = helper.TranslateGPT(message_text)
                reply_message(reply_token, r)

        return 'OK'
    elif request.method == 'GET':
        # 處理 GET 請求
        user_message = "Hello, this is a GET request!"
        reply_message = f"You said: {user_message}"
        return jsonify({"reply": reply_message})
    
    
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