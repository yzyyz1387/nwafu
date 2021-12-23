# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/11/19 20:21
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : login.py
# @Software: PyCharm

import execjs
import re
import requests
import os
from os.path import dirname

req=requests.session()
cookie_path=dirname(__file__)+"/cookies"
def get_des_psswd(data, key):
    """
    调用js
    :param data: 明文密码
    :param key: 密匙
    :return: 密文
    """
    return (context1.call('encryptPassword', data, key))  #调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数

def js_from_file(file_name):
    """
    读取js文件
    :return:
    """
    with open(file_name, 'r', encoding='UTF-8') as file:
        result = file.read()
    return result

context1 = execjs.compile(js_from_file('pwd.js'))

#头部代理
headers = {
     'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://authserver.nwafu.edu.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4741.0 Safari/537.36 Edg/98.0.1100.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://authserver.nwafu.edu.cn/authserver/login?service=https%3A%2F%2Fnewehall.nwafu.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fnewehall.nwafu.edu.cn%2Fywtb-portal%2FLite%2Findex.html%23%2Finformation_center',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

params = ( ('service', 'https://newehall.nwafu.edu.cn:443/login?service=https://newehall.nwafu.edu.cn/ywtb-portal/Lite/index.html#/information_center'),)

def login(username,pwdtext):
    """

    :param username: 学号
    :param pwdtext: 密码
    :return: 登录状态，储存一些cookies
    """
    #如果cookies文件夹不存在则创建该文件夹
    if os.path.exists(cookie_path)==False:
        os.mkdir(cookie_path)
    url="https://authserver.nwafu.edu.cn/authserver/login?service=https%3A%2F%2Fnewehall.nwafu.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fnewehall.nwafu.edu.cn%2Fywtb-portal%2FLite%2Findex.html%23%2Finformation_center"
    #打开网页获取源码并保持会话
    html=req.get(url,headers=headers,verify = False).text
    #定位加密信息
    key=re.compile(r"id=.*?value=\"(.*?)\"")
    keys=re.findall(key,html)
    kes=keys[len(keys)-2]
    excs=keys[len(keys)-1]
    #调用js文件获取密文
    passw=get_des_psswd(pwdtext, kes)
    #拼接data
    data = {
      'username': username,
      'password': passw,
      'captcha': '',
      'rememberMe': 'true',
      '_eventId': 'submit',
      'cllt': 'userNameLogin',
      'lt': '',
    'execution':excs,
    }
    #尝试登录
    try:
        response_ = req.post('http://authserver.nwafu.edu.cn/authserver/login', headers=headers, params=params, data=data)
        response=response_.text
        if "登录" not in response and "冻结" not in response:
            print("登陆成功")
            print("获取cookies")
            print(str(response_.request.headers['Cookie']))
            try:
                test=req.get("https://authserver.nwafu.edu.cn/authserver/login",headers=headers)
                coo=test.cookies.get_dict()['REFERERCE_TOKEN']
                print(coo)
                with open(cookie_path+"/%scookie.txt"%username,"w") as cook:
                    cook.write(str(coo))
                    cook.write("\n")
                    cook.write(str(response_.request.headers['Cookie'].replace('MOD_AUTH_CAS=','')))
                    cook.write("\n")
                    cook.close()
                    print("%sCookies获取成功"%username)
            except Exception as err:
                print("发生错误：",err)
        elif "冻结" in response:
            print(username)
            print("登录失败账号被冻结")
            return "登录失败账号被冻结"
        else:
            print(username)
            print("登陆失败，账号或密码错误")
            return "登陆失败，账号或密码错误"
    except Exception as err:
        print("发生错误：", err)

if __name__ == '__main__':
    user=input("username:")
    pwd = input("pass:")
    login(user,pwd)
