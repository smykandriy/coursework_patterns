import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react'

import { clearStoredTokens, getStoredTokens, setStoredTokens, subscribeToAuthChanges } from '../api/authStorage'
import authService from '../services/authService'
import { AuthTokens, User, UserRole } from '../types'

interface AuthContextValue {
  user: User | null
  tokens: AuthTokens | null
  loading: boolean
  login: (credentials: { username: string; password: string }) => Promise<void>
  register: (payload: RegisterPayload) => Promise<User>
  logout: () => void
  hasRole: (roles?: UserRole[]) => boolean
  refreshProfile: () => Promise<void>
}

interface RegisterPayload {
  username: string
  email: string
  password: string
  full_name: string
  phone: string
  driver_license_no: string
  address: string
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null)
  const [tokens, setTokensState] = useState<AuthTokens | null>(getStoredTokens())
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = subscribeToAuthChanges((newTokens) => {
      setTokensState(newTokens)
    })
    return () => {
      unsubscribe()
    }
  }, [])

  useEffect(() => {
    const bootstrap = async () => {
      if (!tokens) {
        setLoading(false)
        return
      }
      try {
        const profile = await authService.me()
        setUser(profile)
      } catch {
        clearStoredTokens()
        setUser(null)
      } finally {
        setLoading(false)
      }
    }
    bootstrap()
  }, [tokens])

  const login = async (credentials: { username: string; password: string }) => {
    const tokenResponse = await authService.login(credentials)
    setStoredTokens(tokenResponse)
    setTokensState(tokenResponse)
    const profile = await authService.me()
    setUser(profile)
  }

  const register = async (payload: RegisterPayload) => {
    const created = await authService.register(payload)
    return created
  }

  const logout = () => {
    clearStoredTokens()
    setTokensState(null)
    setUser(null)
  }

  const refreshProfile = async () => {
    if (!tokens) return
    const profile = await authService.me()
    setUser(profile)
  }

  const hasRole = (roles?: UserRole[]) => {
    if (!roles || roles.length === 0) return !!user
    return !!user && roles.includes(user.role)
  }

  const value = useMemo(
    () => ({
      user,
      tokens,
      loading,
      login,
      register,
      logout,
      hasRole,
      refreshProfile
    }),
    [user, tokens, loading]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
