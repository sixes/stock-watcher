import akshare as ak

def check_us_stock_market():
    observe_list = ('AAPL', 'NVDA', 'MSFT', 'AMZN', 'AVGO', 'META', 'TSLA', 'COST', 'GOOGL', 'NFLX', 'GOOG', 'WMT', 'ASML', 'TSM', 'MAGS', 'QQQ', 'VOO', 'MGK')
    alerts = []  # List to store alert messages
    results = []  # List to store results as (ticker, closing price, change percentage)
    
    for ticker in observe_list:
        daily = ak.stock_us_daily(symbol=ticker, adjust='qfq')
        #print(daily.tail())
        
        # Get the latest and previous closing prices
        latest_day_data = daily.tail(1)
        latest_closing_px = latest_day_data.iat[0, 4]  # Latest closing price
        previous_closing_px = daily.iloc[-2].iat[4]    # Previous closing price

        highest_day_data = daily[daily.high == daily.high.max()]
        highest_px = highest_day_data.iat[0, 2]

        # Calculate change percentage
        change_percentage = ((latest_closing_px - previous_closing_px) / previous_closing_px) * 100
        # Store result as a tuple
        results.append((ticker, latest_closing_px, change_percentage))

        if latest_closing_px <= highest_px * 0.6:
            alert_message = f"SEVERELY ALERT: {ticker} ({latest_closing_px}, {change_percentage:.2f}%) declined more than 40% from the highest price: {highest_px:.2f}."
            alerts.append(alert_message)  # Store the alert message
        elif latest_closing_px <= highest_px * 0.7:
            alert_message = f"SEVERELY ALERT: {ticker} ({latest_closing_px}, {change_percentage:.2f}%) declined more than 30% from the highest price: {highest_px:.2f}."
            alerts.append(alert_message)  # Store the alert message
        elif latest_closing_px <= highest_px * 0.8:
            alert_message = f"SEVERELY ALERT: {ticker} ({latest_closing_px}, {change_percentage:.2f}%) declined more than 20% from the highest price: {highest_px:.2f}."
            alerts.append(alert_message)  # Store the alert message 
        elif latest_closing_px <= highest_px * 0.9:
            alert_message = f"ALERT: {ticker} ({latest_closing_px},{change_percentage:.2f}%) declined more than 10% from the highest price: {highest_px:.2f}."
            alerts.append(alert_message)  # Store the alert message
            
            

    # Sort results by change percentage in descending order
    results.sort(key=lambda x: x[2], reverse=True)
    # Print sorted results
    ret = []
    for ticker, closing_px, change_percentage in results:
        #ret.append(ticker + "(" + str(closing_px) + "," + str(change_percentage) + "%)")
        ret.append(f"{ticker}({closing_px:.2f},{change_percentage:.2f}%)")

    return "\n".join(alerts), ",".join(ret)  # Return both alerts and sorted list of tuples
    #return alerts

if __name__ == "__main__":
    alerts, results = check_us_stock_market()
    
    # Print alert messages
    for message in alerts:
        print(message)
    
      # Print each result
    print(results)