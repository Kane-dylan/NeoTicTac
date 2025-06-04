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

    } else {
      localStorage.removeItem("token");

    }
    setAuthToken(newToken);
  }, []);

  // Heartbeat system
  const setupHeartbeat = useCallback((socketInstance) => {
    const heartbeatInterval = setInterval(() => {
      if (socketInstance && socketInstance.connected) {
        const start = Date.now();        socketInstance.emit("ping", start, () => {
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

      socket.disconnect();
      setSocket(null);
      setConnected(false);
    }

    const socketUrl = import.meta.env.VITE_SOCKET_URL || "http://localhost:5000";
    console.log('Connecting to socket server:', socketUrl);

    const newSocketInstance = io(
      socketUrl,
      {
        auth: {
          token: authToken || null,
        },
        transports: ["polling", "websocket"],
        forceNew: true,
        reconnection: true,
        reconnectionAttempts: 10,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 20000,
        autoConnect: true,
        // Don't use withCredentials in Socket.IO when CORS is set to '*'
        withCredentials: false,
        extraHeaders: {
          "Access-Control-Allow-Origin": "*"
        }
      }
    );

    newSocketInstance.on("connect", () => {

      setConnected(true);
      setReconnecting(false);
      setConnectionHealth("good");
    });

    newSocketInstance.on("disconnect", (reason) => {

      setConnected(false);
      setConnectionHealth("disconnected");

      if (
        reason === "io server disconnect" ||
        reason === "io client disconnect"
      ) {
        return;
      }
      setReconnecting(true);
    });    newSocketInstance.on("reconnect", () => {
      setReconnecting(false);
      setConnectionHealth("good");
    });    newSocketInstance.on("reconnect_attempt", () => {
      setReconnecting(true);
    });    newSocketInstance.on("reconnect_failed", () => {
      setReconnecting(false);
      setConnectionHealth("disconnected");
    });

    newSocketInstance.on("connect_error", (error) => {
      console.error("Socket connection error:", error.message);
      setConnected(false);
      setConnectionHealth("disconnected");
    });    newSocketInstance.on("connection_confirmed", () => {
      // Connection confirmed
    });

    setSocket(newSocketInstance);

    const cleanupHeartbeat = setupHeartbeat(newSocketInstance);

    return () => {

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
