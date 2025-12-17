import { Card, CardContent, Stack, Typography } from '@mui/material'

const MyBookingsPage = () => {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">My Bookings</Typography>
      <Typography variant="body1" color="text.secondary">
        Booking history and management tools will be added once the backend services are
        available.
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            No bookings yet. Reserve a vehicle to see it listed here.
          </Typography>
        </CardContent>
      </Card>
    </Stack>
  )
}

export default MyBookingsPage
