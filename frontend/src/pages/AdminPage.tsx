import { Container, Typography } from '@mui/material'

const AdminPage = () => {
  return (
    <Container sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Admin Dashboard
      </Typography>
      <Typography variant="body1">
        Administrative tools will be introduced once foundational services are implemented.
      </Typography>
    </Container>
  )
}

export default AdminPage
