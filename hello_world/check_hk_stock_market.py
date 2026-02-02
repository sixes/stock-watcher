import akshare as ak
import logging
from datetime import datetime
from db import save_stock_px_changed

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

def check_hk_stock_market():
    observe_list = ('00700', '09988', '09618', '03690', '09999', '00300', '02800', '03188', '03074', '02840', '02823', '03110',
    '03042', '03195')
    observe_name = ('腾讯', '阿里', '京东', '美团', '网易', '美的', '盈富', '沪深300', 'MS台湾', 'SPDR金', 'A50', '高股息',
    '比特币', 'SP500')
    alerts = []  # List to store alert messages
    results = []  # List to store results as (ticker, name, closing price, change percentage, chg_pct_so_far)
    current_date = datetime.now().strftime('%Y-%m-%d')

    for index, ticker in enumerate(observe_list):
        name = observe_name[index]
        daily = ak.stock_hk_daily(symbol=ticker, adjust='qfq')
        # Get the latest and previous closing prices
        latest_day_data = daily.tail(1)
        latest_closing_px = latest_day_data.iat[0, 4]  # Latest closing price
        previous_closing_px = daily.iloc[-2].iat[4]    # Previous closing price

        highest_day_data = daily[daily.high == daily.high.max()]
        highest_px = highest_day_data.iat[0, 2]

        # Calculate change percentage
        change_percentage = ((latest_closing_px - previous_closing_px) / previous_closing_px) * 100
        chg_pct_so_far = (latest_closing_px - highest_px) / highest_px * 100

        # Store result as a tuple (ticker, name, ...)
        results.append((ticker, name, latest_closing_px, change_percentage, chg_pct_so_far))

        # Save to DynamoDB using shared method
        save_stock_px_changed(
            ticker=ticker,
            name=name,
            closing_px=latest_closing_px,
            change_percentage=change_percentage,
            chg_pct_so_far=chg_pct_so_far,
            highest_px=highest_px,
            market='HK',
            date=current_date
        )

        prompt = ""
        if chg_pct_so_far <= -10:
            if chg_pct_so_far <= -20:
                prompt = "SEVERELY ALERT: "
            else:
                prompt = "ALERT: "
            alert_message = prompt + f"{name} ({latest_closing_px}, {change_percentage:.2f}%, {chg_pct_so_far:.2f}%) declined more than {chg_pct_so_far:.2f}% from the highest price: {highest_px:.2f}."
            alerts.append(alert_message)  # Store the alert message
    """
    # Sort results by change percentage in descending order
    results.sort(key=lambda x: x[2], reverse=True)
    # Print sorted results
    ret = []
    for ticker, closing_px, change_percentage,chg_pct_so_far in results:
        #ret.append(ticker + "(" + str(closing_px) + "," + str(change_percentage) + "%)")
        ret.append(f"{ticker}({closing_px:.2f},{change_percentage:.2f}%, {chg_pct_so_far:.2f}%)")

    return "\n".join(alerts), ",".join(ret)  # Return both alerts and sorted list of tuples
    """
    # Sort results by chg_pct_so_far in descending order
    results.sort(key=lambda x: x[4], reverse=True)

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
    <h2>HK Stock Market Performance</h2>
    <table>
        <tr>
            <th>Ticker</th>
            <th>Name</th>
            <th>Closing Price</th>
            <th>Daily Change %</th>
            <th>Change from High %</th>
        </tr>
    """
    for ticker, name, closing_px, change_percentage, chg_pct_so_far in results:
        html_table += (
            f"<tr>"
            f"<td>{ticker}</td>"
            f"<td>{name}</td>"
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
    alerts, results = check_hk_stock_market()
    
    # Print alert messages
    #for message in alerts:
    #    print(message)
    print(alerts)
      # Print each result
    print(results)
