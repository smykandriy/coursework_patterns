import { Container } from '@mui/material'
import { Route, Routes } from 'react-router-dom'

import NavBar from './components/NavBar'
import ProtectedRoute from './components/ProtectedRoute'
import AdminPage from './pages/AdminPage'
import BookingDetailPage from './pages/BookingDetailPage'
import CarDetailPage from './pages/CarDetailPage'
import CarsPage from './pages/CarsPage'
import LoginPage from './pages/LoginPage'
import ManageBookingsPage from './pages/ManageBookingsPage'
import ManageCarsPage from './pages/ManageCarsPage'
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
          <Route path="/cars/:carId" element={<CarDetailPage />} />
          <Route
            path="/bookings"
            element={
              <ProtectedRoute>
                <MyBookingsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/bookings/:bookingId"
            element={
              <ProtectedRoute>
                <BookingDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute roles={['manager', 'admin']}>
                <AdminPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/manage/cars"
            element={
              <ProtectedRoute roles={['manager', 'admin']}>
                <ManageCarsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/manage/bookings"
            element={
              <ProtectedRoute roles={['manager', 'admin']}>
                <ManageBookingsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/manage/bookings/:bookingId"
            element={
              <ProtectedRoute roles={['manager', 'admin']}>
                <BookingDetailPage />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<CarsPage />} />
        </Routes>
      </Container>
    </>
  )
}

export default App
