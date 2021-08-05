import bs4
import requests
import pandas as pd
import re
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'}


class GetData:
    def __init__(self, id_number):
        root_url = "http://data.baidu1y.com/data/yytextdetail.aspx"
        self.id = str(id_number)
        params = {'id': self.id}
        r = requests.get(root_url, headers=headers, params=params, timeout=15)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        self.drug_name = soup.find('div', attrs={'class': 'zhanhtit2'}).string.strip()
        print(self.drug_name) # 药物名称
        self.div_list = soup.find_all('div', attrs={'class': 'padd6'})

    def get_BasicInfo(self): # 基本信息
        """approvalNum drugsType prescriptions validityPeriod specification enterprise"""
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
        try:
            specification = self.div_list[11].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            specification = 'NULL'
        finally:
            basic_info.append(specification)
        try:
            enterprise = self.div_list[4].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            enterprise = 'NULL'
        finally:
            basic_info.append(enterprise)

        return basic_info

    def get_DrugName(self):  # 药物名称
        """id productName commonName pinyinName"""
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

    def get_PharmacologyToxicology(self):  # 药理学毒理学
        pharmacology_toxicology = [self.id]
        try:
            item = self.div_list[20].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            item = 'NULL'
        finally:
            pharmacology_toxicology.append(item)

        return pharmacology_toxicology

    def get_Pharmacokinetics(self):  # 药代动力学
        pharmacokinetics = [self.id]
        try:
            item = self.div_list[21].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            item = 'NULL'
        finally:
            pharmacokinetics.append(item)

        return pharmacokinetics

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

    def get_Taboo(self):  # 禁忌
        """多列表嵌套"""
        taboo = []
        try:
            item = str(self.div_list[14].find('div', attrs={'class': 'zh2'})).lstrip('<div class="zh2">').rstrip(
                '</div>')
        except TypeError:
            item = 'NULL'
        finally:
            taboo.append(item)

        return [[self.id, item] for item in re.split('<br/>|\n', taboo[0])]

    def get_Storage(self):  # 贮藏
        storage = [self.id]
        try:
            item = self.div_list[22].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            item = 'NULL'
        finally:
            storage.append(item)

        return storage

    def get_SpecialCrowd(self):  # 特殊人群用药
        "pregnant child elderly"
        special_crowd = [self.id]
        try:
            pregnant = self.div_list[16].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            pregnant = 'NULL'
        finally:
            special_crowd.append(pregnant)
        try:
            child = self.div_list[17].find('div', attrs={'class': 'zh4'}).string
        except TypeError:
            child = 'NULL'
        finally:
            special_crowd.append(child)
        try:
            elderly = self.div_list[18].find('div', attrs={'class': 'zh2'}).string
        except TypeError:
            elderly = 'NULL'
        finally:
            special_crowd.append(elderly)

        return special_crowd


if __name__ == "__main__":
    BasicInfo = open("../BasicInfo.txt", 'a', encoding='utf-8')
    DrugName = open("../DrugName.txt", 'a', encoding='utf-8')
    Character = open("../Character.txt", 'a', encoding='utf-8')
    Dosage = open("../Dosage.txt", 'a', encoding='utf-8')
    AdverseReaction = open("../AdverseReaction.txt", 'a', encoding='utf-8')
    DrugInteraction = open("../DrugInteraction.txt", 'a', encoding='utf-8')
    Indication = open("../Indication.txt", 'a', encoding='utf-8')
    MainCompounds = open("../MainCompounds.txt", 'a', encoding='utf-8')
    PharmacologyToxicology = open("../PharmacologyToxicology.txt", 'a', encoding='utf-8')
    Pharmacokinetics = open("../Pharmacokinetics.txt", 'a', encoding='utf-8')
    Precautions = open("../Precautions.txt", 'a', encoding='utf-8')
    Taboo = open("../Taboo.txt", 'a', encoding='utf-8')
    Storage = open("../Storage.txt", 'a', encoding='utf-8')
    SpecialCrowd = open("../SpecialCrowd.txt", 'a', encoding='utf-8')

    url = 'http://data.baidu1y.com/data/yytext.aspx'
    data = pd.read_excel('../../../resources/国家药品编码本位码信息（国产药品）.xlsx', engine='openpyxl', header=2)
    # 国产药品和进口药品分别查询
    for i in range(0, 3530):
        ApproveCode = data.iloc[i]['注册证号']
        try:
            r = requests.get(url, headers=headers, params={'ApproveCode': ApproveCode}, timeout=15)
            try:
                number = bs4.BeautifulSoup(r.text, 'html.parser').find_all('div', attrs={'class': 'yyaodata29'})[1].find('a').get('href').split('?')[1][3:]
            except IndexError:
                continue
            if number != '':
                g = GetData(number)
                # 在不同的表中写入一系列数据
                BasicInfo.write(str(g.get_BasicInfo()) + '\n')
                DrugName.write(str(g.get_DrugName()) + '\n')
                Character.write((str(g.get_Character())) + '\n')
                Dosage.write(str(g.get_Dosage()) + '\n')
                AdverseReaction.write(str(g.get_AdverseReaction()) + '\n')
                DrugInteraction.write(str(g.get_DrugInteraction()) + '\n')
                Indication.write(str(g.get_Indication()) + '\n')
                MainCompounds.write(str(g.get_MainCompounds()) + '\n')
                PharmacologyToxicology.write(str(g.get_PharmacologyToxicology()) + '\n')
                Pharmacokinetics.write(str(g.get_Pharmacokinetics()) + '\n')
                Precautions.write(str(g.get_Precautions()) + '\n')
                Taboo.write(str(g.get_Taboo()) + '\n')
                Storage.write(str(g.get_Storage()) + '\n')
                SpecialCrowd.write(str(g.get_SpecialCrowd()) + '\n')
        except:  # 断连错误
            print('正在重新启动')
            time.sleep(30)







