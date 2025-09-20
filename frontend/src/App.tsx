import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";
import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import CarsPage from "./pages/CarsPage";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import ManagerPage from "./pages/ManagerPage";
import ReportsPage from "./pages/ReportsPage";

const theme = createTheme();

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<CarsPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/manager" element={<ManagerPage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}
