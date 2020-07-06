#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : evaluate.py
# @Author: Shang
# @Date  : 2020/5/23

import pos

def evaluate(data):
    wordlist = []  # 所有词组
    state_seq = []  # 所有词组对应的词性标注
    for line in data:
        line=line.strip().replace('\u3000','')
        words=line.split(' ')
        #print(words)
        words2=list(filter(None, words))  # 过滤空字符串
        for word in words2:
            #print(word)
            p = word.index('/')
            wordlist.append(word[:p])
            state_seq.append(word[p + 1:])
        #print(wordlist,state_seq)
    return state_seq



if __name__ == '__main__':
    test_HMM=pos.readtxt('./test_HMM2.txt')
    test_nlpir=pos.readtxt('./test_nlpir.txt')
    test_HMM_seq=evaluate(test_HMM)
    test_nlpir_seq=evaluate(test_nlpir)
    true=0
    all=len(test_nlpir_seq)
    false=[]
    sum=0
    for i,j in zip(test_nlpir_seq,test_HMM_seq):
        if i==j:
            true+=1
        else:
            false.append((i,j))
            if j!='z':
                print(i,j)
    print(len(false))
    print(sum)
    P=true/all
    print(P)