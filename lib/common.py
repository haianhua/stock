
INDEX_LABELS = ['sh', 'sz', 'hs300', 'sz50', 'cyb', 'zxb', 'zx300', 'zh500']
INDEX_LIST = {'sh': 'sh000001', 'sz': 'sz399001', 'hs300': 'sh000300',
              'sz50': 'sh000016', 'zxb': 'sz399005', 'cyb': 'sz399006', 
              'zx300': 'sz399008', 'zh500':'sh000905'}

def _code_to_symbol(code):
    '''
        生成symbol代码标志
    '''
    code=str(code)
    if code in INDEX_LABELS:
        return INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return code
        else:
            return '%s.SH'%code if code[:1] in ['5', '6', '9'] or code[:2] in ['11', '13'] else '%s.SZ'%code

        
def _code_to_symbol_dgt(code):
    '''
        生成symbol代码标志
    '''
    if code in INDEX_LABELS:
        return INDEX_LIST[code]
    else:
        if len(code) != 6 :
            return code
        else:
            return '0%s'%code if code[:1] in ['5', '6', '9'] else '1%s'%code

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
    print(_code_to_symbol(399008))
    print(_code_to_symbol('399008.SH'))
    print(_code_to_symbol('3001'))
    #print(get_tscodes(pro))
