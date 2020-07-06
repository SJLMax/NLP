#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pos.py
# @Author: Shang
# @Date  : 2020/5/21


from pynlpir import nlpir
import frequency
import random


#读取文献
def readtxt(path):
    data=[]
    with open(path,'r',encoding='utf-8') as f:
        for line in f.readlines():
            data.append(line.strip())
    return data


# 词性标注
def pos_tag(data):
    nlpir.Init(nlpir.PACKAGE_DIR.encode('UTF-8'), nlpir.UTF8_CODE, None)
    new=[]
    for line in data:
        s=line.encode('utf-8')
        new_line=nlpir.ParagraphProcess(s,True).decode('utf-8')
        new.append(new_line)
    return new


#写入文件
def writetxt(path,data):
    with open(path,'w',encoding='utf-8') as f:
        for line in data:
            f.write(line+'\n')
    f.close()


if __name__ == '__main__':
    data = readtxt('没有标注的语料.txt')
    new = pos_tag(data)
    #writetxt('新闻_nlpir.txt',new)
    dic = frequency.cixing(new)
    frequency.write_excel('./中科院-词性频次表.xlsx', dic)
    '''
    random.shuffle(corpus)  # 打乱
    # 划分
    train=corpus[:int(len(corpus)*0.8)]
    test=corpus[int(len(corpus)*0.8):]
    
    writetxt('./test.txt',test)
    writetxt('./train.txt',train)'''


