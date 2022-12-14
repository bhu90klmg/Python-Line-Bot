from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler

from linebot.exceptions import InvalidSignatureError

from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)

line_bot_api = LineBotApi('Fr1wlaDlEUMzQMR49g5iKmzE9yZWn5BaGNhORIPDct0UONifMHknJ4nW42xM0atNwXGjK4XLKDUTlenwbWWvJS9uHGe1iNdY7W1PbiP2kJa4HXkfemLFXnnrlLG3MqFgulsFDT8/F6ORCZVcKiUxAAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d5b2555e7f32cfce4dc1fa10ea4a52c6')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()