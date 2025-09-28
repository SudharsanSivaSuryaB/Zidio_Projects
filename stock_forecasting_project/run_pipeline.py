
# """Run the full pipeline: download data, preprocess, train ARIMA/Prophet/LSTM, evaluate."""
# import os
# import pandas as pd

# from src.data_loader import download_ticker
# from src.preprocessing import load_csv, prepare_series, train_test_split
# from src.models.arima_model import fit_arima, forecast as arima_forecast
# from src.models.sarima_model import fit_sarima, forecast as sarima_forecast
# from src.models.prophet_model import fit_prophet, forecast as prophet_forecast
# from src.models.lstm_model import fit_lstm, forecast_lstm
# from src.evaluation import rmse, mape

# TICKER = 'AAPL'
# TEST_SIZE = 60

# def main():
#     print("=== Stock Forecasting Pipeline ===")
#     # Step 1: Download data
#     data_path = download_ticker(TICKER, period='2y')
#     df = load_csv(data_path)
#     series = prepare_series(df)
#     train, test = train_test_split(series, test_size=TEST_SIZE)

#     results = {}

#     # Step 2: ARIMA
#     try:
#         arima_res = fit_arima(train, order=(5,1,0))
#         mean, conf = arima_forecast(arima_res, steps=TEST_SIZE)
#         results['ARIMA'] = {
#             'rmse': rmse(test['y'], mean),
#             'mape': mape(test['y'], mean)
#         }
#         print("ARIMA done.")
#     except Exception as e:
#         print("ARIMA failed:", e)

#     # Step 3: SARIMA (simple seasonal order)
#     try:
#         sarima_res = fit_sarima(train, order=(1,1,1), seasonal_order=(1,1,1,12))
#         mean, conf = sarima_forecast(sarima_res, steps=TEST_SIZE)
#         results['SARIMA'] = {
#             'rmse': rmse(test['y'], mean),
#             'mape': mape(test['y'], mean)
#         }
#         print("SARIMA done.")
#     except Exception as e:
#         print("SARIMA failed:", e)

#     # Step 4: Prophet
#     try:
#         prophet_train = train.reset_index().rename(columns={'index':'ds'})
#         m = fit_prophet(prophet_train)
#         forecast_df = prophet_forecast(m, periods=TEST_SIZE)
#         y_pred = forecast_df.tail(TEST_SIZE)['yhat'].values
#         results['Prophet'] = {
#             'rmse': rmse(test['y'], y_pred),
#             'mape': mape(test['y'], y_pred)
#         }
#         print("Prophet done.")
#     except Exception as e:
#         print("Prophet failed:", e)

#     # Step 5: LSTM
#     try:
#         model, scaler = fit_lstm(train, look_back=20, epochs=5, verbose=0)
#         preds = forecast_lstm(model, scaler, train['y'].values, steps=TEST_SIZE, look_back=20)
#         results['LSTM'] = {
#             'rmse': rmse(test['y'], preds),
#             'mape': mape(test['y'], preds)
#         }
#         print("LSTM done.")
#     except Exception as e:
#         print("LSTM failed:", e)

#     # Save results
#     out_path = os.path.join(os.path.dirname(__file__), 'results.csv')
#     pd.DataFrame(results).T.to_csv(out_path)
#     print("Saved results to", out_path)
#     print(pd.DataFrame(results).T)

# if __name__ == '__main__':
#     main()


import os
import pandas as pd
import matplotlib.pyplot as plt

from src.data_loader import download_ticker
from src.preprocessing import load_csv, prepare_series, train_test_split
from src.models.arima_model import fit_arima, forecast as arima_forecast
from src.models.sarima_model import fit_sarima, forecast as sarima_forecast
from src.models.prophet_model import fit_prophet, forecast as prophet_forecast
from src.models.lstm_model import fit_lstm, forecast_lstm
from src.evaluation import rmse, mape

TICKER = "AAPL"
TEST_SIZE = 60
RESULTS_DIR = "results"

def plot_forecast(train, test, preds, model_name):
    """Plot train, test, and forecasted values."""
    plt.figure(figsize=(12, 5))
    plt.plot(train.index, train["y"], label="Train")
    plt.plot(test.index, test["y"], label="Test", color="black")
    plt.plot(test.index, preds, label=f"{model_name} Forecast", linestyle="--")
    plt.title(f"{model_name} Forecast vs Actual")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    os.makedirs(RESULTS_DIR, exist_ok=True)
    out_path = os.path.join(RESULTS_DIR, f"{model_name}_forecast.png")
    plt.savefig(out_path)
    plt.close()
    print(f"Saved {model_name} plot → {out_path}")

def main():
    print("=== Stock Forecasting Pipeline ===")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Step 1: Download data
    data_path = download_ticker(TICKER, period="2y")
    df = load_csv(data_path)
    series = prepare_series(df)
    train, test = train_test_split(series, test_size=TEST_SIZE)

    results = {}

    # Step 2: ARIMA
    try:
        arima_res = fit_arima(train, order=(5,1,0))
        mean, conf = arima_forecast(arima_res, steps=TEST_SIZE)
        results["ARIMA"] = {"rmse": rmse(test["y"], mean), "mape": mape(test["y"], mean)}
        plot_forecast(train, test, mean, "ARIMA")
    except Exception as e:
        print("ARIMA failed:", e)

    # Step 3: SARIMA
    try:
        sarima_res = fit_sarima(train, order=(1,1,1), seasonal_order=(1,1,1,12))
        mean, conf = sarima_forecast(sarima_res, steps=TEST_SIZE)
        results["SARIMA"] = {"rmse": rmse(test["y"], mean), "mape": mape(test["y"], mean)}
        plot_forecast(train, test, mean, "SARIMA")
    except Exception as e:
        print("SARIMA failed:", e)

    # Step 4: Prophet
    try:
        prophet_train = train.reset_index().rename(columns={"index": "ds"})
        prophet_train.rename(columns={"y": "y"}, inplace=True)
        m = fit_prophet(prophet_train)
        forecast_df = prophet_forecast(m, periods=TEST_SIZE)
        y_pred = forecast_df.tail(TEST_SIZE)["yhat"].values
        results["Prophet"] = {"rmse": rmse(test["y"], y_pred), "mape": mape(test["y"], y_pred)}
        plot_forecast(train, test, y_pred, "Prophet")
    except Exception as e:
        print("Prophet failed:", e)

    # Step 5: LSTM
    try:
        model, scaler = fit_lstm(train, look_back=20, epochs=5, verbose=0)
        preds = forecast_lstm(model, scaler, train["y"].values, steps=TEST_SIZE, look_back=20)
        results["LSTM"] = {"rmse": rmse(test["y"], preds), "mape": mape(test["y"], preds)}
        plot_forecast(train, test, preds, "LSTM")
    except Exception as e:
        print("LSTM failed:", e)

    # Save results
    out_path = os.path.join(RESULTS_DIR, "metrics.csv")
    pd.DataFrame(results).T.to_csv(out_path)
    print("Saved metrics →", out_path)
    print(pd.DataFrame(results).T)

if __name__ == "__main__":
    main()