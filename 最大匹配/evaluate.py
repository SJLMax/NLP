#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : evaluate.py
# @Author: Shang
# @Date  : 2020/5/26

import frequency_wordlist
import segword

# 单字
def word(data):
    sum=0
    for word in data.keys():
        if len(word)==1:
            sum+=1
    return sum


# 非词典单字
def non_word(data):
    num=0
    for word in data.keys():
        if len(word)==1 and word not in wordlist:
            num+=1
    return num


if __name__ == '__main__':
    wordlist=segword.readxls('./人民日报词汇频次表.xlsx')
    zheng = frequency_wordlist.readtxt('./结果_正向.txt')
    ni = frequency_wordlist.readtxt('./结果_逆向.txt')
    nilist=frequency_wordlist.wordlist(ni)
    zhenglist=frequency_wordlist.wordlist(zheng)
    #frequency_wordlist.wordlist()
    print('逆向结果总词数：',len(nilist))
    print('正向结果总词数：', len(zhenglist))

    sum_ni=word(nilist)
    sum_zheng=word(zhenglist)
    print('逆向结果单字词数：', sum_ni)
    print('正向结果单字词数：', sum_zheng)

    num_ni=non_word(nilist)
    num_zheng=non_word(zhenglist)
    print('逆向结果非词典单字词数：', num_ni)
    print('正向结果非词典单字词数：', num_zheng)



