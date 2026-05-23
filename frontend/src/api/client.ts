export interface PrepPolicyResult {
  prep: number
  waste_portions: number
  shortage_portions: number
  waste_kg: number
  waste_cost_eur: number
  shortage_penalty_eur: number
  total_cost_eur: number
}

export interface PrepComparison {
  max_capacity: number
  actual_visitors: number
  model_predicted_visitors: number
  baseline: PrepPolicyResult
  model: PrepPolicyResult
  cost_saved_eur: number
  waste_saved_kg: number
  waste_saved_pct: number
}

export interface LLMScores {
  menu_appeal: number
  competitor_pressure: number
  weather_effect: number
  overall_demand_signal: number
  rationale: string
}

export interface ForecastResponse {
  date: string
  actual_visitors: number
  predicted_visitors: number
  recommended_prep: number
  waste_saved_pct: number
  model_source: string
  llm_scores: LLMScores | null
  prep_comparison: PrepComparison
  breakdown: {
    naive: number
    gbm: number
    hybrid: number
  }
  inputs: {
    own_menu_text: string
    competitor_1_menu: string
    competitor_2_menu: string
    competitor_3_menu: string
    weather_condition: string
    weather_temp_c: number
    weather_precip_mm: number
    nominal_capacity: number
  }
}

export interface WasteHistoryItem {
  date: string
  actual_visitors: number
  baseline_prep: number
  model_prep: number
  baseline_waste_kg: number
  model_waste_kg: number
  baseline_cost_eur: number
  model_cost_eur: number
  cost_saved_eur: number
  cumulative_baseline_cost_eur: number
  cumulative_model_cost_eur: number
  cumulative_cost_saved_eur: number
  baseline_shortage: number
  model_shortage: number
}

export interface HistoryItem {
  date: string
  day_of_week: number
  visitor_count: number
  own_menu_text: string
  competitor_1_menu: string
  competitor_2_menu: string
  competitor_3_menu: string
  weather_condition: string
  weather_temp_c: number
  weather_precip_mm: number
  week_of_semester: number
  nominal_capacity: number
}

export interface HistorySummary {
  total_records: number
  start_date: string
  end_date: string
  avg_visitors: number
  min_visitors: number
  max_visitors: number
  unique_menus: number
  nominal_capacity: number
  baseline_prep: number
}

export interface HealthResponse {
  status: string
  records: number
  llm_available: boolean
}

export interface MetricsResponse {
  llm_available: boolean
  message?: string
  holdout_days?: number
  mae_hybrid?: number
  avg_waste_saved_pct?: number
  avg_cost_saved_eur?: number
  total_cost_saved_eur?: number
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, init)
  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed: ${response.status}`)
  }
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<HealthResponse>('/api/health'),
  history: (limit = 0) => request<{ items: HistoryItem[] }>(`/api/history?limit=${limit}`),
  historySummary: () => request<HistorySummary>('/api/history/summary'),
  wasteHistory: (limit = 365) => request<{ items: WasteHistoryItem[] }>(`/api/waste/history?limit=${limit}`),
  forecast: (date: string) => request<ForecastResponse>(`/api/forecast/${date}`),
  metrics: () => request<MetricsResponse>('/api/metrics'),
}

export const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
