from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pprint
import json
import os
import dotenv

# Pretty print data
def pretty(data):
    return pprint.PrettyPrinter(indent=4).pprint(data)

dotenv.load_dotenv()
COIN_MARKET_API_KEY = os.getenv("COIN_MARKET_API_KEY")
BASE_URL = 'https://pro-api.coinmarketcap.com/v1/'

class CoinMarketAPI:
    def __init__(self):
        self.session = Session()
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': COIN_MARKET_API_KEY,
        }

    def send_request(self, url, params):
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            data = json.loads(response.text)
            pretty(data)
            return data
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return e