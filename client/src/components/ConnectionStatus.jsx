import React, { useState, useEffect } from "react";
import { checkServerHealth, testDatabaseConnection } from "../services/api";

const ConnectionStatus = () => {
  const [serverStatus, setServerStatus] = useState("checking");
  const [dbStatus, setDbStatus] = useState("checking");
  const [lastChecked, setLastChecked] = useState(null);
  const [isVisible, setIsVisible] = useState(false);

  const checkConnections = async () => {
    try {
      // Check server health
      const healthResponse = await checkServerHealth();
      setServerStatus(
        healthResponse.status === "healthy" ? "connected" : "error"
      );

      // Check database connection
      try {
        const dbResponse = await testDatabaseConnection();
        setDbStatus(dbResponse.status === "success" ? "connected" : "error");
      } catch (dbError) {
        setDbStatus("error");
      }

      setLastChecked(new Date());
    } catch (error) {
      setServerStatus("error");
      setDbStatus("unknown");
      setLastChecked(new Date());
    }
  };

  useEffect(() => {
    // Initial check
    checkConnections();

    // Check every 30 seconds
    const interval = setInterval(checkConnections, 30000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status) => {
    switch (status) {
      case "connected":
        return "🟢";
      case "error":
        return "🔴";
      case "checking":
        return "🟡";
      default:
        return "⚪";
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case "connected":
        return "Connected";
      case "error":
        return "Error";
      case "checking":
        return "Checking...";
      default:
        return "Unknown";
    }
  };

  if (!isVisible) {
    return (
      <button
        onClick={() => setIsVisible(true)}
        className="fixed bottom-4 right-4 bg-gray-800 text-white p-2 rounded-full shadow-lg hover:bg-gray-700 transition-colors z-50"
        title="Show connection status"
      >
        {getStatusIcon(serverStatus)}
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg p-4 min-w-[250px] z-50">
      <div className="flex justify-between items-center mb-3">
        <h3 className="font-semibold text-gray-900 dark:text-white">
          Connection Status
        </h3>
        <button
          onClick={() => setIsVisible(false)}
          className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
        >
          ✕
        </button>
      </div>

      <div className="space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600 dark:text-gray-300">
            Server:
          </span>
          <div className="flex items-center gap-2">
            <span>{getStatusIcon(serverStatus)}</span>
            <span className="text-sm font-medium">
              {getStatusText(serverStatus)}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600 dark:text-gray-300">
            Database:
          </span>
          <div className="flex items-center gap-2">
            <span>{getStatusIcon(dbStatus)}</span>
            <span className="text-sm font-medium">
              {getStatusText(dbStatus)}
            </span>
          </div>
        </div>

        {lastChecked && (
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
            Last checked: {lastChecked.toLocaleTimeString()}
          </div>
        )}

        <button
          onClick={checkConnections}
          className="w-full mt-3 bg-blue-500 hover:bg-blue-600 text-white text-sm py-1 px-2 rounded transition-colors"
        >
          Refresh
        </button>
      </div>
    </div>
  );
};

export default ConnectionStatus;
