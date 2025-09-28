
"""Download historical stock data using yfinance and save CSVs to data/"""
import yfinance as yf
import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DATA_DIR = os.path.abspath(DATA_DIR)

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    return DATA_DIR

def download_ticker(ticker: str, period: str = "5y", interval: str = "1d"):
    ensure_data_dir()
    print(f"Downloading {ticker} period={period} interval={interval} ...")
    df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"Empty data returned for {ticker}")
    out = os.path.join(DATA_DIR, f"{ticker.replace('^','')}.csv")
    df.to_csv(out)
    print(f"Saved to {out}")
    return out

if __name__ == '__main__':
    # Example: python src/data_loader.py
    # Downloads Apple 5 years daily
    download_ticker('AAPL', period='5y', interval='1d')
