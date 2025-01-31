import akshare as ak
from datetime import date, datetime, timedelta

def check_a_stock_market():
    ret = ''
    start_date = date.today() - timedelta(days=10)
    ticker ='000001'
    daily = ak.index_zh_a_hist(symbol=ticker, period='daily', start_date=start_date, end_date=datetime.today())
    #print(daily.tail(5))
    latest_day_data = daily.tail(1)
    latest_low_px = latest_day_data.iat[0, 4]
    last_close_px = latest_day_data.iat[0, 2]
    str_low_px = "SH Index(" + str(latest_low_px) + ")"
    if latest_low_px < 2700:
        ret = " PLS SERIOUSLY CONSIDER BUYING IN! SH Index slumped below 2700"
    elif latest_low_px < 2800:
        ret = " PLS SERIOUSLY CONSIDER BUYING IN! SH Index slumped below 2800"
    elif latest_low_px < 2900:
        ret = " PLS SERIOUSLY CONSIDER BUYING IN! SH Index slumped below 2900"
    elif latest_low_px < 3000:
        ret = "ATTENTION: SH Index(" + str(latest_low_px) + ") declined below 3000"
    else:
        ret = str(latest_day_data.iat[0, 0]) + " SH Index(" +  str(last_close_px) + ")"
    #print(ret)

    ticker = '000016'
    daily = ak.index_zh_a_hist(symbol=ticker, period='daily', start_date=start_date, end_date=datetime.today())
    #print(daily.tail(5))
    latest_day_data = daily.tail(1)
    latest_low_px = latest_day_data.iat[0, 4]
    last_close_px = latest_day_data.iat[0, 2]
    str_low_px = "SH50 Index(" + str(latest_low_px) + ")"
    if latest_low_px < 2378:
        ret += "\n PLS SERIOUSLY CONSIDER BUYING IN! SH50 Index slumped below 2738"
    else:
        ret += " SH50 Index(" +  str(last_close_px) + ")"
    #print(ret)

    ticker = '159841'
    daily = ak.index_zh_a_hist(symbol=ticker, period='daily', start_date=start_date, end_date=datetime.today())
    #print(daily.tail(5))
    latest_day_data = daily.tail(1)
    latest_low_px = latest_day_data.iat[0, 4]
    last_close_px = latest_day_data.iat[0, 2]
    str_low_px = "SecurityETF(" + str(latest_low_px) + ")"
    if latest_low_px < 0.7:
        ret += "\n PLS SERIOUSLY CONSIDER BUYING IN! SecurityETF slumped below 0.7"
    elif latest_low_px < 0.8:
        ret += "\n PLS SERIOUSLY CONSIDER BUYING IN! SecurityETF slumped below 0.8"
    else:
        ret += " SecurityETF(" +  str(last_close_px) + ")"
    print(ret)
    return ret