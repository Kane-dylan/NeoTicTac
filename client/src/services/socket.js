import { io } from "socket.io-client";

let socket = null;

export const initSocket = (token) => {
  if (socket) {
    socket.disconnect();
  }

  const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || "http://localhost:5000";

  socket = io(SOCKET_URL, {
    auth: {
      token,
    },
    transports: ["websocket", "polling"],
  });

  socket.on("connect", () => {
    console.log("Connected to server with socket ID:", socket.id);
  });

  socket.on("disconnect", () => {
    console.log("Disconnected from server");
  });

  socket.on("connect_error", (error) => {
    console.error("Connection error:", error);
  });

  return socket;
};

export const getSocket = () => {
  if (!socket) {
    throw new Error("Socket is not initialized. Call initSocket first.");
  }
  return socket;
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
    socket = null;
  }
};

export const isSocketConnected = () => {
  return socket && socket.connected;
};

export default {
  initSocket,
  getSocket,
  disconnectSocket,
  isSocketConnected,
};
