import datetime
import re

def strtime_today():
    return datetime.date.today().strftime("%Y-%m-%d")

def strtime_by_range(date_b, date_e):
    begin=re.findall(r"\d+", date_b)
    begin=datetime.date(int(begin[0]),int(begin[1]),int(begin[2]))
    end=re.findall(r"\d+", date_e)
    end=datetime.date(int(end[0]),int(end[1]),int(end[2]))
    results=[]
    for i in range((end-begin).days+1):
        date = begin + datetime.timedelta(days=i)
        date=date.strftime("%Y-%m-%d")
        results.append(date)
    return results
