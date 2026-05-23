import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import type { HistoryItem } from '../api/client'

interface Props {
  items: HistoryItem[]
  selectedDate: string
  range: number
}

export function HistoryChart({ items, selectedDate, range }: Props) {
  const sliced = range <= 0 || range >= items.length ? items : items.slice(-range)
  const data = sliced.map((item) => ({
    date: item.date.slice(2),
    visitors: item.visitor_count,
    selected: item.date === selectedDate,
  }))

  return (
    <ResponsiveContainer width="100%" height={320}>
      <LineChart data={data}>
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
          label={{ value: 'Visitors', angle: -90, position: 'insideLeft', fill: '#737373' }}
        />
        <Tooltip
          contentStyle={{ background: '#1f1f1f', border: '1px solid #3a3a3a', color: '#e4e4e4' }}
        />
        <Legend />
        <Line type="monotone" dataKey="visitors" name="Actual visitors" stroke="#599ce7" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}
