import React from "react";

const PlayerInfo = ({
  player,
  isActive,
  isCurrentUser = false,
  isWaiting = false,
  isConnected = true,
}) => {
  const getStatusIndicator = () => {
    if (isWaiting) {
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-neon-yellow rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-neon-yellow font-mono uppercase">
            WAITING...
          </span>
        </div>
      );
    }

    if (!isConnected) {
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-neon-pink rounded-full"></div>
          <span className="text-xs font-medium text-neon-pink font-mono uppercase">
            DISCONNECTED
          </span>
        </div>
      );
    }

    if (isActive) {
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-neon-green rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-neon-green font-mono uppercase neon-text">
            YOUR TURN!
          </span>
        </div>
      );
    }

    return (
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 bg-text-muted rounded-full"></div>
        <span className="text-xs font-medium text-text-muted font-mono uppercase">
          WAITING FOR TURN
        </span>
      </div>
    );
  };

  const getCardStyles = () => {
    let baseStyles = "cyber-card p-4 transition-all duration-200";

    if (isCurrentUser) {
      baseStyles += " ring-2 ring-neon-purple/50 bg-neon-purple/5";
    }

    if (isActive && !isWaiting) {
      baseStyles += " shadow-neon border-neon-green/50";
    }

    return baseStyles;
  };

  const getSymbolIcon = (symbol) => {
    if (symbol === "X") return "✕";
    if (symbol === "O") return "◯";
    return "❓";
  };

  const getSymbolColor = (symbol) => {
    if (symbol === "X") return "text-neon-pink";
    if (symbol === "O") return "text-neon-cyan";
    return "text-text-muted";
  };

  return (
    <div className={getCardStyles()}>
      {/* Player Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-full bg-cyber-darker border-2 border-neon-green">
            <span
              className={`text-xl font-bold ${getSymbolColor(
                player.symbol
              )} neon-text`}
            >
              {getSymbolIcon(player.symbol)}
            </span>
          </div>
          <div>
            <h3 className="font-semibold text-neon-green flex items-center gap-2 font-mono neon-text">
              {player.username || "WAITING..."}
              {isCurrentUser && (
                <span className="text-xs bg-neon-purple text-cyber-black px-2 py-1 rounded-full font-bold">
                  YOU
                </span>
              )}
            </h3>
            <p className="text-sm text-neon-cyan font-mono">
              PLAYER {player.symbol || "?"}
            </p>
          </div>
        </div>
      </div>

      {/* Status Indicator */}
      <div className="flex items-center justify-between">
        {getStatusIndicator()}

        {/* Connection Quality Indicator */}
        <div className="flex items-center gap-1">
          <div
            className={`w-1 h-3 rounded-full ${
              isConnected ? "bg-neon-green" : "bg-neon-pink"
            }`}
          ></div>
          <div
            className={`w-1 h-4 rounded-full ${
              isConnected ? "bg-neon-green" : "bg-text-muted"
            }`}
          ></div>
          <div
            className={`w-1 h-5 rounded-full ${
              isConnected ? "bg-neon-green" : "bg-text-muted"
            }`}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default PlayerInfo;
