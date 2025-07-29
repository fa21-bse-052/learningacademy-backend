import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from decouple import config

# ─── Logging Setup ─────────────────────────────────────────
logger = logging.getLogger("db")
logger.setLevel(logging.INFO)

# ─── MongoDB Connection ────────────────────────────────────
MONGODB_URL = config("MONGODB_URL", default="mongodb://localhost:27017")

try:
    client = AsyncIOMotorClient(MONGODB_URL, server_api=ServerApi('1'))
    db = client["learning_academy"]  # Update your DB name here
    logger.info("Connected to MongoDB successfully.")
except Exception as e:
    logger.error("Failed to connect to MongoDB", exc_info=True)
    raise e

# ─── Mongo Collections ─────────────────────────────────────
user_collection = db["users"]               # For signup/login
progress_collection = db["video_progress"]  # For video progress
