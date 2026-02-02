from datetime import datetime
from check_a_stock_market import check_a_stock_market
from check_crypto_market import check_crypto_market
from check_fut_stock_market import check_fut_stock_market
from check_hk_stock_market import check_hk_stock_market
from check_us_stock_market import check_us_stock_market
from fetch_icbc_auction_data import fetch_icbc_auction_data
from read_Nikkei_news import read_nikkei_news 
import send_ses

def lambda_handler(event, context):

    ret, summary = check_us_stock_market()
    ret += "\n\n" + summary
    ret2, summary2 = check_hk_stock_market()
    ret += "\n\n" + ret2 + "\n\n" + summary2
    ret += "\n\n" + check_a_stock_market()
    ret += "\n" + check_fut_stock_market()
    ret += "\n\n" + check_crypto_market()
    
    news = read_nikkei_news()
    ret += "\n\n" + news 
    
    auction_table = ""
    auction_table, cnt = fetch_icbc_auction_data()

    today = datetime.today().strftime('%Y-%m-%d')
    print(event)
    print(summary)
    #resp = send_ses.send_email(today + " stock market monitoring", "", html_body=summary + "\n" + summary2 + "\n" + news)
    if cnt > 0:
        resp = send_ses.send_email(today + " ICBC auction market monitoring", ret, auction_table)
        if 'ResponseMetadata' in resp and resp['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("email sent successfully") 
        else:
            print("email sent failed")
        
    return {
        'statusCode': 200,
        'body': 'done'
    }

