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
    data_str=data_str.replace('GXL', '股息率(%)')
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
    data_str=data_str.replace('NoticeDate', '最新公告日期')

    data_list = json.loads(data_str)
    seria_data={}
    key_list=list(data_list[0].keys())
    for i in range(len(data_list)):
        for j in range(len(key_list)):
            key=key_list[j]
            if key not in seria_data:
                seria_data[key]=[]
            array=seria_data[key]
            array.append(data_list[i][key])

    data_pd=pd.DataFrame.from_dict(seria_data)
    data_pd.to_csv('./fenhong-data/'+str(page)+'fenhong.csv')

def download_all_page():
    global g_page_count
    for page in range(1, g_page_count+1):
        print("downloading page:", page)
        html=gen_url(page)
        download(page,html)
        #time.sleep(2)

if __name__ == "__main__":
    download_all_page()
