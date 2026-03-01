from faker import Faker
from mimesis import Numeric
import random
from datetime import datetime

fake = Faker()

numeric = Numeric()

# Realistic Baseline populations (ONS sourced.)
baselines = {
    "UKC": 2_600_000,   # North East
    "UKD": 7_400_000,   # North West
    "UKE": 5_600_000,   # Yorkshire and The Humber
    "UKF": 4_900_000,   # East Midlands
    "UKG": 6_000_000,   # West Midlands
    "UKH": 6_300_000,   # East of England
    "UKI": 9_700_000,   # London
    "UKJ": 9_200_000,   # South East
    "UKK": 5_700_000,   # South West
    "UKL": 3_200_000,   # Wales
    "UKM": 5_500_000,   # Scotland
    "UKN": 1_900_000,   # Northern Ireland
}

# Region specific growth patterns (Monthly %)
growth_ranges = {
    "UKC": (-0.05, 0.05),
    "UKD": (0.00, 0.10),
    "UKE": (0.00, 0.10),
    "UKF": (0.00, 0.15),
    "UKG": (0.00, 0.10),
    "UKH": (0.05, 0.20),
    "UKI": (0.15, 0.35),
    "UKJ": (0.05, 0.25),
    "UKK": (0.00, 0.10),
    "UKL": (0.00, 0.10),   
    "UKM": (0.00, 0.10),   
    "UKN": (0.00, 0.10),
}

def generate_population_snapshot(date: datetime):

    snapshot = []

    for region_code, baseline in baselines.items():
        low, high = growth_ranges[region_code]

        # Generate a realsitic monthly percentage change
        pct_change = random.uniform(low, high)

        # Convert to absolute change
        change = int(baseline * (pct_change / 100))

        # Add some random noise using Mimesis
        noise = numeric.integer_number(start=-150, end=150)

        population = baseline + change + noise

        snapshot.append({
            "region_code": region_code,
            "population": population,
            "pct_change": pct_change,
            "change": change + noise,
            "date": date
        })

    return snapshot