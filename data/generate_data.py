import csv
import random
from datetime import date, timedelta

random.seed(42)

STORES = [
    ("S01", "Monterey, CA", "Central Coast"),
    ("S02", "Salinas, CA", "Central Coast"),
    ("S03", "Santa Cruz, CA", "Central Coast"),
    ("S04", "San Jose, CA", "Bay Area"),
    ("S05", "Sacramento, CA", "Central Valley"),
    ("S06", "Fresno, CA", "Central Valley"),
]
ONLINE = ("S00", "QuickCart Online", "National")

CATEGORIES = {
    "Consoles": {"price": (399, 499), "cost_pct": 0.82},
    "Video Games": {"price": (39, 69), "cost_pct": 0.62},
    "Accessories": {"price": (14, 59), "cost_pct": 0.55},
    "Collectibles": {"price": (19, 89), "cost_pct": 0.48},
    "Trade-Ins/Used Games": {"price": (9, 34), "cost_pct": 0.35},
}

WEEKLY_OVERHEAD = {
    "S01": 2400, "S02": 2100, "S03": 2200,
    "S04": 3100, "S05": 2600, "S06": 2300,
    "S00": 900,  # online: lower fixed overhead, cost is folded into per-unit shipping/fulfillment
}

START = date(2024, 1, 1)
WEEKS = 52

def seasonality(week_index):
    # Holiday spike late Nov-Dec (weeks 47-52), back-to-school bump Aug (weeks 31-35)
    if 47 <= week_index <= 52:
        return 1.9
    if 31 <= week_index <= 35:
        return 1.25
    if week_index <= 2:
        return 1.15  # New year console/gift-card redemption bump
    return 1.0

rows = []
all_locations = STORES + [ONLINE]

for week_index in range(1, WEEKS + 1):
    week_start = START + timedelta(weeks=week_index - 1)
    season = seasonality(week_index)
    for store_id, location, region in all_locations:
        is_online = store_id == "S00"
        for category, cfg in CATEGORIES.items():
            base_units = {
                "Consoles": 8, "Video Games": 35, "Accessories": 28,
                "Collectibles": 14, "Trade-Ins/Used Games": 20,
            }[category]
            online_multiplier = 2.6 if is_online else 1.0
            units = max(
                0,
                round(base_units * online_multiplier * season * random.uniform(0.75, 1.3))
            )
            unit_price = round(random.uniform(*cfg["price"]), 2)
            unit_cost = round(unit_price * cfg["cost_pct"] * random.uniform(0.95, 1.05), 2)
            overhead = round(WEEKLY_OVERHEAD[store_id] / len(CATEGORIES), 2)
            rows.append([
                week_start.isoformat(), store_id, location, region,
                "Online" if is_online else "In-Store",
                category, units, unit_price, unit_cost, overhead,
            ])

out_path = "/Users/katelynnsilva/Desktop/katelynn-portfolio/data/retail_sales.csv"
with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "week_start", "store_id", "location", "region", "channel",
        "category", "units_sold", "unit_price", "unit_cost", "overhead_allocated",
    ])
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to {out_path}")
