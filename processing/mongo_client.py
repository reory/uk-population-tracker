from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["uk_population_tracker"]

def get_db():
    return db

collection = db["snapshots"]