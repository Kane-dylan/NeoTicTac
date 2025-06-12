import React from "react";

const Square = ({ value, onClick, isWinning = false, disabled = false }) => {
  const getSquareContent = () => {
    if (value === "X") {
      return (
        <span className="text-4xl font-bold text-accent-error select-none">
          ✕
        </span>
      );
    }
    if (value === "O") {
      return (
        <span className="text-4xl font-bold text-accent-info select-none">
          ◯
        </span>
      );
    }
    return null;
  };

  const getSquareStyles = () => {
    let baseStyles =
      "w-20 h-20 md:w-24 md:h-24 lg:w-28 lg:h-28 flex items-center justify-center transition-all duration-200 ease-in-out border-2 font-bold";

    if (isWinning) {
      baseStyles += " bg-accent-success/20 border-accent-success animate-pulse";
    } else if (value) {
      baseStyles += " bg-background-tertiary border-border-medium";
    } else if (disabled) {
      baseStyles +=
        " bg-background-secondary border-border-light cursor-not-allowed opacity-50";
    } else {
      baseStyles +=
        " bg-background-primary border-border-medium hover:bg-background-tertiary hover:border-primary hover:shadow-md cursor-pointer transform hover:scale-105";
    }

    return baseStyles;
  };

  return (
    <button
      className={getSquareStyles()}
      onClick={onClick}
      disabled={disabled || value}
      style={{ borderRadius: "var(--radius-lg)" }}
      aria-label={value ? `Square filled with ${value}` : "Empty square"}
    >
      {getSquareContent()}
    </button>
  );
};

export default Square;
