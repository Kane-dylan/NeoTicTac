import React from "react";

const PlayerInfo = ({ player, isActive }) => {
  return (
    <div className={`p-4 rounded ${isActive ? "bg-green-100" : "bg-gray-100"}`}>
      <h3 className="font-bold">{player.username}</h3>
      <p>Symbol: {player.symbol}</p>
    </div>
  );
};

export default PlayerInfo;
