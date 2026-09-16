import axios from "axios";

const configuredBase = import.meta.env.VITE_API_BASE_URL?.trim();

const api = axios.create({
  baseURL: configuredBase || "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
