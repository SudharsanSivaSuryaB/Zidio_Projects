
"""LSTM example using TensorFlow/Keras for univariate forecasting."""
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import MinMaxScaler

def create_dataset(series, look_back=20):
    X, y = [], []
    for i in range(len(series)-look_back):
        X.append(series[i:(i+look_back)])
        y.append(series[i+look_back])
    return np.array(X), np.array(y)

def build_lstm(input_shape):
    model = Sequential()
    model.add(LSTM(64, input_shape=input_shape, activation='tanh'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def fit_lstm(train_series, look_back=20, epochs=50, batch_size=16, verbose=1):
    scaler = MinMaxScaler()
    arr = train_series['y'].values.reshape(-1,1)
    arr_scaled = scaler.fit_transform(arr)
    X, y = create_dataset(arr_scaled.flatten(), look_back=look_back)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    model = build_lstm((X.shape[1], X.shape[2]))
    es = EarlyStopping(monitor='loss', patience=5, restore_best_weights=True)
    model.fit(X, y, epochs=epochs, batch_size=batch_size, callbacks=[es], verbose=verbose)
    return model, scaler

def forecast_lstm(model, scaler, history_series, steps=30, look_back=20):
    # history_series: array-like of most recent values (unscaled)
    seq = list(history_series[-look_back:])
    preds = []
    for _ in range(steps):
        arr = np.array(seq[-look_back:]).reshape(-1,1)
        arr_scaled = scaler.transform(arr).flatten()
        X = arr_scaled.reshape((1, look_back, 1))
        p = model.predict(X, verbose=0)[0,0]
        # inverse scale
        p_inv = scaler.inverse_transform([[p]])[0,0]
        preds.append(p_inv)
        seq.append(p_inv)
    return preds
