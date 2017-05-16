# -*- coding:utf-8 -*-
import time,math,numpy as np
from config import config_data
import matplotlib.pyplot as plt
import pandas as pd

class SeeDB:
    query_time,deviance_time,sort_time,visualization_time = 0,0,0,0

    def __init__(self, db, groupby, table, k, aggregate):
        self.con,self.cursor = config_data(db)
        self.groupby, self.table,self.k,self.aggregate = groupby, table, k, aggregate
        self.start = time.time()
        self.top_k = {}
        self.terms()

    def terms(self):
        self.column1, self.where1 = input('1つ目のwhere句の属性を入力してください->'), input('1つ目のwhere句の具体的条件を入力してください->')
        self.column2, self.where2 = input('2つ目のwhere句の属性を入力してください->'), input('2つ目のwhere句の具体的条件を入力してください->')

    def fullshare_query(self):
        g_b = str()
        for group in self.groupby:
            g_b += group + ', '
        select = 'select ' + g_b
        for agg in self.aggregate:
            select = select + 'sum(CAST(' + agg + ' AS BIGINT)) AS ' + agg.split('.')[1] + ', ' + 'count(' + agg + ') AS 個数_' + agg.split('.')[1] + ' , '
        select = select[:-2]
        
        full_query = select + 'from ' + self.table + ' group by ' + g_b[:-2] + ' order by ' + g_b[:-2]

        self.df = pd.io.sql.read_sql(full_query,self.con)

    def roop(self):
        print(len(self.df))
        df1 = self.df
        for i in range(len(self.groupby)):
            dt1 = df1[df1[self.column1] == self.where1].groupby(df1.columns[0]).sum().iloc[:,-6:]
        print(dt1)
        sample = (dt1 - dt1.mean())/dt1.std()
        print(sample)




    def nomalization(self,data):
        z,sum_x = tuple(),0
        for x,y in data:
            sum_x += y
        for x,y in data:
            z += ( (x , y/sum_x), )
        return z

    def distance(self):
        a = time.time()
        #x,y = self.query()
        self.query_time += time.time() - a
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
        if self.attribute1 == '*':
            self.attribute1 = '.'+self.attribute1
        if len(self.top_k) == 0:
            self.top_k[0] = (d,(self.func,self.attribute1,self.attribute2))
        elif len(self.top_k) < self.k:

            target = (d, (self.func,self.attribute1, self.attribute2))
            flg = -1
            for i, j in self.top_k.items():
                if j[0] < target[0]:
                    self.top_k[i] = target
                    target,flg = j,-1
            self.top_k[len(self.top_k)] = target
        else:
            target = (d,(self.func,self.attribute1,self.attribute2))
            for i,j in self.top_k.items():
                if j[0] < target[0]:
                    self.top_k[i] = target
                    target = j

    def visualization(self):
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
        plt.show()
        #plt.savefig('sample.png')

    def output(self):
        print('================================================================')
        print('順位, 乖離度, (集計関数, 集計属性, 集約属性)')
        print('================================================================')
        for i,j in self.top_k.items():
            print(i+1,j[0],j[1])
        print('================================================================')
        print('All_time:',time.time()-self.start)
        print('Query_time:',self.query_time)
        print('Calcu_deviance_time:',self.deviance_time)
        print('Sort_time:',self.sort_time)
        print('Visualization_time:',self.visualization_time)
        print('================================================================')


    def main(self):
        a = time.time()
        self.fullshare_query()
        self.query_time += time.time() - a
        self.roop()
        #self.visualization()
        #self.visualization_time = time.time() - a
        #self.output()

