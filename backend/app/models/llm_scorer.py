from __future__ import annotations

import hashlib
import json
from pathlib import Path

from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL, PROMPTS_DIR
from app.models.hybrid import LLMScores

PROMPT_FILE = PROMPTS_DIR / "menu_demand_v1.txt"
_cache: dict[str, LLMScores] = {}


def llm_available() -> bool:
    return bool(OPENAI_API_KEY)


def _cache_key(date_str: str, own_menu: str, competitors: list[str], weather: str) -> str:
    payload = "|".join([date_str, own_menu, *competitors, weather])
    return hashlib.sha256(payload.encode()).hexdigest()


def _clamp(value: float) -> float:
    return max(1.0, min(5.0, float(value)))


def _parse_scores(raw: str) -> LLMScores:
    data = json.loads(raw)
    return LLMScores(
        menu_appeal=_clamp(data["menu_appeal"]),
        competitor_pressure=_clamp(data["competitor_pressure"]),
        weather_effect=_clamp(data["weather_effect"]),
        overall_demand_signal=_clamp(data["overall_demand_signal"]),
        rationale=str(data.get("rationale", "")),
    )


def score_demand(
    date_str: str,
    own_menu: str,
    competitor_menus: list[str],
    weather_summary: str,
) -> LLMScores:
    if not llm_available():
        raise RuntimeError("OPENAI_API_KEY is not configured")

    key = _cache_key(date_str, own_menu, competitor_menus, weather_summary)
    if key in _cache:
        return _cache[key]

    template = PROMPT_FILE.read_text()
    prompt = template.format(
        date=date_str,
        own_menu=own_menu,
        competitor_1=competitor_menus[0],
        competitor_2=competitor_menus[1],
        competitor_3=competitor_menus[2],
        weather_summary=weather_summary,
    )

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content or "{}"
    scores = _parse_scores(content)
    _cache[key] = scores
    return scores
