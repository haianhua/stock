import pandas as pd
import tushare as ts
import numpy as np
import stock as sk
import re
import os
from lib.time import (strtime_today, strtime_by_range)

save_dir='./tick-data/'
begin_date='2019-05-01'

def get_path(date, code):
    return save_dir+date+'.'+code+'.csv'

def save_all_stock_tick_init(pro):
    tscodes=sk.get_tscodes(pro)
    for i in range(len(tscodes)):
        symbol=re.findall(r"\d+",tscodes[i])[0]
        ticks=sk.get_tick_data(symbol, '2019-02-01', '2019-09-09')
        print(ticks, type(ticks))
        for date in ticks: 
            if ticks[date] is not None:
                print(date)
                ticks[date].to_csv(tscodes[i]+'.csv')
        break

def save_all_stock_tick_update(pro):
    global save_path
    global begin_date
    today=strtime_today()
    date_ranges=strtime_by_range(begin_date, today)
    tscodes=sk.get_tscodes(pro)
    for i in range(len(tscodes)):
        for j in range(len(date_ranges)):
            date = date_ranges[j]
            save_path=get_path(date, tscodes[i])
            if os.path.exists(save_path) == False:
                name=re.findall(r"\d+",tscodes[i])[0]
                tick=sk.get_tick_data(name, date)
                if tick is not None: 
                    print(date, tscodes[i])
                    tick.to_csv(save_path)

if __name__=='__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    #save_all_stock_tick_init(pro)
    save_all_stock_tick_update(pro)

