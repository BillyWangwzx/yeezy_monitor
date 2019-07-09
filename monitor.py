import requests
import pygame
import time
from bs4 import BeautifulSoup


url = "https://yeezysupply.com"

#加载音乐
reminder = "reminder.mp3"
pygame.mixer.init()
track = pygame.mixer.music.load(reminder)

#模拟一个浏览器
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36",
          "Accept-Language": "en-US",
          "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
         "Accept-Encoding":"gzip, deflate, br"
          }
session = requests.session()
session.headers = headers
#最大时间
timeout = 10

while True:
    if int(time.time()) % 5 == 0:
        try:
            r = session.get(url, allow_redirects=True, timeout=timeout)
        except requests.exceptions.Timeout:
            #如果长时间没有加载出来，则是发售且网络很不稳定
            pygame.mixer.music.play(-1)
            time.sleep(60)
            break
        if "password" in r.url:
            #上了密码页，很可能临近发售
            pygame.mixer.music.play(-1)
            print("password page up")
            time.sleep(10)
        else:
            soup = BeautifulSoup(r.text, features="html.parser")
            if soup.find("form", attrs={"action": "/cart/add"}):
                #发售了！
                pygame.mixer.music.play(-1)
                time.sleep(60)
                break
    time.sleep(0.1)
