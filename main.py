import pandas as pd
import tushare as ts
import numpy as np
import stock as sk
import re


def save_all_stock_tick_init(pro):
    codes=sk.get_codes(pro)
    for i in range(len(codes)):
        symbol=re.findall(r"\d+",codes[i])[0]
        ticks=sk.get_tick_data(symbol, '2019-02-01', '2019-09-09')
        for date in ticks: 
            print(date)
            ticks[date].to_csv(codes[i]+'.csv')

#def save_all_stock_tick_update(pro):

if __name__=='__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    save_all_stock_tick_init(pro)

