import { Box, Button, Card, CardContent, Stack, TextField, Typography } from '@mui/material'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { useLocation, useNavigate, Link as RouterLink } from 'react-router-dom'

import ErrorAlert from '../components/ErrorAlert'
import { useAuth } from '../context/AuthContext'

interface LoginForm {
  username: string
  password: string
}

const LoginPage = () => {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const from = (location.state as any)?.from?.pathname || '/cars'

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<LoginForm>({
    defaultValues: { username: '', password: '' }
  })

  const onSubmit = async (data: LoginForm) => {
    setError('')
    setSubmitting(true)
    try {
      await login(data)
      navigate(from, { replace: true })
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to sign in.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box sx={{ py: 4, display: 'flex', justifyContent: 'center' }}>
      <Card sx={{ maxWidth: 480, width: '100%' }} variant="outlined">
        <CardContent>
          <Typography variant="h4" gutterBottom>
            Login
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 2 }}>
            Sign in to manage bookings and reservations.
          </Typography>
          <ErrorAlert message={error} />
          <Stack component="form" spacing={2} onSubmit={handleSubmit(onSubmit)}>
            <TextField
              label="Username"
              {...register('username', { required: 'Username is required' })}
              error={Boolean(errors.username)}
              helperText={errors.username?.message}
            />
            <TextField
              label="Password"
              type="password"
              {...register('password', { required: 'Password is required' })}
              error={Boolean(errors.password)}
              helperText={errors.password?.message}
            />
            <Button type="submit" variant="contained" disabled={submitting}>
              {submitting ? 'Signing in...' : 'Login'}
            </Button>
          </Stack>
          <Typography sx={{ mt: 2 }}>
            No account?{' '}
            <RouterLink to="/register" style={{ textDecoration: 'none' }}>
              Register
            </RouterLink>
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}

export default LoginPage
