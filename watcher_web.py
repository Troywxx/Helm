#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re

from bs4 import BeautifulSoup

p1 = re.compile(r'[[](.*?)[]]', re.S)  #最小匹配

url = "http://172.17.1.166"
rad = "/biz/Radar621/Radar.aspx?cccc=ZJHK"
awos = "/biz/AWOS/awos_all.aspx?cccc=ZJHK"
# awos_net = "/biz/AWOS/96awos.aspx?cccc=ZJHK" 全国自观联网
def webfile(url, prdtype):

    url += prdtype
    cookies = {
        'LoginCookiesGuid': '5274c2de-632d-4611-ac89-8fc3e173',
        'LoginCookiesName': 'ZJHK'
    }
    response = requests.get(url, cookies=cookies, timeout=30)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    return soup
# print soup.find(id="ListBox_Time").option.string #2018-07-18 08:17(UTC)
# print soup.find(id="Repeater_RWYNO_ctl00_Label_RWYName").string #跑道01[2018-07-18 08:36(UTC)]

    # f = open('166.txt', 'w')
    # f.write(soup.encode('utf-8'))

if __name__ == "__main__":
    print webfile(url, rad).find(id="ListBox_Time").option.string
    print re.findall(p1, webfile(url, awos).find(id="Repeater_RWYNO_ctl00_Label_RWYName").string)[0]
