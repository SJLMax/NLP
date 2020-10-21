#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cut_words.py
# @Author: Shang
# @Date  : 2020/5/31
import jieba
import datetime
from snownlp import SnowNLP
import pkuseg

def readtxt(path):
    with open(path,'r',encoding='utf8') as f:
        data=f.readlines()
        data=[line.strip('\n').replace('\u3000','').replace(' ','') for line in data]
        data=list(filter(None,data))
        # print(data)
        return data


# jieba分词
def jiebacut(data):
    re=[]
    for line in data:
        seg_list = jieba.cut(line,cut_all=False)  # 精确模式
        s = "/".join(seg_list)
        re.append(s)
    writetxt('./jieba_result.txt',re)
    #print(re)


# snownlp
def snowcut(data):
    re=[]
    for line in data:
        seg_list=SnowNLP(line)
        s = "/".join(seg_list.words)
        re.append(s)
    writetxt('./SnowNLP_result.txt',re)
    # print(re)


# pkuseg
def pkusegcut(data):
    re=[]
    for line in data:
        seg = pkuseg.pkuseg()  # 程序会自动下载所对应的细领域模型
        text = seg.cut(line)  # 进行分词
        s="/".join(text)
        re.append(s)
    writetxt('./pkuseg_result.txt',re)
    #print(re)



def writetxt(path,data):
    with open(path,'w',encoding='utf8') as f :
        for line in data:
            f.write(line)
            f.write('\n')
    f.close()


if __name__ == '__main__':
    news=readtxt('./corpus.txt')
    sum=0
    for line in news:
        sum=sum+len(line)
    print('总字数：',sum)
    start = datetime.datetime.now()
    jiebacut(news)    # jieba
    end = datetime.datetime.now()
    print('jiabe time:',end-start)

    start = datetime.datetime.now()
    snowcut(news)     # SnowNLP
    end = datetime.datetime.now()
    print('SnowNLP time:', end - start)

    start = datetime.datetime.now()
    pkusegcut(news)   # Pkuseg
    end = datetime.datetime.now()
    print('PkuSeg time:', end - start)


