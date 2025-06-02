import React from "react";

const Square = ({ value, onClick }) => {
  return (
    <button
      className="w-20 h-20 bg-gray-200 text-4xl font-bold border border-gray-400"
      onClick={onClick}
    >
      {value}
    </button>
  );
};

export default Square;
