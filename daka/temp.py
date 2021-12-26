# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/8/15 0:23
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : temp.py
# @Software: PyCharm
# python3
import urllib.request
import urllib.parse
import http.cookiejar
import time


# 日期
date = time.strftime('%Y%m%d')
LOGIN_URL = r'https://app.nwafu.edu.cn/uc/wap/login/check'  # 登录教务系统的URL,目的是获取cookie
get_url = 'https://app.nwafu.edu.cn/ncov/wap/open-report/save'  # 体温填报地址
# 请求头
headers = {'authority': 'app.nwafu.edu.cn', 'pragma': 'no-cache', 'cache-control': 'no-cache',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
           'sec-fetch-dest': 'document',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'navigate',
           'referer': 'https://app.nwafu.edu.cn/site/applicationSquare/index?sid=8',
           'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7', }
############################################################

# post数据
data = {
    'sfzx': '1',
    'tw': '1',
    'area': '\u9655\u897F\u7701 \u54B8\u9633\u5E02 \u6768\u9675\u533A',
    'city': '\u54B8\u9633\u5E02',
    'province': '\u9655\u897F\u7701',
    'address': '\u9655\u897F\u7701\u54B8\u9633\u5E02\u6768\u9675\u533A\u674E\u53F0\u8857\u9053\u897F\u5317\u519C\u6797\u79D1\u6280\u5927\u5B66\u5357\u6821\u533A\u7537\u751F\u516C\u5BD3',
    'geo_api_info': '{"type":"complete","position":{"Q":34.259645724827,"R":108.06678005642402,"lng":108.06678,"lat":34.259646},"location_type":"html5","message":"Get geolocation success.Convert Success.Get address success.","accuracy":40,"isConverted":true,"status":1,"addressComponent":{"citycode":"0910","adcode":"610403","businessAreas":[],"neighborhoodType":"","neighborhood":"","building":"","buildingType":"","street":"\u90B0\u57CE\u8DEF","streetNumber":"183\u53F7","country":"\u4E2D\u56FD","province":"\u9655\u897F\u7701","city":"\u54B8\u9633\u5E02","district":"\u6768\u9675\u533A","township":"\u674E\u53F0\u8857\u9053"},"formattedAddress":"\u9655\u897F\u7701\u54B8\u9633\u5E02\u6768\u9675\u533A\u674E\u53F0\u8857\u9053\u897F\u5317\u519C\u6797\u79D1\u6280\u5927\u5B66\u5357\u6821\u533A\u7537\u751F\u516C\u5BD3","roads":[],"crosses":[],"pois":[],"info":"SUCCESS"}',
    'sfcyglq': '0',
    'sfyzz': '0',
    'qtqk': ''
}


# 登录
values = {
    'username': "2019010088",
    'password': "1796031384yz",
}
postdata = urllib.parse.urlencode(values).encode()

# 设置储存cookies的文件
cookie_filename = '/www/wwwroot/dk/test/tempcookies/' + "2019010088temp" + 'cookie_jar.txt'
cookie_jar = http.cookiejar.MozillaCookieJar(cookie_filename)
handler = urllib.request.HTTPCookieProcessor(cookie_jar)
opener = urllib.request.build_opener(handler)

request = urllib.request.Request(LOGIN_URL, postdata, headers)
try:
    response = opener.open(request)
    # print(response.read().decode())
except urllib.error.URLError as e:
    print(e.code, ':', e.reason)

cookie_jar.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到'学号+cookie.txt'中

data1 = urllib.parse.urlencode(data).encode()
get_request = urllib.request.Request(get_url, headers=headers, data=data1)
get_response = opener.open(get_request)
final = get_response.read().decode()
print(final)


############################################################
