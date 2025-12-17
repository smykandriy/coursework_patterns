import { Card, CardContent, Stack, Typography } from '@mui/material'

const AdminPage = () => {
  return (
    <Stack spacing={2}>
      <Typography variant="h4">Admin Dashboard</Typography>
      <Typography variant="body1" color="text.secondary">
        Role management, fleet oversight, and reporting will be built in later phases.
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="body2" color="text.secondary">
            Admin controls are not yet implemented in this scaffold.
          </Typography>
        </CardContent>
      </Card>
    </Stack>
  )
}

export default AdminPage
