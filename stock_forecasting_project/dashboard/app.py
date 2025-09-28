
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from src.data_loader import download_ticker
from src.preprocessing import load_csv, prepare_series, train_test_split
from src.models.arima_model import fit_arima, forecast as arima_forecast
from src.models.sarima_model import fit_sarima, forecast as sarima_forecast
from src.models.prophet_model import fit_prophet, forecast as prophet_forecast
from src.models.lstm_model import fit_lstm, forecast_lstm
from src.evaluation import rmse, mape

st.set_page_config(page_title="Stock Forecasting Dashboard", layout="wide")
st.title("📈 Stock Forecasting (ARIMA, SARIMA, Prophet, LSTM)")

# Sidebar inputs
ticker = st.sidebar.text_input("Enter Stock Ticker", "AAPL")
test_size = st.sidebar.number_input("Test size (days)", min_value=30, max_value=180, value=60)
period = st.sidebar.selectbox("Download period", ["1y", "2y", "5y"], index=1)

if st.sidebar.button("Run Forecast"):
    try:
        # Step 1: Data download
        data_path = download_ticker(ticker, period=period)
        df = load_csv(data_path)
        series = prepare_series(df)
        train, test = train_test_split(series, test_size=test_size)

        st.subheader(f"Stock Data for {ticker}")
        st.line_chart(series["y"])

        results = {}
        forecasts = {}

        # ARIMA
        try:
            arima_res = fit_arima(train, order=(5,1,0))
            mean, _ = arima_forecast(arima_res, steps=test_size)
            results["ARIMA"] = {"rmse": rmse(test["y"], mean), "mape": mape(test["y"], mean)}
            forecasts["ARIMA"] = mean
        except Exception as e:
            st.error(f"ARIMA failed: {e}")

        # SARIMA
        try:
            sarima_res = fit_sarima(train, order=(1,1,1), seasonal_order=(1,1,1,12))
            mean, _ = sarima_forecast(sarima_res, steps=test_size)
            results["SARIMA"] = {"rmse": rmse(test["y"], mean), "mape": mape(test["y"], mean)}
            forecasts["SARIMA"] = mean
        except Exception as e:
            st.error(f"SARIMA failed: {e}")

        # Prophet
        try:
            prophet_train = train.reset_index().rename(columns={"index": "ds"})
            prophet_train.rename(columns={"y": "y"}, inplace=True)
            m = fit_prophet(prophet_train)
            forecast_df = prophet_forecast(m, periods=test_size)
            y_pred = forecast_df.tail(test_size)["yhat"].values
            results["Prophet"] = {"rmse": rmse(test["y"], y_pred), "mape": mape(test["y"], y_pred)}
            forecasts["Prophet"] = pd.Series(y_pred, index=test.index)
        except Exception as e:
            st.error(f"Prophet failed: {e}")

        # LSTM
        try:
            model, scaler = fit_lstm(train, look_back=20, epochs=5, verbose=0)
            preds = forecast_lstm(model, scaler, train["y"].values, steps=test_size, look_back=20)
            results["LSTM"] = {"rmse": rmse(test["y"], preds), "mape": mape(test["y"], preds)}
            forecasts["LSTM"] = pd.Series(preds, index=test.index)
        except Exception as e:
            st.error(f"LSTM failed: {e}")

        # Show metrics
        if results:
            st.subheader("📊 Model Performance")
            st.dataframe(pd.DataFrame(results).T)

        # Show plots
        st.subheader("🔮 Forecasts vs Actual")
        for model, preds in forecasts.items():
            fig, ax = plt.subplots(figsize=(10,4))
            ax.plot(train.index, train["y"], label="Train")
            ax.plot(test.index, test["y"], label="Test", color="black")
            ax.plot(test.index, preds, label=f"{model} Forecast", linestyle="--")
            ax.set_title(f"{model} Forecast vs Actual")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Pipeline failed: {e}")
