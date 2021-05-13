import mysql.connector
from mysql.connector import pooling
import json
from datetime import datetime
import CurrencyCandles as cc

class DatabaseMySQL:
    """
    Connects to a MySQL Dabase and Uploads the data to it
    """
    def __init__(self):
        self.__create_databse_connection()
        self.__create_MySQL_queries()
    
    def __create_databse_connection(self):
        # Create the MySQL Connection to a test database
        self.databaseMySQL = pooling.MySQLConnectionPool(
            host="sql5.freemysqlhosting.net",
            user="sql5411831",
            password="KjHuJeWGEV",
            database="sql5411831",
            port="3306",
            pool_name = "mypool",
            pool_size = 10
        )

    def __create_MySQL_queries(self):
        # Queries used by the program
        self.__sql_select = "SELECT * FROM sql5411831.Candles WHERE currencyPair = %s"
        self.__sql_update_24h = "UPDATE sql5411831.Candles SET high24h = %s, low24h = %s, updateDate = %s WHERE currencyPair = %s"
        self.__sql_update_1min = "UPDATE sql5411831.Candles SET high1min = %s, low1min = %s, open1min = %s, close1min = %s, updateDate = %s WHERE currencyPair = %s"
        self.__sql_update_5min = "UPDATE sql5411831.Candles SET high5min = %s, low5min = %s, open5min = %s, close5min = %s, updateDate = %s WHERE currencyPair = %s"
        self.__sql_update_10min = "UPDATE sql5411831.Candles SET high10min = %s, low10min = %s, open10min = %s, close10min = %s, updateDate = %s WHERE currencyPair = %s"

    def get_select_currency(self, currency):
        """
        GET - Get the complete candle data of a currecy in relation to USDT
        @param {currecy} Acronym of the desired currecy
        @returns {json} Json data of the currency 
        """
        currency = 'USDT_' + currency.upper()
        val = (currency,)
        connection_object = self.databaseMySQL.get_connection()
        cursor = connection_object.cursor()
        print(cursor.execute(self.__sql_select, val))
        row_headers = [x[0] for x in cursor.description]
        json_data = []
        for result in cursor.fetchall():
            json_data.append(dict(zip(row_headers,result)))
        connection_object.commit()
        connection_object.close()
        return json.dumps(json_data)

    def update_1_min_candle(self, _high, _low, _open, _close, _currency):
        """
        POST - Update data of the 1 min candle of a currency in relation to USDT
        @param {_high} Highest value the in the candle of the currency
        @param {_low} Lowest value in the candle of the currency
        @param {_open} Open value of the candle of the currency
        @param {_close} Close value of the candle of the currency
        @param {_currecy} Acronym of the desired currecy
        """
        _currency = 'USDT_' + _currency.upper()
        val = (_high, _low, _open, _close, datetime.now(), _currency,)
        self.__send_candle_query(self.__sql_update_1min, val)

    def update_5_min_candle(self, _high, _low, _open, _close, _currency):
        """
        POST - Update data of the 5 min candle of a currency in relation to USDT
        @param {_high} Highest value the in the candle of the currency
        @param {_low} Lowest value in the candle of the currency
        @param {_open} Open value of the candle of the currency
        @param {_close} Close value of the candle of the currency
        @param {_currecy} Acronym of the desired currecy
        """
        _currency = 'USDT_' + _currency.upper()
        val = (_high, _low, _open, _close, datetime.now(), _currency,)
        self.__send_candle_query(self.__sql_update_5min, val)

    def update_10_min_candle(self, _high, _low, _open, _close, _currency):
        """
        POST - Update data of the 10 min candle of a currency in relation to USDT
        @param {_high} Highest value the in the candle of the currency
        @param {_low} Lowest value in the candle of the currency
        @param {_open} Open value of the candle of the currency
        @param {_close} Close value of the candle of the currency
        @param {_currecy} Acronym of the desired currecy
        """
        _currency = 'USDT_' + _currency.upper()
        val = (_high, _low, _open, _close, datetime.now(), _currency,)
        self.__send_candle_query(self.__sql_update_10min, val)

    def __send_candle_query(self, sql, val):
        try:
            # Get a connection object from a pool
            connection_object = self.databaseMySQL.get_connection()
            cursor = connection_object.cursor()
            cursor.execute(sql, val)
            connection_object.commit()
            connection_object.close()
        except ex:
            logging.error("MySQL Error")
            raise ex
