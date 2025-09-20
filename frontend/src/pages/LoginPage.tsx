import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { Box, Button, Paper, TextField, Typography } from "@mui/material";
import client from "../api/client";
import useAuthStore from "../store/useAuthStore";

interface LoginForm {
  email: string;
  password: string;
}

export default function LoginPage() {
  const { register, handleSubmit } = useForm<LoginForm>({
    defaultValues: { email: "customer@example.com", password: "customer123" }
  });
  const setToken = useAuthStore(state => state.setToken);
  const navigate = useNavigate();

  const onSubmit = handleSubmit(async values => {
    const response = await client.post("/api/auth/login/", values);
    setToken(response.data.access);
    navigate("/dashboard");
  });

  return (
    <Paper sx={{ p: 4, maxWidth: 400 }}>
      <Typography variant="h5" gutterBottom>
        Login
      </Typography>
      <Box component="form" onSubmit={onSubmit} sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField label="Email" {...register("email", { required: true })} />
        <TextField label="Password" type="password" {...register("password", { required: true })} />
        <Button variant="contained" type="submit">
          Sign in
        </Button>
      </Box>
    </Paper>
  );
}
