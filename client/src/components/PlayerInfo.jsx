import React from "react";

const PlayerInfo = ({ player, isActive, isCurrentUser = false }) => {
  return (
    <div
      className={`p-4 rounded border-2 ${
        isActive
          ? "bg-green-100 border-green-300"
          : "bg-gray-100 border-gray-300"
      } ${isCurrentUser ? "ring-2 ring-blue-400" : ""}`}
    >
      <h3 className="font-bold flex items-center gap-2">
        {player.username}
        {isCurrentUser && (
          <span className="text-xs bg-blue-500 text-white px-2 py-1 rounded">
            YOU
          </span>
        )}
      </h3>
      <p className="text-sm">Symbol: {player.symbol}</p>
      {isActive && (
        <p className="text-xs text-green-600 font-medium">Current Turn</p>
      )}
    </div>
  );
};

export default PlayerInfo;
