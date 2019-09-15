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

g_page_count=10

#原始网页:http://data.eastmoney.com/yjfp/

def gen_url(page):
    #return 'http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?js=var%20SjkvdbeI&pagesize=3045&page='+str(page)+'&sr=-1&sortType=YAGGR&mtk=%C8%AB%B2%BF%B9%C9%C6%B1&rt=52282319'
    #return 'http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?js=var%20SjkvdbeI&pagesize=3045&page=3&sr=-1&sortType=YAGGR&mtk=%C8%AB%B2%BF%B9%C9%C6%B1&rt=52282319'
    return 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=DCSOBS&token=70f12f2f4f091e459a279469fe49eca5&p='+str(page)+'&ps=3045&sr=-1&st=YAGGR&filter=&cmd='

def download(page, html):
    content=requests.get(html).text
    #print(content)
    b=content.find('[')
    e=content.find(']')+1
    data_str=content[b:e]
    data_str=data_str.replace('MarketType', '市场')
    data_str=data_str.replace('Code', '代码')
    data_str=data_str.replace('Name', '名称')
    data_str=data_str.replace('SZZBL', '送转总比例')
    data_str=data_str.replace('SGBL', '送股比例')
    data_str=data_str.replace('ZGBL', '转股比例')
    data_str=data_str.replace('XJFH', '现金分红比例')
    data_str=data_str.replace('GXL', '股息率')
    data_str=data_str.replace('YAGGR', '预案公告日')
    #data_str=data_str.replace('YAGGRHSRZF', '')
    #data_str=data_str.replace('GQDJRQSRZF', '')
    data_str=data_str.replace('GQDJR', '股权登记日')
    data_str=data_str.replace('CQCXR', '除权除息日')
    #data_str=data_str.replace('CQCXRHSSRZF', '')
    #data_str=data_str.replace('YCQTS', '')
    data_str=data_str.replace('TotalEquity', '总股本(亿）')
    data_str=data_str.replace('EarningsPerShare', '每股收益(元)')
    data_str=data_str.replace('NetAssetsPerShare', '每股净资产(元)')
    data_str=data_str.replace('MGGJJ', '每股公积金(元)')
    data_str=data_str.replace('MGWFPLY', '每股未分配利润(元)')
    data_str=data_str.replace('JLYTBZZ', '净利润同比增长(%)')
    data_str=data_str.replace('ReportingPeriod', '报告期')
    data_str=data_str.replace('ResultsbyDate', '业绩披露日期')
    data_str=data_str.replace('ProjectProgress', '方案进度')
    data_str=data_str.replace('AllocationPlan', '分配计划')
    #data_str=data_str.replace('NOTICEDATE', '最新公告日期')
    

    data_list = json.loads(data_str)
    seria_data={}
    key_list=list(data_list[0].keys())
    for i in range(len(data_list)):
        for j in range(len(key_list)):
            key=key_list[j]
            if key not in seria_data:
                seria_data[key]=[]
            array=seria_data[key]
            if key=='预案公告日':
                year=19910101
                if len(re.findall(r"\d+", data_list[i][key]))==0:
                    year=19910101
                else:
                    t=re.findall(r"\d+", data_list[i][key])
                    year=int(t[0])*10000+int(t[1])*100+int(t[2])
                data_list[i][key]=year
            if key=='代码':
                if data_list[i]['市场']=='沪市':
                    data_list[i][key]=str(data_list[i][key])+'.SH'
                else:
                    data_list[i][key]=str(data_list[i][key])+'.SZ'
            array.append(data_list[i][key])

    df=pd.DataFrame.from_dict(seria_data)
    if page==1:
        df.to_csv('./fenhong-data/fenhong.csv')
    else:
        df.to_csv('./fenhong-data/fenhong.csv', mode='a', header=None)

def download_all_page():
    global g_page_count
    for page in range(1, g_page_count+1):
        print("downloading page:", page)
        html=gen_url(page)
        download(page,html)
        #time.sleep(2)

def get_since_year(year):
    if os.path.exists('./fenhong-data/fenhong.csv') == False:
        download_all_page()
    df=pd.read_csv('./fenhong-data/fenhong.csv')
    crit_year_1=df['预案公告日']>= year*10000
    crit_year_2=df['预案公告日']<= year*10000+12*100+29
    get_field=['代码','名称','股息率','送转总比例','送股比例','转股比例','现金分红比例','预案公告日','市场']
    year_df=df.loc[crit_year_1&crit_year_2, get_field]
    return year_df

g_year_xjfh={}
def load_xjfh(year):
    year_df=get_since_year(year)
    codes=year_df['代码'].tolist()
    xjfhs=year_df['现金分红比例'].tolist()
    moneys={}
    for i in range(len(codes)):
        code=codes[i]
        if code not in moneys:
            moneys[code]=0
        if xjfhs[i] == '-': 
            xjfhs[i]=0
        moneys[code] = moneys[code]+float(xjfhs[i])
    g_year_xjfh[year]=moneys

def get_xjfh(year, code):
    global g_year_xjfh
    if g_year_xjfh[year] is None
        load_xjfh(year)
    return g_year_xjfh[year][code]

#股息率
def sort_by_GXL(year=2019):
    year_df=get_since_year(year)
    sort_df=year_df.sort_values(by='股息率', ascending=False)
    #print(sort_df)
    sort_df.to_csv('./fenhong-data/'+str(year)+'_sort_by_gxl.csv')
    return sort_df

def compare_today_2():
    sort_df=sort_by_GXL(year=2018)
    codes=sort_df['代码'].tolist()
    xjfhs=sort_df['现金分红比例'].tolist()
    moneys={}
    for i in range(len(codes)):
        code=codes[i]
        if code not in moneys:
            moneys[code]=0
        if xjfhs[i] == '-': 
            xjfhs[i]=0
        moneys[code] = moneys[code]+float(xjfhs[i])

    gxl=[]
    for i in range(len(codes)):
        code=codes[i]
        now_price=get_price(code, '20190830')['close']*10
        gxl.append(moneys[code]/now_price)
        print(code, moneys[code]/now_price)
    df=pd.DataFrame.from_dict({'codes':codes, 'gxl':gxl})
    sort_df=df.sort_values(by='gxl', ascending=False)
    sort_df.to_csv('./fenhong-data/now_sort_by_gxl.csv')


def compare_today():
    sort_df=sort_by_GXL(year=2018)
    codes=sort_df['代码'].tolist()
    markets=sort_df['市场'].tolist()
    dates=sort_df['预案公告日'].tolist()
    for i in range(len(codes)):
        code=codes[i]
        h=get_price(code,dates[i])['close']
        date_h=get_price(code,dates[i])['date']
        n=get_price(code,'20190830')['close']
        date_n=get_price(code,'20190830')['date']
        print(code, date_h, h, date_n, n)
        if i == 50:
            break


if __name__ == "__main__":
    #download_all_page()
    #sort_by_GXL(2019)
    #sort_by_GXL(2018)
    #sort_by_GXL(2017)
    #sort_by_GXL(2016)
    #sort_by_GXL(2015)
    #sort_by_GXL(2014)
    compare_today_2()
