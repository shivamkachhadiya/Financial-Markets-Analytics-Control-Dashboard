import yfinance as yf
import pandas as pd

tickers = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BZ=F", "^TNX"]

data = yf.download(tickers, start="2025-01-01", auto_adjust=True)
raw_prices = data["Close"]

print("\n========== RAW PRICES ==========")
print(raw_prices.tail())

print("\n========== DATA SHAPE ==========")
print(raw_prices.shape)

print("\n========== MISSING VALUES ==========")
print(raw_prices.isna().sum())

prices = raw_prices.ffill()
prices = prices.dropna()

returns = prices.pct_change()
returns["^TNX"] = prices["^TNX"].diff()
returns = returns.dropna()

print("\n========== RETURNS ==========")
print(returns.tail())
print("\nReturns shape:", returns.shape)

correlation = returns.corr()

print("\n========== CORRELATION ==========")
print(correlation.round(2))

missing_values = raw_prices.isna().sum()
duplicate_dates = raw_prices.index.duplicated().sum()
invalid_prices = (raw_prices <= 0).sum()

z_score = (returns - returns.mean()) / returns.std()
abnormal_moves = z_score.abs() > 3

print("\n========== DATA QUALITY ==========")
print("Missing values:", missing_values)
print("Duplicate dates:", duplicate_dates)
print("Invalid prices:", invalid_prices)
print("Abnormal moves:", abnormal_moves.sum())


print("===============================EXCEPTIONS=========================================================================")
exceptions = []

for asset in raw_prices.columns:
    missing_dates = raw_prices.index[raw_prices[asset].isna()]
    for date in missing_dates:
        exceptions.append({"date": date, "asset": asset, "issue": "Missing value", "value": None})

    invalid_dates = raw_prices.index[raw_prices[asset] <= 0]
    for date in invalid_dates:
        exceptions.append({"date": date, "asset": asset, "issue": "Invalid price", "value": raw_prices.loc[date, asset]})

    abnormal_dates = z_score.index[abnormal_moves[asset]]
    for date in abnormal_dates:
        exceptions.append({"date": date, "asset": asset, "issue": "Abnormal move", "value": returns.loc[date, asset]})

report = pd.DataFrame(exceptions, columns=["date", "asset", "issue", "value"])

print("\n========== EXCEPTION REPORT ==========")
print(report.head(20))

print("\n========== EXCEPTION COUNT ==========")
print(report.groupby("issue").size())

report.to_csv("exceptions_report.csv", index=False)

print("\nException report saved successfully.")