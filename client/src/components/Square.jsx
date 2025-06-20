import React from "react";

const Square = ({ value, onClick, isWinning = false, disabled = false }) => {
  const getSquareContent = () => {
    if (value === "X") {
      return (
        <span className="text-4xl font-bold text-neon-pink select-none neon-text">
          ✕
        </span>
      );
    }
    if (value === "O") {
      return (
        <span className="text-4xl font-bold text-neon-cyan select-none neon-text">
          ◯
        </span>
      );
    }
    return null;
  };

  const getSquareStyles = () => {
    let baseStyles =
      "w-20 h-20 md:w-24 md:h-24 lg:w-28 lg:h-28 flex items-center justify-center transition-all duration-200 ease-in-out border-2 font-bold font-mono";

    if (isWinning) {
      baseStyles +=
        " bg-neon-green/20 border-neon-green animate-neon-pulse shadow-neon";
    } else if (value) {
      baseStyles += " bg-cyber-darker border-neon-green/60";
    } else if (disabled) {
      baseStyles +=
        " bg-cyber-black border-neon-green/20 cursor-not-allowed opacity-50";
    } else {
      baseStyles +=
        " bg-cyber-dark border-neon-green/40 hover:bg-cyber-darker hover:border-neon-green hover:shadow-neon-sm cursor-pointer transform hover:scale-105";
    }

    return baseStyles;
  };

  return (
    <button
      className={getSquareStyles()}
      onClick={onClick}
      disabled={disabled || value}
      style={{ borderRadius: "8px" }}
      aria-label={value ? `Square filled with ${value}` : "Empty square"}
    >
      {getSquareContent()}
    </button>
  );
};

export default Square;
