from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ ERROR: MONGO_URI environment variable is missing!")
    # We assign None to avoid crashing the whole server on import
    client = None
    db = None
    users_collection = None
    asteroid_collection = None
else:
    print("✅ MONGO_URI detected.")
    client = MongoClient(MONGO_URI)
    db = client.jwt_auth
    users_collection = db.users
    asteroid_collection = db.asteroids