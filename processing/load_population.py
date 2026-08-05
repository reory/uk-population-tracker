import polars as pl

from processing.mongo_client import get_db


def load_population_snapshots():
    """Makes a Polars Dataframe from MongoDB snapshot records."""

    db = get_db()

    # Fetch all snapshots. Drop the MongoDB id.
    records = list(db.snapshots.find({}, {"_id": 0}))

    # Load into Polars DataFrame
    df = pl.DataFrame(records)

    # Convert the Mongo datetime to Polars date
    df = df.with_columns(pl.col("date").cast(pl.Date))

    # Explode the list of 12 region dicts.
    df = df.explode("data")

    # Unpack the structure inside data.
    df = df.with_columns(pl.col("data").struct.unnest())

    return df


if __name__ == "__main__":
    df = load_population_snapshots()
    print(df)
