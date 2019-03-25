# -*- coding: utf-8 -*-
import pymysql
import math
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="1", db="other")
#这是待判断变量
iii=[12,90,84,33,105,30.0,0.488,46]

def pd(val):
    if val[0]<0 or val[0]>100:
        print("怀孕次数异常")
        exit()
    if val[1]<0 or val[1]>250:
        print("血糖浓度异常")
        exit()
    if val[2]<0 or val[2]>200:
        print("血压异常")
        exit()
    if val[3]<0 or val[3]>100:
        print("三头肌皮脂厚度异常")
        exit()
    if val[4]<0 or val[4]>900:
        print("2小时血清胰岛素数值异常")
        exit()
    if val[5]<0 or val[5]>100:
        print("身体质量指数异常")
        exit()
    if val[6]<0 or val[6]>5:
        print("糖尿病家族遗传作用值异常")
        exit()
    if val[7]<0 or val[7]>150:
        print("年龄值异常")
        exit()
    print("数据有效")
#高斯公式
def gs(x, avg, std):
    exponent = math.exp(-(math.pow(x-avg,2)/(2*math.pow(std,2))))
    return (1 / (math.sqrt(2*math.pi) * std)) * exponent
#计算根据均值和标准差而来的概率的累乘
def hz(ivalues,yvalues):
    p=1
    for i in range(len(ivalues)):
        avg,std=ivalues[i]
        p=p*gs(yvalues[i],avg,std)
    return p

pd(iii)
#生成游标
cursor = conn.cursor()
#查询表有多少特征值
order='desc tnb;'
cursor.execute(order)
data = len(cursor.fetchall())
#v用于存储两种分类的各自可能性
v=[0.0,0.0]
#分别计算两种分的可能性
for ii in range(0,2):
    a=[]
    #计算每种情况的可能性
    for i in range(1,data):
        #查询在当前情况下的每个特征的特征值
        order='select iavg,istd from tnbValues where id='+str(i)+' and vid='+str(ii)+';'
        cursor.execute(order)
        idata=cursor.fetchall()[0]
        #将特征值转成列表存储
        a.append(idata)
    
    #调用汇总函数，计算概率
    v[ii]=hz(a,iii)
if v[0]>v[1]:
    print('经判断是0，预测准确率为：'+str((v[0]/(v[0]+v[1]))*100)+'%')
elif v[0]<v[1]:
    print('经判断是1，预测准确率为：'+str((v[1]/(v[0]+v[1]))*100)+'%')
else:
    print('判断两种结果概率相等。')
