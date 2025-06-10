import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getGameDetails, testConnection } from "../services/api";
import GameBoard from "../components/GameBoard";
import PlayerInfo from "../components/PlayerInfo";
import ChatBox from "../components/ChatBox";

const GameRoom = () => {
  const { id: gameId } = useParams();
  const { socket } = useSocket();
  const navigate = useNavigate();

  // Safety check for required parameters
  if (!gameId) {
    console.error("GameRoom: Missing gameId parameter");
    navigate("/lobby");
    return null;
  }
  const [game, setGame] = useState(null);
  const [messages, setMessages] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [connectionStatus, setConnectionStatus] = useState("connecting");
  const [typingUsers, setTypingUsers] = useState(new Set());
  const [restartRequested, setRestartRequested] = useState(false);
  const [restartRequestedBy, setRestartRequestedBy] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [lastFetchTime, setLastFetchTime] = useState(0);
  const [fetchInProgress, setFetchInProgress] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    if (!token || !username) {
      navigate("/");
      return;
    }

    setCurrentPlayer(username);
    fetchGameDetails();

    // Setup socket with retry logic
    const setupSocketListeners = () => {
      if (!socket || !socket.connected) {
        console.log("Socket not ready, waiting...");
        return false;
      }

      setConnectionStatus("connected");
      console.log("Setting up socket listeners for game room:", gameId); // Join the game room
      socket.emit("join_room", {
        room: gameId,
        player: username,
        timestamp: new Date().toISOString(),
      });

      console.log("Emitted join_room event for:", { gameId, username }); // Game state updates
      socket.on("game_state_update", (data) => {
        console.log("Game state update received:", data);
        try {
          if (data && data.game && typeof data.game === "object") {
            setGame((prevGame) => {
              // Ensure we properly update the game state
              const newGame = { ...data.game };
              console.log("Updating game state:", {
                old_player_o: prevGame?.player_o,
                new_player_o: newGame.player_o,
                both_players_present: !!newGame.player_o,
              });
              return newGame;
            });
            setLoading(false); // Ensure loading is false when we get game data
          } else {
            console.warn(
              "Invalid game data received in game_state_update:",
              data
            );
          }
          setError("");
          if (data.last_move) {
            // Track the last move for potential UI updates
            console.log("Last move:", data.last_move);
          }
          if (data.player_o_joined || data.both_players_present) {
            console.log("Player O joined - updating UI");
            setError("🎉 Second player joined! Game is ready to start.");
            setTimeout(() => setError(""), 3000);
          }
        } catch (err) {
          console.error("Error handling game_state_update:", err);
          setError("Error updating game state");
        }
      }); // Game ready notification
      socket.on("game_ready", (data) => {
        console.log("Game ready event received:", data);
        try {
          if (data && data.game && typeof data.game === "object") {
            setGame((prevGame) => {
              const newGame = { ...data.game };
              console.log("Game ready - updating state:", {
                player_x: newGame.player_x,
                player_o: newGame.player_o,
                both_players_present: !!newGame.player_o,
              });
              return newGame;
            });
            setError("🎉 Game is ready! Both players have joined.");
            setTimeout(() => setError(""), 3000); // Force refresh to ensure we have the latest state
            setTimeout(() => {
              fetchGameDetails(true);
            }, 1000); // Increased delay to reduce rapid calls
          } else {
            console.warn("Invalid game data received in game_ready:", data);
            setError("Game ready but invalid data received");
          }
        } catch (err) {
          console.error("Error handling game_ready:", err);
          setError("Error processing game ready event");
        }
      }); // Move made by any player
      socket.on("move_made", (moveData) => {
        try {
          if (moveData && moveData.game && typeof moveData.game === "object") {
            if (moveData.player !== currentPlayer) {
              setGame(moveData.game);
              // Add visual feedback for opponent moves
            }
          } else {
            console.warn("Invalid move data received:", moveData);
          }
        } catch (err) {
          console.error("Error handling move_made:", err);
          setError("Error processing move");
        }
      });

      // Player joined the game
      socket.on("player_joined", (data) => {
        console.log("Player joined event received:", data);

        // If this indicates the game is ready, force a game state refresh
        if (data.game_ready && data.player !== username) {
          console.log("Game became ready - forcing state refresh");
          setError(`🎉 ${data.player} has joined! Game is ready to start.`);
          setTimeout(() => setError(""), 4000); // Immediately refresh game state
          setTimeout(() => {
            fetchGameDetails(true);
          }, 500); // Reduced delay but keep some debouncing
        } else if (data.player !== username) {
          setError(`👋 ${data.player} joined as ${data.role}.`);
          setTimeout(() => setError(""), 3000); // Refresh game state for any player join
          setTimeout(() => {
            fetchGameDetails(true);
          }, 800); // Increased delay to reduce rapid calls
        }
      });

      // Player left the game
      socket.on("player_left", (data) => {
        setError(`${data.player} has left the game`);
        setTimeout(() => setError(""), 5000);
      });

      // Player disconnected
      socket.on("player_disconnected", (data) => {
        setError(`${data.player} has disconnected`);
      });

      // Chat messages
      socket.on("receive_message", (message) => {
        setMessages((prev) => [...prev, message]);
      });

      // Typing indicators
      socket.on("user_typing", (data) => {
        if (data.is_typing) {
          setTypingUsers((prev) => new Set([...prev, data.user]));
        } else {
          setTypingUsers((prev) => {
            const newSet = new Set(prev);
            newSet.delete(data.user);
            return newSet;
          });
        }

        setTimeout(() => {
          setTypingUsers((prev) => {
            const newSet = new Set(prev);
            newSet.delete(data.user);
            return newSet;
          });
        }, 3000);
      }); // Game over
      socket.on("game_over", (result) => {
        try {
          if (result && typeof result === "object") {
            setGame((prev) => ({
              ...prev,
              winner: result.winner,
              is_draw: result.is_draw,
            }));

            // Show game result
            if (result.is_draw) {
              setError("Game ended in a draw!");
            } else {
              const winnerName =
                result.winner_name || `Player ${result.winner}`;
              setError(`🎉 ${winnerName} wins the game!`);
            }
          } else {
            console.warn("Invalid game over data received:", result);
            setError("Game ended with invalid data");
          }
        } catch (err) {
          console.error("Error handling game_over:", err);
          setError("Error processing game over event");
        }
      });

      // Restart game handlers
      socket.on("restart_requested", (data) => {
        setRestartRequested(true);
        setRestartRequestedBy(data.requesting_player);

        if (data.requesting_player === currentPlayer) {
          setError("Restart request sent! Waiting for other player...");
        } else {
          setError(`${data.requesting_player} wants to restart the game.`);
        }
      });
      socket.on("game_restarted", (data) => {
        try {
          if (data && data.game && typeof data.game === "object") {
            setGame(data.game);
            setRestartRequested(false);
            setRestartRequestedBy(null);
            setError("🔄 Game has been restarted!");
            setTimeout(() => setError(""), 3000);
          } else {
            console.warn("Invalid restart data received:", data);
            setError("Game restart failed - invalid data");
          }
        } catch (err) {
          console.error("Error handling game_restarted:", err);
          setError("Error processing game restart");
        }
      });

      // Game deletion handlers
      socket.on("game_deleted", (data) => {
        setError(
          `🗑️ Game deleted by ${data.deleted_by}. Redirecting to lobby...`
        );
        setTimeout(() => {
          navigate("/lobby");
        }, 3000);
      });
      socket.on("game_auto_deleted", () => {
        setError(
          "🧹 Game automatically deleted due to inactivity. Redirecting to lobby..."
        );
        setTimeout(() => {
          navigate("/lobby");
        }, 3000);
      });

      // Socket errors
      socket.on("error", (error) => {
        console.error("Socket error:", error);
        setError(error.message || "An error occurred");
      });

      // Connection events
      socket.on("connect", () => {
        setConnectionStatus("connected");
        setError("");

        // Re-join room on reconnect
        socket.emit("join_room", {
          room: gameId,
          player: username,
          timestamp: new Date().toISOString(),
        });
      });

      socket.on("disconnect", () => {
        setConnectionStatus("disconnected");
        setError("Connection lost. Attempting to reconnect...");
      });

      return true;
    };

    // Try setup immediately
    if (!setupSocketListeners()) {
      setConnectionStatus("connecting");

      // Retry setup when socket becomes available
      const checkInterval = setInterval(() => {
        if (setupSocketListeners()) {
          clearInterval(checkInterval);
        }
      }, 1000);

      return () => clearInterval(checkInterval);
    }

    return () => {
      if (socket) {
        try {
          socket.emit("leave_room", {
            room: gameId,
            player: username,
            timestamp: new Date().toISOString(),
          });
        } catch {
          // Error leaving room - continue cleanup
        }

        // Clean up all event listeners
        const events = [
          "game_state_update",
          "game_ready",
          "move_made",
          "player_joined",
          "player_left",
          "player_disconnected",
          "receive_message",
          "user_typing",
          "game_over",
          "restart_requested",
          "game_restarted",
          "game_deleted",
          "game_auto_deleted",
          "error",
          "connect",
          "disconnect",
        ];

        events.forEach((event) => {
          try {
            socket.off(event);
          } catch {
            // Error removing event listener - continue cleanup
          }
        });
      }
    };
  }, [socket, gameId, navigate, currentPlayer]);
  const fetchGameDetails = async (force = false) => {
    if (!gameId) {
      setError("Invalid game ID");
      setLoading(false);
      return;
    }

    // Prevent concurrent API calls
    if (fetchInProgress && !force) {
      console.log("Fetch already in progress, skipping duplicate call");
      return;
    }

    // Debounce API calls - prevent rapid successive calls
    const now = Date.now();
    if (!force && now - lastFetchTime < 3000) {
      console.log("Debouncing fetchGameDetails call");
      return;
    }

    setFetchInProgress(true);
    setLastFetchTime(now);

    try {
      console.log(`Fetching game details for game ${gameId}...`);
      const gameData = await getGameDetails(gameId);
      if (gameData && typeof gameData === "object") {
        setGame(gameData);
        setError("");
        console.log("Game data fetched successfully");
      } else {
        throw new Error("Invalid game data received");
      }
    } catch (error) {
      console.error("Failed to fetch game details:", error);

      if (error.response?.status === 404) {
        setError(`Game ${gameId} not found. Redirecting to lobby...`);
        setTimeout(() => {
          navigate("/lobby");
        }, 3000);
      } else if (error.response?.status === 401) {
        setError("Session expired. Please log in again.");
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setTimeout(() => {
          navigate("/");
        }, 2000);
      } else if (error.code === "ECONNABORTED") {
        setError(
          "Server timeout. Click 'Refresh Game' button above to try again."
        );
      } else if (
        error.code === "NETWORK_ERROR" ||
        error.code === "ECONNREFUSED"
      ) {
        setError(
          "Cannot connect to server. Please check if the server is running."
        );
      } else {
        setError("Failed to load game. Please try refreshing.");
      }
    } finally {
      setLoading(false);
      setFetchInProgress(false);
    }
  };
  const handleRefreshGame = async () => {
    setRefreshing(true);
    setError("");

    try {
      // First test connection
      const connectionTest = await testConnection();
      if (!connectionTest.connected) {
        setError(`Cannot connect to server: ${connectionTest.error}`);
        return;
      }

      await fetchGameDetails(true);

      // Re-emit join room to get latest game state from server
      if (socket && currentPlayer) {
        socket.emit("join_room", {
          room: gameId,
          player: currentPlayer,
          timestamp: new Date().toISOString(),
        });
      }

      setError("Game refreshed successfully!");
      setTimeout(() => setError(""), 2000);
    } catch (error) {
      console.error("Failed to refresh game:", error);
      setError("Failed to refresh game");
    } finally {
      setRefreshing(false);
    }
  };
  const handleSquareClick = async (index) => {
    // Safety check for game state
    if (!game || !game.board) {
      console.log("Game not loaded yet");
      setError("Game not loaded yet. Please wait...");
      return;
    }

    console.log("Square clicked:", index, "Current game state:", {
      player_x: game.player_x,
      player_o: game.player_o,
      current_turn: game.current_turn,
      board: game.board[index],
    });

    // Prevent moves on completed games
    if (game.board[index] !== "" || game.winner || game.is_draw) {
      console.log("Move blocked - game completed or square occupied");
      return;
    } // Use current game state - don't fetch fresh data for every move
    const currentGame = game;

    // Check if both players are present
    if (!currentGame.player_o) {
      console.log("Move blocked - Player O not present yet");
      setError("Waiting for another player to join!");
      return;
    }

    // Check if it's player's turn
    const isPlayerTurn =
      (currentGame.current_turn === "X" &&
        currentPlayer === currentGame.player_x) ||
      (currentGame.current_turn === "O" &&
        currentPlayer === currentGame.player_o);

    console.log("Turn check:", {
      current_turn: currentGame.current_turn,
      currentPlayer,
      player_x: currentGame.player_x,
      player_o: currentGame.player_o,
      isPlayerTurn,
    });

    if (!isPlayerTurn) {
      console.log("Move blocked - not player's turn");
      setError("It's not your turn!");
      setTimeout(() => setError(""), 2000);
      return;
    }

    // Clear any previous errors
    setError("");

    console.log("Making move - emitting to server");
    // Make the move
    if (socket && socket.connected) {
      socket.emit("make_move", {
        room: gameId,
        index: index,
        symbol: currentGame.current_turn,
        player: currentPlayer,
        timestamp: new Date().toISOString(),
      });
    } else {
      setError("Not connected to server. Please wait...");
    }
  };

  const sendMessage = (text) => {
    if (socket && currentPlayer) {
      const message = {
        room: gameId,
        sender: currentPlayer,
        text: text,
        timestamp: Date.now(),
      };
      socket.emit("send_message", message);
    }
  };

  // Enhanced typing indicator
  const handleTyping = (isTyping) => {
    if (socket && currentPlayer) {
      socket.emit("typing_indicator", {
        room: gameId,
        user: currentPlayer,
        is_typing: isTyping,
      });
    }
  };

  const requestGameRestart = () => {
    if (socket && currentPlayer) {
      socket.emit("request_game_restart", {
        room: gameId,
        player: currentPlayer,
      });
    }
  };

  const acceptGameRestart = () => {
    if (socket && currentPlayer) {
      socket.emit("accept_restart", {
        room: gameId,
        player: currentPlayer,
      });
      setRestartRequested(false);
      setRestartRequestedBy(null);
      setError("Restart accepted! Waiting for game to restart...");
    }
  };

  const deleteGame = () => {
    if (socket && currentPlayer) {
      socket.emit("delete_finished_game", {
        room: gameId,
        player: currentPlayer,
      });
    }
  };

  const refreshGameState = () => {
    setError("Refreshing game state...");
    fetchGameDetails();
    if (socket && currentPlayer) {
      // Re-emit join room to get latest state
      socket.emit("join_room", {
        room: gameId,
        player: currentPlayer,
        timestamp: new Date().toISOString(),
      });
    }
    setTimeout(() => {
      if (error === "Refreshing game state...") {
        setError("");
      }
    }, 2000);
  };

  const reloadConnection = () => {
    if (socket) {
      // Force disconnect and reconnect
      socket.disconnect();
      setTimeout(() => {
        socket.connect();
      }, 1000);
    }
    setError("Reloading connection...");
  };

  const leaveGame = () => {
    navigate("/lobby");
  };
  const getCurrentPlayerRole = () => {
    if (!game) return "spectator";
    if (currentPlayer === game.player_x) return "X";
    if (currentPlayer === game.player_o) return "O";
    return "spectator";
  };

  const isCurrentPlayerTurn = () => {
    if (!game || !game.player_o) return false; // Can't play until both players are present
    const playerRole = getCurrentPlayerRole();
    return playerRole !== "spectator" && game.current_turn === playerRole;
  };

  const getOpponentName = () => {
    if (!game) return null;
    if (currentPlayer === game.player_x) return game.player_o;
    if (currentPlayer === game.player_o) return game.player_x;
    return null;
  };

  if (loading) {
    return (
      <div className="container mx-auto p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p>Loading game...</p>
        </div>
      </div>
    );
  }
  // Add error state handling
  if (error && error.includes("not found")) {
    return (
      <div className="container mx-auto p-4">
        <div className="bg-red-100 text-red-700 p-4 rounded mb-4">
          <h2 className="text-xl font-bold mb-2">Game Not Found</h2>
          <p>{error}</p>
        </div>
        <button
          className="bg-blue-500 text-white py-2 px-4 rounded"
          onClick={() => navigate("/lobby")}
        >
          Back to Lobby
        </button>
      </div>
    );
  }

  // Safety check for game state
  if (!game) {
    return (
      <div className="container mx-auto p-4">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p>Loading game data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      {" "}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">
            Game Room: {gameId}
          </h1>
          <div className="flex items-center gap-2 mt-1">
            <div
              className={`w-3 h-3 rounded-full ${
                connectionStatus === "connected"
                  ? "bg-green-500"
                  : connectionStatus === "connecting"
                  ? "bg-yellow-500"
                  : "bg-red-500"
              }`}
            ></div>
            <span className="text-sm text-gray-600 capitalize">
              {connectionStatus}
            </span>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            className="bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 disabled:bg-gray-400 flex items-center gap-2 transition-colors"
            onClick={handleRefreshGame}
            disabled={refreshing}
          >
            <span className={refreshing ? "animate-spin" : ""}>🔄</span>
            {refreshing ? "Refreshing..." : "Refresh Game"}
          </button>
          {connectionStatus === "disconnected" && (
            <button
              className="bg-yellow-500 text-white py-2 px-4 rounded-lg hover:bg-yellow-600 flex items-center gap-2"
              onClick={reloadConnection}
            >
              🔌 Reconnect
            </button>
          )}
          <button
            className="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 flex items-center gap-2"
            onClick={leaveGame}
          >
            🚪 Leave Game
          </button>
        </div>
      </div>
      {error && (
        <div
          className={`p-3 rounded mb-4 ${
            error.includes("🎉")
              ? "bg-green-100 text-green-700"
              : error.includes("joined") || error.includes("ready")
              ? "bg-blue-100 text-blue-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {error}
        </div>
      )}{" "}
      {(game?.winner || game?.is_draw) && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 p-4 rounded mb-4">
          <div className="flex flex-col space-y-3">
            <div className="text-center text-lg font-semibold">
              {game?.is_draw
                ? "🤝 Game ended in a draw!"
                : `🎉 ${
                    game?.winner === "X"
                      ? game?.player_x || "Player X"
                      : game?.player_o || "Player O"
                  } (Player ${game?.winner}) wins!`}
            </div>

            {/* Show restart request status if pending */}
            {restartRequested && (
              <div className="text-center text-sm">
                {restartRequestedBy === currentPlayer
                  ? "⏳ Waiting for opponent to accept restart..."
                  : `⏳ ${restartRequestedBy} has requested a restart`}
              </div>
            )}

            {/* Action buttons */}
            <div className="flex justify-center gap-2">
              {(currentPlayer === game.player_x ||
                currentPlayer === game.player_o) &&
                !restartRequested && (
                  <button
                    className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
                    onClick={requestGameRestart}
                  >
                    🔄 Play Again
                  </button>
                )}

              {(currentPlayer === game.player_x ||
                currentPlayer === game.player_o) && (
                <button
                  className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition-colors"
                  onClick={() => {
                    if (
                      window.confirm(
                        "Are you sure you want to delete this game? This action cannot be undone."
                      )
                    ) {
                      deleteGame();
                    }
                  }}
                >
                  🗑️ Delete Game
                </button>
              )}

              <button
                className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition-colors"
                onClick={() => navigate("/lobby")}
              >
                🏠 Back to Lobby
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Show restart request notification */}
      {restartRequested &&
        restartRequestedBy &&
        restartRequestedBy !== currentPlayer && (
          <div className="bg-blue-100 border border-blue-400 text-blue-700 p-4 rounded mb-4">
            <div className="flex justify-between items-center">
              <div>🔄 {restartRequestedBy} wants to restart the game</div>
              <div className="flex gap-2">
                <button
                  className="bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition-colors"
                  onClick={acceptGameRestart}
                >
                  ✅ Accept
                </button>
                <button
                  className="bg-gray-500 text-white py-2 px-4 rounded hover:bg-gray-600 transition-colors"
                  onClick={() => {
                    setRestartRequested(false);
                    setRestartRequestedBy(null);
                    setError("Restart request declined");
                    setTimeout(() => setError(""), 2000);
                  }}
                >
                  ❌ Decline
                </button>
              </div>
            </div>
          </div>
        )}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-3">Players</h2>
          {/* Connection Status Indicator */}
          <div
            className={`mb-3 p-3 rounded flex justify-between items-center ${
              connectionStatus === "connected"
                ? "bg-green-100 text-green-700"
                : connectionStatus === "disconnected"
                ? "bg-red-100 text-red-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
          >
            <span className="text-sm font-medium">
              Connection: {connectionStatus}
            </span>
            {connectionStatus === "disconnected" && (
              <button
                className="bg-red-600 text-white px-2 py-1 rounded text-xs hover:bg-red-700"
                onClick={reloadConnection}
              >
                🔄 Reload
              </button>
            )}
          </div>{" "}
          <div className="space-y-3">
            <PlayerInfo
              player={{ username: game.player_x || "Player X", symbol: "X" }}
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
          <div className="mt-4">
            {game.player_o ? (
              isCurrentPlayerTurn() ? (
                <div className="bg-green-100 p-2 rounded text-center">
                  Your turn! (Playing as {getCurrentPlayerRole()})
                </div>
              ) : getCurrentPlayerRole() !== "spectator" ? (
                <div className="bg-gray-100 p-2 rounded text-center">
                  {getOpponentName()}'s turn (
                  {game.current_turn === "X" ? "X" : "O"})
                </div>
              ) : (
                <div className="bg-blue-100 p-2 rounded text-center">
                  Spectating:{" "}
                  {game.current_turn === "X" ? game.player_x : game.player_o}'s
                  turn
                </div>
              )
            ) : (
              <div className="bg-yellow-100 p-2 rounded text-center">
                Waiting for opponent
              </div>
            )}
          </div>
          {/* Typing indicators */}
          {typingUsers.size > 0 && (
            <div className="mt-2 text-sm text-gray-500">
              {Array.from(typingUsers).join(", ")}{" "}
              {typingUsers.size === 1 ? "is" : "are"} typing...
            </div>
          )}
        </div>

        <div className="flex items-center justify-center">
          <GameBoard board={game.board} onSquareClick={handleSquareClick} />
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-3">Chat</h2>
          <ChatBox
            messages={messages}
            sendMessage={sendMessage}
            onTyping={handleTyping}
          />
        </div>
      </div>
    </div>
  );
};

export default GameRoom;
