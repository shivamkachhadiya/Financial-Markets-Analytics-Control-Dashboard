import yfinance as yf
import pandas as pd

TICKERS = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BZ=F", "^TNX"]
START = "2025-01-01"

SECTORS = {
    "Nifty 50": "^NSEI",
    "Bank": "^NSEBANK",
    "IT": "^CNXIT",
    "Pharma": "^CNXPHARMA",
    "Auto (Maruti)": "MARUTI.NS",
    "FMCG (HUL)": "HINDUNILVR.NS",
    "Metal (Tata Steel)": "TATASTEEL.NS",
    "Energy (ONGC)": "ONGC.NS",
}


def load_prices(tickers, start):
    data = yf.download(tickers, start=start, auto_adjust=True, progress=False)
    return data["Close"]


def clean_prices(raw):
    return raw.ffill().dropna()


def calc_returns(prices):
    returns = prices.pct_change()
    returns["^TNX"] = prices["^TNX"].diff()
    return returns.dropna()


def find_exceptions(raw, returns, z_limit=3):
    rows = []
    z = (returns - returns.mean()) / returns.std()

    for date in raw.index[raw.index.duplicated()]:
        rows.append({"date": date, "asset": "ALL", "issue": "Duplicate date", "value": None})

    for col in raw.columns:
        for date in raw.index[raw[col].isna().values]:
            rows.append({"date": date, "asset": col, "issue": "Missing value", "value": None})

        for date in raw.index[(raw[col] <= 0).values]:
            rows.append({"date": date, "asset": col, "issue": "Invalid price", "value": raw.loc[date, col]})

        for date in z.index[(z[col].abs() > z_limit).values]:
            rows.append({"date": date, "asset": col, "issue": "Abnormal move", "value": returns.loc[date, col]})

    return pd.DataFrame(rows, columns=["date", "asset", "issue", "value"])


def calc_volatility(returns, window=20):
    return returns.rolling(window).std() * (252 ** 0.5)


def calc_drawdown(prices):
    prices = prices.drop(columns=["^TNX"])
    return prices / prices.cummax() - 1


def calc_correlation(returns):
    return returns.corr()


def calc_sector_performance(sectors, start):
    rows = []
    for name, symbol in sectors.items():
        df = yf.download(symbol, start=start, auto_adjust=True, progress=False)
        if df.empty:
            continue
        close = df["Close"].iloc[:, 0]
        if len(close) < 22:
            continue
        rows.append({
            "sector": name,
            "total_return_pct": round((close.iloc[-1] / close.iloc[0] - 1) * 100, 2),
            "one_month_pct": round((close.iloc[-1] / close.iloc[-22] - 1) * 100, 2),
        })
    return pd.DataFrame(rows).sort_values("total_return_pct", ascending=False)


def main():
    raw = load_prices(TICKERS, START)
    prices = clean_prices(raw)
    returns = calc_returns(prices)
    exceptions = find_exceptions(raw, returns)

    vol = calc_volatility(returns)
    drawdown = calc_drawdown(prices)
    corr = calc_correlation(returns)
    sector = calc_sector_performance(SECTORS, START)

    prices.to_csv("prices_clean.csv")
    returns.to_csv("returns.csv")
    exceptions.to_csv("exceptions_report.csv", index=False)
    vol.to_csv("volatility.csv")
    drawdown.to_csv("drawdown.csv")
    corr.to_csv("correlation.csv")
    sector.to_csv("sector_performance.csv", index=False)

    print("Exceptions found:", len(exceptions))
    print()
    print("Latest annualized volatility:")
    print(vol.iloc[-1].round(3))
    print()
    print("Max drawdown:")
    print(drawdown.min().round(3))
    print()
    print("Correlation:")
    print(corr.round(2))
    print()
    print("Sector performance:")
    print(sector.to_string(index=False))


if __name__ == "__main__":
    main()