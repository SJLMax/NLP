#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : HMM.py
# @Author: Shang
# @Date  : 2020/5/21

import xlrd


#读取训练语料
def readtxt(path):
    with open(path,encoding='utf8') as f:
        corpus=f.readlines()
        corpus=[line.strip('\n') for line in corpus]
        #print(corpus)
    return corpus


# 获取隐状态词性
def readxls(path):
    statelist = []
    rbook = xlrd.open_workbook(path)
    table = rbook.sheets()[0]
    nrows = table.nrows  # 获取行号
    ncols = table.ncols  # 获取列号
    for i in range(1, nrows):  # 第0行为表头
        alldata = table.row_values(i)  # 循环输出excel表中每一行，即所有数据
        result = alldata[0]  # 取出表中第一列数据
        statelist.append(result)
    statelist=[i.replace('/','')for i in statelist]
    #print(statelist)
    return statelist


def HMM():
    linenum=0
    for line in train:
        wordlist = []  # 所有词组
        state_seq = []  # 所有词组对应的词性标注
        linenum+=1
        line=line.strip().replace('\u3000','')
        words=line.split(' ')
        print(words)
        words2=list(filter(None, words))  # 过滤空字符串
        for word in words2:
            #print(word)
            p = word.index('/')
            wordlist.append(word[:p])
            state_seq.append(word[p + 1:])
        #print(wordlist,state_seq)
        if len(wordlist)!=len(state_seq):
            print('词组与词性不一致')
        else:
            for i in range(len(wordlist)):
                # 计算词性频次
                state_count[state_seq[i]]+=1.0
                if i==0:
                    # 开始概率
                    start_p[state_seq[i]]+=1.0
                else:
                    # 转移概率 后一个词性出现在前一个词性之后的次数
                    trans_p[state_seq[i-1]][state_seq[i]]+=1.0
                # 发射概率 词组对应词性的次数
                if wordlist[i] in emit_p[state_seq[i]]:
                    emit_p[state_seq[i]][wordlist[i]]+=1.0
                else:
                    emit_p[state_seq[i]][wordlist[i]] =1.0
    # 计算概率 除以总频次
    for st in statelist:
        start_p[st]=start_p[st]/linenum
        for word in emit_p[st]:
            emit_p[st][word]=emit_p[st][word]/state_count[st]
        for st1 in trans_p[st]:
            trans_p[st][st1]=trans_p[st][st1]/state_count[st]
    # print(start_p,emit_p,trans_p)
    writetxt('./result/start.txt',start_p)
    writetxt('./result/emit.txt',emit_p)
    writetxt('./result/trans.txt',trans_p)


def writetxt(path,data):
    with open(path,'w',encoding='utf8') as f:
        f.write(str(data))
    f.close()


if __name__ == '__main__':
    train = readtxt('./疫情_nlpir.txt')
    statelist=readxls('./中科院-词性频次表.xlsx')   # 隐状态
    # statelist=['n','wkz','wky','vshi','p','y']  测试
    start_p = {}  # 先验概率
    trans_p = {}  # 转移概率
    emit_p = {}  # 发射概率
    state_count={} # 词性频次
    # 初始化
    for state in statelist:
        start_p[state]=0.0
        state_count[state] = 0.0
        emit_p[state]={}
        trans_p[state]={}
        for s in statelist:
            trans_p[state][s]=0.0
    HMM()