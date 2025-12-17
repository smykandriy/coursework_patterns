import { Box, Button, Card, CardContent, Grid, Stack, TextField, Typography } from '@mui/material'
import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link as RouterLink, useNavigate } from 'react-router-dom'

import ErrorAlert from '../components/ErrorAlert'
import { useAuth } from '../context/AuthContext'

interface RegisterForm {
  username: string
  email: string
  password: string
  full_name: string
  phone: string
  driver_license_no: string
  address: string
}

const RegisterPage = () => {
  const { register: registerUser } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<RegisterForm>({
    defaultValues: {
      username: '',
      email: '',
      password: '',
      full_name: '',
      phone: '',
      driver_license_no: '',
      address: ''
    }
  })

  const onSubmit = async (data: RegisterForm) => {
    setError('')
    setSubmitting(true)
    try {
      await registerUser(data)
      setSuccess('Account created. Please login to continue.')
      setTimeout(() => navigate('/login'), 800)
    } catch (err: any) {
      const resp = err?.response?.data
      const detail = resp?.detail
      const message =
        detail ||
        resp?.username?.[0] ||
        resp?.email?.[0] ||
        'Unable to complete registration.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box sx={{ py: 4, display: 'flex', justifyContent: 'center' }}>
      <Card sx={{ maxWidth: 720, width: '100%' }} variant="outlined">
        <CardContent>
          <Typography variant="h4" gutterBottom>
            Register
          </Typography>
          <Typography color="text.secondary" sx={{ mb: 2 }}>
            Create a customer account to book vehicles.
          </Typography>
          <ErrorAlert message={error} />
          {success && (
            <Card variant="outlined" sx={{ mb: 2, borderColor: 'success.main' }}>
              <CardContent>
                <Typography color="success.main">{success}</Typography>
              </CardContent>
            </Card>
          )}
          <Stack component="form" spacing={2} onSubmit={handleSubmit(onSubmit)}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Username"
                  fullWidth
                  {...register('username', { required: 'Username is required' })}
                  error={Boolean(errors.username)}
                  helperText={errors.username?.message}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Email"
                  fullWidth
                  type="email"
                  {...register('email', { required: 'Email is required' })}
                  error={Boolean(errors.email)}
                  helperText={errors.email?.message}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Password"
                  type="password"
                  fullWidth
                  {...register('password', {
                    required: 'Password is required',
                    minLength: { value: 8, message: 'Min 8 characters' }
                  })}
                  error={Boolean(errors.password)}
                  helperText={errors.password?.message}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Full name"
                  fullWidth
                  {...register('full_name', { required: 'Full name is required' })}
                  error={Boolean(errors.full_name)}
                  helperText={errors.full_name?.message}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Phone"
                  fullWidth
                  {...register('phone', { required: 'Phone is required' })}
                  error={Boolean(errors.phone)}
                  helperText={errors.phone?.message}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField
                  label="Driver license number"
                  fullWidth
                  {...register('driver_license_no', {
                    required: 'Driver license number is required'
                  })}
                  error={Boolean(errors.driver_license_no)}
                  helperText={errors.driver_license_no?.message}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Address"
                  fullWidth
                  multiline
                  minRows={2}
                  {...register('address', { required: 'Address is required' })}
                  error={Boolean(errors.address)}
                  helperText={errors.address?.message}
                />
              </Grid>
            </Grid>
            <Button type="submit" variant="contained" disabled={submitting}>
              {submitting ? 'Creating...' : 'Create account'}
            </Button>
          </Stack>
          <Typography sx={{ mt: 2 }}>
            Already registered?{' '}
            <RouterLink to="/login" style={{ textDecoration: 'none' }}>
              Login
            </RouterLink>
          </Typography>
        </CardContent>
      </Card>
    </Box>
  )
}

export default RegisterPage
