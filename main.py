# !/usr/bin/env python3
# -*-coding: utf-8-*-
# @author:  wangtao
# @data: 21/07/14, Wed

# 国家药品编码本位码（截至2021年6月30日）
# https://www.nmpa.gov.cn/zwfw/zwfwzxfw/zxfwsjxz/20210705092119131.html

from get_ins import *
from parser import *

if __name__ == '__main__':
    data = pd.read_excel('resources/国家药品编码本位码信息（国产药品）.xlsx', sheet_name=0, engine='openpyxl', header=2)
    # 从cde中请求说明书 解析，并作标识
    cde_ins = [] # 表示是否在cde中找到数据
    for i in range(data.shape[0]):  # 行数
        drug_info = data.iloc[i]
        g = GetIns(drug_info)
        links = g._get_links()
        if links:  # 不为空
            link = 'http:' + links[0]
            cde_ins.append(True)
            file_name = g.down_ins(link)
            # 处理成为txt文档
            docParse(file_name, 'demo.txt')
            # 提取数据的部分
        else:
            cde_ins.append(False)
    data['cde_ins'] = cde_ins

