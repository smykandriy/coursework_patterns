import { Container, Typography } from '@mui/material'

const CarsPage = () => {
  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Cars
      </Typography>
      <Typography variant="body1">
        Vehicle browsing and filters will appear here once the inventory service is available.
      </Typography>
    </Container>
  )
}

export default CarsPage
