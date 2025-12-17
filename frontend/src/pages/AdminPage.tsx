import { Box, Card, CardActionArea, CardContent, Grid, Typography } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'

const AdminPage = () => {
  const cards = [
    {
      title: 'Manage cars',
      description: 'Create, update, and retire vehicles from the fleet.',
      to: '/manage/cars'
    },
    {
      title: 'Booking queue',
      description: 'Confirm, check-in, return, or cancel reservations.',
      to: '/manage/bookings'
    }
  ]

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Manager console
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 2 }}>
        Use the tools below to manage inventory and active reservations.
      </Typography>
      <Grid container spacing={2}>
        {cards.map((card) => (
          <Grid item xs={12} md={6} key={card.to}>
            <Card variant="outlined">
              <CardActionArea component={RouterLink} to={card.to}>
                <CardContent>
                  <Typography variant="h6">{card.title}</Typography>
                  <Typography color="text.secondary">{card.description}</Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  )
}

export default AdminPage
