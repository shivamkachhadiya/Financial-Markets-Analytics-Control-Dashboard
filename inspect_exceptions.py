import pandas as pd

report = pd.read_csv("exceptions_report.csv")

print(report.groupby(["asset", "issue"]).size())

abnormal = report[report["issue"] == "Abnormal move"]
print(abnormal.sort_values("value").head(5))
print(abnormal.sort_values("value").tail(5))