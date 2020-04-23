from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    TextMessage, TextSendMessage,
    AudioMessage,
)

from speechtranscript import SpeechTranscript
import os
import sys
import json
import requests
from pydub import AudioSegment

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['YOUR_CHANNEL_ACCESS_TOKEN']
YOUR_CHANNEL_SECRET = os.environ['YOUR_CHANNEL_SECRET']

FILE_PATH = './'
FILE_NAME = 'audio_message'

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

speechtranscript = SpeechTranscript()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
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


@handler.add(MessageEvent, message=AudioMessage)
def get_audio_content(event):
    line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)

    audio_content = line_bot_api.get_message_content(event.message.id)

    with open(FILE_PATH+FILE_NAME, 'wb') as fd:
        for chunk in audio_content.iter_content():
            fd.write(chunk)
    sound = AudioSegment.from_file(FILE_NAME, format="m4a")
    sound.export("audio_message", format="mp3")
    text_transcripted = speechtranscript.transcript(file_name=FILE_NAME)
    print(text_transcripted)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='audio_file'))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
