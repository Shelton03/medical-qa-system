from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.logger import logger

class MongoDBClient:
    client: AsyncIOMotorClient = None

    def connect(self):
        try:
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            raise e

    def close(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

    def get_database(self):
        return self.client[settings.MONGODB_DB_NAME]

db_client = MongoDBClient()

def get_database():
    return db_client.get_database()
