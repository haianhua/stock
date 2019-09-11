#!/usr/local/python3/bin/python3
import sys
sys.path.append("..")
import tushare as ts
import re
import datetime
import basicdata.basic_mgr as sk

ctcode_name=None
#ctcode_name['TS56']='电改'
tscode_concept=None
#tscode_concept['000008.SZ']={'id':['TS56','TS59'],'name':['电改','特斯拉']}

def get_ctname_by_tscode(pro, tscode):
    global tscode_concept
    if tscode_concept is None:
        init_tscode_concept(pro)
    return tscode_concept[tscode]['name']

def get_ctcode_by_tscode(pro, tscode):
    global tscode_concept
    if tscode_concept is None:
        init_tscode_concept(pro)
    return tscode_concept[tscode]['id']

def init_tscode_concept(pro):
    global tscode_concept
    if tscode_concept is None:
        tscode_concept = {}
        ts_codes=sk.get_tscodes(pro)
        for i in range(len(ts_codes)):
            ts_code=ts_codes[i]
            conceptdf=pro.concept_detail(ts_code=ts_code)
            if conceptdf is not None:
                conceptdf.to_csv('./concept-data/'+ts_code+'.concept.csv')
                conceptids=conceptdf['id'].values.tolist()
                conceptnames=conceptdf['concept_name'].values.tolist()
                tscode_concept[ts_code]={'id':conceptids, 'name':conceptnames}
            time.sleep(1)


def get_concept_map(pro):
    global ctcode_name
    if ctcode_name is None:
        init_ctcode_name(pro)
    return ctcode_name

def get_name(pro, code):
    global ctcode_name
    if ctcode_name is None:
        init_ctcode_name(pro)
    return ctcode_name[code]

def init_ctcode_name(pro):
    global ctcode_name
    if ctcode_name is None:
        ctcode_name = {}
        conceptdf=pro.concept(src='ts')
        conceptcodes=conceptdf['code'].values.tolist()
        conceptnames=conceptdf['name'].values.tolist()
        for i  in range(len(conceptcodes)):
            ctcode_name[conceptcodes[i]]= conceptnames[i]

if __name__== '__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    init_ctcode_name(pro)
    print(ctcode_name)
    print(get_name(pro, 'TS2'))
    print(get_ctcode_by_tscode(pro, '600848.SH'))
    #conceptdf.to_csv('./concept.csv')
