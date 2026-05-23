from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas as pd

from app.config import BASELINE_CAPACITY_RATIO, SYNTHETIC_DAYS
from app.data.generator import generate_synthetic_data
from app.data.store import ensure_data_file, load_dataframe, save_dataframe
from app.features.builder import build_features
from app.metrics.waste import compute_comparison
from app.models.baseline import BaselineModels, mae, train_baselines
from app.models.hybrid import LLMScores, build_breakdown
from app.models.llm_scorer import llm_available, score_demand


@dataclass
class AppState:
    df: pd.DataFrame
    models: BaselineModels
    holdout_df: pd.DataFrame


_state: AppState | None = None


def weather_summary(row: pd.Series) -> str:
    return (
        f"{row['weather_condition']}, {row['weather_temp_c']}C, "
        f"{row['weather_precip_mm']}mm precipitation"
    )


def bootstrap() -> AppState:
    global _state
    df = ensure_data_file()
    models, holdout_df = train_baselines(df)
    _state = AppState(df=build_features(df), models=models, holdout_df=holdout_df)
    return _state


def get_state() -> AppState:
    if _state is None:
        return bootstrap()
    return _state


def regenerate_data(days: int | None = None) -> pd.DataFrame:
    global _state
    day_count = days or SYNTHETIC_DAYS
    df = generate_synthetic_data(days=day_count)
    save_dataframe(df)
    df = load_dataframe()
    models, holdout_df = train_baselines(df)
    _state = AppState(df=build_features(df), models=models, holdout_df=holdout_df)
    return _state.df


def row_for_date(date_str: str) -> pd.Series:
    state = get_state()
    match = state.df[state.df["date"].dt.strftime("%Y-%m-%d") == date_str]
    if match.empty:
        raise KeyError(f"No data for date {date_str}")
    return match.iloc[0]


def _neutral_llm_scores() -> LLMScores:
    return LLMScores(
        menu_appeal=3.0,
        competitor_pressure=3.0,
        weather_effect=3.0,
        overall_demand_signal=3.0,
        rationale="GBM-only estimate (LLM skipped for bulk history).",
    )


def _forecast_row(row: pd.Series, actual_override: int | None, use_llm: bool) -> dict:
    state = get_state()
    date_str = row["date"].strftime("%Y-%m-%d") if hasattr(row["date"], "strftime") else str(row["date"])[:10]
    naive = state.models.naive_predict(row)
    gbm = state.models.gbm_predict(row)

    if use_llm:
        llm_scores = score_demand(
            date_str=date_str,
            own_menu=str(row["own_menu_text"]),
            competitor_menus=[
                str(row["competitor_1_menu"]),
                str(row["competitor_2_menu"]),
                str(row["competitor_3_menu"]),
            ],
            weather_summary=weather_summary(row),
        )
        model_source = "hybrid_llm"
    else:
        llm_scores = _neutral_llm_scores()
        model_source = "gbm_bulk"

    breakdown = build_breakdown(naive, gbm, llm_scores)
    if not use_llm:
        from dataclasses import replace
        breakdown = replace(breakdown, hybrid=round(gbm, 1))

    actual = int(actual_override if actual_override is not None else row["visitor_count"])
    capacity = int(row.get("nominal_capacity", 220))
    comparison = compute_comparison(actual, breakdown.hybrid, capacity)

    return {
        "date": date_str,
        "actual_visitors": actual,
        "predicted_visitors": breakdown.hybrid,
        "recommended_prep": comparison.model.prep,
        "waste_saved_pct": comparison.waste_saved_pct,
        "llm_scores": llm_scores.as_dict() if use_llm else None,
        "model_source": model_source,
        "breakdown": {
            "naive": breakdown.naive,
            "gbm": breakdown.gbm,
            "hybrid": breakdown.hybrid,
        },
        "prep_comparison": comparison.as_dict(),
        "inputs": {
            "own_menu_text": row["own_menu_text"],
            "competitor_1_menu": row["competitor_1_menu"],
            "competitor_2_menu": row["competitor_2_menu"],
            "competitor_3_menu": row["competitor_3_menu"],
            "weather_condition": row["weather_condition"],
            "weather_temp_c": float(row["weather_temp_c"]),
            "weather_precip_mm": float(row["weather_precip_mm"]),
            "nominal_capacity": capacity,
        },
    }


def run_forecast_for_row(row: pd.Series, actual_override: int | None = None) -> dict:
    return _forecast_row(row, actual_override, use_llm=True)


def run_forecast_for_date(date_str: str) -> dict:
    return run_forecast_for_row(row_for_date(date_str))


def run_custom_forecast(payload: dict) -> dict:
    target_date = date.fromisoformat(payload["date"])
    row = pd.Series(
        {
            "date": pd.Timestamp(target_date),
            "day_of_week": target_date.weekday(),
            "is_holiday": False,
            "week_of_semester": payload.get("week_of_semester", 8),
            "weather_temp_c": payload["weather_temp_c"],
            "weather_precip_mm": payload["weather_precip_mm"],
            "weather_condition": payload["weather_condition"],
            "own_menu_text": payload["own_menu_text"],
            "own_menu_popularity_score": payload.get("own_menu_popularity_score", 0.6),
            "competitor_1_menu": payload["competitor_1_menu"],
            "competitor_2_menu": payload["competitor_2_menu"],
            "competitor_3_menu": payload["competitor_3_menu"],
            "competitor_pressure_score": payload.get("competitor_pressure_score", 0.6),
            "visitor_count": payload.get("actual_visitors", 0),
            "nominal_capacity": payload.get("nominal_capacity", 220),
        }
    )
    actual = payload.get("actual_visitors")
    return run_forecast_for_row(row, actual_override=actual)


def waste_history(limit: int = 365) -> list[dict]:
    state = get_state()
    sorted_df = state.df.sort_values("date")
    tail = sorted_df if limit <= 0 or limit >= len(sorted_df) else sorted_df.tail(limit)
    items: list[dict] = []
    cumulative_baseline = 0.0
    cumulative_model = 0.0
    cumulative_saved = 0.0
    for _, row in tail.iterrows():
        forecast = _forecast_row(row, actual_override=None, use_llm=False)
        comp = forecast["prep_comparison"]
        baseline_cost = float(comp["baseline"]["total_cost_eur"])
        model_cost = float(comp["model"]["total_cost_eur"])
        cost_saved = float(comp["cost_saved_eur"])
        cumulative_baseline = round(cumulative_baseline + baseline_cost, 2)
        cumulative_model = round(cumulative_model + model_cost, 2)
        cumulative_saved = round(cumulative_saved + cost_saved, 2)
        items.append(
            {
                "date": forecast["date"],
                "actual_visitors": forecast["actual_visitors"],
                "baseline_prep": comp["baseline"]["prep"],
                "model_prep": comp["model"]["prep"],
                "baseline_waste_kg": comp["baseline"]["waste_kg"],
                "model_waste_kg": comp["model"]["waste_kg"],
                "baseline_cost_eur": baseline_cost,
                "model_cost_eur": model_cost,
                "cost_saved_eur": cost_saved,
                "cumulative_baseline_cost_eur": cumulative_baseline,
                "cumulative_model_cost_eur": cumulative_model,
                "cumulative_cost_saved_eur": cumulative_saved,
                "baseline_shortage": comp["baseline"]["shortage_portions"],
                "model_shortage": comp["model"]["shortage_portions"],
            }
        )
    return items


def history(limit: int = 30) -> list[dict]:
    state = get_state()
    sorted_df = state.df.sort_values("date")
    tail = sorted_df if limit <= 0 or limit >= len(sorted_df) else sorted_df.tail(limit)
    return [
        {
            "date": row["date"].strftime("%Y-%m-%d"),
            "day_of_week": int(row["day_of_week"]),
            "visitor_count": int(row["visitor_count"]),
            "own_menu_text": row["own_menu_text"],
            "competitor_1_menu": row["competitor_1_menu"],
            "competitor_2_menu": row["competitor_2_menu"],
            "competitor_3_menu": row["competitor_3_menu"],
            "weather_condition": row["weather_condition"],
            "weather_temp_c": float(row["weather_temp_c"]),
            "weather_precip_mm": float(row["weather_precip_mm"]),
            "week_of_semester": int(row["week_of_semester"]),
            "nominal_capacity": int(row.get("nominal_capacity", 220)),
        }
        for _, row in tail.iterrows()
    ]


def history_summary() -> dict:
    state = get_state()
    sorted_df = state.df.sort_values("date")
    return {
        "total_records": len(sorted_df),
        "start_date": sorted_df["date"].iloc[0].strftime("%Y-%m-%d"),
        "end_date": sorted_df["date"].iloc[-1].strftime("%Y-%m-%d"),
        "avg_visitors": round(float(sorted_df["visitor_count"].mean()), 1),
        "min_visitors": int(sorted_df["visitor_count"].min()),
        "max_visitors": int(sorted_df["visitor_count"].max()),
        "unique_menus": int(sorted_df["own_menu_text"].nunique()),
        "nominal_capacity": int(sorted_df.get("nominal_capacity", pd.Series([220])).iloc[0]),
        "baseline_prep": int(round(sorted_df.get("nominal_capacity", pd.Series([220])).iloc[0] * BASELINE_CAPACITY_RATIO)),
    }


def evaluate_holdout() -> dict:
    state = get_state()
    if not llm_available():
        return {"llm_available": False, "message": "Configure OPENAI_API_KEY to compute metrics"}

    actuals: list[float] = []
    hybrid_preds: list[float] = []
    waste_saved_pct: list[float] = []
    cost_saved: list[float] = []

    for _, row in state.holdout_df.iterrows():
        forecast = run_forecast_for_row(row)
        comp = forecast["prep_comparison"]
        actuals.append(float(row["visitor_count"]))
        hybrid_preds.append(float(forecast["predicted_visitors"]))
        waste_saved_pct.append(float(comp["waste_saved_pct"]))
        cost_saved.append(float(comp["cost_saved_eur"]))

    return {
        "llm_available": True,
        "holdout_days": len(actuals),
        "mae_hybrid": round(mae(np.array(actuals), np.array(hybrid_preds)), 2),
        "avg_waste_saved_pct": round(float(np.mean(waste_saved_pct)), 2),
        "avg_cost_saved_eur": round(float(np.mean(cost_saved)), 2),
        "total_cost_saved_eur": round(float(np.sum(cost_saved)), 2),
    }
