import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("username");
    }
    return Promise.reject(error);
  }
);

// Auth API
export const registerUser = async (userData) => {
  const response = await api.post("/auth/register", userData);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await api.post("/auth/login", credentials);
  return response.data;
};

// Game API
export const createGame = async () => {
  const response = await api.post("/game/create");
  return response.data;
};

export const getGameDetails = async (gameId) => {
  const response = await api.get(`/game/${gameId}`);
  return response.data;
};

export const getAllGames = async () => {
  const response = await api.get("/game/active");
  return response.data;
};
