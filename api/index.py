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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()