import polars as pl

from processing.map_regions import load_nuts1_geography
from processing.trends import compute_trends


def trend_summary():
    """Calculates growth rates and percentage changes across all regions."""

    df = compute_trends()

    # Load GeoPandas
    geo = load_nuts1_geography()

    # Remove Geometry column 
    # (shapely objects cannot be converted to Polars)
    geo = geo.drop(columns=["geometry"])

    # Convert to Polars
    geo = pl.from_pandas(geo)

    # Merge region names into the trends DataFrame
    df = df.join(
        geo.select([
            pl.col("nuts118cd").alias("region_code"),
            pl.col("nuts118nm").alias("region_name")
        ]),
        on="region_code",
        how="left"
    )

    # Keep the latest snapshot per region.
    latest = (
        df.sort(["region_code", "date"])
          .group_by("region_code")
          .tail(1)
    )

    # Select the summary columns
    summary = latest.select([
        "region_code",
        "region_name",
        "population",
        "change",
        "pct_change",
        "rank"
    ]).sort("rank")

    return summary

if __name__ == "__main__":
    print(trend_summary())