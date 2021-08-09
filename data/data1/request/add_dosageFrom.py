# !/usr/bin/env python3
# -*-coding: utf-8-*-
# @author:  wangtao
# @data: 21/08/06, Fri

import re
import pandas as pd
import numpy as np

# table = pd.read_excel('../table/BasicInfo.xlsx', engine='openpyxl', header=0)
# data = pd.read_excel('../../../resources/国家药品编码本位码信息（国产药品）.xlsx', engine='openpyxl', header=2)
#
# dosageFrom_list = []
#
# for line_index in range(table.shape[0]):
#     print(line_index)
#     line = table.iloc[line_index]
#     approvalNum = line[1]
#     if re.match('^国药准字[A-Z][0-9]{8}\s*', approvalNum): # 单个国药准字精准匹配
#         pass
#     else:
#         approvalNum = re.search('^国药准字[A-Z][0-9]{8}\s*', approvalNum)
#     for j in range(data.shape[0]):
#         number = data.iloc[j][1]
#         if number == approvalNum:
#             dosageFrom_list.append(data.iloc[j][3])
#             break
#     else:
#         dosageFrom_list.append(np.NaN)
#
# table['dosageFrom'] = dosageFrom_list
# table.to_excel('new_BasicInfo.xlsx')




