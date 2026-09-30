import yfinance as yf
import numpy as np
df = yf.download("RELIANCE.NS", start="2025-01-01", auto_adjust=True)

print(df.head())
print(df.tail())
print(df.shape)

close = df["Close"].squeeze()
print("DF INFO===============================================")
print(df.info())

print("CLOSE TAIL INFO========================================")
print(close.tail())

print("CLOSE ISNA AND SUM INFO===============================")
print(close.isna().sum())


returns = close.pct_change()
print("returns=============================================")
print(returns.tail())
print(returns.describe())

log_returns=np.log(close/close.shift(1))
vol=returns.rolling(20).std()*np.sqrt(252)

print("log returns tail==================================")
print(log_returns.tail())

print("volatitlity tail======================================")
print(vol.tail())
print("latest annualized volatility: ",vol.iloc[-1])

print("================================================")

running_max = close.cummax()
drawdown = close / running_max - 1
max_dd = drawdown.min()
print("=========RUNNING MAX===========")
print(drawdown.tail())
print("Max drawdown:", max_dd)
print("Max drawdown date:", drawdown.idxmin())


