
"""Evaluation metrics for forecasts"""
import numpy as np
import pandas as pd

def mse(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean((y_true - y_pred)**2)

def rmse(y_true, y_pred):
    return np.sqrt(mse(y_true, y_pred))

def mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-9))) * 100.0

if __name__ == '__main__':
    import numpy as np
    y = np.array([1,2,3])
    print('rmse', rmse(y, y+0.1))
