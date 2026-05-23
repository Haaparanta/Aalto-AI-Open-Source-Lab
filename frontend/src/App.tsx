import { useEffect, useMemo, useState } from 'react'
import {
  api,
  type ForecastResponse,
  type HealthResponse,
  type HistoryItem,
  type HistorySummary,
  type MetricsResponse,
  type WasteHistoryItem,
} from './api/client'
import { DataSummary } from './components/DataSummary'
import { ForecastPanel } from './components/ForecastPanel'
import { HistoryChart } from './components/HistoryChart'
import { HistoryTable } from './components/HistoryTable'
import { ScoreBreakdown } from './components/ScoreBreakdown'
import { WasteChart } from './components/WasteChart'
import './styles/cursor-dark.css'

const CHART_RANGES = [
  { label: '90 days', value: 90 },
  { label: '180 days', value: 180 },
  { label: '365 days', value: 365 },
  { label: 'All', value: 0 },
]

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [summary, setSummary] = useState<HistorySummary | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([])
  const [wasteHistory, setWasteHistory] = useState<WasteHistoryItem[]>([])
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null)
  const [selectedDate, setSelectedDate] = useState('')
  const [chartRange, setChartRange] = useState(365)
  const [forecast, setForecast] = useState<ForecastResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadInitial() {
      try {
        const [healthRes, summaryRes, historyRes, wasteRes] = await Promise.all([
          api.health(),
          api.historySummary(),
          api.history(0),
          api.wasteHistory(0),
        ])
        setHealth(healthRes)
        setSummary(summaryRes)
        setHistory(historyRes.items)
        setWasteHistory(wasteRes.items)
        const latest = historyRes.items[historyRes.items.length - 1]?.date
        if (latest) {
          setSelectedDate(latest)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load initial data')
      }
    }
    loadInitial()
  }, [])

  useEffect(() => {
    if (!selectedDate) return
    async function loadForecast() {
      setLoading(true)
      setError(null)
      try {
        const [forecastRes, metricsRes] = await Promise.all([
          api.forecast(selectedDate),
          api.metrics(),
        ])
        setForecast(forecastRes)
        setMetrics(metricsRes)
      } catch (err) {
        setForecast(null)
        setError(err instanceof Error ? err.message : 'Failed to load forecast')
      } finally {
        setLoading(false)
      }
    }
    loadForecast()
  }, [selectedDate])

  const dateBounds = useMemo(() => {
    if (!history.length) return { min: '', max: '' }
    return { min: history[0].date, max: history[history.length - 1].date }
  }, [history])

  const selectedHistory = useMemo(
    () => history.find((item) => item.date === selectedDate),
    [history, selectedDate],
  )

  const cumulativeThroughSelected = useMemo(() => {
    const item = wasteHistory.find((row) => row.date === selectedDate)
    if (!item) return null
    return {
      baseline: item.cumulative_baseline_cost_eur,
      model: item.cumulative_model_cost_eur,
      saved: item.cumulative_cost_saved_eur,
    }
  }, [wasteHistory, selectedDate])

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>LunchLens</h1>
          <p>See tomorrow&apos;s lunch crowd before the soup hits the pot.</p>
        </div>
        {health && (
          <div className={`status-pill ${health.llm_available ? 'ok' : 'warn'}`}>
            {health.llm_available ? 'LLM connected' : 'LLM unavailable — set OPENAI_API_KEY'}
          </div>
        )}
      </header>

      {summary && (
        <div className="card span-3" style={{ marginBottom: '16px' }}>
          <h3>Dataset overview</h3>
          <DataSummary summary={summary} />
        </div>
      )}

      <div className="controls">
        <label htmlFor="date">Forecast date</label>
        <input
          id="date"
          type="date"
          value={selectedDate}
          min={dateBounds.min}
          max={dateBounds.max}
          onChange={(event) => setSelectedDate(event.target.value)}
          disabled={!dateBounds.min}
        />
        <button type="button" disabled={loading || !selectedDate} onClick={() => setSelectedDate(selectedDate)}>
          Refresh
        </button>
        <span className="control-note">{history.length} days loaded</span>
      </div>

      {selectedHistory && (
        <div className="card span-3" style={{ marginBottom: '16px' }}>
          <h3>Selected day snapshot</h3>
          <table>
            <tbody>
              <tr>
                <td>Menu</td>
                <td>{selectedHistory.own_menu_text}</td>
              </tr>
              <tr>
                <td>Weather</td>
                <td>
                  {selectedHistory.weather_condition}, {selectedHistory.weather_temp_c}C,{' '}
                  {selectedHistory.weather_precip_mm}mm
                </td>
              </tr>
              <tr>
                <td>Actual visitors</td>
                <td>{selectedHistory.visitor_count}</td>
              </tr>
              <tr>
                <td>Competitors</td>
                <td>
                  {selectedHistory.competitor_1_menu}; {selectedHistory.competitor_2_menu};{' '}
                  {selectedHistory.competitor_3_menu}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {error && <div className="error">{error}</div>}
      {loading && <div className="loading">Running hybrid forecast and LLM scoring...</div>}

      {forecast && !loading && (
        <>
          <ForecastPanel forecast={forecast} cumulative={cumulativeThroughSelected} />
          <div className="grid">
            <ScoreBreakdown forecast={forecast} />
            <div className="card">
              <h3>Holdout metrics</h3>
              {metrics?.llm_available ? (
                <table>
                  <tbody>
                    <tr>
                      <td>Holdout days</td>
                      <td>{metrics.holdout_days}</td>
                    </tr>
                    <tr>
                      <td>MAE hybrid</td>
                      <td>{metrics.mae_hybrid}</td>
                    </tr>
                    <tr>
                      <td>Avg waste saved</td>
                      <td>{metrics.avg_waste_saved_pct}%</td>
                    </tr>
                    <tr>
                      <td>Avg cost saved / day</td>
                      <td>{metrics.avg_cost_saved_eur} €</td>
                    </tr>
                    <tr>
                      <td>Total cost saved (holdout)</td>
                      <td>{metrics.total_cost_saved_eur} €</td>
                    </tr>
                  </tbody>
                </table>
              ) : (
                <p style={{ color: 'var(--cursor-text-secondary)' }}>{metrics?.message}</p>
              )}
            </div>
          </div>
        </>
      )}

      <div className="card span-3" style={{ marginTop: '16px' }}>
        <div className="section-header">
          <h3>Visitor history chart</h3>
          <div className="range-controls">
            {CHART_RANGES.map((option) => (
              <button
                key={option.label}
                type="button"
                className={chartRange === option.value ? 'range-btn active' : 'range-btn'}
                onClick={() => setChartRange(option.value)}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
        <HistoryChart items={history} selectedDate={selectedDate} range={chartRange} />
      </div>

      <div className="card span-3" style={{ marginTop: '16px' }}>
        <div className="section-header">
          <h3>Food waste & cost (baseline vs model)</h3>
          <div className="range-controls">
            {CHART_RANGES.map((option) => (
              <button
                key={`waste-${option.label}`}
                type="button"
                className={chartRange === option.value ? 'range-btn active' : 'range-btn'}
                onClick={() => setChartRange(option.value)}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
        <WasteChart items={wasteHistory} range={chartRange} />
      </div>

      <div className="card span-3" style={{ marginTop: '16px' }}>
        <h3>Full dataset table ({history.length} rows)</h3>
        <HistoryTable items={history} selectedDate={selectedDate} />
      </div>
    </div>
  )
}

export default App
