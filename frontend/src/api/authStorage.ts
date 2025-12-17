import { AuthTokens } from '../types'

type Listener = (tokens: AuthTokens | null) => void

const STORAGE_KEY = 'car-rental-auth'
const listeners = new Set<Listener>()

export const getStoredTokens = (): AuthTokens | null => {
  const raw = localStorage.getItem(STORAGE_KEY)
  if (!raw) return null
  try {
    return JSON.parse(raw) as AuthTokens
  } catch {
    return null
  }
}

export const setStoredTokens = (tokens: AuthTokens) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tokens))
  listeners.forEach((listener) => listener(tokens))
}

export const clearStoredTokens = () => {
  localStorage.removeItem(STORAGE_KEY)
  listeners.forEach((listener) => listener(null))
}

export const subscribeToAuthChanges = (listener: Listener) => {
  listeners.add(listener)
  return () => listeners.delete(listener)
}
