# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/5 18:32
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : main.py
# @Software: PyCharm



import httpx
from bs4 import BeautifulSoup
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


#访问
def askUrl(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWe bKit/537.36 (KHTML, like Gecko) Chrome/93.0.4544.0 Safari/537.36 Edg/93.0.933.1",
    }#头部信息用户代理
    try:
        html= httpx.get(url).read().decode("utf-8")
        return html
    except Exception as err:
        print('错误：',err)

#解析
def htmlAnalyze(html):
    bsObj = BeautifulSoup(str(html),'lxml')
    divData=bsObj.find_all('div',class_='list-i')
    list=[]
    list.append(divData)
    text=str(list[0]).split('</li>')
    findTitle=re.compile(r'target="_blank">(.*?)</a>')
    findLink= re.compile((r'href="(.*?).htm'))
    infoUrl = 'https://jiaowu.nwsuaf.edu.cn/tzggB/'
    dataList=[]
    dic={}
    for i in range(len(text)-1):
        title=re.findall(findTitle,text[i])[0]
        link=infoUrl+re.findall(findLink,text[i])[0]+'.htm'
        dic[title]=link
        dataList.append(title)

    return (dic,dataList)

def main(url):
    html =  askUrl(url)
    output=[]
    newsText,datalist=htmlAnalyze(html)
    for i in range(5):
        a='【'+str(i+1)+'】'
        inform= a+datalist[i]+' '+newsText[datalist[i]]+'      ==============================    '
        output.append(inform)
    text=str(output)
    mark=["[","]","'",","]
    for marks in mark:
        text=text.replace(marks,'')
    text=str("最新五条通知如下：  "+text)
    return [text,newsText]


newsUrl = 'https://jiaowu.nwsuaf.edu.cn/tzggB/index.htm'
if __name__ == '__main__':
    dic=main(newsUrl)[1]
    print(dic)