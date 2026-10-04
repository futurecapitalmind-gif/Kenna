from __future__ import annotations

from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    telegram_admin_id: int = int(os.getenv("TELEGRAM_ADMIN_ID", "0") or 0)
    default_timeframe: str = os.getenv("DEFAULT_TIMEFRAME", "1h")
    market_data_provider: str = os.getenv("MARKET_DATA_PROVIDER", "yahoo")
    min_signal_confidence: float = float(os.getenv("MIN_SIGNAL_CONFIDENCE", "0.65"))


settings = Settings()
