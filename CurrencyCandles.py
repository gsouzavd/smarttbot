import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector

disponible_currencies = ['USDT_AAVE',
                        'USDT_ADABEAR',
                        'USDT_ADABULL',
                        'USDT_ADD',
                        'USDT_ADEL',
                        'USDT_AKRO',
                        'USDT_ALPHA',
                        'USDT_AMP',
                        'USDT_ANK',
                        'USDT_API3',
                        'USDT_ATOM',
                        'USDT_AVA',
                        'USDT_AKITA',
                        'USDT_BAC',
                        'USDT_BADGER',
                        'USDT_BAL',
                        'USDT_BAND',
                        'USDT_BAT',
                        'USDT_BCH',
                        'USDT_BCHA',
                        'USDT_BCHBEAR',
                        'USDT_BCHBULL',
                        'USDT_BCHC',
                        'USDT_BCHSV',
                        'USDT_BCN',
                        'USDT_BDP',
                        'USDT_BEAR',
                        'USDT_BID',
                        'USDT_BLY',
                        'USDT_BNB',
                        'USDT_BOND',
                        'USDT_BREE',
                        'USDT_BRG',
                        'USDT_BSVBEAR',
                        'USDT_BSVBULL',
                        'USDT_BTC',
                        'USDT_BTT',
                        'USDT_BULL',
                        'USDT_BUSD',
                        'USDT_BVOL',
                        'USDT_BZRX',
                        'USDT_BTCST',
                        'USDT_B20',
                        'USDT_CHR',
                        'USDT_COMBO',
                        'USDT_COMP',
                        'USDT_CORN',
                        'USDT_CREAM',
                        'USDT_CRT',
                        'USDT_CRV',
                        'USDT_CUDOS',
                        'USDT_CUSDT',
                        'USDT_CVP',
                        'USDT_DAI',
                        'USDT_DASH',
                        'USDT_DEC',
                        'USDT_DEXT',
                        'USDT_DGB',
                        'USDT_DHT',
                        'USDT_DIA',
                        'USDT_DOGE',
                        'USDT_DOS',
                        'USDT_DOT',
                        'USDT_DEGO',
                        'USDT_EOS',
                        'USDT_EOSBEAR',
                        'USDT_EOSBULL',
                        'USDT_ESD',
                        'USDT_ETC',
                        'USDT_ETH',
                        'USDT_ETHBEAR',
                        'USDT_ETHBULL',
                        'USDT_EXE',
                        'USDT_ELON',
                        'USDT_FARM',
                        'USDT_FCT2',
                        'USDT_FRONT',
                        'USDT_FSW',
                        'USDT_FTT',
                        'USDT_FUND',
                        'USDT_FXC',
                        'USDT_FIL',
                        'USDT_FORTH',
                        'USDT_GEEQ',
                        'USDT_GHST',
                        'USDT_GLM',
                        'USDT_GRIN',
                        'USDT_GRT',
                        'USDT_HEGIC',
                        'USDT_HGET',
                        'USDT_IBVOL',
                        'USDT_INJ',
                        'USDT_JFI',
                        'USDT_JST',
                        'USDT_KP3R',
                        'USDT_KTON',
                        'USDT_KCS',
                        'USDT_KLV',
                        'USDT_LEND',
                        'USDT_LINK',
                        'USDT_LINKBEAR',
                        'USDT_LINKBULL',
                        'USDT_LPT',
                        'USDT_LON',
                        'USDT_LRC',
                        'USDT_LSK',
                        'USDT_LTC',
                        'USDT_LTCBEAR',
                        'USDT_LTCBULL',
                        'USDT_LIVE',
                        'USDT_LQTY',
                        'USDT_LUSD',
                        'USDT_MANA',
                        'USDT_MATIC',
                        'USDT_MCB',
                        'USDT_MDT',
                        'USDT_MEME',
                        'USDT_MEXP',
                        'USDT_MKR',
                        'USDT_MPH',
                        'USDT_MTA',
                        'USDT_MIR',
                        'USDT_MIST',
                        'USDT_NEO',
                        'USDT_NU',
                        'USDT_NFTX',
                        'USDT_OCEAN',
                        'USDT_OM',
                        'USDT_ONEINCH',
                        'USDT_OPT',
                        'USDT_PAX',
                        'USDT_PBTC35A',
                        'USDT_PEARL',
                        'USDT_PERX',
                        'USDT_POLS',
                        'USDT_PRQ',
                        'USDT_QTUM',
                        'USDT_QUICK',
                        'USDT_RARI',
                        'USDT_REEF',
                        'USDT_REN',
                        'USDT_REPV2',
                        'USDT_RFUEL',
                        'USDT_RING',
                        'USDT_RSR',
                        'USDT_SAL',
                        'USDT_SAND',
                        'USDT_SC',
                        'USDT_SENSO',
                        'USDT_SNX',
                        'USDT_SRM',
                        'USDT_STAKE',
                        'USDT_STEEM',
                        'USDT_STPT',
                        'USDT_STR',
                        'USDT_SUN',
                        'USDT_SUSHI',
                        'USDT_SWAP',
                        'USDT_SWFTC',
                        'USDT_SWINGBY',
                        'USDT_SWRV',
                        'USDT_SXP',
                        'USDT_SFI',
                        'USDT_SHIB',
                        'USDT_TAI',
                        'USDT_TEND',
                        'USDT_TRADE',
                        'USDT_TRB',
                        'USDT_TRU',
                        'USDT_TRX',
                        'USDT_TRXBEAR',
                        'USDT_TRXBULL',
                        'USDT_TUSD',
                        'USDT_UMA',
                        'USDT_UNI',
                        'USDT_USDJ',
                        'USDT_UST',
                        'USDT_VALUE',
                        'USDT_VSP',
                        'USDT_WBTC',
                        'USDT_WETH',
                        'USDT_WIN',
                        'USDT_WNXM',
                        'USDT_WRX',
                        'USDT_WHALE',
                        'USDT_XFLR',
                        'USDT_XLMBEAR',
                        'USDT_XLMBULL',
                        'USDT_XMR',
                        'USDT_XRP',
                        'USDT_XRPBEAR',
                        'USDT_XRPBULL',
                        'USDT_XTZ',
                        'USDT_XOR',
                        'USDT_YFI',
                        'USDT_YFII',
                        'USDT_YFL',
                        'USDT_ZAP',
                        'USDT_ZEC',
                        'USDT_ZKS',
                        'USDT_ZLOT',
                        'USDT_ZRX']

class _CurrencyCandle:
    def __init__(self, currency, period):
        self.currency = currency
        self.period = period
        self._high_candle = 0
        self._low_candle = 0
        self.open = 0
        self.close = 0
        self.lastUpdateDateTime = datetime.now()
        self.trades_df = pd.DataFrame(columns = ['timestamp','value'])
        
    def addToCandle(self, last):
        # Add new values to the dataframe 
        self.trades_df = self.trades_df.append({'timestamp': datetime.now().timestamp(), 'value' : last}, ignore_index=True)
        # Drop all timestamps lower than the candle
        self.trades_df = self.trades_df[~(self.trades_df['timestamp'] <= (datetime.now()-timedelta(seconds=self.period)).timestamp() ) ] 
        # Get current max and min
        self._high_candle = self.trades_df['value'].max()
        self._low_candle = self.trades_df['value'].min()
        self.lastUpdateDateTime = datetime.now()

    def getCandleMax(self):
        return self._high_candle

    def getCandleMin(self):
        return self._low_candle


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
