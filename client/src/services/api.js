import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";
console.log('Using API URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // Add timeout to prevent hanging requests
  timeout: 15000,
  // Enable credentials for cross-origin requests
  withCredentials: false
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
    });

    // Handle specific error cases
    if (error.response?.status === 404) {
      // Not found - let component handle
    } else if (
      error.response?.status === 401 ||
      error.response?.status === 422
    ) {
      // Authentication/validation error - let component handle
    } else if (error.response?.status === 500) {
      // Server error - could be database connection issue
      console.error(
        "Server error detected - possibly database connection issue"
      );
    } else if (
      error.code === "NETWORK_ERROR" ||
      error.code === "ECONNREFUSED"
    ) {
      // Network connectivity issues
      console.error("Network connectivity issue detected");
    }

    return Promise.reject(error);
  }
);

// 🔐 Auth API
export const registerUser = async (userData) => {
  try {
    console.log('Registering user:', { ...userData, password: '[REDACTED]' });
    const response = await api.post("/auth/register", userData);
    return response.data;
  } catch (error) {
    console.error('Registration error:', error.response?.data || error.message);
    throw error;
  }
};

export const loginUser = async (credentials) => {
  try {
    console.log('Logging in user:', { ...credentials, password: '[REDACTED]' });
    const response = await api.post("/auth/login", credentials);
    return response.data;
  } catch (error) {
    console.error('Login error:', error.response?.data || error.message);
    throw error;
  }
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

// 🔍 Health Check API
export const checkServerHealth = async () => {
  try {
    const response = await api.get("/health");
    return response.data;
  } catch (error) {
    console.error("Health check failed:", error);
    throw error;
  }
};

export const testDatabaseConnection = async () => {
  try {
    const response = await api.get("/api/test-db");
    return response.data;
  } catch (error) {
    console.error("Database test failed:", error);
    throw error;
  }
};

export default api;
