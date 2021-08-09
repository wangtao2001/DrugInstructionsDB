# 中药、中成药主要成分分割
import pandas as pd
import re


def get(id_and_compoundsInfo: pd.DataFrame):
    """
    :param id_and_compoundsInfo: 包含药品id和成分+辅料描述的df表
    :return: 两张df表的tuple
    """
    MainCompounds = pd.DataFrame(columns=['id', 'compounds', 'content'])
    Accessories = pd.DataFrame(columns=['id', 'accessories'])

    separator = '﹑|、|，|,|;|；|'  # 不同药材之间的分隔符
    # 主要成分与辅料之间使用中文逗号隔开
    for i in range(id_and_compoundsInfo.shape[0]):  # i是行号,每一条药品
        id = id_and_compoundsInfo.iloc[i][0]
        compoundsInfo = id_and_compoundsInfo.iloc[i][1]
        part = compoundsInfo.split('。')  # 第一个部分是主要成分，第二个部分是辅料

        compounds = part[0]
        #主要成分解析
        compounds_list = [re.sub('(本品)?(主要)?成分为?是?：?', '', item) for item in re.split(separator, compounds)]  # 药材+剂量?
        for item in compounds_list:
            r = re.search('[0-9]*.?[0-9]*g', item)
            if r is not None:
                content = r.group()
                compounds = item.replace(content, '').strip()
            else:
                compounds = item
                content = 'NULL'
            # 1: n模型
            MainCompounds.append([id, compounds, content], ignore_index=True)

        # 辅料解析
        if len(part) == 2:
            accessories = part[1]
            accessories_list = [re.sub('辅料为?是?：?', '', item) for item in re.split(separator, accessories)]
            for item in accessories_list:
                accessories = item
                Accessories.append([id, item])

    return MainCompounds, Accessories


if __name__ == '__main__':
    pass

    


