import docx
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed  # Error


def pdfParse(file, save_path):
    parser = PDFParser(file)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize()
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmagr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmagr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmagr, device)
        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                try:
                    if isinstance(x, LTTextBoxHorizontal):
                        with open(f'{save_path}', 'a', encoding='utf-8') as f:
                            result = x.get_text()
                            # print(result)
                            f.write(result + "\n")
                except:
                    print("Failed")


def htmlParser(html, save_path):
    pass


def docParse(file_name, save_path):
    f = open(f'{save_path}', 'a', encoding='utf-8')
    doc = docx.Document(f'instructions/{file_name}')
    # 两种组织形式 段落和表格，无法同时读取
    for para in doc.paragraphs:  # 读取基本文字
        f.write(para.text + '\n')
    tables = doc.tables  # 获取文件中的表格集
    for table in tables[:]:
        result = []
        for i, row in enumerate(table.rows[:]):  # 读每行
            row_content = []
            for cell in row.cells[:]:  # 读一行中的所有单元格
                c = cell.text
                row_content.append(c)
            result.append(row_content)  # 将每一行组织起来
        # result 写入表格 还原顺序在解析中尝试
        f.write(str(result) + '\n')
    f.close()


class Parser:  # 解析当前目录下已经转换为txt的说明书
    def __init__(self):
        f = open('demo.txt', 'r', encoding='utf-8')
        data = f.readlines()


if __name__ == '__main__':
    docParse('gyzzH20203307sms.doc', 'demo.txt')