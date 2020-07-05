import xlrd
import datetime
import re


# 读取文献
def readtxt(path):
    data=[]
    with open(path,'r',encoding='utf8') as f:
        line = f.readlines()
        for i in line:
            i = i.strip(' ')
            i = i.replace('\n','').replace('\u3000','').replace('\xa0','').replace(' ','')
            if i!='':
                data.append(i)
    #print(data)
    return data


# 清洗文本
def remove_sentence(data):
    sentences=[]
    for line in data:
        print(line)
        pattern = re.findall(r'/(.*)/', line)
        if len(pattern)>=1:
            line = line.replace('/' + pattern[0] + '/', '')
        sentences.append(line)
    return list(filter(None, sentences))



# 获取底表
def readxls(path):
    word=[]
    rbook = xlrd.open_workbook(path)
    table = rbook.sheets()[0]
    nrows = table.nrows  # 获取行号
    ncols = table.ncols  # 获取列号
    for i in range(1, nrows):  # 第0行为表头
        alldata = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        result = alldata[0]  # 取出表中第一列数据
        word.append(result)
    #print(word)
    return word


# 逆向最大匹配分词
def segword(data):
    wordlis= sorted(wordlexicon, key=lambda i: len(i), reverse=True)  # 按长度大小排序
    #print(wordlis)
    re=[]
    for i in range(len(data)):
        s1 = data[i]
        #print(s1)
        s2 = ''
        maxlen = 5
        w = s1[-maxlen:]  # 逆向
        while (w):
            if len(w) != 1:
                if w in wordlis:
                    s2 = w + ' ' + s2
                    n=len(s1)-len(w)
                    s1 = s1[0:n]
                    w = s1[-maxlen:]
                    #print(s2,s1)
                else:
                    w = w[1:len(w)]
                    #print(w)
            else:
                s2 = w + ' ' + s2
                n = len(s1) - len(w)
                s1 = s1[0:n]
                w = s1[-maxlen:]
                #print(s2, s1)
        re.append(s2)
    print(re)
    return re


# 正向最大匹配分词
def segword_2(data):
    wordlis= sorted(wordlexicon, key=lambda i: len(i), reverse=True)  # 按长度大小排序
    # print(wordlis)
    re=[]
    for i in range(len(data)):
        s1 = data[i]
        #print(s1)
        s2 = ''
        maxlen = 5
        w = s1[:maxlen]  # 逆向
        #print(w)
        while (w):
            if len(w) != 1:
                if w in wordlis:
                    s2 = s2 + w+ ' '
                    s1 = s1[len(w):]
                    w = s1[:maxlen]
                    #print(s2,s1)
                else:
                    w = w[:len(w)-1]
                    #print(w)
            else:
                s2 = s2 + w + ' '
                s1 = s1[len(w):]
                w = s1[:maxlen]
                #print(s2, s1)
        re.append(s2)
    print(re)
    return re


# 去停用词（没有采用该函数）
def remove(data,stopwords):
    corpus=[]
    for line in data:
        l=''
        for word in line.split(' '):
            # print(word)
            if word not in stopwords:
                l=l+word+' '
        corpus.append(l)
    corpus=[i.strip(' ') for i in corpus]
    final = list(filter(None, corpus))
    print(final)
    return final


def writetxt(path,data):
    with open(path,'w',encoding='utf8') as f:
        for i in data:
            f.write(i+'\n')


if __name__ == '__main__':
    data1 = readtxt('./新闻1.txt')
    #data2 = readtxt('./新闻2.txt')
    #data3 = readtxt('./待分词文本0519.txt')
    wordlexicon=readxls('./人民日报词汇频次表.xlsx')

    # 逆向最大匹配
    start = datetime.datetime.now()  #开始时间
    re = segword(data1)
    # re2 = segword(data)
    end = datetime.datetime.now()   #结束时间
    print((end - start).seconds)

    # 正向最大匹配
    start = datetime.datetime.now()  # 开始时间
    new1=segword_2(data1)
    end = datetime.datetime.now()  # 结束时间
    print((end - start).seconds)


    writetxt('./结果_逆向.txt', re)
    writetxt('./结果_正向.txt',new1)

    #writetxt('./实践分词结果.txt', re)
