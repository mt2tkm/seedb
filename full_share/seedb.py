# -*- coding:utf-8 -*-
import time,math,numpy as np
from config import config_data
import matplotlib.pyplot as plt
import pandas as pd

class SeeDB:
    query_time,calc_time,visualization_time = 0,0,0

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
        # make fullshare_query
        g_b = str()
        for group in self.groupby:
            g_b += group + ', '
        select = 'select ' + g_b
        for agg in self.aggregate:
            select = select + 'sum(CAST(' + agg + ' AS BIGINT)) AS ' + agg.split('.')[1] + ', '
        select = select[:-2]
        full_query = select + ' from ' + self.table + ' group by ' + g_b[:-2] + ' order by ' + g_b[:-2]
        #print(full_query)
        # execute fullshare_query and put in DataFrame
        self.df = pd.io.sql.read_sql(full_query,self.con)

    def roop(self):
        df1 = self.df
        for i in range(len(self.groupby)):
            # whether terms match group-by column
            if self.column1 != df1.columns[i] and self.column2 != df1.columns[i]:
                dt1, dt2 = pd.DataFrame(), pd.DataFrame()
                if self.column1 != '':
                    dt1 = df1[df1[self.column1] == self.where1].groupby(df1.columns[i]).sum().iloc[:,-3:]
                else:
                    dt1 = df1.groupby(df1.columns[i]).sum().iloc[:, -3:]
                if self.column2 != '':
                    dt2 = df1[df1[self.column2] == self.where2].groupby(df1.columns[i]).sum().iloc[:, -3:]
                else:
                    dt2 = df1.groupby(df1.columns[i]).sum().iloc[:, -3:]
                """
                dt1['平均注文金額'] = [dt1.ix[pp, -3] / dt1.ix[pp, -2] for pp in range(len(dt1.ix[:, -2]))]
                dt2['平均注文金額'] = [dt2.ix[pp, -3] / dt2.ix[pp, -2] for pp in range(len(dt2.ix[:, -2]))]
                
                dt1['平均注文時追加金額'] = [dt1.ix[pp, 2] / dt1.ix[pp, 1] for pp in range(len(dt1.ix[:, 1]))]
                dt2['平均注文時追加金額'] = [dt2.ix[pp, 2] / dt2.ix[pp, 1] for pp in range(len(dt2.ix[:, 1]))]
                """
                #dt1.to_csv('test.csv')
                # z_nomalization phase
                n_dt1, n_dt2 = (dt1 - dt1.mean())/dt1.std(), (dt2 - dt2.mean())/dt2.std()
                dev_df = np.fabs(n_dt1 - n_dt2)

                # top-k chaek phase
                for xx in range(len(dev_df.columns)):
                    self.cheak(dev_df.ix[:,xx].sum(),dev_df.columns[xx],df1.columns[i])

            else:
                pass

    """
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
    """

    def cheak(self,dev,y_axis,x_axis):
        z = (dev,x_axis,y_axis)
        if len(self.top_k)== 0:
            self.top_k[0] = z
        elif len(self.top_k) < self.k:
            for i,j in self.top_k.items():
                if j[0] < z[0]:
                    self.top_k[i] = z
                    z = j
            self.top_k[len(self.top_k)] = z
        else:
            for i,j in self.top_k.items():
                if j[0] < z[0]:
                    self.top_k[i] = z
                    z = j

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
            print(i+1,j[0],j[1],j[2])
        print('================================================================')
        print('All_time:',time.time()-self.start)
        print('Query_time:',self.query_time)
        print('Calculate_time:',self.calc_time)
        print('Visualization_time:',self.visualization_time)
        print('================================================================')


    def main(self):
        # query phase
        a = time.time()
        self.fullshare_query()
        self.query_time = time.time() - a
        # calculate phase
        a = time.time()
        self.roop()
        self.calc_time = time.time() - a
        """
        # visualization phase
        a = time.time()
        self.visualization()
        self.visualization_time = time.time() - a
        """
        # output phase
        self.output()

