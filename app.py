import CurrencyCandles as cc
import DatabaseMySQL as db
from datetime import datetime
import sched, time
from flask import Flask
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
import logging

# Global variables to setup the program
# Period in seconds of the task that gets current currency values from Poloniex
# Value chosen due to system limitations
BASE_UPDATE_SCHEDULE_PERIOD = 2 
CANDLE_60_SECONDS_PERIOD = 60 # Period of the task - update the 1 min candle
CANDLE_300_SECONDS_PERIOD = 300 # Period of the task - update the 5 min candle
CANDLE_600_SECONDS_PERIOD = 600 # Period of the task - update the 10 min candle

# Currency list that will be used
currency_list = ['BTC', 'ZRX']
#scheduler = APScheduler()
scheduler = BackgroundScheduler()
databaseMySQL = db.DatabaseMySQL()

class Config:
    """Flask app configuration."""
    # Use threads to assure it's possible to do multiple tasks at the same time
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 200}}
    # Avoid having too many executions at once, but gives window to a possible time lag
    SCHEDULER_JOB_DEFAULTS = {"coalesce": True, "max_instances": 1}
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/currency_sumary')
def get_currency_sumary():
    return databaseMySQL.get_select_currency(request.args.get('currency', default = 'BTC', type = str))

def start_currency_candles(currency):
    """
    Schedulers to USDT - Desired_currency pairs
    """
    currencyPair = cc.CurrencyCandles('USDT_' + currency.upper())

    #@scheduler.task("interval", id="update_"+currencyPair.key, seconds=BASE_UPDATE_SCHEDULE_PERIOD, misfire_grace_time = 1)
    def update_currency_value(): 
        """
        Get values from Poloniex server
        """
        currencyPair.updateCurrencyCandles()
        print(currency)
        
    #@scheduler.task("interval", id="candle_60_"+currencyPair.key, seconds=CANDLE_60_SECONDS_PERIOD, misfire_grace_time = 1)
    def add_1_min_candle():
        """
        Updates 1 min candle to the MySQL server
        """
        candle = currencyPair.candle_60_seconds
        databaseMySQL.update_1_min_candle(candle.getCandleMax(), candle.getCandleMin(),
                                        candle.getOpen(), candle.getClose(),
                                        currency)
        
    #@scheduler.task("interval", id="candle_300_"+currencyPair.key, seconds=CANDLE_300_SECONDS_PERIOD, misfire_grace_time = 1)
    def add_5_min_candle():
        """
        Updates 5 min candle to the MySQL server
        """
        candle = currencyPair.candle_300_seconds
        databaseMySQL.update_5_min_candle(candle.getCandleMax(), candle.getCandleMin(),
                                        candle.getOpen(), candle.getClose(),
                                        currency)
    #@scheduler.task("interval", id="candle_600_"+currencyPair.key, seconds=CANDLE_600_SECONDS_PERIOD, misfire_grace_time = 1)
    def add_10_min_candle():
        """
        Updates 10 min candle to the MySQL server
        """
        candle = currencyPair.candle_600_seconds
        databaseMySQL.update_10_min_candle(candle.getCandleMax(), candle.getCandleMin(),
                                        candle.getOpen(), candle.getClose(),
                                        currency)
    #logging.info("{} - Starting task for {}".format(datetime.now(), currency))
    
    scheduler.add_job(id=currency + "_update", name=currency + "_update", func=update_currency_value, trigger="interval", seconds=BASE_UPDATE_SCHEDULE_PERIOD)
    scheduler.add_job(id=currency + "_1min_candle", name=currency + "_1min_candle", func=add_1_min_candle, trigger="interval", seconds=CANDLE_60_SECONDS_PERIOD)
    scheduler.add_job(id=currency + "_5min_candle", name=currency + "_5min_candle", func=add_5_min_candle, trigger="interval", seconds=CANDLE_300_SECONDS_PERIOD)
    scheduler.add_job(id=currency + "_10min_candle", name=currency + "_10min_candle", func=add_10_min_candle, trigger="interval", seconds=CANDLE_600_SECONDS_PERIOD)


if __name__ == "__main__":   
    # Init log file
    logging.basicConfig(filename='Execution_log.log', 
                        encoding='utf-8',
                        level=logging.INFO)
    logging.warning("{} - Starting the Scheduler".format(datetime.now()))
    for currency in currency_list:
        if (currency in cc.disponible_currencies):
            start_currency_candles(currency)
        else:
            logging.warning("Currency {} not disponible, it will be ignored during the execution".format(currency))
    scheduler.start()
    app.run()
    
    
    

