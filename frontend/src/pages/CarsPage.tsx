import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Chip,
  Grid,
  Stack,
  TextField,
  Typography
} from '@mui/material'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'
import { Link as RouterLink } from 'react-router-dom'

import ErrorAlert from '../components/ErrorAlert'
import LoadingState from '../components/LoadingState'
import carService, { CarFilters } from '../services/carService'
import { Car } from '../types'

const CarsPage = () => {
  const [cars, setCars] = useState<Car[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const { register, handleSubmit, reset } = useForm<CarFilters>({
    defaultValues: { make: '', model: '', search: '' }
  })

  const fetchCars = async (filters: CarFilters = {}) => {
    setLoading(true)
    setError('')
    try {
      const response = await carService.listCars(filters)
      setCars(response.results)
    } catch (err: any) {
      setError(
        err?.response?.status === 401
          ? 'Login is required to browse inventory.'
          : err?.response?.data?.detail ?? 'Unable to load cars.'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCars()
  }, [])

  const onFilter = (values: CarFilters) => {
    fetchCars(values)
  }

  const clearFilters = () => {
    reset({ make: '', model: '', type: '', status: '', year_min: '', year_max: '', search: '' })
    fetchCars()
  }

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Cars
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
        Browse available vehicles and filter by make, model, or status.
      </Typography>
      <ErrorAlert message={error} />
      <Card variant="outlined" sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Filters
          </Typography>
          <Stack
            component="form"
            spacing={2}
            direction={{ xs: 'column', md: 'row' }}
            alignItems="flex-end"
            onSubmit={handleSubmit(onFilter)}
          >
            <TextField label="Make" {...register('make')} />
            <TextField label="Model" {...register('model')} />
            <TextField label="Type" {...register('type')} />
            <TextField label="Status" {...register('status')} />
            <TextField label="Year min" type="number" {...register('year_min')} />
            <TextField label="Year max" type="number" {...register('year_max')} />
            <TextField label="Search" {...register('search')} />
            <Stack direction="row" spacing={1}>
              <Button type="submit" variant="contained">
                Apply
              </Button>
              <Button variant="text" onClick={clearFilters}>
                Reset
              </Button>
            </Stack>
          </Stack>
        </CardContent>
      </Card>
      {loading ? (
        <LoadingState label="Loading cars..." />
      ) : (
        <Grid container spacing={2}>
          {cars.map((car) => (
            <Grid item xs={12} md={6} lg={4} key={car.id}>
              <Card variant="outlined" sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    {car.make} {car.model} ({car.year})
                  </Typography>
                  <Stack spacing={1}>
                    <Typography color="text.secondary">Type: {car.type}</Typography>
                    <Typography color="text.secondary">
                      Rate: ${car.base_price_per_day} / day
                    </Typography>
                    <Typography color="text.secondary">Mileage: {car.mileage} km</Typography>
                    <Chip label={car.status} size="small" sx={{ textTransform: 'capitalize' }} />
                  </Stack>
                </CardContent>
                <CardActions>
                  <Button component={RouterLink} to={`/cars/${car.id}`} size="small">
                    View details
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
      {!loading && !error && cars.length === 0 && (
        <Typography sx={{ mt: 2 }}>No cars match the selected filters.</Typography>
      )}
    </Box>
  )
}

export default CarsPage
