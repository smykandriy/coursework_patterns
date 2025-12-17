import { Container, Typography } from '@mui/material'

const MyBookingsPage = () => {
  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        My Bookings
      </Typography>
      <Typography variant="body1">Booking history and actions will be added in the booking service milestone.</Typography>
    </Container>
  )
}

export default MyBookingsPage
