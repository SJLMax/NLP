#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : frequency_wordlist.py
# @Author: Shang
# @Date  : 2020/5/16

import re
import xlsxwriter

def readtxt(path):
    with open(path,'r',encoding='utf8') as f:
        line = f.readlines()
        line = [i.replace('\n','') for i in line]
        print(line)
    return line


# 匹配词性
def cixing(data):
    dic = {}
    for line in data:   # 匹配普通词性标注
        pattern = re.findall(r'/[A-Za-z]{1,30}', line)
        for p in pattern:
                if p in dic:
                    dic[p] += 1
                else:
                    dic[p] = 1
    for line in data:   # 匹配实体词性标注,如[江  峡  大道]ns
        pattern2 = re.findall(r'][A-Za-z]{1,30}', line)
        for p in pattern2:
                #print(p)
                if p in dic:
                    dic[p] += 1
                else:
                    dic[p] = 1
    print(dic)
    print(len(dic))
    return dic


# 去除词性标注
def restore(dic, data):
    raw_data=[]
    final=[]
    for line in data:
        #print(line)  这里其实可以对字典排序一下 但是我懒得改了
        line=line.strip(' ').replace('[','')
        for i in dic.keys():
            if len(i)>=3:
                line = line.replace(i,'')  # 防止部分词性前缀相似导致的错误匹配
        raw_data.append(line)
    for l in raw_data:
        for i in dic.keys():
            l = l.replace(i,'').strip(' ')
        final.append(l)
    #print(final)
    return final


# 统计词汇
def wordlist(data):
    wordlist={}
    for line in data:
        line=line.split(' ')
        for word in line:
            if word in wordlist.keys():
                wordlist[word] += 1
            else:
                wordlist[word] = 1
    #wordlist.pop('')
    print(wordlist)
    return wordlist


def write_excel(path,dic):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet('sheet1')
    worksheet.write(0, 0, '词汇')
    worksheet.write(0, 1, '频次')
    for k, i in zip(range(len(dic)), dic.keys()):
        j = dic[i]
        #print(i, j)
        worksheet.write(k+1, 0, i)
        worksheet.write(k+1, 1, j)
    workbook.close()



if __name__ == '__main__':
    data= readtxt('./199801人民日报语料.txt')
    dic=cixing(data)
    final = restore(dic,data)
    wordlist = wordlist(final)
    write_excel('./人民日报词汇频次表.xlsx',wordlist)