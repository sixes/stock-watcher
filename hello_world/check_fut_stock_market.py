import akshare as ak
from datetime import date, datetime, timedelta

def check_fut_stock_market():
    ret = ''
    start_date = date.today() - timedelta(days=3)
    ticker ='AG0'
    daily = ak. futures_main_sina(symbol=ticker, start_date=start_date, end_date=datetime.today())
    #print(daily.tail(5))
    latest_day_data = daily.tail(1)
    last_close_px = latest_day_data.iat[0, 4]
    ret = str(latest_day_data.iat[0, 0]) + " AG0(" +  str(last_close_px) + ")"
    print(ret)
    return ret

if __name__ == "__main__":
    check_fut_stock_market()