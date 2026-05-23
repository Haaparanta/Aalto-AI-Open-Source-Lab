from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LLMScores:
    menu_appeal: float
    competitor_pressure: float
    weather_effect: float
    overall_demand_signal: float
    rationale: str

    def as_dict(self) -> dict:
        return {
            "menu_appeal": self.menu_appeal,
            "competitor_pressure": self.competitor_pressure,
            "weather_effect": self.weather_effect,
            "overall_demand_signal": self.overall_demand_signal,
            "rationale": self.rationale,
        }


@dataclass
class ForecastBreakdown:
    naive: float
    gbm: float
    hybrid: float
    llm_scores: LLMScores


def hybrid_predict(naive: float, gbm: float, llm_scores: LLMScores) -> float:
    signal = llm_scores.overall_demand_signal
    adjustment = signal / 3.0
    hybrid = 0.7 * gbm + 0.3 * (naive * adjustment)
    return round(max(20.0, hybrid), 1)


def build_breakdown(naive: float, gbm: float, llm_scores: LLMScores) -> ForecastBreakdown:
    return ForecastBreakdown(
        naive=round(naive, 1),
        gbm=round(gbm, 1),
        hybrid=hybrid_predict(naive, gbm, llm_scores),
        llm_scores=llm_scores,
    )
