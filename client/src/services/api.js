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

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error Details:", {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      message: error.message,
    });  // Handle specific error cases
  if (error.response?.status === 404) {
    // Not found - let component handle
  } else if (
    error.response?.status === 401 ||
    error.response?.status === 422
  ) {
    // Authentication/validation error - let component handle
  }

    return Promise.reject(error);
  }
);

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
  try {

    const response = await api.get(`/game/${gameId}`);
    return response.data;
  } catch (error) {
    console.error(
      `Failed to get game details for ID ${gameId}:`,
      error.response?.data || error.message
    );
    throw error;
  }
};

// ✅ ADD THIS
export const getActiveGames = async () => {
  const response = await api.get("/game/active");
  return response.data;
};

export default api;
