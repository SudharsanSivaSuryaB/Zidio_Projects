
"""Preprocessing utilities: load CSV, handle missing values, create train/test splits."""
import pandas as pd
import os
from typing import Tuple

# def load_csv(path: str) -> pd.DataFrame:
#     df = pd.read_csv(path, parse_dates=True, index_col=0)
#     # Ensure datetime index
#     if not isinstance(df.index, pd.DatetimeIndex):
#         df.index = pd.to_datetime(df.index)
#     return df



def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Drop metadata rows (where first column is not a date)
    # Example: "Ticker,AAPL"
    df = df[~df.iloc[:, 0].astype(str).str.contains("Ticker", na=False)]

    # Case 1: Date column exists
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.set_index('Date', inplace=True)
    else:
        # Use first column as date
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0], errors='coerce')
        df.set_index(df.columns[0], inplace=True)

    # Drop any rows with invalid dates
    df = df[~df.index.isna()]

    # Convert all other columns to numeric
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with NaNs (from parsing errors)
    df = df.dropna()

    return df

def prepare_series(df: pd.DataFrame, column: str = 'Close') -> pd.DataFrame:
    # Keep only Close price and drop NaNs
    s = df[[column]].rename(columns={column: 'y'}).copy()
    s = s.dropna()
    return s

def train_test_split(series_df: pd.DataFrame, test_size: int = 90) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # test_size can be number of days for test set
    train = series_df.iloc[:-test_size]
    test = series_df.iloc[-test_size:]
    return train, test

if __name__ == '__main__':
    p = os.path.join(os.path.dirname(__file__), '..', 'data', 'AAPL.csv')
    if os.path.exists(p):
        df = load_csv(p)
        s = prepare_series(df)
        train, test = train_test_split(s)
        print(train.tail())
        print(test.head())
