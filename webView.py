import DatabaseMySQL as db
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return databaseMySQL.select_currency('BTC')


if __name__ == "__main__":  
    databaseMySQL = db.DatabaseMySQL()   
    app.run(debug=True, host='0.0.0.0')