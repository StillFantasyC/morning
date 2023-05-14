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

def get_days():
  words = "2023年5月15日，星期一。"
  return words

def get_words():
  words = "讨人厌的周一，忙碌的开始，依然爱你么么哒。\n"
  return words

def get_weather():
  url = "https://devapi.qweather.com/v7/weather/now?location=101271401&key=02b35e6addfb4ae09f7467644e3bed96"
  res = requests.get(url).json()
  return res['now']['text'], int(res['now']['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_count_2():
  delta = today - datetime.strptime("2023-04-28", "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime("2023-04-26", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days + 1

def get_birthday_2():
  next = datetime.strptime("2023-05-14", "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days + 1

def get_words_2():
  words = requests.get("https://api.shadiao.pro/chp")   
  if words.status_code != 200:
    return get_words_2()  
  if len(words.json()['data']['text']) > 20:
    return get_words_2()  
  return words.json()['data']['text']
 

#def get_random_color():
  #return "#%06x" % random.randint(0, 0xFFFFFF)
#, "color":get_random_color()

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"nowDay":{"value":get_days()},"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"lastMeet_days":{"value":get_count_2()},"birthday_left":{"value":get_birthday()},"birthday_left_2":{"value":get_birthday_2()},"words":{"value":get_words()},"words_2":{"value":get_words_2()}}
res = wm.send_template(user_id, template_id, data)
print(res)
