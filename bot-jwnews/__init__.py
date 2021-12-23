# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/19 19:58
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py
# @Software: PyCharm
import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event,Message
from . import main
import os.path
from os.path import dirname
from nonebot import require
scheduler = require("nonebot_plugin_apscheduler").scheduler
groups=nonebot.get_driver().config.jwnews


news = on_command("教务", priority=2)
@news.handle()
async def news_(bot: Bot, event: Event, state: dict):

    if event.get_user_id != event.self_id:
        text_path = dirname(__file__) + "/cache/cache.txt"
        cachedir=dirname(__file__)+"/cache"
        if os.path.exists(cachedir)==False:
            os.mkdir(cachedir)
        data_sum=main.main('https://jiaowu.nwsuaf.edu.cn/tzggB/index.htm')[0]
        with open(text_path , "w",encoding="utf-8") as txt:
            txt.write(data_sum)
            txt.close()
        await bot.send(
            event = event,
            message =data_sum,
            at_sender = True
        )
async def jwnewstime():
    ask = main.main('https://jiaowu.nwsuaf.edu.cn/tzggB/index.htm')
    newstext_time = ask[0]
    dic = ask[1]
    text_path = dirname(__file__) + "/cache/cache.txt"
    cache=open(text_path,"r",encoding="utf-8")
    cachetext=cache.read()
    cache.close()
    count=0
    for i in dic:
        count+=1
        if count<6:
            if i not in cachetext:
                print(i, dic[i])
                for g in groups:
                    await nonebot.get_bot().send_group_msg(group_id=g, message="有新通知啦：\n%s\n%s" % (i,dic[i]))
                with open(text_path, "w", encoding="utf-8") as txt:
                    txt.write(newstext_time)
                    txt.close()
            else:
                pass
scheduler.add_job(jwnewstime, "cron",minute="0/1", id="jwnews")
__usage__ = """
直接发送： 教务
"""
__help_plugin_name__ ="教务"
__permission__ = 2
__help__version__ = '0.1'