from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


def get_db(uri: str):
    client = AsyncIOMotorClient(uri)
    db = client.college
    return db


db = get_db(settings.DATABASE_URI)
