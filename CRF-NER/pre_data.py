from pyquery import PyQuery as pq
import os
import re
from collections import Counter
from sklearn.model_selection import KFold
import numpy as np
from sklearn.utils import shuffle
import sjl_baseio
k_10 = KFold(n_splits=10, shuffle=True, random_state=42)
entity_set = set([])
import codecs

def add_tag(text, entity_type):
    seq = ""
    if not text:
        return seq
    t_l = len(text)
    if entity_type:
        for (idx, w) in enumerate(text):
            if w == "" or w == " " or w == "\xa0" or w == "\u3000":
                continue
            if t_l <= 1:
                tag = "S-{}".format(entity_type)
                entity_set.add(tag)
            else:
                if idx == 0:
                    tag = "B-{}".format(entity_type)
                    entity_set.add(tag)
                elif idx == t_l - 1:
                    tag = "E-{}".format(entity_type)
                    entity_set.add(tag)
                else:
                    tag = "I-{}".format(entity_type)
                    entity_set.add(tag)

            seq += "{}\t{}\n".format(w, tag)
        return seq
    else:
        tag = "O"
        for (idx, w) in enumerate(text):
            if w == "" or w == " " or w == "\xa0" or w == "\u3000" or w=="\ufeff":
                continue
            seq += "{}\t{}\n".format(w, tag)

        return seq


def remove_pos(line):
    # new_line =re.sub("/[A-Za-z1-4]+(?=" ")", "", line)
    new_line = re.sub("/[A-Za-z1-4]+(?=" ")", "", line)  # 去掉词性标注  需要字符型 i为每个实体
    return new_line


def parse_file(lines, contain_pos):
    sequences = []
    for line in lines:
        line = line.strip()
        if contain_pos:
            line = remove_pos(line)
            line= re.sub("<[+]",'</',line)
            # print(line)
        if line:
            seq = ""
            for o in pq("<doc>{}<+doc>".format(line)).contents():
                # print(pq("<doc>{}<+doc>".format(line)))
                if hasattr(o, "tag"):
                    text = pq(o).text().replace("\n", "")
                    seq += add_tag(text, entity_type=o.tag)
                else:
                    seq += add_tag(o, entity_type=None)
            sequences.append(seq)
    # print(sequences)
    return sequences




def read_file(file_path):
    f_p = file_path
    with open(f_p, "r", encoding="utf-8") as fr:
        lines = fr.readlines()
    return lines


def dir_traverse(fold_path):
    fo_p = fold_path
    f_names = os.listdir(fo_p)
    f_p_list = []
    for f_n in f_names:
        f_p = os.path.join(fo_p, f_n)
        f_p_list.append(f_p)

    return f_p_list

def union():
    outdata = codecs.open('./alldata.txt', 'w', 'utf-8')
    pos=sjl_baseio.readtxt_all('./data_pos.txt')
    entity=sjl_baseio.readtxt_all('./data_entity.txt')
    # sjl_baseio.writetxt_line('./data_entity.txt',entity)
    for i,j in zip(pos,entity):
        if i!='\n' and j!='\n':
            i=i.replace('\n','')
            j=j.replace('\n','')
            if str(i[0])==str(j[0]):
                outdata.write(i+'\t'+j[2:7]+'\n')
            # else:
            #      print(i[0])
            #      print(j[0])
        else:
            outdata.write('\n')

    all=[]



def main():
    # news_fold = "data\新闻_已校对"

    # file_paths = dir_traverse(news_fold)
    # for f_p in file_paths:
    #     lines = read_file(f_p)
    #     sequence = parse_file(lines)

    virus_path = "data.txt"

    lines = read_file(virus_path)
    new_lines=[]
    for l in lines:
        new=re.sub("</", '<+', l)
        # print(new)
        new_lines.append(new)
    #  lines = ['<num>2020/m</num> 年/t <num>01/m</num>  月/t <num>01/m</num>日/t <num>09/m</num> :/wm <num>21/m <num>来源/n ：/wm 钱江/ns 晚报/n',' <gro>中小学生/n</gro> 下周/t 就要/d 考试/vi 了/y ，/wd 许多/m <gro>家长/n</gro> <gro>孩子/n</gro> 鼓足/v 了/ule 劲/n ，/wd 结果/n 却/d 被/pbei 不期而遇/vl 的/ude1 <dis>流感/n</dis> 击倒/v ，/wd 不得不/d 请假/vi 挤/v 医院/n 。/wj 但/c 不/d 想/v 未/d 考/v 就/d 输/v ，/wd 有的/rz <gro>孩子/n</gro> 去/vf 不/d 了/y 学校/n ，/wd 就/d 坚持/v 上/vf 校外/s 培训班/n ，/wd 结果/n 病毒/n 传播/v 开/v 来/vf ，/wd 更/d 多/a <gro>孩子/n</gro> 中招/v ；/wf 着急/a 的/ude1 <gro>孩子/n</gro> 发/v 着/uzhe 高烧/n 想/v 着/uzhe 功课/n ，/wd 口中/s 还/d 念念有词/vl ……/ws 临/v 考/v 前/f 的/ude1 病/a 娃/ng 和/cc <gro>家长/n</gro> 都/d 好/a 糟心/a 。/wj 上/v 完/vi 培训班/n ，/wd 回到/v 家/n 就/d 不/d 舒服/a']
    sequence = parse_file(new_lines, True)
    # print(entity_set)
    print(sequence)
    # sjl_baseio.writetxt_line('./data_entity.txt',sequence)
    seq_len = []
    # sequence = shuffle(sequence, random_state=42)

    for fold_index, (train_index, test_index) in enumerate(k_10.split(sequence)):
        seqs_train_tag = np.array(sequence)[train_index].tolist()
        seqs_test_tag = np.array(sequence)[test_index].tolist()
        seqs_train = seqs_train_tag
        seqs_test = seqs_test_tag
        print(seqs_test)

        # output_seq("train{}.txt".format(fold_index), seqs_train)
        # output_seq("test{}.txt".format(fold_index), seqs_test)

if __name__ == '__main__':
    main()
    #union()
    # data=sjl_baseio.readtxt_all('./alldata.txt')
    # print(data)
    # sjl_baseio.kfold(data)



