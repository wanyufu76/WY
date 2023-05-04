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

app = Flask(__name__)

line_bot_api = LineBotApi('pXckCMa8Foxfi8s5c0dApP2rCgrjQZzVCI7xmdexXbJxfIrpqyUKM/OugdnTWd8oktfef05z7IUro3T6vSq7dn4pJSbihYnqMYT3MRJnkpWqFHq6eEJQFNVt7/9u1auYpJiaMhxHKs7fP+o1pMew/QdB04t89/1O/w1cDnyilFU=')
webhook_handler = WebhookHandler('aa9dc5e2812d0f06ba44a63957fc1023')

import openai
import os

# 設定 OpenAI API 密鑰
# openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = "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"

# 輸入文本
input_text = "今天天氣很好，請用中文回答。請做一首跟天氣有關的詩"

# 設定 GPT-3.5 模型的檢索引擎
model_engine = "text-davinci-003"

# 設定生成的文本長度
output_length = 300


@app.route("/")
def home():
    return "Line Bot API Server is running."


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    response = openai.Completion.create(
        engine=model_engine,
        prompt=event.message.text,
        max_tokens=output_length,
    )

    output_text = response.choices[0].text.strip()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=output_text))
    
   


if __name__ == "__main__":
    app.run()