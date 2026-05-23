import type { ForecastResponse } from '../api/client'

interface CumulativeTotals {
  baseline: number
  model: number
  saved: number
}

interface Props {
  forecast: ForecastResponse
  cumulative?: CumulativeTotals | null
}

export function ForecastPanel({ forecast, cumulative }: Props) {
  const comp = forecast.prep_comparison
  const baseline = comp.baseline
  const model = comp.model
  const baselinePct = Math.round((baseline.prep / comp.max_capacity) * 100)

  return (
    <div className="grid">
      <div className="card">
        <div className="label">Baseline prep ({baselinePct}% capacity)</div>
        <div className="value">{baseline.prep}</div>
        <p className="card-note">Expects {baseline.prep} of {comp.max_capacity} max</p>
      </div>
      <div className="card">
        <div className="label">Model prep (LunchLens)</div>
        <div className="value accent">{model.prep}</div>
        <p className="card-note">Forecast {forecast.predicted_visitors} visitors</p>
      </div>
      <div className="card">
        <div className="label">Cost saved vs baseline</div>
        <div className="value success">{comp.cost_saved_eur} €</div>
        <p className="card-note">{comp.waste_saved_kg} kg less waste (this day)</p>
      </div>
      {cumulative && (
        <div className="card">
          <div className="label">Cumulative difference</div>
          <div className={`value ${cumulative.saved >= 0 ? 'success' : 'warn'}`}>
            {cumulative.saved >= 0 ? '+' : ''}
            {cumulative.saved} €
          </div>
          <p className="card-note">
            Baseline {cumulative.baseline} € vs model {cumulative.model} € (dataset start → this day)
          </p>
        </div>
      )}
      <div className="card span-3">
        <h3>Cost comparison (selected day)</h3>
        <table>
          <thead>
            <tr>
              <th>Policy</th>
              <th>Prep</th>
              <th>Waste (kg)</th>
              <th>Waste cost</th>
              <th>Shortage penalty</th>
              <th>Total cost</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Baseline ({baselinePct}% max)</td>
              <td>{baseline.prep}</td>
              <td>{baseline.waste_kg}</td>
              <td>{baseline.waste_cost_eur} €</td>
              <td>{baseline.shortage_penalty_eur} €</td>
              <td>{baseline.total_cost_eur} €</td>
            </tr>
            <tr>
              <td>LunchLens model</td>
              <td>{model.prep}</td>
              <td>{model.waste_kg}</td>
              <td>{model.waste_cost_eur} €</td>
              <td>{model.shortage_penalty_eur} €</td>
              <td>{model.total_cost_eur} €</td>
            </tr>
            <tr>
              <td>Actual visitors</td>
              <td colSpan={5}>{comp.actual_visitors}</td>
            </tr>
          </tbody>
        </table>
        <p className="card-note" style={{ marginTop: '12px' }}>
          Pricing: 10 €/kg wasted food · 5 € penalty per unmet visitor (0.4 kg/portion)
        </p>
      </div>
      <div className="card span-3">
        <h3>Model breakdown</h3>
        <table>
          <thead>
            <tr>
              <th>Model</th>
              <th>Prediction</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Naive weekday mean</td>
              <td>{forecast.breakdown.naive}</td>
            </tr>
            <tr>
              <td>GBM tabular</td>
              <td>{forecast.breakdown.gbm}</td>
            </tr>
            <tr>
              <td>LunchLens hybrid</td>
              <td>{forecast.breakdown.hybrid}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  )
}
