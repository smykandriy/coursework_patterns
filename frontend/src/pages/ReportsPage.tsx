import { useState } from "react";
import { Box, Button, Paper, TextField, Typography } from "@mui/material";
import { useForm } from "react-hook-form";
import client from "../api/client";

interface ReportForm {
  from: string;
  to: string;
}

export default function ReportsPage() {
  const [fleet, setFleet] = useState<any>(null);
  const [financial, setFinancial] = useState<any>(null);
  const { register, handleSubmit } = useForm<ReportForm>({
    defaultValues: {
      from: new Date().toISOString().slice(0, 10),
      to: new Date().toISOString().slice(0, 10)
    }
  });

  const onSubmit = handleSubmit(async values => {
    const [fleetRes, finRes] = await Promise.all([
      client.get("/api/reports/fleet-utilization/", { params: values }),
      client.get("/api/reports/financials/", { params: values })
    ]);
    setFleet(fleetRes.data);
    setFinancial(finRes.data);
  });

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Reports
      </Typography>
      <Box component="form" onSubmit={onSubmit} sx={{ display: "flex", gap: 2, mb: 3 }}>
        <TextField type="date" label="From" InputLabelProps={{ shrink: true }} {...register("from")} />
        <TextField type="date" label="To" InputLabelProps={{ shrink: true }} {...register("to")} />
        <Button type="submit" variant="contained">
          Load
        </Button>
      </Box>
      {fleet && (
        <Typography variant="body1" gutterBottom>
          Fleet utilization: {fleet.utilization_pct}% ({fleet.total_bookings} bookings)
        </Typography>
      )}
      {financial && (
        <Typography variant="body1">
          {`Revenue $${Number(financial.rental_revenue).toFixed(2)} | Fines $${Number(financial.fines_total).toFixed(2)}`}
        </Typography>
      )}
    </Paper>
  );
}
