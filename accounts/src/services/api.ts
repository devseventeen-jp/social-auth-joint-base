import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export const fetchProviders = async () => {
  const res = await axios.get(`${API_BASE}/auth/providers/`);
  return res.data.providers;
};

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  withCredentials: true,
})

export default api
