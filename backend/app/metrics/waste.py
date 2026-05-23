from __future__ import annotations

from dataclasses import asdict, dataclass

from app.config import (
    BASELINE_CAPACITY_RATIO,
    KG_PER_PORTION,
    SHORTAGE_PENALTY_EUR,
    WASTE_EUR_PER_KG,
)


def recommended_prep(predicted_visitors: float) -> int:
    buffer = max(10, 0.10 * predicted_visitors)
    return int(round(predicted_visitors + buffer))


def baseline_prep(max_capacity: int) -> int:
    """Baseline kitchen policy: prep for 70% of maximum capacity."""
    return int(round(max_capacity * BASELINE_CAPACITY_RATIO))


def waste_portions(prep: int, actual: int) -> int:
    return max(0, prep - actual)


def shortage_portions(prep: int, actual: int) -> int:
    return max(0, actual - prep)


def portions_to_kg(portions: int) -> float:
    return round(portions * KG_PER_PORTION, 2)


def total_cost_eur(waste_kg: float, shortage: int) -> float:
    waste_cost = waste_kg * WASTE_EUR_PER_KG
    penalty_cost = shortage * SHORTAGE_PENALTY_EUR
    return round(waste_cost + penalty_cost, 2)


@dataclass
class PrepPolicyResult:
    prep: int
    waste_portions: int
    shortage_portions: int
    waste_kg: float
    waste_cost_eur: float
    shortage_penalty_eur: float
    total_cost_eur: float


def evaluate_policy(prep: int, actual: int) -> PrepPolicyResult:
    waste = waste_portions(prep, actual)
    shortage = shortage_portions(prep, actual)
    waste_kg = portions_to_kg(waste)
    waste_cost = round(waste_kg * WASTE_EUR_PER_KG, 2)
    penalty_cost = round(shortage * SHORTAGE_PENALTY_EUR, 2)
    return PrepPolicyResult(
        prep=prep,
        waste_portions=waste,
        shortage_portions=shortage,
        waste_kg=waste_kg,
        waste_cost_eur=waste_cost,
        shortage_penalty_eur=penalty_cost,
        total_cost_eur=round(waste_cost + penalty_cost, 2),
    )


@dataclass
class PrepComparison:
    max_capacity: int
    actual_visitors: int
    model_predicted_visitors: float
    baseline: PrepPolicyResult
    model: PrepPolicyResult
    cost_saved_eur: float
    waste_saved_kg: float
    waste_saved_pct: float

    def as_dict(self) -> dict:
        return {
            "max_capacity": self.max_capacity,
            "actual_visitors": self.actual_visitors,
            "model_predicted_visitors": self.model_predicted_visitors,
            "baseline": asdict(self.baseline),
            "model": asdict(self.model),
            "cost_saved_eur": self.cost_saved_eur,
            "waste_saved_kg": self.waste_saved_kg,
            "waste_saved_pct": self.waste_saved_pct,
        }


def compute_comparison(
    actual_visitors: int,
    model_predicted: float,
    max_capacity: int,
) -> PrepComparison:
    baseline_result = evaluate_policy(baseline_prep(max_capacity), actual_visitors)
    model_result = evaluate_policy(recommended_prep(model_predicted), actual_visitors)
    cost_saved = round(baseline_result.total_cost_eur - model_result.total_cost_eur, 2)
    waste_saved_kg = round(baseline_result.waste_kg - model_result.waste_kg, 2)
    if baseline_result.waste_kg == 0:
        waste_saved_pct = 100.0 if model_result.waste_kg == 0 else 0.0
    else:
        waste_saved_pct = round((baseline_result.waste_kg - model_result.waste_kg) / baseline_result.waste_kg * 100, 1)
    return PrepComparison(
        max_capacity=max_capacity,
        actual_visitors=actual_visitors,
        model_predicted_visitors=round(model_predicted, 1),
        baseline=baseline_result,
        model=model_result,
        cost_saved_eur=cost_saved,
        waste_saved_kg=waste_saved_kg,
        waste_saved_pct=waste_saved_pct,
    )
