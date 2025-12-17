import { Container } from '@mui/material'
import { Navigate, Route, Routes } from 'react-router-dom'
import Navigation from './components/Navigation'
import AdminPage from './pages/AdminPage'
import CarsPage from './pages/CarsPage'
import LoginPage from './pages/LoginPage'
import MyBookingsPage from './pages/MyBookingsPage'
import NotFoundPage from './pages/NotFoundPage'
import RegisterPage from './pages/RegisterPage'

const App = () => {
  return (
    <>
      <Navigation />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Routes>
          <Route path="/" element={<Navigate to="/cars" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/cars" element={<CarsPage />} />
          <Route path="/bookings" element={<MyBookingsPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
