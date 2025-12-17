import apiClient from '../api/client'
import { Booking, Fine } from '../types'

export interface BookingPayload {
  car_id: string
  start_date: string
  end_date: string
}

const bookingService = {
  async listBookings(): Promise<{ results: Booking[]; count?: number }> {
    const response = await apiClient.get('/bookings/')
    if (Array.isArray(response.data)) {
      return { results: response.data }
    }
    return { results: response.data.results ?? [], count: response.data.count }
  },

  async getBooking(id: string): Promise<Booking> {
    const response = await apiClient.get(`/bookings/${id}/`)
    return response.data as Booking
  },

  async createBooking(payload: BookingPayload): Promise<Booking> {
    const response = await apiClient.post('/bookings/', payload)
    return response.data as Booking
  },

  async cancelBooking(id: string): Promise<Booking> {
    const response = await apiClient.post(`/bookings/${id}/cancel/`)
    return response.data as Booking
  },

  async confirmBooking(id: string): Promise<Booking> {
    const response = await apiClient.post(`/bookings/${id}/confirm/`)
    return response.data as Booking
  },

  async checkinBooking(id: string): Promise<Booking> {
    const response = await apiClient.post(`/bookings/${id}/checkin/`)
    return response.data as Booking
  },

  async returnBooking(id: string): Promise<Booking> {
    const response = await apiClient.post(`/bookings/${id}/return/`)
    return response.data as Booking
  },

  async listFines(id: string): Promise<Fine[]> {
    const response = await apiClient.get(`/bookings/${id}/fines/`)
    return response.data as Fine[]
  },

  async addFine(
    id: string,
    payload: { type: Fine['type']; amount: string; notes?: string }
  ): Promise<Fine> {
    const response = await apiClient.post(`/bookings/${id}/fines/`, payload)
    return response.data as Fine
  },

  async holdDeposit(id: string, amount: string) {
    const response = await apiClient.post(`/bookings/${id}/deposit/hold/`, { amount })
    return response.data
  },

  async releaseDeposit(id: string, partial = false) {
    const response = await apiClient.post(`/bookings/${id}/deposit/release/`, {
      partial
    })
    return response.data
  },

  async forfeitDeposit(id: string) {
    const response = await apiClient.post(`/bookings/${id}/deposit/forfeit/`)
    return response.data
  },

  async payInvoice(id: string, method = 'card') {
    const response = await apiClient.post(`/bookings/${id}/invoice/pay/`, { method })
    return response.data
  }
}

export default bookingService
