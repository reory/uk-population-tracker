import random
from datetime import datetime, timezone

from processing.generator import baselines, growth_ranges, numeric
from processing.mongo_client import collection


def get_latest_snapshot():
    """Retrieves the single most recent population entry from MongoDB."""

    latest = list(collection.find().sort("date", -1).limit(1))
    return latest[0] if latest else None


def generate_next_month():
    """Appends a new population snapshot for the upcoming month to MongoDB."""
    
    latest = get_latest_snapshot()

    if latest is None:
        current_baselines = baselines
        date = datetime(2024, 1, 1, tzinfo=timezone.utc)
    else:
        current_baselines = {
            item["region_code"]: item["population"]
            for item in latest["data"]
        }

        last_date = latest["date"]
        year = last_date.year
        month = last_date.month + 1

        if month > 12:
            month = 1
            year += 1

        date = datetime(year, month, 1, tzinfo=timezone.utc)

    snapshot = []

    for region_code, baseline in current_baselines.items():
        low, high = growth_ranges[region_code]
        pct_change = random.uniform(low, high)
        change = int(baseline * (pct_change / 100))
        noise = numeric.integer_number(start=-150, end=150)
        population = baseline + change + noise

        snapshot.append({
            "region_code": region_code,
            "population": population,
            "pct_change": pct_change,
            "change": change + noise,
        })

    collection.insert_one({
        "date": date,
        "data": snapshot
    })

    return snapshot

def generate_history(months: int = 24):
    """
    Backfills MongoDB with monthly population 
    snapshots for the past 24 months
    """

    history = []

    # If DB is empty, generate the first month.
    latest = get_latest_snapshot()
    if latest is None:
        first = generate_next_month()
        history.append(first)

    # Now generate the remaining months.
    for _ in range(months - 1):
        next_month = generate_next_month()
        history.append(next_month)

    return history

if __name__ == "__main__":
    generate_history(24)
    print("🗺️ Generated 24 months of population history.")
