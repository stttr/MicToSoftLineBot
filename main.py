from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import sys
import json
import requests

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']


line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)

    bj = json.loads(body)
    message_id = bj['events'][0]['message']['id']

    get_content(message_id)

    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def get_content(message_id):
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

    message_content = line_bot_api.get_message_content(message_id)

    sum_byte = 0
    for chunk in message_content.iter_content():
        print(chunk)
        sum_byte += sys.getsizeof(chunk)
        print(sys.getsizeof(chunk))
    
    print(sum_byte)

def speech_to_text():
    pass
    # APIに接続するための情報


    # url = os.environ['IBM_URL']
    # api_key = os.environ['IBM_API_KEY']
    #
    # # APIに送信する情報
    # headers = {'Content-Type': 'application/json', 'key':API_Key}
    # body = {date='today', area=Tokyo}
    #
    # # API接続の実行
    # result = requests.post(API_Endpoint, data=json.dumps(body), headers=headers)


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
