import tushare as ts
import re
def get_tick_data_by_date(code, date):
    '''
    parameters
        code:string
            股票代码 format 600848
        date:string
            日期 format: YYYY-MM-DD
    return
        DataFrame 当日股票交易数据
            属性: 成交时间、成交价格、价格变动、成交手、成交金额、买卖类型
    '''
    return ts.get_tick_data(code, date, 3, 1 , 'tt')

def get_tick_data_by_range(code, date_b, date_e):
    '''
    parameters
        code:string
            股票代码 format 600848
        date_b:string
            开始日期(闭区间) format: YYYY-MM-DD
        date_e:string
            结束日期(闭区间) format: YYYY-MM-DD
    return
        results 该时间段内股票交易数据
            format: ['2019-01-02':DataFrame, '2019-01-03':DataFrame]
            DataFrame 属性: 成交时间、成交价格、价格变动、成交手、成交金额、买卖类型
    '''
    begin=re.findall(r"\d+", date_b)
    begin=datetime.date(begin[0],begin[1],begin[2])
    end=re.findall(r"\d+", date_e)
    end=datetime.date(end[0],end[1],end[2])
    results={}
    for i in range((end-begin).days+1):
        date = begin + datetime.timedelta(days=i)
        results[date]=ts.get_tick_data(code, date, 3, 1, 'tt')
    return results

def get_tick_data(code, date_b, date_e=None):
    '''
    parameters
        code:string
            股票代码 format 600848
        date_b:string
            开始日期(闭区间) format: YYYY-MM-DD
        date_e:string
            结束日期(闭区间) format: YYYY-MM-DD
            为None时，则只获取date_b那天的数据
    return
        results 该时间段内股票交易数据
            format: ['2019-01-02':DataFrame, '2019-01-03':DataFrame]
            DataFrame 属性: 成交时间、成交价格、价格变动、成交手、成交金额、买卖类型
        或
        同get_tick_data_by_date
    '''
    if date_e==None:
        return ts.get_tick_data(code, date, 3, 1 , 'tt')
    else:
        return get_tick_data_by_range(code, date_b, date_e)
