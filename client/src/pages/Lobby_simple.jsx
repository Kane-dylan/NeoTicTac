import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSocket } from "../context/SocketContext";
import { getAllGames, createGame } from "../services/api";

const Lobby = () => {
  const [games, setGames] = useState([]);
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { socket } = useSocket();
  const navigate = useNavigate();

  const fetchGames = async () => {
    setLoading(true);
    setError("");
    try {
      const allGames = await getAllGames();
      setGames(allGames);
    } catch (err) {
      setError("Failed to load games");
    } finally {
      setLoading(false);
    }
  };

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

    // Simple socket listeners
    if (socket) {
      socket.emit("join_lobby");
      socket.on("lobby_games_update", (data) => setGames(data.games || []));
      socket.on("game_created", (newGame) => {
        if (newGame?.id) setGames((prev) => [...prev, newGame]);
      });
    }

    return () => {
      if (socket) {
        socket.emit("leave_lobby");
        socket.off("lobby_games_update");
        socket.off("game_created");
      }
    };
  }, [socket, navigate]);

  const handleCreateGame = async () => {
    if (!username.trim()) {
      setError("Please enter a username first");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const response = await createGame();
      localStorage.setItem("username", username);
      if (response?.gameId) {
        navigate(`/game/${response.gameId}`);
      }
    } catch (err) {
      setError("Failed to create game");
    } finally {
      setLoading(false);
    }
  };

  const handleJoinGame = (gameId) => {
    if (!username.trim()) {
      setError("Please enter a username first");
      return;
    }
    localStorage.setItem("username", username);
    navigate(`/game/${gameId}`);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    if (socket) socket.disconnect();
    navigate("/");
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">🎮 Game Lobby</h1>
          <p className="text-gray-600">Welcome, {username || "Player"}!</p>
        </div>
        <button
          className="bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600"
          onClick={handleLogout}
        >
          Logout
        </button>
      </div>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4">{error}</div>
      )}

      <div className="mb-6 p-4 border rounded bg-white">
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">
            Your Username:
          </label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-3 border rounded focus:ring-2 focus:ring-blue-500"
            placeholder="Enter your username"
          />
        </div>

        <div className="flex gap-3">
          <button
            onClick={handleCreateGame}
            className="bg-green-500 text-white py-3 px-6 rounded hover:bg-green-600 disabled:bg-gray-400"
            disabled={!username.trim() || loading}
          >
            {loading ? "Creating..." : "Create New Game"}
          </button>
          <button
            onClick={fetchGames}
            className="bg-blue-500 text-white py-3 px-6 rounded hover:bg-blue-600"
          >
            Refresh Games
          </button>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-semibold mb-4">
          All Games ({games.length})
        </h2>

        {loading && games.length === 0 && (
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p>Loading games...</p>
          </div>
        )}

        {!loading && games.length === 0 && (
          <div className="text-center py-12 bg-gray-50 rounded">
            <div className="text-4xl mb-4">🎮</div>
            <p className="text-gray-600">No games found</p>
            <p className="text-gray-500">
              Create the first game to get started!
            </p>
          </div>
        )}

        {games.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {games.map((game) => (
              <div
                key={game.id}
                className="border p-4 rounded shadow hover:shadow-md transition"
              >
                <div className="mb-3">
                  <p className="font-semibold text-lg">
                    🎮 {game.host}
                    {game.player_o && ` vs ${game.player_o}`}
                  </p>
                  <p className="text-xs text-gray-500">ID: {game.id}</p>
                </div>

                <div className="mb-3">
                  <p className="text-sm text-gray-500">
                    Status: <span className="font-medium">{game.status}</span>
                  </p>
                  {game.status === "completed" && (
                    <p className="text-sm">
                      Result: {game.is_draw ? "Draw" : `${game.winner} Won`}
                    </p>
                  )}
                </div>

                <button
                  onClick={() => handleJoinGame(game.id)}
                  className="w-full py-2 px-4 rounded font-medium bg-blue-500 hover:bg-blue-600 text-white disabled:bg-gray-300"
                  disabled={!username.trim() || loading}
                >
                  {game.status === "waiting"
                    ? "Join Game"
                    : game.status === "in_progress"
                    ? "Watch Game"
                    : "View Results"}
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
