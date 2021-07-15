# !/usr/bin/env python3
# -*-coding: utf-8-*-
# @author:  wangtao
# @data: 21/07/15, Thurs

import requests
from bs4 import BeautifulSoup
import re


class GetData(object):
    def __init__(self, approval_number: str):
        self.approval_number = approval_number
        self.root_url = 'https://db.yaozh.com/'

    def get_data(self):
        url = self.root_url + 'pijian/'
        params = {'pizhunwenhao': self.approval_number}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                   'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                   'Connection': 'keep-alive'}
        r1 = requests.get(url, headers=headers, timeout=15, params=params)
        r1.encoding = r1.apparent_encoding

        soup1 = BeautifulSoup(r1.text, 'html.parser')
        tbody = soup1.find('table', attrs={'class': 'table table-striped zjlsearFromVal'}).find('tbody') # 表格
        links = list()
        for tr in tbody.find_all('tr'):  # 查询结果行
            td_list = tr.find_all('td')
            if td_list[3].string == self.approval_number:
                links.append(self.root_url[:-1] + td_list[0].find('a').get('href'))
        link = links[0]  # 只需要第一条查询结果

        r2 = requests.get(link, headers=headers, timeout=15, params=params)
        r2.encoding = r2.apparent_encoding

        ins_link = '#'
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        for a in soup2.find_all('a'):
            if re.match('说明书\([0-9]*\)',a.get_text()):
                ins_link = self.root_url+ a.get('href')
                break  # 只会有一条匹配结果

        r3 = requests.get(ins_link, headers=headers, timeout=15, params=params)
        r3.encoding = r3.apparent_encoding

        soup3 = BeautifulSoup(r3.text, 'html.parser')
        tbody = soup3.find('table', attrs={'class': 'table table-striped zjlsearFromVal'}).find('tbody')  # 表格
        links = list()
        for tr in tbody.find_all('tr'):  # 查询结果行
            td_list = tr.find_all('td')
            links.append(td_list[4].find('a').get('href'))  # 查询结果细节待处理...
        print(links)


if __name__ == "__main__":
    GetData('国药准字Z20063009').get_data()
