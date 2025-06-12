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
          <div className="w-2 h-2 bg-accent-warning rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-accent-warning">
            Waiting...
          </span>
        </div>
      );
    }

    if (!isConnected) {
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-accent-error rounded-full"></div>
          <span className="text-xs font-medium text-accent-error">
            Disconnected
          </span>
        </div>
      );
    }

    if (isActive) {
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-accent-success rounded-full animate-pulse"></div>
          <span className="text-xs font-medium text-accent-success">
            Your turn!
          </span>
        </div>
      );
    }

    return (
      <div className="flex items-center gap-2">
        <div className="w-2 h-2 bg-text-muted rounded-full"></div>
        <span className="text-xs font-medium text-muted">Waiting for turn</span>
      </div>
    );
  };

  const getCardStyles = () => {
    let baseStyles = "card p-4 transition-all duration-200";

    if (isCurrentUser) {
      baseStyles += " ring-2 ring-primary/30 bg-primary/5";
    }

    if (isActive && !isWaiting) {
      baseStyles += " shadow-lg border-accent-success/30";
    }

    return baseStyles;
  };

  const getSymbolIcon = (symbol) => {
    if (symbol === "X") return "✕";
    if (symbol === "O") return "◯";
    return "❓";
  };

  const getSymbolColor = (symbol) => {
    if (symbol === "X") return "text-accent-error";
    if (symbol === "O") return "text-accent-info";
    return "text-text-muted";
  };

  return (
    <div className={getCardStyles()}>
      {/* Player Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-10 h-10 rounded-full bg-background-tertiary border-2 border-border-light">
            <span
              className={`text-xl font-bold ${getSymbolColor(player.symbol)}`}
            >
              {getSymbolIcon(player.symbol)}
            </span>
          </div>
          <div>
            <h3 className="font-semibold text-text-primary flex items-center gap-2">
              {player.username || "Waiting..."}
              {isCurrentUser && (
                <span className="text-xs bg-primary text-text-inverse px-2 py-1 rounded-full font-medium">
                  YOU
                </span>
              )}
            </h3>
            <p className="text-sm text-text-secondary">
              Player {player.symbol || "?"}
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
              isConnected ? "bg-accent-success" : "bg-accent-error"
            }`}
          ></div>
          <div
            className={`w-1 h-4 rounded-full ${
              isConnected ? "bg-accent-success" : "bg-text-muted"
            }`}
          ></div>
          <div
            className={`w-1 h-5 rounded-full ${
              isConnected ? "bg-accent-success" : "bg-text-muted"
            }`}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default PlayerInfo;
