import CurrencyCandles as cc
import DatabaseMySQL as db
from datetime import datetime
import sched, time
from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from redis import Redis
from flask_mysqlpool import MySQLPool

# Global variables to setup the program
# Period in seconds of the task that gets current currency values from Poloniex
# Value chosen due to system limitations
BASE_UPDATE_SCHEDULE_PERIOD = 2 
CANDLE_60_SECONDS_PERIOD = 60 # Period of the task - update the 1 min candle
CANDLE_300_SECONDS_PERIOD = 60 # Period of the task - update the 5 min candle
CANDLE_600_SECONDS_PERIOD = 60 # Period of the task - update the 10 min candle

# Currency list that will be used
currency_list = ['BTC', 'XMR'] # Bitcoin BTC and Monero XMR
#scheduler = APScheduler()
scheduler = BackgroundScheduler()

class Config:
    """Flask app configuration."""
    # Use threads to assure it's possible to do multiple tasks at the same time
    SCHEDULER_EXECUTORS = {"default": {"type": "threadpool", "max_workers": 200}}
    # Avoid having too many executions at once, but gives window to a possible time lag
    SCHEDULER_JOB_DEFAULTS = {"coalesce": True, "max_instances": 1}
    SCHEDULER_API_ENABLED = True
    
    # Set pretty JSON and block key sort
    JSONIFY_PRETTYPRINT_REGULAR = False
    JSON_SORT_KEYS = False

    # Database configuration
    MYSQL_HOST = "sql5.freemysqlhosting.net"
    MYSQL_PORT = 3306
    MYSQL_USER = "sql5411831"
    MYSQL_PASS = "KjHuJeWGEV"
    MYSQL_DB = "sql5411831"
    MYSQL_POOL_NAME = 'mypool'
    MYSQL_POOL_SIZE = 8
    MYSQL_AUTOCOMMIT = True

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
databaseMySQL = db.DatabaseMySQL(MySQLPool(app))
app.config.from_object(Config())

@app.route('/currency_sumary')
def get_currency_sumary():
    try:
        return jsonify(databaseMySQL.get_select_currency(request.args.get('currency', default = 'BTC', type = str)))
    except ex:
        return jsonify(db.HttpResponse(500, "Failed to obtain data"))

@app.route('/currency_sumary/all')
def get_currency_all():
    try:
        return jsonify(databaseMySQL.get_select_all())
    except ex:
        return jsonify(db.HttpResponse(500, "Failed to obtain data"))
        
def start_currency_candles(currency):
    """
    Schedulers to USDT - Desired_currency pairs
    """
    currencyPair = cc.CurrencyCandles('USDT_' + currency.upper())

    def update_currency_value(): 
        """
        Get values from Poloniex server
        """
        currencyPair.updateCurrencyCandles()
        
    def add_1_min_candle():
        """
        Updates 1 min candle to the MySQL server
        """
        candle = currencyPair.candle_60_seconds
        databaseMySQL.update_1_min_candle(candle.getCandleMax(), candle.getCandleMin(),
                                        candle.getOpen(), candle.getClose(),
                                        currency)
        logging.info("1 min candle updated")
        
    def add_5_min_candle():
        """
        Updates 5 min candle to the MySQL server
        """
        candle = currencyPair.candle_300_seconds
        databaseMySQL.update_5_min_candle(candle.getCandleMax(), candle.getCandleMin(),
                                        candle.getOpen(), candle.getClose(),
                                        currency)
        logging.info("5 min candle updated")
    
    def add_10_min_candle():
        """
        Updates 10 min candle to the MySQL server
        """
        candle = currencyPair.candle_600_seconds
        databaseMySQL.update_10_min_candle(candle.getCandleMax(), candle.getCandleMin(),
                                        candle.getOpen(), candle.getClose(),
                                        currency)
        logging.info("10 min candle updated")
    
    logging.info("{} - Starting task for {}".format(datetime.now(), currency))
    
    scheduler.add_job(id=currency + "_update", name=currency + "_update", func=update_currency_value, trigger="interval", seconds=BASE_UPDATE_SCHEDULE_PERIOD)
    scheduler.add_job(id=currency + "_1min_candle", name=currency + "_1min_candle", func=add_1_min_candle, trigger="interval", seconds=CANDLE_60_SECONDS_PERIOD)
    scheduler.add_job(id=currency + "_5min_candle", name=currency + "_5min_candle", func=add_5_min_candle, trigger="interval", seconds=CANDLE_300_SECONDS_PERIOD)
    scheduler.add_job(id=currency + "_10min_candle", name=currency + "_10min_candle", func=add_10_min_candle, trigger="interval", seconds=CANDLE_600_SECONDS_PERIOD)


if __name__ == "__main__":      
    # Init log file
    logging.basicConfig(filename='Execution_log.log', 
                        level=logging.INFO)
    logging.warning("{} - Starting the Scheduler".format(datetime.now()))
    
    # Init currency list
    for currency in currency_list:
        if (currency in cc.disponible_currencies):
            logging.info("Logging currency {}".format(currency))
            start_currency_candles(currency)
        else:
            logging.warning("Currency {} not disponible, it will be ignored during the execution".format(currency))
    
    # Create the tasks and run the app
    scheduler.start()
    app.run(host="0.0.0.0", debug=True)
    
    
    

