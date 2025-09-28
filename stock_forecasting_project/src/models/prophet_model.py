
"""Prophet example. Uses `prophet` package (previously fbprophet)."""
from prophet import Prophet
import pandas as pd

def fit_prophet(train_df):
    # train_df should have columns ds (datetime) and y (value)
    m = Prophet(daily_seasonality=True)
    m.fit(train_df.reset_index().rename(columns={'index':'ds'}))
    return m

def forecast(m, periods=30, freq='D'):
    future = m.make_future_dataframe(periods=periods, freq=freq)
    forecast = m.predict(future)
    return forecast
