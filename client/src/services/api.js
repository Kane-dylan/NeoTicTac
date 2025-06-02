import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 🔐 Auth API
export const registerUser = async (userData) => {
  const response = await api.post("/auth/register", userData);
  return response.data;
};

export const loginUser = async (credentials) => {
  const response = await api.post("/auth/login", credentials);
  return response.data;
};

// 🎮 Game API
export const createGame = async () => {
  const response = await api.post("/game/create");
  return response.data;
};

export const getGameDetails = async (gameId) => {
  const response = await api.get(`/game/${gameId}`);
  return response.data;
};

// ✅ ADD THIS
export const getActiveGames = async () => {
  const response = await api.get("/game/active");
  return response.data;
};

export default api;
