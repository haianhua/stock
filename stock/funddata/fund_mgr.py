#!/usr/local/python3/bin/python3
import requests
import datetime
import pandas as pd
import json
import re
import sys
import time
sys.path.append("..")
sys.path.append("../..")
from lib.time import (strtime_convert, strtime_delta_n_day)
from hdailydata.hdaily_mgr import (get_price)
import os
import numpy as np

root='/home/worker/stock/stock/'
g_page_count=10

#原始网页:http://fund.eastmoney.com/fundguzhi.html
def get_url():
    return 'http://fund.eastmoney.com/data/FundGuideapi.aspx?dt=0&sd=&ed=&sc=z&st=desc&pi=1&pn=8000&zf=diy&sh=list&rnd=0.7802489924781851'

def download():
    html=get_url()
    content=requests.get(html).text
    #print(content)
    b=content.find('{')
    data_str=content[b:]
    data_list = json.loads(data_str)
    print(len(data_list['datas']))
    print(data_list['datas'][0])
    print(list(map(str, data_list['datas'][5000].split(','))))
if __name__ == "__main__":
    download()
