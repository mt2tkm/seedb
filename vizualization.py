import pandas as pd, matplotlib.pyplot as plt
import math
import numpy as np


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
    t = np.linspace(-np.pi, np.pi, 1000)
    
    x1 = np.sin(2*t)
    x2 = np.cos(2*t)
    x3 = x1 + x2

    fig,axes = plt.subplots(nrows=2,ncols=3,figsize=(10,8))
    
    axes[0,0].plot(t, x1, linewidth=2)
    axes[0,0].plot(t, x2, linewidth=2)
    axes[0,0].set_xticks([-1,0,1])
    axes[0,0].set_xticklabels(['A','B','C'])
    axes[0,0].set_title('sin')
    axes[0,0].set_xlabel('t')
    axes[0,0].set_ylabel('x')
    axes[0,0].set_xlim(-np.pi, np.pi)
    axes[0,0].grid(True)

    axes[0,1].plot(t, x2, linewidth=2)
    axes[0,1].set_title('cos')
    axes[0,1].set_xlabel('t')
    axes[0,1].set_ylabel('x')
    axes[0,1].set_xlim(-np.pi, np.pi)
    axes[0,1].grid(True)
    
    axes[0,2].plot(t, x2, linewidth=2)
    axes[0,2].set_title('cos')
    axes[0,2].set_xlabel('t')
    axes[0,2].set_ylabel('x')
    axes[0,2].set_xlim(-np.pi, np.pi)
    axes[0,2].grid(True)
    
    axes[1,0].plot(t, x3, linewidth=2)
    axes[1,0].set_title('sin+cos')
    axes[1,0].set_xlabel('t')
    axes[1,0].set_ylabel('x')
    axes[1,0].set_xlim(-np.pi, np.pi)
    axes[1,0].grid(True)

    axes[1,1].axis('off')
    axes[1,2].axis('off')

    plt.show()
