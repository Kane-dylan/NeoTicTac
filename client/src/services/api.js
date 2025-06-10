import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000/api";
console.log("Using API URL:", API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // Increase timeout for better reliability
  timeout: 15000,
  // Enable credentials for cross-origin requests
  withCredentials: false,
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
    if (error.response?.status === 401) {
      // Authentication error - token might be expired
      console.error("Authentication error - token might be expired");
      // Don't automatically redirect here, let components handle it
    } else if (error.response?.status === 404) {
      // Not found - let component handle
    } else if (error.response?.status === 422) {
      // Validation error - let component handle
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
    console.log("Registering user:", { ...userData, password: "[REDACTED]" });
    const response = await api.post("/auth/register", userData);
    return response.data;
  } catch (error) {
    console.error("Registration error:", error.response?.data || error.message);
    throw error;
  }
};

export const loginUser = async (credentials) => {
  try {
    console.log("Logging in user:", { ...credentials, password: "[REDACTED]" });
    const response = await api.post("/auth/login", credentials);
    return response.data;
  } catch (error) {
    console.error("Login error:", error.response?.data || error.message);
    throw error;
  }
};

// 🎮 Game API
export const createGame = async () => {
  const response = await api.post("/game/create");
  return response.data;
};

// Cache for game details to prevent rapid API calls
const gameDetailsCache = new Map();
const CACHE_DURATION = 2000; // 2 seconds

export const getGameDetails = async (gameId, retries = 2) => {
  // Check cache first
  const cacheKey = `game_${gameId}`;
  const cached = gameDetailsCache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
    console.log(`Using cached game data for game ${gameId}`);
    return cached.data;
  }

  try {
    console.log(
      `Fetching game details for ID ${gameId}, attempt ${3 - retries}/3`
    );
    const response = await api.get(`/game/${gameId}`);

    // Cache the successful response
    gameDetailsCache.set(cacheKey, {
      data: response.data,
      timestamp: Date.now(),
    });

    return response.data;
  } catch (error) {
    console.error(
      `Failed to get game details for ID ${gameId}:`,
      error.response?.data || error.message
    );

    // Retry on timeout or network errors
    if (
      retries > 0 &&
      (error.code === "ECONNABORTED" || error.code === "NETWORK_ERROR")
    ) {
      const delay = (3 - retries) * 1000; // Exponential backoff: 1s, 2s
      console.log(
        `Retrying getGameDetails for game ${gameId}, ${retries} attempts left... (waiting ${delay}ms)`
      );
      await new Promise((resolve) => setTimeout(resolve, delay));
      return getGameDetails(gameId, retries - 1);
    }

    throw error;
  }
};

// ✅ Get all games (active, completed, waiting)
export const getAllGames = async (retries = 2) => {
  try {
    const response = await api.get("/game/active");
    return response.data;
  } catch (error) {
    if (
      retries > 0 &&
      (error.code === "ECONNABORTED" || error.code === "NETWORK_ERROR")
    ) {
      const delay = (3 - retries) * 1000; // Exponential backoff: 1s, 2s
      console.log(
        `Retrying getAllGames, ${retries} attempts left... (waiting ${delay}ms)`
      );
      await new Promise((resolve) => setTimeout(resolve, delay));
      return getAllGames(retries - 1);
    }
    throw error;
  }
};

// Keep the old function name for backward compatibility
export const getActiveGames = getAllGames;

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

export const testConnection = async () => {
  try {
    // Try a simple request with short timeout using the existing api instance
    const response = await api.get("/game/active", {
      timeout: 3000,
    });
    return { connected: true, status: response.status };
  } catch (error) {
    console.error("Connection test failed:", error);
    return {
      connected: false,
      error:
        error.code === "ECONNABORTED"
          ? "Timeout"
          : error.code === "NETWORK_ERROR"
          ? "Network Error"
          : error.response?.status || "Unknown Error",
    };
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
