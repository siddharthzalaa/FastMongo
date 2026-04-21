from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

def get_db():
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    try:
        client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")

        db = client["college"]
        yield db

    finally:
        client.close()

