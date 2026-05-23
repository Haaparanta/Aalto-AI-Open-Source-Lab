from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.config import DATA_DIR, DATA_FILE, SYNTHETIC_DAYS
from app.data.generator import generate_synthetic_data


def ensure_data_file(path: Path | None = None, days: int | None = None) -> pd.DataFrame:
    target = path or DATA_FILE
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    day_count = days or SYNTHETIC_DAYS
    if not target.exists():
        df = generate_synthetic_data(days=day_count)
        df.to_csv(target, index=False)
    return pd.read_csv(target, parse_dates=["date"])


def save_dataframe(df: pd.DataFrame, path: Path | None = None) -> Path:
    target = path or DATA_FILE
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
    return target


def load_dataframe(path: Path | None = None) -> pd.DataFrame:
    target = path or DATA_FILE
    return pd.read_csv(target, parse_dates=["date"])
