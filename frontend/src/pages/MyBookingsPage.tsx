import {
  Box,
  Card,
  CardActionArea,
  CardContent,
  Chip,
  Grid,
  Stack,
  Typography
} from '@mui/material'
import { useEffect, useState } from 'react'
import { Link as RouterLink } from 'react-router-dom'

import ErrorAlert from '../components/ErrorAlert'
import LoadingState from '../components/LoadingState'
import bookingService from '../services/bookingService'
import { Booking } from '../types'

const MyBookingsPage = () => {
  const [bookings, setBookings] = useState<Booking[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadBookings = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await bookingService.listBookings()
      setBookings(response.results)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to load bookings.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadBookings()
  }, [])

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        My Bookings
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 2 }}>
        Track reservation status, deposits, and invoices.
      </Typography>
      <ErrorAlert message={error} />
      {loading ? (
        <LoadingState label="Loading bookings..." />
      ) : (
        <Grid container spacing={2}>
          {bookings.map((booking) => (
            <Grid item xs={12} md={6} key={booking.id}>
              <Card variant="outlined">
                <CardActionArea component={RouterLink} to={`/bookings/${booking.id}`}>
                  <CardContent>
                    <Stack direction="row" justifyContent="space-between" alignItems="center">
                      <Typography variant="h6">
                        {booking.car.make} {booking.car.model}
                      </Typography>
                      <Chip
                        label={booking.status}
                        size="small"
                        sx={{ textTransform: 'capitalize' }}
                      />
                    </Stack>
                    <Typography color="text.secondary" sx={{ mt: 1 }}>
                      {booking.start_date} → {booking.end_date}
                    </Typography>
                    <Typography color="text.secondary">
                      Updated {new Date(booking.updated_at).toLocaleString()}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      {!loading && !error && bookings.length === 0 && (
        <Typography sx={{ mt: 2 }}>No bookings yet. Reserve a car to get started.</Typography>
      )}
    </Box>
  )
}

export default MyBookingsPage
