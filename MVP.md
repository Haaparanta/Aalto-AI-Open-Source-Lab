# LunchLens MVP

Runnable demo: FastAPI backend + React frontend with synthetic campus lunch data, hybrid ML forecasting, and OpenAI menu scoring.

## Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key

## Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add OPENAI_API_KEY
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Service status |
| GET | `/api/history` | Recent visitor history |
| GET | `/api/forecast/{date}` | Hybrid forecast for a dataset date |
| POST | `/api/forecast` | Custom forecast inputs |
| GET | `/api/metrics` | Holdout MAE and waste saved % |
| POST | `/api/data/generate` | Regenerate synthetic dataset |

## Architecture

1. **Synthetic data** — 730 days (~2 years) of menu, weather, competitor, and visitor records
2. **Tabular ML** — weekday naive mean + gradient boosting regressor
3. **LLM scorer** — OpenAI JSON scores for menu, competition, weather (1-5)
4. **Hybrid fusion** — combines GBM + LLM demand signal
5. **Waste metric** — prep recommendation and waste saved % vs naive baseline

## Notes

- First forecast for a date calls OpenAI; subsequent calls use an in-memory cache.
- `/api/metrics` evaluates the holdout set and may take a minute on first run.
- Generated CSV lives in `backend/data/synthetic.csv` (gitignored).
