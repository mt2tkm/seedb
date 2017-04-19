import pandas as pd, numpy, math

def nomarization(self,dt):
    """〜正規化の種類を増やす〜
        avg の際の正規化の作成

        問題点；正規化の手法の違いから生じる距離の差
    """
    


    print(2)

def calc(self):
    a = time.time()
    x,y = self.query()
    self.query_time += time.time() - a
    deviance = 0

    a = time.time()
    x,y = self.nomalization(x),self.nomalization(y)

    """〜距離計算部分の改良〜

        長さが違う場合？
        x 座標の抜け漏れがある場合？
    if len(x) == len(y):
        deviance = 0
        for i in range(len(x)):
            deviance += math.fabs(x[i][1]-y[i][1])
    """
    
    dd = dict()
    for i,j in x:
        dd[i] = j
    for i,j in y:
        if i in dd:
            dd[i] = math.fabs(dd[i] - j)
        else:
            dd[i] = j

    for x,dis in dd.items():
        deviance += dis
    
    
    
    self.deviance_time += time.time() - a
    return deviance
