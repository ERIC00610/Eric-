from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('WVLgVUWyn8HNzx/pnM50aJAn387xz+7wN7E4DG8axlV4IZahRZjAKBB2BGFWFP4Hvl+cZwA7e5js9F1cMLzRA9yFeuzStYF6TgzkGCksEZpYHI8Und5I++8WaVqIoslR3ov4XW8yC/CJWXk5L6FWIAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6eb5bb3788f614b02fc27494dfc6d230')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    reply_text = f"你吃了：{user_message}\n我來幫你查營養資訊中…"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run()
