# !/usr/bin/env python3
# -*-coding: utf-8-*-
# @author:  wangtao
# @data: 21/07/28, Wed

import re

import numpy as np
import pandas as pd
import string


def update_id(data):
    data = data.drop(['ID'], axis=1)
    cols = list(data)
    cols.insert(0, cols.pop(cols.index('new_ID')))
    data = data.loc[:, cols]
    return data


def get_compounds():
    separator = '﹑|、|，|;|；'  # 英文逗号留给了化学式
    data = pd.read_excel('./basic/MainCompounds.xlsx', engine='openpyxl')
    data = update_id(data)
    mainCompoundsList = []  # 主成分
    accessoriesList = []  # 辅料
    for i in range(data.shape[0]):
        compounds = str(data.iloc[i][1]).strip('。')
        part = compounds.split('。')  # 两个部分，第一个部分是主要成分，第二个部分是辅料
        _mainCompounds = part[0]

        # 主成分解析部分
        mainCompounds = '#'.join([re.sub('(本品)?(主要)?成分为?是?：?','',item) for item in re.split(separator, _mainCompounds)])  # 英文逗号留给化学成分

        accessories = 'NULL'
        if len(part) == 2:
            _accessories = part[1]
            # 辅料解析部分
            accessories = '#'.join([re.sub('辅料为?是?：?', '', item) for item in re.split(separator, _accessories)])

        mainCompoundsList.append(mainCompounds)
        accessoriesList.append(accessories)
    data = data.drop(['compounds'], axis=1)
    data['mainCompounds'] = mainCompoundsList
    data['accessories'] = accessoriesList
    data.to_excel('./new/Compounds.xlsx', na_rep='NULL', index=False)


def get_adverseReaction():
    data = pd.read_excel('./basic/AdverseReaction.xlsx', engine='openpyxl')
    data = update_id(data)
    for i in range(data.shape[0]):
        this = data.iloc[i][1]
        if this is np.NaN:
            data.iloc[i][1] = "NULL"
            continue
        data.iloc[i][1] = str(this).strip().lstrip(string.digits).lstrip(".")
    data.to_excel('./new/AdverseReaction.xlsx', na_rep='NULL', index=False)


def get_character():
    separator = '﹑|、|，|;|；|,|\.|。'
    data = pd.read_excel('./basic/Character.xlsx', engine='openpyxl')
    data = update_id(data)
    appearanceList = []
    odorList = []
    tasteList = []
    for i in range(data.shape[0]):
        if data.iloc[i][1] is np.NaN:
            appearanceList.append('NULL')
            odorList.append('NULL')
            tasteList.append('NULL')
        else:
            info = [i for i in re.split(separator, str(data.iloc[i][1])) if i != '']
            f_index = 100 # 最大值
            taste_tp = []
            app_tp = []
            odor = 'NULL'
            for index,item in enumerate(info):
                if re.match('气.+',item) or item=='无臭':
                    odor = item.lstrip('气')
                elif '味' in item:
                    f_index = index
                    taste_tp.append(item.lstrip('味'))
                elif index > f_index:
                    taste_tp.append(item)
                else:
                    item = item.lstrip('本品').lstrip('为')
                    app_tp.append(item)
            if len(taste_tp) == 0:
                tasteList.append('NULL')
            else:
                tasteList.append("#".join(taste_tp))
            odorList.append(odor)
            appearanceList.append('，'.join(app_tp))
    data['appearance'] = appearanceList
    data['odor'] = odorList
    data['taste'] = tasteList
    data = data.drop(['Character'],axis=1)
    data.to_excel('./new/Character.xlsx', na_rep='NULL', index=False)


if __name__ == "__main__":
    get_character()
