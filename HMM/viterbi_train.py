#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : viterbi_train.py
# @Author: Shang
# @Date  : 2020/5/23

import HMM
import pos
import datetime


def readtxt(path):
    with open(path,'r',encoding='utf8') as f:
        data=f.read()
        # print(type(data))
    return data


# 维特比算法
def viterbi(sentence):
    path={}
    max_pro=[{}]
    # 初始化
    for state in statelist:
        # 计算句子第一个词所有词性标注的概率
        max_pro[0][state] = start_p[state] * emit_p[state].get(sentence[0],1e-5)  # 数据平滑
        # 初始路径
        path[state] = [state]

    # 遍历所有词
    for i in range(1,len(sentence)):
        max_pro.append({})
        newpath={}
        for now in statelist: # 当前预测
            record=[]
            for pre in statelist:  # 前一个
                t=max_pro[i-1][pre] * trans_p[pre].get(now,0) * emit_p[now].get(sentence[i],1e-5)  # 数据平滑
                record.append((t,pre))
            max_pro[i][now],state=max(record)  # 纪录最大概率
            # print(state)
            newpath[now] = path[state] + [now]
            # print(newpath)
        path=newpath
    max_p,state = max([(max_pro[len(sentence)-1][j],j) for j in statelist])   # 最后一个词对应最大概率的状态序列
    return max_p,path[state]


if __name__ == '__main__':
    # 读取训练参数
    start_p=eval(readtxt('./result/start.txt'))
    emit_p=eval(readtxt('./result/emit.txt'))
    trans_p=eval(readtxt('./result/trans.txt'))
    statelist = HMM.readxls('./中科院-词性频次表.xlsx')
    print(statelist)

    # 读取待标注文本
    f=open('./test原始.txt','r',encoding='utf8')
    corpus=f.readlines()
    corpus=[line.strip('\n') for line in corpus]
    corpus = list(filter(None, corpus))
    print(corpus)
    # corpus=['欧盟 和 中国 应当 携手 合作 抗击 疫情 ， 协助 所有 国家 阻止 疫情 蔓延 ']
    # 测试句子
    # sentences=['鼠疫 为 自然 疫 源 性 传染病 ， 主要 在 啮 齿 类 动物 间 流行' ,' 鼠 、 旱獭 等 为 鼠疫 耶 尔 森 菌 的 自然 宿主 。']

    # 结果输出
    output=[]
    start=datetime.datetime.now()
    for line in corpus:
        line=line.split()
        # print(line)
        # viterbi算法
        probility,path=viterbi(line)
        print(probility,path)
        if len(line)!=len(path):
            print('标注出错')
        else:
            sen = []
            for word,state in zip(line,path):
                sen.append(word+'/'+state)
            sen=" ".join(sen)
            output.append(sen)
    print(output)
    end=datetime.datetime.now()
    print((end-start).seconds)
    pos.writetxt('./test_HMM2.txt',output)
