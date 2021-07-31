# !/usr/bin/env python3
# -*-coding: utf-8-*-
# @author:  wangtao
# @data: 21/07/15, Thurs

import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


class GetIns(object):
    def __init__(self, drug_info: pd.Series):  # 不是全部下载的原因是系统限制只展示前10页
        self.firm = drug_info['生产单位']
        if self.firm is np.NaN:  # 极少数药品没有生产单位标注，使用上市许可证持有人替代(一般不涉及)
            # 2998条数据二者不一致
            self.firm = str(drug_info['上市许可持有人']).replace('（', '(').replace('）', ')')  # 中文括号转换
        self.number = drug_info['批准文号']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }

    def get_links(self):
        root_url = 'https://db.yaozh.com'
        params = {'pizhunwenhao': self.number}

        print(self.number)
        url = root_url + '/pijian'
        r1 = requests.get(url, headers=self.headers, timeout=15, params=params)
        soup1 = BeautifulSoup(r1.text, 'html.parser')
        tbody = soup1.find('table', attrs={'class': 'table table-striped zjlsearFromVal'}).find('tbody') # 表格
        links = list()
        for tr in tbody.find_all('tr'):  # 查询结果行
            td_list = tr.find_all('td')
            if td_list[3].string == self.number:
                links.append(root_url + td_list[0].find('a').get('href'))
        link = links[0]  # 只需要第一条查询结果（精确查询）

        r2 = requests.get(link, headers=self.headers, timeout=15)
        ins_link = '#'
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        for a in soup2.find_all('a'):
            if re.match('说明书\([0-9]*\)', a.get_text()):
                ins_link = root_url + a.get('href')
                break  # 只会有一条匹配结果

        r3 = requests.get(ins_link, headers=self.headers, timeout=15)
        soup3 = BeautifulSoup(r3.text, 'html.parser')
        links = list()
        try:
            tbody = soup3.find('table', attrs={'class': 'table table-striped zjlsearFromVal'}).find('tbody')  # 表格
            for tr in tbody.find_all('tr'):  # 查询结果行
                td_list = tr.find_all('td')
                if td_list[1].get_text() == self.firm:  # 来源匹配
                    links.append(td_list[4].find('a').get('href'))
        except AttributeError:
            pass
        # 不从名称直接查询的原因就是希望将准确结果排前
        # 关于药品说明书的查询并不是精确查询，网页是按照查询条件先匹配，再匹配出满足药品名称的
        # 满足条件的也不一定在第一位
        # 另外还有修订的版本（时间顺序）
        # 部分药品还没有收录说明书
        # 说明书的格式可能为：html jpg pdf
        # 链接包含绝对链接、相对链接
        return links

    def get_links_cde(self):
        """
        从cde上抓取说明书链接并返回
        """
        root_url = 'http://list.cde.org.cn/index/instruction'
        params = {'pzwh': self.number}

        r = requests.get(root_url, params=params, headers=self.headers, timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = list()
        try:
            tbody = soup.find('table', attrs={'class': 'drug-lists'}).find('tbody')  # 表格
            for tr in tbody.find_all('tr'):
                links.append(tr.find('a').get('href'))
        except AttributeError:
            pass
        return links

    def down_ins(self, link):  # 化学药品
        """
        下载说明书文件并返回文件名
        """
        r = requests.get(link, headers=self.headers, timeout=30)
        r.encoding = r.apparent_encoding
        file_name = link.split("/")[-1]  # ins file_name
        f = open(f'../instructions/cde_domestic/{file_name}', 'wb')
        f.write(r.content)
        f.close()
        return file_name



