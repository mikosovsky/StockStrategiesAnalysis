import yfinance as yf
import pandas as pd
import numpy as np
import ccxt
import mplfinance as mpf

def download_stock_data(ticker, period, interval):
    df = yf.download(ticker, period=period, interval=interval)
    df.columns = df.columns.droplevel(1)
    return df

def download_crypto_data(symbol, timeframe, since):
    exchange = ccxt.binance()
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df.rename(columns={
        'timestamp': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)
    return df

def mean_reversion(df):
    df['IBS'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
    df['HL_avg'] = df['High'].rolling(window=25).mean() - df['Low'].rolling(window=25).mean()
    df['Band'] = df['High'].rolling(window=25).mean() - 2.25 * df['HL_avg']
    return df

def plot_backtesting_results(df, backtesting_data):
    ap = [
        mpf.make_addplot(backtesting_data['Entry'], type='scatter', markersize=100, marker='^', color='g'),
        mpf.make_addplot(backtesting_data['Exit'], type='scatter', markersize=100, marker='v', color='r')
    ]

    mpf.plot(
        df,
        type='candle',
        addplot=ap,
        volume=False,
        style='yahoo',
        title='Mean Reversion Strategy Backtest',
        tight_layout=True
    )