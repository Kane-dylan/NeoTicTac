import React from "react";

const PlayAgainButton = ({
  onClick,
  disabled = false,
  pending = false,
  visible = true,
}) => {
  if (!visible) return null;

  return (
    <button
      onClick={onClick}
      disabled={disabled || pending}
      className={`
        bg-neon-green/20 hover:bg-neon-green/30 border-2 border-neon-green text-neon-green 
        py-2 px-4 rounded font-mono font-bold uppercase tracking-wider text-sm
        transition-all duration-300 hover:transform hover:scale-105 
        hover:shadow-lg hover:shadow-neon-green/25
        disabled:opacity-50 disabled:cursor-not-allowed 
        disabled:hover:transform-none disabled:hover:shadow-none
        ${pending ? "animate-pulse" : ""}
      `}
      title={pending ? "Waiting for response..." : "Request to play again"}
    >
      {pending ? (
        <span className="flex items-center gap-2">
          <div className="animate-spin rounded-full h-3 w-3 border-2 border-current border-t-transparent"></div>
          WAITING...
        </span>
      ) : (
        "🔁 PLAY AGAIN"
      )}
    </button>
  );
};

export default PlayAgainButton;
