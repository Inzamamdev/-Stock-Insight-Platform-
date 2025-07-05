import os
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score
from decouple import config
from django.conf import settings

def predict_stock(ticker, user):
    ticker = ticker.upper() 

    # Load model
    model_path = config('MODEL_PATH', default='stock_prediction_model.keras')
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    
    model = load_model(model_path)

    # Get historical data
    df = yf.download(ticker, period="10y")
    if df.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
    
    data = df[['Close']].values
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i])
        y.append(scaled_data[i])
    X, y = np.array(X), np.array(y)

    # Predict
    predictions = model.predict(X)
    predicted_next = model.predict(np.expand_dims(scaled_data[-60:], axis=0))
    next_day_price = scaler.inverse_transform(predicted_next)[0][0]

    # Metrics
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y, predictions)

    # Save plots
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    plot_dir = os.path.join(settings.BASE_DIR, 'static', 'plots')
    os.makedirs(plot_dir, exist_ok=True)
    plot1_path = os.path.join(plot_dir, f"{ticker}_history_{timestamp}.png")
    plot2_path = os.path.join(plot_dir, f"{ticker}_predicted_{timestamp}.png")

    # Plot 1: Historical closing prices
    plt.figure()
    df['Close'].plot(title="Closing Price History")
    plt.savefig(plot1_path)
    plt.close()

    # Plot 2: Actual vs Predicted
    plt.figure()
    plt.plot(scaler.inverse_transform(y), label='Actual')
    plt.plot(scaler.inverse_transform(predictions), label='Predicted')
    plt.legend()
    plt.title("Actual vs Predicted")
    plt.savefig(plot2_path)
    plt.close()

    # Save to DB
    from .models import Prediction
    prediction = Prediction.objects.create(
        user=user,
        ticker=ticker,
        next_day_price=next_day_price,
        metrics={'mse': mse, 'rmse': rmse, 'r2': r2},
        plot_1_path=plot1_path,
        plot_2_path=plot2_path
    )

    return {
        "next_day_price": next_day_price,
        "mse": mse,
        "rmse": rmse,
        "r2": r2,
          "plot_urls": [str(plot1_path).replace(str(settings.BASE_DIR), ''), 
                              str(plot2_path).replace(str(settings.BASE_DIR), ''),],
        
    }
