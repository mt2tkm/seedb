# -*- coding:utf-8 -*-
import time,math,numpy as np
from config import config_data
import matplotlib.pyplot as plt

class SeeDB:
    query_time,deviance_time,sort_time,visualization_time = 0,0,0,0

    def __init__(self, db, groupby, table, k, aggregate):
        self.cursor = config_data(db)
        self.groupby, self.table,self.k,self.aggregate = groupby, table, k, aggregate
        self.start = time.time()
        self.top_k = {}
        self.terms()

    def terms(self):
        self.where1,self.where2 = input('1つ目のwhere句を入力してください->'),input('2つ目のwhere句を入力してください->')

    def fullshare_query(self):
        g_b = str()
        for group in self.groupby:
            g_b += group + ', '
        select = 'select ' + g_b + ', '
        for agg in self.aggregate:
            select = select + 'sum(CAST(' + agg + ' AS BIGINT)), ' + 'count(' + agg + '), '
        select = select[:-2]
        
        full_query = select + 'from ' + self.table + ' group by ' + g_b[:-2] + ' order by ' + g_b[:-2]
        cur.execute(full_query)
        self.results = cur.fetchall()
        
        
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
        self.fullshare_query()
        
        a = time.time()
        #self.visualization()
        #self.visualization_time = time.time() - a
        #self.output()

