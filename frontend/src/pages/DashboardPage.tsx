import { useEffect, useState } from "react";
import { Box, Card, CardContent, Typography } from "@mui/material";
import client from "../api/client";

interface Booking {
  id: string;
  start_date: string;
  end_date: string;
  status: string;
  invoice?: { amount_total: number } | null;
}

export default function DashboardPage() {
  const [bookings, setBookings] = useState<Booking[]>([]);

  useEffect(() => {
    client.get("/api/bookings/").then(res => setBookings(res.data.results ?? res.data));
  }, []);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        My Bookings
      </Typography>
      {bookings.map(booking => (
        <Card key={booking.id} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="subtitle1">
              {booking.start_date} → {booking.end_date}
            </Typography>
            <Typography variant="body2">Status: {booking.status}</Typography>
            {booking.invoice && (
              <Typography variant="body2">
                Invoice total: ${booking.invoice.amount_total?.toFixed(2)}
              </Typography>
            )}
          </CardContent>
        </Card>
      ))}
    </Box>
  );
}
