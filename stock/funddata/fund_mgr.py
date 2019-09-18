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
from bs4 import BeautifulSoup

root='/home/worker/stock/stock/'
g_page_count=10

#https://www.cnblogs.com/hjw1/p/8278170.html
#http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=161213&topline=10&year=&month=6&rt=0.3279408627843189
#http://fund.eastmoney.com/pingzhongdata/160632.js?v=20190919001912
#http://api.fund.eastmoney.com/F10/JJPJ/?callback=jQuery18306888443304534078_1568825132565&fundcode=260103&pageIndex=1&pageSize=50&_=1568825132663
#http://nufm3.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=0005682,6005191,6013181,6011551,0027272,0023042,6000361,0006512,3004982,6038991,&sty=E1OQCPZT&st=z&sr=&p=&ps=&cb=&js=var%20js_fav={favif:[%28x%29]}&token=8a36403b92724d5d1dd36dc40534aec5&rt=0.4202386646772137[

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
    print(list(map(str, data_list['datas'][1].split(','))))
if __name__ == "__main__":
    #download()

    content=requests.get('http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=161213&topline=10&year=&month=6&rt=0.3279408627843189').text
    soup=BeautifulSoup(content,"html.parser")
    s=soup.prettify()
    print(s)
