import { Box, Card, CardContent, Stack, Typography } from '@mui/material'

const placeholderCars = [
  { id: 1, name: 'Sedan', description: 'Comfort-first option for city trips.' },
  { id: 2, name: 'SUV', description: 'Spacious pick for family travel.' },
  { id: 3, name: 'Electric', description: 'Eco-friendly rides for daily commutes.' },
]

const CarsPage = () => {
  return (
    <Stack spacing={2}>
      <div>
        <Typography variant="h4">Available Cars</Typography>
        <Typography variant="body1" color="text.secondary">
          Final catalog, pricing, and booking actions will be implemented later.
        </Typography>
      </div>
      <Box
        display="grid"
        gap={2}
        gridTemplateColumns="repeat(auto-fit, minmax(240px, 1fr))"
      >
        {placeholderCars.map((car) => (
          <Card key={car.id}>
            <CardContent>
              <Typography variant="h6">{car.name}</Typography>
              <Typography variant="body2" color="text.secondary">
                {car.description}
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Stack>
  )
}

export default CarsPage
