# -*- coding: utf-8 -*-
from seedb import SeeDB
from fasionec import data

if __name__ == "__main__":
    #データベース関連の指定
    db,table,groupby,aggregate = data()

    top_k = 10

    framework = SeeDB(db,groupby,table,top_k,aggregate)
    framework.main()