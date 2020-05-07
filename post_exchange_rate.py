# 為替レートを取得して条件を満たしたときにlineに通知するbot

import os
import requests
import yaml
import json

# 通知したい条件（これを下回ったら通知）
target_ask = 105

# config読み込み
with open("./conf/config.yml", mode='r', encoding="utf-8") as f:
    config = yaml.safe_load(f)

# line notifyの設定
line_notify_token = config["default"]["line_notify_token"]
line_notify_api = 'https://notify-api.line.me/api/notify'

# 前回取得時の為替レートのファイル
last_ask_file = "./last_ask.txt"

# 前回取得時のレートを読み込む
# 存在しない場合は極大値をセット
if os.path.exists(last_ask_file):
    with open(last_ask_file) as f:
        last_ask = float(f.read())
else:
    last_ask = 99999999.9

# 為替レートの取得
rate_data = requests.get("https://www.gaitameonline.com/rateaj/getrate").json()
# USDJPYのみを取得
usd_jpy = {i for i in rate_data["quotes"] if i["currencyPairCode"] == "USDJPY"}
# 買値を取得
ask = float(usd_jpy["ask"])

# 買値がtarget_askを下回ったら通知
# 一度通知したら、再度target_askを上回るまでは通知したくない
if ask < target_ask and last_ask >= target_ask:
    message = f"ドル円レートが{target_ask}を下回ったよ！！！"
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
