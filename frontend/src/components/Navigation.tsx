import { AppBar, Button, Stack, Toolbar, Typography } from '@mui/material'
import { Link as RouterLink, useLocation } from 'react-router-dom'

const navItems = [
  { label: 'Cars', to: '/cars' },
  { label: 'My Bookings', to: '/bookings' },
  { label: 'Admin', to: '/admin' },
  { label: 'Login', to: '/login' },
  { label: 'Register', to: '/register' },
]

const Navigation = () => {
  const location = useLocation()

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          Car Rental System (Variant 19)
        </Typography>
        <Stack direction="row" spacing={1}>
          {navItems.map((item) => {
            const isActive =
              location.pathname === item.to ||
              location.pathname.startsWith(`${item.to}/`)

            return (
              <Button
                key={item.to}
                color="inherit"
                component={RouterLink}
                to={item.to}
                sx={{
                  textTransform: 'none',
                  fontWeight: isActive ? 700 : 500,
                }}
              >
                {item.label}
              </Button>
            )
          })}
        </Stack>
      </Toolbar>
    </AppBar>
  )
}

export default Navigation
