from datetime import date
import random
from processing.mongo_client import get_db
from data_generation.regions import UK_REGIONS

def generate_population_snapshot():
    """Creates a single point in time population record for all regions."""
    
    # Connect to the database.
    db = get_db()

    # Temporary override for testing multi-date trends.
    today = date.today().isoformat()

    for region in UK_REGIONS:
        snapshot = {
            "region_code": region["region_code"],
            "region_name": region["region_name"],
            "date": today,
            "population": random.randint(500_000, 10_000_000)
        }

        db.population_snapshots.insert_one(snapshot)

    print("Population snapshots generated")

if __name__ == "__main__":
    generate_population_snapshot()