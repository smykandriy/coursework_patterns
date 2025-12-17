export type UserRole = 'customer' | 'manager' | 'admin'

export interface CustomerProfile {
  full_name: string
  phone: string
  driver_license_no: string
  address: string
}

export interface User {
  id: string
  username: string
  email: string
  role: UserRole
  profile?: CustomerProfile
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface Car {
  id: string
  make: string
  model: string
  year: number
  vin: string
  type: string
  base_price_per_day: string
  status: 'available' | 'reserved' | 'rented' | 'service'
  mileage: number
  last_service_at?: string | null
}

export interface Booking {
  id: string
  customer: string
  car: Car
  start_date: string
  end_date: string
  status: 'pending' | 'confirmed' | 'active' | 'completed' | 'canceled'
  created_at: string
  updated_at: string
  fines: Fine[]
  deposit?: Deposit
  invoice?: Invoice
}

export interface Fine {
  id: string
  type: 'damage' | 'late_return' | 'cleaning' | 'other'
  amount: string
  notes?: string
  assessed_at: string
}

export interface Deposit {
  id: string
  amount: string
  status: 'held' | 'released' | 'partially_released' | 'forfeited'
  txn_ref?: string
  created_at: string
  updated_at: string
}

export interface Invoice {
  id: string
  breakdown: Array<{ label: string; amount: string }>
  total: string
  paid_at?: string | null
  method?: string
  payment_reference?: string
  created_at: string
  updated_at: string
}

export interface QuoteBreakdownItem {
  label: string
  amount: string
}

export interface QuoteResponse {
  total: string
  breakdown: QuoteBreakdownItem[]
}
