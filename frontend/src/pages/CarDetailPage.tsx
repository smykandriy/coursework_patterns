import {
  Box,
  Button,
  Card,
  CardContent,
  Divider,
  Grid,
  Stack,
  TextField,
  Typography
} from '@mui/material'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useNavigate, useParams } from 'react-router-dom'

import ErrorAlert from '../components/ErrorAlert'
import LoadingState from '../components/LoadingState'
import { useAuth } from '../context/AuthContext'
import bookingService from '../services/bookingService'
import carService from '../services/carService'
import pricingService from '../services/pricingService'
import { Car, QuoteResponse } from '../types'

interface QuoteForm {
  start_date: string
  end_date: string
}

const CarDetailPage = () => {
  const { carId } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [car, setCar] = useState<Car | null>(null)
  const [quote, setQuote] = useState<QuoteResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<QuoteForm>({
    defaultValues: {
      start_date: '',
      end_date: ''
    }
  })

  useEffect(() => {
    const loadCar = async () => {
      if (!carId) return
      setLoading(true)
      setError('')
      try {
        const data = await carService.getCar(carId)
        setCar(data)
      } catch (err: any) {
        setError(err?.response?.data?.detail ?? 'Unable to load car details.')
      } finally {
        setLoading(false)
      }
    }
    loadCar()
  }, [carId])

  const onQuote = async (formData: QuoteForm) => {
    if (!carId) return
    setSuccess('')
    setError('')
    try {
      const quoteResponse = await pricingService.quote(
        carId,
        formData.start_date,
        formData.end_date
      )
      setQuote(quoteResponse)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to retrieve quote.')
    }
  }

  const onCreateBooking = async (formData: QuoteForm) => {
    if (!carId) return
    if (!user) {
      setError('Please login to create a booking.')
      return
    }
    setError('')
    setSuccess('')
    try {
      const booking = await bookingService.createBooking({
        car_id: carId,
        start_date: formData.start_date,
        end_date: formData.end_date
      })
      setSuccess('Booking created successfully.')
      navigate(`/bookings/${booking.id}`)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to create booking.')
    }
  }

  if (loading) {
    return <LoadingState label="Loading car..." />
  }

  if (!car) {
    return <ErrorAlert message={error || 'Car not found.'} />
  }

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        {car.make} {car.model} ({car.year})
      </Typography>
      <ErrorAlert message={error} />
      {success && (
        <Card sx={{ mb: 2, borderColor: 'success.main' }} variant="outlined">
          <CardContent>
            <Typography color="success.main">{success}</Typography>
          </CardContent>
        </Card>
      )}
      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Vehicle details
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Make</Typography>
                  <Typography>{car.make}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Model</Typography>
                  <Typography>{car.model}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Year</Typography>
                  <Typography>{car.year}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">VIN</Typography>
                  <Typography>{car.vin}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Type</Typography>
                  <Typography sx={{ textTransform: 'capitalize' }}>{car.type}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Status</Typography>
                  <Typography sx={{ textTransform: 'capitalize' }}>{car.status}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Base Price / day</Typography>
                  <Typography>${car.base_price_per_day}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Mileage</Typography>
                  <Typography>{car.mileage.toLocaleString()} km</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography color="text.secondary">Last service</Typography>
                  <Typography>{car.last_service_at ?? 'Not recorded'}</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={5}>
          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Get quote & book
              </Typography>
              {!user && (
                <Typography color="text.secondary" sx={{ mb: 2 }}>
                  You can browse publicly. Sign in to complete a booking.
                </Typography>
              )}
              <Stack
                component="form"
                spacing={2}
                onSubmit={handleSubmit((data) => {
                  onQuote(data)
                })}
              >
                <TextField
                  label="Start date"
                  type="date"
                  InputLabelProps={{ shrink: true }}
                  {...register('start_date', { required: 'Start date is required' })}
                  error={Boolean(errors.start_date)}
                  helperText={errors.start_date?.message}
                />
                <TextField
                  label="End date"
                  type="date"
                  InputLabelProps={{ shrink: true }}
                  {...register('end_date', { required: 'End date is required' })}
                  error={Boolean(errors.end_date)}
                  helperText={errors.end_date?.message}
                />
                <Stack direction="row" spacing={1}>
                  <Button type="submit" variant="contained">
                    Get quote
                  </Button>
                  <Button variant="outlined" onClick={handleSubmit(onCreateBooking)} disabled={!user}>
                    Create booking
                  </Button>
                </Stack>
              </Stack>
              {quote && (
                <Box sx={{ mt: 3 }}>
                  <Divider sx={{ mb: 2 }} />
                  <Typography variant="subtitle1" gutterBottom>
                    Quote
                  </Typography>
                  {quote.breakdown.map((item, idx) => (
                    <Stack
                      key={idx}
                      direction="row"
                      justifyContent="space-between"
                      sx={{ mb: 1 }}
                    >
                      <Typography color="text.secondary">{item.label}</Typography>
                      <Typography>${item.amount}</Typography>
                    </Stack>
                  ))}
                  <Stack direction="row" justifyContent="space-between" sx={{ mt: 1 }}>
                    <Typography variant="h6">Total</Typography>
                    <Typography variant="h6">${quote.total}</Typography>
                  </Stack>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default CarDetailPage
