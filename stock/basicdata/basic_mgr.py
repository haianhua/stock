import tushare as ts

basic_datas=None
#names
codes=None

def get_tscodes(pro):
    '''
    desc: 取得所有上市公司股票代码
    return 股票代码
        format:list ['000001.SZ','000002.SZ']
    '''
    global codes
    global basic_datas
    if codes is None:
        basic_datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        codes = basic_datas['ts_code'].values.tolist()
    return codes

if __name__== '__main__':
    pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    print(get_tscodes(pro))
    #data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    #print(data, type(data))
    #print(pro.concept_detail(id='TS2'))
