import React from "react";
import Square from "./Square";

const GameBoard = ({
  board,
  onSquareClick,
  winningLine = null,
  disabled = false,
}) => {
  const isWinningSquare = (index) => {
    return winningLine && winningLine.includes(index);
  };
  return (
    <div className="inline-block p-6 cyber-card relative overflow-hidden">
      {/* Pixel Art Cloud Background */}
      <div
        className="absolute inset-0 opacity-5 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/clouds-pixel.png')`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          filter: "brightness(0.3) contrast(1.2)",
        }}
      ></div>

      <div className="relative z-10 grid grid-cols-3 gap-3 md:gap-4">
        {board.map((value, index) => (
          <Square
            key={index}
            value={value}
            onClick={() => onSquareClick(index)}
            isWinning={isWinningSquare(index)}
            disabled={disabled}
          />
        ))}
      </div>
    </div>
  );
};

export default GameBoard;
