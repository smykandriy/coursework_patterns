import { AppBar, Box, Button, Container, Toolbar, Typography } from "@mui/material";
import { Outlet, useNavigate } from "react-router-dom";
import useAuthStore from "../store/useAuthStore";

const links = [
  { label: "Cars", path: "/" },
  { label: "Dashboard", path: "/dashboard" },
  { label: "Manager", path: "/manager" },
  { label: "Reports", path: "/reports" }
];

export default function Layout() {
  const navigate = useNavigate();
  const { token, logout } = useAuthStore();

  return (
    <Box sx={{ minHeight: "100vh" }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Car Rental
          </Typography>
          {links.map(link => (
            <Button key={link.path} color="inherit" onClick={() => navigate(link.path)}>
              {link.label}
            </Button>
          ))}
          {token ? (
            <Button color="inherit" onClick={logout}>
              Logout
            </Button>
          ) : (
            <Button color="inherit" onClick={() => navigate("/login")}>
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>
      <Container sx={{ py: 4 }}>
        <Outlet />
      </Container>
    </Box>
  );
}
