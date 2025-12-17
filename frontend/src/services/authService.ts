import apiClient from '../api/client'
import { AuthTokens, User } from '../types'

const authService = {
  async login(payload: { username: string; password: string }): Promise<AuthTokens> {
    const response = await apiClient.post('/auth/login/', payload)
    return { access: response.data.access, refresh: response.data.refresh }
  },

  async register(payload: {
    username: string
    email: string
    password: string
    full_name: string
    phone: string
    driver_license_no: string
    address: string
  }): Promise<User> {
    const response = await apiClient.post('/auth/register/', payload)
    return response.data as User
  },

  async refresh(refresh: string): Promise<AuthTokens> {
    const response = await apiClient.post('/auth/refresh/', { refresh })
    return { access: response.data.access, refresh: response.data.refresh ?? refresh }
  },

  async me(): Promise<User> {
    const response = await apiClient.get('/auth/me/')
    return response.data as User
  }
}

export default authService
