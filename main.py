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
    cde_ins = [] # 表示是否在cde中找到数据,有数据的话写进下载文件名
    for i in range(17754, data.shape[0]):  # 行数
        drug_info = data.iloc[i]
        try:
            g = GetIns(drug_info)
            links = g.get_links_cde()
        except:
            break
        print(i)
        if links:  # 不为空
            cde_ins.append(True)
        else:
            cde_ins.append(False)






