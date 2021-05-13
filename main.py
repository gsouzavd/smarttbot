import CurrencyCandles as cc
import DatabaseMySQL as db
from datetime import datetime
import sched, time
from flask import Flask
from flask_apscheduler import APScheduler
import logging

# Global variables to setup the program
# Period in seconds of the task that gets current currency values from Poloniex
# Value chosen due to system limitations
BASE_UPDATE_SCHEDULE_PERIOD = 2 
CANDLE_60_SECONDS_PERIOD = 60 # Period of the task - update the 1 min candle
CANDLE_300_SECONDS_PERIOD = 300 # Period of the task - update the 5 min candle
CANDLE_600_SECONDS_PERIOD = 600 # Period of the task - update the 10 min candle

# Currency list that will be used
currency_list = ['BTC', 'AAVE']
scheduler = APScheduler()
databaseMySQL = db.DatabaseMySQL()

class Config:
    """Flask app configuration."""
    # Use threads to assure it's possible to do multiple tasks at the same time
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 50}}
    # Avoid having too many executions at once, but gives window to a possible time lag
    SCHEDULER_JOB_DEFAULTS = {"coalesce": False, "max_instances": 2}
    SCHEDULER_API_ENABLED = True

def start_currency_candles(currency):
    currencyPair = cc.CurrencyCandles('USDT_' + currency.upper())

    @scheduler.task("interval", id="update_"+currencyPair.key, seconds=BASE_UPDATE_SCHEDULE_PERIOD, misfire_grace_time = None)
    def update_currency_value(): 
        currencyPair.updateCurrencyCandles()
        
    @scheduler.task("interval", id="candle_60_"+currencyPair.key, seconds=CANDLE_60_SECONDS_PERIOD, misfire_grace_time = None)
    def add_1_min_candle():
        candle = currencyPair.candle_60_seconds
        databaseMySQL.update_1_min_candle(2, candle.getCandleMin(), currency)
    
    @scheduler.task("interval", id="candle_300_"+currencyPair.key, seconds=CANDLE_300_SECONDS_PERIOD, misfire_grace_time = None)
    def add_5_min_candle():
        candle = currencyPair.candle_300_seconds
        databaseMySQL.update_5_min_candle(candle.getCandleMax(), candle.getCandleMin(), currency)

    @scheduler.task("interval", id="candle_600_"+currencyPair.key, seconds=CANDLE_600_SECONDS_PERIOD, misfire_grace_time = None)
    def add_10_min_candle():
        candle = currencyPair.candle_600_seconds
        databaseMySQL.update_10_min_candle(candle.getCandleMax(), candle.getCandleMin(), currency)
 
    logging.info("{} - Starting task for {}".format(datetime.now(), currency))


app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def hello_world():
    return databaseMySQL.select_currency('BTC')

if __name__ == "__main__":   
    # Init log file
    logging.basicConfig(filename='Execution_log.log', 
                        encoding='utf-8',
                        level=logging.INFO)
    for currency in currency_list:
        start_currency_candles(currency)
    scheduler.init_app(app)
    scheduler.start()
    app.run()
    
    
    

