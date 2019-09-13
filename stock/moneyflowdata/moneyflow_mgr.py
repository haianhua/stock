#!/usr/local/python3/bin/python3
import sys
sys.path.append("..")
sys.path.append("../..")
import tushare as ts
import re
import datetime
import basicdata.basic_mgr as sk
import time
import os
import pandas as pd
from lib.time import (strtime_convert, strtime_delta_n_day)

save_dir='./moneyflow-data/'
g_start_date='2014-01-01'

def download(pro):
    global g_start_date
    temp_start_date=g_start_date
    start_flag=False
    while True:
        start_date=temp_start_date
        end_date=strtime_delta_n_day(start_date, 300)
        df=pro.moneyflow_hsgt(start_date=strtime_convert(start_date), end_date=strtime_convert(end_date))
        if start_flag==True and df.empty == True:
            break
        temp_start_date=strtime_delta_n_day(start_date, 301)
        if df.empty == False:
            start_flag=True
            path=save_dir+start_date+".csv"
            df.to_csv(path)
    
if __name__ =='__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    download(pro)
