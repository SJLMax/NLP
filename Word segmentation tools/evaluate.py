#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : evaluate.py
# @Author: Shang
# @Date  : 2020/5/26

import cut_words


# 单字
def word(data):
    sum=0
    for word in data.keys():
        if len(word)==1:
            sum+=1
    print(sum)


# 统计词汇
def wordlist(data):
    wordlist={}
    for line in data:
        line=line.split('/')
        for word in line:
            if word in wordlist.keys():
                wordlist[word] += 1
            else:
                wordlist[word] = 1
    #wordlist.pop('')
    print(len(wordlist))
    return wordlist


if __name__ == '__main__':

    jieba = cut_words.readtxt('./jieba_result.txt')
    snow = cut_words.readtxt('./SnowNLP_result.txt')
    pku = cut_words.readtxt('./pkuseg_result.txt')
    print('总词数：')
    jiebalist = wordlist(jieba)
    snowlist=wordlist(snow)
    pkulist=wordlist(pku)

    print('单字词数：')
    word(jiebalist)
    word(snowlist)
    word(pkulist)





