import axios from "axios";
import { clearTokens, getAccessToken, getRefreshToken, setTokens } from "./auth";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const refresh = getRefreshToken();

    if (error.response?.status === 401 && refresh && !original._retry) {
      original._retry = true;

      try {
        const res = await axios.post(`${API_BASE_URL}/token/refresh/`, {
          refresh,
        });
        setTokens(res.data.access, refresh);
        original.headers.Authorization = `Bearer ${res.data.access}`;
        return api(original);
      } catch (refreshError) {
        clearTokens();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);
