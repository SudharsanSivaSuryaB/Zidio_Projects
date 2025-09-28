
"""SARIMA example using statsmodels"""
from statsmodels.tsa.statespace.sarimax import SARIMAX

def fit_sarima(train_series, order=(1,1,1), seasonal_order=(0,0,0,0)):
    model = SARIMAX(train_series['y'], order=order, seasonal_order=seasonal_order, enforce_stationarity=False, enforce_invertibility=False)
    res = model.fit(disp=False)
    return res

def forecast(res, steps=30):
    pred = res.get_forecast(steps=steps)
    mean = pred.predicted_mean
    conf = pred.conf_int()
    return mean, conf
