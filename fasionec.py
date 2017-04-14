# -*- coding: utf-8 -*-

def data():
    db_name = 'FasionEC'

    table = "[Order] "
    table += "left outer join OrderDetail on [Order].注文番号 = [OrderDetail].注文番号 " + "left outer join Member2 on [Order].顧客番号 = [Member2].顧客番号 "
    table += "inner join Item on [OrderDetail].商品番号 = [Item].商品番号 AND [OrderDetail].商品詳細番号 = [Item].商品詳細番号 " + "left outer join Enquete on [Order].顧客番号 = [Enquete].顧客番号"

    data_set = {}

    return db_name,table,data_set
