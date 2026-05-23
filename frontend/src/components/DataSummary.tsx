import { type HistorySummary } from '../api/client'

interface Props {
  summary: HistorySummary
}

export function DataSummary({ summary }: Props) {
  const baselinePct = Math.round((summary.baseline_prep / summary.nominal_capacity) * 100)

  return (
    <div className="summary-grid">
      <div className="summary-item">
        <div className="label">Records</div>
        <div className="value">{summary.total_records}</div>
      </div>
      <div className="summary-item">
        <div className="label">Date range</div>
        <div className="value small">{summary.start_date} → {summary.end_date}</div>
      </div>
      <div className="summary-item">
        <div className="label">Avg visitors</div>
        <div className="value">{summary.avg_visitors}</div>
      </div>
      <div className="summary-item">
        <div className="label">Range</div>
        <div className="value small">{summary.min_visitors} – {summary.max_visitors}</div>
      </div>
      <div className="summary-item">
        <div className="label">Unique menus</div>
        <div className="value">{summary.unique_menus}</div>
      </div>
      <div className="summary-item">
        <div className="label">Max capacity</div>
        <div className="value">{summary.nominal_capacity}</div>
      </div>
      <div className="summary-item">
        <div className="label">Baseline prep ({baselinePct}%)</div>
        <div className="value">{summary.baseline_prep}</div>
      </div>
    </div>
  )
}
