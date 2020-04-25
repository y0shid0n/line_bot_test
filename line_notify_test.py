# line notify test

import requests
import yaml

# config読み込み
with open("./conf/config.yml", mode='r', encoding="utf-8") as f:
    config = yaml.safe_load(f)

line_notify_token = config["default"]["line_notify_token"]
line_notify_api = 'https://notify-api.line.me/api/notify'
message = 'test'


payload = {'message': message}
headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
line_notify = requests.post(line_notify_api, data=payload, headers=headers)
