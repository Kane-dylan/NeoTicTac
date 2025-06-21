import React, { useState, useEffect } from "react";
import { useSocket } from "../context/SocketContext";
import toast from "react-hot-toast";

const PlayAgainManager = ({
  game,
  currentPlayer,
  gameId,
  isGameCompleted,
  canControlGame,
}) => {
  const { socket } = useSocket();
  const [hasRequestedPlayAgain, setHasRequestedPlayAgain] = useState(false);
  const [incomingInvite, setIncomingInvite] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    if (!socket) return;

    // Handle incoming play again invitation
    const handlePlayAgainInvite = (data) => {
      if (data.invitee === currentPlayer && data.inviter !== currentPlayer) {
        setIncomingInvite({
          inviter: data.inviter,
          gameId: data.gameId,
          timestamp: Date.now(),
        });
        toast.success(`${data.inviter} wants to play again!`, {
          duration: 5000,
          icon: "🎮",
        });
      }
    };

    // Handle invitation response
    const handleInviteResponse = (data) => {
      if (data.inviter === currentPlayer) {
        if (data.accepted) {
          toast.success(`${data.invitee} accepted! Starting new game...`, {
            icon: "🎉",
          });
          setHasRequestedPlayAgain(false);
        } else {
          toast.error(`${data.invitee} declined the rematch.`, {
            icon: "❌",
          });
          setHasRequestedPlayAgain(false);
        }
      }
    };

    // Handle game restart success
    const handleGameRestarted = (data) => {
      setHasRequestedPlayAgain(false);
      setIncomingInvite(null);
      setIsProcessing(false);
      toast.success("New game started! 🎮", {
        icon: "🚀",
      });
    };

    // Handle invitation cancelled (e.g., player disconnected)
    const handleInviteCancelled = (data) => {
      if (data.reason === "player_disconnected") {
        setIncomingInvite(null);
        setHasRequestedPlayAgain(false);
        toast.error("Play again invitation cancelled - player disconnected", {
          icon: "🔌",
        });
      }
    };

    socket.on("play_again_invite", handlePlayAgainInvite);
    socket.on("play_again_response", handleInviteResponse);
    socket.on("game_restarted", handleGameRestarted);
    socket.on("play_again_cancelled", handleInviteCancelled);

    return () => {
      socket.off("play_again_invite", handlePlayAgainInvite);
      socket.off("play_again_response", handleInviteResponse);
      socket.off("game_restarted", handleGameRestarted);
      socket.off("play_again_cancelled", handleInviteCancelled);
    };
  }, [socket, currentPlayer]);

  // Reset state when game changes or completes
  useEffect(() => {
    if (!isGameCompleted) {
      setHasRequestedPlayAgain(false);
      setIncomingInvite(null);
    }
  }, [isGameCompleted, gameId]);

  const sendPlayAgainInvite = () => {
    if (!socket || !canControlGame || hasRequestedPlayAgain || isProcessing)
      return;

    const otherPlayer =
      currentPlayer === game.player_x ? game.player_o : game.player_x;

    if (!otherPlayer) {
      toast.error("No opponent to invite!");
      return;
    }

    setHasRequestedPlayAgain(true);
    setIsProcessing(true);

    socket.emit("send_play_again_invite", {
      gameId: gameId,
      inviter: currentPlayer,
      invitee: otherPlayer,
    });

    toast.success(`Play again invitation sent to ${otherPlayer}`, {
      icon: "📤",
    });

    // Auto-cancel if no response in 30 seconds
    setTimeout(() => {
      if (hasRequestedPlayAgain) {
        setHasRequestedPlayAgain(false);
        setIsProcessing(false);
        toast.error("Play again invitation timed out", {
          icon: "⏰",
        });
      }
    }, 30000);
  };

  const respondToInvite = (accepted) => {
    if (!socket || !incomingInvite) return;

    setIsProcessing(true);

    socket.emit("respond_to_play_again", {
      gameId: incomingInvite.gameId,
      inviter: incomingInvite.inviter,
      invitee: currentPlayer,
      accepted: accepted,
    });

    setIncomingInvite(null);

    if (!accepted) {
      setIsProcessing(false);
      toast.success("Invitation declined", {
        icon: "👋",
      });
    }
  };

  const closeInviteModal = () => {
    setIncomingInvite(null);
  };

  if (!isGameCompleted || !canControlGame) {
    return null;
  }

  return (
    <>
      {/* Play Again Button */}
      <button
        className={`text-sm px-4 py-2 rounded-md font-medium transition-all duration-200 ${
          hasRequestedPlayAgain || isProcessing
            ? "bg-gray-600 text-gray-400 cursor-not-allowed"
            : "btn-primary hover:transform hover:scale-105"
        }`}
        onClick={sendPlayAgainInvite}
        disabled={hasRequestedPlayAgain || isProcessing}
        title={
          hasRequestedPlayAgain
            ? "Invitation sent - waiting for response"
            : "Send play again invitation"
        }
      >
        {hasRequestedPlayAgain ? (
          <>
            <div className="inline-block animate-spin rounded-full h-3 w-3 border border-gray-400 border-t-transparent mr-2"></div>
            Invitation Sent...
          </>
        ) : (
          "🔁 Play Again"
        )}
      </button>

      {/* Incoming Invitation Modal */}
      {incomingInvite && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-2xl border-2 border-blue-500">
            <div className="text-center">
              {/* Header */}
              <div className="text-4xl mb-4">🎮</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                Play Again Invitation
              </h3>
              <p className="text-gray-600 mb-6">
                <span className="font-semibold text-blue-600">
                  {incomingInvite.inviter}
                </span>{" "}
                wants to play again!
              </p>

              {/* Action Buttons */}
              <div className="flex gap-3 justify-center">
                <button
                  className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-md font-medium transition-all duration-200 flex items-center gap-2 hover:transform hover:scale-105"
                  onClick={() => respondToInvite(true)}
                  disabled={isProcessing}
                >
                  ✅ Accept
                </button>
                <button
                  className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-md font-medium transition-all duration-200 flex items-center gap-2 hover:transform hover:scale-105"
                  onClick={() => respondToInvite(false)}
                  disabled={isProcessing}
                >
                  ❌ Decline
                </button>
              </div>

              {/* Close button */}
              <button
                className="mt-4 text-gray-500 hover:text-gray-700 text-sm"
                onClick={closeInviteModal}
                disabled={isProcessing}
              >
                Close
              </button>
            </div>

            {isProcessing && (
              <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center rounded-lg">
                <div className="animate-spin rounded-full h-8 w-8 border-4 border-blue-500 border-t-transparent"></div>
              </div>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default PlayAgainManager;
