import yfinance as yf

sectors = {
    "Nifty 50": "^NSEI",
    "Bank": "^NSEBANK",
    "IT": "^CNXIT",
    "Pharma": "^CNXPHARMA",
    "Auto (Maruti)": "MARUTI.NS",
    "FMCG (HUL)": "HINDUNILVR.NS",
    "Metal (Tata Steel)": "TATASTEEL.NS",
    "Energy (ONGC)": "ONGC.NS",
}
for name, symbol in sectors.items():
    df = yf.download(symbol, start="2025-01-01", auto_adjust=True, progress=False)

    if df.empty:
        print(name, "-> no data")
        continue

    close = df["Close"].iloc[:, 0]
  
    if len(close) < 22:
        print(name, "-> not enough data, rows:", len(close))
        continue

    total = (close.iloc[-1] / close.iloc[0] - 1) * 100
    month = (close.iloc[-1] / close.iloc[-22] - 1) * 100

    print(name, "| Total:", round(total, 2), "% | 1 month:", round(month, 2), "%")