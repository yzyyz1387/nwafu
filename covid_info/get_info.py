# python3
# -*- coding: utf-8 -*-
# @Time    : 2022/2/28 18:13
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : get_info.py
# @Software: PyCharm
import httpx
import json
from typing import Optional


async def get_info(place):
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    try:
        sum_info_json = httpx.get(url).json()
    except Exception as e:
        print(f'疫情查询发生错误 {type(e)}：{e}')
        return None
    data = sum_info_json['data']
    data = json.loads(data)
    update = data['lastUpdateTime']
    China = ['中国', '全国', '中华人民共和国']
    if place in China:
        rely = analyze(data['areaTree'][0], "中国", update)
        return rely
    else:
        children_ = data["areaTree"][0]['children']
        for children in children_:
            if place in children["name"]:
                # print(children)
                rely = analyze(children, place, update)
                # print(rely)
                return rely
            else:
                city_ = children['children']
                for city in city_:
                    if place in city["name"]:
                        # print(city)
                        rely = analyze(city, place, update)
                        # print(rely)
                        return rely


def analyze(children: dict, place: str, update: str) -> Optional[str]:
    """
    :param children: 所查询地区疫情信息字典
    :param place: 地区
    :param update: 更新时间
    :return: 格式化字符串
    """
    t_confirm = children['today']['confirm']
    total = children['total']
    nowConfirm = total['nowConfirm']
    confirm = total['confirm']
    # suspect=total['suspect']
    dead = total['dead']
    heal = total['heal']
    # deadRate=total['deadRate']
    # healRate=total['healRate']
    return (
        f"{place} 疫情数据：\n"
        f" ——————————————\n"
        f"    现有确诊：{nowConfirm}(+{t_confirm})\n"
        f"    累计确诊：{confirm}\n"
        # f"    疑似病例：{suspect}\n"
        f"    死亡人数：{dead}\n"
        f"    累计治愈：{heal}\n"
        # f"    治愈率：{healRate}%\n"
        # f"    死亡率{deadRate}%\n"
        f"——————————————\n"
        f"更新时间：{update}"
    )



