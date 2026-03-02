import pytest
import mongomock
import polars as pl
from datetime import datetime

# This test is to make sure that the connection to the mocked database is healthy.

@pytest.fixture(autouse=True)
def mock_mongo_globally(mocker):
    """Set up a fake database."""

    # 1. Setup the fake client and database
    mock_client = mongomock.MongoClient()
    mock_db = mock_client.population_tracker_db
    
    
    # The code expects a 'snapshots' collection with a 'data' list to explode
    mock_db.snapshots.insert_many([
        {
            "date": datetime(2024, 1, 1),
            "data": [
                {"region_name": "London", "population": 9000000},
                {"region_name": "North West", "region_code": "A124567", "population": 7000000}
            ]
        },
        {
            "date": datetime(2025, 1, 1),
            "data": [
                {"region_name": "London", "population": 9100000},
                {"region_name": "North West", "region_code": "A124567", "population": 7070000}
            ]
        }
    ])

    # 3. Patch the specific function that the code uses to get the DB
    mocker.patch('processing.load_population.get_db', return_value=mock_db)
    
    return mock_db

def test_trend_calculation_logic():
    """
    Verify that the population
    growth math and noise parameters works as expected.
    """

    # Import inside to ensure the patch is ready
    from processing.summary import trend_summary

    df = trend_summary()

    # Test the results
    assert isinstance(df, pl.DataFrame)
    
    # London math: (9,100,000 / 9,000,000) - 1 = 0.0111
    london_data = df.filter(pl.col("region_name") == "London")
    assert round(london_data["pct_change"][0], 4) == 0.0111