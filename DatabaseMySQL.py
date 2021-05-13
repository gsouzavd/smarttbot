import mysql.connector
import json
from datetime import datetime
import CurrencyCandles as cc

class DatabaseMySQL:
    def __init__(self):
        self.__create_databse_connection()
        self.__create_MySQL_queries()
    
    def __create_databse_connection(self):
        # Create the MySQL Connection
        self.databaseMySQL = mysql.connector.connect(
            host="sql5.freemysqlhosting.net",
            user="sql5411831",
            password="KjHuJeWGEV",
            database="sql5411831",
            port="3306"
        )
        self.mycursor = self.databaseMySQL.cursor()

    def __create_MySQL_queries(self):
        self.__sql_select = "SELECT * FROM sql5411831.Candles WHERE currencyPair = %s"
        self.__sql_update_24h = "UPDATE sql5411831.Candles SET high24h = %s, low24h = %s, updateDate = %s WHERE currencyPair = %s"
        self.__sql_update_1min = "UPDATE sql5411831.Candles SET high1min = %s, low1min = %s, updateDate = %s WHERE currencyPair = %s"
        self.__sql_update_5min = "UPDATE sql5411831.Candles SET high5min = %s, low5min = %s, updateDate = %s WHERE currencyPair = %s"
        self.__sql_update_10min = "UPDATE sql5411831.Candles SET high10min = %s, low10min = %s, updateDate = %s WHERE currencyPair = %s"

    def __create_currencies_table(self):
        sql = "INSERT INTO sql5411831.Candles (currencyPair, updateDate) VALUES (%s, %s)"
        for currency in cc.disponible_currencies:
            val = (currency, datetime.now())
            self.mycursor.execute(sql, val, multi=True)
            self.databaseMySQL.commit()

    def __to_JSON(self, fetchResponse):
        json_data=[]
        row_headers=[x[0] for x in self.mycursor.description]
        for result in fetchResponse:
            json_data.append(dict(zip(row_headers,result)))
        # Updates table to a new version
        try:
            self.databaseMySQL.commit()
        except Exception as e:
            self.databaseMySQL.rollback()
            raise e
        return json.dumps(json_data)

    def select_currency(self, currency):
        currency = 'USDT_' + currency.upper()
        val = (currency,)
        self.mycursor.execute(self.__sql_select, val)
        return self.__to_JSON(self.mycursor.fetchall())

    def update_1_min_candle(self, high, low, currency):
        currency = 'USDT_' + currency.upper()
        val = (high, low, datetime.now(), currency,)
        try:
            self.mycursor.execute(self.__sql_update_1min, val, multi=True)
            self.databaseMySQL.commit()
        except Exception as e:
            self.__create_databse_connection()

    def update_5_min_candle(self, high, low, currency):
        currency = 'USDT_' + currency.upper()
        val = (high, low, datetime.now(), currency,)
        try:
            self.mycursor.execute(self.__sql_update_5min, val, multi=True)
            self.databaseMySQL.commit()
        except Exception as e:
            self.__create_databse_connection()

    def update_10_min_candle(self, high, low, currency):
        currency = 'USDT_' + currency.upper()
        val = (high, low, datetime.now(), currency,)
        try:
            self.mycursor.execute(self.__sql_update_10min, val, multi=True)
            self.databaseMySQL.commit()
        except Exception as e:
            self.__create_databse_connection()
        #return self.__to_JSON(self.mycursor.fetchall())

