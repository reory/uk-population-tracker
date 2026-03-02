import pytest
import mongomock
import polars as pl

@pytest.fixture
def client(mocker):
    # 1. Create a fake collection with data that matches your route's needs
    mock_col = mongomock.MongoClient().db.collection
    mock_col.insert_one({
        "date": "2024-01-01", 
        "population": 68000000,
        "region_name": "United Kingdom"
    })

    # 2. Mock 'trend_summary' so it doesn't try to hit the DB either
    # We return a small Polars DataFrame since your route expects one
    mock_df = pl.DataFrame({
        "region_name": ["London", "North West"],
        "population": [9000000, 7000000],
        "change": [9000, 35000],
        "pct_change": [0.01, 0.005]
    })
    
    # 3. APPLY PATCHES BEFORE IMPORTING THE APP
    mocker.patch('app.routes.collection', mock_col)
    mocker.patch('app.routes.trend_summary', return_value=mock_df)
    
    # 4. NOW import the app (this avoids the early connection attempt)
    from run import app as flask_app
    flask_app.config['TESTING'] = True
    
    with flask_app.test_client() as client:
        yield client

def test_index_route(client):
    """Make sure the homepage loads with mocked data."""

    response = client.get('/')
    assert response.status_code == 200
    assert b"UK Population Tracker" in response.data

def test_trends_route(client):
    """Test the trends route with mocked data."""

    response = client.get('/trends')
    assert response.status_code == 200