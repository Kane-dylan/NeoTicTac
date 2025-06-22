import React from "react";
import Modal from "./Modal";

const RematchModal = ({ isOpen, onAccept, onDecline, requestingPlayer }) => {
  if (!isOpen || !requestingPlayer) return null;

  return (
    <Modal isOpen={isOpen} onClose={onDecline} closeOnOverlayClick={false}>
      <div className="cyber-card rounded-lg p-8 w-full max-w-md mx-4 backdrop-blur-lg">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="text-5xl mb-4 animate-neon-pulse">🎮</div>
          <h3 className="text-2xl font-bold text-neon-green mb-3 neon-text font-mono">
            REMATCH REQUEST
          </h3>
          <p className="text-neon-cyan text-sm font-mono">
            PLAYER CHALLENGE • RESPOND REQUIRED
          </p>
        </div>

        {/* Message */}
        <div className="bg-neon-cyan/10 border-2 border-neon-cyan text-neon-cyan p-4 rounded-lg mb-6">
          <div className="flex items-center gap-2 font-mono">
            <span className="text-lg">🎯</span>
            <span className="text-sm uppercase tracking-wide">
              {requestingPlayer} wants to play again!
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button
            onClick={onAccept}
            className="flex-1 bg-neon-green/20 hover:bg-neon-green/30 border-2 border-neon-green text-neon-green py-3 px-4 rounded font-mono font-bold uppercase tracking-wider transition-all duration-300 hover:transform hover:scale-105 hover:shadow-lg hover:shadow-neon-green/25"
          >
            ✅ Accept
          </button>
          <button
            onClick={onDecline}
            className="flex-1 bg-neon-pink/20 hover:bg-neon-pink/30 border-2 border-neon-pink text-neon-pink py-3 px-4 rounded font-mono font-bold uppercase tracking-wider transition-all duration-300 hover:transform hover:scale-105 hover:shadow-lg hover:shadow-neon-pink/25"
          >
            ❌ Decline
          </button>
        </div>

        {/* Footer */}
        <div className="mt-6 text-center">
          <div className="terminal-window p-3 rounded bg-cyber-black">
            <p className="text-xs text-neon-green font-mono">
              REMATCH_PROTOCOL v1.0.0 • WAITING_FOR_RESPONSE
            </p>
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default RematchModal;
