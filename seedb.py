# -*- coding:utf-8 -*-
import time,math
from config import config_data
#import matplotlib.pyplot as plt

class SeeDB:
    query_time,deviance_time,sort_time = 0,0,0

    def __init__(self, db,data_set,table,k):
        self.cursor = config_data(db)
        self.data_set, self.table,self.k = data_set, table, k
        self.start = time.time()
        self.top_k = {}
        self.terms()

    def terms(self):
        self.where1,self.where2 = input('1つ目のwhere句を入力してください->'),input('2つ目のwhere句を入力してください->')

    def query(self):
        query1 = 'select ' + self.attribute2 +',' + self.func + '(' + self.attribute1 + ')' + ' from ' + self.table
        if self.where1 != '':
            query1 += ' where ' + self.where1
        query1 += ' group by ' + self.attribute2 + ' order by ' + self.attribute2

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
        a = time.time()
        x,y = self.query()
        self.query_time += time.time() - a
        deviance = 0

        a = time.time()
        x,y = self.nomalization(x),self.nomalization(y)

        if len(x) == len(y):
            for i in range(len(x)):
                deviance += math.fabs(x[i][1]-y[i][1])

        self.deviance_time += time.time()-a

        return deviance

    def cheak_k(self,d):
        if len(self.top_k) == 0:
            self.top_k[0] = (d,(self.func,self.attribute1.split('.')[1],self.attribute2.split('.')[1]))
        elif len(self.top_k) < self.k:
            target = (d, (self.func,self.attribute1.split('.')[1], self.attribute2.split('.')[1]))
            flg = -1
            for i, j in self.top_k.items():
                if j[0] > target[0]:
                    self.top_k[i] = target
                    target,flg = j,-1
            self.top_k[len(self.top_k)] = target
        else:
            target = (d,(self.func,self.attribute1.split('.')[1],self.attribute2.split('.')[1]))
            for i,j in self.top_k.items():
                if j[0] > target[0]:
                    self.top_k[i] = target
                    target = j

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
        print('================================================================')

    def main(self):
        self.attribute1, self.attribute2, self.func = '[member2].顧客番号', '[member2].都道府県', 'count'
        for i in range(5):
            d = self.distance()

            if i %2 == 0:
                d += i/40
            else:
                d -= i/40

            a = time.time()
            self.cheak_k(d)
            self.sort_time += time.time() - a

            #print('time:',time.time()-self.start)

        self.output()

