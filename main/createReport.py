from docx import Document
from docx.shared import Inches, Cm
# from docxtpl import DocxTemplate
# import win32com.client
# import inspect, os
# import pythoncom

report_data_path = "./main/static/report/"


# def update_toc(docx_file):
#     pythoncom.CoInitialize()
#     word = win32com.client.DispatchEx("Word.Application")
#     pythoncom.CoInitialize()
#     doc = word.Documents.Open(docx_file)
#     doc.TablesOfContents(1).Update()
#     doc.Close(SaveChanges=True)
#     word.Quit()

def renew_text(p,text):
    p.clear()
    p.add_run()
    p.runs[0].text = text
    p.runs[0].font.name = 'Times New Roman'


def replace_pic(p, pic_list, width=None, height=None):
    p.clear()
    p.add_run()
    for pic in pic_list:
        pic = report_data_path + pic
        if width:
            p.runs[0].add_picture(pic,width=width)
        elif height:
            p.runs[0].add_picture(pic,height=height)


def createReport():
    document = Document(report_data_path+'模板.docx')
    style = document.styles['Normal']
    style.font.name = 'Times New Roman'
    paragraphs = document.paragraphs
    i = 0
    for para in paragraphs:
        print(i)
        print(para.text)
        images = para._element.xpath('.//pic:pic')
        for im in images:
            print(im)
        i += 1
    # week_period = '（4月28日—5月4日）'
    # report_date = '2020年5月4日'
    # title_2_1 = '2.1 全球累计确诊'
    # major_distribution = '主要分布在美国、西班牙、意大利。'
    # pic_title_2_1 = '图2-1 全球累计确诊分布图'
    # title_2_2 = '2.2 全球确诊率：0.046%，病死率：7.0%'
    # title_2_3 = '2.3 全球本周新增确诊：570,433例，死亡：41,253例'
    # title_2_4 = '2.4 本周新增确诊主要来源：美国、俄罗斯'
    # title_2_5 = '2.5 本周新增确诊主要来源：美国、英国'
    # title_2_6 = '2.6 本周新增确诊增长最快：阿富汗，新增死亡增长最快：厄瓜多尔'

    texts = []
    with open(report_data_path+'text.txt',encoding='utf-8') as f:
        for line in f:
            texts.append(line.strip())
    to_replace_text_paragraphs = [
    paragraphs[4],
    paragraphs[6],
    paragraphs[20],
    paragraphs[32],
    paragraphs[33],
    paragraphs[34],
    paragraphs[36],
    paragraphs[38],
    paragraphs[41],
    paragraphs[44],
    paragraphs[45],
    paragraphs[47],
    paragraphs[49],
    paragraphs[50],
    paragraphs[52],
    paragraphs[54],
    paragraphs[56],
    paragraphs[58],
    paragraphs[59],
    paragraphs[61],
    paragraphs[62],
    paragraphs[64],
    paragraphs[65],
    paragraphs[67],
    paragraphs[68],
    paragraphs[70],
    paragraphs[71],
    paragraphs[73],
    paragraphs[74],
    paragraphs[77],
    paragraphs[84],
    paragraphs[85],
    paragraphs[94],
    paragraphs[95]
    ]
    if len(to_replace_text_paragraphs) != len(texts):
        print('error: inconsistent texts')
        print(len(to_replace_text_paragraphs))
        print(len(texts))
    else:
        for i in range(0, len(texts)):
            if i > 0:
                renew_text(to_replace_text_paragraphs[i], texts[i])
    #替换文本，需要使用renew_text的方法，有三个参数分别是文档对应段落以及新的文本
    # renew_text(paragraphs[6],week_period)
    # renew_text(paragraphs[20],report_date)
    # renew_text(paragraphs[33],title_2_1)
    # renew_text(paragraphs[34],major_distribution)
    # renew_text(paragraphs[50],title_2_2)
    # renew_text(paragraphs[59],title_2_3)
    # renew_text(paragraphs[62],title_2_4)
    # renew_text(paragraphs[65],title_2_5)
    # renew_text(paragraphs[68],title_2_6)

    #替换图片，需要使用replace_pic方法，有三个参数分别是文档对应段落、图片地址以及图片宽度

    pic_2_1 = ['2_1.png']
    pic_2_2 = ['2_2.png']
    pic_2_3 = ['2_3_a.png','2_3_b.png']
    pic_2_4 = ['2_4_a.png','2_4_b.png']
    pic_2_5 = ['2_5.png']
    pic_2_6 = ['2_6.png']
    pic_2_7 = ['2_7.png']
    pic_2_8 = ['2_8.png']
    pic_2_9 = ['2_9.png']
    pic_2_10 = ['2_10.png']
    pic_2_11 = ['2_11.png']
    pic_2_12 = ['2_12.png']
    pic_2_13 = ['2_13.png']
    pic_2_14 = ['2_14.png']
    pic_2_15 = ['2_15.png']
    pic_2_16 = ['2_16.png']
    pic_2_17 = ['2_17.png']
    pic_2_18 = ['2_18.png']

    replace_pic(paragraphs[35],pic_2_1, height=Cm(8.6))
    replace_pic(paragraphs[37],pic_2_2, height=Cm(8.6))
    replace_pic(paragraphs[39],pic_2_3, width=Cm(7.3))
    replace_pic(paragraphs[42],pic_2_4, width=Cm(7.3))
    replace_pic(paragraphs[46],pic_2_5, height=Cm(7.8))
    replace_pic(paragraphs[48],pic_2_6, height=Cm(7.8))
    replace_pic(paragraphs[51],pic_2_7, height=Cm(10.6))
    replace_pic(paragraphs[53],pic_2_8, height=Cm(10.6))
    replace_pic(paragraphs[55],pic_2_9, height=Cm(10.6))
    replace_pic(paragraphs[57],pic_2_10, height=Cm(10.6))
    replace_pic(paragraphs[60],pic_2_11, height=Cm(8))
    replace_pic(paragraphs[63],pic_2_12, height=Cm(7.8))
    replace_pic(paragraphs[66],pic_2_13, height=Cm(7.8))
    replace_pic(paragraphs[69],pic_2_14, height=Cm(19.2))
    replace_pic(paragraphs[72],pic_2_15, height=Cm(19.2))
    replace_pic(paragraphs[76],pic_2_16,width=Cm(10.2))
    replace_pic(paragraphs[83],pic_2_17,width=Cm(10.2))
    replace_pic(paragraphs[93],pic_2_18,width=Cm(10.2))

    file_name = report_data_path + 'report.docx'

    # script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    # file_path = os.path.join(script_dir, file_name)

    # print(file_path)
    document.save(file_name)  # 保存文档
    # update_toc(file_path)


if __name__ == "__main__":
    createReport()
