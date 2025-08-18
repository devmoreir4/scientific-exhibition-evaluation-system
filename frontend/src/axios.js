import axios from "axios";
import { useAuthStore } from "./stores/auth";

function getBaseURL() {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return "http://localhost:5000/api/v1";
  }

  if (window.location.hostname.match(/^10\.|^192\.168\.|^172\.(1[6-9]|2[0-9]|3[0-1])\./)) {
    return `http://${window.location.hostname}:5000/api/v1`;
  }

  return "http://localhost:5000/api/v1";
}

const api = axios.create({
  baseURL: getBaseURL(),
});

// Interceptor para adicionar token automaticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Interceptor para lidar com erros de autenticação
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token inválido ou expirado
      const auth = useAuthStore();
      auth.logout();
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export default api;
