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
    <div className="inline-block p-6 card">
      <div className="grid grid-cols-3 gap-3 md:gap-4">
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
