from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://devapi.qweather.com/v7/weather/now?location=101271401&key=02b35e6addfb4ae09f7467644e3bed96"
  res = requests.get(url).json()
  return res['now']['text'], int(res['now']['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime("2023-04-26", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_birthday_2():
  next = datetime.strptime("2023-05-14", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  wordDay = "今天是2023年5月5日，星期五。\n早上好呀宝儿，这两天身体不太舒服，还在忙着开题报告，有点冷落宝儿了，么么么么。爱你么么哒。\n"  
  if words.status_code != 200:
    return wordDay+get_words()  
  return wordDay+words.json()['data']['text']
  

#def get_random_color():
  #return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
#, "color":get_random_color()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"birthday_left_2":{"value":get_birthday_2()},"words":{"value":get_words()}}
res = wm.send_template(user_id, template_id, data)
print(res)
