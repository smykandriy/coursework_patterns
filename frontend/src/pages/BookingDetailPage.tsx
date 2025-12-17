import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Divider,
  Grid,
  Stack,
  TextField,
  Typography
} from '@mui/material'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { useParams } from 'react-router-dom'

import ErrorAlert from '../components/ErrorAlert'
import LoadingState from '../components/LoadingState'
import { useAuth } from '../context/AuthContext'
import bookingService from '../services/bookingService'
import { Booking, Fine } from '../types'

interface FineForm {
  type: Fine['type']
  amount: string
  notes?: string
}

interface DepositForm {
  amount: string
}

const BookingDetailPage = () => {
  const { bookingId } = useParams()
  const { user } = useAuth()
  const [booking, setBooking] = useState<Booking | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const fineForm = useForm<FineForm>({
    defaultValues: { type: 'other', amount: '', notes: '' }
  })

  const depositForm = useForm<DepositForm>({
    defaultValues: { amount: '250.00' }
  })

  const loadBooking = async () => {
    if (!bookingId) return
    setLoading(true)
    setError('')
    try {
      const data = await bookingService.getBooking(bookingId)
      setBooking(data)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to load booking.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadBooking()
  }, [bookingId])

  const handleAction = async (fn: () => Promise<any>, successMessage: string) => {
    setError('')
    setMessage('')
    try {
      await fn()
      setMessage(successMessage)
      await loadBooking()
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Action failed.')
    }
  }

  const isManager = user?.role === 'manager' || user?.role === 'admin'

  if (loading) {
    return <LoadingState label="Loading booking..." />
  }

  if (!booking) {
    return <ErrorAlert message={error || 'Booking not found.'} />
  }

  return (
    <Box sx={{ py: 4 }}>
      <Stack direction="row" alignItems="center" spacing={2} sx={{ mb: 2 }}>
        <Typography variant="h4">
          Booking for {booking.car.make} {booking.car.model}
        </Typography>
        <Chip label={booking.status} sx={{ textTransform: 'capitalize' }} />
      </Stack>
      <Typography color="text.secondary" sx={{ mb: 2 }}>
        {booking.start_date} → {booking.end_date}
      </Typography>
      <ErrorAlert message={error} />
      {message && (
        <Card variant="outlined" sx={{ borderColor: 'success.main', mb: 2 }}>
          <CardContent>
            <Typography color="success.main">{message}</Typography>
          </CardContent>
        </Card>
      )}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card variant="outlined" sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Booking details
              </Typography>
              <Typography color="text.secondary">
                Vehicle: {booking.car.make} {booking.car.model} ({booking.car.year})
              </Typography>
              <Typography color="text.secondary">VIN: {booking.car.vin}</Typography>
              <Typography color="text.secondary" sx={{ mt: 1 }}>
                Created {new Date(booking.created_at).toLocaleString()}
              </Typography>
              <Typography color="text.secondary">
                Last updated {new Date(booking.updated_at).toLocaleString()}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Stack direction="row" spacing={1}>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={() =>
                    handleAction(() => bookingService.cancelBooking(booking.id), 'Booking canceled.')
                  }
                  disabled={booking.status === 'canceled' || booking.status === 'completed'}
                >
                  Cancel booking
                </Button>
                {isManager && (
                  <>
                    <Button
                      variant="outlined"
                      onClick={() =>
                        handleAction(
                          () => bookingService.confirmBooking(booking.id),
                          'Booking confirmed.'
                        )
                      }
                      disabled={booking.status !== 'pending'}
                    >
                      Confirm
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() =>
                        handleAction(
                          () => bookingService.checkinBooking(booking.id),
                          'Check-in recorded.'
                        )
                      }
                      disabled={booking.status !== 'confirmed'}
                    >
                      Check-in
                    </Button>
                    <Button
                      variant="outlined"
                      onClick={() =>
                        handleAction(
                          () => bookingService.returnBooking(booking.id),
                          'Vehicle returned.'
                        )
                      }
                      disabled={booking.status !== 'active'}
                    >
                      Return
                    </Button>
                  </>
                )}
              </Stack>
            </CardContent>
          </Card>

          <Card variant="outlined" sx={{ mb: 2 }}>
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">Invoice</Typography>
                {booking.invoice?.paid_at ? (
                  <Chip label="Paid" color="success" size="small" />
                ) : (
                  booking.invoice && (
                    <Chip label="Unpaid" color="warning" size="small" variant="outlined" />
                  )
                )}
              </Stack>
              {booking.invoice ? (
                <Box sx={{ mt: 2 }}>
                  {booking.invoice.breakdown.map((item, idx) => (
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
                    <Typography fontWeight="bold">Total</Typography>
                    <Typography fontWeight="bold">${booking.invoice.total}</Typography>
                  </Stack>
                  {!booking.invoice.paid_at && (
                    <Button
                      sx={{ mt: 2 }}
                      variant="contained"
                      onClick={() =>
                        handleAction(
                          () => bookingService.payInvoice(booking.id),
                          'Invoice marked as paid.'
                        )
                      }
                    >
                      Pay invoice (mock)
                    </Button>
                  )}
                </Box>
              ) : (
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  Invoice will be generated after return.
                </Typography>
              )}
            </CardContent>
          </Card>

          <Card variant="outlined">
            <CardContent>
              <Typography variant="h6">Fines</Typography>
              {booking.fines.length === 0 ? (
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  No fines assessed.
                </Typography>
              ) : (
                booking.fines.map((fine) => (
                  <Card key={fine.id} variant="outlined" sx={{ mt: 1 }}>
                    <CardContent>
                      <Stack direction="row" justifyContent="space-between">
                        <Typography sx={{ textTransform: 'capitalize' }}>
                          {fine.type.replace('_', ' ')}
                        </Typography>
                        <Typography>${fine.amount}</Typography>
                      </Stack>
                      <Typography color="text.secondary">
                        {new Date(fine.assessed_at).toLocaleString()}
                      </Typography>
                      {fine.notes && <Typography sx={{ mt: 1 }}>{fine.notes}</Typography>}
                    </CardContent>
                  </Card>
                ))
              )}
              {isManager && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle1" gutterBottom>
                    Add fine
                  </Typography>
                  <Stack
                    component="form"
                    spacing={2}
                    onSubmit={fineForm.handleSubmit((data) =>
                      handleAction(
                        () =>
                          bookingService.addFine(booking.id, {
                            type: data.type,
                            amount: data.amount,
                            notes: data.notes
                          }),
                        'Fine added.'
                      )
                    )}
                  >
                    <TextField label="Type" {...fineForm.register('type')} />
                    <TextField
                      label="Amount"
                      type="number"
                      {...fineForm.register('amount', { required: 'Amount is required' })}
                      error={Boolean(fineForm.formState.errors.amount)}
                      helperText={fineForm.formState.errors.amount?.message}
                    />
                    <TextField label="Notes" multiline minRows={2} {...fineForm.register('notes')} />
                    <Button type="submit" variant="outlined">
                      Apply fine
                    </Button>
                  </Stack>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card variant="outlined">
            <CardContent>
              <Stack direction="row" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">Deposit</Typography>
                {booking.deposit ? (
                  <Chip
                    label={booking.deposit.status}
                    size="small"
                    sx={{ textTransform: 'capitalize' }}
                  />
                ) : (
                  <Chip label="Not held" size="small" />
                )}
              </Stack>
              {booking.deposit ? (
                <Box sx={{ mt: 2 }}>
                  <Typography color="text.secondary">
                    Amount: ${booking.deposit.amount}
                  </Typography>
                  <Typography color="text.secondary">
                    Updated: {new Date(booking.deposit.updated_at).toLocaleString()}
                  </Typography>
                  {isManager && (
                    <Stack spacing={1} sx={{ mt: 2 }}>
                      <Button
                        variant="outlined"
                        onClick={() =>
                          handleAction(
                            () => bookingService.releaseDeposit(booking.id),
                            'Deposit released.'
                          )
                        }
                      >
                        Release deposit
                      </Button>
                      <Button
                        variant="outlined"
                        color="error"
                        onClick={() =>
                          handleAction(
                            () => bookingService.forfeitDeposit(booking.id),
                            'Deposit forfeited.'
                          )
                        }
                      >
                        Forfeit deposit
                      </Button>
                    </Stack>
                  )}
                </Box>
              ) : (
                <Typography color="text.secondary" sx={{ mt: 1 }}>
                  No deposit has been captured for this booking.
                </Typography>
              )}
              {isManager && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="subtitle1">Hold deposit</Typography>
                  <Stack
                    component="form"
                    spacing={2}
                    onSubmit={depositForm.handleSubmit((data) =>
                      handleAction(
                        () => bookingService.holdDeposit(booking.id, data.amount),
                        'Deposit held.'
                      )
                    )}
                  >
                    <TextField
                      label="Amount"
                      type="number"
                      {...depositForm.register('amount', { required: 'Amount is required' })}
                      error={Boolean(depositForm.formState.errors.amount)}
                      helperText={depositForm.formState.errors.amount?.message}
                    />
                    <Button type="submit" variant="outlined">
                      Hold deposit
                    </Button>
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

export default BookingDetailPage
