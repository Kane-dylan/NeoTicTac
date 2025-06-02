import React, {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
  useRef,
} from "react";
import { io } from "socket.io-client";

const SocketContext = createContext();

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [reconnecting, setReconnecting] = useState(false);
  const [connectionHealth, setConnectionHealth] = useState("good");
  const [authToken, setAuthToken] = useState(() =>
    localStorage.getItem("token")
  );

  const connectionAttemptRef = useRef(false);
  const cleanupTimeoutRef = useRef(null);

  const updateAuthToken = useCallback((newToken) => {
    if (newToken) {
      localStorage.setItem("token", newToken);
      console.log("Token set in localStorage by updateAuthToken");
    } else {
      localStorage.removeItem("token");
      console.log("Token removed from localStorage by updateAuthToken");
    }
    setAuthToken(newToken);
  }, []);

  // Heartbeat system
  const setupHeartbeat = useCallback((socketInstance) => {
    const heartbeatInterval = setInterval(() => {
      if (socketInstance && socketInstance.connected) {
        const start = Date.now();
        socketInstance.emit("ping", start, (response) => {
          const latency = Date.now() - start;
          if (latency < 100) {
            setConnectionHealth("good");
          } else if (latency < 300) {
            setConnectionHealth("fair");
          } else {
            setConnectionHealth("poor");
          }
        });
      }
    }, 5000); // Check every 5 seconds

    return () => clearInterval(heartbeatInterval);
  }, []);

  useEffect(() => {
    // Prevent multiple connection attempts
    if (connectionAttemptRef.current) {
      return;
    }
    connectionAttemptRef.current = true;

    // Clear any pending cleanup
    if (cleanupTimeoutRef.current) {
      clearTimeout(cleanupTimeoutRef.current);
    }

    // Disconnect existing socket
    if (socket) {
      console.log("Disconnecting existing socket");
      socket.disconnect();
      setSocket(null);
      setConnected(false);
    }

    console.log("Creating new socket connection");
    const newSocketInstance = io(
      import.meta.env.VITE_SOCKET_URL || "http://localhost:5000",
      {
        auth: {
          token: authToken || null,
        },
        transports: ["websocket", "polling"],
        forceNew: true,
        reconnection: true,
        reconnectionAttempts: 3,
        reconnectionDelay: 2000,
        timeout: 10000,
        autoConnect: true,
      }
    );

    newSocketInstance.on("connect", () => {
      console.log(
        "Socket connected successfully with ID:",
        newSocketInstance.id
      );
      setConnected(true);
      setReconnecting(false);
      setConnectionHealth("good");
    });

    newSocketInstance.on("disconnect", (reason) => {
      console.log("Socket disconnected:", reason);
      setConnected(false);
      setConnectionHealth("disconnected");

      if (
        reason === "io server disconnect" ||
        reason === "io client disconnect"
      ) {
        return;
      }
      setReconnecting(true);
    });

    newSocketInstance.on("reconnect", (attemptNumber) => {
      console.log("Socket reconnected after", attemptNumber, "attempts");
      setReconnecting(false);
      setConnectionHealth("good");
    });

    newSocketInstance.on("reconnect_attempt", (attemptNumber) => {
      console.log("Reconnection attempt", attemptNumber);
      setReconnecting(true);
    });

    newSocketInstance.on("reconnect_failed", () => {
      console.log("Failed to reconnect to server");
      setReconnecting(false);
      setConnectionHealth("disconnected");
    });

    newSocketInstance.on("connect_error", (error) => {
      console.error("Socket connection error:", error.message);
      setConnected(false);
      setConnectionHealth("disconnected");
    });

    newSocketInstance.on("connection_confirmed", (data) => {
      console.log("Connection confirmed for user:", data.username);
    });

    setSocket(newSocketInstance);

    const cleanupHeartbeat = setupHeartbeat(newSocketInstance);

    return () => {
      console.log("Cleaning up socket connection");
      connectionAttemptRef.current = false;
      cleanupHeartbeat();

      // Delay the disconnect to prevent rapid reconnections
      cleanupTimeoutRef.current = setTimeout(() => {
        if (newSocketInstance && newSocketInstance.connected) {
          newSocketInstance.disconnect();
        }
      }, 100);
    };
  }, [authToken, setupHeartbeat]);

  return (
    <SocketContext.Provider
      value={{
        socket,
        connected,
        reconnecting,
        connectionHealth,
        updateAuthToken,
      }}
    >
      {children}
    </SocketContext.Provider>
  );
};
