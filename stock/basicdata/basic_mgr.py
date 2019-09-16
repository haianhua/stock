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
from lib.common import (formatcode)

root='/home/worker/stock/stock/'
basic_datas=None
#names
codes=None

#http://quote.eastmoney.com/center/gridlist.html#hs_a_board
def get_url(): 
    return 'http://84.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405101567698142537_1568522603227&pn=1&pz=4000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1568522603239'



def gen_df(diff_list):
    from fenhongdata.fenhong_mgr import (get_xjfh)
    key_list=list(diff_list[0].keys())
    key_list.append('gxl')
    values_dict={}
    for i in range(len(diff_list)):
        for j in range(len(key_list)):
            key=key_list[j]
            if key not in values_dict:
                values_dict[key]=[]
            if key=='f12':                
                diff_list[i]['f12']=formatcode(str(diff_list[i]['f12']))
            value=0
            if key=='gxl':
                xjfh=get_xjfh(2019,diff_list[i]['f12'])
                if diff_list[i]['f2'] == '-':
                    #退市了
                    diff_list[i]['f2'] = 0
                elif float(diff_list[i]['f2']) != 0:
                    value=xjfh/float(diff_list[i]['f2'])
                else:
                    print(diff_list[i]['f12'])
            elif key=='市盈动':
                if diff_list[i]['市盈动'] == '-':
                    diff_list[i]['市盈动'] = 0
            else: 
                value=diff_list[i][key]
            array=values_dict[key]
            array.append(value)

    df=pd.DataFrame.from_dict(values_dict)
    df['市盈动']=df['市盈动'].astype('float64')
    return df

def convert_for_read(diff_list):
    font={
    'f115':'市盈率',
    'f62':'主力净流入',
    'f25':'f25',
    'f24':'f24',
    'f23':'市净率',
    'f21':'总市值',
    'f20':'流通市值',
    'f18':'昨天收盘价',
    'f17':'今日开盘价', 
    'f16':'今日最低价',
    'f15':'今日最高价',
    'f14':'名字',
    #'f12':'代号',
    'f12':'f12',
    'f10':'量比',
    'f9':'市盈动',
    'f8':'换手',
    'f7':'f7',
    'f6':'成交额',
    'f5':'成交量',
    'f4':'价格变动',
    'f3':'今日涨幅',
    #'f2':'收盘价',
    'f2':'f2',
    'f1':'f1',
    'f11':'f11',
    'f13':'f13',
    'f22':'f22',
    'f128':'f128',
    'f140':'f140',
    'f141':'f141',
    'f136':'f136',
    'f152':'f152',
    'gxl':'gxl',
    }
    convert_list=[]
    key_list=list(diff_list[0].keys())
    for i in range(len(diff_list)):
        diff_item=diff_list[i]
        new_item={}
        for j in range(len(key_list)):
            key=key_list[j]
            new_item[font[key]]=diff_item[key]
        convert_list.append(new_item)
    return convert_list

def save_for_read(diff_list):
    global root
    convert_list=convert_for_read(diff_list)
    df=gen_df(convert_list)
    df.to_csv(root+'basicdata/basic-data/basic_for_read.csv')
    return df

def save_for_analysis(diff_list):
    global root
    df=gen_df(diff_list)
    df.to_csv(root+'basicdata/basic-data/basic_for_analysis.csv')

def download():
    html=get_url()
    content=requests.get(html).text
    #print(content)
    b=content.find('(')+1
    e=content.find(')')
    data_str=content[b:e]
    data_dict=json.loads(data_str)
    diff_list=data_dict['data']['diff']
    df=save_for_read(diff_list)
    save_for_analysis(diff_list)
    return df

def sort_by_gxl(df=None):
    if df==None:
        df=download()
    sort_df=df.sort_values(by='gxl', ascending=False)
    sort_df.to_csv(root+'basicdata/basic-data/sort_by_gxl.csv')

def sort_by_syl(df=None):
    if df==None:
        df=download()
    sort_df=df.sort_values(by='市盈动', ascending=False)
    sort_df.to_csv(root+'basicdata/basic-data/sort_by_syl.csv')

if __name__== '__main__':
    #pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    #print(get_tscodes(pro))
    #data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    #print(data, type(data))
    #print(pro.concept_detail(id='TS2'))
    #sort_by_gxl()
    sort_by_syl()
