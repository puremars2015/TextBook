from flask import Flask, request, jsonify, render_template, abort
import requests
import json
from lib.gpt_helper import MyGPT
from lib.file_helper import save_to_file, generate_random_filename_with_timestamp
from code_gpt_engine_helper import auto_generate_code
import my_config

#---以下是從langflow的code中抄來的---
import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "a77ae42a-5e69-4e74-9b70-baf439d82be4"
FLOW_ID = "cad8edef-3f7c-4147-965e-a6542522a46b"
APPLICATION_TOKEN = "AstraCS:HeZRYcspcZdvFXZLjHgogGwe:a12148bd7b63916a0c60634f39155245d07d7e5b5309ff7fed0d84ba26beb4ee"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-1FsZt": {},
  "Prompt-fOg1S": {},
  "ChatOutput-o7c1K": {},
  "OpenAIModel-DLN21": {}
}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

#---以上是從langflow的code中抄來的---



app = Flask(__name__)

# 替換為你的 Channel Access Token
CHANNEL_ACCESS_TOKEN = my_config.section['CHANNEL_ACCESS_TOKEN']
# 替換為你的 Channel Secret
CHANNEL_SECRET = my_config.section['CHANNEL_SECRET']

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
            # 以下嵌入要改變的對話------
            js = run_flow(message_text, ENDPOINT or FLOW_ID, "chat", "chat", TWEAKS, APPLICATION_TOKEN)
            text = js["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
            print(f"message_text: {text}")
            # 以上嵌入要改變的對話------
            reply_message(reply_token, text)

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
    app.run(host='0.0.0.0',port=5050)