# line bot test
# require: pip install line-bot-sdk

import yaml
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

# config読み込み
with open("./conf/config.yml", mode='r', encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 定数定義
line_access_token = config["default"]["line_access_token"]
line_user_id = config["default"]["line_user_id"]

# インスタンス生成
line_bot_api = LineBotApi(line_access_token)

# 投稿内容
text_message ="test message"


try:
    # ラインユーザIDは配列で指定する。
    line_bot_api.multicast(
    [line_user_id], TextSendMessage(text=text_message)
)
except LineBotApiError as e:
    # エラーが起こり送信できなかった場合
    print(e)
