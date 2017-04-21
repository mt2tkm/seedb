import pandas as pd, matplotlib.pyplot as plt
import math
import numpy as np
from config import config_data
from fasionec import data

def visualization(self):
    n = math.ceil(np.sqrt(self.k))
    m = math.ceil(self.k/n)
    fig,axes = plt.subplots(nrows=n,ncols=m,figsize=(10,8))
    
    i,j = 0,0
    
    for dt in self.top_k.items():
        self.attribute1,self.attribute2,self.func = dt[1][1],dt[1][2],dt[1][0]
        data1,data2 = self.query()
        data1,data2 = self.nomalization(x),self.nomalization(y)
        
        x_agre = list()
        for i,j in data1+data2:
            if not i in x_agre:
                x_agre.append(i)
        
        t1,t2 = dict(data1),dict(data2)

        x,y1,y2 = list(),list(),list()
        
        x = [i for i in range(0,len(x_agre))]
        
        for i in x_agre:
            if i in t1:
                y1.append(t1[i])
            else:
                y1.append(0)
            if i in t2:
                y2.append(t2[i])
            else:
                y2.appen(0)
        
        axes[i,j].plot(x, y1, linewidth=2)
        axes[i,j].plot(x, y2, linewidth=2)
        
        axes[i,j].set_xticks(x)
        axes[i,j].set_xticklabels(x_agre, rotation=30)
        
        axes[i,j].set_title(' rank : ',dt[0],self.func,self.attribute1.split('.')[1])
        axes[i,j].set_xlabel(self.attiribute2)
        
        axes[i,j].grid(True)
        
        if j+1 == m-1:
            j = 0
            i +=1
        else:
            j +=1
    
    plt.show()
    

if __name__ == '__main__':
    db, table, data_set = data()
    cursor =config_data(db)
    query = 'select ' + '[Member2].都道府県' + ',' + 'sum' + '(' + 'CAST(' + '[OrderDetail].注文金額' + ' AS BIGINT' + '))' + ' from ' + table
    query += ' group by ' + '[Member2].都道府県' + ' order by ' + '[Member2].都道府県'

    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10, 8))
    m,n = 0,0
    for i in range(5):
        cursor.execute(query)
        data1 = cursor.fetchall()
        x_agre = list()
        for i, j in data1:
            if not i in x_agre:
                x_agre.append(i)
        t1,y1 = dict(data1),list()
        x = [i for i in range(0, len(x_agre))]
        for i in x_agre:
            if i in t1:
                y1.append(t1[i])
            else:
                y1.append(0)

        axes[m, n].plot(x, y1, linewidth=2)

        axes[m, n].set_xticks(x)
        axes[m, n].set_xticklabels(x_agre, rotation=30)

        #axes[m, n].set_title(' rank : ', dt[0], self.func, self.attribute1.split('.')[1])
        #axes[m, n].set_xlabel(self.attiribute2)

        axes[m, n].grid(True)
    plt.show()



