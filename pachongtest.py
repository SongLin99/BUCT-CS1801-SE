# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup,Comment
import re
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
import pymysql

import datetime
##爬虫最好带上代理IP

urls = []
imgs = []
num = 1
while True:
    try:
        hd = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6)',
              'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
        kv = {
            'qtext': '故宫博物馆',
            'sort': 'date',
            'type': 'web',
            'datepid': str(1),
            'channel': '新闻',
            'page': str(num),
        }
        r = requests.get('https://search.cctv.com/search.php', headers=hd, params=kv)
        # print(r.text)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'html.parser')
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        result = re.compile(r'(.)*全部网页结果共')
        aaa = soup.find(text=result)
        aa = str(aaa)
        print(aa)
        xxx = result.match(aa).span()
        tot = int(aa[xxx[1]:len(aa) - 1:])
        tot = (tot + 9) // 10

        pre = re.compile(r'link_p.php[?]targetpage=http://news(.)*html&')
        for xa in soup.find_all(name='div', class_='tright'):
            link = xa.find('a')
            x = link.get('href')

            if pre.match(x):
                xx = pre.match(x).span()
                urls.append(x[22:xx[1] - 1:])
            else:
                continue
            imgg = xa.find('img')
            imgx = imgg.get('src')
            if imgx:
                imgs.append(imgx)
            else:
                imgs.append('https://p1.img.cctvpic.com/photoAlbum/templet/common/DEPA1546583592748817/logo31.png')
        num += 1
        if num > tot:
            break
    except:
        # print('fuck')
        print(urls, imgs)
print(urls, imgs)
print(r.url)