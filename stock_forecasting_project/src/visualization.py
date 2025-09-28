
"""Simple plotting helpers using matplotlib/plotly."""
import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_series(series_df, title='Series', savepath=None):
    plt.figure(figsize=(12,5))
    plt.plot(series_df.index, series_df['y'], label='y')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.legend()
    plt.tight_layout()
    if savepath:
        os.makedirs(os.path.dirname(savepath), exist_ok=True)
        plt.savefig(savepath)
    else:
        plt.show()

if __name__ == '__main__':
    p = os.path.join(os.path.dirname(__file__), '..', 'data', 'AAPL.csv')
    if os.path.exists(p):
        import preprocessing as pp
        df = pp.load_csv(p)
        s = pp.prepare_series(df)
        plot_series(s, title='AAPL Close')
