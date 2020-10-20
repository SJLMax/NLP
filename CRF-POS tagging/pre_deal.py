#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : pre_deal.py
# @Author: Shang
# @Date  : 2020/6/15


import codecs
import random

def readtxt(path):
    with open(path,'r',encoding='utf8') as f:
        lines=f.readlines()
        lines=[i.replace('\u3000','').replace('\xa0','').replace('\n','').replace('\ufeff','') for i in lines]
        # random.shuffle(lines)
        print(lines)
        return lines


def deal(data):
    outdata = codecs.open('/home/ugrad/Shang/crf/crf词性标注/diease/alldata.txt', 'w', 'utf-8')
    # data=['中小学生/n 下周/t 就要/d 考试/vi 了/y ，/wd 许多/m 家长/n 孩子/n 鼓足/v 了/ule 劲/n ，/wd 结果/n 却/d 被/pbei 不期而遇/vl 的/ude1 流感/n 击倒/v ，/wd 不得不/d 请假/vi 挤/v 医院/n 。/wj 但/c 不/d 想/v 未/d 考/v 就/d 输/v ，/wd 有的/rz 孩子/n 去/vf 不/d 了/y 学校/n ，/wd 就/d 坚持/v 上/vf 校外/s 培训班/n ，/wd 结果/n 病毒/n 传播/v 开/v 来/vf ，/wd 更/d 多/a 孩子/n 中招/v ；/wf 着急/a 的/ude1 孩子/n 发/v 着/uzhe 高烧/n 想/v 着/uzhe 功课/n ，/wd 口中/s 还/d 念念有词/vl ……/ws 临/v 考/v 前/f 的/ude1 病/a 娃/ng 和/cc 家长/n 都/d 好/a 糟心/a 。/wj']
    cut_list=['。', '？', '！']
    for line in data:
        line=line.split(' ')
        line=filter(None,line)
        for word in line:
            word=word.split('/')
            print(word)
            if len(word[0])==1:
                if word[0] in cut_list:
                    outdata.write(word[0] + '\tS-' + word[1] + '\n'+'\n')
                else:
                    outdata.write(word[0] + '\tS-' + word[1] + '\n')
            else:
                for i in range(len(word[0])):
                    if i == 0:
                        f = "B-"+word[1]
                    elif i == len(word[0]) - 1:
                        f = "E-"+word[1]
                    else:
                        f = "I-"+word[1]
                    outdata.write(word[0][i] + '\t' + f + '\r\n')

def writetxt(path,data):
    with open(path,'w',encoding='utf8') as f:
        for i in data:
            f.write(str(i)+'\n')


if __name__ == '__main__':
    # data=readtxt('/home/ugrad/Shang/crf/crf词性标注/diease/data.txt')
    # deal(data)
    data = readtxt('/home/ugrad/Shang/crf/crf词性标注/diease/alldata.txt')
    print(data)
    train_list = data[:int(len(data) * 0.9)]
    text_list = data[int(len(data) * 0.9):]
    writetxt("./train.txt", train_list)
    writetxt("./test.txt", text_list)