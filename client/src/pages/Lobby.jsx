import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getAllGames, createGame } from "../services/api";

const Lobby = () => {
  const [games, setGames] = useState([]);
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false); // Added loading state
  const [error, setError] = useState(""); // Added error state
  const { socket } = useSocket();
  const navigate = useNavigate();
  const fetchGames = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const allGames = await getAllGames();
      setGames(allGames);
    } catch (err) {
      console.error("Failed to fetch games:", err);

      // Better error messaging based on error type
      let errorMessage = "Failed to load games.";
      if (err.response?.status === 401) {
        errorMessage = "Session expired. Please log in again.";
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        setTimeout(() => navigate("/"), 2000);
      } else if (err.code === "ECONNABORTED") {
        errorMessage =
          "Server is taking too long to respond. Please check if the server is running.";
      } else if (err.code === "NETWORK_ERROR" || err.code === "ECONNREFUSED") {
        errorMessage =
          "Cannot connect to server. Please check if the server is running on the correct port.";
      } else if (err.response?.status === 500) {
        errorMessage = "Server error. Please try again later.";
      } else if (err.response?.data?.msg) {
        errorMessage = err.response.data.msg;
      } else if (err.message) {
        errorMessage = err.message;
      }

      setError(errorMessage);
      setGames([]); // Clear games on error
    } finally {
      setLoading(false);
    }
  }, [navigate]); // Add navigate to dependency array

  useEffect(() => {
    const token = localStorage.getItem("token");
    const storedUsername = localStorage.getItem("username");

    if (!token) {
      navigate("/");
      return;
    }

    if (storedUsername) {
      setUsername(storedUsername);
    }

    fetchGames(); // Setup socket event handling with cleanup
    const setupSocketListeners = () => {
      if (!socket || !socket.connected) {
        return false;
      }

      // Join lobby room for real-time updates
      socket.emit("join_lobby");

      // Real-time lobby updates
      socket.on("lobby_games_update", (data) => {
        console.log("Lobby games update:", data);
        setGames(data.games || []);
      });

      socket.on("game_created", (newGame) => {
        if (newGame && newGame.id) {
          setGames((prevGames) => [...prevGames, newGame]);
        }
      });

      socket.on("game_started", (data) => {
        console.log("Game started:", data);
        setGames((prevGames) =>
          prevGames.filter((game) => game.id !== data.game_id)
        );
      });

      socket.on("game_completed", () => {
        // Refresh games list when a game is completed
        setTimeout(fetchGames, 1000);
      });

      socket.on("player_count_updated", (data) => {
        setGames((prevGames) =>
          prevGames.map((game) =>
            game.id === data.game_id
              ? { ...game, playerCount: data.playerCount }
              : game
          )
        );
      });

      // Handle lobby refresh notifications
      socket.on("lobby_refresh_needed", (data) => {
        console.log("Lobby refresh needed:", data);
        fetchGames();
      });

      // Connection status indicators
      socket.on("connect", () => {
        setError("");
        fetchGames(); // Refresh on reconnect
      });

      socket.on("disconnect", () => {
        setError("Connection lost. Attempting to reconnect...");
      });

      // Handle delete responses
      socket.on("success", (data) => {
        setError("");
        console.log("Success:", data.message);
      });

      socket.on("error", (data) => {
        setError(data.message);
      });

      return true;
    };

    // Try to setup listeners immediately
    if (!setupSocketListeners()) {
      // If socket not ready, retry periodically
      const retryInterval = setInterval(() => {
        if (setupSocketListeners()) {
          clearInterval(retryInterval);
        }
      }, 1000);

      return () => clearInterval(retryInterval);
    }

    return () => {
      if (socket) {
        try {
          socket.emit("leave_lobby");
        } catch {
          // Error leaving lobby - continue cleanup
        } // Clean up event listeners
        const events = [
          "lobby_games_update",
          "game_created",
          "game_started",
          "game_completed",
          "player_count_updated",
          "lobby_refresh_needed",
          "connect",
          "disconnect",
          "success",
          "error",
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
  }, [socket, navigate, fetchGames]);

  const handleCreateGame = async () => {
    // Renamed from createGame to avoid conflict
    if (!username.trim()) {
      setError("Please enter a username in the input field first.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const response = await createGame(); // API call
      localStorage.setItem("username", username); // Ensure username is saved
      if (response && response.gameId) {
        navigate(`/game/${response.gameId}`);
      } else {
        throw new Error("Game creation did not return a gameId.");
      }
    } catch (err) {
      console.error("Failed to create game:", err);
      setError(
        err.response?.data?.msg || err.message || "Failed to create game."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleJoinGame = async (gameId) => {
    // Renamed from joinGame
    if (!username.trim()) {
      setError("Please enter a username in the input field first.");
      return;
    }
    setError("");
    localStorage.setItem("username", username); // Ensure username is saved

    try {
      const token = localStorage.getItem("token");
      // Optional: API call to server to formally join, if your backend requires it
      // For now, we assume joining is by navigating and socket emitting 'join_room' in GameRoom
      // If an API call is needed:
      // await api.post(`/game/join/${gameId}`, { username }); // Example
      navigate(`/game/${gameId}`);
    } catch (err) {
      console.error("Failed to join game:", err);
      setError(
        err.response?.data?.msg || err.message || "Failed to join game."
      );
    }
  };
  const handleLogout = () => {
    // Renamed from logout
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    // Disconnect socket if necessary, or let SocketProvider handle it
    if (socket) {
      socket.disconnect();
    }
    navigate("/");
  };

  const handleDeleteGame = (gameId) => {
    if (!username.trim()) {
      setError("Please enter a username first.");
      return;
    }

    if (
      window.confirm(
        "Are you sure you want to delete this game? This action cannot be undone."
      )
    ) {
      if (socket) {
        socket.emit("delete_game_from_lobby", {
          game_id: gameId,
          player: username,
        });
      }
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-6xl">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800">🎮 Game Lobby</h1>
          <p className="text-gray-600 mt-1">Welcome, {username || "Player"}!</p>
        </div>
        <button
          className="bg-red-500 text-white py-2 px-4 rounded-lg hover:bg-red-600 transition-colors flex items-center gap-2"
          onClick={handleLogout}
        >
          🚪 Logout
        </button>
      </div>
      {error && (
        <div
          className={`border px-4 py-3 rounded-lg relative mb-4 ${
            error.includes("Connection lost")
              ? "bg-yellow-50 border-yellow-400 text-yellow-700"
              : "bg-red-50 border-red-400 text-red-700"
          }`}
          role="alert"
        >
          <div className="flex items-center gap-2">
            <span>{error.includes("Connection lost") ? "⚠️" : "❌"}</span>
            <span>{error}</span>
          </div>
        </div>
      )}
      <div className="mb-6 p-6 border border-gray-200 rounded-lg shadow-sm bg-white">
        <div className="mb-4">
          <label
            htmlFor="usernameInput"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Your Username:
          </label>
          <input
            id="usernameInput"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
            placeholder="Enter your username"
          />
        </div>

        <div className="flex flex-wrap gap-3">
          <button
            onClick={handleCreateGame}
            className="bg-green-500 hover:bg-green-600 text-white font-medium py-3 px-6 rounded-lg disabled:bg-gray-400 flex items-center gap-2 transition-colors"
            disabled={!username.trim() || loading}
          >
            <span>✨</span>
            {loading ? "Creating..." : "Create New Game"}
          </button>
          <button
            onClick={fetchGames}
            className="bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-6 rounded-lg disabled:bg-gray-400 flex items-center gap-2 transition-colors"
            disabled={loading}
          >
            <span className={loading ? "animate-spin" : ""}>🔄</span>
            {loading ? "Refreshing..." : "Refresh Games"}
          </button>
        </div>
      </div>{" "}
      <div>
        {" "}
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-gray-800">
            🎯 All Games ({games.length})
          </h2>
          <div className="text-sm text-gray-600 flex gap-4">
            <span className="text-yellow-600">
              ⏳ Waiting: {games.filter((g) => g.status === "waiting").length}
            </span>
            <span className="text-blue-600">
              🎮 Playing:{" "}
              {games.filter((g) => g.status === "in_progress").length}
            </span>
            <span className="text-green-600">
              ✅ Completed:{" "}
              {games.filter((g) => g.status === "completed").length}
            </span>
          </div>
        </div>
        {loading && games.length === 0 && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-500">Loading games...</p>
          </div>
        )}{" "}
        {!loading && games.length === 0 && (
          <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
            <div className="text-4xl mb-4">🎮</div>
            <p className="text-gray-600 text-lg mb-2">
              No games found in the database
            </p>
            <p className="text-gray-500">
              Create the first game to get started!
            </p>
          </div>
        )}{" "}
        {games.length > 0 && (
          <div className="space-y-8">
            {/* Waiting Games Section */}
            {games.filter((g) => g.status === "waiting").length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-yellow-700 mb-3 flex items-center gap-2">
                  ⏳ Games Waiting for Players (
                  {games.filter((g) => g.status === "waiting").length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {games
                    .filter((g) => g.status === "waiting")
                    .map((game) => (
                      <div
                        key={game.id}
                        className="border border-yellow-200 bg-yellow-50 p-4 rounded-lg shadow-sm hover:shadow-md transition-all duration-200"
                      >
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <p className="font-semibold text-lg text-gray-800 flex items-center gap-2">
                              🎮 {game.host}
                              {game.host === username && (
                                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                  You
                                </span>
                              )}
                            </p>
                            <p className="text-xs text-gray-500">
                              ID: {game.id}
                            </p>
                          </div>
                        </div>

                        <div className="space-y-1 mb-3">
                          <p className="text-sm text-gray-500 flex items-center gap-1">
                            📅{" "}
                            {game.createdAt
                              ? new Date(game.createdAt).toLocaleString()
                              : "N/A"}
                          </p>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-600">
                              Players:
                            </span>
                            <div className="flex items-center gap-1">
                              <div className="w-2 h-2 rounded-full bg-green-500"></div>
                              <div className="w-2 h-2 rounded-full bg-gray-300"></div>
                              <span className="text-sm text-gray-600 ml-1">
                                1/2
                              </span>
                            </div>
                          </div>
                        </div>

                        <button
                          onClick={() => handleJoinGame(game.id)}
                          className={`w-full py-2 px-4 rounded-lg font-medium transition-colors ${
                            !username.trim() || loading
                              ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                              : "bg-indigo-500 hover:bg-indigo-600 text-white"
                          }`}
                          disabled={!username.trim() || loading}
                        >
                          🚀 Join Game
                        </button>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* In Progress Games Section */}
            {games.filter((g) => g.status === "in_progress").length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-blue-700 mb-3 flex items-center gap-2">
                  🎮 Games in Progress (
                  {games.filter((g) => g.status === "in_progress").length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {games
                    .filter((g) => g.status === "in_progress")
                    .map((game) => (
                      <div
                        key={game.id}
                        className="border border-blue-200 bg-blue-50 p-4 rounded-lg shadow-sm hover:shadow-md transition-all duration-200"
                      >
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <p className="font-semibold text-lg text-gray-800 flex items-center gap-2">
                              🎮 {game.host} vs {game.player_o}
                              {(game.host === username ||
                                game.player_o === username) && (
                                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                  {game.host === username
                                    ? "You (X)"
                                    : "You (O)"}
                                </span>
                              )}
                            </p>
                            <p className="text-xs text-gray-500">
                              ID: {game.id}
                            </p>
                          </div>
                        </div>

                        <div className="space-y-1 mb-3">
                          <p className="text-sm text-gray-500 flex items-center gap-1">
                            📅{" "}
                            {game.createdAt
                              ? new Date(game.createdAt).toLocaleString()
                              : "N/A"}
                          </p>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-600">Turn:</span>
                            <span className="text-sm font-medium text-blue-700">
                              Player {game.current_turn}
                            </span>
                          </div>
                        </div>

                        <button
                          onClick={() => handleJoinGame(game.id)}
                          className="w-full py-2 px-4 rounded-lg font-medium bg-blue-500 hover:bg-blue-600 text-white transition-colors"
                        >
                          👁️ Watch Game
                        </button>
                      </div>
                    ))}
                </div>
              </div>
            )}

            {/* Completed Games Section */}
            {games.filter((g) => g.status === "completed").length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-green-700 mb-3 flex items-center gap-2">
                  ✅ Completed Games (
                  {games.filter((g) => g.status === "completed").length})
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {games
                    .filter((g) => g.status === "completed")
                    .map((game) => (
                      <div
                        key={game.id}
                        className="border border-green-200 bg-green-50 p-4 rounded-lg shadow-sm hover:shadow-md transition-all duration-200"
                      >
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <p className="font-semibold text-lg text-gray-800 flex items-center gap-2">
                              🎮 {game.host} vs {game.player_o || "N/A"}
                              {(game.host === username ||
                                game.player_o === username) && (
                                <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                                  You
                                </span>
                              )}
                            </p>
                            <p className="text-xs text-gray-500">
                              ID: {game.id}
                            </p>
                          </div>
                          {game.host === username && (
                            <button
                              onClick={() => handleDeleteGame(game.id)}
                              className="text-red-500 hover:text-red-700 p-1 rounded hover:bg-red-50 transition-colors"
                              title="Delete game"
                            >
                              🗑️
                            </button>
                          )}
                        </div>

                        <div className="space-y-1 mb-3">
                          <p className="text-sm text-gray-500 flex items-center gap-1">
                            📅{" "}
                            {game.createdAt
                              ? new Date(game.createdAt).toLocaleString()
                              : "N/A"}
                          </p>
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-600">
                              Result:
                            </span>
                            <span
                              className={`text-xs px-2 py-1 rounded-full font-medium ${
                                game.is_draw
                                  ? "bg-gray-100 text-gray-800"
                                  : "bg-green-100 text-green-800"
                              }`}
                            >
                              {game.is_draw
                                ? "🤝 Draw"
                                : `🏆 ${game.winner} Won`}
                            </span>
                          </div>
                        </div>

                        <button
                          onClick={() => handleJoinGame(game.id)}
                          className="w-full py-2 px-4 rounded-lg font-medium bg-gray-500 hover:bg-gray-600 text-white transition-colors"
                        >
                          📋 View Results
                        </button>
                      </div>
                    ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Lobby;
