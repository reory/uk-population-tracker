import pytest
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from processing.mongo_client import MONGO_URI

# This test is to verify the actual connection from the database to the rest of
# the app is solid.

@pytest.mark.live
def test_real_mongodb_connection():
    """Check to see if the real MongoDB service is reachable."""

    try:
        # Try to connect. (short timeout 2 secs)
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)

        # The admin command is the standard way to check if the server is alive.
        client.admin.command('ping')
        success = True
    except PyMongoError as e:
        print(f"Connection failed: {e}")
        success = False

    assert success is True, "MongoDB is OFF. Turn it on to pass this specific test!"