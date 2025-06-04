import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getActiveGames, createGame } from "../services/api";

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
      const activeGames = await getActiveGames();
      setGames(activeGames);
    } catch (err) {
      console.error("Failed to fetch games:", err);
      setError(
        err.response?.data?.msg || err.message || "Failed to load games."
      );
      setGames([]); // Clear games on error
    } finally {
      setLoading(false);
    }
  }, []); // Empty dependency array as getActiveGames is stable

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

    fetchGames();

    // Setup socket event handling with cleanup
    const setupSocketListeners = () => {
      if (!socket || !socket.connected) {

        return false;
      }

      // Join lobby room for real-time updates
      socket.emit("join_lobby");

      // Real-time lobby updates
      socket.on("lobby_games_update", (data) => {

        setGames(data.games || []);
      });

      socket.on("game_created", (newGame) => {
        if (newGame && newGame.id) {
          setGames((prevGames) => [...prevGames, newGame]);
        }
      });

      socket.on("game_started", (data) => {

        setGames((prevGames) =>
          prevGames.filter((game) => game.id !== data.game_id)
        );
      });      socket.on("game_completed", () => {
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

      // Connection status indicators
      socket.on("connect", () => {
        setError("");
        fetchGames(); // Refresh on reconnect
      });

      socket.on("disconnect", () => {
        setError("Connection lost. Attempting to reconnect...");
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
      if (socket) {        try {
          socket.emit("leave_lobby");        } catch {
          // Error leaving lobby - continue cleanup
        }

        // Clean up event listeners
        const events = [
          "lobby_games_update",
          "game_created",
          "game_started",
          "game_completed",
          "player_count_updated",
          "connect",
          "disconnect",
        ];

        events.forEach((event) => {          try {
            socket.off(event);          } catch {
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

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Game Lobby</h1>
        <button
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>

      {error && (
        <div
          className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4"
          role="alert"
        >
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      <div className="mb-6 p-4 border rounded shadow-sm bg-white">
        <div className="mb-4">
          <label
            htmlFor="usernameInput"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Your Username:
          </label>
          <input
            id="usernameInput"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded shadow-sm focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter your username"
          />
        </div>

        <div className="flex space-x-3">
          <button
            onClick={handleCreateGame}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded disabled:bg-gray-400"
            disabled={!username.trim() || loading}
          >
            {loading ? "Creating..." : "Create New Game"}
          </button>
          <button
            onClick={fetchGames}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:bg-gray-400"
            disabled={loading}
          >
            {loading ? "Refreshing..." : "Refresh Games"}
          </button>
        </div>
      </div>

      <div>
        <h2 className="text-xl font-semibold mb-3 text-gray-700">
          Available Games
        </h2>
        {loading && games.length === 0 && (
          <p className="text-gray-500">Loading games...</p>
        )}
        {!loading && games.length === 0 && (
          <p className="text-gray-500">No active games. Create one!</p>
        )}
        {games.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {games.map((game) => (
              <div
                key={game.id}
                className="border p-4 rounded shadow bg-white hover:shadow-lg transition-shadow"
              >
                <p className="font-semibold text-lg text-gray-800">
                  Host: {game.host}
                </p>
                <p className="text-sm text-gray-500">Game ID: {game.id}</p>
                <p className="text-sm text-gray-500">
                  Created:{" "}
                  {game.createdAt
                    ? new Date(game.createdAt).toLocaleString()
                    : "N/A"}
                </p>
                <p className="text-sm text-gray-600">
                  Players: {game.playerCount || 1}/2
                </p>
                <button
                  onClick={() => handleJoinGame(game.id)}
                  className="mt-3 w-full bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded disabled:bg-gray-400"
                  disabled={
                    !username.trim() || game.playerCount >= 2 || loading
                  }
                >
                  {game.playerCount >= 2 ? "Game Full" : "Join Game"}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Lobby;
