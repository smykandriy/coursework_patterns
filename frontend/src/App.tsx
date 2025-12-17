import { Container } from '@mui/material'
import { Route, Routes } from 'react-router-dom'

import NavBar from './components/NavBar'
import AdminPage from './pages/AdminPage'
import CarsPage from './pages/CarsPage'
import LoginPage from './pages/LoginPage'
import MyBookingsPage from './pages/MyBookingsPage'
import RegisterPage from './pages/RegisterPage'

const App = () => {
  return (
    <>
      <NavBar />
      <Container maxWidth="lg">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/cars" element={<CarsPage />} />
          <Route path="/bookings" element={<MyBookingsPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="*" element={<CarsPage />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
