#!/usr/local/python3/bin/python3
import sys
sys.path.append("..")
import tushare as ts
import re
import datetime
import basicdata.basic_mgr as sk
import time
import os
import pandas as pd

g_update_newest=False #True|False
#是否下载最新的概念，一般不需要

g_ctcode_name=None
#g_ctcode_name['TS56']='电改'

g_tscode_concept=None
#g_tscode_concept['000008.SZ']={'id':['TS56','TS59'],'name':['电改','特斯拉']}

def get_ctname_by_tscode(pro, tscode):
    global g_tscode_concept
    if g_tscode_concept is None:
        init_tscode_concept(pro)
    return g_tscode_concept[tscode]['name']

def get_ctcode_by_tscode(pro, tscode):
    global g_tscode_concept
    if g_tscode_concept is None:
        init_tscode_concept(pro)
    return g_tscode_concept[tscode]['id']

def init_tscode_concept(pro):
    global g_tscode_concept
    global g_update_newest
    if g_tscode_concept is None:
        g_tscode_concept = {}
        ts_codes=sk.get_tscodes(pro)
        for i in range(len(ts_codes)):
            ts_code=ts_codes[i]
            path='./concept-data/'+ts_code+'.concept.csv'
            if g_update_newest == False and os.path.exists(path) == True:
                conceptdf=pd.read_csv(path)
            else:
                conceptdf=pro.concept_detail(ts_code=ts_code)
                if conceptdf is not None:
                    conceptdf.to_csv(path)
                time.sleep(1)
                print("download", path)
            if conceptdf is not None:
                conceptids=conceptdf['id'].values.tolist()
                conceptnames=conceptdf['concept_name'].values.tolist()
                g_tscode_concept[ts_code]={'id':conceptids, 'name':conceptnames}


def get_concept_map(pro):
    global g_ctcode_name
    if g_ctcode_name is None:
        init_ctcode_name(pro)
    return g_ctcode_name

def get_name(pro, code):
    global g_ctcode_name
    if g_ctcode_name is None:
        init_ctcode_name(pro)
    return g_ctcode_name[code]

def init_ctcode_name(pro):
    global g_ctcode_name
    if g_ctcode_name is None:
        g_ctcode_name = {}
        conceptdf=pro.concept(src='ts')
        conceptcodes=conceptdf['code'].values.tolist()
        conceptnames=conceptdf['name'].values.tolist()
        for i  in range(len(conceptcodes)):
            g_ctcode_name[conceptcodes[i]]= conceptnames[i]

if __name__== '__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    init_ctcode_name(pro)
    print(g_ctcode_name)
    print(get_name(pro, 'TS2'))
    print(get_ctcode_by_tscode(pro, '600848.SH'))
    #conceptdf.to_csv('./concept.csv')
