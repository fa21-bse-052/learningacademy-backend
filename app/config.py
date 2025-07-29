import logging
from pydantic_settings import BaseSettings  # For Pydantic v2+

# ─── Logging Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger("config")
logger.info("Initializing settings configuration")

# ─── Settings Model ────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    groq_api_key: str
    mongodb_url: str
    jwt_secret: str  # ← Used in auth.py for JWT generation

    class Config:
        env_file = ".env"
        extra = "forbid"  # Prevent loading unexpected env variables

# ─── Load Settings ─────────────────────────────────────────────────────────────
try:
    settings = Settings()
    logger.info("Settings loaded successfully")
except Exception as e:
    logger.error("Failed to load settings", exc_info=True)
    raise e
