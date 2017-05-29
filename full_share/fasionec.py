# -*- coding: utf-8 -*-
import pandas as pd

def data():
    db_name = 'FasionEC'

    table = "[Order] "
    table += "left outer join OrderDetail on [Order].注文番号 = [OrderDetail].注文番号 " + "left outer join Member2 on [Order].顧客番号 = [Member2].顧客番号 "
    table += "inner join Item on [OrderDetail].商品番号 = [Item].商品番号 AND [OrderDetail].商品詳細番号 = [Item].商品詳細番号 " + "left outer join Enquete on [Order].顧客番号 = [Enquete].顧客番号"

    groupby = (['[Item].商品カテゴリ大', '[Item].商品カテゴリ小', 'SUBSTRING(CONVERT(VARCHAR, [Order].注文日, 111), 1, 7)', '[Member2].アンケートフラグ','[Member2].年代', '[Order].予約FLG', '[OrderDetail].セール商品FLG', '[Item].ショップ番号', '[Member2].都道府県', '[Member2].性別', '[Item].商品詳細番号', '[Item].カラーカテゴリ', '[Item].サイズ', '[Item].ブランド番号', '[Order].購入時デバイス'])

    aggregate = ('[OrderDetail].注文金額','[OrderDetail].数量','[Order].注文時追加料金')

    return db_name, table, groupby, aggregate

if __name__ == '__main__':
    print(0)
