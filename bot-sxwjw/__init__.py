# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 13:38
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py.py
# @Software: PyCharm
import logging

import nonebot
from nonebot import on_command,logger
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event,MessageEvent,MessageSegment
from . import wjw
from . import html2png
import os.path
from os.path import dirname
from nonebot import require
import datetime
scheduler = require("nonebot_plugin_apscheduler").scheduler
groups=nonebot.get_driver().config.wjw


path=dirname(__file__)+'/cache'
cache=path+'/cache.txt'

news = on_command("陕西卫健委",aliases={"卫健委","陕西卫健委","wjw"}, priority=2)
@news.handle()
async def news_(bot: Bot, event: MessageEvent, state: dict):
    titles,links=wjw.main()
    if os.path.exists(path)==False:
        os.mkdir(path)
    with open(cache , "w",encoding="utf-8") as ca:
        ca.write(str(titles))
    msg=str(event.get_message()).split()

    if not msg:
        message = ''
        i=0
        for title in titles:
            i+=1
            message = message+str(i)+'、'+title+'\n'
        await news.send(message)
    elif 0<int(msg[0])<=len(titles):
        num=int(msg[0])-1
        await html2png.save_image(links[num],titles[num])
        fname=str(datetime.datetime.now()).replace(" ","-")
        await news.send(message=links[num])
        await news.send(MessageSegment.image("file:///"+dirname(__file__)+fname+".png"))
        logger.info(titles[num])

async def wjwtime():
    titles,links = wjw.main()
    cachetxt=open(cache , "r",encoding="utf-8").read()
    count=0
    for title in titles:
        if title not in cachetxt and '确诊病例' in title:
            for g in groups:
                fname=str(datetime.datetime.now()).replace(" ","-")
                await html2png.save_image(links[count], fname)
                await nonebot.get_bot().send_group_msg(group_id=g, message="卫健委最新确诊要闻：")
                await nonebot.get_bot().send_group_msg(group_id=g, message=links[count])
                await nonebot.get_bot().send_group_msg(group_id=g, message=MessageSegment.image("file:///"+dirname(__file__)+fname+".png"))
                with open(cache, "w", encoding="utf-8") as txt:
                            txt.write(str(titles))
                            txt.close()
        elif title not in cachetxt and '确诊病例' not in title:
            with open(cache, "w", encoding="utf-8") as txt:
                txt.write(str(titles))
                txt.close()
        count+=1

scheduler.add_job(wjwtime, "cron",minute="0/10", id="wjwtime")
__usage__ = """
直接发送：
    陕西卫健委
    wjw
    卫健委
获取某一条:
    陕西卫健委 1
    wjw 1
    卫健委 1
"""

__help_plugin_name__ ="陕西卫健委"
__permission__ = 2
__help__version__ = '0.1'