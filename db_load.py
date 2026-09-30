import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

PASSWORD = "root123"

url = URL.create(
    "postgresql+psycopg",
    username="postgres",
    password=PASSWORD,
    host="localhost",
    port=5432,
    database="market_db",
)
engine = create_engine(url)


def to_long(path, value_name):
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    df.index.name = "date"
    return df.reset_index().melt(id_vars="date", var_name="asset", value_name=value_name)


prices = to_long("prices_clean.csv", "price")
returns = to_long("returns.csv", "return_value")
volatility = to_long("volatility.csv", "volatility").dropna()
drawdown = to_long("drawdown.csv", "drawdown")

exceptions = pd.read_csv("exceptions_report.csv", parse_dates=["date"])
sector = pd.read_csv("sector_performance.csv")

corr = pd.read_csv("correlation.csv", index_col=0)
corr.index.name = "asset"
corr = corr.reset_index()

tables = {
    "prices": prices,
    "returns": returns,
    "volatility": volatility,
    "drawdown": drawdown,
    "exceptions": exceptions,
    "sector_performance": sector,
    "correlation": corr,
}

for name, df in tables.items():
    df.to_sql(name, engine, if_exists="replace", index=False)
    print(name, "->", len(df), "rows loaded")