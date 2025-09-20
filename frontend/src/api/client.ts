import axios from "axios";
import useAuthStore from "../store/useAuthStore";

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000"
});

client.interceptors.request.use(config => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers = {
      ...config.headers,
      Authorization: `Bearer ${token}`
    };
  }
  return config;
});

export default client;
