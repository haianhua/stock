#!/usr/local/python3/bin/python3
import tushare as ts
import re
import datetime

concept_map=None

def get_concept_map(pro):
    global concept_map
    if concept_map is None:
        init(pro)
    return concept_map

def get_name(pro, code):
    global concept_map
    if concept_map is None:
        init(pro)
    return concept_map[code]

def init(pro):
    global concept_map
    if concept_map is None:
        concept_map = {}
        conceptdf=pro.concept(src='ts')
        conceptcodes=conceptdf['code'].values.tolist()
        conceptnames=conceptdf['name'].values.tolist()
        for i  in range(len(conceptcodes)):
            concept_map[conceptcodes[i]]= conceptnames[i]

if __name__== '__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    init(pro)
    print(concept_map)
    print(get_name(pro, 'TS2'))
    #conceptdf.to_csv('./concept.csv')
