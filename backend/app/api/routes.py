from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from app.api.schemas import ForecastRequest
from app.config import SYNTHETIC_DAYS
from app.models.llm_scorer import llm_available
from app.service import (
    evaluate_holdout,
    get_state,
    history,
    history_summary,
    regenerate_data,
    run_custom_forecast,
    run_forecast_for_date,
    waste_history,
)

router = APIRouter()


@router.get("/health")
def health() -> dict:
    state = get_state()
    return {
        "status": "ok",
        "records": len(state.df),
        "llm_available": llm_available(),
    }


@router.post("/data/generate")
def generate_data(days: Optional[int] = None) -> dict:
    day_count = days or SYNTHETIC_DAYS
    df = regenerate_data(days=day_count)
    return {"status": "generated", "records": len(df), "days": day_count}


@router.get("/history")
def get_history(limit: int = 30) -> dict:
    return {"items": history(limit=limit)}


@router.get("/history/summary")
def get_history_summary() -> dict:
    return history_summary()


@router.get("/forecast/{date}")
def forecast_by_date(date: str) -> dict:
    if not llm_available():
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
    try:
        return run_forecast_for_date(date)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/forecast")
def forecast_custom(payload: ForecastRequest) -> dict:
    if not llm_available():
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY is not configured")
    try:
        return run_custom_forecast(payload.model_dump())
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/waste/history")
def get_waste_history(limit: int = 365) -> dict:
    return {"items": waste_history(limit=limit)}


@router.get("/metrics")
def metrics() -> dict:
    return evaluate_holdout()
