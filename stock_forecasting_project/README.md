
# Stock Forecasting Project

This project shows a full example of time series analysis and forecasting for stock market data.
It includes examples for data collection, preprocessing, models (ARIMA, SARIMA, Prophet, LSTM), evaluation,
and a simple Streamlit dashboard. Install dependencies from `requirements.txt` and run scripts as needed.

Structure:
```
stock_forecasting_project/
├── data/
├── notebooks/
├── src/
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── visualization.py
│   ├── models/
│   │   ├── arima_model.py
│   │   ├── sarima_model.py
│   │   ├── prophet_model.py
│   │   ├── lstm_model.py
│   └── evaluation.py
├── dashboard/
│   └── app.py
├── requirements.txt
└── README.md
```

Notes:
- The code expects Python 3.8+.
- `prophet` (the package formerly `fbprophet`) may require pystan or cmdstanpy. See requirements.
- LSTM uses TensorFlow / Keras.
- The `data_loader.py` uses `yfinance` to download data when executed.


`Train` = historical data used to fit the model.

`Test` = recent unseen data used to evaluate how well the model forecasts.

`Forecast/Prediction` = the model’s predicted values plotted against the actual test values.

`python run_pipeline.py` -- Run Command