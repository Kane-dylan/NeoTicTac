import React from "react";

const PlayerInfo = ({
  player,
  isActive,
  isCurrentUser = false,
  isWaiting = false,
  isConnected = true,
}) => {
  const getStatusColor = () => {
    if (isWaiting) return "bg-yellow-100 border-yellow-300";
    if (isActive) return "bg-green-100 border-green-300";
    return "bg-gray-100 border-gray-300";
  };

  const getSymbolIcon = (symbol) => {
    return symbol === "X" ? "❌" : symbol === "O" ? "⭕" : "❓";
  };

  return (
    <div
      className={`p-4 rounded-lg border-2 transition-all duration-300 ${getStatusColor()} ${
        isCurrentUser ? "ring-2 ring-blue-400 shadow-md" : ""
      } ${!isConnected ? "opacity-75" : ""}`}
    >
      <div className="flex items-center justify-between mb-2">
        <h3 className="font-bold flex items-center gap-2 text-gray-800">
          <span className="text-lg">{getSymbolIcon(player.symbol)}</span>
          {player.username || "Waiting..."}
          {isCurrentUser && (
            <span className="text-xs bg-blue-500 text-white px-2 py-1 rounded-full">
              YOU
            </span>
          )}
        </h3>
        <div className="flex items-center gap-1">
          <div
            className={`w-2 h-2 rounded-full ${
              isConnected ? "bg-green-500" : "bg-red-500"
            }`}
            title={isConnected ? "Connected" : "Disconnected"}
          ></div>
        </div>
      </div>

      <div className="space-y-1">
        <p className="text-sm text-gray-600">
          Symbol: <span className="font-medium">{player.symbol || "?"}</span>
        </p>

        {isWaiting && (
          <p className="text-xs text-yellow-600 font-medium flex items-center gap-1">
            <span className="animate-pulse">⏳</span>
            Waiting for player...
          </p>
        )}

        {isActive && !isWaiting && (
          <p className="text-xs text-green-600 font-medium flex items-center gap-1">
            <span className="animate-bounce">🎯</span>
            Your turn!
          </p>
        )}

        {!isActive && !isWaiting && player.username && (
          <p className="text-xs text-gray-500">Waiting for turn...</p>
        )}
      </div>
    </div>
  );
};

export default PlayerInfo;
