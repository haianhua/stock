
def formatcode(code):
    '''
    desc: 把股票代号加上后缀
    param:code 
        format: 300541
    return:
        format: 300541.SZ
    '''
    if str(code).find('.') != -1:
        return code
    if str(code)[0:1] ==  '6':
        return str(code)+'.SH'
    return str(code)+'.SZ'

def get_tscodes(pro=None):
    '''
    desc: 取得所有上市公司股票代码
    return 股票代码
        format:list ['000001.SZ','000002.SZ']
    '''
    if pro==None:
        import tushare as ts
        pro = ts.pro_api('08aedc1cc54171e54a64bbe834ec1cb45026fa2ab39e9e4cb8208cad')
    global codes
    global basic_datas
    if codes is None:
        basic_datas = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        codes = basic_datas['ts_code'].values.tolist()
    return codes

if __name__=='__main__':
    print(formatcode(6001))
    print(formatcode('6001.SH'))
    print(formatcode('3001'))
    #print(get_tscodes(pro))
