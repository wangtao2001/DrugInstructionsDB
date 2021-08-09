# !/usr/bin/env python3
# -*-coding: utf-8-*-
# @author:  wangtao
# @data: 21/07/03, Tues

import pandas as pd
import multiprocessing
import xlsxwriter

# 单列表
def one_list(name):
    f = open(f"../{name}.txt", 'r', encoding='utf-8')
    data = pd.DataFrame(columns=['id', name])
    lines = f.readlines()
    for i in range(len(lines)):
        data.loc[i] = eval(lines[i])
    data.to_excel(f"../{name}.xlsx")


# 多列表嵌套
def more_list(name):
    f = open(f"../{name}.txt", 'r', encoding='utf-8')
    data = pd.DataFrame(columns=['id', name])
    lines = f.readlines()
    n = 0
    for line in lines:
        for item in eval(line):
            data.loc[n] = item
            n += 1
            print(n)
    data.to_excel(f"../{name}.xlsx", engine='xlsxwriter')


class toExcel(multiprocessing.Process):
    def __init__(self, name, one=False):
        multiprocessing.Process.__init__(self)
        self.name = name
        self.one = one

    def run(self):
        if self.one:
            one_list(self.name)
        else:
            more_list(self.name)


if __name__ == '__main__':
    li = ["Precautions"]

    p_pool = []
    for filename in li:
        p = toExcel(filename)
        p_pool.append(p)

    for p in p_pool:
        p.start()

    for p in p_pool:
        p.join()
