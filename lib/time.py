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
import os
import numpy as np

g_latest_date=None
def strtime_today():
    return datetime.date.today().strftime("%Y-%m-%d")

def strtime_by_range(date_b, date_e):
    begin=re.findall(r"\d+", date_b)
    begin=datetime.date(int(begin[0]),int(begin[1]),int(begin[2]))
    end=re.findall(r"\d+", date_e)
    end=datetime.date(int(end[0]),int(end[1]),int(end[2]))
    results=[]
    for i in range((end-begin).days+1):
        date = begin + datetime.timedelta(days=i)
        date=date.strftime("%Y-%m-%d")
        results.append(date)
    return results

def strtime_convert(date):
    begin=re.findall(r"\d+", date)
    return str(int(begin[0])*10000+int(begin[1])*100+int(begin[2]))

def strtime_anti_convert(date):
    if len(str(date))==8:
        date=str(date)
        return date[0:4]+'-'+date[4:6]+'-'+date[6:8]
    return str(date)

def strtime_delta_n_day(date_b, days):
    begin=re.findall(r"\d+", date_b)
    begin=datetime.date(int(begin[0]),int(begin[1]),int(begin[2]))
    date = begin + datetime.timedelta(days=days)
    date=date.strftime("%Y-%m-%d")
    return date

def strtime_latest_trade_date(date=None):
    if date is None:
        date=strtime_today()
    date=strtime_anti_convert(date)
    while True:
        html='http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page=1,sortRule=-1,sortType=,startDate='+date+',endDate='+date+',gpfw=0,js=var%20data_tab_2.html?rt=26142563'
        content=requests.get(html).text
        b=content.find('pages')+7
        count=int(content[b:b+1])
        if count != 0:
            return date
        date=strtime_delta_n_day(date, -1)

if __name__=='__main__':
    strtime_latest_trade_date()
