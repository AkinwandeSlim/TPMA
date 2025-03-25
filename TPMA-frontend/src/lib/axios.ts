import axios, { AxiosInstance, AxiosRequestConfig } from "axios";
// import { config } from "./config";
import { getAccessToken, refreshTokens, logout } from "./auth";

const api: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api",
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const newToken = await refreshTokens();
      if (newToken) {
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } else {
        logout();
        window.location.href = "/signin";
      }
    }
    return Promise.reject(error);
  },
);

export default api;