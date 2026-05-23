from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ForecastRequest(BaseModel):
    date: str
    own_menu_text: str
    competitor_1_menu: str
    competitor_2_menu: str
    competitor_3_menu: str
    weather_condition: str
    weather_temp_c: float
    weather_precip_mm: float
    week_of_semester: int = 8
    own_menu_popularity_score: float = 0.6
    competitor_pressure_score: float = 0.6
    actual_visitors: Optional[int] = None
