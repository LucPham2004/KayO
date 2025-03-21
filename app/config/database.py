from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

from app.config import Config


class MongoDB:
    client = None
    db = None

    @classmethod
    def connect(cls):
        if cls.client is None:
            print(f"🔄 Connecting to MongoDB with URI: {Config.MONGO_URI}")
            cls.client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            cls.db = cls.client.get_database(Config.MONGO_DB_NAME)
            try:
                cls.client.admin.command('ping')
                print("✅ Connected to MongoDB Atlas successfully!")
            except Exception as e:
                print(f"❌ Connection failed: {e}")

    @classmethod
    def get_db(cls):
        if cls.db is None:
            cls.connect()
        return cls.db

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()
            print("🛑 MongoDB connection closed.")