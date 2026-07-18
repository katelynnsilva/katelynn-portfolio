import sqlite3
import csv
import json
import re
import os

BASE = "/Users/katelynnsilva/Desktop/katelynn-portfolio"
csv_path = os.path.join(BASE, "data/retail_sales.csv")
sql_path = os.path.join(BASE, "sql/analysis.sql")
out_path = os.path.join(BASE, "charts/data.json")

conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE retail_sales (
        week_start TEXT, store_id TEXT, location TEXT, region TEXT,
        channel TEXT, category TEXT, units_sold INTEGER,
        unit_price REAL, unit_cost REAL, overhead_allocated REAL
    )
""")

with open(csv_path) as f:
    reader = csv.DictReader(f)
    rows = [
        (
            r["week_start"], r["store_id"], r["location"], r["region"],
            r["channel"], r["category"], int(r["units_sold"]),
            float(r["unit_price"]), float(r["unit_cost"]), float(r["overhead_allocated"]),
        )
        for r in reader
    ]
cur.executemany("INSERT INTO retail_sales VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
conn.commit()

with open(sql_path) as f:
    sql_text = f.read()

statements = [s.strip() for s in sql_text.split(";") if s.strip() and not s.strip().startswith("--")]
# Reattach the leading comment/name for each statement for readability, then strip comments before exec
named_statements = re.split(r"\n(?=-- \d\.)", sql_text)
named_statements = [s.strip() for s in named_statements if s.strip()]
named_statements = [s for s in named_statements if re.match(r"-- \d\.", s)]

results = {}
keys = ["monthly_revenue", "by_location", "by_category", "by_channel", "overhead_by_location"]

for key, block in zip(keys, named_statements):
    stmt = "\n".join(line for line in block.splitlines() if not line.strip().startswith("--")).strip()
    cur.execute(stmt)
    cols = [d[0] for d in cur.description]
    rows_out = [dict(zip(cols, row)) for row in cur.fetchall()]
    results[key] = rows_out

with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print(f"Wrote analysis results to {out_path}")
for k, v in results.items():
    print(f"\n-- {k} --")
    for row in v:
        print(row)
