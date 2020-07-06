import re
import xlsxwriter
import codecs
from ctypes import c_char_p


# 读取文献
def readtxt(path):
    data = []
    with open(path, 'r', encoding='utf8') as f:
        line = f.readlines()
        for i in line:
            i = i.replace('\n','').replace('\u3000','')
            data.append(i)
        #print(data)
    return data


# 统计词性频次
def cixing(data):
    dic = {}
    for line in data:
        pattern = re.findall(r'/[A-Za-z0-9]{1,30}', line)  # 匹配出'/'之后的1至6个大写英文单词
        #print(pattern)
        for p in pattern:
            #print(p)
            if p in dic:
                dic[p] += 1
            else:
                dic[p] = 1
    print(dic)
    print(len(dic))
    return dic


def write_excel(path,dic):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet('sheet2')
    worksheet.write(0, 0, '词性')
    worksheet.write(0, 1, '频次')
    for k, i in zip(range(len(dic)), dic.keys()):
        j = dic[i]
        #print(i, j)
        worksheet.write(k+1, 0, i)
        worksheet.write(k+1, 1, j)
    workbook.close()


# 去除词性标注 保留空格
def restore(dic,data):
    raw_data=[]
    dic2 = sorted(dic, key=lambda i: len(i), reverse=True)  # 按长度大小排序
    print(dic2)
    for line in data:
        #print(line)
        for i in dic2:
            line = line.replace(i,'')  # 防止部分词性前缀相似导致的错误匹配
        raw_data.append(line)
    print(raw_data)
    return raw_data


def writetxt(path,data):
    with open(path,'w',encoding='utf8') as f:
        for i in data:
            f.write(i+'\n')


if __name__ == '__main__':
    data= readtxt('./test.txt')
    dic = cixing(data)
    #write_excel('./原词性频次表.xlsx',dic)
    final=restore(dic,data)
    writetxt('./test原始.txt',final)