# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 13:40
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : main.py
# @Software: PyCharm
from nonebot import logger
import httpx
from bs4 import BeautifulSoup
import re



def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe bKit/537.36 (KHTML, like Gecko) Chrome/93.0.4544.0 Safari/537.36 Edg/93.0.933.1",
    }#头部信息用户代理（不用也可以，出于尊重）
    url="http://sxwjw.shaanxi.gov.cn/sy/wjyw/"
    try:
        html=httpx.get(url).text
        soup=BeautifulSoup(html,'lxml')
        data=soup.find_all('ul',class_='cm-news-list gl-news-list')[0]
        find_title=re.compile('title="(.*?)"')
        find_link=re.compile('href=".(.*?)"')
        titles=re.findall(find_title,str(data))
        links=re.findall(find_link,str(data))
        for i in range(len(links)):
            links[i]="http://sxwjw.shaanxi.gov.cn/sy/wjyw"+links[i]
        return titles,links
    except Exception as err:
        # print('卫健委爬虫出现错误：',err)
        logger.debug('卫健委爬虫出现错误：',err)

if __name__ == '__main__':
    print(main())