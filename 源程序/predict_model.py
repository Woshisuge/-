# 数据分析包导入
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import warnings
from scipy import spatial
warnings.filterwarnings(action = 'ignore') # 忽略警告

# 计算数量
def countN(column):
    count = dict()
    for row in column:
        for ele in row:
            if ele in count:
                count[ele] += 1
            else:
                count[ele] = 1
    return count

# 数据导入，这个数据集是标准的csv格式
movies_15 = pd.read_csv('D:/movie_new.csv',engine='python')
# 数据预览
movies_15.head(2)
movies_15.info()

#首先对于每部影片都构造二元数组表示类型、导演和主演：
def binary(wordlist0, wordlist):
    binary = [] 
    for word in wordlist0.index:
        if word in wordlist:
            binary.append(1)
        else:
            binary.append(0)
    return binary
# 构建向量
genres = pd.Series(countN(movies_15.genres)).sort_values(ascending=False)
movies_15['genres_bin'] = [binary(genres, x) for x in movies_15.genres]  #影片类型的二元数组
directors = movies_15.groupby('director').size().sort_values(ascending=False)
print(2)
movies_15['director_bin'] = [binary(directors, x) for x in movies_15.director]  #影片导演的二元数组
actors = pd.Series(countN(movies_15.actors)).sort_values(ascending=False)  
print(3)
movies_15['actors_bin'] = [binary(actors, x) for x in movies_15.actors]# 影片主演的二元数组

# 定义一个函数计算两部影片的夹角（即不相似度）：
def angle(movie1, movie2):
    dis_tot = 0
    iterlist = [[movie1.genres_bin, movie2.genres_bin],
                [movie1.director_bin, movie2.director_bin],
                [movie1.actors_bin, movie2.actors_bin]]
    for b1, b2 in iterlist:
        if(1 not in b1) or (1 not in b2):
            dis = 1
        else:
            dis = spatial.distance.cosine(b1, b2)
        dis_tot += dis
    return dis_tot

print(angle(movies_15.iloc[0], movies_15.iloc[5]))  #打印两部电影的夹角

# 评分预测函数
def predictor(new_movie):
    movie_bin = pd.Series()
    movie_bin['genres_bin'] = binary(genres, new_movie['genres'])
    movie_bin['director_bin'] = binary(directors, new_movie['director'])
    movie_bin['actors_bin'] = binary(actors, new_movie['actors'])
    vote = movies_15.copy()
    vote['angle'] = [angle(vote.iloc[i], movie_bin) for i in range(len(vote))]
    vote = vote.sort_values('angle')
    vote_avg = np.mean(vote.vote_average[0:5])
    return vote_avg

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

# 待预测的十部影片信息
sou_movie = [0 for x in range(0, 10)] 
sou_movie[0] = {'genres': ['剧情', '喜剧'], 'director': ['文牧野'], 'actors': ['徐峥', '王传君', '周一围', '谭卓', '章宇']}
sou_movie[1] = {'genres': ['剧情', '喜剧', '爱情'], 'director': ['冯小刚'], 'actors': ['葛优', '徐帆']}
sou_movie[2] = {'genres': ['剧情', '爱情'], 'director': ['谢晋'], 'actors': ['朱时茂', '丛珊', '牛犇', '奇梦石']}
sou_movie[3] = {'genres': ['剧情', '喜剧'], 'director': ['英勉'], 'actors': ['中村苍', '池松壮亮']}
sou_movie[4] = {'genres': ['喜剧', '动作', '爱情'], 'director': ['吴天戈'], 'actors': ['陈姝', '金为珩', '曾晨', '周大勇', '周国宾']}
sou_movie[5] = {'genres': ['喜剧', '动作', '爱情', '科幻'], 'director': ['华子'], 'actors': ['华子', '杨潇', '罗江', '雷德鹏', '姜虎章']}
sou_movie[6] = {'genres': ['剧情', '爱情'], 'director': ['郭帆'], 'actors': ['周冬雨', '林更新', '隋凯', '王啸坤', '龚格尔']}
sou_movie[7] = {'genres': ['剧情'], 'director': ['田羽生'], 'actors': ['韩庚', '郑恺', '于文文', '曾梦雪', '罗米']}
sou_movie[8] = {'genres': ['剧情'], 'director': ['郭敬明'], 'actors': ['杨幂', '柯震东', '郭采洁', '陈学冬', '郭碧婷']}
sou_movie[9] = {'genres': ['剧情', '动作', '爱情'], 'director': ['冯小刚'], 'actors': ['章子怡', '葛优', '吴彦祖', '周迅', '马精武']}

# 实际十部影片的评分
sou_grade=[]
sou_grade.append(7.0) 
sou_grade.append(7.8) 
sou_grade.append(7.9)
sou_grade.append(7.0)
sou_grade.append(6.8)
sou_grade.append(7.1)
sou_grade.append(6.3)
sou_grade.append(6.5)
sou_grade.append(6.5)
sou_grade.append(7.3)

# 预测出的十部影片的评分
pre_movie=[]
for i in range(10):
    a=predictor(sou_movie[i])
    a=round(a,1)
    print(predictor(sou_movie[i]))
    pre_movie.append(a)

cc=[]
for i in range(10):
    cc.append(i)

plt.plot(cc,sou_grade,'o-',c='r',label ='Actual')
plt.plot(cc,pre_movie,'o-',c='b',label ='Predict')    
# 设置数字标签

for a, b in zip(cc, sou_grade):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
for a, b in zip(cc, pre_movie):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=10)
# 绘图，预测与实际相比较
plt.xlabel('Movie lable')
plt.ylabel('Score lable')
plt.ylim((0,10))
plt.title("Prediction results ")
plt.legend()
plt.show()

