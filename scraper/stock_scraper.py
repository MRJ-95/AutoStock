import mysql.connector
from configparser import ConfigParser
import time
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os

# Load configuration
config = ConfigParser()
config.optionxform = str  # Preserve case sensitivity
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config', 'config.ini')
config.read(config_path, encoding='utf-8')

print("Loaded Config Sections:", config.sections())  # Debugging line to confirm it's loading properly


def get_db_connection():
    return mysql.connector.connect(
        host=config.get('mysql', 'host'),
        user=config.get('mysql', 'user'),
        password=config.get('mysql', 'password'),
        database=config.get('mysql', 'database')
    )

def get_stock_data(symbol):
    try:
        ts = TimeSeries(
            key=config.get('alpha_vantage', 'api_key'),
            output_format='pandas',
            indexing_type='date'
        )
        
        # Get intraday data
        data, _ = ts.get_intraday(
            symbol=symbol,
            interval='15min',
            outputsize='compact'
        )
        
        # Process latest data point
        latest = data.iloc[0]
        return {
            'symbol': symbol,
            'timestamp': latest.name.to_pydatetime(),
            'open': float(latest['1. open']),
            'high': float(latest['2. high']),
            'low': float(latest['3. low']),
            'close': float(latest['4. close']),
            'volume': int(latest['5. volume'])
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}")
        return None

def store_data(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
        INSERT INTO stock_data 
        (symbol, timestamp, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (
            data['symbol'],
            data['timestamp'],
            data['open'],
            data['high'],
            data['low'],
            data['close'],
            data['volume']
        ))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    symbols = ['GOOGL', 'AAPL', 'MSFT', 'AMZN']
    for symbol in symbols:
        print(f"Processing {symbol}...")
        data = get_stock_data(symbol)
        if data:
            store_data(data)
            print(f"Stored data for {symbol}")
        time.sleep(12)  # Vantage Alpha API rate limit is 5 calls per minute so 12 seconds per call.