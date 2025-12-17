import { CircularProgress, Container } from '@mui/material'
import { Navigate, useLocation } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'
import { UserRole } from '../types'

interface ProtectedRouteProps {
  children: JSX.Element
  roles?: UserRole[]
}

const ProtectedRoute = ({ children, roles }: ProtectedRouteProps) => {
  const { user, loading, hasRole } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <Container sx={{ py: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress />
      </Container>
    )
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  if (!hasRole(roles)) {
    return <Navigate to="/cars" replace />
  }

  return children
}

export default ProtectedRoute
