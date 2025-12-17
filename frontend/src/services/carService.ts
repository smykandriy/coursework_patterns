import apiClient from '../api/client'
import { Car } from '../types'

export interface CarFilters {
  make?: string
  model?: string
  type?: string
  status?: string
  year_min?: string
  year_max?: string
  search?: string
  page?: number
}

const carService = {
  async listCars(filters: CarFilters = {}): Promise<{ results: Car[]; count?: number }> {
    const response = await apiClient.get('/cars/', { params: filters })
    if (Array.isArray(response.data)) {
      return { results: response.data }
    }
    return { results: response.data.results ?? [], count: response.data.count }
  },

  async getCar(id: string): Promise<Car> {
    const response = await apiClient.get(`/cars/${id}/`)
    return response.data as Car
  },

  async createCar(payload: Omit<Car, 'id'>): Promise<Car> {
    const response = await apiClient.post('/cars/', payload)
    return response.data as Car
  },

  async updateCar(id: string, payload: Partial<Car>): Promise<Car> {
    const response = await apiClient.patch(`/cars/${id}/`, payload)
    return response.data as Car
  },

  async deleteCar(id: string): Promise<void> {
    await apiClient.delete(`/cars/${id}/`)
  }
}

export default carService
