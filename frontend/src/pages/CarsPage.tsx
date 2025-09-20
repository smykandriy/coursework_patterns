import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CardActions,
  CardContent,
  Grid,
  Typography,
  Button,
  TextField
} from "@mui/material";
import { useForm } from "react-hook-form";
import client from "../api/client";

interface Car {
  id: string;
  make: string;
  model: string;
  year: number;
  type: string;
  base_price_per_day: number;
  status: string;
}

interface QuoteResponse {
  total: number;
  breakdown: { strategy: string; delta: number; reason: string }[];
}

export default function CarsPage() {
  const [cars, setCars] = useState<Car[]>([]);
  const [quote, setQuote] = useState<QuoteResponse | null>(null);
  const { register, handleSubmit } = useForm({
    defaultValues: { start: "", end: "" }
  });

  useEffect(() => {
    client.get("/api/cars", { params: { status: "available" } }).then(res => setCars(res.data.results ?? res.data));
  }, []);

  const onSubmit = handleSubmit(async values => {
    if (!values.start || !values.end) return;
    if (!cars.length) return;
    const response = await client.get<QuoteResponse>("/api/pricing/quote/", {
      params: { car: cars[0].id, start: values.start, end: values.end }
    });
    setQuote(response.data);
  });

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Available Cars
      </Typography>
      <Box component="form" onSubmit={onSubmit} sx={{ mb: 3, display: "flex", gap: 2 }}>
        <TextField type="date" label="Start" InputLabelProps={{ shrink: true }} {...register("start")} />
        <TextField type="date" label="End" InputLabelProps={{ shrink: true }} {...register("end")} />
        <Button variant="contained" type="submit">
          Get Quote for first car
        </Button>
      </Box>
      {quote && (
        <Box sx={{ mb: 3 }}>
          <Typography variant="h6">Quote total: ${quote.total.toFixed(2)}</Typography>
          {quote.breakdown.map(item => (
            <Typography key={item.strategy} variant="body2">
              {item.strategy}: {item.reason} ({item.delta.toFixed(2)})
            </Typography>
          ))}
        </Box>
      )}
      <Grid container spacing={2}>
        {cars.map(car => (
          <Grid item xs={12} md={4} key={car.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">
                  {car.make} {car.model}
                </Typography>
                <Typography variant="body2">Year: {car.year}</Typography>
                <Typography variant="body2">Type: {car.type}</Typography>
                <Typography variant="body2">${car.base_price_per_day} / day</Typography>
              </CardContent>
              <CardActions>
                <Button size="small" disabled>
                  Book
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
