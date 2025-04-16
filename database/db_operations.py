import mysql.connector
from configparser import ConfigParser

def get_historical_data(symbol):
    config = ConfigParser()
    config.read('config/config.ini')
    
    conn = mysql.connector.connect(
        host=config['mysql']['host'],
        user=config['mysql']['user'],
        password=config['mysql']['password'],
        database=config['mysql']['database']
    )
    
    query = f"SELECT date, price FROM stock_data WHERE symbol = '{symbol}' ORDER BY date"
    df = pd.read_sql(query, conn)
    conn.close()
    return df