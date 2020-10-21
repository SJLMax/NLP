#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 词性标注.py
# @Author: Shang
# @Date  : 2020/6/10

import jieba
import jieba.posseg as pseg
from snownlp import SnowNLP
import thulac
import datetime


# 读取文献
def readtxt(path):
    data = []
    with open(path, 'r', encoding='utf8') as f:
        line = f.readlines()
        for i in line:
            i = i.replace('\n','').replace('\xa0','').replace('\u3000','')
            data.append(i)
        #print(data)
    return data


def pos_jiaba(data):
    sentences=[]
    for line in data:
        words=pseg.cut(line)
        sen=[]
        for w in words:
            p = "/".join(w)
            sen.append(p)
        temp = " ".join(sen)
        sentences.append(temp)
    # print(sentences)
    writetxt('./jiaba词性标注.txt',sentences)


def pos_snow(data):
    sentences = []
    for line in data:
        s = SnowNLP(line)
        sen = []
        for w in s.tags:
            p = "/".join(list(w))
            sen.append(p)
        temp = " ".join(sen)
        sentences.append(temp)
    #print(sentences)
    writetxt('./SnowNLP词性标注.txt', sentences)


def pos_thu(data):
    sentences=[]
    thu = thulac.thulac()
    for line in data:
        words = thu.cut(line)
        sen=[]
        for w in words:
            p = "/".join(list(w))
            sen.append(p)
        temp = " ".join(sen)
        sentences.append(temp)
    #print(sentences)
    writetxt('./thu词性标注.txt', sentences)


def writetxt(path,data):
    with open(path,'w',encoding='utf8') as f:
        for line in data:
            f.write(line+'\n')
    f.close()


if __name__ == '__main__':
    data = readtxt(r'./待分词文本0519.txt')
    # data=['新华社北京12月31日电 （记者邹伟、王思北）2020年新年戏曲晚会31日晚在国家大剧院举行。','党和国家领导人习近平、李克强、栗战书、汪洋、王沪宁、赵乐际、韩正、王岐山等，同首都近千名群众欢聚一堂，一起观看演出，迎接新年的到来。']
    s = datetime.datetime.now()
    #pos_jiaba(data)
    e = datetime.datetime.now()
    print('jiaba用时：',(e-s).seconds)
    s = datetime.datetime.now()
    #pos_snow(data)
    e = datetime.datetime.now()
    print('Snow用时：', (e - s).seconds)
    s = datetime.datetime.now()
    pos_thu(data)
    e = datetime.datetime.now()
    print('thu用时：', (e - s).seconds)


