# -*- coding: utf-8 -*-
import pymysql
import math

#用于计算标准差
def std(numbers,avg):
    var = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    return math.sqrt(var)
#用于生成查询某一特征值所有样本的命令
def torder(id,value):
    order='select a'+str(id)+' from tnb where a9='+str(value)+';'
    return order
#用于生成查询某一特征值所有样本均值的命令
def avgorder(id,value):
    order='select avg(a'+str(id)+') from tnb where a9='+str(value)+';'
    return order
#链接数据库
conn = pymysql.connect(host="127.0.0.1", user="root", passwd="1", db="other")
#查询库修改标记变量
order='select val from bysnum where name="change";'
cursor = conn.cursor()
cursor.execute(order)
data = int(cursor.fetchone()[0])

#数据库内容已经被修改，则执行下列语句
if data==1:
    print("the data is changed,we will flash the data.")
    #将库修改标记变量置0
    order="update bysnum set val=0 where name='change';"
    cursor.execute(order)
    conn.commit()
    #查询表结构，确认有多少特征值
    order='desc tnb;'
    cursor.execute(order)
    data = len(cursor.fetchall())
    #开始计算各个特征值的均值和标准差
    for i in range(1,data):
        #在结果不同的情况下计算
        for ii in range(0,2):
            #生成查询该特征值在该分类情况下均值的MySQL命令
            order=avgorder(i,ii)
            cursor.execute(order)
            avg = float(cursor.fetchall()[0][0])
            #生成获取该特征值在该分类情况下所有样本数据的MySQL命令
            order=torder(i,ii)
            cursor.execute(order)
            valueAll = cursor.fetchall()
            num=[]
            #将所有样本数据转换为标准一维列表
            for ai in valueAll:
                num.append(float(ai[0]))
            #计算标准差
            valueAll=std(num,avg)
            #更新特征值存放数据库
            order='update tnbValues set iavg='+str(avg)+',istd='+str(valueAll)+' where id='+str(i)+' and vid='+str(ii)+';'
            print(order)
            cursor.execute(order)
            conn.commit()
#数据库内容未被修改
elif data==0:
    print('data is not changed,we will exit.')
#查询到的值非标准量，出现错误
else:
    print('error,we fount a error value is '+str(data))
