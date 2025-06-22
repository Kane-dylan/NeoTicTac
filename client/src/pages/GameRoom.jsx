import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { useSocket } from "../context/SocketContext";
import { getGameDetails } from "../services/api";
import GameBoard from "../components/GameBoard";
import PlayerInfo from "../components/PlayerInfo";
import ChatBox from "../components/ChatBox";
import PlayAgainButton from "../components/PlayAgainButton";
import RematchModal from "../components/RematchModal";

const GameRoom = () => {
  const { id: gameId } = useParams();
  const { socket, playerConnections } = useSocket();
  const navigate = useNavigate();
  const [game, setGame] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Rematch-related state
  const [rematchRequestPending, setRematchRequestPending] = useState(false);
  const [showRematchModal, setShowRematchModal] = useState(false);
  const [rematchRequestingPlayer, setRematchRequestingPlayer] = useState(null);
  const [pendingRematchRequests, setPendingRematchRequests] = useState(
    new Set()
  );
  const fetchGameDetails = useCallback(async () => {
    if (!gameId) return;
    try {
      const gameData = await getGameDetails(gameId);
      setGame(gameData);
      setError("");
    } catch {
      setError("Failed to load game");
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  useEffect(() => {
    if (!gameId) {
      navigate("/lobby");
      return;
    }

    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    if (!token || !username) {
      navigate("/");
      return;
    }

    setCurrentPlayer(username);
    fetchGameDetails();

    // Socket setup
    if (socket) {
      socket.emit("join_room", { room: gameId, player: username });

      // Game state updates
      socket.on("game_state_update", (data) => {
        if (data?.game) setGame(data.game);
      });

      socket.on("move_made", (data) => {
        if (data?.game) setGame(data.game);
      });

      // Chat messages
      socket.on("receive_message", (message) => {
        setMessages((prev) => [...prev, message]);
      }); // Game events
      socket.on("player_joined", () => fetchGameDetails());
      socket.on("game_over", () => fetchGameDetails());
      // Rematch event handlers
      socket.on("rematch_requested", (data) => {
        const { requesting_player } = data;
        if (requesting_player !== currentPlayer) {
          setRematchRequestingPlayer(requesting_player);
          setShowRematchModal(true);
          toast(`${requesting_player} wants to play again!`, {
            icon: "🎮",
            duration: 6000,
          });
        }
      });

      socket.on("rematch_accepted", (data) => {
        setRematchRequestPending(false);
        setPendingRematchRequests(new Set());
        setShowRematchModal(false);
        setRematchRequestingPlayer(null);
        toast.success("New game started!", {
          icon: "🚀",
          duration: 3000,
        });
        fetchGameDetails();
      });

      socket.on("rematch_declined", (data) => {
        const { declining_player } = data;
        setRematchRequestPending(false);
        setPendingRematchRequests(new Set());
        if (declining_player !== currentPlayer) {
          toast.error(`${declining_player} declined the rematch`, {
            icon: "❌",
            duration: 4000,
          });
        }
      });

      socket.on("player_disconnected", (data) => {
        const { player } = data;
        // Reset rematch state if the disconnected player was involved
        if (
          player === rematchRequestingPlayer ||
          pendingRematchRequests.has(player)
        ) {
          setRematchRequestPending(false);
          setPendingRematchRequests(new Set());
          setShowRematchModal(false);
          setRematchRequestingPlayer(null);
          toast.error(`${player} disconnected`, {
            icon: "🔌",
            duration: 4000,
          });
        }
      });
    }
    return () => {
      if (socket) {
        socket.emit("leave_room", { room: gameId, player: username });
        socket.off("game_state_update");
        socket.off("move_made");
        socket.off("receive_message");
        socket.off("player_joined");
        socket.off("game_over");
        socket.off("rematch_requested");
        socket.off("rematch_accepted");
        socket.off("rematch_declined");
        socket.off("player_disconnected");
      }
    };
  }, [socket, gameId, navigate, fetchGameDetails]);

  const handleSquareClick = (index) => {
    if (!game || !socket || !currentPlayer) return;

    // Basic validations
    if (game.board[index] !== "" || game.winner || game.is_draw) return;
    if (!game.player_o) {
      setError("Waiting for another player to join!");
      return;
    }

    // Check if it's player's turn
    const isPlayerTurn =
      (game.current_turn === "X" && currentPlayer === game.player_x) ||
      (game.current_turn === "O" && currentPlayer === game.player_o);

    if (!isPlayerTurn) {
      setError("It's not your turn!");
      setTimeout(() => setError(""), 2000);
      return;
    }

    // Make the move
    socket.emit("make_move", {
      room: gameId,
      index: index,
      symbol: game.current_turn,
      player: currentPlayer,
    });
  };

  const sendMessage = (text) => {
    if (socket && currentPlayer) {
      socket.emit("send_message", {
        room: gameId,
        sender: currentPlayer,
        text: text,        timestamp: Date.now(),
      });
    }
  };
  const requestRestart = () => {
    if (socket && currentPlayer) {
      socket.emit("request_game_restart", {
        room: gameId,
        player: currentPlayer,
      });
    }
  };

  // Rematch handler functions
  const handlePlayAgain = () => {
    if (!socket || !currentPlayer || !game) return;

    // Prevent duplicate requests
    if (rematchRequestPending) return;

    const otherPlayer =
      currentPlayer === game.player_x ? game.player_o : game.player_x;

    // Check for simultaneous requests
    if (pendingRematchRequests.has(otherPlayer)) {
      // Other player already requested, accept it
      handleAcceptRematch();
      return;
    }

    setRematchRequestPending(true);
    setPendingRematchRequests((prev) => new Set([...prev, currentPlayer]));

    socket.emit("rematch_request", {
      room: gameId,
      requesting_player: currentPlayer,
      target_player: otherPlayer,
    });

    toast("Rematch request sent!", {
      icon: "📤",
      duration: 3000,
    });
  };

  const handleAcceptRematch = () => {
    if (!socket || !currentPlayer) return;

    socket.emit("rematch_accept", {
      room: gameId,
      accepting_player: currentPlayer,
      requesting_player: rematchRequestingPlayer,
    });

    setShowRematchModal(false);
    setRematchRequestingPlayer(null);
  };

  const handleDeclineRematch = () => {
    if (!socket || !currentPlayer) return;

    socket.emit("rematch_decline", {
      room: gameId,
      declining_player: currentPlayer,
      requesting_player: rematchRequestingPlayer,
    });

    setShowRematchModal(false);
    setRematchRequestingPlayer(null);
  };
  const leaveGame = () => navigate("/lobby");

  const isCurrentPlayerTurn = () => {
    if (!game || !game.player_o) return false;
    const playerRole =
      currentPlayer === game.player_x
        ? "X"
        : currentPlayer === game.player_o
        ? "O"
        : "spectator";
    return playerRole !== "spectator" && game.current_turn === playerRole;
  };

  // Enhanced control functions
  const reloadGameState = async () => {
    setLoading(true);
    try {
      await fetchGameDetails();
      if (socket && currentPlayer) {
        socket.emit("join_room", { room: gameId, player: currentPlayer });
      }
    } catch (error) {
      setError("Failed to reload game state");
    } finally {
      setLoading(false);
    }
  };

  const deleteGame = () => {
    if (socket && currentPlayer) {
      const confirmDelete = window.confirm(
        "Are you sure you want to delete this game? This action cannot be undone."
      );
      if (confirmDelete) {
        socket.emit("delete_game_from_lobby", {
          game_id: gameId,
          player: currentPlayer,
        });
      }
    }
  };

  const isGameCompleted = () => {
    return game && (game.winner || game.is_draw);
  };
  const canControlGame = () => {
    return currentPlayer === game.player_x || currentPlayer === game.player_o;
  };

  const canRequestRematch = () => {
    return (
      game &&
      (game.winner || game.is_draw) &&
      game.player_o &&
      canControlGame() &&
      !rematchRequestPending &&
      !showRematchModal
    );
  };
  if (loading) {
    return (
      <div className="min-h-screen bg-background-secondary flex items-center justify-center">
        <div className="card p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mx-auto mb-4"></div>
          <p className="text-text-secondary">Loading game...</p>
        </div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="min-h-screen bg-background-secondary flex items-center justify-center">
        <div className="card p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="text-6xl mb-4">🎮</div>
            <h2 className="text-2xl font-bold text-text-primary mb-4">
              Game Not Found
            </h2>
            <p className="text-text-secondary mb-6">
              The game you're looking for doesn't exist or has been deleted.
            </p>
            <button
              className="btn-primary w-full"
              onClick={() => navigate("/lobby")}
            >
              🏠 Back to Lobby
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background-secondary">
      <div className="container mx-auto px-4 py-6">
        {/* Header Section */}
        <div className="card p-6 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-text-primary mb-2">
                🎮 Game Room
              </h1>
              <p className="text-text-secondary">
                Game ID: <span className="font-mono font-medium">{gameId}</span>
              </p>
            </div>

            {/* Control Buttons */}
            <div className="flex flex-wrap gap-2">
              {" "}
              <button
                className="btn-secondary text-sm px-4 py-2"
                onClick={reloadGameState}
                disabled={loading}                title="Refresh game state"
              >
                🔄 Reload
              </button>
              {canControlGame() && isGameCompleted() && (
                <PlayAgainButton
                  onClick={handlePlayAgain}
                  disabled={!canRequestRematch()}
                  pending={rematchRequestPending}
                  visible={canRequestRematch() || rematchRequestPending}
                />
              )}

              {canControlGame() && isGameCompleted() && (
                <button
                  className="bg-accent-error hover:bg-accent-error/90 text-text-inverse text-sm px-4 py-2 rounded-md font-medium transition-all duration-200"
                  onClick={deleteGame}
                  title="Delete this game"
                >
                  🗑️ Delete Game
                </button>
              )}

              <button
                className="bg-text-muted hover:bg-text-secondary text-text-inverse text-sm px-4 py-2 rounded-md font-medium transition-all duration-200"
                onClick={leaveGame}
                title="Leave game and return to lobby"
              >
                🚪 Leave
              </button>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-accent-error/10 border border-accent-error/20 text-accent-error p-4 rounded-lg mb-6">
            <div className="flex items-center gap-2">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          </div>
        )}

        {/* Game Result Banner */}
        {isGameCompleted() && (
          <div className="card p-6 mb-6 bg-accent-success/5 border-accent-success/20">
            <div className="text-center">
              <div className="text-4xl mb-3">{game.is_draw ? "🤝" : "🎉"}</div>
              <h2 className="text-2xl font-bold text-text-primary mb-4">
                {game.is_draw
                  ? "Game ended in a draw!"
                  : `${
                      game.winner === "X" ? game.player_x : game.player_o
                    } wins!`}
              </h2>
              <p className="text-text-secondary mb-4">
                {game.is_draw
                  ? "Great game! Both players played well."
                  : `Player ${game.winner} achieved victory!`}
              </p>
            </div>
          </div>
        )}

        {/* Main Game Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Players Section */}
          <div className="lg:col-span-1">
            <div className="card p-6">
              <h2 className="text-xl font-semibold text-text-primary mb-4 flex items-center gap-2">
                👥 Players
              </h2>
              <div className="space-y-4">
                {" "}
                <PlayerInfo
                  player={{
                    username: game.player_x || "Player X",
                    symbol: "X",
                  }}
                  isActive={
                    game.current_turn === "X" &&
                    game.player_o &&
                    !game.winner &&
                    !game.is_draw
                  }
                  isCurrentUser={currentPlayer === game.player_x}
                  isWaiting={false}
                  isConnected={playerConnections[game.player_x] !== false}
                />
                <PlayerInfo
                  player={{
                    username: game.player_o || "Waiting for Player O...",
                    symbol: "O",
                  }}
                  isActive={
                    game.current_turn === "O" && !game.winner && !game.is_draw
                  }
                  isCurrentUser={currentPlayer === game.player_o}
                  isWaiting={!game.player_o}
                  isConnected={
                    game.player_o
                      ? playerConnections[game.player_o] !== false
                      : true
                  }
                />
              </div>

              {/* Game Status */}
              <div className="mt-6">
                {game.player_o ? (
                  isCurrentPlayerTurn() ? (
                    <div className="bg-accent-success/10 border border-accent-success/20 text-accent-success p-3 rounded-lg text-center">
                      <div className="font-medium">🎯 Your turn!</div>
                      <div className="text-sm opacity-75">Make your move</div>
                    </div>
                  ) : (
                    <div className="bg-background-tertiary border border-border-light text-text-secondary p-3 rounded-lg text-center">
                      <div className="font-medium">⏳ Waiting for opponent</div>
                      <div className="text-sm">
                        {currentPlayer === game.player_x
                          ? game.player_o
                          : game.player_x}
                        's turn
                      </div>
                    </div>
                  )
                ) : (
                  <div className="bg-accent-warning/10 border border-accent-warning/20 text-accent-warning p-3 rounded-lg text-center">
                    <div className="font-medium">🔍 Waiting for opponent</div>
                    <div className="text-sm">
                      Share the game ID to invite players
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
          {/* Game Board Section */}
          <div className="lg:col-span-2 flex items-center justify-center">
            <GameBoard
              board={game.board}
              onSquareClick={handleSquareClick}
              disabled={!isCurrentPlayerTurn() || isGameCompleted()}
            />
          </div>{" "}
          {/* Chat Section */}
          <div className="lg:col-span-1">
            <ChatBox messages={messages} sendMessage={sendMessage} />{" "}
          </div>
        </div>

        {/* Rematch Modal */}
        <RematchModal
          isOpen={showRematchModal}
          onAccept={handleAcceptRematch}
          onDecline={handleDeclineRematch}
          requestingPlayer={rematchRequestingPlayer}
        />
      </div>

      {/* React Hot Toast Container */}
      <Toaster
        position="top-center"
        toastOptions={{
          duration: 4000,
          style: {
            background: "#1f2937",
            color: "#f9fafb",
            border: "1px solid #374151",
            borderRadius: "0.5rem",
            fontSize: "14px",
            fontFamily: "monospace",
          },
        }}
      />
    </div>
  );
};

export default GameRoom;
