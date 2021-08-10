# 中药、中成药主要成分提取
# 准备：统一‘成分’； 主成分与辅料使用。分开；药材间隔使用separator；
# 待解决： 等xx味
import pandas as pd
import re


def get(id_and_compoundsInfo: pd.DataFrame):
    """
    :param id_and_compoundsInfo: 品id和成分+辅料描述的df表
    :return: 两张df表的tuple
    """
    MainCompounds = pd.DataFrame(columns=['id', 'compounds', 'content'])
    Accessories = pd.DataFrame(columns=['id', 'accessories'])

    m_index = 0
    a_index = 0
    separator = '﹑|、|，|,|;|；'  # 不同药材之间的分隔符
    # 主要成分与辅料之间使用中文逗号隔开
    for i in range(100):  # i是行号,每一条药品 #id_and_compoundsInfo.shape[0]
        print(i)
        id = id_and_compoundsInfo.iloc[i][0]
        compoundsInfo = str(id_and_compoundsInfo.iloc[i][1])
        part = compoundsInfo.split('。')  # 第一个部分是主要成分，第二个部分是辅料

        compounds = part[0]
        #主要成分解析
        compounds_list = [re.sub('((本品)?(主要)?成分为?是?：?)|(本品(主要)?为?是?：?)', '', item) for item in re.split(separator, compounds)]  # 药材+剂量?
        for item in compounds_list:
            r = re.search('([0-9]+.)?[0-9]*g', item)
            if r is not None:
                content = r.group()
                compounds = item.replace(content, '')
            else:
                compounds = item
                content = 'NULL'
            # 1: n模型
            compounds = compounds.strip(' .:')
            if compounds == '':
                compounds = 'NULL'
            MainCompounds.loc[m_index] = [id, compounds, content]
            m_index += 1

        # 辅料解析
        if len(part) >= 2:
            accessories = part[1]
            accessories_list = [re.sub('辅料为?是?：?', '', item) for item in re.split(separator, accessories)]
            for item in accessories_list:
                accessories = item.strip()
                # 没有辅料不写进表
                if accessories == '':
                    pass
                else:
                    Accessories.loc[a_index] = [id, accessories]
                    a_index += 1

    return MainCompounds, Accessories


if __name__ == '__main__':
    data = pd.read_excel('./test/test1_MainCompounds.xlsx', engine='openpyxl', dtype=str)
    MainCompounds, Accessories = get(data)
    MainCompounds.to_excel('test/MainCompounds.xlsx')
    Accessories.to_excel('test/Accessories.xlsx')
    


