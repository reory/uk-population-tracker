import polars as pl
from processing.load_population import load_population_snapshots

def wide_population_table():
    """Pivots data from the long to the wide format for the dashboard table."""

    df = load_population_snapshots()

    # Pivot: Rows = regions, Columns = dates, Values = population
    wide = df.pivot(
        values="population",
        index=["region_code", "region_name"],
        on="date"
    ).sort("region_code")

    return wide

if __name__ == "__main__":
    print(wide_population_table())