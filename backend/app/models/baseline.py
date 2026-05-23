from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

from app.features.builder import FEATURE_COLUMNS, build_features


@dataclass
class BaselineModels:
    weekday_means: dict[int, float]
    gbm: GradientBoostingRegressor
    train_df: pd.DataFrame

    def naive_predict(self, row: pd.Series) -> float:
        return float(self.weekday_means.get(int(row["day_of_week"]), self.train_df["visitor_count"].mean()))

    def gbm_predict(self, row: pd.Series, extra_features: dict[str, float] | None = None) -> float:
        features = row[FEATURE_COLUMNS].astype(float).copy()
        if extra_features:
            for key, value in extra_features.items():
                features[key] = value
        matrix = features.to_frame().T
        for col in FEATURE_COLUMNS:
            if col not in matrix.columns:
                matrix[col] = 0.0
        matrix = matrix[FEATURE_COLUMNS]
        return float(self.gbm.predict(matrix)[0])


def train_baselines(df: pd.DataFrame, train_ratio: float = 0.8) -> tuple[BaselineModels, pd.DataFrame]:
    features = build_features(df)
    split_idx = int(len(features) * train_ratio)
    train_df = features.iloc[:split_idx].copy()
    holdout_df = features.iloc[split_idx:].copy()

    weekday_means = train_df.groupby("day_of_week")["visitor_count"].mean().to_dict()
    gbm = GradientBoostingRegressor(random_state=42)
    gbm.fit(train_df[FEATURE_COLUMNS], train_df["visitor_count"])

    models = BaselineModels(weekday_means=weekday_means, gbm=gbm, train_df=train_df)
    return models, holdout_df


def mae(actual: np.ndarray, predicted: np.ndarray) -> float:
    return float(np.mean(np.abs(actual - predicted)))
