import akshare as ak
import logging
from datetime import datetime
from db import save_stock_px_changed

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# Add a mapping of tickers to Chinese short names
TICKER_TO_NAME = {
    'AAPL': '苹果', 'NVDA': '英伟达', 'MSFT': '微软', 'AMZN': '亚马逊', 'AVGO': '博通',
    'META': '脸书', 'TSLA': '特斯拉', 'COST': '好市多', 'GOOGL': '谷歌A', 'NFLX': '奈飞',
    'GOOG': '谷歌C', 'WMT': '沃尔玛', 'ASML': '阿斯麦', 'TSM': '台积电', 'MAGS': '麦格斯',
    'QQQ': '纳指ETF', 'TQQQ': '纳指三倍', 'VOO': '标普ETF', 'SPY': '标普500', 'MGK': '成长ETF',
    'SPLG': '标普低价', 'FNGB': '金融ETF', 'TEXL': '科技三倍', 'MSFU': '微软三倍',
    'TSLL': '特斯拉三倍', 'NVDU': '英伟达三倍', 'QULL': '纳指三倍', 'SPXL': '标普三倍',
    'ROM': '科技双倍', 'QLD': '纳指双倍', 'SSO': '标普双倍', 'UPRO': '标普三倍',
    'TECL': '科技三倍', 'SOXL': '半导体三倍'
}

def check_us_stock_market():
    #observe_list = ('AAPL', 'NVDA', 'MSFT', 'AMZN', 'AVGO', 'META', 'TSLA', 'COST', 'GOOGL', 'NFLX', 'GOOG', 'WMT', 'ASML', 'TSM', 'MAGS', 'QQQ', 'TQQQ', 'VOO', 'SPY', 'MGK', 'SPLG', 'FNGB', 'TEXL', 'MSFU', 'TSLL', 'NVDU', 'QULL', 'SPXL', 'ROM')
    observe_list = (
    'AAPL', 'NVDA', 'MSFT', 'AMZN', 'AVGO', 'META', 'TSLA', 'COST', 'GOOGL', 'NFLX',
    'GOOG', 'WMT', 'ASML', 'TSM', 'MAGS', 'QQQ', 'TQQQ', 'VOO', 'SPY', 'MGK',
    'SPLG', 'FNGB', 'TEXL', 'MSFU', 'TSLL', 'NVDU', 'QULL', 'SPXL', 'ROM', 'QLD',
    'SSO', 'UPRO', 'TECL', 'SOXL')
    i = 0
    alerts = []  # List to store alert messages
    results = []  # List to store results as (ticker, closing price, change percentage, chg_pct_so_far)

    current_date = datetime.now().strftime('%Y-%m-%d')

    for ticker in observe_list:
        try:
            daily = ak.stock_us_daily(symbol=ticker, adjust='qfq')
            # Get the latest and previous closing prices
            latest_day_data = daily.tail(1)
            latest_closing_px = latest_day_data.iat[0, 4]  # Latest closing price
            previous_closing_px = daily.iloc[-2].iat[4]    # Previous closing price

            highest_day_data = daily[daily.high == daily.high.max()]
            highest_px = highest_day_data.iat[0, 2]
            logger.info(f"{ticker}: {highest_px}")
            # Calculate change percentage
            change_percentage = ((latest_closing_px - previous_closing_px) / previous_closing_px) * 100
            chg_pct_so_far = (latest_closing_px - highest_px) / highest_px * 100
            print(f"{ticker}: {latest_closing_px}, {highest_px}, {change_percentage:.2f}, {chg_pct_so_far:.2f}")

            # Store result as a tuple
            results.append((ticker, latest_closing_px, change_percentage, chg_pct_so_far))

            # Save to DynamoDB using shared method, name is the Chinese short name
            save_stock_px_changed(
                ticker=ticker,
                name=TICKER_TO_NAME.get(ticker, ticker),  # Use Chinese name or fallback to ticker
                closing_px=latest_closing_px,
                change_percentage=change_percentage,
                chg_pct_so_far=chg_pct_so_far,
                highest_px=highest_px,
                market='US',
                date=current_date
            )

            prompt = ""
            if chg_pct_so_far <= -10:
                if chg_pct_so_far <= -20:
                    prompt = "SEVERELY ALERT: "
                else:
                    prompt = "ALERT: "
                alert_message = prompt + f"{ticker} ({latest_closing_px}, {change_percentage:.2f}%, {chg_pct_so_far:.2f}%) declined more than {chg_pct_so_far:.2f}% from the highest price: {highest_px:.2f}."
                alerts.append(alert_message)  # Store the alert message
        except Exception as e:
            logger.error(f"Error processing {ticker}: {e}")
            
    """
    # Sort results by change percentage in descending order
    results.sort(key=lambda x: x[2], reverse=True)
    # Print sorted results
    ret = []
    for ticker, closing_px, change_percentage, chg_pct_so_far in results:
        #ret.append(ticker + "(" + str(closing_px) + "," + str(change_percentage) + "%)")
        ret.append(f"{ticker}({closing_px:.2f},{change_percentage:.2f}%, {chg_pct_so_far:.2f}%)")

    return "\n".join(alerts), ",".join(ret)  # Return both alerts and sorted list of tuples
    #return alerts
    """
    # Sort results by chg_pct_so_far in descending order
    results.sort(key=lambda x: x[3], reverse=True)

    # Create HTML table
    html_table = """
    <html>
    <head><style>
        table { border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
    </style></head>
    <body>
    <h2>US Stock Market Performance</h2>
    <table>
        <tr>
            <th>Ticker</th>
            <th>Closing Price</th>
            <th>Daily Change %</th>
            <th>Change from High %</th>
        </tr>
    """
    for ticker, closing_px, change_percentage, chg_pct_so_far in results:
        html_table += (
            f"<tr>"
            f"<td>{ticker}</td>"
            f"<td>${closing_px:.2f}</td>"
            f"<td>{change_percentage:.2f}%</td>"
            f"<td>{chg_pct_so_far:.2f}%</td>"
            f"</tr>"
        )
    html_table += "</table></body></html>"

    # Create plain text for alerts
    alerts_text = "\n".join(alerts) if alerts else "No alerts triggered."

    return alerts_text, html_table

if __name__ == "__main__":
    alerts, results = check_us_stock_market()
    
    # Print alert messages
    #for message in alerts:
    #    print(message)
    
      # Print each result
    print(alerts)
    print(results)
