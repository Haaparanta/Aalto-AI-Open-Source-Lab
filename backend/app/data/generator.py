from __future__ import annotations

import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

MENU_TEMPLATES: list[tuple[str, float]] = [
    ("Burger and fries", 0.85),
    ("Double cheeseburger meal", 0.88),
    ("Chicken pasta", 0.75),
    ("Creamy chicken soup", 0.68),
    ("Salmon soup and rye bread", 0.7),
    ("Grilled salmon plate", 0.79),
    ("Vegetarian lasagna", 0.65),
    ("Spinach and feta pie", 0.58),
    ("Liver casserole with mashed potatoes", 0.35),
    ("Meatballs and mashed potatoes", 0.8),
    ("Swedish meatballs with lingonberry", 0.82),
    ("Caesar salad with chicken", 0.6),
    ("Halloumi salad bowl", 0.63),
    ("Fish and chips", 0.72),
    ("Fried vendace with potatoes", 0.71),
    ("Beef stew", 0.68),
    ("Reindeer stew with mash", 0.74),
    ("Mushroom risotto", 0.55),
    ("Truffle pasta", 0.77),
    ("Pizza slice and salad", 0.78),
    ("Margherita pizza day", 0.84),
    ("Karelian pie with egg butter", 0.5),
    ("Thai curry with rice", 0.7),
    ("Green curry tofu bowl", 0.64),
    ("BBQ pulled pork wrap", 0.82),
    ("Smoked salmon bagel", 0.69),
    ("Tomato soup and grilled cheese", 0.58),
    ("Poke bowl", 0.73),
    ("Teriyaki salmon bowl", 0.76),
    ("Schnitzel with potatoes", 0.76),
    ("Vegan buddha bowl", 0.62),
    ("Falafel platter", 0.66),
    ("Sausage and potato salad", 0.67),
    ("Chef's surprise stew", 0.45),
    ("Mac and cheese with bacon", 0.81),
    ("Taco rice bowl", 0.7),
    ("Butter chicken with naan", 0.78),
    ("Minestrone and garlic bread", 0.57),
    ("BLT sandwich with soup", 0.61),
    ("Wok noodles with vegetables", 0.65),
]

COMPETITOR_MENUS: list[list[tuple[str, float]]] = [
    [
        ("Guild pizza day", 0.9),
        ("Cheap daily pasta", 0.6),
        ("Student lunch deal", 0.55),
        ("Free coffee with lunch", 0.62),
        ("Kebab plate special", 0.73),
    ],
    [
        ("Chain burger combo", 0.75),
        ("Rotating chicken wrap", 0.65),
        ("Soup of the day", 0.5),
        ("Meal deal wrap", 0.68),
        ("Asian noodle box", 0.7),
    ],
    [
        ("Fresh salad bar", 0.6),
        ("Soup and bread", 0.55),
        ("Smoothie and wrap", 0.58),
        ("Quinoa power bowl", 0.64),
        ("Seasonal soup duo", 0.52),
    ],
]

FINNISH_HOLIDAY_RANGES = [
    ((6, 20), (8, 10)),
    ((12, 23), (1, 6)),
]


def _pick_menu(rng: random.Random) -> tuple[str, float]:
    item, score = rng.choice(MENU_TEMPLATES)
    return item, score


def _pick_competitor_menus(rng: random.Random) -> tuple[list[str], float]:
    menus: list[str] = []
    pressures: list[float] = []
    for pool in COMPETITOR_MENUS:
        item, score = rng.choice(pool)
        menus.append(item)
        pressures.append(score)
    return menus, float(np.mean(pressures))


def _weekday_effect(dow: int) -> float:
    effects = {0: -8, 1: 12, 2: 18, 3: 20, 4: 10, 5: -25, 6: -30}
    return effects.get(dow, 0)


def _weather_effect(temp_c: float, precip_mm: float) -> float:
    effect = (temp_c - 5) * 0.3
    if precip_mm > 2:
        effect -= 15 + precip_mm * 0.5
    return effect


def _is_break_period(current: date) -> bool:
    month, day = current.month, current.day
    for (start_m, start_d), (end_m, end_d) in FINNISH_HOLIDAY_RANGES:
        if start_m <= end_m:
            if (month, day) >= (start_m, start_d) or (month, day) <= (end_m, end_d):
                return True
        elif (month, day) >= (start_m, start_d) or (month, day) <= (end_m, end_d):
            return True
    return False


def _week_of_semester(offset: int) -> int:
    cycle_day = offset % 140
    if cycle_day >= 112:
        return 0
    return min(16, cycle_day // 7 + 1)


def generate_synthetic_data(
    days: int = 730,
    start: date | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    start_date = start or date(2024, 1, 8)
    rows: list[dict] = []

    for offset in range(days):
        current = start_date + timedelta(days=offset)
        dow = current.weekday()
        week_of_semester = _week_of_semester(offset)
        is_holiday = _is_break_period(current)

        temp_c = float(np_rng.normal(8 if current.month in (11, 12, 1, 2) else 16, 6))
        precip_mm = float(max(0, np_rng.exponential(1.5) if temp_c < 12 else np_rng.exponential(0.4)))
        if precip_mm > 4:
            condition = "rain"
        elif temp_c < 0:
            condition = "snow"
        elif precip_mm > 0.5:
            condition = "cloudy"
        else:
            condition = "clear"

        own_menu, menu_score = _pick_menu(rng)
        comp_menus, comp_pressure = _pick_competitor_menus(rng)

        semester_boost = week_of_semester * 2
        base = 150
        visitors = (
            base
            + _weekday_effect(dow)
            + semester_boost
            + _weather_effect(temp_c, precip_mm)
            + menu_score * 40
            - comp_pressure * 25
            - (35 if is_holiday else 0)
            + float(np_rng.normal(0, 10))
        )
        visitors = int(max(40, round(visitors)))

        rows.append(
            {
                "date": current.isoformat(),
                "day_of_week": dow,
                "is_holiday": is_holiday,
                "week_of_semester": week_of_semester,
                "weather_temp_c": round(temp_c, 1),
                "weather_precip_mm": round(precip_mm, 1),
                "weather_condition": condition,
                "own_menu_text": own_menu,
                "own_menu_popularity_score": menu_score,
                "competitor_1_menu": comp_menus[0],
                "competitor_2_menu": comp_menus[1],
                "competitor_3_menu": comp_menus[2],
                "competitor_pressure_score": round(comp_pressure, 3),
                "visitor_count": visitors,
                "nominal_capacity": 220,
            }
        )

    return pd.DataFrame(rows)
