import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"
DATA_FILE = DATA_DIR / "synthetic.csv"

load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYNTHETIC_DAYS = int(os.getenv("SYNTHETIC_DAYS", "730"))

BASELINE_CAPACITY_RATIO = float(os.getenv("BASELINE_CAPACITY_RATIO", "0.70"))
KG_PER_PORTION = float(os.getenv("KG_PER_PORTION", "0.4"))
WASTE_EUR_PER_KG = float(os.getenv("WASTE_EUR_PER_KG", "10"))
SHORTAGE_PENALTY_EUR = float(os.getenv("SHORTAGE_PENALTY_EUR", "5"))
