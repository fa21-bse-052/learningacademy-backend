import logging
from pydantic_settings import BaseSettings  # ← Correct import for Pydantic v2

# ─── Logging ────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger("config")
logger.info("Initializing settings configuration")

# ─── Settings ────────────────────────────────────────────────────────────────
class Settings(BaseSettings):
    groq_api_key: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
    logger.info("Settings loaded successfully")
except Exception as e:
    logger.error("Failed to load settings", exc_info=True)
    raise e
