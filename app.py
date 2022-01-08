from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('9r6i8kSQ8670AKQ2Y70TI8EHMnQmtQJfH0bQhKgsNQ49oAWtlAAjgjrVuenkblNninqXStAXAFET1+n3pozCIzrrlzpSnxhZU2HgV9Gg3AmeAF5l5Athej+fhyazcpRpB8Nuc37a91+3W3YUo/wt5gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ad7b08690ed2cfd44c02f29df3deb8c6')


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
    msg = event.message.text
    r = '很抱歉，我看不懂您說什麼'

    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        )

        line_bot_api.reply_message(
            event.reply_token,
            
            sticker_message)
        return

    if msg in ['hi' , 'Hi']:
        r = '哈囉，很高興認識你～'
    elif msg == '這是什麼？':
        r = '用了就知道哇～'
    elif msg == '好酷':
        r = '謝謝讚美 ><'
    elif '?' in msg:
        r = '已記錄您的問題，稍晚會儘快回復您～'
    elif '？' in msg:
        r = '已記錄您的問題，稍晚會儘快回復您～'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text= r))


if __name__ == "__main__":
    app.run()