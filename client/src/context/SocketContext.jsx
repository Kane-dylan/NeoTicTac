import React, { createContext, useContext, useEffect, useState } from "react";
import { io } from "socket.io-client";

const SocketContext = createContext();

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children }) => {
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [playerConnections, setPlayerConnections] = useState({});

  useEffect(() => {
    const token = localStorage.getItem("token");
    const socketUrl =
      import.meta.env.VITE_SOCKET_URL || "http://localhost:5000";

    const newSocket = io(socketUrl, {
      auth: { token },
      reconnection: true,
    });

    newSocket.on("connect", () => setConnected(true));
    newSocket.on("disconnect", () => setConnected(false));

    // Track player connections for better status display
    newSocket.on("player_disconnected", (data) => {
      setPlayerConnections((prev) => ({
        ...prev,
        [data.player]: false,
      }));
    });

    newSocket.on("player_joined", (data) => {
      setPlayerConnections((prev) => ({
        ...prev,
        [data.player]: true,
      }));
    });

    setSocket(newSocket);

    return () => newSocket.disconnect();
  }, []);

  return (
    <SocketContext.Provider value={{ socket, connected, playerConnections }}>
      {children}
    </SocketContext.Provider>
  );
};
