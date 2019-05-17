# encoding:utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv

def get_Co_authors(filePath):
    with open(filePath, 'r', encoding='utf-8-sig') as f:
        text = f.read()
      #  text.remove('"') 
        co_authors_list = text.split('\n')
        co_authors_list.remove('')          
        return co_authors_list

def str2csv(filePath, s):
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(s)
    print('写入文件成功,请在'+filePath+'中查看')

def sortDictValue(dict, is_reverse):
    tups = sorted(dict.items(), key=lambda item: item[1], reverse=is_reverse)
    s = ''
    for tup in tups:  # 合并成csv需要的逗号分隔格式
        s = s + tup[0] + ',' + str(tup[1]) + '\n'
    return s

def build_matrix(co_authors_list, is_reverse):
    node_dict = {}  # 节点字典,包含节点名+节点权值(频数)
    edge_dict = {}  # 边字典,包含起点+目标点+边权值(频数)
    for row_authors in co_authors_list:
        row_authors_list = row_authors.split(',') 
        for index, pre_au in enumerate(row_authors_list):             
            if pre_au not in node_dict:
                node_dict[pre_au] = 1
            else:
                node_dict[pre_au] += 1
            if pre_au == row_authors_list[-1]:
                break
            connect_list = row_authors_list[index+1:]
            for next_au in connect_list:
                A, B = pre_au, next_au    
                if A > B:
                    A, B = B, A
                key = A+','+B  # 格式化为逗号分隔A,B形式,作为字典的键           
                if key not in edge_dict:
                    edge_dict[key] = 1
                else:
                    edge_dict[key] += 1
    # 对得到的字典按照value进行排序
    node_str = sortDictValue(node_dict, is_reverse)  # 节点
    edge_str = sortDictValue(edge_dict, is_reverse)   # 边
    return node_str, edge_str
if __name__ == '__main__':
    readfilePath = r'F:\\04.txt'
    writefilePath1 = r'F:\\03node.csv'
    writefilePath2 = r'F:\\03edge.csv'
    # 读取csv文件获取信息并存储到列表中
    co_authors_list = get_Co_authors(readfilePath)
    # 构建共现矩阵(存储到字典中), 并将该字典按照权值排序
    node_str, edge_str = build_matrix(co_authors_list, is_reverse=True)
    print(edge_str)
    # 将字符串写入到本地csv文件中
    str2csv(writefilePath1, node_str)
    str2csv(writefilePath2, edge_str)