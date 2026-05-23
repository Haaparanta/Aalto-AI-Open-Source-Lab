import type { ForecastResponse } from '../api/client'

interface Props {
  forecast: ForecastResponse
}

export function ScoreBreakdown({ forecast }: Props) {
  const scores = forecast.llm_scores

  return (
    <div className="card span-2">
      <h3>LLM signal scores (1-5)</h3>
      {scores ? (
        <>
          <div className="score-grid">
            {(
              [
                ['Menu appeal', scores.menu_appeal],
                ['Competitor pressure', scores.competitor_pressure],
                ['Weather effect', scores.weather_effect],
                ['Overall demand', scores.overall_demand_signal],
              ] as const
            ).map(([name, score]) => (
              <div className="score-item" key={name}>
                <div className="name">{name}</div>
                <div className="score">{score}</div>
              </div>
            ))}
          </div>
          <p style={{ color: 'var(--cursor-text-secondary)', marginTop: '16px' }}>{scores.rationale}</p>
        </>
      ) : (
        <p style={{ color: 'var(--cursor-text-secondary)' }}>LLM scores unavailable for this forecast.</p>
      )}
      <h3 style={{ marginTop: '20px' }}>Inputs</h3>
      <table>
        <tbody>
          <tr>
            <td>Menu</td>
            <td>{forecast.inputs.own_menu_text}</td>
          </tr>
          <tr>
            <td>Competitors</td>
            <td>
              {forecast.inputs.competitor_1_menu}; {forecast.inputs.competitor_2_menu};{' '}
              {forecast.inputs.competitor_3_menu}
            </td>
          </tr>
          <tr>
            <td>Weather</td>
            <td>
              {forecast.inputs.weather_condition}, {forecast.inputs.weather_temp_c}C,{' '}
              {forecast.inputs.weather_precip_mm}mm
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}
