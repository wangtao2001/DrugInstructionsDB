import bs4
import requests
import pandas as pd
import re


class GetData:
    def __init__(self, id_number):
        root_url = "http://data.baidu1y.com/data/yytextdetail.aspx"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.id = str(id_number)
        params = {'id': self.id}
        r = requests.get(root_url, headers=headers, params=params, timeout=15)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        self.drug_name = soup.find('div', attrs={'class': 'zhanhtit2'}).string.strip()
        self.div_list = soup.find_all('div', attrs={'class': 'padd6'})

    def get_BasicInfo(self): # 基本信息
        """id approvalNum drugsType prescriptions validityPeriod"""
        basic_info = [self.id]
        try:
            approvalNum = self.div_list[5].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            approvalNum = 'NULL'
        finally:
            basic_info.append(approvalNum)
        try:
            drugsType = self.div_list[3].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            drugsType = 'NULL'
        finally:
            basic_info.append(drugsType)
        try:
            prescriptions = self.div_list[6].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            prescriptions = 'NULL'
        finally:
            basic_info.append(prescriptions)
        try:
            validityPeriod = self.div_list[23].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            validityPeriod = 'NULL'
        finally:
            basic_info.append(validityPeriod)

        return basic_info

    def get_DrugName(self):  # 药物名称
        drug_name = [self.id]
        try:
            productName = self.div_list[1].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            productName = 'NULL'
        finally:
            drug_name.append(productName)
        try:
            commonName = self.div_list[0].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            commonName = 'NULL'
        finally:
            drug_name.append(commonName)
        try:
            pinyinName = self.div_list[2].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            pinyinName = 'NULL'
        finally:
            drug_name.append(pinyinName)

        return drug_name

    def get_Character(self):  # 性状
        character = [self.id]
        try:
            item = self.div_list[8].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            item = 'NULL'
        finally:
            character.append(item)

        return character

    def get_Dosage(self):  # 用法用量
        """多列表嵌套 分不同用法和用量"""
        dosage = []
        try:
            item = str(self.div_list[13].find('div', attrs={'class': 'zh2'})).lstrip('<div class="zh2">').rstrip('</div>')
        except TypeError:
            item = 'NULL'
        finally:
            dosage.append(item)

        return [[self.id, item] for item in re.split('<br/>|\n', dosage[0])]

    def get_AdverseReaction(self):  # 不良反应
        """多列表嵌套"""
        adverse_reaction = []
        try:
            item = str(self.div_list[12].find('div', attrs={'class': 'zh4'})).lstrip('<div class="zh4">').rstrip('</div>')
        except TypeError:
            item = 'NULL'
        finally:
            adverse_reaction.append(item)

        return [[self.id, item] for item in re.split('<br/>|\n', adverse_reaction[0])]

    def get_DrugInteraction(self):  # 药物相互作用
        """多列表嵌套"""
        drug_interaction = []
        try:
            item = str(self.div_list[19].find('div', attrs={'class': 'zh4'})).lstrip('<div class="zh4">').rstrip('</div>')
        except TypeError:
            item = 'NULL'
        finally:
            drug_interaction.append(item)

        return [[self.id, item] for item in re.split('<br/>|\n', drug_interaction[0])]

    def get_Indication(self):  # 适应症
        """多列表嵌套"""
        indication = []
        try:
            item = str(self.div_list[10].find('div', attrs={'class': 'zh4'})).lstrip('<div class="zh4">').rstrip('</div>')
        except TypeError:
            item = 'NULL'
        finally:
            indication.append(item)

        return [[self.id, item] for item in re.split('<br/>|\n', indication[0])]

    def get_MainCompounds(self):  # 主要成分
        main_compounds = [self.id]
        try:
            item = self.div_list[9].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            item = 'NULL'
        finally:
            main_compounds.append(item)

        return main_compounds

    def get_PharmacologyToxicology(self):  # 主要成分
        pharmacology_toxicology = [self.id]
        try:
            item = self.div_list[20].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            item = 'NULL'
        finally:
            pharmacology_toxicology.append(item)

        return pharmacology_toxicology

    def get_Precautions(self):  # 注意事项
        """多列表嵌套"""
        precautions = []
        try:
            item = str(self.div_list[15].find('div', attrs={'class': 'zh4'})).lstrip('<div class="zh4">').rstrip(
                '</div>')
        except TypeError:
            item = 'NULL'
        finally:
            precautions.append(item)

        return [[self.id, item] for item in re.split('<br/>|\n', precautions[0])]

    def get_Storage(self):  # 贮藏
        storage = [self.id]
        try:
            item = self.div_list[22].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            item = 'NULL'
        finally:
            storage.append(item)

        return storage


if __name__ == "__main__":
    g = GetData(2020618155041112)
    print(g.get_Storage())