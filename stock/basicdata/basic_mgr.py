#!/usr/local/python3/bin/python3
import tushare as ts
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
from lib.common import (_code_to_symbol)

root='/home/worker/stock/stock/'
basic_datas=None
#names
codes=None

#http://quote.eastmoney.com/center/gridlist.html#hs_a_board
def get_url(): 
    return 'http://84.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405101567698142537_1568522603227&pn=1&pz=4000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1568522603239'


g_name_convert={
    'f115':'市盈率',
    'f62':'主力净流入',
    'f25':'f25',
    'f24':'f24',
    'f23':'市净率',
    'f21':'流通市值',
    'f20':'总市值',
    'f18':'昨天收盘价',
    'f17':'今日开盘价', 
    'f16':'今日最低价',
    'f15':'今日最高价',
    'f14':'名字',
    'f12':'代号',
    'f10':'量比',
    'f9':'市盈动',
    'f9':'f9',
    'f8':'换手',
    'f7':'f7',
    'f6':'成交额',
    'f5':'成交量',
    'f4':'价格变动',
    'f3':'今日涨幅',
    'f2':'收盘价',
    'f1':'f1',
    'f11':'f11',
    'f13':'f13',
    'f22':'f22',
    'f128':'f128',
    'f140':'f140',
    'f141':'f141',
    'f136':'f136',
    'f152':'f152',
    'gxl':'股息率',
}

def gen_df(dataslist):
    from fenhongdata.fenhong_mgr import (get_xjfh)
    column_names=list(dataslist[0].keys())
    column_names.append('gxl')
    columnname_values={}
    for i in range(len(dataslist)):
        itemdata=dataslist[i]
        code=str(itemdata['f12'])
        close=itemdata['f2']
        for j in range(len(column_names)):
            column_name=column_names[j]
            if column_name not in columnname_values:
                columnname_values[column_name]=[]
            if column_name=='f12':                
                itemdata['f12']=_code_to_symbol(code)
            value=0
            if column_name=='gxl':
                xjfh=get_xjfh(2019,code)
                if close == '-': #退市了
                    itemdata['f2'] = 0
                elif float(close) != 0:
                    value=xjfh/float(close)
            else:
                value=dataslist[i][column_name]
            array=columnname_values[column_name]
            array.append(value)

    df=pd.DataFrame.from_dict(columnname_values)
    df=df.replace("-", 0)
    for j in range(len(column_names)):
        column_name=column_names[j]
        if column_name!= 'f12' and column_name!= 'f14':
            df[column_name]=df[column_name].astype(float)
    return df

def save_for_read(diff_list):
    global root
    df=gen_df(diff_list)
    readdf=df.rename(columns=g_name_convert, inplace=False)
    readdf.to_csv(root+'basicdata/basic-data/basic_for_read.csv')
    return readdf

def save_for_analysis(diff_list):
    global root
    df=gen_df(diff_list)
    df.to_csv(root+'basicdata/basic-data/basic_for_analysis.csv')
    return df

def download():
    html=get_url()
    content=requests.get(html).text
    #print(content)
    b=content.find('(')+1
    e=content.find(')')
    data_str=content[b:e]
    data_dict=json.loads(data_str)
    diff_list=data_dict['data']['diff']
    save_for_read(diff_list)
    df=save_for_analysis(diff_list)
    return df

def sort_by_gxl(df=None):
    if df==None:
        df=download()
    sort_df=df.sort_values(by='gxl', ascending=False)
    sort_df.to_csv(root+'basicdata/basic-data/sort_by_gxl.csv')

def sort_by_syl(df=None):
    if df==None:
        df=download()
    sort_df=df.sort_values(by='f9', ascending=False)
    sort_df.to_csv(root+'basicdata/basic-data/sort_by_syl.csv')


#闭区间 单位亿
def get_by_shizhi(min_value, max_value, df=None):
    if df==None:
        df=download()
    min_value=min_value*100000000
    max_value=max_value*100000000
    shizhidf=df[(df['f20']>=min_value) & (df['f20']<=max_value) ].to_csv('./temp1.csv')
    return shizhidf

#闭区间 
def filter_by_columns(columns_name, min_value, max_value, df=None):
    if df==None:
        df=download()
    filterdf=df[(df[columns_name]>=min_value) & (df[columns_name]<=max_value) ]#.to_csv('./temp1.csv')
    filterdf.to_csv("./temp2.csv")
    return filterdf

if __name__== '__main__':
    #pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    #print(get_tscodes(pro))
    #data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    #print(data, type(data))
    #print(pro.concept_detail(id='TS2'))
    #sort_by_gxl()
    #sort_by_syl()
    get_by_shizhi(10, 12)
    filter_by_columns('f20', 1000000000, 1200000000)
