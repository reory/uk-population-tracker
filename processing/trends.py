import polars as pl

from processing.load_population import load_population_snapshots


def compute_trends():
    """
    Computes year over year growth and statistical summaries for each region.
    """

    df = load_population_snapshots()

    df = df.sort(["region_code", "date"])
    
    df = df.with_columns([
        # Monthly volume change - difference between current and previous months per region.
        pl.col("population")
        .diff()
        .over("region_code")
        .alias("change"),
        # Percentage change from previous months per region.
        pl.col("population")
        .pct_change()
        .over("region_code")
        .alias("pct_change"),
        # Regional leaderboard - Rank regions by population size for every specific date.
        pl.col("population")
        .rank("dense", descending=True)
        .over("date")
        .alias("rank"),
    ])

    return df

if __name__ == "__main__":
    print(compute_trends())