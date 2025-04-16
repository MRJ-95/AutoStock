import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from db_operations import get_historical_data

def predict_stock(symbol):
    # Get historical data
    data = get_historical_data(symbol)
    
    # Feature engineering
    data['days'] = (data['date'] - data['date'].min()).dt.days
    X = data[['days']]
    y = data['price']
    
    # Train model
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Predict next day
    next_day = data['days'].max() + 1
    prediction = model.predict([[next_day]])
    
    return prediction[0]

if __name__ == "__main__":
    symbol = 'AAPL'
    print(f"Predicted price for {symbol}: {predict_stock(symbol)}")