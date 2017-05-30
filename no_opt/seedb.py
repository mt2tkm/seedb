# -*- coding:utf-8 -*-
import time,math,numpy as np
from config import config_data
import matplotlib.pyplot as plt
"""課題
・　query 作成の際に’注文金額’という属性があることを必要としている。

"""


class SeeDB:
    query_time,deviance_time,sort_time,visualization_time = 0,0,0,0
    def __init__(self, db,data_set,table,k):
        self.cursor = config_data(db)
        self.data_set, self.table,self.k = data_set, table, k
        self.terms()
        self.start = time.time()
        self.top_k = {}

    def terms(self):
        self.where1,self.where2 = input('1つ目のwhere句を入力してください->'),input('2つ目のwhere句を入力してください->')

    def query(self):
        if self.func == 'sum' or '注文金額' in self.attribute1:
            query1 = 'select ' + self.attribute2 +',' + self.func + '(' + 'CAST(' + self.attribute1 + ' AS BIGINT' + '))' + ' from ' + self.table
        else:
            query1 = 'select ' + self.attribute2 + ',' + self.func + '(' + self.attribute1 + ')' + ' from ' + self.table
        if self.where1 != '':
            query1 += ' where ' + self.where1
        query1 += ' group by ' + self.attribute2 + ' order by ' + self.attribute2

        if self.func == 'sum' or '注文金額' in self.attribute1:
            query2 = 'select ' + self.attribute2 + ',' + self.func + '(' + 'CAST(' + self.attribute1 + ' AS BIGINT' + ')) ' + ' from ' + self.table
        else:
            query2 = 'select ' + self.attribute2 +',' + self.func + '(' + self.attribute1 + ')' + ' from ' + self.table
        if self.where2 != '':
            query2 += ' where ' + self.where2
        query2 += ' group by ' + self.attribute2 + ' order by ' + self.attribute2

        self.cursor.execute(query1)
        data1 = self.cursor.fetchall()
        self.cursor.execute(query2)
        data2 = self.cursor.fetchall()

        return data1,data2

    def nomalization(self,data):
        z,sum_x = tuple(),0
        for x,y in data:
            sum_x += y
        for x,y in data:
            z += ( (x , y/sum_x), )
        return z

    def distance(self):
        # make queries and execute these
        a = time.time()
        x,y = self.query()
        self.query_time += time.time() - a

        # calclate deviance
        deviance = 0
        a = time.time()
        x,y = self.nomalization(x),self.nomalization(y)
        dd = dict()
        for i, j in x:
            dd[i] = j
        for i, j in y:
            if i in dd:
                dd[i] = math.fabs(dd[i] - j)
            else:
                dd[i] = j
        for x, dis in dd.items():
            deviance += dis
        self.deviance_time += time.time() - a

        return deviance

    def cheak_k(self,d):
        # preprocessing
        if self.attribute1 == '*':
            self.attribute1 = '.'+self.attribute1
        # cheak deviance and sort results
        if len(self.top_k) == 0:
            self.top_k[0] = (d,(self.func,self.attribute1,self.attribute2))
        elif len(self.top_k) < self.k:
            target = (d, (self.func,self.attribute1, self.attribute2))
            for i, j in self.top_k.items():
                if j[0] < target[0]:
                    self.top_k[i] = target
                    target = j
            self.top_k[len(self.top_k)] = target
        else:
            target = (d,(self.func,self.attribute1,self.attribute2))
            for i,j in self.top_k.items():
                if j[0] < target[0]:
                    self.top_k[i] = target
                    target = j

    def visualization(self):
        # setting n*m
        n = math.ceil(np.sqrt(self.k))
        m = math.ceil(self.k / n)
        fig, axes = plt.subplots(nrows=n, ncols=m, figsize=(10, 8))
        ii = 0
        for dis,dt in self.top_k.items():
            self.attribute1, self.attribute2, self.func = dt[1][1].split('.')[1], dt[1][2], dt[1][0]
            data1, data2 = self.query()
            data1, data2 = self.nomalization(data1), self.nomalization(data2)
            x_agre = list()
            for i, j in data1 + data2:
                if not i in x_agre:
                    x_agre.append(i)
            t1, t2 = dict(data1), dict(data2)
            x, y1, y2 = [i for i in range(0, len(x_agre))], list(), list()
            for i in x_agre:
                if i in t1:
                    y1.append(t1[i])
                else:
                    y1.append(0)
                if i in t2:
                    y2.append(t2[i])
                else:
                    y2.append(0)
            axes[int(ii/m), ii%m].plot(x, y1, linewidth=2)
            axes[int(ii/m), ii%m].plot(x, y2, linewidth=2)
            axes[int(ii/m), ii%m].set_xticks(x)
            axes[int(ii/m), ii%m].set_xticklabels(x_agre, rotation=30)
            axes[int(ii/m), ii%m].set_title(ii)
            axes[int(ii/m), ii%m].set_xlabel(self.attribute2)
            axes[int(ii/m), ii%m].grid(True)
            ii+=1
            if ii > self.k:
                break
        #plt.show()
        #plt.savefig('sample.png')

    def output(self):
        print('================================================================')
        print('All_time:',time.time()-self.start)
        print('Query_time:',self.query_time)
        print('Calcu_deviance_time:',self.deviance_time+self.sort_time)
        print('Visualization_time:',self.visualization_time)
        print('================================================================')
        print('順位, 乖離度, (集計関数, 集計属性, 集約属性)')
        print('================================================================')
        for i,j in self.top_k.items():
            print(i+1,j[0],j[1])
        print('================================================================')

    def main(self):
        # roop
        for self.attribute2, ite in self.data_set.items():
            for self.func, self.attribute1 in ite:
                # calclate euclid distance
                d = self.distance()
                # sort results
                a = time.time()
                if d != -1 and d<1:
                    self.cheak_k(d)
                self.sort_time += time.time() - a
            #print(time.time() - self.start)
        a = time.time()
        self.visualization()
        self.visualization_time = time.time() - a
        self.output()
