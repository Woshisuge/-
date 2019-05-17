import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
# 对数据集进行处理，除去对此次分析无用的数据，和无效数据
data = pd.DataFrame(pd.read_excel('F:\\02.xlsx'))
data.to_csv("F:\\02.csv")
df=pd.read_csv('F:\\02.csv')
df=df.drop(["5星人数","4星人数","3星人数","2星人数","1星人数","短评数量","语言","豆瓣网址","官方网址","IMDb链接","宣传海报链接","剧情简介","片长"],axis=1)
df=df.drop(index=(df.loc[(df['评价人数']==0)].index))
df=df.dropna() 
df=df.rename(columns={'电影名称':'title','评分':'vote_average','评价人数':'vote_count','类型':'genres','导演':'director','编剧':'writer','主演':'actors','制片国家/地区':'production_countries','上映日期':'year','总分(评分×评价人数)':'score','影评数量':'comment'})
df = df.reset_index(drop=True)
for i in range(len(df)):
    df['year'][i]=df['year'][i][0:4]
    df.to_csv("F:\\02.csv")

# 对处理后的表格做数据分析
full_df=pd.read_csv('F:\\02.csv') 
full_df['genres'].head()

real_genres=set()
for i in full_df['genres'].str.split('/'):
    real_genres=real_genres.union(i)
real_genres=list(real_genres)# 将集合转换成列表
print(real_genres)

# 将所有类型添加到列表
for i in real_genres:
    full_df[i]=full_df['genres'].str.contains(i).apply(lambda x:1 if x else 0)
full_df.head(2)
full_df.info()
full_df=full_df.rename(columns={'音乐':'music' , '古装':'ancient costume', '动作':'action', '历史': 'history', '惊栗':'thrilling', '武侠':'martial arts', '爱情':' love ', '同性': 'gay' , '驚悚 Thriller':'horror Thriller', '悬疑':'mystery', '灾难':'disaster', '荒诞':'absurd', '脱口秀':'show', '战争':'war', '舞台艺术':'stage', '奇幻':'fantasy', '惊悚':'Thriller', '纪录片': 'documentary', '西部':'the west', '冒险':'adventure', '鬼怪':'ghosts', '恐怖':' terrorists', '真人秀': 'Reality', '歌舞':'dancing', '运动':'sports', '悬念': 'suspense', '戏曲':'drama', '喜剧':'comedy', '黑色电影':'Film noir', '剧情':'plot', '儿童':'children', '犯罪':'criminal', '情色':'sex', '音樂 Music':'Music', '动画':'cartoon', '科幻':'science', '家庭':'family', '愛情 Romance':'romance', '短片':'short', '传记':'biography'})

part1_df=full_df[['year','music' , 'ancient costume','action',  'history','thrilling','martial arts', ' love ',  'gay' , 'horror Thriller', 'mystery', 'disaster', 'absurd', 'show', 'war', 'stage', 'fantasy', 'Thriller', 'documentary', 'the west', 'adventure', 'ghosts', ' terrorists', 'Reality', 'dancing', 'sports', 'suspense', 'drama', 'comedy', 'Film noir', 'plot', 'children', 'criminal', 'sex', 'Music', 'cartoon', 'science', 'family', 'romance', 'short', 'biography']]
# 按年分组统计每年各类型电影数量
year_cnt=part1_df.groupby('year').sum()
year_cnt.tail()

# 画图1每年电影类型数量
plt.figure(figsize=(14,16))
plt.rc('font',family='SimHei',size=13)#设置字体和大小，否则中文无法显示
ax1=plt.subplot(1,1,1)
year_cnt.plot(kind='line',ax=ax1)
plt.title('The number of movie types per year')
plt.show()

# 不同电影类型总数量
genre=year_cnt.sum(axis=0)#对列求和
genre=genre.sort_values(ascending=True)

# 画图2“不同电影类型数量”横向条形图
plt.figure(figsize=(13,15))
plt.rc('font',family='SimHei',size=14)
ax2=plt.subplot(1,1,1)
label=list(genre.index)
data=genre.values
rect=ax2.barh(range(len(label)),data,color='#6495ED',alpha=1)
ax2.set_title('The number of different types of movies')#设置标题
ax2.set_yticks(range(len(label)))
ax2.set_yticklabels(label)
# 添加数据标签
for x,y in zip(data,range(len(label))):
    ax2.text(x,y,'{}'.format(x),ha='left',va='center',fontsize=10)
plt.show()

# 统计各个国家的电影数
part3_df=full_df[['production_countries','year']]#提取需要的列子集
# 由于有的电影产地属于多个国家，故需要对production_countries进行分列
split_df=pd.DataFrame([x.split('/')for x in part3_df['production_countries']],index=part3_df.index)
# 将分列后的数据集与源数据集合并
part3_df=pd.merge(part3_df,split_df,left_index=True,right_index=True)
# 下面代码实现列转行
st_df=part3_df[['year',0,1,2,3]]
st_df=st_df.set_index('year')
st_df=st_df.stack()
st_df=st_df.reset_index()

st_df=st_df.rename(columns={0:'production_countries'})# 对列重命名
countries=st_df['production_countries'].value_counts()# 统计各个国家的电影数
countries.sum()
countries_rate=countries/countries.sum()# 计算占比
countries_top5=countries_rate.head(5)
other={'other':1-countries_top5.sum()}
countries_top6=countries_top5.append(pd.Series(other))
countries_top7=countries_top6.rename(index={'美国':'American','日本':'Japan','中国大陆':'Chinese Mainland','香港':'HongKong','英国':'UK'})
countries_top7

# 画图3“电影产地分布”饼图
labels=list(countries_top7.index)
plt.figure(figsize=(6,6))
plt.rc('font',family='SimHei',size=14)
ax=plt.subplot(1,1,1)
ax.pie(countries_top7,labels=labels,startangle=90,autopct='%1.1f%%')
ax.set_title('Film distribution')
plt.show()

# 计算不同类型电影平均分
real_genres=['music' , 'ancient costume','action',  'history','thrilling','martial arts', ' love ',  'gay' , 'horror Thriller', 'mystery', 'disaster', 'absurd', 'show', 'war', 'stage', 'fantasy', 'Thriller', 'documentary', 'the west', 'adventure', 'ghosts', ' terrorists', 'Reality', 'dancing', 'sports', 'suspense', 'drama', 'comedy', 'Film noir', 'plot', 'children', 'criminal', 'sex', 'Music', 'cartoon', 'science', 'family', 'romance', 'short', 'biography']
r={}
for i in real_genres:
    r[i]=full_df.loc[full_df[i]==1,'vote_average'].sum(axis=0)/genre[i]
mean=pd.Series(r).sort_values(ascending=True)

# 画图4“不同类型电影平均分”横向条形图
plt.figure(figsize=(10,14))
plt.rc('font',family='Simhei',size=14)
ax=plt.subplot(1,1,1)
label=mean.index
data=mean.values
ax.barh(range(len(label)),data,color='#B0E0E6',alpha=1)
ax.set_yticks(range(len(label)))# 设置y轴刻度
ax.set_yticklabels(label)# 设置刻度名称
ax.set_title('Average scores of different types of movies')
# 添加数据标签
for x,y in zip(data,range(len(label))):
    ax.text(x,y,'{:.1f}'.format(x),fontsize=10)# 坐标位置，及要显示的文字内容
plt.show()

grouped=full_df['vote_average'].groupby(full_df['director'])
real_director=grouped.mean().sort_values(ascending=False).head(50)
real_director=real_director.sort_values(ascending=True)
real_director=real_director.rename(index={'马修·纳斯奇克':'Matthew nascik','藤田阳一':'藤田陽一','杨洁':'Yang jie','迈克尔·约翰·沃伦':'Michael John warren','麦瑞安·艾利俄特':'Miriam elliott','乔恩·欧布':'Jon obi','迈克尔·恩格勒':'Michael engler','彼得·戴维森':'Peter Davidson','阿兰·本奈特':'Alan Bennett','索尔·斯威默':'Saul schwimmer','彼得·惠特莫尔':'Peter whitmore'})

# 画图5“高分电影导演top50”横向条形图
plt.figure(figsize=(10,12))
plt.rc('font',family='Simhei',size=12)
ax=plt.subplot(1,1,1)
label=real_director.index
data=real_director.values
ax.barh(range(len(label)),data,color='#87CEFA',alpha=1)
ax.set_yticks(range(len(label)))# 设置y轴刻度
ax.set_yticklabels(label)# 设置刻度名称
ax.set_title('Directors top50')
# 添加数据标签
for x,y in zip(data,range(len(label))):
    ax.text(x,y,'{:.1f}'.format(x),fontsize=10)# 坐标位置，及要显示的文字内容
plt.show()

# 计算各变量间的相关性，画散点图
corr=full_df.corr()
corr_average=corr['vote_average'].sort_values(ascending=False)
corr_average.head(10)

# 画图6“评分与评论人数的相关程度散点图”
x=full_df.loc[:,'vote_count']
y=full_df.loc[:,'vote_average']
plt.rc('font',family='SimHei',size=14)
plt.scatter(x,y,color='#5F9EA0')
plt.xlabel('vote_count')
plt.ylabel('vote_average')
plt.title('A scatter plot of vote_average and vote_count')
plt.show()

# 画图7“评分与年份的相关程度散点图”
x=full_df.loc[:,'year']
y=full_df.loc[:,'vote_average']
plt.rc('font',family='SimHei',size=14)
plt.scatter(x,y,color='#FF7F50')
plt.xlabel('year')
plt.ylabel('vote_average')
plt.title('A scatter plot of vote_average and year')
plt.show()

# 画图8“评论人数与年份的相关程度散点图”
x=full_df.loc[:,'year']
y=full_df.loc[:,'vote_count']
plt.rc('font',family='SimHei',size=14)
plt.scatter(x,y,color='#90EE90')
plt.xlabel('year')
plt.ylabel('vote_count')
plt.title('A scatter plot of vote_count and year')
plt.show()

# 每年所有电影综合的平均总分
grouped=full_df['score'].groupby(full_df['year'])
score_year=grouped.mean().sort_index(ascending=True)

# 画图9“不同年份电影行业总体评分”横向条形图
plt.figure(figsize=(17,5))
plt.rc('font',family='Simhei',size=8)
ax=plt.subplot(1,1,1)
label=score_year.index
data=score_year.values
ax.bar(range(len(label)),data,color='#8B4513',alpha=1)
ax.set_xticks(range(len(label)))#设置x轴刻度
for tick in ax.get_xticklabels():
    tick.set_rotation(70)
ax.set_xticklabels(label)#设置刻度名称
ax.set_title('Overall score for different years',fontsize=20)
plt.show()







