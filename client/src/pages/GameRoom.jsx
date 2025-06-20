import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getGameDetails } from "../services/api";
import GameBoard from "../components/GameBoard";
import PlayerInfo from "../components/PlayerInfo";
import ChatBox from "../components/ChatBox";

const GameRoom = () => {
  const { id: gameId } = useParams();
  const { socket } = useSocket();
  const navigate = useNavigate();

  const [game, setGame] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
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
      });

      // Game events
      socket.on("player_joined", () => fetchGameDetails());
      socket.on("game_over", () => fetchGameDetails());
    }

    return () => {
      if (socket) {
        socket.emit("leave_room", { room: gameId, player: username });
        socket.off("game_state_update");
        socket.off("move_made");
        socket.off("receive_message");
        socket.off("player_joined");
        socket.off("game_over");
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
        text: text,
        timestamp: Date.now(),
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
  if (loading) {
    return (
      <div className="min-h-screen bg-cyber-black flex items-center justify-center">
        <div className="cyber-card p-8 text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-neon-green border-t-transparent mx-auto mb-4"></div>
          <p className="text-neon-cyan font-mono">LOADING GAME MATRIX...</p>
        </div>
      </div>
    );
  }

  if (!game) {
    return (
      <div className="min-h-screen bg-cyber-black flex items-center justify-center">
        <div className="cyber-card p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="text-6xl mb-4 animate-neon-pulse">🎮</div>
            <h2 className="text-2xl font-bold text-neon-green mb-4 neon-text font-mono">
              GAME NOT FOUND
            </h2>
            <p className="text-neon-cyan mb-6 font-mono">
              The game you're looking for doesn't exist or has been deleted.
            </p>
            <button
              className="btn-neon w-full py-3 font-mono"
              onClick={() => navigate("/lobby")}
            >
              🏠 BACK TO LOBBY
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-cyber-black relative overflow-hidden">
      {/* Floating Particles */}
      <div className="floating-particles">
        {[...Array(10)].map((_, i) => (
          <div
            key={i}
            className="particle"
            style={{
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${6 + Math.random() * 4}s`,
            }}
          />
        ))}
      </div>

      {/* Animated Background Grid */}
      <div className="absolute inset-0 game-grid opacity-10"></div>

      <div className="relative z-10 min-h-screen">
        <div className="container mx-auto px-4 py-6">
          {/* Header Section */}
          <div className="cyber-card p-6 mb-6">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <h1 className="text-3xl font-bold text-neon-green mb-2 flex items-center gap-2 neon-text font-mono">
                  🎮 GAME ROOM
                </h1>
                <p className="text-neon-cyan font-mono">
                  GAME ID:{" "}
                  <span className="font-mono font-medium text-neon-purple">
                    {gameId}
                  </span>
                </p>
              </div>

              {/* Control Buttons */}
              <div className="flex flex-wrap gap-2">
                <button
                  className="btn-neon-cyan text-sm px-4 py-2 font-mono"
                  onClick={reloadGameState}
                  disabled={loading}
                  title="Refresh game state"
                >
                  🔄 RELOAD
                </button>

                {canControlGame() && isGameCompleted() && (
                  <button
                    className="btn-neon text-sm px-4 py-2 font-mono"
                    onClick={requestRestart}
                    title="Request to play again"
                  >
                    🔁 PLAY AGAIN
                  </button>
                )}

                {canControlGame() && isGameCompleted() && (
                  <button
                    className="bg-neon-pink/20 hover:bg-neon-pink/30 text-neon-pink border-2 border-neon-pink text-sm px-4 py-2 rounded-md font-mono font-bold transition-all duration-300"
                    onClick={deleteGame}
                    title="Delete this game"
                  >
                    🗑️ DELETE
                  </button>
                )}

                <button
                  className="bg-text-muted/20 hover:bg-text-muted/30 text-text-muted border-2 border-text-muted text-sm px-4 py-2 rounded-md font-mono font-bold transition-all duration-300"
                  onClick={leaveGame}
                  title="Leave game and return to lobby"
                >
                  🚪 LEAVE
                </button>
              </div>
            </div>
          </div>

          {/* Error Message */}
          {error && (
            <div className="bg-neon-pink/10 border-2 border-neon-pink text-neon-pink p-4 rounded-lg mb-6 animate-neon-flicker">
              <div className="flex items-center gap-2 font-mono">
                <span>⚠️</span>
                <span className="uppercase tracking-wide">{error}</span>
              </div>
            </div>
          )}

          {/* Game Result Banner */}
          {isGameCompleted() && (
            <div className="cyber-card p-6 mb-6 bg-neon-green/5 border-neon-green/20">
              <div className="text-center">
                <div className="text-4xl mb-3 animate-neon-pulse">
                  {game.is_draw ? "🤝" : "🎉"}
                </div>
                <h2 className="text-2xl font-bold text-neon-green mb-4 neon-text font-mono">
                  {game.is_draw
                    ? "GAME ENDED IN DRAW!"
                    : `${
                        game.winner === "X" ? game.player_x : game.player_o
                      } WINS!`}
                </h2>
                <p className="text-neon-cyan mb-4 font-mono">
                  {game.is_draw
                    ? "EXCELLENT STRATEGY FROM BOTH PLAYERS"
                    : `PLAYER ${game.winner} ACHIEVED VICTORY!`}
                </p>
              </div>
            </div>
          )}

          {/* Main Game Content */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Players Section */}
            <div className="lg:col-span-1">
              <div className="cyber-card p-6">
                <h2 className="text-xl font-semibold text-neon-green mb-4 flex items-center gap-2 neon-text font-mono">
                  👥 PLAYERS
                </h2>
                <div className="space-y-4">
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
                    isConnected={true}
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
                    isConnected={true}
                  />
                </div>

                {/* Game Status */}
                <div className="mt-6">
                  {game.player_o ? (
                    isCurrentPlayerTurn() ? (
                      <div className="bg-neon-green/10 border-2 border-neon-green text-neon-green p-3 rounded-lg text-center">
                        <div className="font-medium font-mono neon-text">
                          🎯 YOUR TURN!
                        </div>
                        <div className="text-sm opacity-75 font-mono">
                          MAKE YOUR MOVE
                        </div>
                      </div>
                    ) : (
                      <div className="bg-cyber-darker border-2 border-neon-cyan/30 text-neon-cyan p-3 rounded-lg text-center">
                        <div className="font-medium font-mono">
                          ⏳ WAITING FOR OPPONENT
                        </div>
                        <div className="text-sm font-mono">
                          {currentPlayer === game.player_x
                            ? game.player_o
                            : game.player_x}
                          'S TURN
                        </div>
                      </div>
                    )
                  ) : (
                    <div className="bg-neon-yellow/10 border-2 border-neon-yellow text-neon-yellow p-3 rounded-lg text-center">
                      <div className="font-medium font-mono">
                        🔍 WAITING FOR OPPONENT
                      </div>
                      <div className="text-sm font-mono">
                        SHARE GAME ID TO INVITE
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
            </div>

            {/* Chat Section */}
            <div className="lg:col-span-1">
              <ChatBox messages={messages} sendMessage={sendMessage} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GameRoom;
