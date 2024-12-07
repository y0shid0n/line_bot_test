# ピューロランドの来場予約の空きを確認する
# lxmlのインストールが必要

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import yaml
import time
from bs4 import BeautifulSoup
import requests

# config読み込み
with open("./conf/config.yml", mode='r', encoding="utf-8") as f:
    config = yaml.safe_load(f)

# line notifyの設定
line_notify_token = config["default"]["line_notify_token"]
line_notify_api = 'https://notify-api.line.me/api/notify'

# オプション
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('--headless')

# driver
driver = webdriver.Chrome(options=ChromeOptions)

# 対象のurl
target_url = "https://www.puroland.jp/passport/"

# ページを開く
driver.get(target_url)

# ラズパイだと時間がかかるので待機時間を設定
# driver.implicitly_wait(30)
# time.sleep(20)
wait = WebDriverWait(driver, 20)
wait.until(expected_conditions.visibility_of_all_elements_located((By.CLASS_NAME, "c-btns c-row")))

# htmlを取得
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, 'lxml')

# 全日付のliタグを取得
li_tag_classes = soup.find_all(attrs={"class": "c-passport-calendar-list__item"})

# 1つ目のspanタグに日付が入っているので14日になっているものを取得
li_tag_target = [li_tag for li_tag in li_tag_classes if "14日" in li_tag.find("span").text][0]

# アイコンの状態を取得
icon_status = li_tag_target.find("svg").find("use").get("xlink:href")

# アイコンがcloseでなければ通知する
if icon_status != "#icon-traffic-circle-close":
    message = f"来場予約に空きが出たよ！"
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
# テスト用
else:
    message = f"来場予約に空きはないよ！"
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
