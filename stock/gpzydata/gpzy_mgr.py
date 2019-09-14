#!/usr/local/python3/bin/python3
import requests
import datetime
import pandas as pd
import json
import re
import sys
sys.path.append("..")
sys.path.append("../..")
from lib.time import (strtime_convert, strtime_delta_n_day)

g_sort_types=[
    "scode", #代码 0
    "sname", #名称 1
    "tdate", #日期 2
    "hy", #行业 3
    "amtshareratio",#质押比例 4
    "bballowance",#质押股数 5
    "zysz",#质押市值 6
    "amtsharenum",#质押笔数 7
    "bbyallowance",#无限售股质押数 8
    "bbwallowance",#限售股质押数 9
    "zdf"#近年来涨跌幅 10
]

def parse_token():
    response=requests.get('http://data.eastmoney.com/gpzy/pledgeRatio.aspx').text
    b=response.find('token')+6
    e=response.find('token')+38
    return response[b:e]

def gen_url():
    global g_sort_types
    token=parse_token()
    sort_type=g_sort_types[2]
    #html='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=ZD_QL_LB&token='+token+'&cmd=&st='+sort_type+'&sr=-1&p=1&ps=50000&js=vartqeDNZJD={pages:(tp),data:(x),font:(font)}&filter=(tdate=%272019-09-12%27)&rt=52281468'
    html='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=ZD_QL_LB&token='+token+'&cmd=&st='+sort_type+'&sr=-1&p=1&ps=50000&js=vartqeDNZJD={pages:(tp),data:(x),font:(font)}&rt=52281468'
    return html

def gen_date_url(date):
    global g_sort_types
    token=parse_token()
    sort_type=g_sort_types[2]
    html='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=ZD_QL_LB&token='+token+'&cmd=&st='+sort_type+'&sr=-1&p=1&ps=4000&js=vartqeDNZJD={pages:(tp),data:(x),font:(font)}&filter=(tdate=%27'+date+'%27)&rt=52281468'
    return html

def gen_latest_content():
    temp_date=datetime.date.today().strftime("%Y-%m-%d")
    while True:
        date=temp_date
        html=gen_date_url(date)
        content=requests.get(html).text
        print(type(content), len(content))
        if len(content)!=84:
            return content
        temp_date=strtime_delta_n_day(date, -1)

def download():
    content=gen_latest_content()
    b=content.find('data')+5
    e=content.find('font')-1
    data_str=content[b:e]
    #print(data_str)
    data = json.loads(data_str)
    #print(data)

    b=content.find('FontMapping')+13
    code_str=content[b:-2]
    #print(code_str)
    code_list = json.loads(code_str)
    #print(code_list)
    for i in range(len(code_list)):
        code=code_list[i]['code']
        value=str(code_list[i]['value'])
        data_str = data_str.replace(code, value)
    #print(data_str)
    data_list = json.loads(data_str)
    scode=[]
    sname=[]
    tdate=[]
    hy=[]
    blfb=[]
    amtshareratio=[]
    bballowance=[]
    zysz=[]
    amtsharenum=[]
    bbyallowance=[]
    bbwallowance=[]
    zdf=[]

    for i in range(len(data_list)):
        scode.append(data_list[i]['scode'])
        sname.append(data_list[i]['sname'])
        tdate.append(data_list[i]['tdate'])
        hy.append(data_list[i]['hy'])
        blfb.append(data_list[i]['blfb'])
        amtshareratio.append(data_list[i]['amtshareratio'])
        bballowance.append(data_list[i]['bballowance'])
        zysz.append(data_list[i]['zysz'])
        amtsharenum.append(data_list[i]['amtsharenum'])
        bbyallowance.append(data_list[i]['bbyallowance'])
        bbwallowance.append(data_list[i]['bbwallowance'])
        zdf.append(data_list[i]['zdf'])
    #print(scode)
    #print(sname)
    data = {
        '代码':scode, 
        '名称':sname, 
        '行业':hy, 
        '质押比例(%)':amtshareratio, 
        '质押股数(万股)':bballowance,
        '质押市值(亿元)':zysz,
        '质押笔数':amtsharenum,
        '无限售股质押数(股)':bbyallowance,
        '限售股质押数(股)':bbwallowance,
        '近年来涨跌幅(%)':zdf,
        '日期':tdate
    }
    data_pd=pd.DataFrame.from_dict(data)
    data_pd.to_csv('./gpzy-data/gpzy.csv')

if __name__=='__main__':
    download()
