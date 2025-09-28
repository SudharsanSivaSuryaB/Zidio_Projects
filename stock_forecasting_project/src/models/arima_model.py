
"""ARIMA modelling example using statsmodels"""
from statsmodels.tsa.arima.model import ARIMA
import pickle
import os

def fit_arima(train_series, order=(5,1,0)):
    # train_series: pd.Series or pd.DataFrame with single 'y' column and DateTime index
    model = ARIMA(train_series['y'], order=order)
    res = model.fit()
    return res

def forecast(res, steps=30):
    pred = res.get_forecast(steps=steps)
    mean = pred.predicted_mean
    conf = pred.conf_int()
    return mean, conf

if __name__ == '__main__':
    print('ARIMA module. Import and use fit_arima / forecast functions.')
