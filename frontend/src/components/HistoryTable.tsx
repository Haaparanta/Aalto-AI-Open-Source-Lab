import { DAY_NAMES, type HistoryItem } from '../api/client'

interface Props {
  items: HistoryItem[]
  selectedDate: string
}

export function HistoryTable({ items, selectedDate }: Props) {
  const reversed = [...items].reverse()

  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Day</th>
            <th>Visitors</th>
            <th>Menu</th>
            <th>Weather</th>
            <th>Competitors</th>
          </tr>
        </thead>
        <tbody>
          {reversed.map((item) => (
            <tr key={item.date} className={item.date === selectedDate ? 'row-selected' : undefined}>
              <td>{item.date}</td>
              <td>{DAY_NAMES[item.day_of_week]}</td>
              <td>{item.visitor_count}</td>
              <td>{item.own_menu_text}</td>
              <td>
                {item.weather_condition}, {item.weather_temp_c}C, {item.weather_precip_mm}mm
              </td>
              <td>
                {item.competitor_1_menu}; {item.competitor_2_menu}; {item.competitor_3_menu}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
