import { Button, Stack, Typography } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'

const NotFoundPage = () => {
  return (
    <Stack spacing={2} alignItems="flex-start">
      <Typography variant="h4">Page Not Found</Typography>
      <Typography variant="body1" color="text.secondary">
        The page you are looking for does not exist yet.
      </Typography>
      <Button variant="contained" component={RouterLink} to="/cars">
        Return to Cars
      </Button>
    </Stack>
  )
}

export default NotFoundPage
