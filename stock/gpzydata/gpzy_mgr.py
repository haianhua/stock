import requests
import json
import re

g_sort_types=[
    "scode", #股票代码 0
    "sname", #股票名字 1
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

def gen_url(type_index):
    global g_sort_types
    token=parse_token()
    sort_type=g_sort_types[0]
    html='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=ZD_QL_LB&token='+token+'&cmd=&st='+sort_type+'&sr=-1&p=1&ps=3&js=vartqeDNZJD={pages:(tp),data:(x),font:(font)}&filter=(tdate=%272019-09-12%27)&rt=52281468'
    content=requests.get(html).text
    b=content.find('data')+5
    e=content.find('font')-1
    c=content[b:e]
    #print(c)
    data = json.loads(c)
    #print(data)

    b=content.find('FontMapping')+13
    c=content[b:-2]
    print(c)
    data = json.loads(c)
    print(data)

gen_url(1)
