from __future__ import annotations

import pandas as pd


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    features = df.copy()
    features["month"] = features["date"].dt.month
    features["day_of_month"] = features["date"].dt.day
    features["is_weekend"] = features["day_of_week"].isin([5, 6]).astype(int)
    features["is_holiday"] = features["is_holiday"].astype(int)
    features["rainy"] = (features["weather_precip_mm"] > 2).astype(int)
    return features


FEATURE_COLUMNS = [
    "day_of_week",
    "month",
    "day_of_month",
    "is_weekend",
    "is_holiday",
    "week_of_semester",
    "weather_temp_c",
    "weather_precip_mm",
    "rainy",
    "own_menu_popularity_score",
    "competitor_pressure_score",
]
