import { useEffect, useState } from "react";
import { Box, Button, Card, CardActions, CardContent, Typography } from "@mui/material";
import client from "../api/client";

interface Booking {
  id: string;
  start_date: string;
  end_date: string;
  status: string;
}

export default function ManagerPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);

  const load = () => client.get("/api/bookings/").then(res => setBookings(res.data.results ?? res.data));

  useEffect(() => {
    load();
  }, []);

  const update = async (id: string, action: string) => {
    await client.post(`/api/bookings/${id}/${action}/`);
    load();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Manager Queue
      </Typography>
      {bookings.map(booking => (
        <Card key={booking.id} sx={{ mb: 2 }}>
          <CardContent>
            <Typography>{booking.start_date} → {booking.end_date}</Typography>
            <Typography>Status: {booking.status}</Typography>
          </CardContent>
          <CardActions>
            <Button disabled={booking.status !== "pending"} onClick={() => update(booking.id, "confirm")}>
              Confirm
            </Button>
            <Button disabled={booking.status !== "confirmed"} onClick={() => update(booking.id, "checkin")}>
              Check-in
            </Button>
            <Button disabled={booking.status !== "active"} onClick={() => update(booking.id, "return_car")}>
              Complete
            </Button>
          </CardActions>
        </Card>
      ))}
    </Box>
  );
}
