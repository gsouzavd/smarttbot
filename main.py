import CurrencyCandles as cc
import DatabaseMySQL as db
import sched, time

BASE_UPDATE_SCHEDULE_PERIOD = 2
CANDLE_60_SECONDS_PERIOD = 5
CANDLE_300_SECONDS_PERIOD = 5
CANDLE_600_SECONDS_PERIOD = 5
databaseMySQL = db.DatabaseMySQL()
s = sched.scheduler(time.time, time.sleep)

currency_list = ['BTC']

def start_currency_candles(currency):
    USDT_BTC = cc.CurrencyCandles('USDT_' + currency.upper())

    def update_currency_value(sc): 
        USDT_BTC.updateCurrencyCandles()
        print(USDT_BTC.candle_60_seconds.getCandleMax())
        s.enter(BASE_UPDATE_SCHEDULE_PERIOD, 1, update_currency_value, (sc,))

    def add_1_min_candle(sc):
        candle = USDT_BTC.candle_60_seconds
        databaseMySQL.update_1_min_candle(candle.getCandleMax(), candle.getCandleMin(), currency)
        s.enter(CANDLE_60_SECONDS_PERIOD, 1, add_1_min_candle, (sc,))

    def add_5_min_candle(sc):
        candle = USDT_BTC.candle_300_seconds
        databaseMySQL.update_5_min_candle(candle.getCandleMax(), candle.getCandleMin(), currency)
        s.enter(CANDLE_300_SECONDS_PERIOD, 1, add_5_min_candle, (sc,))

    def add_10_min_candle(sc):
        candle = USDT_BTC.candle_600_seconds
        databaseMySQL.update_10_min_candle(candle.getCandleMax(), candle.getCandleMin(), currency)
        s.enter(CANDLE_600_SECONDS_PERIOD, 1, add_10_min_candle, (sc,))

    print("Starting task for {}".format(currency))
    s.enter(BASE_UPDATE_SCHEDULE_PERIOD, 1, update_currency_value, (s,))
    s.enter(CANDLE_60_SECONDS_PERIOD, 1, add_1_min_candle, (s,))
    s.enter(CANDLE_300_SECONDS_PERIOD, 1, add_5_min_candle, (s,))
    s.enter(CANDLE_600_SECONDS_PERIOD, 1, add_10_min_candle, (s,)) 

if __name__ == "__main__":   
    for currency in currency_list:
        start_currency_candles(currency)
    s.run()
    
