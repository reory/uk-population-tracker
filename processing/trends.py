import polars as pl
from processing.load_population import load_population_snapshots

def compute_trends():

    df = load_population_snapshots()

    df = df.sort(["region_code", "date"])

    df = df.with_columns([
        pl.col("population")
        .diff()
        .over("region_code")
        .alias("change"),

        pl.col("population")
        .pct_change()
        .over("region_code")
        .alias("pct_change"),

        pl.col("population")
        .rank("dense", descending=True)
        .over("date")
        .alias("rank"),
    ])

    return df

if __name__ == "__main__":
    print(compute_trends())