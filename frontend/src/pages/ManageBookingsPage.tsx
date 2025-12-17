import {
  Box,
  Button,
  Card,
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

const ManageBookingsPage = () => {
  const [bookings, setBookings] = useState<Booking[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

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

  const handleAction = async (id: string, action: 'confirm' | 'checkin' | 'return' | 'cancel') => {
    setError('')
    setSuccess('')
    try {
      const updated =
        action === 'confirm'
          ? await bookingService.confirmBooking(id)
          : action === 'checkin'
            ? await bookingService.checkinBooking(id)
            : action === 'return'
              ? await bookingService.returnBooking(id)
              : await bookingService.cancelBooking(id)
      setBookings((prev) => prev.map((b) => (b.id === id ? updated : b)))
      setSuccess(`Booking ${action}ed.`)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Action failed.')
    }
  }

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Booking queue
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 2 }}>
        Manage confirmations, check-ins, returns, and cancellations.
      </Typography>
      <ErrorAlert message={error} />
      {success && (
        <Card variant="outlined" sx={{ mb: 2, borderColor: 'success.main' }}>
          <CardContent>
            <Typography color="success.main">{success}</Typography>
          </CardContent>
        </Card>
      )}
      {loading ? (
        <LoadingState label="Loading bookings..." />
      ) : (
        <Grid container spacing={2}>
          {bookings.map((booking) => (
            <Grid item xs={12} key={booking.id}>
              <Card variant="outlined">
                <CardContent>
                  <Stack
                    direction={{ xs: 'column', md: 'row' }}
                    justifyContent="space-between"
                    alignItems={{ xs: 'flex-start', md: 'center' }}
                    spacing={1}
                  >
                    <Box>
                      <Typography variant="h6">
                        {booking.car.make} {booking.car.model} ({booking.car.year})
                      </Typography>
                      <Typography color="text.secondary">
                        {booking.start_date} → {booking.end_date}
                      </Typography>
                      <Typography color="text.secondary">Status: {booking.status}</Typography>
                    </Box>
                    <Stack direction="row" spacing={1} alignItems="center">
                      <Chip label={booking.status} size="small" sx={{ textTransform: 'capitalize' }} />
                      <Button component={RouterLink} to={`/manage/bookings/${booking.id}`} size="small">
                        Detail
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => handleAction(booking.id, 'confirm')}
                        disabled={booking.status !== 'pending'}
                      >
                        Confirm
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => handleAction(booking.id, 'checkin')}
                        disabled={booking.status !== 'confirmed'}
                      >
                        Check-in
                      </Button>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => handleAction(booking.id, 'return')}
                        disabled={booking.status !== 'active'}
                      >
                        Return
                      </Button>
                      <Button
                        size="small"
                        color="error"
                        variant="outlined"
                        onClick={() => handleAction(booking.id, 'cancel')}
                        disabled={booking.status === 'canceled' || booking.status === 'completed'}
                      >
                        Cancel
                      </Button>
                    </Stack>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      {!loading && !error && bookings.length === 0 && (
        <Typography sx={{ mt: 2 }}>No bookings in the queue.</Typography>
      )}
    </Box>
  )
}

export default ManageBookingsPage
