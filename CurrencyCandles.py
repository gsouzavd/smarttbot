import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector

disponible_currencies = ['AAVE',
                        'ADABEAR',
                        'ADABULL',
                        'ADD',
                        'ADEL',
                        'AKRO',
                        'ALPHA',
                        'AMP',
                        'ANK',
                        'API3',
                        'ATOM',
                        'AVA',
                        'AKITA',
                        'BAC',
                        'BADGER',
                        'BAL',
                        'BAND',
                        'BAT',
                        'BCH',
                        'BCHA',
                        'BCHBEAR',
                        'BCHBULL',
                        'BCHC',
                        'BCHSV',
                        'BCN',
                        'BDP',
                        'BEAR',
                        'BID',
                        'BLY',
                        'BNB',
                        'BOND',
                        'BREE',
                        'BRG',
                        'BSVBEAR',
                        'BSVBULL',
                        'BTC',
                        'BTT',
                        'BULL',
                        'BUSD',
                        'BVOL',
                        'BZRX',
                        'BTCST',
                        'B20',
                        'CHR',
                        'COMBO',
                        'COMP',
                        'CORN',
                        'CREAM',
                        'CRT',
                        'CRV',
                        'CUDOS',
                        'CUSDT',
                        'CVP',
                        'DAI',
                        'DASH',
                        'DEC',
                        'DEXT',
                        'DGB',
                        'DHT',
                        'DIA',
                        'DOGE',
                        'DOS',
                        'DOT',
                        'DEGO',
                        'EOS',
                        'EOSBEAR',
                        'EOSBULL',
                        'ESD',
                        'ETC',
                        'ETH',
                        'ETHBEAR',
                        'ETHBULL',
                        'EXE',
                        'ELON',
                        'FARM',
                        'FCT2',
                        'FRONT',
                        'FSW',
                        'FTT',
                        'FUND',
                        'FXC',
                        'FIL',
                        'FORTH',
                        'GEEQ',
                        'GHST',
                        'GLM',
                        'GRIN',
                        'GRT',
                        'HEGIC',
                        'HGET',
                        'IBVOL',
                        'INJ',
                        'JFI',
                        'JST',
                        'KP3R',
                        'KTON',
                        'KCS',
                        'KLV',
                        'LEND',
                        'LINK',
                        'LINKBEAR',
                        'LINKBULL',
                        'LPT',
                        'LON',
                        'LRC',
                        'LSK',
                        'LTC',
                        'LTCBEAR',
                        'LTCBULL',
                        'LIVE',
                        'LQTY',
                        'LUSD',
                        'MANA',
                        'MATIC',
                        'MCB',
                        'MDT',
                        'MEME',
                        'MEXP',
                        'MKR',
                        'MPH',
                        'MTA',
                        'MIR',
                        'MIST',
                        'NEO',
                        'NU',
                        'NFTX',
                        'OCEAN',
                        'OM',
                        'ONEINCH',
                        'OPT',
                        'PAX',
                        'PBTC35A',
                        'PEARL',
                        'PERX',
                        'POLS',
                        'PRQ',
                        'QTUM',
                        'QUICK',
                        'RARI',
                        'REEF',
                        'REN',
                        'REPV2',
                        'RFUEL',
                        'RING',
                        'RSR',
                        'SAL',
                        'SAND',
                        'SC',
                        'SENSO',
                        'SNX',
                        'SRM',
                        'STAKE',
                        'STEEM',
                        'STPT',
                        'STR',
                        'SUN',
                        'SUSHI',
                        'SWAP',
                        'SWFTC',
                        'SWINGBY',
                        'SWRV',
                        'SXP',
                        'SFI',
                        'SHIB',
                        'TAI',
                        'TEND',
                        'TRADE',
                        'TRB',
                        'TRU',
                        'TRX',
                        'TRXBEAR',
                        'TRXBULL',
                        'TUSD',
                        'UMA',
                        'UNI',
                        'USDJ',
                        'UST',
                        'VALUE',
                        'VSP',
                        'WBTC',
                        'WETH',
                        'WIN',
                        'WNXM',
                        'WRX',
                        'WHALE',
                        'XFLR',
                        'XLMBEAR',
                        'XLMBULL',
                        'XMR',
                        'XRP',
                        'XRPBEAR',
                        'XRPBULL',
                        'XTZ',
                        'XOR',
                        'YFI',
                        'YFII',
                        'YFL',
                        'ZAP',
                        'ZEC',
                        'ZKS',
                        'ZLOT',
                        'ZRX']

class _CurrencyCandle:
    def __init__(self, currency, period):
        self.currency = currency
        self.period = period
        self.__high_candle = 0
        self.__low_candle = 0
        self.__open = 0
        self.__close = 0
        self.lastUpdateDateTime = datetime.now()
        self.trades_df = pd.DataFrame(columns = ['timestamp','value'])
        
    def addToCandle(self, last):
        # Add new values to the dataframe 
        self.trades_df = self.trades_df.append({'timestamp': datetime.now().timestamp(), 'value' : last}, ignore_index=True)
        # Drop all timestamps lower than the candle
        self.trades_df = self.trades_df[~(self.trades_df['timestamp'] <= (datetime.now()-timedelta(seconds=self.period)).timestamp() ) ] 
        # Get current max and min
        self.__high_candle = self.trades_df['value'].max()
        self.__low_candle = self.trades_df['value'].min()
        self.__open = self.trades_df['value'].iloc[0]
        self.__close = self.trades_df['value'].iloc[-1]
        self.lastUpdateDateTime = datetime.now()

    def getCandleMax(self):
        return self.__high_candle

    def getCandleMin(self):
        return self.__low_candle

    def getOpen(self):
        return self.__open

    def getClose(self):
        return self.__close


class _CurrencySumary:
    def __init__(self, key, currecy_dict):
        self.key = key
        self.id = currecy_dict[key]['id']
        self.last = currecy_dict[key]['last']
        self.lowestAsk = currecy_dict[key]['lowestAsk']
        self.baseVolume = currecy_dict[key]['baseVolume']
        self.quoteVolume = currecy_dict[key]['quoteVolume']
        self.isFrozen = currecy_dict[key]['isFrozen']
        self.postOnly = currecy_dict[key]['postOnly']
        self.high24hr = currecy_dict[key]['high24hr']
        self.low24hr = currecy_dict[key]['low24hr']
        self.createdDateTime = datetime.now()
        self.lastUpdateDateTime = datetime.now()    

    def update_currency_values(currecy_dict):
        self.id = currecy_dict[self.key]['id']
        self.last = currecy_dict[self.key]['last']
        self.lowestAsk = currecy_dict[self.key]['lowestAsk']
        self.baseVolume = currecy_dict[self.key]['baseVolume']
        self.quoteVolume = currecy_dict[self.key]['quoteVolume']
        self.isFrozen = currecy_dict[self.key]['isFrozen']
        self.postOnly = currecy_dict[self.key]['postOnly']
        self.high24hr = currecy_dict[self.key]['high24hr']
        self.low24hr = currecy_dict[self.key]['low24hr']
        self.lastUpdateDateTime = datetime.now()

class CurrencyCandles:
    def __init__(self, key):
        self.key = key
        self.candle_60_seconds = _CurrencyCandle(self.key,60)
        self.candle_300_seconds = _CurrencyCandle(self.key,300)
        self.candle_600_seconds = _CurrencyCandle(self.key,600)

    def updateCurrencyCandles(self):
        response = requests.get('https://poloniex.com/public?command=returnTicker')
        self.current_currency = _CurrencySumary(self.key, response.json())
        self.candle_60_seconds.addToCandle(self.current_currency.last)
        self.candle_300_seconds.addToCandle(self.current_currency.last)
        self.candle_600_seconds.addToCandle(self.current_currency.last)
