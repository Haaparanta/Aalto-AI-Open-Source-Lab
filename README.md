---
marp: true
theme: default
paginate: true
size: 16:9
title: LunchLens Elevator Deck
description: Menu-aware hybrid forecasting for campus lunch demand and food-waste reduction
style: |
  :root {
    --cursor-bg: #181818;
    --cursor-chrome: #141414;
    --cursor-elevated: #1f1f1f;
    --cursor-text: #e4e4e4;
    --cursor-text-secondary: #a8a8a8;
    --cursor-text-tertiary: #737373;
    --cursor-accent: #599ce7;
    --cursor-link: #87c3ff;
    --cursor-stroke: #3a3a3a;
    --cursor-fill: #2a2a2a;
    --cursor-fill-subtle: #222222;
  }
  section {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    padding: 48px 56px 40px;
    background-color: var(--cursor-bg);
    color: var(--cursor-text);
  }
  section.lead {
    background-color: var(--cursor-chrome);
  }
  section.lead h1 {
    font-size: 2.4em;
    color: var(--cursor-accent);
  }
  section.lead h2 {
    color: var(--cursor-text-secondary);
  }
  section.lead p {
    font-size: 1.1em;
    color: var(--cursor-text-secondary);
  }
  section.lead strong {
    color: var(--cursor-text);
  }
  h1 {
    color: var(--cursor-text);
    font-size: 1.9em;
  }
  h2 {
    color: var(--cursor-accent);
    font-size: 1.1em;
    margin-bottom: 0.2em;
  }
  h3 {
    color: var(--cursor-text);
  }
  p, li, td {
    color: var(--cursor-text-secondary);
  }
  strong {
    color: var(--cursor-text);
  }
  em {
    color: var(--cursor-link);
  }
  blockquote {
    border-left: 4px solid var(--cursor-accent);
    background: var(--cursor-fill-subtle);
    padding: 0.6em 1em;
    font-size: 0.85em;
    color: var(--cursor-text-secondary);
  }
  blockquote strong {
    color: var(--cursor-text);
  }
  table {
    font-size: 0.78em;
    width: 100%;
    border-collapse: collapse;
    background: var(--cursor-elevated);
  }
  th {
    background: var(--cursor-fill);
    color: var(--cursor-accent);
    border-bottom: 1px solid var(--cursor-stroke);
  }
  td {
    border-bottom: 1px solid var(--cursor-stroke);
  }
  tr:nth-child(even) td {
    background: var(--cursor-fill-subtle);
  }
  code {
    background: var(--cursor-fill);
    color: var(--cursor-link);
    padding: 0.1em 0.35em;
    border-radius: 4px;
  }
  pre {
    background: var(--cursor-chrome);
    border: 1px solid var(--cursor-stroke);
    border-radius: 6px;
    padding: 0.8em 1em;
  }
  pre code {
    background: transparent;
    color: var(--cursor-text);
  }
  .meta {
    position: absolute;
    top: 22px;
    right: 56px;
    font-size: 0.55em;
    color: var(--cursor-text-tertiary);
  }
  .speaker-notes {
    position: absolute;
    bottom: 28px;
    left: 56px;
    right: 56px;
    font-size: 0.52em;
    color: var(--cursor-text-tertiary);
    border-top: 1px solid var(--cursor-stroke);
    padding-top: 0.6em;
    line-height: 1.45;
  }
  .speaker-notes strong {
    color: var(--cursor-accent);
  }
  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1em;
  }
  .pill {
    display: inline-block;
    background: var(--cursor-fill);
    color: var(--cursor-accent);
    border: 1px solid var(--cursor-stroke);
    padding: 0.15em 0.6em;
    border-radius: 4px;
    font-size: 0.75em;
    margin-right: 0.4em;
  }
  footer, header {
    color: var(--cursor-text-tertiary);
    font-size: 0.5em;
  }
  a {
    color: var(--cursor-link);
  }
---

<!-- _class: lead -->

<span class="meta">Slide 1 / 15 · Intro · ~10s</span>

# LunchLens

## See tomorrow's lunch crowd before the soup hits the pot.

Menu-aware hybrid forecasting for campus lunch demand and food-waste reduction.

**Aalto AI Open Source Lab** · Hybrid ML + LLM · **MVP live**

**[Run the MVP →](MVP.md)** · **[Download PDF deck →](LunchLens-Elevator-Deck.pdf)**

<div class="speaker-notes">

**Speaker notes:** Open with the project name and tagline — let it land. One breath: hybrid AI for campus lunch forecasting and food-waste reduction. Frame it as applied research, not a weekend demo.

</div>

<!--
Open with the project name and tagline — let it land.
One breath: hybrid AI for campus lunch forecasting and food-waste reduction.
Frame it as Aalto Open Source Lab — applied research, not a weekend demo.
-->

---

<span class="meta">Slide 2 / 15 · Story · ~15s</span>

# 10:30 AM. Prep starts for 200 lunches.

<div class="two-col">

| Signal | Today |
|--------|-------|
| **Weather** | Pouring rain |
| **Competition** | Free guild pizza nearby |
| **Menu** | Liver casserole special |

> **By 2 PM:** Half the trays come back untouched — not carelessness, but **invisible demand**.

</div>

<div class="speaker-notes">

**Speaker notes:** Paint the scene slowly — rain, guild pizza, liver casserole. Pause before the punchline. Key line: demand was invisible until it was too late.

</div>

<!--
Paint the scene slowly — rain, guild pizza, liver casserole.
Pause before the punchline: half the trays come back untouched.
Key line: demand was invisible until it was too late.
-->

---

<span class="meta">Slide 3 / 15 · Story · ~12s</span>

# Campus kitchens cook blind

Lunch spots prep on instinct. Nearby prices are roughly equal — so **something else drives the crowd**.

<div class="two-col">

**Over-prep**
→ food in the bin

**Under-prep**
→ stockouts and lost revenue

</div>

<div class="speaker-notes">

**Speaker notes:** Kitchens prep on gut feel — everyone on campus knows this rhythm. Prices are similar, so price is not the lever. Two failure modes: waste vs stockouts.

</div>

<!--
Kitchens prep on gut feel — everyone on campus knows this rhythm.
Prices are similar, so price is not the lever.
Two failure modes: waste on one side, stockouts on the other.
-->

---

<span class="meta">Slide 4 / 15 · Story · ~15s</span>

# What actually moves the needle

| Signal | Why it matters |
|--------|----------------|
| **Today's menu** | Not every dish draws the same crowd |
| **Weather** | Rain and cold change walk-in behavior |
| **Day of week** | Tuesday lunch is not Friday lunch |
| **Competitor menus** | Guild pizza next door pulls demand away |

<div class="speaker-notes">

**Speaker notes:** Walk through the four signals. Use a campus example: guild pizza day steals your lunch rush. Transition: both bad outcomes share one root cause — guessing demand.

</div>

<!--
Walk through the four signals — menu, weather, weekday, competitors.
Use a campus example: guild pizza day steals your lunch rush.
Transition: both bad outcomes share one root cause — guessing demand.
-->

---

<span class="meta">Slide 5 / 15 · Story · ~12s</span>

# Two bad outcomes, one root cause

<div class="two-col">

**Over-prepare**
Avoidable waste — cost, climate, full trays returned

**Under-prepare**
Stockouts, lost revenue, peak-hour chaos

</div>

**Both come from guessing demand instead of forecasting it.**

<div class="speaker-notes">

**Speaker notes:** Over-prepare hits cost, climate, and morale. Under-prepare means angry customers and a scrambling kitchen. Land the line: both come from forecasting by guesswork.

</div>

<!--
Over-prepare: waste hits cost, climate, and morale.
Under-prepare: angry customers and a scrambling kitchen.
Land the line: both come from forecasting by guesswork.
-->

---

<span class="meta">Slide 6 / 15 · Science · ~18s</span>

# Our research question

> *We are asking a research question with a real sustainability payoff.*

<span class="pill">RQ1</span> Does hybrid ML + LLM beat classical forecasting?

<span class="pill">RQ2</span> How much waste and cost disappear vs a fixed baseline prep policy?

<span class="pill">RQ3</span> Weather, own menu, or competitors — what matters most?

<div class="speaker-notes">

**Speaker notes:** Pivot tone: this is not another dashboard. Read RQ1–RQ3 clearly; judges care about depth. RQ2 is the sustainability hook.

</div>

<!--
Pivot tone: this is not another dashboard — it is a research question.
Read RQ1–RQ3 clearly; judges care about depth.
RQ2 is the sustainability hook: better forecast → less simulated waste.
-->

---

<span class="meta">Slide 7 / 15 · Science · ~15s</span>

# LunchLens in one sentence

**A hybrid forecaster that reads the menu, checks the weather, scans competitor menus, and estimates how many people are coming.**

| ML | LLM | Output |
|----|-----|--------|
| Numbers from history | Context from menus | One unified forecast |

*Less guesswork. Less waste. More lunch.*

<div class="speaker-notes">

**Speaker notes:** Read the one-liner verbatim — it is the elevator pitch. Three beats: ML for numbers, LLM for menu context, one fused forecast.

</div>

<!--
Read the one-liner verbatim — it is the elevator pitch.
Three beats: ML for numbers, LLM for menu context, one fused forecast.
Close with the tagline rhythm: less guesswork, less waste, more lunch.
-->

---

<span class="meta">Slide 8 / 15 · Science · ~12s</span>

# Step 1 — Look back

## Tabular baselines on history and calendar

Historical counts capture weekday rhythms, holidays, and semester patterns.

| Baseline | Method |
|----------|--------|
| Naive weekday mean | Historical average by day of week |
| Linear regression | Calendar and date features |
| Gradient boosting | XGBoost / LightGBM on tabular signals |

<div class="speaker-notes">

**Speaker notes:** Start the three-step pipeline: look back, look around, look ahead. This is the floor we need to beat before adding LLM signals.

</div>

<!--
Start the three-step pipeline: look back, look around, look ahead.
Baselines are weekday means, regression, gradient boosting.
This is the floor we need to beat before adding LLM signals.
-->

---

<span class="meta">Slide 9 / 15 · Science · ~15s</span>

# Step 2 — Look around

## LLM scores demand signals from 1 to 5

The LLM **rates** menu appeal, competitor pressure, and weather pull — it does not invent visitor counts.

| Input | Role |
|-------|------|
| Date | Calendar and semester context |
| Own menu | Semantic appeal of today's dishes |
| Competitor menus | Local competition pressure |
| Weather | Walk-in sensitivity to rain and temperature |

<div class="speaker-notes">

**Speaker notes:** Critical distinction: the LLM does not invent visitor counts. Structured JSON output — not free-text guessing.

</div>

<!--
Critical distinction: the LLM does not invent visitor counts.
It scores menu appeal, competitor pressure, and weather like a regular who knows the block.
Structured JSON output — not free-text guessing.
-->

---

<span class="meta">Slide 10 / 15 · Science · ~12s</span>

# Step 3 — Look ahead

## Hybrid fusion → operational outputs

<div class="two-col">

### Output 1
**Estimated daily visitors**
Fused tabular + LLM forecast → recommended prep

### Output 2
**Baseline vs model cost (€)**
70% max-capacity baseline · 10 €/kg waste · 5 € shortage penalty

</div>

Cumulative cost charts show the running difference over time

<div class="speaker-notes">

**Speaker notes:** Fusion combines tabular ML and LLM scores. Compare against a simple baseline: prep for 70% of max capacity. Track waste kg, shortage penalties, and cumulative € saved.

</div>

<!--
Fusion combines tabular ML and LLM scores.
Output 1: estimated visitors — operational number for prep.
Output 2: waste saved % vs naive baseline — the sustainability metric.
-->

---

<span class="meta">Slide 11 / 15 · Science · ~12s</span>

# Structured LLM output

## JSON scores with guardrails

```json
{
  "menu_appeal": 4,
  "competitor_pressure": 2,
  "weather_effect": 3,
  "overall_demand_signal": 3.5
}
```

JSON schema · scores clamped 1–5 · prompts logged for reproducibility

<div class="speaker-notes">

**Speaker notes:** Show the JSON — judges want structured outputs, not vibes. Emphasize reproducibility — every score is cached and auditable.

</div>

<!--
Show the JSON — judges want to see structured outputs, not vibes.
Point out guardrails: schema validation, 1–5 clamp, logged prompts.
Emphasize reproducibility — every score is cached and auditable.
-->

---

<span class="meta">Slide 12 / 15 · Science · ~15s</span>

# Ablation study

## What does each signal buy us?

| Model | Signals | Expected lift |
|-------|---------|---------------|
| Naive | Weekday average | Baseline to beat |
| + Weather | Rain and temperature | Small gain |
| + LLM menu | Semantic appeal | Does text help? |
| + Competitors | Local competition | Full context |
| **LunchLens full** | All fused | Best forecast, waste, and cost savings |

Metrics: MAE · waste saved % · daily and **cumulative cost difference (€)**

<div class="speaker-notes">

**Speaker notes:** This table is the research flex — incremental signal additions. Hypothesis: full LunchLens fusion wins on both forecast and waste.

</div>

<!--
This table is the research flex — incremental signal additions.
Metrics: MAE, RMSE, MAPE on visitors plus waste saved %.
Hypothesis: full LunchLens fusion wins on both forecast and waste.
-->

---

<span class="meta">Slide 13 / 15 · Impact · ~12s</span>

# Who it is for

## Starts on campus. Does not stay there.

| Audience | Why they care |
|----------|---------------|
| Campus cafés | Less waste, fewer stockouts |
| Sustainability teams | Reportable waste-saved metric |
| ML / NLP researchers | Hybrid benchmark: menus + time series |
| Future OSL teams | Fork, plug in real data, rerun eval |

<div class="speaker-notes">

**Speaker notes:** Campus cafés get operational value. Sustainability teams get a metric they can report. Researchers get an open benchmark.

</div>

<!--
Campus cafés get operational value — prep smarter.
Sustainability teams get a metric they can report.
Researchers get an open benchmark; future teams can fork with real data.
-->

---

<span class="meta">Slide 14 / 15 · Impact · ~15s</span>

# What we shipped

| Layer | Deliverable |
|-------|-------------|
| **Data** | 730-day synthetic campus dataset (menus, weather, competitors) |
| **Backend** | FastAPI — hybrid forecast, LLM scorer, waste/cost API |
| **Frontend** | React dashboard — visitor chart, waste kg, cumulative cost (€) |
| **Baseline** | Fixed prep at **70% of max capacity** vs LunchLens model |

Run locally: `backend` + `frontend` · OpenAI key for live LLM scoring · see [MVP.md](MVP.md)

<div class="speaker-notes">

**Speaker notes:** MVP is runnable today — not a slide-deck prototype. Show the dashboard: pick a date, see baseline vs model prep, waste in kg, and cumulative € difference. Synthetic data now; partner restaurant pilot next.

</div>

<!--
Name the four phases — Ground truth, Menu brain, Fusion and fight, Ship it open.
Be honest: synthetic data now, partner restaurant pilot later.
Deliverables: dataset generator, hybrid model, ablation, open repo.
-->

---

<!-- _class: lead -->

<span class="meta">Slide 15 / 15 · Close · ~15s</span>

# Why it matters

Food waste is not abstract. It is trays coming back full while someone else goes hungry.

**Tech for Good** — turn forecast error into waste kg and € people can feel.

**Open source** — benchmark, eval harness, prompt templates, live MVP — fork and extend.

## *We go beyond courses. We build, we measure, we share.*

<div class="speaker-notes">

**Speaker notes:** Slow down for the close. Final line: We go beyond courses. We build, we measure, we share. Pause. Thank the judges. Offer to walk through the ablation design.

</div>

<!--
Slow down for the close — food waste is trays coming back full.
Tech for Good plus open source: benchmark, eval harness, prompt templates.
Final line: We go beyond courses. We build, we measure, we share.
Pause. Thank the judges. Offer to walk through the ablation design.
-->
