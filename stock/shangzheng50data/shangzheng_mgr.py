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

def get_url():
    return 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C.BK06111&type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=50&js=var%20xoZLmiIR={pages:(pc),data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITA&rt=52284426'

def download():
    html=get_url()
    content=requests.get(html).text
    #print(content)
    b=content.find('data')+5
    data_str=content[b:-1]
    data_dict=json.loads(data_str)
    #print(data_dict)
    print(data_dict[0])

    je=0
    for i in range(len(data_dict)):
        je=je+float(list(map(str, data_dict[i].split(',')))[5]) * 10000
    print(je)

if __name__=="__main__":
    download()
