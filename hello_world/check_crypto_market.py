import os
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

api_key = os.getenv('COINLAYER_API_KEY')

def check_crypto_market():
    # Define the base URL and endpoint for live data
    base_url = "https://api.coinlayer.com/live"
    
    if not api_key:
        logger.error("coinlayer API key not found")
        return "coinlayer API key not found"
    # Set up parameters for the API request
    params = {
        'access_key': api_key,  # Your API access key
        'target': 'USD',         # Target currency (optional)
        'symbols': 'BTC,TRUMP,ETH,LTC' # Specify which cryptocurrencies to retrieve (optional)
    }

    try:
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response
        data = response.json()
        
        if data['success']:
            #print("Cryptocurrency Prices:")
            #print(data)
            logger.info(data)
            ret = ''
            for symbol, price in data['rates'].items():
                print(f"{symbol}: {price} {data['target']}")
                ret += f"{symbol},{price:,.0f},"
        else:
            # print("Error:", data['error']['info'])
            ret = "failed to retrieve crypto market data"
    
    except requests.exceptions.RequestException as e:
        print("API request failed:", e)
    return ret

if __name__ == "__main__":
    check_crypto_market()
