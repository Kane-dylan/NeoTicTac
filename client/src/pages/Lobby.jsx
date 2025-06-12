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
    } catch {
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
    } catch {
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
    <div className="min-h-screen bg-background-secondary">
      <div className="container mx-auto px-4 py-6 max-w-6xl">
        {/* Header Section */}
        <div className="card p-6 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-text-primary mb-2 flex items-center gap-3">
                🎮 Game Lobby
              </h1>
              <p className="text-text-secondary">
                Welcome back,{" "}
                <span className="font-medium text-text-primary">
                  {username || "Player"}
                </span>
                !
              </p>
            </div>
            <button
              className="bg-accent-error hover:bg-accent-error/90 text-text-inverse py-2 px-4 rounded-md font-medium transition-all duration-200 self-start"
              onClick={handleLogout}
            >
              🚪 Logout
            </button>
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

        {/* User Controls Section */}
        <div className="card p-6 mb-6">
          <h2 className="text-xl font-semibold text-text-primary mb-4 flex items-center gap-2">
            👤 Player Setup
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Username Input */}
            <div>
              <label className="block text-sm font-medium text-text-primary mb-2">
                Your Username:
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="input-field w-full"
                placeholder="Enter your username"
                maxLength={20}
              />
              <p className="text-xs text-text-muted mt-1">
                This name will be shown to other players
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col justify-end">
              <div className="flex flex-wrap gap-3">
                <button
                  onClick={handleCreateGame}
                  className="btn-primary flex items-center gap-2 px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                  disabled={!username.trim() || loading}
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-text-inverse border-t-transparent"></div>
                      Creating...
                    </>
                  ) : (
                    <>➕ Create New Game</>
                  )}
                </button>
                <button
                  onClick={fetchGames}
                  className="btn-secondary flex items-center gap-2 px-4 py-3"
                >
                  🔄 Refresh
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Games List Section */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-semibold text-text-primary flex items-center gap-2">
              🎯 Available Games
              <span className="bg-background-tertiary text-text-secondary px-3 py-1 rounded-full text-sm font-medium">
                {games.length}
              </span>
            </h2>
          </div>

          {/* Loading State */}
          {loading && games.length === 0 && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mx-auto mb-4"></div>
              <p className="text-text-secondary">Loading games...</p>
            </div>
          )}

          {/* Empty State */}
          {!loading && games.length === 0 && (
            <div className="text-center py-16 bg-background-tertiary rounded-lg">
              <div className="text-6xl mb-4">🎮</div>
              <h3 className="text-xl font-semibold text-text-primary mb-2">
                No games found
              </h3>
              <p className="text-text-secondary mb-6">
                Be the first to create a game and start playing!
              </p>
              <button
                onClick={handleCreateGame}
                className="btn-primary px-6 py-3 disabled:opacity-50 disabled:cursor-not-allowed"
                disabled={!username.trim() || loading}
              >
                ➕ Create First Game
              </button>
            </div>
          )}

          {/* Games Grid */}
          {games.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {games.map((game) => (
                <div
                  key={game.id}
                  className="card p-6 hover:shadow-lg transition-all duration-200 border-l-4 border-l-primary"
                >
                  {/* Game Header */}
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-text-primary text-lg">
                        🎮 {game.host}
                        {game.player_o && (
                          <span className="text-text-secondary">
                            {" "}
                            vs {game.player_o}
                          </span>
                        )}
                      </h3>
                      <span className="text-xs font-mono text-text-muted bg-background-tertiary px-2 py-1 rounded">
                        #{game.id}
                      </span>
                    </div>
                  </div>

                  {/* Game Status */}
                  <div className="mb-4 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-text-secondary">
                        Status:
                      </span>
                      <span
                        className={`text-sm font-medium px-2 py-1 rounded-full ${
                          game.status === "waiting"
                            ? "bg-accent-warning/10 text-accent-warning"
                            : game.status === "in_progress"
                            ? "bg-accent-info/10 text-accent-info"
                            : "bg-accent-success/10 text-accent-success"
                        }`}
                      >
                        {game.status === "waiting" && "🟡 Waiting"}
                        {game.status === "in_progress" && "🔵 In Progress"}
                        {game.status === "completed" && "🟢 Completed"}
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-text-secondary">
                        Players:
                      </span>
                      <span className="text-sm font-medium text-text-primary">
                        {game.playerCount}/2
                      </span>
                    </div>

                    {game.status === "completed" && (
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-text-secondary">
                          Result:
                        </span>
                        <span className="text-sm font-medium text-text-primary">
                          {game.is_draw ? "🤝 Draw" : `🏆 ${game.winner} Won`}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Join Button */}
                  <button
                    onClick={() => handleJoinGame(game.id)}
                    className="w-full py-3 px-4 rounded-md font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={!username.trim() || loading}
                    style={{
                      backgroundColor:
                        game.status === "waiting"
                          ? "var(--color-accent-success)"
                          : game.status === "in_progress"
                          ? "var(--color-accent-info)"
                          : "var(--color-secondary)",
                      color: "var(--color-text-inverse)",
                    }}
                  >
                    {game.status === "waiting" && "🚀 Join Game"}
                    {game.status === "in_progress" && "👀 Watch Game"}
                    {game.status === "completed" && "📊 View Results"}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Lobby;
