# -*- coding: utf-8 -*-
from seedb import SeeDB
from fasionec import data

if __name__ == "__main__":
    #データベース関連の指定
    db,table,data_set = data()

    top_k = 10

    framework = SeeDB(db,data_set,table,top_k)
    framework.main()