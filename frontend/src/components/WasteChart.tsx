import { useMemo } from 'react'
import {
  Bar,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { WasteHistoryItem } from '../api/client'

interface Props {
  items: WasteHistoryItem[]
  range: number
}

function round2(value: number) {
  return Math.round(value * 100) / 100
}

function buildChartData(items: WasteHistoryItem[]) {
  let cumulativeBaseline = 0
  let cumulativeModel = 0
  let cumulativeSaved = 0

  return items.map((item) => {
    cumulativeBaseline += item.baseline_cost_eur
    cumulativeModel += item.model_cost_eur
    cumulativeSaved += item.cost_saved_eur

    return {
      date: item.date.slice(2),
      baselineWasteKg: item.baseline_waste_kg,
      modelWasteKg: item.model_waste_kg,
      baselineCost: item.baseline_cost_eur,
      modelCost: item.model_cost_eur,
      costSaved: item.cost_saved_eur,
      cumulativeBaselineCost: round2(cumulativeBaseline),
      cumulativeModelCost: round2(cumulativeModel),
      cumulativeCostSaved: round2(cumulativeSaved),
    }
  })
}

export function WasteChart({ items, range }: Props) {
  const sliced = range <= 0 || range >= items.length ? items : items.slice(-range)
  const data = useMemo(() => buildChartData(sliced), [sliced])

  const totals = useMemo(() => {
    if (!data.length) {
      return { baseline: 0, model: 0, saved: 0, days: 0 }
    }
    const last = data[data.length - 1]
    return {
      baseline: last.cumulativeBaselineCost,
      model: last.cumulativeModelCost,
      saved: last.cumulativeCostSaved,
      days: data.length,
    }
  }, [data])

  return (
    <div className="chart-stack">
      <div className="cumulative-summary">
        <div className="summary-item">
          <div className="label">Cumulative baseline cost</div>
          <div className="value">{totals.baseline} €</div>
        </div>
        <div className="summary-item">
          <div className="label">Cumulative model cost</div>
          <div className="value accent">{totals.model} €</div>
        </div>
        <div className="summary-item">
          <div className="label">Cumulative difference</div>
          <div className={`value ${totals.saved >= 0 ? 'success' : 'warn'}`}>
            {totals.saved >= 0 ? '+' : ''}
            {totals.saved} €
          </div>
        </div>
        <div className="summary-item">
          <div className="label">Days in range</div>
          <div className="value small">{totals.days}</div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={data}>
          <CartesianGrid stroke="#3a3a3a" strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            stroke="#737373"
            interval={Math.max(0, Math.floor(data.length / 12) - 1)}
            angle={-35}
            textAnchor="end"
            height={60}
          />
          <YAxis
            yAxisId="kg"
            stroke="#737373"
            label={{ value: 'Waste (kg)', angle: -90, position: 'insideLeft', fill: '#737373' }}
          />
          <Tooltip
            contentStyle={{ background: '#1f1f1f', border: '1px solid #3a3a3a', color: '#e4e4e4' }}
          />
          <Legend />
          <Bar yAxisId="kg" dataKey="baselineWasteKg" name="Baseline waste (kg)" fill="#f0a040" />
          <Bar yAxisId="kg" dataKey="modelWasteKg" name="Model waste (kg)" fill="#599ce7" />
        </ComposedChart>
      </ResponsiveContainer>

      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={data}>
          <CartesianGrid stroke="#3a3a3a" strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            stroke="#737373"
            interval={Math.max(0, Math.floor(data.length / 12) - 1)}
            angle={-35}
            textAnchor="end"
            height={60}
          />
          <YAxis
            stroke="#737373"
            label={{ value: 'Daily cost (€)', angle: -90, position: 'insideLeft', fill: '#737373' }}
          />
          <Tooltip
            contentStyle={{ background: '#1f1f1f', border: '1px solid #3a3a3a', color: '#e4e4e4' }}
          />
          <Legend />
          <Line type="monotone" dataKey="baselineCost" name="Baseline cost (€)" stroke="#f0a040" dot={false} />
          <Line type="monotone" dataKey="modelCost" name="Model cost (€)" stroke="#599ce7" dot={false} />
          <Line type="monotone" dataKey="costSaved" name="Daily savings (€)" stroke="#3fa266" dot={false} />
        </ComposedChart>
      </ResponsiveContainer>

      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={data}>
          <CartesianGrid stroke="#3a3a3a" strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            stroke="#737373"
            interval={Math.max(0, Math.floor(data.length / 12) - 1)}
            angle={-35}
            textAnchor="end"
            height={60}
          />
          <YAxis
            stroke="#737373"
            label={{ value: 'Cumulative cost (€)', angle: -90, position: 'insideLeft', fill: '#737373' }}
          />
          <Tooltip
            contentStyle={{ background: '#1f1f1f', border: '1px solid #3a3a3a', color: '#e4e4e4' }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="cumulativeBaselineCost"
            name="Cumulative baseline (€)"
            stroke="#f0a040"
            dot={false}
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="cumulativeModelCost"
            name="Cumulative model (€)"
            stroke="#599ce7"
            dot={false}
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="cumulativeCostSaved"
            name="Cumulative difference (€)"
            stroke="#3fa266"
            dot={false}
            strokeWidth={2}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
