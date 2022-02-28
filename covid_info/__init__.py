# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/28 18:07
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py
# @Software: PyCharm
from covid_info.get_info import *
from covid_info.other_ import *

# 腾讯借口（国内） get_info.py
# 凤凰网页（国外) other_.py
if __name__ == '__main__':
    import asyncio
    place = input('请输入地点：')
    loop = asyncio.get_event_loop()
    result_ = loop.run_until_complete(get_info(place))
    if result_:
        print(result_)
    else:
        result_ = loop.run_until_complete(get_other_data(place))
        print(result_)
