import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PRIMARY_DOCS_DIR = DATA_DIR / "primary_documents"
FRONTEND_DIST_DIR = BASE_DIR / "frontend" / "dist"
STATIC_DIR = BASE_DIR / "frontend" / "static"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
PRIMARY_DOCS_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

# Server Config
HOST = os.getenv("FINN_HOST", "0.0.0.0")
PORT = int(os.getenv("FINN_PORT", 8000))
DEBUG = os.getenv("FINN_DEBUG", "True").lower() == "true"

# API Keys (Optional)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Default Alert Thresholds
DEFAULT_PRICE_MOVE_THRESHOLD = float(os.getenv("DEFAULT_PRICE_MOVE_THRESHOLD", 3.0))
DEFAULT_VOLUME_MULT_THRESHOLD = float(os.getenv("DEFAULT_VOLUME_MULT_THRESHOLD", 2.0))
DEFAULT_DIGEST_WINDOW_HOURS = int(os.getenv("DEFAULT_DIGEST_WINDOW_HOURS", 24))

# Monitored Categories Default
ALL_CATEGORIES = [
    "results", "M&A", "fund_raise", "management_change", "litigation",
    "insider_trading", "earnings_call", "investor_meetings", "credit_rating",
    "dividend", "bonus_split", "capex", "press_release", "postal_ballot",
    "agm_egm", "pledging", "unclassified"
]

DEFAULT_MONITORED_CATEGORIES = [
    "results", "M&A", "management_change", "litigation", "fund_raise",
    "dividend", "capex", "credit_rating", "bonus_split"
]

