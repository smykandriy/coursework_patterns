import { AppBar, Button, Stack, Toolbar, Typography } from '@mui/material'
import { Link as RouterLink } from 'react-router-dom'

const NavBar = () => {
  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Car Rental System
        </Typography>
        <Stack direction="row" spacing={2}>
          <Button color="inherit" component={RouterLink} to="/login">
            Login
          </Button>
          <Button color="inherit" component={RouterLink} to="/register">
            Register
          </Button>
          <Button color="inherit" component={RouterLink} to="/cars">
            Cars
          </Button>
          <Button color="inherit" component={RouterLink} to="/bookings">
            My Bookings
          </Button>
          <Button color="inherit" component={RouterLink} to="/admin">
            Admin
          </Button>
        </Stack>
      </Toolbar>
    </AppBar>
  )
}

export default NavBar
