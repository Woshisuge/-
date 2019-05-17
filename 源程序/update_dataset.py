from xlrd import open_workbook
import xlrd
from datetime import date,datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import xlwt
import xlsxwriter

# 读取文件
wb = open_workbook('movie.xls')
sheet = wb.sheet_by_name('movie')

# 定义列表
genres=[]
actors=[]
country=[]
director=[]
feature=[]
vote_average=[]
title=[]
Genres=[]
Actors=[]
Country=[]
Director=[]
Feature=[]
Vote_average=[]
Title=[]

# 读取原文件中的列，存于列表中
for i in range(1,sheet.nrows):
    genres.append([sheet.row(i)[0].value])
    actors.append(sheet.row(i)[1].value)
    country.append(sheet.row(i)[2].value)
    director.append(sheet.row(i)[3].value)
    feature.append(sheet.row(i)[4].value)
    vote_average.append(sheet.row(i)[5].value)
    title.append(sheet.row(i)[6].value)
Genres.append(genres[0])
Actors.append(actors[0])
Country.append(country[0])
Director.append(director[0])
Feature.append(feature[0])
Vote_average.append(vote_average[0])
Title.append(title[0])

Actors[0] = Actors[0].split("|")
# 取原导演中的第一个人作为最终导演
if('|' in Director[0]):
    a=Director[0].index('|')
    Director[0]=Director[0][0:a]

# 遍历整个数据集，修改电影类型标签
for i in range(sheet.nrows-1):
    T=False
    print(len(Title))
    for j in range(len(Title)):
        T=False
        if(title[i]==Title[j]):
            if(genres[i][0] not in Genres[j]):
                print(genres[i][0])
                Genres[j].append(genres[i][0])
            break
        else:
            T=True
    if T==True:
        Genres.append(genres[i])
        Actors.append(actors[i])
        if('|' in Actors[len(Actors)-1]):
            Actors[len(Actors)-1]=Actors[len(Actors)-1].split("|")
        else:
            Actors[len(Actors)-1]=[Actors[len(Actors)-1]]
        Country.append(country[i])
        Director.append(director[i])
        if('|' in Director[len(Actors)-1]):
            a=Director[len(Actors)-1].index('|')
            Director[len(Actors)-1]=Director[len(Actors)-1][0:a]
        Feature.append(feature[i])
        Vote_average.append(vote_average[i])
        Title.append(title[i])

# 新建xlsx，存储
f = xlsxwriter.Workbook('movie_new.xlsx') #创建工作簿
sheet1 = f.add_worksheet('sheet1') #创建sheet

lable=['genres','actors','country','director','feature','vote_average','title']
print(Genres)
for i in range(len(lable)):
    sheet1.write(0,i+1,lable[i])
for i in range(len(Actors)):
    sheet1.write(i+1,0,i)
    sheet1.write(i+1,1,str(Genres[i]))
    sheet1.write(i+1,2,str(Actors[i]))
    sheet1.write(i+1,3,Country[i])
    sheet1.write(i+1,4,Director[i])
    sheet1.write(i+1,5,Feature[i])
    sheet1.write(i+1,6,vote_average[i])
    sheet1.write(i+1,7,Title[i])
f.close()

    
