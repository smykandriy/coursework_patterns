import {
  AppBar,
  Avatar,
  Box,
  Button,
  Divider,
  IconButton,
  Menu,
  MenuItem,
  Stack,
  Toolbar,
  Typography
} from '@mui/material'
import { useState } from 'react'
import { Link as RouterLink, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'

const NavBar = () => {
  const { user, logout } = useAuth()
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const navigate = useNavigate()

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => setAnchorEl(null)

  const handleLogout = () => {
    logout()
    handleMenuClose()
    navigate('/login')
  }

  const isManager = user?.role === 'manager' || user?.role === 'admin'

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Car Rental System
        </Typography>
        <Stack direction="row" spacing={2}>
          <Button color="inherit" component={RouterLink} to="/cars">
            Cars
          </Button>
          {user && (
            <Button color="inherit" component={RouterLink} to="/bookings">
              My Bookings
            </Button>
          )}
          {isManager && (
            <>
              <Button color="inherit" component={RouterLink} to="/manage/cars">
                Cars Admin
              </Button>
              <Button color="inherit" component={RouterLink} to="/manage/bookings">
                Booking Queue
              </Button>
            </>
          )}
          {!user && (
            <>
              <Button color="inherit" component={RouterLink} to="/login">
                Login
              </Button>
              <Button color="inherit" component={RouterLink} to="/register">
                Register
              </Button>
            </>
          )}
          {user && (
            <Box>
              <IconButton color="inherit" onClick={handleMenuOpen}>
                <Avatar sx={{ width: 28, height: 28 }}>
                  {user.username.substring(0, 1).toUpperCase()}
                </Avatar>
              </IconButton>
              <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleMenuClose}>
                <MenuItem disabled>{user.email}</MenuItem>
                <MenuItem disabled sx={{ textTransform: 'capitalize' }}>
                  Role: {user.role}
                </MenuItem>
                <Divider />
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </Box>
          )}
        </Stack>
      </Toolbar>
    </AppBar>
  )
}

export default NavBar
