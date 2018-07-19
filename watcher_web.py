#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import re

from bs4 import BeautifulSoup
from config import config

# url = "http://172.17.1.166"
# rad = "/biz/Radar621/Radar.aspx?cccc=ZJHK"
# awos = "/biz/AWOS/awos_all.aspx?cccc=ZJHK"
# awos_net = "/biz/AWOS/96awos.aspx?cccc=ZJHK" 全国自观联网
def product166(product166):

    url = product166['url_166']
    prd_type = product166['prd_type']
    cookies = config['cookie166']
    
    pattern = re.compile(r'[[](.*?)[]]', re.S)  #最小匹配

    response = requests.get(url, cookies=cookies, timeout=30)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")

    if prd_type == 'radar_166':
        result = soup.find(id="ListBox_Time").option.string #2018-07-18 08:17(UTC)
    elif prd_type == 'awos_166':
        result = re.findall(pattern, soup.find(id="Repeater_RWYNO_ctl00_Label_RWYName").string)[0] #2018-07-18 08:36(UTC)

    return result

if __name__ == "__main__":
    product166(config['products']['radar_166'])
