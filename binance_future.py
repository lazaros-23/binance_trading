from os import makedev
from types import MethodDescriptorType
import requests
import pprint
import logging

logger = logging.getLogger() 

class BinanceFuturesClient():
    def __init__(self, testnet):
        if testnet:
            self.base_url = 'https://testnet.binancefuture.com'
        else:
            self.base_url = 'https://fapi.binance.com'

        logger.info("Binance futures client succussfully initialized")

    def make_request(self, method, endpoint, data):
        if method == 'GET':
            response = requests.get(self.base_url + endpoint, params=data)
        else:
            raise ValueError()

        if response.status_code == 200:
            return response.json()
        else:
            logger.error('Error while making request')
            
            return None

    def get_contracts(self):

        exchange_info = self.make_request('GET', '/fapi/v1/exchangeInfo', None)
        contracts = dict()

        if exchange_info is not None:
            for contract_data in exchange_info['symbols']:
                contracts[contract_data['pair']] == contract_data

        return contracts

    def get_historical_candles(self, symbol, intreval):
        data = dict()
        data['symbol'] = symbol
        data['interval'] = intreval
        data['limit'] = 1000

        raw_candles = self.make_request('GET', '/fapi/v1/klines', data)
        candles = []

        if raw_candles is not None:
            for c in raw_candles:
                candles.append([c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])])

        return candles


    def get_bid_ask(self,symbol):

        data = dict()
        data['symbol'] = symbol
        cd_data = self.make_request('GET', '/fapi/v1/ticker/bookTicker', data)

        if cd_data is not None:
            if symbol not in self.prices:
                self.prices[symbol] = {'bid': float(cd_data['bidPrice']), 'ask': float(cd_data['askPrice'])}
            else:
                self.prices[symbol]['bid'] = float(cd_data['bidPrice'])
                self.prices[symbol]['ask'] = float(cd_data['askPrice'])
        
        return self.prices[symbol]
