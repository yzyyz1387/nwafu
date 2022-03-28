# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 15:05
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : html2png.py
# @Software: PyCharm
from os.path import dirname
import os
from pyppeteer import launch


async def save_image(url, title):
    if not os.path.exists(dirname(__file__) + "/imgs"):
        os.mkdir(dirname(__file__) + "/imgs")
    img_path = dirname(__file__) + '/imgs/%s.png' % title
    browser = await launch(options={"args": ['--no-sandbox', "--start-maximized", '--user-agent=Mozilla/5.0 (Linux; '
                                                                                  'Android 9; SKW-A0 '
                                                                                  'Build/SKYW2001110CN00MP7; wv) '
                                                                                  'AppleWebKit/537.36 (KHTML, '
                                                                                  'like Gecko) Version/4.0 '
                                                                                  'Chrome/76.0.3809.89 Mobile '
                                                                                  'Safari/537.36 T7/11.19 '
                                                                                  'SP-engine/2.15.0 '
                                                                                  'baiduboxapp/11.19.5.10 (Baidu; P1 '
                                                                                  '9)']})
    page = await browser.newPage()
    # 加载指定的网页url
    await page.goto(url)
    # 设置网页显示尺寸
    await page.setViewport({'width': 800, 'height': 1200})
    '''
    path: 图片存放位置
    clip: 位置与图片尺寸信息
        x: 网页截图的x坐标
        y: 网页截图的y坐标
        width: 图片宽度
        height: 图片高度
    '''
    await page.screenshot({'path': img_path, 'clip': {'x': 0, 'y': 0, 'width': 800, 'height': 1200}})
    await browser.close()
    return img_path
    # save_image(url, img_path)


if __name__ == '__main__':
    import os
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(save_image('http://sxwjw.shaanxi.gov.cn/sy/wjyw/202112/t20211223_2205338.html', 'test'))
