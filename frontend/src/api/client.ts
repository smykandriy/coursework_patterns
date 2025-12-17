import axios from 'axios'

declare module 'axios' {
  export interface AxiosRequestConfig {
    _retry?: boolean
  }
}

import { clearStoredTokens, getStoredTokens, setStoredTokens } from './authStorage'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  withCredentials: true
})

apiClient.interceptors.request.use((config) => {
  const tokens = getStoredTokens()
  if (tokens?.access) {
    config.headers.Authorization = `Bearer ${tokens.access}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url?.includes('/auth/login') &&
      !originalRequest.url?.includes('/auth/refresh')
    ) {
      const tokens = getStoredTokens()
      if (!tokens?.refresh) {
        clearStoredTokens()
        return Promise.reject(error)
      }

      originalRequest._retry = true
      try {
        const refreshResponse = await axios.post(
          `${apiClient.defaults.baseURL}/auth/refresh/`,
          { refresh: tokens.refresh },
          { withCredentials: true }
        )
        const newTokens = {
          access: refreshResponse.data.access,
          refresh: refreshResponse.data.refresh ?? tokens.refresh
        }
        setStoredTokens(newTokens)
        originalRequest.headers.Authorization = `Bearer ${newTokens.access}`
        return apiClient(originalRequest)
      } catch (refreshError) {
        clearStoredTokens()
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default apiClient
