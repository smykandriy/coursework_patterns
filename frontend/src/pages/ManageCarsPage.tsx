import {
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Grid,
  Stack,
  TextField,
  Typography
} from '@mui/material'
import { useEffect, useState } from 'react'
import { useForm } from 'react-hook-form'

import ErrorAlert from '../components/ErrorAlert'
import LoadingState from '../components/LoadingState'
import carService from '../services/carService'
import { Car } from '../types'

type CarFormValues = Omit<Car, 'id'>

const ManageCarsPage = () => {
  const [cars, setCars] = useState<Car[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [editingCar, setEditingCar] = useState<Car | null>(null)
  const [success, setSuccess] = useState('')

  const createForm = useForm<CarFormValues>({
    defaultValues: {
      make: '',
      model: '',
      year: new Date().getFullYear(),
      vin: '',
      type: '',
      base_price_per_day: '0',
      status: 'available',
      mileage: 0,
      last_service_at: ''
    }
  })

  const editForm = useForm<CarFormValues>()

  const loadCars = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await carService.listCars()
      setCars(response.results)
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to load cars.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadCars()
  }, [])

  const handleCreate = async (values: CarFormValues) => {
    setError('')
    setSuccess('')
    try {
      await carService.createCar(values)
      setSuccess('Car created.')
      createForm.reset()
      loadCars()
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to create car.')
    }
  }

  const handleDelete = async (id: string) => {
    setError('')
    try {
      await carService.deleteCar(id)
      setSuccess('Car removed.')
      loadCars()
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to delete car.')
    }
  }

  const handleEditSubmit = async (values: CarFormValues) => {
    if (!editingCar) return
    setError('')
    setSuccess('')
    try {
      await carService.updateCar(editingCar.id, values)
      setSuccess('Car updated.')
      setEditingCar(null)
      loadCars()
    } catch (err: any) {
      setError(err?.response?.data?.detail ?? 'Unable to update car.')
    }
  }

  const openEdit = (car: Car) => {
    setEditingCar(car)
    editForm.reset({ ...car, last_service_at: car.last_service_at ?? '' })
  }

  return (
    <Box sx={{ py: 4 }}>
      <Typography variant="h4" gutterBottom>
        Manage cars
      </Typography>
      <Typography color="text.secondary" sx={{ mb: 2 }}>
        Create, update, or retire vehicles from the fleet.
      </Typography>
      <ErrorAlert message={error} />
      {success && (
        <Card variant="outlined" sx={{ mb: 2, borderColor: 'success.main' }}>
          <CardContent>
            <Typography color="success.main">{success}</Typography>
          </CardContent>
        </Card>
      )}
      <Card variant="outlined" sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Add car
          </Typography>
          <Stack
            component="form"
            spacing={2}
            onSubmit={createForm.handleSubmit(handleCreate)}
            direction={{ xs: 'column', md: 'row' }}
            flexWrap="wrap"
          >
            <TextField
              label="Make"
              {...createForm.register('make', { required: 'Required' })}
              error={Boolean(createForm.formState.errors.make)}
              helperText={createForm.formState.errors.make?.message}
            />
            <TextField
              label="Model"
              {...createForm.register('model', { required: 'Required' })}
              error={Boolean(createForm.formState.errors.model)}
              helperText={createForm.formState.errors.model?.message}
            />
            <TextField label="Year" type="number" {...createForm.register('year', { valueAsNumber: true })} />
            <TextField label="VIN" {...createForm.register('vin', { required: 'Required' })} />
            <TextField label="Type" {...createForm.register('type', { required: 'Required' })} />
            <TextField
              label="Base price per day"
              type="number"
              {...createForm.register('base_price_per_day', { required: 'Required' })}
            />
            <TextField label="Status" {...createForm.register('status')} />
            <TextField label="Mileage" type="number" {...createForm.register('mileage', { valueAsNumber: true })} />
            <TextField
              label="Last service at"
              type="date"
              InputLabelProps={{ shrink: true }}
              {...createForm.register('last_service_at')}
            />
            <Button type="submit" variant="contained">
              Add car
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {loading ? (
        <LoadingState label="Loading cars..." />
      ) : (
        <Grid container spacing={2}>
          {cars.map((car) => (
            <Grid item xs={12} md={6} key={car.id}>
              <Card variant="outlined">
                <CardContent>
                  <Typography variant="h6">
                    {car.make} {car.model} ({car.year})
                  </Typography>
                  <Typography color="text.secondary">VIN: {car.vin}</Typography>
                  <Typography color="text.secondary">Type: {car.type}</Typography>
                  <Typography color="text.secondary">Status: {car.status}</Typography>
                  <Typography color="text.secondary">
                    Rate: ${car.base_price_per_day} / day
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small" onClick={() => openEdit(car)}>
                    Edit
                  </Button>
                  <Button size="small" color="error" onClick={() => handleDelete(car.id)}>
                    Delete
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog open={Boolean(editingCar)} onClose={() => setEditingCar(null)} maxWidth="md" fullWidth>
        <DialogTitle>Edit car</DialogTitle>
        <DialogContent>
          <Stack component="form" spacing={2} sx={{ mt: 1 }}>
            <TextField
              label="Make"
              {...editForm.register('make', { required: 'Required' })}
              error={Boolean(editForm.formState.errors.make)}
              helperText={editForm.formState.errors.make?.message}
            />
            <TextField
              label="Model"
              {...editForm.register('model', { required: 'Required' })}
              error={Boolean(editForm.formState.errors.model)}
              helperText={editForm.formState.errors.model?.message}
            />
            <TextField label="Year" type="number" {...editForm.register('year', { valueAsNumber: true })} />
            <TextField label="VIN" {...editForm.register('vin', { required: 'Required' })} />
            <TextField label="Type" {...editForm.register('type', { required: 'Required' })} />
            <TextField
              label="Base price per day"
              type="number"
              {...editForm.register('base_price_per_day', { required: 'Required' })}
            />
            <TextField label="Status" {...editForm.register('status')} />
            <TextField label="Mileage" type="number" {...editForm.register('mileage', { valueAsNumber: true })} />
            <TextField
              label="Last service at"
              type="date"
              InputLabelProps={{ shrink: true }}
              {...editForm.register('last_service_at')}
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEditingCar(null)}>Cancel</Button>
          <Button onClick={editForm.handleSubmit(handleEditSubmit)} variant="contained">
            Save
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}

export default ManageCarsPage
