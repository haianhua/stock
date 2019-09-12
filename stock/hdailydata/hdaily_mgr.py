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
from lib.time import (strtime_today, strtime_by_range)

save_dir='./hdaily-data/'
g_start_date='20030501'
g_end_date='20190901'

def download(pro):
    tscodes=sk.get_tscodes(pro)
    for i in range(len(tscodes)):
        save_path=save_dir+tscodes[i]+".csv"
        if os.path.exists(save_path) == False:
            print(tscodes[i])
            df = ts.pro_bar(ts_code=tscodes[i], start_date=g_start_date, end_date=g_end_date, ma=[2,3,4,5,8,10,15,20],factors=['tor','vr'])
            df.to_csv(save_path)
        time.sleep(0.5)

if __name__=='__main__':
    ts.set_token('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    download(pro)
