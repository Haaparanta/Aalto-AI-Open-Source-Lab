# LunchLens

> *See tomorrow's lunch crowd before the soup hits the pot.*

Hybrid ML + LLM forecasting for campus lunch demand and food-waste reduction.

**[Read the full proposal →](docs/proposal.md)**

---

## The idea in 30 seconds

Rainy Tuesday. Guild pizza next door. Liver casserole today.

LunchLens reads those signals — menu, weather, competitors, history — and forecasts who's actually showing up. Better forecasts mean kitchens prep smarter, and less food ends up in the bin.

---

## Outputs

- **Estimated daily visitors** — how many people to expect
- **Estimated food waste saved (%)** — improvement vs. naive baseline prep

---

## How it works

1. **Look back** — tabular ML on historical visitor counts and date patterns
2. **Look around** — LLM scores menu appeal, competitor pressure, and weather (1–5)
3. **Look ahead** — hybrid model fuses both into a visitor forecast + waste metric

---

## Stack

Python · XGBoost · LLM structured scoring · open eval harness

---

## Project status

Proposal phase — applied research with open-source artifacts.

Planned deliverables: synthetic benchmark dataset, hybrid forecaster, ablation study, reproducible evaluation scripts.

---

## Aalto AI Open Source Lab

A student-driven initiative to build real-world AI & software projects with impact, depth, and purpose.
